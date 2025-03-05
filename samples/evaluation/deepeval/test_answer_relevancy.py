import os

from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

from vertex_ai.google_vertex_ai import GoogleVertexAI
from vertex_ai.google_vertex_ai_langchain import GoogleVertexAILangChain

from utils import get_project_id

# The answer relevancy metric measures the quality of your RAG pipeline's generator by evaluating how relevant the
# actual_output of your LLM application is compared to the provided input
# https://docs.confident-ai.com/docs/metrics-answer-relevancy

TEST_MODEL = "gemini-2.0-flash-001"
EVAL_MODEL = "gemini-2.0-pro-exp-02-05"
LOCATION = "us-central1"

def test_answer_relevancy():
    test_model = GoogleVertexAI(model_name=TEST_MODEL,
                           project=get_project_id(),
                           location=LOCATION)

    input = "Why is sky blue?"

    test_case = LLMTestCase(
        input=input,
        actual_output=test_model.generate(input)
    )

    eval_model = GoogleVertexAI(model_name=EVAL_MODEL,
                           project=get_project_id(),
                           location=LOCATION)

    metric = AnswerRelevancyMetric(
        model=eval_model,
        threshold=0.5)

    assert_test(test_case, [metric])



