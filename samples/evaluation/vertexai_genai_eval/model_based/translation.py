import pandas
import sys
from vertexai.evaluation import EvalTask
from vertexai.evaluation.metrics.pointwise_metric import Comet, MetricX

sys.path.append("../../../../")
from samples.evaluation.vertexai_genai_eval.utils import get_experiment_name,  print_eval_result

# Model-based metrics specifically for translation related tasks.
# See: https://cloud.google.com/vertex-ai/generative-ai/docs/models/determine-eval#translation-models
def main():
    sources = [
        "Dem Feuer konnte Einhalt geboten werden",
        "Schulen und Kindergärten wurden eröffnet.",
    ]

    responses = [
        "The fire could be stopped",
        "Schools and kindergartens were open",
    ]

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
        # COMET is an open-source evaluation model for machine translation
        # https://huggingface.co/Unbabel/wmt22-comet-da
        Comet(),

        # MetricX is an open-source evaluation model for machine translation
        # https://github.com/google-research/metricx
        MetricX()
    ]

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=metrics,
        experiment=get_experiment_name(__file__)
    )

    eval_result = eval_task.evaluate()
    print_eval_result(eval_result)


if __name__ == "__main__":
    main()
