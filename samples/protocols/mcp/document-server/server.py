# Reference: Introduction to Model Context Protocol:
# https://anthropic.skilljar.com/introduction-to-model-context-protocol

import os
from fastmcp import FastMCP
from fastmcp.prompts.prompt import PromptMessage, TextContent

mcp = FastMCP("DocumentMCP", log_level="DEBUG")

DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")


# Note: Ideally, this would be handled as a resource but Gemini CLI does not
# support MCP resources as of Feb 2026.
@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string.",
)
def read_document(doc_id: str) -> str:
    """Read the contents of a document and return it as a string."""
    doc_path = os.path.join(DOCS_DIR, doc_id)
    if not os.path.exists(doc_path):
        raise ValueError(f"Doc with id {doc_id} not found")

    with open(doc_path, "r", encoding="utf-8") as f:
        return f.read()


@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string",
)
def edit_document(doc_id: str, old_str: str, new_str: str) -> None:
    """Edit a document by replacing a string in the documents content with a new string."""
    doc_path = os.path.join(DOCS_DIR, doc_id)
    if not os.path.exists(doc_path):
        raise ValueError(f"Doc with id {doc_id} not found")

    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace(old_str, new_str)

    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(content)


@mcp.resource("docs://documents", mime_type="application/json")
def list_docs() -> list[str]:
    """List all documents available in the docs directory."""
    return os.listdir(DOCS_DIR)


@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def fetch_doc(doc_id: str) -> str:
    """Fetch the contents of a specific document by its ID."""
    doc_path = os.path.join(DOCS_DIR, doc_id)
    if not os.path.exists(doc_path):
        raise ValueError(f"Doc with id {doc_id} not found")

    with open(doc_path, "r", encoding="utf-8") as f:
        return f.read()


@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format.",
)
def format_document(doc_id: str) -> PromptMessage:
    """Return a prompt message to reformat a document into Markdown."""
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.

    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary. Feel free to add in extra text, but don't change the meaning of the report.
    Use the 'edit_document' tool to edit the document. After the document has been edited, respond with the final version of the doc. Don't explain your changes.
    """

    return PromptMessage(role="user", content=TextContent(type="text", text=prompt))


if __name__ == "__main__":
    #mcp.run(transport="stdio")
    mcp.run(transport="http", host="127.0.0.1", port=8000)
