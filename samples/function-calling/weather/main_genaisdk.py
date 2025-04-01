from google import genai
from google.genai.types import GenerateContentConfig, AutomaticFunctionCallingConfig
import logging
import requests

# Automatic function calling with the Google Gen AI SDK for Python

logger = logging.getLogger(__name__)

PROMPT = "What's the temperature, wind, humidity like in London, Paris, Tokyo?"
PROJECT_ID = "genai-atamel"
LOCATION = "us-central1"
MODEL_ID = "gemini-2.0-flash-001"

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
            #automatic_function_calling=AutomaticFunctionCallingConfig(disable=True),
            temperature=0),
    )

    print(response.text)
    #print(response.automatic_function_calling_history)


def main():
    #logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    generate_content_with_function_calls()

if __name__ == '__main__':
    main()
