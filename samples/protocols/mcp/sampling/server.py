from fastmcp import FastMCP, Context

mcp = FastMCP("Sampling Server")

# Example with a basic prompt

@mcp.tool
async def generate_summary(content: str, ctx: Context) -> str:
    """Generate a summary of the provided content."""
    prompt = f"Please provide a concise summary of the following content:\n\n{content}"

    response = await ctx.sample(prompt)
    return response.text


# Example with a more advanced prompt

@mcp.tool
async def generate_code(concept: str, ctx: Context) -> str:
    """Generate a Python code example for a given concept."""
    response = await ctx.sample(
        messages=f"Write a simple Python code example demonstrating '{concept}'.",
        system_prompt="You are an expert Python programmer. Provide concise, working code examples without explanations.",
        model_preferences=["gemini-2.5-pro", "gemini-2.5-flash"],  # Prefer specific models
        temperature=0.2, # Low randomness for consistency
        max_tokens=800
    )

    return response.text


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8080, path="/mcp")