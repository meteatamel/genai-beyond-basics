import os

from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

from vertex_ai.google_vertex_ai import GoogleVertexAI
from vertex_ai.google_vertex_ai_langchain import GoogleVertexAILangChain

# The answer relevancy metric measures the quality of your RAG pipeline's generator by evaluating how relevant the
# actual_output of your LLM application is compared to the provided input
# https://docs.confident-ai.com/docs/metrics-answer-relevancy


def get_project_id():
    project_id = os.environ.get("GOOGLE_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_PROJECT_ID environment variable not set")
    return project_id


def test_answer_relevancy():
    model = GoogleVertexAI(model_name="gemini-1.5-flash-001",
                           project=get_project_id(),
                           location="us-central1")

    input = "Why is sky blue?"

    test_case = LLMTestCase(
        input=input,
        actual_output=model.generate(input)
    )

    metric = AnswerRelevancyMetric(
        model=model,
        threshold=0.5)

    assert_test(test_case, [metric])


def test_answer_relevancy_langchain():
    model = GoogleVertexAILangChain(model_name="gemini-1.0-pro-002",
                                    project=get_project_id(),
                                    location="us-central1")

    input = "Why is sky blue?"

    test_case = LLMTestCase(
        input=input,
        actual_output=model.generate(input)
    )

    metric = AnswerRelevancyMetric(
        model=model,
        threshold=0.5)

    assert_test(test_case, [metric])

