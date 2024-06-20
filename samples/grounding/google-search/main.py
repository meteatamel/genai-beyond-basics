import argparse
import logging
import vertexai

from vertexai.generative_models import GenerationConfig, GenerativeModel, Tool
from vertexai.preview.generative_models import grounding

logger = logging.getLogger(__name__)


def generate_text_with_grounding_vertex_ai_search(project_id: str, google_search_grounding: bool):

    vertexai.init(project=project_id, location="us-central1")

    model = GenerativeModel(model_name="gemini-1.5-flash-001")

    tools = [Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())] if google_search_grounding else None

    logger.debug(f"Project id: {project_id}")
    logger.debug(f"Grounding with Google Search? {google_search_grounding}")

    prompt = "What was the weather like in London yesterday?"
    logger.info(f"Prompt: {prompt}")

    response = model.generate_content(
        prompt,
        tools=tools,
        generation_config=GenerationConfig(
            temperature=0.0,
        ),
    )

    logger.debug(f"Response: {response}")

    logger.info(f"Response text: {response.candidates[0].content.parts[0].text}")


def parse_args():
    parser = argparse.ArgumentParser(description='Grounding with public data with Google Search')
    parser.add_argument('--project_id', type=str, required=True, help='Google Cloud project id (required)')
    parser.add_argument('--google_search_grounding', action='store_true',
                        help='Use Vertex AI Google Search grounding (default: False)')

    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    args = parse_args()
    generate_text_with_grounding_vertex_ai_search(args.project_id, args.google_search_grounding)


if __name__ == '__main__':
    main()
