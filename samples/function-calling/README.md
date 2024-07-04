# Function calling

[Function Calling](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling) is useful to augment
LLMs with more up-to-date data via external API calls. 

You can use function calling to define custom functions and provide these to an LLM. While processing a prompt, 
the LLM can choose to delegate tasks to the functions that you identify. The model does not call the functions directly
but rather makes function call requests with parameters. Your application code responds to function call
requests by calling external APIs and providing the responses back to the model, allowing the LLM to complete its
response to the prompt. 

![Function calling](https://cloud.google.com/static/vertex-ai/generative-ai/docs/multimodal/images/function-calling.png)

In this sample, you'll learn how to use function calling for multiple and parallel functions 
through the sample [main.py](./main.py). 

More specifically, you'll:

1. Define a function to use a geocoding API to locate the latitude and longitude of a city.
1. Define a function to use a weather API to get the weather information for a latitude and longitude.
1. Register both functions in a tool for the LLM.
1. Use the tool to generate a response from the LLM with multiple function calls, some in parallel.
1. Ask the LLM about the weather from single and multiple cities and observe how LLM responds with function calls.

## Introduction

The question we want LLM to answer is: 

`What's the temperature, wind, humidity like in London, Tokyo, Paris?`

The question requires:

1. A weather API. Most weather APIs work for a certain latitude and longitude.
1. A geocoding API to go from a city name to a latitude and a longitude for the weather API.
1. Answers for multiple cities. That means we can take advantage of the parallel function
   calling feature of Gemini.  

## Geocoding function

First, let's define a geocoding function called `location_to_lat_long`. 

```python
def api_request(url):
    logger.debug(f"Making a request to: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logger.debug(f"Response: {data}")
        return data
    except requests.exceptions.HTTPError as err:
        logger.error(f"HTTP error occurred: {err}")
    except Exception as err:
        logger.error(f"Other error occurred: {err}")


def location_to_lat_long(location: str):
    logger.debug(f"Calling location_to_lat_long({location})")
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
    return api_request(url)
```

This function uses [Open Meteo](https://open-meteo.com/), an open source weather/geocoding API, and it simply returns 
a JSON with latitude and longitude of a given location:  

```json
{
  "results": [
    {
      "id": 2643743,
      "name": "London",
      "latitude": 51.50853,
      "longitude": -0.12574,
      "elevation": 25.0,
      "feature_code": "PPLC",
      "country_code": "GB",
      "admin1_id": 6269131,
      "admin2_id": 2648110,
      "timezone": "Europe/London",
      "population": 7556900,
      "country_id": 2635167,
      "country": "United Kingdom",
      "admin1": "England",
      "admin2": "Greater London"
    }
  ],
  "generationtime_ms": 0.73099136
}
```

## Weather function

Next, let's define a weather function called `lat_long_to_weather`:

```python
def lat_long_to_weather(latitude: str, longitude: str):
    logger.debug(f"Calling lat_long_to_weather({latitude}, {longitude})")
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,"
           f"relative_humidity_2m,surface_pressure,wind_speed_10m,wind_direction_10m&forecast_days=1")
    return api_request(url)
```

This uses Open Meteo's forecast API for a given latitude and longitude and returns a JSON with the forecast:

```json
{
  "latitude": 51.5,
  "longitude": -0.120000124,
  "generationtime_ms": 0.051021575927734375,
  "utc_offset_seconds": 0,
  "timezone": "GMT",
  "timezone_abbreviation": "GMT",
  "elevation": 23.0,
  "current_units": {
    "time": "iso8601",
    "interval": "seconds",
    "temperature_2m": "°C",
    "relative_humidity_2m": "%",
    "surface_pressure": "hPa",
    "wind_speed_10m": "km/h",
    "wind_direction_10m": "°"
  },
  "current": {
    "time": "2024-07-03T08:30",
    "interval": 900,
    "temperature_2m": 14.4,
    "relative_humidity_2m": 77,
    "surface_pressure": 1007.4,
    "wind_speed_10m": 9.1,
    "wind_direction_10m": 187
  }
}
```

## Tool

Now that the two functions are ready, let's now create a tool where we describe each function and their parameters.
We'll pass this tool to the LLM later, so it's crucial that you give good descriptions for the function and parameters: 

```python
def create_tool_with_function_declarations():
    return Tool(
        function_declarations=[
            FunctionDeclaration(
                name=location_to_lat_long.__name__,
                description="Given a location name, return the latitude and the longitude",
                parameters={
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "Location to search the latitude and longitude for",
                        }
                    }
                }
            ),
            FunctionDeclaration(
                name=lat_long_to_weather.__name__,
                description="Given a latitude and longitude, return the weather information",
                parameters={
                    "type": "object",
                    "properties": {
                        "latitude": {
                            "type": "string",
                            "description": "The latitude of the location",
                        },
                        "longitude": {
                            "type": "string",
                            "description": "The longitude of the location",
                        }
                    }
                }
            )
        ],
    )
```

## Define model

Now, we're ready to generate content with function calls.

First, define the model with some system instructions:

```python
def generate_content_with_function_calls(prompt: str):
    logger.info(f"Prompt: {prompt}")

    model = GenerativeModel(
        model_name="gemini-1.5-pro-001",
        system_instruction=[
            "You are a helpful weather assistant.",
            "Your mission is to provide weather information for different cities."
            "Make sure your responses are plain text format and include all the cities asked.",
        ]
    )
```

Next, create a tool with our function declarations and also a content list with the first prompt:

```python
    tool = create_tool_with_function_declarations()

    # Define a contents list that can be reused in model calls
    contents = [Content(role="user", parts=[Part.from_text(prompt)])]
```

We're ready to generate some content but first let's talk about function calls.

## Multiple function calls

The model can request one or more different function calls in sequence. For example, `location_to_lat_long("London")` 
followed by `lat_long_to_weather("London")`. We need to handle these requests in order and append both the function 
request and also the function responses in contents.

## Parallel function calls

The recent versions of Gemini has the ability to return two or more function calls in parallel
(i.e., two or more function call responses within the first function call response object). 
Parallel function calling allows you to fan out and parallelize your API calls, so you don't have to do each API call
one-by-one. Note that, the model doesn't have to request parallel calls but it can, so you need to design your code accordingly.

![Parallel function calling](https://camo.githubusercontent.com/c5e9118987bbb4d5f4aab90f326a8b34c798f909a932c07a25fcf3c7c888cb89/68747470733a2f2f73746f726167652e676f6f676c65617069732e636f6d2f6769746875622d7265706f2f67656e657261746976652d61692f67656d696e692f66756e6374696f6e2d63616c6c696e672f706172616c6c656c2d66756e6374696f6e2d63616c6c696e672d696e2d67656d696e692e706e67)

In our sample, the model can request `lat_long_to_weather("London")` and `lat_long_to_weather("Paris")` in a single response. 

## Generate content with function calls

Given these points, this is the code we need:

```python
    while True:
        response = model.generate_content(
            contents,
            generation_config=GenerationConfig(temperature=0),
            tools=[weather_tool],
        )
        logger.debug(f"Response: {response}")

        # Exit the loop if there are no more function calls
        if not response.candidates[0].function_calls:
            break

        # Add the function call request to the contents
        contents.append(response.candidates[0].content)

        # You can have parallel function call requests for the same function type.
        # For example, 'location_to_lat_long("London")' and 'location_to_lat_long("Paris")'
        # In that case, collect API responses in parts and send them back to the model
        function_response_parts = []

        for function_call in response.candidates[0].function_calls:
            api_response = handle_function_call(function_call)
            function_response_parts.append(
                Part.from_function_response(
                    name=function_call.name,
                    response={"contents": api_response}
                )
            )

        # Add the function call response to the contents
        contents.append(Content(role="user", parts=function_response_parts))

    logger.info(f"Response: {response.text}")
    return response.text


def handle_function_call(function_call):
    function = globals().get(function_call.name)
    if function and callable(function):
        return function(**function_call.args)
    else:
        raise ValueError(f"Unknown function: {function_call.name}")
```

## Run

We're finally ready to run the sample. Let's start with a single city:

```shell
python main.py --project_id your-project-id --prompt "What's the temperature, wind, humidity like in London?"
```

You can see that there were calls to our 2 functions and the final response from the model:

```log
Prompt: What's the temperature, wind, humidity like in London?
Calling location_to_lat_long(London)
Calling lat_long_to_weather(51.50853, -0.12574)
Response: The temperature in London is 16°C, the wind speed is 16.9 km/h, and the humidity is 48%.
```

Now, let's try with multiple cities:

```shell
python main.py --project_id your-project-id \
  --prompt "What's the temperature, wind, humidity like in London, Paris, Tokyo?"
```

We get multiple function calls and a final response:

```log
Prompt: What's the temperature, wind, humidity like in London, Paris, Tokyo?
Calling location_to_lat_long(London)
Calling location_to_lat_long(Paris)
Calling location_to_lat_long(Tokyo)
Calling lat_long_to_weather(51.50853, -0.12574)
Calling lat_long_to_weather(48.85341, 2.3488)
Calling lat_long_to_weather(35.6895, 139.69171)
Response: The current weather in London is 16 degrees Celsius, wind speed is 16.9 km/h, humidity is 48%. 
The current weather in Paris is 18.1 degrees Celsius, wind speed is 15.5 km/h, humidity is 59%. 
The current weather in Tokyo is 30.9 degrees Celsius, wind speed is 2.9 km/h, humidity is 68%. 
```

To see what happens under the covers, let's now enable the `--debug` flag:

```shell
python main.py --project_id genai-atamel \
  --prompt "What's the temperature, wind, humidity like in Mumbai, Seoul, Jakarta?" --debug
```

You can see that you get parallel function requests sometimes:

```log
Response: candidates {
  content {
    role: "model"
    parts {
      function_call {
        name: "location_to_lat_long"
        args {
          fields {
            key: "location"
            value {
              string_value: "Mumbai"
            }
          }
        }
      }
    }
    parts {
      function_call {
        name: "location_to_lat_long"
        args {
          fields {
            key: "location"
            value {
              string_value: "Seoul"
            }
          }
        }
      }
    }
    parts {
      function_call {
        name: "location_to_lat_long"
        args {
          fields {
            key: "location"
            value {
              string_value: "Jakarta"
            }
          }
        }
      }
    }
  }
```

But other times, you might still get sequential function calls. It's up to the model to decide:

```log
Response: candidates {
  content {
    role: "model"
    parts {
      function_call {
        name: "location_to_lat_long"
        args {
          fields {
            key: "location"
            value {
              string_value: "Mumbai"
            }
          }
        }
      }
    }
  }
  ...
Response: candidates {
  content {
    role: "model"
    parts {
      function_call {
        name: "location_to_lat_long"
        args {
          fields {
            key: "location"
            value {
              string_value: "Seoul"
            }
          }
        }
      }
    }
  }
...
Response: candidates {
  content {
    role: "model"
    parts {
      function_call {
        name: "location_to_lat_long"
        args {
          fields {
            key: "location"
            value {
              string_value: "Jakarta"
            }
          }
        }
      }
    }
  }
```

## References

* [Documentation: Function calling](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling)
* [Codelab: How to Interact with APIs Using Function Calling in Gemini](https://codelabs.developers.google.com/codelabs/gemini-function-calling)
* [Notebooks: Function calling](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/function-calling)
* [Sample: function_calling.py](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/4282aa905763af06354225ae0f422c09201b41da/generative_ai/function_calling.py)