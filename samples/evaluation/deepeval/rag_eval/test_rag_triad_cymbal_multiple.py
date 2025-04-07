import sys

from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ContextualRelevancyMetric
from deepeval.models import GeminiModel

sys.path.append("../../../../")
from utils import setup_rag_chain

# Using the RAG Triad for RAG evaluation:
# https://docs.confident-ai.com/docs/guides-rag-triad

EVAL_MODEL =  "gemini-1.5-pro"
PROJECT_ID = "genai-atamel"
LOCATION = "us-central1"

def test_rag_triad_cymbal_multiple():
    rag_chain = setup_rag_chain()

    inputs = [
        "What is the cargo capacity of Cymbal Starlight?",
        "Is there a tire repair kit in Cymbal Starlight?",
        "What's the emergency roadside assistance number for Cymbal?"
    ]

    test_cases = []

    for input in inputs:
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
        test_cases.append(test_case)

    print(f"Evaluating with model: {EVAL_MODEL}")
    eval_model = GeminiModel(
        model_name=EVAL_MODEL,
        project=PROJECT_ID,
        location=LOCATION
    )

    metrics = [
        AnswerRelevancyMetric(model=eval_model),
        FaithfulnessMetric(model=eval_model),
        ContextualRelevancyMetric(model=eval_model)
    ]

    evaluation_result = evaluate(test_cases=test_cases, metrics=metrics)



