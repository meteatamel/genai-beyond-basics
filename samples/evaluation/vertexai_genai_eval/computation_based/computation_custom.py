import pandas as pd
import sys
from vertexai.evaluation import EvalTask, CustomMetric

sys.path.append("../../../../")
from samples.evaluation.vertexai_genai_eval.utils import print_eval_result

# A sample custom computation-based metric to count the number of words
# See: https://github.com/GoogleCloudPlatform/generative-ai/blob/6424f10b0ed5a2a31801173ea407d356d299a852/gemini/evaluation/bring_your_own_computation_based_metric.ipynb
def word_count(instance: dict[str, str]) -> dict[str, float]:
    """Count the number of words in the response."""

    response = instance["response"]
    score = len(response.split(" "))

    return {
        "word_count": score,
    }


def main():
    responses = [
        "Hello, how are you?",
        "I'm good",
        "The cat lay on the mat."
    ]

    eval_dataset = pd.DataFrame(
        {
            "response": responses,
        }
    )

    custom_word_count_metric = CustomMetric(
        name="word_count",
        metric_function=word_count)

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[custom_word_count_metric],
        experiment="computation-custom"
    )

    eval_result = eval_task.evaluate()
    print_eval_result(eval_result)


if __name__ == "__main__":
    main()
