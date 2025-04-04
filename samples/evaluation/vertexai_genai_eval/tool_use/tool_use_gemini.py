from google import genai
from google.genai.types import GenerateContentConfig
import json
from vertexai.evaluation import EvalTask
from vertexai.evaluation.constants import Metric
import logging
import requests
import pandas
import sys

sys.path.append("../../../../")
from samples.evaluation.vertexai_genai_eval.utils import print_eval_result

# An example on how you can setup 2 functions for automatic function calling in Gemini,
# use those functions from a prompt, and then evaluate the function call results with the Gen AI evaluation service. It
# involves getting the function call history, converting it to the format Gen AI evaluation service expects and running
# the evaluation.
# See: https://cloud.google.com/vertex-ai/generative-ai/docs/models/determine-eval#tool-use

PROMPT = "What's the temperature, wind, humidity like in London, Paris?"
PROJECT_ID = "genai-atamel"
LOCATION = "us-central1"
MODEL_ID = "gemini-2.0-flash-001"

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
    """Given a location, returns the latitude and longitude

    Args:
        location: The location for which to get the weather.

    Returns:
        The latitude and longitude information in JSON.
    """
    logger.info(f"Calling location_to_lat_long({location})")
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
    return api_request(url)


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

def generate_content_with_function_calls():
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION)

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=PROMPT,
        config=GenerateContentConfig(
            system_instruction=[
                "You are a helpful weather assistant.",
                "Your mission is to provide weather information for different cities."
                "Make sure your responses are in plain text format (no markdown) and include all the cities asked.",
            ],
            tools=[location_to_lat_long, lat_long_to_weather],
            temperature=0),
    )

    print(f"Response text: {response.text}")
    print(f"Automatic function calling history: {response.automatic_function_calling_history}")
    return response


def convert_function_calling_history_for_eval(automatic_function_calling_history):
    function_calls = []
    for item in automatic_function_calling_history:
        if item.role == 'model':
            for part in item.parts:
                if part.function_call:
                    output_format = {
                        "content": "",
                        "tool_calls": [
                            {
                                "name": part.function_call.name,
                                "arguments": part.function_call.args
                            }
                        ]
                    }
                    function_calls.append(output_format)
    return function_calls


def evaluate_function_calling(automatic_function_calling_history):
    converted_function_calling_history = convert_function_calling_history_for_eval(automatic_function_calling_history)
    print(f"Converted function calling history: {converted_function_calling_history}")

    references = [
        {
            "content": "",
            "tool_calls": [
                {
                    "name": "location_to_lat_long",
                    "arguments": {
                        "location": "London"
                    }
                }
            ]
        },
        {
            "content": "",
            "tool_calls": [
                {
                    "name": "location_to_lat_long",
                    "arguments": {
                        "location": "Paris"
                    }
                }
            ]
        },
        {
            "content": "",
            "tool_calls": [
                {
                    "name": "lat_long_to_weather",
                    "arguments": {
                        "longitude": "-0.12574",
                        "latitude": "51.50853"
                    }
                }
            ]
        },
        {
            "content": "",
            "tool_calls": [
                {
                    "name": "lat_long_to_weather",
                    "arguments": {
                        "longitude": "2.3488",
                        "latitude": "48.85341"
                    }
                }
            ]
        },
    ]
    print(f"References: {references}")

    eval_dataset = pandas.DataFrame(
        {
            "response": [json.dumps(history) for history in converted_function_calling_history],
            "reference": [json.dumps(reference) for reference in references],
        }
    )

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[
            Metric.TOOL_CALL_VALID,
            Metric.TOOL_NAME_MATCH,
            Metric.TOOL_PARAMETER_KEY_MATCH,
            Metric.TOOL_PARAMETER_KV_MATCH
        ],
        experiment="tool-use-gemini"
    )

    eval_result = eval_task.evaluate()
    print_eval_result(eval_result)

def main():
    #logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    response = generate_content_with_function_calls()
    evaluate_function_calling(response.automatic_function_calling_history)

if __name__ == '__main__':
    main()
