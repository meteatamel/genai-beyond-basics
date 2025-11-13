import os
import sys
import time

from google import genai
from google.genai.types import GenerateContentConfig, Tool, FileSearch

"""
This module exposes simple helper functions that show how to use File 
Search Tool of Gemini API. Note that File Search Tool is only supported 
by Gemini API (not Vertex AI API)
Each function is intended to be callable from the command line via the `cli()` helper.
"""

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def create_store(display_name: str = None) -> str:
    """Create a new file search store.

    Args:
        display_name: Optional human-readable display name for the store.

    Returns:
        The resource name (string) of the created file search store.
    """
    file_search_store = client.file_search_stores.create(
        config={'display_name': display_name}
    )
    print(f"Created a file search store:")
    print(f"  {file_search_store.name} - {file_search_store.display_name}")
    return file_search_store.name


def list_stores():
    """List all file search stores in the current project.

    Prints the display name and resource name for each store.
    """
    print("List of file search stores:")
    for file_search_store in client.file_search_stores.list():
        print(f"  {file_search_store.name} - {file_search_store.display_name}")


def delete_store(file_search_store_name: str = None):
    """Delete a file search store.

    If `file_search_store_name` is provided, deletes that single store (force
    delete). If None, deletes all stores by iterating over them.

    Args:
        file_search_store_name: Optional resource name of the store to delete.
    """
    if file_search_store_name:
        client.file_search_stores.delete(name=file_search_store_name, config={"force": True})
        print(f"Deleted file search store:")
        print(f"  {file_search_store_name}")
    else:
        for file_search_store in client.file_search_stores.list():
            delete_store(file_search_store.name)


def upload_to_store(file_search_store_name: str, file_path: str, display_name: str = None):
    """Upload a local file to a file search store.

    Args:
        file_search_store_name: Resource name of the target file search store.
        file_path: Local path to the file to upload.
        display_name: Optional human-readable display name for the file.

    The function polls the long-running operation until completion and prints
    progress to stdout.
    """
    print(f"Uploading file: {file_path} with display name: {display_name} to file search store:")
    print(f"  {file_search_store_name}")
    upload_op = client.file_search_stores.upload_to_file_search_store(
        file_search_store_name=file_search_store_name,
        file=file_path,
        config={
            # Optional display name for the uploaded file.
            'display_name': display_name,
            # Optional config for telling the service how to chunk the data.
            # 'chunking_config': {
            #     'white_space_config': {
            #         'max_tokens_per_chunk': 200,
            #         'max_overlap_tokens': 20
            #     }
            # },
            # Optional custom metadata to associate with the file.
            # 'custom_metadata': [
            #     {"key": "author", "string_value": "Robert Graves"},
            #     {"key": "year", "numeric_value": 1934}
            # ]
        }
    )

    while not upload_op.done:
        print("Waiting for upload to complete...")
        time.sleep(5)
        upload_op = client.operations.get(upload_op)
    print("Upload completed.")


def list_docs(file_search_store_name: str):
    """List all documents in a file search store.

    Args:
        file_search_store_name: The file search store name.
    """

    print(f"List of documents in file search store: ")
    for document in client.file_search_stores.documents.list(parent=file_search_store_name):
        print(f"  {document.name} - {document.display_name}")


def delete_doc(document_name: str):
    """Delete a document from a file search store.

    Args:
        document_name: Resource name of the document to delete.
    """
    client.file_search_stores.documents.delete(name=document_name, config={"force": True})
    print(f"Deleted document:")
    print(f"  {document_name}")


def generate_content(prompt: str, file_search_store_name: str = None):
    """Generate content optionally grounded with a file-search store.

    Args:
        prompt: The prompt (string) to send to the model.
        file_search_store_name: Optional resource name; if provided, the model
            will be allowed to use the File Search tool for grounding.

    The function prints the model response and any grounding sources found.
    """
    generate_config = None
    if file_search_store_name:
        generate_config = GenerateContentConfig(
            tools=[Tool(
                file_search=FileSearch(
                    file_search_store_names=[file_search_store_name]
                )
            )]
        )

    print(f"Generating content with file search store: {file_search_store_name}")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=generate_config
    )
    print(f"Response: {response.text}")

    if file_search_store_name:
        grounding = response.candidates[0].grounding_metadata
        if not grounding:
            print("Grounding sources: None")
        else:
            sources = {c.retrieved_context.title for c in grounding.grounding_chunks}
            print("Grounding sources: ", *sources)


def _cli():
    """Simple command-line interface to call the helper functions.

    Usage: python main.py <function> [args...]

    The CLI maps the first positional argument to a function defined in this
    module and passes the remaining positional arguments as strings. Example:
        python main.py create my-store-name
        python main.py upload <store-name> ./path/to/file.pdf

    Note: arguments from the CLI are strings; functions that require other
    types must convert them when called programmatically.
    """
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
    _cli()
