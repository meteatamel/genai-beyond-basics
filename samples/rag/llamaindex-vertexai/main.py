import argparse
import logging
from typing import Optional

import vertexai
from google.cloud.aiplatform_v1beta1.services.vertex_rag_data_service.pagers import ListRagFilesPager
from vertexai.generative_models import GenerationConfig, GenerativeModel
from vertexai.preview import rag
from vertexai.preview.generative_models import Tool
from vertexai.preview.rag.utils.resources import RagCorpus, RagFile

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')


def get_or_create_corpus(corpus_display_name: str) -> RagCorpus:
    corpus = get_corpus_by_display_name(corpus_display_name)
    if corpus:
        logger.info("Existing corpus fetched:")
        log_names(corpus)
    else:
        corpus = rag.create_corpus(display_name=corpus_display_name)
        logger.info("Corpus created:")
        log_names(corpus)
    return corpus


def get_corpus_by_display_name(display_name: str) -> RagCorpus:
    corpora = rag.list_corpora()
    return next((corpus for corpus in corpora if corpus.display_name == display_name), None)


def list_corpus():
    corpora = rag.list_corpora()
    for corpus in corpora:
        log_names(corpus)


def delete_corpus(corpus_name: str):
    rag.delete_corpus(name=corpus_name)
    logger.info(f"Corpus deleted: {corpus_name}")


def get_or_upload_file(corpus_name: str, path: str, display_name: Optional[str] = None,
                       description: Optional[str] = None) -> RagFile:
    rag_file = get_file_by_display_name(corpus_name, display_name)
    if rag_file:
        logger.info(f"Existing file fetched from corpus: {corpus_name}")
    else:
        rag_file = rag.upload_file(
            corpus_name=corpus_name,
            path=path,
            display_name=display_name,
            description=description,
        )
        logger.info(f"File upload to corpus: {corpus_name}")

    log_names(rag_file)
    return rag_file


def get_file_by_display_name(corpus_name: str, display_name: str) -> RagFile:
    files = rag.list_files(corpus_name=corpus_name)
    file = next((file for file in files if file.display_name == display_name), None)
    return file


def list_files(corpus_name: str) -> ListRagFilesPager:
    files = rag.list_files(corpus_name=corpus_name)
    logger.info(f"Files in corpus: {corpus_name}")
    for file in files:
        log_names(file)
    return files


def log_names(file):
    logger.info(f"-name: {file.name}")
    logger.info(f" display_name: {file.display_name}")


def delete_file(file_name: str):
    rag.delete_file(name=file_name)
    logger.info(f"File {file_name} deleted.")


def direct_retrieve_from_rag_corpus(corpus_name: str, text: str):
    response = rag.retrieval_query(
        rag_resources=[
            rag.RagResource(
                rag_corpus=corpus_name
                # Supply IDs from `rag.list_files()`.
                # rag_file_ids=["rag-file-1", "rag-file-2", ...],
            )
        ],
        text=text,
        similarity_top_k=10,  # Optional
        vector_distance_threshold=0.5,  # Optional
    )

    logger.info(f"Text: {text}")
    logger.info(f"Response: {response}")


def generate_text_with_llamaindex_vertexai(corpus_name: str, prompt: str):
    model = GenerativeModel(model_name="gemini-1.5-flash-001")

    logger.info(f"Corpus name: {corpus_name}")

    tools = None
    if corpus_name:
        tools = [Tool.from_retrieval(
            retrieval=rag.Retrieval(
                source=rag.VertexRagStore(
                    rag_resources=[
                        rag.RagResource(
                            rag_corpus=corpus_name,  # Currently only 1 corpus is allowed.
                            # Supply IDs from `rag.list_files()`.
                            # rag_file_ids=["rag-file-1", "rag-file-2", ...],
                        )
                    ],
                    similarity_top_k=3,  # Optional
                    vector_distance_threshold=0.5,  # Optional
                ),
            )
        )]

    response = model.generate_content(
        prompt,
        tools=tools,
        generation_config=GenerationConfig(
            temperature=0.0,
        ),
    )

    logger.info(f"Prompt: {prompt}")
    logger.debug(f"Response: {response}")
    logger.info(f"Response text: {response.candidates[0].content.parts[0].text}")


def get_args_parser():
    parser = argparse.ArgumentParser(description="RAG with LlamaIndex on Vertex AI CLI")

    parser.add_argument('--project_id', type=str, required=True, help='Google Cloud project id (required)')

    # Subparsers for commands
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_corpus_parser = subparsers.add_parser("create_corpus", help="Create a RAG corpus")
    create_corpus_parser.add_argument("--display_name", type=str, required=True, help="Display name of the corpus")

    subparsers.add_parser("list_corpus", help="List RAG corpora")

    delete_corpus_parser = subparsers.add_parser("delete_corpus", help="Delete a RAG corpus")
    delete_corpus_parser.add_argument("--corpus_name", type=str, required=True, help="Name of the corpus to delete")

    upload_file_parser = subparsers.add_parser("upload_file", help="Upload a local file to a RAG corpus")
    upload_file_parser.add_argument("--corpus_name", type=str, required=True, help="Name of the corpus")
    upload_file_parser.add_argument("--path", type=str, required=True, help="Path to the file")
    upload_file_parser.add_argument("--display_name", type=str, help="Display name for the file (optional)")
    upload_file_parser.add_argument("--description", type=str, help="Description for the file (optional)")

    list_files_parser = subparsers.add_parser("list_files", help="List files in a RAG corpus")
    list_files_parser.add_argument("--corpus_name", type=str, required=True, help="Name of the corpus")

    delete_file_parser = subparsers.add_parser("delete_file", help="Delete a file from a RAG corpus")
    delete_file_parser.add_argument("--file_name", type=str, required=True, help="Name of the file to delete")

    direct_retrieve_parser = subparsers.add_parser("direct_retrieve", help="Directly retrieve from RAG corpus")
    direct_retrieve_parser.add_argument("--corpus_name", type=str, required=True, help="Name of the corpus")
    direct_retrieve_parser.add_argument("--text", type=str, required=True, help="Text to retrieve")

    generate_text_parser = subparsers.add_parser("generate_text", help="Generate text with LLM")
    generate_text_parser.add_argument("--corpus_name", type=str, help="Name of the corpus (optional)")
    generate_text_parser.add_argument("--prompt", type=str, required=True, help="Prompt for text generation")

    return parser.parse_args()


def main():
    args = get_args_parser()

    vertexai.init(project=args.project_id, location="us-central1")

    command_map = {
        "create_corpus": lambda: get_or_create_corpus(args.display_name),
        "list_corpus": list_corpus,
        "delete_corpus": lambda: delete_corpus(args.corpus_name),
        "upload_file": lambda: get_or_upload_file(args.corpus_name, args.path, args.display_name, args.description),
        "list_files": lambda: list_files(args.corpus_name),
        "delete_file": lambda: delete_file(args.file_name),
        "direct_retrieve": lambda: direct_retrieve_from_rag_corpus(args.corpus_name, args.text),
        "generate_text": lambda: generate_text_with_llamaindex_vertexai(args.corpus_name, args.prompt)
    }

    if args.command in command_map:
        command_map[args.command]()
    else:
        print(f"Unknown command: {args.command}")


if __name__ == '__main__':
    main()
