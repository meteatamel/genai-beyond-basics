from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import SummarizationMetric
from deepeval.models import GeminiModel
from google import genai

# The summarization metric uses LLMs to determine whether your LLM (application) is generating factually correct
# summaries while including the necessary details from the original text
# https://docs.confident-ai.com/docs/metrics-summarization

TEST_MODEL = "gemini-2.0-flash-001"
EVAL_MODEL =  "gemini-1.5-pro"
PROJECT_ID = "genai-atamel"
LOCATION = "us-central1"

def test_summarization():
    # Generate response from the test model as usual
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION
    )

    input = """
    Please summarize the following:
    The 'coverage score' is calculated as the percentage of assessment questions
    for which both the summary and the original document provide a 'yes' answer. This
    method ensures that the summary not only includes key information from the original
    text but also accurately represents it. A higher coverage score indicates a
    more comprehensive and faithful summary, signifying that the summary effectively
    encapsulates the crucial points and details from the original content.
    """

    response = client.models.generate_content(
        model=TEST_MODEL,
        contents=input
    )

    test_case = LLMTestCase(
        input=input,
        actual_output=response.text,
    )

    # Set the evaluation model in code:
    eval_model = GeminiModel(
        model_name=EVAL_MODEL,
        project=PROJECT_ID,
        location=LOCATION
    )

    metric = SummarizationMetric(
        threshold=0.8,
        model=eval_model,
        assessment_questions=[
            "Is the coverage score based on a percentage of 'yes' answers?",
            "Does the score ensure the summary's accuracy with the source?",
            "Does a higher score mean a more comprehensive summary?"
        ]
    )

    metric.measure(test_case)
    print(f"Metric score: {metric.score}")
    print(f"Metric reason: {metric.reason}")

    assert_test(test_case, [metric])
