import os
import sys
import time

from google import genai
from google.genai.types import GenerateContentConfig, Tool, FileSearch

# File Search Tool is only supported by Gemini API right now (not Vertex AI API)
# Reference: https://ai.google.dev/gemini-api/docs/file-search
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def create(display_name: str = "my-file-search-store") -> str:
    file_search_store = client.file_search_stores.create(
        config={'display_name': display_name}
    )
    print(f"Created a file search store:")
    print(f"  {file_search_store.display_name} - {file_search_store.name}")
    return file_search_store.name


def list():
    print("List of file search stores:")
    for file_search_store in client.file_search_stores.list():
        print(f"  {file_search_store.display_name} - {file_search_store.name}")


def delete(file_search_store_name: str = None):
    if file_search_store_name:
        print(f"Deleting file search store '{file_search_store_name}'")
        client.file_search_stores.delete(name=file_search_store_name, config={"force": True})
    else:
        for file_search_store in client.file_search_stores.list():
            delete(file_search_store.name)


def upload(file_search_store_name: str, file_path: str):
    print(f"Uploading file '{file_path}' to file search store '{file_search_store_name}'")
    upload_op = client.file_search_stores.upload_to_file_search_store(
        file_search_store_name=file_search_store_name,
        file=file_path,
        # config={
        #     'chunking_config': {
        #         'white_space_config': {
        #             'max_tokens_per_chunk': 200,
        #             'max_overlap_tokens': 20
        #         }
        #     }
        # }
    )

    while not upload_op.done:
        print("Waiting for upload to complete...")
        time.sleep(5)
        upload_op = client.operations.get(upload_op)
    print("Upload completed.")


def generate(prompt: str, file_search_store_name: str = None):
    generate_config = None
    if file_search_store_name:
        generate_config = GenerateContentConfig(
            tools=[Tool(
                file_search=FileSearch(
                    file_search_store_names=[file_search_store_name]
                )
            )]
        )

    print(f"Generating content with file search store '{file_search_store_name}'")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=generate_config
    )
    print(f"Response: {response.text}")

    grounding = response.candidates[0].grounding_metadata
    if not grounding:
        print("Grounding sources: None")
    else:
        sources = {c.retrieved_context.title for c in grounding.grounding_chunks}
        print("Grounding sources: ", *sources)


def cli():
    if len(sys.argv) < 2:
        print("Usage: python main.py <function> [args...]")
        sys.exit(1)

    func_name = sys.argv[1]
    func = globals().get(func_name)
    if not callable(func):
        print(f"Unknown function: {func_name}")
        sys.exit(1)

    args = sys.argv[2:]
    try:
        func(*args)
    except TypeError as e:
        print(f"Error calling {func_name}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
