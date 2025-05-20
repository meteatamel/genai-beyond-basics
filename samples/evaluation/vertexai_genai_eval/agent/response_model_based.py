import pandas
import sys
from vertexai.preview.evaluation import EvalTask, MetricPromptTemplateExamples

sys.path.append("../../../../")
from samples.evaluation.vertexai_genai_eval.utils import get_experiment_name, print_eval_result

# Final response evaluation: Evaluate the final output of an agent (whether the agent achieved its goal). It's very
# similar to the model evaluations.
# See: https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-agents

def main():
    prompts = [
        "Get price for smartphone",
        "Get product details and price for headphones",
        "Get details for usb charger",
        "Get product details and price for shoes",
        "Get product details for speaker?",
    ]

    responses = [
        "500",
        "50",
        "A super fast and light usb charger",
        "100",
        "A voice-controlled smart speaker that plays music, sets alarms, and controls smart home devices.",
    ]

    eval_dataset = pandas.DataFrame(
        {
            "prompt": prompts,
            "response": responses
        }
    )

    metrics = [
        # Fluency metric needs 'prompt' and 'response' columns
        MetricPromptTemplateExamples.Pointwise.FLUENCY,
    ]

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=metrics,
        experiment=get_experiment_name(__file__)
    )

    eval_result = eval_task.evaluate()
    print_eval_result(eval_result, colwidth=50)


if __name__ == "__main__":
    main()
