import os

from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import HallucinationMetric

from vertex_ai.google_vertex_ai import GoogleVertexAI

from utils import get_project_id

# The hallucination metric determines whether your LLM generates factually correct information by comparing the
# actual_output to the provided context.
# https://docs.confident-ai.com/docs/metrics-hallucination

TEST_MODEL = "gemini-2.0-flash-001"
EVAL_MODEL = "gemini-2.0-pro-exp-02-05"
LOCATION = "us-central1"

def test_hallucination():
    test_model = GoogleVertexAI(model_name=TEST_MODEL,
                           project=get_project_id(),
                           location=LOCATION)

    context = [
        "Paris is the capital of France."
    ]

    input = "What's the capital of France?"

    test_case = LLMTestCase(
        input=input,
        actual_output=test_model.generate(input),
        context=context
    )

    eval_model = GoogleVertexAI(model_name=EVAL_MODEL,
                           project=get_project_id(),
                           location=LOCATION)

    metric = HallucinationMetric(
        model=eval_model,
        threshold=0.5)

    metric.measure(test_case)
    print(f"Metric score: {metric.score}")
    print(f"Metric reason: {metric.reason}")

    assert_test(test_case, [metric])


def test_hallucination_fails():
    test_model = GoogleVertexAI(model_name=TEST_MODEL,
                           project=get_project_id(),
                           location=LOCATION)

    context = [
        "London is the capital of France."
    ]

    input = "What's the capital of France?"

    test_case = LLMTestCase(
        input=input,
        actual_output=test_model.generate(input),
        context=context
    )

    eval_model = GoogleVertexAI(model_name=EVAL_MODEL,
                           project=get_project_id(),
                           location=LOCATION)

    metric = HallucinationMetric(
        model=eval_model,
        threshold=0.5)

    metric.measure(test_case)
    print(f"Metric score: {metric.score}")
    print(f"Metric reason: {metric.reason}")

    assert_test(test_case, [metric])
