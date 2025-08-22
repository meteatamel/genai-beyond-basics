from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from travel_helper.sub_agents.weather.agent import root_agent as weather_agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH

instruction_prompt = """
    You're an agent to provide currency and weather information for upcoming travel.
    - For any currency conversion questions, use `currency_agent`.
    - For any weather questions, use `weather_agent`.
 """

# Currency agent is a remote agent available over A2A
currency_agent = RemoteA2aAgent(
    name="currency_agent",
    description="Agent that can convert from one currency to another.",
    agent_card=f"http://localhost:8001/{AGENT_CARD_WELL_KNOWN_PATH}"
    # This does not seem to work due to this bug [2405](https://github.com/google/adk-python/issues/2405)
    #agent_card=f"https://a2a-currency-agent-207195257545.us-central1.run.app/{AGENT_CARD_WELL_KNOWN_PATH}"
)

root_agent = Agent(
    name="travel_helper_agent",
    model="gemini-2.0-flash",
    description="Agent to provide currency and weather information for upcoming travel.",
    instruction=instruction_prompt,
    tools=[
        AgentTool(agent=weather_agent),
        AgentTool(agent=currency_agent)
    ]
)