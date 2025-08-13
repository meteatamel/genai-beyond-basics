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
    # By default, it uses the stdio transport
    # mcp.run()
    # mcp.run(transport="stdio")

    # Both 'http' or 'streaming-http' refer to the same streaming-http transport
    # mcp.run(transport="http")
    mcp.run(transport="http", host="127.0.0.1", port=8000)
