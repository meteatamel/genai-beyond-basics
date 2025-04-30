import pandas
import sys
from vertexai.evaluation import EvalTask
from vertexai.evaluation.constants import Metric

sys.path.append("../../../../")
from samples.evaluation.vertexai_genai_eval.utils import get_experiment_name, print_eval_result

# Computation based metrics
# See: https://cloud.google.com/vertex-ai/generative-ai/docs/models/determine-eval#computation-based-metrics
def main():
    responses = [
        "Hello, how are you?",
        "I'm good",
        "The cat lay on the mat."
    ]

    references = [
        "Hello, how are you?",
        "I am good",
        "The cat sat on the mat."
    ]

    eval_dataset = pandas.DataFrame(
        {
            "response": responses,
            "reference": references,
        }
    )

    metrics = [
        # Exact match metric computes whether a generated text matches a reference text exactly.
        # 0: No match, 1: Match
        Metric.EXACT_MATCH,

        # Bleu (BiLingual Evaluation Understudy) metric evaluates the similarity between generated text and reference text.
        # It measures precision (accuracy)
        # A float in the range of [0,1]
        # 0: Poor similarity, 1: Perfect match to reference
        Metric.BLEU,

        # Rouge (Recall-Oriented Understudy for Gisting Evaluation) metric evaluates text summaries.
        # It measures recall (completeness)
        # A float in the range of [0,1]
        # 0: Poor similarity, 1: Strong similarity to reference.
        Metric.ROUGE,
        # Metric.ROUGE_1,
        # Metric.ROUGE_2,
        # Metric.ROUGE_L,
        # Metric.ROUGE_L_SUM
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
