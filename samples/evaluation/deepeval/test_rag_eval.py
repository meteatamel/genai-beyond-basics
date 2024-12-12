import os

from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric,
    FaithfulnessMetric
)

from deepeval import assert_test

from vertex_ai.google_vertex_ai import GoogleVertexAI


# RAG evaluation
# https://docs.confident-ai.com/docs/guides-rag-evaluation


def get_project_id():
    project_id = os.environ.get("GOOGLE_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_PROJECT_ID environment variable not set")
    return project_id


def test_rag_retrieval():
    test_case = LLMTestCase(
        input="I'm on an F-1 visa, how long can I stay in the US after graduation?",
        actual_output="You can stay up to 30 days after completing your degree.",
        expected_output="You can stay up to 60 days after completing your degree.",
        retrieval_context=[
            """If you are in the U.S. on an F-1 visa, you are allowed to stay for 60 days after completing
            your degree, unless you have applied for and been approved to participate in OPT."""
        ]
    )

    eval_model = GoogleVertexAI(model_name="gemini-1.5-pro-002",
                           project=get_project_id(),
                           location="us-central1")

    contextual_precision = ContextualPrecisionMetric(model=eval_model)
    contextual_recall = ContextualRecallMetric(model=eval_model)
    contextual_relevancy = ContextualRelevancyMetric(model=eval_model)

    assert_test(test_case, [contextual_precision, contextual_recall, contextual_relevancy])


def test_rag_generation():
    test_case = LLMTestCase(
        input="I'm on an F-1 visa, how long can I stay in the US after graduation?",
        actual_output="You can stay up to 30 days after completing your degree.",
        expected_output="You can stay up to 60 days after completing your degree.",
        retrieval_context=[
            """If you are in the U.S. on an F-1 visa, you are allowed to stay for 60 days after completing
            your degree, unless you have applied for and been approved to participate in OPT."""
        ]
    )

    eval_model = GoogleVertexAI(model_name="gemini-1.5-pro-002",
                           project=get_project_id(),
                           location="us-central1")

    answer_relevancy = AnswerRelevancyMetric(model=eval_model)
    faithfulness = FaithfulnessMetric(model=eval_model)

    assert_test(test_case, [answer_relevancy, faithfulness])

