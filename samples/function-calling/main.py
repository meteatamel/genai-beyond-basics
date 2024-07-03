import argparse
import logging
import requests
import vertexai
from vertexai.generative_models import (
    Content, FunctionDeclaration, GenerationConfig, GenerativeModel, Part, Tool
)

logger = logging.getLogger(__name__)


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


def lat_long_to_weather(latitude: str, longitude: str):
    logger.debug(f"Calling lat_long_to_weather({latitude}, {longitude})")
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,"
           f"relative_humidity_2m,surface_pressure,wind_speed_10m,wind_direction_10m&forecast_days=1")
    return api_request(url)


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

    tool = create_tool_with_function_declarations()

    # Define a contents list that can be reused in model calls
    contents = [Content(role="user", parts=[Part.from_text(prompt)])]

    while True:
        response = model.generate_content(
            contents,
            generation_config=GenerationConfig(temperature=0),
            tools=[tool],
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
    if function_call.name == location_to_lat_long.__name__:
        return location_to_lat_long(function_call.args["location"])
    elif function_call.name == lat_long_to_weather.__name__:
        return lat_long_to_weather(function_call.args["latitude"], function_call.args["longitude"])
    else:
        raise ValueError(f"Unknown function: {function_call.name}")


def get_args_parser():
    parser = argparse.ArgumentParser(description="Parallel function calls")

    parser.add_argument('--project_id', type=str, required=True, help='Google Cloud project id (required)')
    parser.add_argument('--prompt', type=str, required=True, help='Prompt')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging (default: False)')

    parser.add_argument('--google_search_grounding', action='store_true',
                        help='Use Vertex AI Google Search grounding (default: False)')

    return parser.parse_args()


def setup_logging_level(debug=False):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format='%(message)s')


def main():
    args = get_args_parser()
    setup_logging_level(args.debug)
    vertexai.init(project=args.project_id, location="us-central1")
    generate_content_with_function_calls(args.prompt)


if __name__ == '__main__':
    main()
