import sys

from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (AnswerRelevancyMetric, ContextualPrecisionMetric, ContextualRecallMetric,
                              ContextualRelevancyMetric, FaithfulnessMetric)

sys.path.append("../../../../")
from samples.evaluation.deepeval.vertex_ai.google_vertex_ai import GoogleVertexAI
from samples.evaluation.deepeval.utils import get_project_id

# RAG evaluation
# https://docs.confident-ai.com/docs/guides-rag-evaluation

def get_test_case(expected_output=None):
    return LLMTestCase(
        input="I'm on an F-1 visa, how long can I stay in the US after graduation?",
        actual_output="You can stay up to 30 days after completing your degree.",
        expected_output=expected_output,
        retrieval_context=[
            """If you are in the U.S. on an F-1 visa, you are allowed to stay for 60 days after completing
            your degree, unless you have applied for and been approved to participate in OPT."""
        ]
    )

EVAL_MODEL_NAME = "gemini-1.5-pro-002"

def get_eval_model():
    return GoogleVertexAI(
        model_name=EVAL_MODEL_NAME,
        project=get_project_id(),
        location="us-central1"
    )

def test_retrieval():
    test_case = get_test_case(
        expected_output="You can stay up to 60 days after completing your degree."
    )
    eval_model = get_eval_model()

    metrics = [
        ContextualPrecisionMetric(model=eval_model),
        ContextualRecallMetric(model=eval_model),
        ContextualRelevancyMetric(model=eval_model)
    ]

    assert_test(test_case, metrics)


def test_generation():
    test_case = get_test_case()
    eval_model = get_eval_model()

    metrics = [
        AnswerRelevancyMetric(model=eval_model),
        FaithfulnessMetric(model=eval_model)
    ]

    assert_test(test_case, metrics)

