import asyncio
import random
from fastmcp import FastMCP, Context

mcp = FastMCP("Progress Server")

# Example with absolute progress

@mcp.tool
async def process_items(items: list[str], ctx: Context) -> dict:
    """Process a list of items with progress updates."""
    total = len(items)
    results = []

    for i, item in enumerate(items):
        # Report progress as we process each item
        await ctx.report_progress(progress=i, total=total)

        # Simulate processing time
        await asyncio.sleep(0.1)
        results.append(item.upper())

    # Report completion
    await ctx.report_progress(progress=total, total=total)

    return {"Processed": len(results), "results": results}


# Example with percentage based progress

@mcp.tool
async def download_file(url: str, ctx: Context) -> str:
    """Download a file with percentage progress."""
    total_size = 1000  # KB
    downloaded = 0

    while downloaded < total_size:
        # Download chunk
        chunk_size = min(50, total_size - downloaded)
        downloaded += chunk_size

        # Report percentage progress
        percentage = (downloaded / total_size) * 100
        await ctx.report_progress(progress=percentage, total=100)

        await asyncio.sleep(0.1)  # Simulate download time

    return f"Downloaded file from {url}"


# Example with indeterminate progress

@mcp.tool
async def scan_directory(directory: str, ctx: Context) -> dict:
    """Scan directory with indeterminate progress."""
    files_found = 0

    # Simulate directory scanning
    for i in range(random.randint(1, 20)):  # Unknown number of files
        files_found += 1

        # Report progress without total for indeterminate operations
        await ctx.report_progress(progress=files_found)

        await asyncio.sleep(0.2)

    return {"files_found": files_found, "directory": directory}


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8080, path="/mcp")