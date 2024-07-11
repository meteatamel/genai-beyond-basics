from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

from google_vertexai import GoogleVertexAI
from google_vertexai_langchain import GoogleVertexAILangChain


def test_google_vertexai():
    model = GoogleVertexAI(model_name="gemini-1.0-pro-002",
                           project="genai-atamel",
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


def test_google_vertexai_langchain():
    model = GoogleVertexAILangChain(model_name="gemini-1.0-pro-002",
                                    project="genai-atamel",
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