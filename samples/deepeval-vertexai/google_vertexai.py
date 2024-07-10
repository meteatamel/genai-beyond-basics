import asyncio
import vertexai

from vertexai.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold
from deepeval.models.base_model import DeepEvalBaseLLM


class GoogleVertexAI(DeepEvalBaseLLM):
    """Class that implements Vertex AI for DeepEval"""
    def __init__(self, model_name, *args, **kwargs):
        super().__init__(model_name, *args, **kwargs)

    def load_model(self, *args, **kwargs):
        # Initialize safety filters for Vertex AI model
        # This is important to ensure no evaluation responses are blocked
        safety_settings = {
            HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
        }

        vertexai.init(project=kwargs['project'], location=kwargs['location'])

        return GenerativeModel(
            model_name=self.model_name,
            safety_settings=safety_settings)

    def generate(self, prompt: str) -> str:
        return self.model.generate_content(prompt).text

    async def a_generate(self, prompt: str) -> str:
        response = await self.model.generate_content_async(prompt)
        return response.text

    def get_model_name(self) -> str:
        return self.model_name


def main():
    model = GoogleVertexAI(model_name="gemini-1.0-pro-002",
                           project="genai-atamel",
                           location="us-central1")
    prompt = "Write me a joke"
    print(f"Prompt: {prompt}")
    response = model.generate(prompt)
    print(f"Response: {response}")


async def main_async():
    model = GoogleVertexAI(model_name="gemini-1.0-pro-002")
    prompt = "Write me a joke"
    print(f"Prompt: {prompt}")
    response = await model.a_generate(prompt)
    print(f"Response: {response}")


if __name__ == '__main__':
    main()
    # asyncio.run(main_async())

