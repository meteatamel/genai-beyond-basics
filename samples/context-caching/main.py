import argparse
import datetime
import logging

import vertexai
from vertexai.generative_models import Part
from vertexai.preview import caching
from vertexai.preview.generative_models import GenerativeModel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')


def create_cached_content():
    system_instruction = """
    You are an expert researcher. You always stick to the facts in the sources provided, and never make up new facts.
    Now look at these research papers, and answer the following questions.
    """

    contents = [
        Part.from_uri(
            "gs://cloud-samples-data/generative-ai/pdf/2312.11805v3.pdf",
            mime_type="application/pdf",
        ),
        Part.from_uri(
            "gs://cloud-samples-data/generative-ai/pdf/2403.05530.pdf",
            mime_type="application/pdf",
        ),
    ]

    cached_content = caching.CachedContent.create(
        model_name="gemini-1.5-pro-001",
        system_instruction=system_instruction,
        contents=contents,
        ttl=datetime.timedelta(minutes=60),
    )

    logger.info(f"Cached content: {cached_content}")


def list_cached_content():
    cached_content_list = caching.CachedContent.list()
    logger.info(f"Cached content list: {cached_content_list}")


def delete_cached_content(cache_id: str):
    cached_content = caching.CachedContent(cached_content_name=cache_id)
    cached_content.delete()
    logger.info(f"Cached content deleted: {cached_content.name}")


def generate_content(cache_id: str):
    if cache_id:
        cached_content = caching.CachedContent(cached_content_name=cache_id)
        model = GenerativeModel.from_cached_content(cached_content=cached_content)
    else:
        model = GenerativeModel('gemini-1.5-flash-001')

    prompt = "What are the papers about?"
    response = model.generate_content(prompt)
    log_prompt_response(prompt, response)


def log_prompt_response(prompt, response):
    logger.info(f"Prompt: {prompt}")
    logger.debug(f"Response: {response}")
    logger.info(f"Response: {response.candidates[0].content.parts[0].text}")


def get_args_parser():
    parser = argparse.ArgumentParser(description="Context caching")

    parser.add_argument('--project_id', type=str, required=True, help='Google Cloud project id (required)')

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("create_cached_content", help="Create cached content")
    subparsers.add_parser("list_cached_content", help="List cached content")

    delete_cached_content_parser = subparsers.add_parser("delete_cached_content", help="Delete cached content")
    delete_cached_content_parser.add_argument("--cache_id", type=str, required=True, help="Cache id")

    generate_parser = subparsers.add_parser("generate_content", help="Generate content with or without cached content")
    generate_parser.add_argument("--cache_id", type=str, help="Cache id (optional)")

    return parser.parse_args()


def main():
    args = get_args_parser()

    vertexai.init(project=args.project_id, location="us-central1")

    command_map = {
        "generate_content": lambda: generate_content(args.cache_id),
        "create_cached_content": lambda: create_cached_content(),
        "list_cached_content": lambda: list_cached_content(),
        "delete_cached_content": lambda: delete_cached_content(args.cache_id)
    }

    if args.command in command_map:
        command_map[args.command]()
    else:
        print(f"Unknown command: {args.command}")


if __name__ == '__main__':
    main()
