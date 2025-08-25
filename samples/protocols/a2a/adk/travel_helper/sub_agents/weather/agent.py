from google.adk.agents import Agent
import logging
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def api_request(url):
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
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,"
           f"temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_sum,precipitation_probability_max,wind_speed_10m_max")
    return api_request(url)


instruction_prompt = """
    You're a weather agent that can answer user questions about the weather in a city. Make sure to answer in this format:
    For the next 7 days, the weather in <city> will be:
    * Temperature: 
    * Rain: 
    * Wind: 
    * UV index: 
"""

root_agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",
    description="Agent to answer questions about weather in a city.",
    instruction=instruction_prompt,
    tools=[location_to_lat_long, lat_long_to_weather]
)