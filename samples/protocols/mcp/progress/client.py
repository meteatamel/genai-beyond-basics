import asyncio
from fastmcp import Client

# Progress handler to handle progress updates from the server
async def progress_handler(
    progress: float,
    total: float | None,
    message: str | None
) -> None:
    if total is not None:
        if total == 100:
            percentage = (progress / total) * 100
            print(f"Progress: {percentage:.1f}%")
        else:
            print(f"Progress: {progress}/{total}")
    else:
        print(f"Progress: {progress}")


async def process_items(items: list[str]):
    client = Client("http://127.0.0.1:8080/mcp/", progress_handler=progress_handler)
    async with client:
        result = await client.call_tool("process_items", {"items": items})
        print(f"Tool result: {result.content[0].text}")


async def download_file(url: str):
    client = Client("http://127.0.0.1:8080/mcp/", progress_handler=progress_handler)
    async with client:
        result = await client.call_tool("download_file", {"url": url})
        print(f"Tool result: {result.content[0].text}")

async def scan_directory(directory: str):
    client = Client("http://127.0.0.1:8080/mcp/", progress_handler=progress_handler)
    async with client:
        result = await client.call_tool("scan_directory", {"directory": directory})
        print(f"Tool result: {result.content[0].text}")


async def main():

    while True:
        print("\nAvailable tools:")
        print("1. process_items")
        print("2. download_file")
        print("3. scan_directory")

        choice = input("\nSelect a tool: ").strip()

        if choice == "1":
            user_input = input("Enter comma separated items to process: ").strip()
            await process_items([item.strip() for item in user_input.split(",")])
        elif choice == "2":
            user_input = input("Enter a url to download: ").strip()
            await download_file(user_input)
        elif choice == "3":
            user_input = input("Enter a directory to scan:: ").strip()
            await scan_directory(user_input)
        else:
            print("Goodbye!")
            break


if __name__ == "__main__":
    asyncio.run(main())