import os
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"


if __name__ == "__main__":
    # host="0.0.0.0" and port are required for Cloud Run
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=os.getenv("PORT", 8080)
    )

