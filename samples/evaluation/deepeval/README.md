# DeepEval and Gemini

![DeepEval and Gemini](images/deepeval_gemini.png)

[DeepEval](https://docs.confident-ai.com/) is an open-source evaluation framework for LLMs. It allows to "unit test"
LLM outputs in a similar way to Pytest with 14+ LLM-evaluated metrics backed by research.

In this tutorial, you'll learn how to use DeepEval with Gemini running on Google AI and also Vertex AI.

## How to use DeepEval and Gemini

You can check out the [Gemini](https://www.deepeval.com/docs/metrics-introduction#gemini) documentation
of DeepEval to see how to use Gemini from DeepEval for evaluations. There are 2 ways to set Gemini 
as the evaluation model: from code or from command line.

## Vertex AI

To set Gemini on Vertex AI from code, create a `GeminiModel` with Vertex AI parameters and pass it to the metric in code: 

```python
from deepeval.models import GeminiModel

TEST_MODEL = "gemini-2.0-flash-001"
EVAL_MODEL =  "gemini-1.5-pro"

# Vertex AI parameters
PROJECT_ID = "genai-atamel"
LOCATION = "us-central1"

eval_model = GeminiModel(
    model_name=EVAL_MODEL,
    project=PROJECT_ID,
    location=LOCATION
)
metric = AnswerRelevancyMetric(
    model=eval_model,
    threshold=0.8)
```

Alternatively, you can set the evaluation model from the command line:

```console
deepeval set-gemini --model-name="gemini-1.5-pro" \
     --project-id="genai-atamel" \
     --location="us-central1"
```

The metric will use that model automatically:
```python
metric = AnswerRelevancyMetric(threshold=0.8)
```

## Google AI

To set Gemini on Google AI from code, create a `GeminiModel` with Google AI parameters and pass it to the metric in code: 

```python
from deepeval.models import GeminiModel

TEST_MODEL = "gemini-2.0-flash-001"
EVAL_MODEL =  "gemini-1.5-pro"

# Google AI parameters
GOOGLEAI_API_KEY = "your-google-ai-api-key"

eval_model = GeminiModel(
    model_name=EVAL_MODEL,
    api_key=GOOGLEAI_API_KEY
)
metric = AnswerRelevancyMetric(
    model=eval_model,
    threshold=0.8)
```

Alternatively, you can set the evaluation model from the command line:

```console
deepeval set-gemini --model-name="gemini-1.5-pro" \
     --google-api-key="your-google-ai-api-key"
```

The metric will use that model automatically:
```python
metric = AnswerRelevancyMetric(threshold=0.8)
```

## Answer relevancy

The [answer relevancy](https://docs.confident-ai.com/docs/metrics-answer-relevancy) metric measures the quality of your
RAG pipeline's generator by evaluating how relevant the actual_output of your LLM application is compared to the provided
input

To test answer relevancy with Vertex AI, take a look at [test_answer_relevancy.py](./test_answer_relevancy.py).

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

To test summarization with Vertex AI, take a look at [test_summarization.py](./test_summarization.py).

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
