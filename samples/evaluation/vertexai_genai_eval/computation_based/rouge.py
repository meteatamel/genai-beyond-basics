import pandas
import sys
from vertexai.evaluation import EvalTask
from vertexai.evaluation.constants import Metric

sys.path.append("../../../../")
from samples.evaluation.vertexai_genai_eval.utils import print_eval_result

# Rouge (Recall-Oriented Understudy for Gisting Evaluation) metric evaluates text summaries
# It measures recall (completeness)
# A float in the range of [0,1]
# 0 means poor similarity. 1 means strong similarity between response and reference.
def main():
    # Actual LLM responses
    responses = [
        "The cat lay on the mat.",
        "I am good"
    ]

    # Expected LLM responses
    references = [
        "The cat sat on the mat.",
        "I'm good"
    ]

    eval_dataset = pandas.DataFrame(
        {
            "response": responses,
            "reference": references,
        }
    )

    metrics = [
        Metric.ROUGE,
        # Metric.ROUGE_1,
        # Metric.ROUGE_2,
        # Metric.ROUGE_L,
        # Metric.ROUGE_L_SUM
    ]

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=metrics,
        experiment="rouge"
    )

    eval_result = eval_task.evaluate()
    print_eval_result(eval_result)


if __name__ == "__main__":
    main()
