import pandas
import sys
from vertexai.evaluation import EvalTask
from vertexai.evaluation.constants import Metric

sys.path.append("../../../../")
from samples.evaluation.vertexai_genai_eval.utils import print_eval_result

# Exact match metric computes whether a generated text matches a reference text exactly.
# 0: No match
# 1: Match
def main():
    # Actual LLM responses
    responses = [
        "This will match",
        "This will not match",
    ]

    # Expected LLM responses
    references = [
        "This will match",
        "This won't match",
    ]

    eval_dataset = pandas.DataFrame(
        {
            "response": responses,
            "reference": references,
        }
    )

    metrics = [
        Metric.EXACT_MATCH,
    ]

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=metrics,
        experiment="exact-match-experiment"
    )

    eval_result = eval_task.evaluate()
    print_eval_result(eval_result)


if __name__ == "__main__":
    main()
