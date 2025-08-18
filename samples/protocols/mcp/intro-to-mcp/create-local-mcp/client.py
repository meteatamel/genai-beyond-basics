import asyncio
from fastmcp import Client

async def call_tool(name: str):
    async with Client("http://127.0.0.1:8000/mcp") as client:
        tools = await client.list_tools()
        print(f"List of tools:")
        for tool in tools:
            print(f"-{tool.name}")
        print(f"Calling greet with name: {name}")
        result = await client.call_tool("greet", {"name": name})
        print(f"Result: {result}")
        print(f"{result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(call_tool("Mete"))
