import argparse
import logging

import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')


def without_controlled_generation1():
    model = GenerativeModel('gemini-1.5-flash-001')

    prompt = "List a few popular cookie recipes"
    response = model.generate_content(prompt)
    log_prompt_response(prompt, response)


def without_controlled_generation2():
    model = GenerativeModel('gemini-1.5-flash-001')

    prompt = """
        List a few popular cookie recipes using this JSON schema:
        Recipe = {"recipe_name": str}
        Return: list[Recipe]
      """
    response = model.generate_content(prompt)
    log_prompt_response(prompt, response)


def with_response_mime_type():
    model = GenerativeModel('gemini-1.5-flash-001',
                            generation_config=GenerationConfig(
                                response_mime_type="application/json"
                            ))

    prompt = """
        List a few popular cookie recipes using this JSON schema:
        Recipe = {"recipe_name": str}
        Return: list[Recipe]
      """
    response = model.generate_content(prompt)
    log_prompt_response(prompt, response)


def with_response_schema1():
    response_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "recipe_name": {"type": "string"},
                "calories": {"type": "integer"}
            },
            "required": ["recipe_name"]
        },
    }

    model = GenerativeModel('gemini-1.5-pro-001',
                            generation_config=GenerationConfig(
                                response_mime_type="application/json",
                                response_schema=response_schema))

    prompt = "List a few popular cookie recipes"
    response = model.generate_content(prompt)
    log_prompt_response(prompt, response)


def with_response_schema2():
    response_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "dessert_name": { "type": "string"},
                "rating" : { "type": "integer"},
                "message": { "type": "string"}
            },
            "required": ["dessert_name", "rating", "message"]
        },
    }

    model = GenerativeModel('gemini-1.5-pro-001',
                            generation_config=GenerationConfig(
                                response_mime_type="application/json",
                                response_schema=response_schema))

    prompt = """
      Extract reviews from our social media:

      - "Absolutely loved it! Best ice cream I've ever had." Rating: 4
      - "Quite good cheese cake, but a bit too sweet for my taste." Rating: 2
      - "Did not like the tiramisu." Rating: 0
    """
    response = model.generate_content(prompt)
    log_prompt_response(prompt, response)


def log_prompt_response(prompt, response):
    logger.info(f"Prompt: {prompt}")
    logger.debug(f"Response: {response}")
    logger.info(f"Response: {response.candidates[0].content.parts[0].text}")


def get_args_parser():
    parser = argparse.ArgumentParser(description="Controlled generation")

    parser.add_argument('--project_id', type=str, required=True, help='Google Cloud project id (required)')

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("without_controlled_generation1", help="Generate without controlled generation")
    subparsers.add_parser("without_controlled_generation2", help="Generate without controlled generation")
    subparsers.add_parser("with_response_mime_type", help="Generate with JSON response mime type")
    subparsers.add_parser("with_response_schema1", help="Generate with JSON response schema")
    subparsers.add_parser("with_response_schema2", help="Generate with JSON response schema")

    return parser.parse_args()


def run_command(args):
    try:
        func = globals()[f"{args.command}"]
        func()
    except KeyError:
        print(f"Error: Unknown command '{args.command}'")
        exit(1)


def main():
    args = get_args_parser()
    vertexai.init(project=args.project_id, location="us-central1")
    run_command(args)


if __name__ == '__main__':
    main()
