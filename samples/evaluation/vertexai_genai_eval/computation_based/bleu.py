import pandas
import sys
from vertexai.evaluation import EvalTask
from vertexai.evaluation.constants import Metric

sys.path.append("../../../../")
from samples.evaluation.vertexai_genai_eval.utils import print_eval_result

# Bleu (BiLingual Evaluation Understudy) metric evaluates the similarity between generated text and reference text.
# It measures precision (accuracy)
# A float in the range of [0,1]
# 0 means poor similarity. 1 represents a perfect match to the reference.
def main():
    # Actual LLM responses
    responses = [
        "Hello, how are you?",
        "I'm good"
    ]

    # Expected LLM responses
    references = [
        "Hello, how are you?",
        "I am good"
    ]

    eval_dataset = pandas.DataFrame(
        {
            "response": responses,
            "reference": references,
        }
    )

    metrics = [
        Metric.BLEU,
    ]

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=metrics,
        experiment="blue-experiment"
    )

    eval_result = eval_task.evaluate()
    print_eval_result(eval_result)


if __name__ == "__main__":
    main()
