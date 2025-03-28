import pandas
import sys
from vertexai.evaluation import EvalTask, PointwiseMetric, PointwiseMetricPromptTemplate

sys.path.append("../../../../../")
from samples.evaluation.vertexai_genai_eval.utils import print_eval_result

# Pointwise with a custom metric
# https://cloud.google.com/vertex-ai/generative-ai/docs/models/determine-eval#model-based-metrics
def main():

    responses = [
        "This is a funny and single sentence",
        "This is a funny sentence. But it's 2 sentences",
        "This is neither funny. Nor a single sentence"
    ]


    eval_dataset = pandas.DataFrame(
        {
            "response": responses,
        }
    )

    # Define a pointwise metric with two criteria
    custom_metric_prompt_template = PointwiseMetricPromptTemplate(
            criteria={
                "one_sentence": (
                    "The response is one short sentence."
                ),
                "entertaining": (
                    "The response is entertaining."
                ),
            },
            rating_rubric={
                "3": "The response performs well on both criteria.",
                "2": "The response performs well with only one of the criteria.",
                "1": "The response falls short on both criteria",
            },
        )

    print(f"custom_metric_prompt_template: {custom_metric_prompt_template}")

    custom_metric = PointwiseMetric(
        metric="custom_metric",
        metric_prompt_template=custom_metric_prompt_template
    )

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[custom_metric],
        experiment="pointwise-custom-metric"
    )

    eval_result = eval_task.evaluate()
    print_eval_result(eval_result)


if __name__ == "__main__":
    main()
