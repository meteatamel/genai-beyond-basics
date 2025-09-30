from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.models import GeminiModel
from google import genai

# The answer relevancy metric measures the quality of your RAG pipeline's generator by evaluating how relevant the
# actual_output of your LLM application is compared to the provided input
# https://docs.confident-ai.com/docs/metrics-answer-relevancy

TEST_MODEL = "gemini-2.0-flash"
EVAL_MODEL =  "gemini-2.0-flash"

# Vertex AI parameters
PROJECT_ID = "genai-atamel"
LOCATION = "us-central1"

def test_vertexai():
    # Generate response from the test model as usual
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION
    )

    input = "Why is sky blue?"

    response = client.models.generate_content(
        model=TEST_MODEL,
        contents=input
    )

    test_case = LLMTestCase(
        input=input,
        actual_output=response.text,
    )

    # Set the evaluation model in code:
    eval_model = GeminiModel(
        model_name=EVAL_MODEL,
        project=PROJECT_ID,
        location=LOCATION
    )
    metric = AnswerRelevancyMetric(
        model=eval_model,
        threshold=0.8)

    # Or you can set/unset the evaluation model from the command line:
    # deepeval set-gemini --model-name="gemini-1.5-pro" \
    #     --project-id="genai-atamel" \
    #     --location="us-central1"
    #
    # deepeval unset-gemini
    #
    # metric = AnswerRelevancyMetric(threshold=0.8)

    assert_test(test_case, [metric])

# Google AI parameters
GOOGLEAI_API_KEY = "your-google-ai-api-key"

def test_google_ai():
    # Generate response from the test model as usual
    client = genai.Client(
        api_key=GOOGLEAI_API_KEY
    )

    input = "Why is sky blue?"

    response = client.models.generate_content(
        model=TEST_MODEL,
        contents=input
    )

    test_case = LLMTestCase(
        input=input,
        actual_output=response.text,
    )

    # Set the evaluation model in code:
    eval_model = GeminiModel(
        model_name=EVAL_MODEL,
        api_key=GOOGLEAI_API_KEY
    )
    metric = AnswerRelevancyMetric(
        model=eval_model,
        threshold=0.8)

    # Or you can set/unset the evaluation model from the command line:
    # deepeval set-gemini --model-name="gemini-1.5-pro" \
    #     --google-api-key="your-google-ai-api-key"
    #
    # deepeval unset-gemini
    #
    # metric = AnswerRelevancyMetric(threshold=0.8)

    assert_test(test_case, [metric])



