# Filesystem Assistant Agent with Model Context Protocol

## Introduction

The Model Context Protocol (MCP) is an open standard to standardize how LLMs communicate with external applications,
data sources and tools. MCP servers expose tools that MCP clients consume. 

There are [reference MCP servers](https://github.com/modelcontextprotocol/servers) that one can run locally and have apps
like Claude Desktop can use as tools. For example, this [quickstart](https://modelcontextprotocol.io/quickstart/user) 
shows how to use [Filesystem MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) and 
enable Claude Desktop to access the filesystem.

ADK has a [MCPToolset](https://google.github.io/adk-docs/tools/mcp-tools/) to integrate tools from external MCP servers
into your ADK agents.   

Let's build an ADK agent to have access to the filesystem using the reference MCP Filesystem Server. We can then use 
that agent to save the travel information to a file. 

Take a look at the [agent.py](agent.py) for details. 

## Run agent - terminal

Before running the travel helper with filesystem agent: 

1- In [agent.py](agent.py), change the `TARGET_FOLDER_PATH` to a location in your system.

2- In the root [agent.py](../../agent.py), uncomment this line to change the instruction prompt to use the filesystem agent:
   ```
   # instruction=instruction_prompt + instruction_prompt_for_filesystem + response_format,
   ```
3- In the root [agent.py](../../agent.py), uncomment this line to include the filesystem agent in the tools:
   ```
   # AgentTool(agent=filesystem_assistant_agent)
   ```

Now, run the travel helper:

```shell
adk run ./travel_helper
```

After generating the travel information, you can ask it to save to a file:

```shell
...
----------------
Enjoy your trip!

[user]: Can you save the information to a file?
Allowed directories: [ '/Users/atamel/Desktop' ]
[travel_helper_agent]: OK. I have saved the information to the file `/Users/atamel/Desktop/dubai_trip_summary.txt`.
```

