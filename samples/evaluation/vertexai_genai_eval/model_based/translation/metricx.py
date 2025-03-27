import pandas
import sys
from vertexai.evaluation import EvalTask
from vertexai.evaluation.metrics.pointwise_metric import MetricX

sys.path.append("../../../../../")
from samples.evaluation.vertexai_genai_eval.utils import print_eval_result

# MetricX is an open-source evaluation model for machine translation
# https://github.com/google-research/metricx
def main():
    # Source to translate
    sources = [
        "Dem Feuer konnte Einhalt geboten werden",
        "Schulen und Kindergärten wurden eröffnet.",
    ]

    # Actual LLM responses
    responses = [
        "The fire could be stopped",
        "Schools and kindergartens were open",
    ]

    # Expected LLM responses
    references = [
        "They were able to control the fire.",
        "Schools and kindergartens opened",
    ]

    eval_dataset = pandas.DataFrame(
        {
            "source": sources,
            "response": responses,
            "reference": references,
        }
    )

    metrics = [
        MetricX()
    ]

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=metrics,
        experiment="metricx"
    )

    eval_result = eval_task.evaluate()
    print_eval_result(eval_result)


if __name__ == "__main__":
    main()
