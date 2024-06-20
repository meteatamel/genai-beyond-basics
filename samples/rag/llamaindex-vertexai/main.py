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


def get_or_create_corpus(display_name: str) -> RagCorpus:
    rag_corpus = get_corpus_by_display_name(display_name)
    if rag_corpus:
        logger.info(f"Existing corpus fetched: {rag_corpus.name}")
    else:
        rag_corpus = rag.create_corpus(display_name=display_name)
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


def direct_retrieval(rag_corpus: RagCorpus, text: str):
    response = rag.retrieval_query(
        rag_resources=[
            rag.RagResource(
                rag_corpus=rag_corpus.name,
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


def generate_text_with_llamaindex_vertexai(rag_corpus: RagCorpus, prompt: str):
    model = GenerativeModel(model_name="gemini-1.5-flash-001")

    rag_retrieval_tool = Tool.from_retrieval(
        retrieval=rag.Retrieval(
            source=rag.VertexRagStore(
                rag_resources=[
                    rag.RagResource(
                        rag_corpus=rag_corpus.name,  # Currently only 1 corpus is allowed.
                        # Supply IDs from `rag.list_files()`.
                        # rag_file_ids=["rag-file-1", "rag-file-2", ...],
                    )
                ],
                similarity_top_k=3,  # Optional
                vector_distance_threshold=0.5,  # Optional
            ),
        )
    )

    logger.info(f"Prompt: {prompt}")

    response = model.generate_content(
        prompt,
        tools=[rag_retrieval_tool],
        generation_config=GenerationConfig(
            temperature=0.0,
        ),
    )

    logger.debug(f"Response: {response}")

    logger.info(f"Response text: {response.candidates[0].content.parts[0].text}")


def parse_args():
    parser = argparse.ArgumentParser(description='RAG with LlamaIndex on Vertex AI')
    parser.add_argument('--project_id', type=str, required=True, help='Google Cloud project id (required)')

    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    args = parse_args()

    vertexai.init(project=args.project_id, location="us-central1")

    rag_corpus = get_or_create_corpus("llamaindex-vertexai-sample-corpus")

    get_or_upload_file(corpus_name=rag_corpus.name, path="cymbal-starlight-2024.pdf",
                       display_name="cymbal-starlight-2024.pdf", description="User manual for Cymbal Starlight 2024")

    direct_retrieval(rag_corpus=rag_corpus,
                     text="What is the cargo capacity of Cymbal Starlight?")

    generate_text_with_llamaindex_vertexai(rag_corpus=rag_corpus,
                                           prompt="What is the cargo capacity of Cymbal Starlight?")


if __name__ == '__main__':
    main()
