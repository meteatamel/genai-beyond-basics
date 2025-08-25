# Weather Agent

## Introduction

This agent provides weather information to the traveler. It has a couple of functions that use a weather API to get the
latitude and longitude of a location and then retrieve the weather information for that latitude and longitude. These
functions are used as tools in the agent.

Take a look at the [agent.py](agent.py) for details. 

## Run agent - terminal

Outside the folder of the agent use `adk run`:

```shell
adk run ./weather
```

Ask about weather for different cities:

```shell
user: How's the weather in Dubai?
[weather_agent]: For the next 7 days, the weather in Dubai will be:
* Temperature: Min temperature between 21.1-24.5°C and Max temperature between 29.4-40.9°C
* Rain: There is 0 rain
* Wind: Max wind speed between 16-29.3km/h
* UV index: Max UV index between 8.3-8.7
```

---

Go back to [Travel Helper Agent - sub-agents](../README.md) to continue building the rest of the agents.