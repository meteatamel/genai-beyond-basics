import os

from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ContextualRelevancyMetric
from deepeval import assert_test, evaluate

from vertex_ai.google_vertex_ai import GoogleVertexAI


# Using the RAG Triad for RAG evaluation:
# https://docs.confident-ai.com/docs/guides-rag-triad


def get_project_id():
    project_id = os.environ.get("GOOGLE_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_PROJECT_ID environment variable not set")
    return project_id


def test_rag_triad():
    test_case = LLMTestCase(
        input="I'm on an F-1 visa, how long can I stay in the US after graduation?",
        actual_output="You can stay up to 30 days after completing your degree.",
        retrieval_context=[
            """If you are in the U.S. on an F-1 visa, you are allowed to stay for 60 days after completing
            your degree, unless you have applied for and been approved to participate in OPT."""
        ]
    )


    eval_model = GoogleVertexAI(model_name="gemini-1.5-pro-002",
                           project=get_project_id(),
                           location="us-central1")

    answer_relevancy = AnswerRelevancyMetric(model=eval_model, threshold=0.8)
    faithfulness = FaithfulnessMetric(model=eval_model, threshold=1.0)
    contextual_relevancy = ContextualRelevancyMetric(model=eval_model, threshold=0.8)

    # Measure and print each metric individually
    # answer_relevancy.measure(test_case)
    # print(answer_relevancy.score)
    # print(answer_relevancy.reason)

    # Or, measure all metrics in parallel and print them
    # evaluate([test_case], [answer_relevancy, faithfulness, contextual_relevancy])

    # Or, measure all metrics in parallel as part of a test case that can pass/fail depending on each threshold
    assert_test(test_case, [answer_relevancy, faithfulness, contextual_relevancy])


