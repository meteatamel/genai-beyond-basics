from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import HallucinationMetric
from deepeval.models import GeminiModel
from google import genai

# The hallucination metric determines whether your LLM generates factually correct information by comparing the
# actual_output to the provided context.
# https://docs.confident-ai.com/docs/metrics-hallucination

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

    context = [
        "Paris is the capital of France."
    ]

    input = "What's the capital of France?"

    response = client.models.generate_content(
        model=TEST_MODEL,
        contents=input
    )

    test_case = LLMTestCase(
        input=input,
        actual_output=response.text,
        context=context
    )

    # Set the evaluation model in code:
    eval_model = GeminiModel(
        model_name=EVAL_MODEL,
        project=PROJECT_ID,
        location=LOCATION
    )

    metric = HallucinationMetric(
        model=eval_model,
        threshold=0.8)

    metric.measure(test_case)
    print(f"Metric score: {metric.score}")
    print(f"Metric reason: {metric.reason}")

    assert_test(test_case, [metric])


def test_vertexai_fails():
    # Generate response from the test model as usual
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION
    )

    context = [
        "London is the capital of France."
    ]

    input = "What's the capital of France?"

    response = client.models.generate_content(
        model=TEST_MODEL,
        contents=input
    )

    test_case = LLMTestCase(
        input=input,
        actual_output=response.text,
        context=context
    )

    # Set the evaluation model in code:
    eval_model = GeminiModel(
        model_name=EVAL_MODEL,
        project=PROJECT_ID,
        location=LOCATION
    )

    metric = HallucinationMetric(
        model=eval_model,
        threshold=0.8)

    metric.measure(test_case)
    print(f"Metric score: {metric.score}")
    print(f"Metric reason: {metric.reason}")

    assert_test(test_case, [metric])
