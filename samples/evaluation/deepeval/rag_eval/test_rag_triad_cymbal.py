import sys

from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ContextualRelevancyMetric

sys.path.append("../../../../")
from samples.evaluation.deepeval.vertex_ai.google_vertex_ai import GoogleVertexAI
from utils import get_project_id, setup_rag_chain

# Using the RAG Triad for RAG evaluation:
# https://docs.confident-ai.com/docs/guides-rag-triad

CHAT_MODEL_NAME = "gemini-1.5-flash-002"
EVAL_MODEL_NAME = "gemini-1.5-pro-002"

def test_rag_triad_cymbal():
    rag_chain = setup_rag_chain(CHAT_MODEL_NAME)

    input = "What is the cargo capacity of Cymbal Starlight?"
    print(f"Input: {input}")

    print("Invoking RAG chain")
    response = rag_chain.invoke({"input": input})

    output = response['answer']
    print(f"Output: {output}")

    retrieval_context = [doc.page_content for doc in response['context']]
    print(f"Retrieval context: {retrieval_context}")

    test_case = LLMTestCase(
        input=input,
        actual_output=output,
        retrieval_context=retrieval_context
    )

    print(f"Evaluating with model: {EVAL_MODEL_NAME}")
    eval_model = GoogleVertexAI(model_name=EVAL_MODEL_NAME,
                           project=get_project_id(),
                           location="us-central1")

    answer_relevancy = AnswerRelevancyMetric(model=eval_model)
    faithfulness = FaithfulnessMetric(model=eval_model)
    contextual_relevancy = ContextualRelevancyMetric(model=eval_model)

    assert_test(test_case, [answer_relevancy, faithfulness, contextual_relevancy])



