import asyncio
from fastmcp import Client
from fastmcp.client.sampling import (
    SamplingMessage,
    SamplingParams,
    RequestContext,
)
from google import genai
from google.genai.types import GenerateContentConfig

async def generate_content(model: str,
                     system_prompt: str,
                     temperature: float,
                     max_tokens: int,
                     contents: list[str]) -> str:

    gemini_client = genai.Client(vertexai=True,
                    project="genai-atamel",
                    location="global").aio

    response = await gemini_client.models.generate_content(
        model=model,
        contents=contents,
        config=GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
    )

    return response.text


async def sampling_handler(
    messages: list[SamplingMessage],
    params: SamplingParams,
    context: RequestContext) -> str:

    # Extract message content
    contents = []
    for message in messages:
        content = message.content.text if hasattr(message.content, 'text') else str(message.content)
        contents.append(content)

    # Use the provided preferences
    system_prompt = params.systemPrompt or "You are a helpful assistant."
    temperature = params.temperature or 0.7
    max_tokens = params.maxTokens or 500
    model = params.modelPreferences.hints[0].name if params.modelPreferences else "gemini-2.5-flash"

    # Integrate with the LLM
    response_text = await generate_content(model, system_prompt, temperature, max_tokens, contents)

    return response_text


async def generate_summary(content):
    client = Client("http://127.0.0.1:8080/mcp/", sampling_handler=sampling_handler)
    async with client:
        result = await client.call_tool("generate_summary", {"content": content})
        print(f"Tool result: {result.content[0].text}")


async def generate_code(concept):
    client = Client("http://127.0.0.1:8080/mcp/", sampling_handler=sampling_handler)
    async with client:
        result = await client.call_tool("generate_code", {"concept": concept})
        print(f"Tool result: {result.content[0].text}")


async def main():

    while True:
        print("\nAvailable tools:")
        print("1. generate_summary")
        print("2. generate_code")

        choice = input("\nSelect a tool: ").strip()

        if choice == "1":
            user_input = input("Enter content to summarize: ").strip()
            await generate_summary(user_input)
        elif choice == "2":
            user_input = input("Enter concept to generate code for: ").strip()
            await generate_code(user_input)
        else:
            print("Goodbye!")
            break


if __name__ == "__main__":
    asyncio.run(main())