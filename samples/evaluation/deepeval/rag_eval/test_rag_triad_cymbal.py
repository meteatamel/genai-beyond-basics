import sys

from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ContextualRelevancyMetric
from deepeval.models import GeminiModel

sys.path.append("../../../../")
from utils import setup_rag_chain

# Using the RAG Triad for RAG evaluation:
# https://docs.confident-ai.com/docs/guides-rag-triad

EVAL_MODEL =  "gemini-2.0-pro"
PROJECT_ID = "genai-atamel"
LOCATION = "us-central1"

def test_rag_triad_cymbal():
    rag_chain = setup_rag_chain()

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

    print(f"Evaluating with model: {EVAL_MODEL}")
    eval_model = GeminiModel(
        model_name=EVAL_MODEL,
        project=PROJECT_ID,
        location=LOCATION
    )

    answer_relevancy = AnswerRelevancyMetric(model=eval_model)
    faithfulness = FaithfulnessMetric(model=eval_model)
    contextual_relevancy = ContextualRelevancyMetric(model=eval_model)

    assert_test(test_case, [answer_relevancy, faithfulness, contextual_relevancy])



