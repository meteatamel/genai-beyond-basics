import os

from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import HallucinationMetric

from vertex_ai.google_vertex_ai import GoogleVertexAI

# The hallucination metric determines whether your LLM generates factually correct information by comparing the
# actual_output to the provided context.
# https://docs.confident-ai.com/docs/metrics-hallucination


def get_project_id():
    project_id = os.environ.get("GOOGLE_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_PROJECT_ID environment variable not set")
    return project_id


def test_hallucination():
    model = GoogleVertexAI(model_name="gemini-1.5-flash-001",
                           project=get_project_id(),
                           location="us-central1")

    context = [
        "Paris is the capital of France."
    ]

    input = "What's the capital of France?"

    test_case = LLMTestCase(
        input=input,
        actual_output=model.generate(input),
        context=context
    )

    metric = HallucinationMetric(
        model=model,
        threshold=0.5)

    metric.measure(test_case)
    print(f"Metric score: {metric.score}")
    print(f"Metric reason: {metric.reason}")

    assert_test(test_case, [metric])


def test_hallucination_fails():
    model = GoogleVertexAI(model_name="gemini-1.5-flash-001",
                           project=get_project_id(),
                           location="us-central1")

    context = [
        "London is the capital of France."
    ]

    input = "What's the capital of France?"

    test_case = LLMTestCase(
        input=input,
        actual_output=model.generate(input),
        context=context
    )

    metric = HallucinationMetric(
        model=model,
        threshold=0.5)

    metric.measure(test_case)
    print(f"Metric score: {metric.score}")
    print(f"Metric reason: {metric.reason}")

    assert_test(test_case, [metric])
