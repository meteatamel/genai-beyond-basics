import logging
import os
import requests
from google.adk.agents import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

logger = logging.getLogger(__name__)

def convert_currency(from_currency: str,  to_currency: str):
    """Given a from and to currency, returns the converted amount.

    Args:
        from_currency: The currency to convert from.
        to_currency: The currency to convert to.

    Returns:
        The converted amount in the to_currency or None if the conversion failed.
    """
    logger.debug(f"from_currency: {from_currency}, to_currency: {to_currency}")

    url = f"https://api.frankfurter.dev/v1/latest?base={from_currency}&symbols={to_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logger.debug(f"Response: {data}")
        return data['rates'][to_currency]
    except requests.exceptions.HTTPError as err:
        logger.error(f"HTTP error occurred: {err}")
        return None
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        return None


instruction_prompt = """
    You're a currency agent that can convert from one currency to another.
    Make sure you always use the convert_currency tool to answer the question.
    Don't ask for clarifications, just convert what you think is correct and output in this sample format:
    X British Pounds (GBP) = Y Euros (EUR)
    If you don't have the conversion information, just say "I'm sorry, I cannot convert from X to Y"
"""

root_agent = Agent(
    name="currency_agent",
    model="gemini-2.0-flash",
    description="Agent to convert from one currency to another.",
    instruction=instruction_prompt,
    tools=[convert_currency]
)

# Expose the agent over A2A protocol
a2a_app = to_a2a(root_agent, port=int(os.getenv('PORT', '8001')))
#a2a_app = to_a2a(root_agent, host="a2a-currency-agent-207195257545.us-central1.run.app", port=int(os.getenv('PORT', '8001')))