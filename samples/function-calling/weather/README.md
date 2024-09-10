# Function calling - Weather

## Introduction

In this sample, you'll deep dive into function calling in Gemini. More specifically, you'll see how to handle multiple and
parallel function call requests from `generate_content` and `chat` interfaces and take a look at the new magical auto
function calling feature through a sample weather application.

## What is function calling?

[Function Calling](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling) is useful to augment LLMs with more up-to-date data via external API calls. 

You can use function calling to define custom functions and provide these to an LLM. While processing a prompt, 
the LLM can choose to delegate tasks to the functions that you identify. The model does not call the functions directly
but rather makes function call requests with parameters. Your application code responds to function call
requests by calling external APIs and providing the responses back to the model, allowing the LLM to complete its
response to the prompt. 

![Function calling](https://cloud.google.com/static/vertex-ai/generative-ai/docs/multimodal/images/function-calling.png)

## The problem

The question we want the model to answer is: 

`What's the temperature, wind, humidity like in London, Tokyo, Paris?`

Since this question requires realtime data, the model cannot answer it. However, the model can use public APIs to get
the data it needs via the function calling requests.

The question requires:

1. A weather API to get weather data for a location. Most weather APIs require a certain latitude and longitude.
1. A geocoding API to go from a city name to a latitude and a longitude for the weather API.
1. Answers for multiple cities. That means we can take advantage of the parallel function calling feature of Gemini.

Let's get started!

## Weather application

For the weather application powered by function calls and the model, you'll need to: 

1. Define a function to use a geocoding API to locate the latitude and longitude of a city.
1. Define a function to use a weather API to get the weather information for a latitude and longitude.
1. Register both functions in a tool for the LLM.
1. Use the tool to generate a response from the LLM with multiple function calls, some in parallel.
1. Ask the LLM about the weather from multiple cities and observe how LLM responds with function calls.

The full code is in [main.py](./main.py). Let's go through it. 

## Geocoding function

First, let's define a helper method to make API calls: 

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
```

Then, define a geocoding function called `location_to_lat_long`. Note how we properly documented the function. This will be 
important later when we do function declarations for the model:

```python
def location_to_lat_long(location: str):
    """Given a location, returns the latitude and longitude

    Args:
        location: The location for which to get the weather.

    Returns:
        The latitude and longitude information in JSON.
    """
    logger.info(f"Calling location_to_lat_long({location})")
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
    return api_request(url)
```

This function uses [Open Meteo](https://open-meteo.com/), an open source weather/geocoding API, and it returns a JSON with latitude and 
longitude of a given location:  

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

Next, define a weather function called `lat_long_to_weather`. Again note the proper documentation for the LLM:

```python
def lat_long_to_weather(latitude: str, longitude: str):
    """Given a latitude and longitude, returns the weather information

    Args:
        latitude: The latitude of a location
        longitude: The longitude of a location

    Returns:
        The weather information for the location in JSON.
    """
    logger.info(f"Calling lat_long_to_weather({latitude}, {longitude})")
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

Note that we're not doing any special processing of the JSON. We simply return the full JSON to the model and hope that
it will know what to do!

## Create a tool

Now that the two functions are ready, create a tool where we describe each function. There are 2 ways of doing this. 

The first one is create function declarations explicitly providing description and parameters manually:

```python
def create_weather_tool_with_declarations():
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

The second and easier way is to use `FunctionDeclaration.from_func` method to get a function declaration for the LLM. This
is when the public documentation of the methods are crucial to give enough hints to the model:

```python
def create_weather_tool():
    return Tool(
        function_declarations=[
            FunctionDeclaration.from_func(location_to_lat_long),
            FunctionDeclaration.from_func(lat_long_to_weather)
        ],
    )
```

## Create a model with the tool

Now, you create the model with the tool:

```python
def create_model_with_tool():
    return GenerativeModel(
        model_name="gemini-1.5-pro-001",
        system_instruction=[
            "You are a helpful weather assistant.",
            "Your mission is to provide weather information for different cities."
            "Make sure your responses are plain text format and include all the cities asked.",
        ],
        generation_config=GenerationConfig(temperature=0),
        tools=[create_weather_tool()]
    )
```

## Multiple and parallel function call requests

We're ready to generate some content but let's talk about multiple and parallel function call requests first.

The model can request one or more different function calls in sequence. For example, `location_to_lat_long("London")` 
followed by `lat_long_to_weather("London")`. If we're using `generate_content` method, we need to handle these requests
and append both the function requests and also the function responses in our response contents. If you're using `chat`
interface, it handles this for you with its session.

In the recent versions of Gemini, model can also request two or more function calls in parallel. In our sample, the model
can request `lat_long_to_weather("London")` and `lat_long_to_weather("Paris")` in a single response. 

Note that, the model doesn't have to request parallel calls, but it can, so you need to design your code accordingly.

![Parallel function calling](https://camo.githubusercontent.com/c5e9118987bbb4d5f4aab90f326a8b34c798f909a932c07a25fcf3c7c888cb89/68747470733a2f2f73746f726167652e676f6f676c65617069732e636f6d2f6769746875622d7265706f2f67656e657261746976652d61692f67656d696e692f66756e6374696f6e2d63616c6c696e672f706172616c6c656c2d66756e6374696f6e2d63616c6c696e672d696e2d67656d696e692e706e67)

## Generate content with function calls

Given these points, this is the code we need with the `generate_content` method. Note how we're keeping track of contents
and appending function responses before sending the contents list back to the model: 

```python
def generate_content_with_function_calls(prompt: str):
    model = create_model_with_tool()

    # Define a contents list that can be reused in model calls
    contents = [Content(role="user", parts=[Part.from_text(prompt)])]

    logger.info(f"Prompt: {prompt}")
    response = model.generate_content(contents)
    logger.debug(f"Response: {response}")

    while response.candidates[0].function_calls:

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

        response = model.generate_content(contents)
        logger.debug(f"Response: {response}")

    logger.info(f"Response: {response.text}")
```

We also have a helper method to handle function call requests. It looks up the name in the function call request and 
calls the actual function with the parameters supplied by the model:

```python
def handle_function_call(function_call):
    function = globals().get(function_call.name)
    if function and callable(function):
        return function(**function_call.args)
    else:
        raise ValueError(f"Unknown function: {function_call.name}")
```

We're ready to run the sample:

```shell
python main.py --project_id genai-atamel \
  --prompt "What's the temperature, wind, humidity like in London, Paris, Tokyo?" \
  generate_content
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
  --prompt "What's the temperature, wind, humidity like in Mumbai, Seoul, Jakarta?" \
  --debug
  generate_content
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

## Chat with function calls

If you use the `chat` interface, function calling gets a little bit easier because the chat session keeps track of the
contents, so you don't have to. However, you still have to handle parallel function calls. The code looks like this:

```python
def chat_with_function_calls(prompt: str):
    model = create_model_with_tool()

    logger.info(f"Prompt: {prompt}")
    chat = model.start_chat()
    response = chat.send_message(prompt)
    logger.debug(f"Response: {response}")

    while response.candidates[0].function_calls:

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

        response = chat.send_message(function_response_parts)
        logger.debug(f"Response: {response}")

    logger.info(f"Response: {response.text}")
```

Run the sample:

```shell
python main.py --project_id genai-atamel \
  --prompt "What's the temperature, wind, humidity like in London, Paris, Tokyo?" \
  chat
```

You get a similar response:

```log
Prompt: What's the temperature, wind, humidity like in London, Paris, Tokyo?
Calling location_to_lat_long(London)
Calling location_to_lat_long(Paris)
Calling location_to_lat_long(Tokyo)
Calling lat_long_to_weather(51.50853, -0.12574)
Calling lat_long_to_weather(48.85341, 2.3488)
Calling lat_long_to_weather(35.6895, 139.69171)
Response: The current weather in London is 19.5°C with a wind speed of 10.8 km/h and 76% humidity. 
In Paris, it is 26.1°C with a wind speed of 14.5 km/h and 36% humidity. 
Tokyo has a temperature of 26°C, a wind speed of 4.1 km/h, and 93% humidity. 
```

## Chat with auto function calls

Last but not least, there's a new feature in the `chat` interface where the library automatically calls your functions, 
so you don't have to. This greatly simplifies the code.

To use this feature, you need to import the preview libraries:

```python
from vertexai.preview.generative_models import (
    AutomaticFunctionCallingResponder, GenerativeModel
)
```

Then, start a chat with `AutomaticFunctionCallingResponder`. This is the class that will handle calling back to your
local functions. Note the `max_automatic_function_calls` parameter. You need to somehow guess the number of automatic 
function calls you'll need but once that's specified, there's nothing else you need to do in your code. No tracking of 
function call requests to functions, no need to worry about parallel function calls. This is much simpler!

```python
def chat_with_auto_function_calls(prompt: str):
    model = create_model_with_tool()

    logger.info(f"Prompt: {prompt}")
    chat = model.start_chat(responder=AutomaticFunctionCallingResponder(max_automatic_function_calls=10))
    response = chat.send_message(prompt)
    logger.info(f"Response: {response.text}")
```

Run the sample:

```shell
python main.py --project_id your-project-id \
  --prompt "What's the temperature, wind, humidity like in London, Paris, Tokyo?" \
  chat_auto
```

You get a similar response but with much simpler code to maintain!

```log
Prompt: What's the temperature, wind, humidity like in London, Paris, Tokyo?
Calling location_to_lat_long(London)
Calling location_to_lat_long(Paris)
Calling location_to_lat_long(Tokyo)
Calling lat_long_to_weather(51.50853, -0.12574)
Calling lat_long_to_weather(48.85341, 2.3488)
Calling lat_long_to_weather(35.6895, 139.69171)
Response: The current weather in London is 19.5°C with a wind speed of 10.8 km/h and 76% humidity. 
In Paris, it is 26.1°C with a wind speed of 14.5 km/h and 36% humidity. 
Tokyo has a temperature of 26°C, a wind speed of 4.1 km/h, and 93% humidity. 
```

## References

* [Documentation: Function calling](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling)
* [Codelab: How to Interact with APIs Using Function Calling in Gemini](https://codelabs.developers.google.com/codelabs/gemini-function-calling)
* [Notebooks: Function calling](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/function-calling)
* [Sample: function_calling.py](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/4282aa905763af06354225ae0f422c09201b41da/generative_ai/function_calling.py)