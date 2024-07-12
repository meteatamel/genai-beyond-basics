# DeepEval and Vertex AI

![DeepEval and Vertex AI](images/deepeval_vertexai.png)

[DeepEval](https://docs.confident-ai.com/) is an open-source evaluation framework for LLMs. It allows to "unit test" 
LLM outputs in a similar way to Pytest with 14+ LLM-evaluated metrics backed by research.

In this tutorial, you'll learn how to use DeepEval with Vertex AI.

## Set up DeepEval and Vertex AI

By default, DeepEval uses Open AI but it can be configured to use any LLM as explained in 
[Using a custom LLM](https://docs.confident-ai.com/docs/metrics-introduction#using-a-custom-llm) docs. To use a custom
LLM, you need to inherit `DeepEvalBaseLLM` class and implement its methods such as `get_model_name`, `load_model`, 
`generate` with your LLM.

There's  a [Google VertexAI Example](https://docs.confident-ai.com/docs/metrics-introduction#google-vertexai-example)
that shows how to implement DeepEval for Vertex AI. However, it unnecessarily uses LangChain and the implementation
seems  a little lacking.

Instead, I created 2 implementations of DeepEval for Vertex AI in [vertex_ai](./vertex_ai) folder:

1. [google_vertex_ai.py](./vertex_ai/google_vertex_ai.py) contains `GoogleVertexAI` class and it implements DeepEval
   with Vertex AI library.
2. [google_vertex_ai_langchain.py](./vertex_ai/google_vertex_ai_langchain.py) contains `GoogleVertexAILangChain` class 
    and it implements DeepEval via LangChain over Vertex AI library.

## How to use DeepEval and Vertex AI

To use the `GoogleVertexAI` class, you simply need to specify the model name, your project id, and location:

```python
from vertex_ai.google_vertex_ai import GoogleVertexAI

model = GoogleVertexAI(model_name="gemini-1.0-pro-002",
                       project="genai-atamel",
                       location="us-central1")
```

Then, you can pass the model to the metric you want to use in your tests:

```python
metric = AnswerRelevancyMetric(
    model=model,
    threshold=0.5)
```

The same applies to `GoogleVertexAILangChain` class.  Let's look at some test cases.

## Answer relevancy

The [answer relevancy](https://docs.confident-ai.com/docs/metrics-answer-relevancy) metric measures the quality of your
RAG pipeline's generator by evaluating how relevant the actual_output of your LLM application is compared to the provided 
input

To test answer relevancy with Vertex AI, take a look at [test_answer_relevancy.py](./test_answer_relevancy.py):

```python
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
```

Run it:

```shell
deepeval test run test_answer_relevancy.py
```

You should get a nice report on the outcome:

```shell
                                                                                                             Test Results                                                                                                              
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Test case                       ┃ Metric           ┃ Score                                                                                                                                          ┃ Status ┃ Overall Success Rate ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ test_answer_relevancy           │                  │                                                                                                                                                │        │ 100.0%               │
│                                 │ Answer Relevancy │ 1.0 (threshold=0.5, evaluation model=gemini-1.5-flash-001, reason=The score is 1.00 because the response perfectly addresses the input,        │ PASSED │                      │
│                                 │                  │ providing a clear and concise explanation for why the sky is blue!  Keep up the great work!, error=None)                                       │        │                      │
│                                 │                  │                                                                                                                                                │        │                      │
└─────────────────────────────────┴──────────────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴────────┴──────────────────────┘
```

## Summarization

The [summarization](https://docs.confident-ai.com/docs/metrics-summarization) metric uses LLMs to determine whether your
LLM (application) is generating factually correct summaries while including the necessary details from the original text

To test summarization with Vertex AI, take a look at [test_summarization.py](./test_summarization.py):

```python
def test_summarization():
    model = GoogleVertexAI(model_name="gemini-1.5-flash-001",
                           project=get_project_id(),
                           location="us-central1")

    input = """
    Please summarize the following:
    The 'coverage score' is calculated as the percentage of assessment questions
    for which both the summary and the original document provide a 'yes' answer. This
    method ensures that the summary not only includes key information from the original
    text but also accurately represents it. A higher coverage score indicates a
    more comprehensive and faithful summary, signifying that the summary effectively
    encapsulates the crucial points and details from the original content.
    """

    test_case = LLMTestCase(
        input=input,
        actual_output=model.generate(input))

    metric = SummarizationMetric(
        threshold=0.5,
        model=model,
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
```

Run it:

```shell
deepeval test run test_summarization.py
```

Result:

```shell
                                                                                                             Test Results                                                                                                              
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Test case          ┃ Metric        ┃ Score                                                                                                                                                          ┃ Status ┃ Overall Success Rate ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ test_summarization │               │                                                                                                                                                                │        │ 100.0%               │
│                    │ Summarization │ 0.67 (threshold=0.5, evaluation model=gemini-1.5-flash-001, reason=The score is 0.67 because the summary fails to answer a question that the original text can │ PASSED │                      │
│                    │               │ answer. It is not clear from the summary whether the coverage score is calculated based on the percentage of 'yes' answers, but this information is present in │        │                      │
│                    │               │ the original text., error=None)                                                                                                                                │        │                      │
└────────────────────┴───────────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴────────┴──────────────────────┘
```

## Hallucination

The [hallucination](https://docs.confident-ai.com/docs/metrics-hallucination) metric determines whether your LLM generates
factually correct information by comparing the `actual_output` to the provided context.

To test hallucination with Vertex AI, take a look at [test_hallucination.py](./test_hallucination.py).

This makes sure the LLM does not hallucinate:

```python
def test_hallucination():
    model = GoogleVertexAI(model_name="gemini-1.5-flash-001",
                           project=get_project_id(),
                           location="us-central1")

    context = [
        "Paris is the capital of France."
    ]

    input = "What's the capital of France?"

    test_case = LLMTestCase(
        input=input,
        actual_output=model.generate(input),
        context=context
    )

    metric = HallucinationMetric(
        model=model,
        threshold=0.5)

    metric.measure(test_case)
    print(f"Metric score: {metric.score}")
    print(f"Metric reason: {metric.reason}")

    assert_test(test_case, [metric])
```

You can also trick the LLM and give a wrong context to see that the hallucination test fails:

```python
def test_hallucination_fails():
    model = GoogleVertexAI(model_name="gemini-1.5-flash-001",
                           project=get_project_id(),
                           location="us-central1")

    context = [
        "London is the capital of France."
    ]

    input = "What's the capital of France?"

    test_case = LLMTestCase(
        input=input,
        actual_output=model.generate(input),
        context=context
    )

    metric = HallucinationMetric(
        model=model,
        threshold=0.5)

    metric.measure(test_case)
    print(f"Metric score: {metric.score}")
    print(f"Metric reason: {metric.reason}")
```

Run it:

```shell
deepeval test run test_hallucination.py
```

Result:

```shell
                                                                                                             Test Results                                                                                                              
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Test case                ┃ Metric        ┃ Score                                                                                                                                                    ┃ Status ┃ Overall Success Rate ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ test_hallucination       │               │                                                                                                                                                          │        │ 100.0%               │
│                          │ Hallucination │ 0.0 (threshold=0.5, evaluation model=gemini-1.5-flash-001, reason=The score is 0.00 because the output aligns with the provided context, indicating no   │ PASSED │                      │
│                          │               │ hallucinations., error=None)                                                                                                                             │        │                      │
│                          │               │                                                                                                                                                          │        │                      │
│ test_hallucination_fails │               │                                                                                                                                                          │        │ 0.0%                 │
│                          │ Hallucination │ 1.0 (threshold=0.5, evaluation model=gemini-1.5-flash-001, reason=The score is 1.00 because the output contradicts a key fact from the context, stating  │ FAILED │                      │
│                          │               │ that London is the capital of France, which is incorrect. This indicates a significant hallucination., error=None)                                       │        │                      │
└──────────────────────────┴───────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴────────┴──────────────────────┘
```

DeepEval have more metrics you can check out on their [Metrics](https://docs.confident-ai.com/docs/metrics-introduction)
page.