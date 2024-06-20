import argparse
import logging
import vertexai

from vertexai.generative_models import GenerationConfig, GenerativeModel, Tool
from vertexai.preview.generative_models import grounding

logger = logging.getLogger(__name__)


def generate_text_with_grounding_vertex_ai_search(project_id: str, datastore_path: str):
    vertexai.init(project=project_id, location="us-central1")

    model = GenerativeModel(model_name="gemini-1.5-flash-001")

    tools = [Tool.from_retrieval(
        grounding.Retrieval(grounding.VertexAISearch(datastore=datastore_path)))] if datastore_path else None

    logger.debug(f"Project id: {project_id}")
    logger.debug(f"Grounding with data store path: {datastore_path}")

    prompt = "What is the cargo capacity of Cymbal Starlight?"
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
    parser = argparse.ArgumentParser(description='Grounding with your own data with Vertex AI Search')
    parser.add_argument('--project_id', type=str, required=True, help='Google Cloud project id (required)')
    parser.add_argument('--datastore_path', type=str, help='The full path of the datastore in this format: '
                                                           'projects/{project_id}/locations/{location}/collections/'
                                                           'default_collection/dataStores/{data_store_id}')

    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    args = parse_args()
    generate_text_with_grounding_vertex_ai_search(args.project_id, args.datastore_path)


if __name__ == '__main__':
    main()
