import argparse
import logging
from typing import Optional

import vertexai
from google.cloud.aiplatform_v1beta1.services.vertex_rag_data_service.pagers import (ListRagCorporaPager,
                                                                                     ListRagFilesPager)
from vertexai.generative_models import GenerationConfig, GenerativeModel
from vertexai.preview import rag
from vertexai.preview.generative_models import Tool
from vertexai.preview.rag.utils.resources import RagCorpus, RagFile

logger = logging.getLogger(__name__)


def get_or_create_corpus(corpus_display_name: str) -> RagCorpus:
    rag_corpus = get_corpus_by_display_name(corpus_display_name)
    if rag_corpus:
        logger.info(f"Existing corpus fetched: {rag_corpus.name}")
    else:
        rag_corpus = rag.create_corpus(display_name=corpus_display_name)
        logger.info(f"Corpus created: {rag_corpus.name}")
    return rag_corpus


def get_corpus_by_display_name(display_name: str) -> RagCorpus:
    corpora = rag.list_corpora()
    return next((corpus for corpus in corpora if corpus.display_name == display_name), None)


def list_corpora() -> ListRagCorporaPager:
    corpora = rag.list_corpora()
    logger.info(f"List of corpora: {corpora}")
    return corpora


def delete_corpus(corpus_name: str):
    rag.delete_corpus(name=corpus_name)
    logger.info(f"Corpus deleted: {corpus_name}")


def get_or_upload_file(corpus_name: str, path: str, display_name: Optional[str] = None,
                       description: Optional[str] = None) -> RagFile:
    rag_file = get_file_by_display_name(corpus_name, display_name)
    if rag_file:
        logger.info(f"Existing file fetched: {rag_file.display_name}")
    else:
        rag_file = rag.upload_file(
            corpus_name=corpus_name,
            path=path,
            display_name=display_name,
            description=description,
        )
        logger.info(f"File: {rag_file.display_name} upload to corpus: {corpus_name}")
    return rag_file


def get_file_by_display_name(corpus_name: str, display_name: str) -> RagFile:
    files = rag.list_files(corpus_name=corpus_name)
    file = next((file for file in files if file.display_name == display_name), None)
    return file


def list_files(corpus_name: str) -> ListRagFilesPager:
    files = rag.list_files(corpus_name=corpus_name)
    logger.info(f"Files in corpus: {corpus_name}")
    for file in files:
        logger.info(f"-{file.display_name}")
    return files


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

    logger.info(f"Response: {response}")


def generate_text_with_llamaindex_vertexai(corpus_name: str, prompt: str):
    model = GenerativeModel(model_name="gemini-1.5-flash-001")

    logger.info(f"RAG corpus name: {corpus_name}")

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

    logger.debug(f"Response: {response}")

    logger.info(f"Response text: {response.candidates[0].content.parts[0].text}")


def prepare_rag_corpus(corpus_display_name: str):

    rag_corpus = get_or_create_corpus(corpus_display_name)

    get_or_upload_file(corpus_name=rag_corpus.name, path="cymbal-starlight-2024.pdf",
                       display_name="cymbal-starlight-2024.pdf", description="User manual for Cymbal Starlight 2024")


def parse_args():
    parser = argparse.ArgumentParser(description='RAG with LlamaIndex on Vertex AI')
    parser.add_argument('--project_id', type=str, required=True, help='Google Cloud project id (required)')
    parser.add_argument('--rag_corpus_display_name', type=str, help='RAG corpus display name '
                                                                    '(required unless --generate_text is used)')
    parser.add_argument('--prepare_rag_corpus', action='store_true', help='Prepare RAG corpus')
    parser.add_argument('--direct_retrieve_from_rag_corpus', action='store_true', help='Directly retrieve '
                                                                                       'from RAG corpus')
    parser.add_argument('--generate_text', action='store_true', help='Generate text with LLM')

    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    args = parse_args()

    vertexai.init(project=args.project_id, location="us-central1")

    if args.prepare_rag_corpus:
        prepare_rag_corpus(args.rag_corpus_display_name)
    else:
        corpus = get_corpus_by_display_name(args.rag_corpus_display_name)
        prompt = "What is the cargo capacity of Cymbal Starlight?"
        logger.info(f"Prompt: {prompt}")
        if args.direct_retrieve_from_rag_corpus:
            direct_retrieve_from_rag_corpus(corpus.name, prompt)
        elif args.generate_text:
            corpus_name = corpus.name if corpus else None
            generate_text_with_llamaindex_vertexai(corpus_name, prompt)


if __name__ == '__main__':
    main()
