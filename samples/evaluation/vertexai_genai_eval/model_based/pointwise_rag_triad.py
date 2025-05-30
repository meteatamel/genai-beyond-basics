import pandas
import sys
from vertexai.evaluation import (
    EvalTask,
    PointwiseMetric,
    PointwiseMetricPromptTemplate,
)

sys.path.append("../../../../")
from samples.evaluation.vertexai_genai_eval.utils import get_experiment_name, print_eval_result

# An attempt to implement the RAG triad metrics: answer relevance, context relevance, groundedness:
# See: https://atamel.dev/posts/2025/01-09_evaluating_rag_pipelines/

answer_relevance_metric = PointwiseMetric(
    metric="answer_relevance",
    metric_prompt_template=PointwiseMetricPromptTemplate(
        criteria={
            "answer_relevance": (
                "Only check response and prompt. Ignore context. Is the response relevant to the prompt?"
            ),
        },
        metric_definition="Answer relevance: Checks to see if the response is relevant to the prompt",
        rating_rubric={
            "4": "The response is totally relevant to the prompt",
            "3": "The response is somewhat relevant to the prompt",
            "2": "The response is somewhat irrelevant to the prompt",
            "1": "The response is totally irrelevant to the prompt",
        },
        input_variables=["prompt"]
    )
)
# print(f"Metric prompt template: {answer_relevance_metric.metric_prompt_template}")

def answer_relevance():
    prompts = [
        "What is Cymbal Starlight?",
        "Where is the cargo area located?",
    ]

    responses = [
        "Sky is blue",  # Bad answer_relevance
        "The cargo area located in the trunk of the vehicle",  # Good answer_relevance
    ]

    eval_dataset = pandas.DataFrame(
        {
            "prompt": prompts,
            "response": responses,
        }
    )

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[answer_relevance_metric],
        experiment=get_experiment_name(__file__, "answer-relevance")
    )
    eval_result = eval_task.evaluate()
    print_eval_result(eval_result, colwidth=50)


context_relevance_metric = PointwiseMetric(
    metric="context_relevance",
    metric_prompt_template=PointwiseMetricPromptTemplate(
        criteria={
            "context_relevance": (
                "Only check context and prompt. Ignore response. Is the context relevant to the prompt?"
            ),
        },
        metric_definition="Context relevance: Check to see if the context is relevant to the prompt",
        rating_rubric={
            "4": "The context is totally relevant to the prompt",
            "3": "The context is somewhat relevant to the prompt",
            "2": "The context is somewhat irrelevant to the prompt",
            "1": "The context is totally irrelevant to the prompt",
        },
        input_variables=["prompt", "context"]
    )
)
# print(f"Metric prompt template: {context_relevance_metric.metric_prompt_template}")

def context_relevance():
    prompts = [
        "What is Cymbal Starlight?",
        "Where is the cargo area located?",
    ]

    contexts = [
        "Cymbal Starlight is a year 2024 car model", # Good context_relevance
        "Maintain tire pressure at all times",  # Bad context_relevance
    ]

    responses = [
        "Cymbal Starlight is a car",
        "The cargo area located in the trunk of the vehicle",
    ]

    eval_dataset = pandas.DataFrame(
        {
            "prompt": prompts,
            "context": contexts,
            "response": responses,
        }
    )

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[context_relevance_metric],
        experiment=get_experiment_name(__file__, "context-relevance")
    )
    eval_result = eval_task.evaluate()
    print_eval_result(eval_result, colwidth=50)


groundedness_metric = PointwiseMetric(
    metric="groundedness",
    metric_prompt_template=PointwiseMetricPromptTemplate(
        criteria={
            "groundedness": (
                "Only check context and response. Ignore prompt. Is the response supported by the context?"
            ),
        },
        metric_definition="Groundedness: Check to see if the response is supported by the context",
        rating_rubric={
            "4": "The response is totally supported by the context",
            "3": "The response is somewhat supported by the context",
            "2": "The response is somewhat not supported by the context",
            "1": "The response is totally not supported by the context",
        },
        input_variables=["prompt", "context"]
    )
)
#print(f"Metric prompt template: {groundedness_metric.metric_prompt_template}")

def groundedness():
    prompts = [
        "What is Cymbal Starlight?",
        "Where is the cargo area located?",
    ]

    contexts = [
        "Cymbal Starlight is a year 2024 car model",
        "The cargo area located in the trunk of the vehicle",
    ]

    responses = [
        "Cymbal Starlight is a car", # Good groundedness
        "The cargo area located in the front of the vehicle", # Bad groundedness
    ]

    eval_dataset = pandas.DataFrame(
        {
            "prompt": prompts,
            "context": contexts,
            "response": responses,
        }
    )

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[groundedness_metric],
        experiment=get_experiment_name(__file__, "groundedness")
    )
    eval_result = eval_task.evaluate()
    print_eval_result(eval_result, colwidth=50)


def all_metrics():
    prompts = [
        "What is Cymbal Starlight?",
        "Does Cymbal have an Anti-Lock braking system?",
        "Where is the cargo area located?",
        "What is the cargo capacity of Cymbal Starlight?"
    ]

    contexts = [
        "Cymbal Starlight is a year 2024 car model",
        "Maintain tire pressure at all times",  # (Bad) context_relevance
        "The cargo area is located in the trunk of\nthe vehicle.",
        "Cargo\nThe Cymbal Starlight 2024 has a cargo capacity of 13.5 cubic feet."  # (Good) context_relevance
    ]

    responses = [
        "Sky is blue",  # (Bad) answer_relevance
        "The Cymbal Starlight 2024 has a cargo capacity of 13.5 cubic feet.",
        "The cargo area located in the front of the vehicle",  # (Bad) groundedness
        "The Cymbal Starlight 2024 has a cargo capacity of 13.5 cubic feet."  # (Good) answer_relevance and groundedness
    ]

    eval_dataset = pandas.DataFrame(
        {
            "prompt": prompts,
            "context": contexts,
            "response": responses,
        }
    )

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[answer_relevance_metric, context_relevance_metric, groundedness_metric],
        experiment=get_experiment_name(__file__)
    )

    eval_result = eval_task.evaluate()
    print_eval_result(eval_result)


if __name__ == "__main__":
    globals()[sys.argv[1]]()
