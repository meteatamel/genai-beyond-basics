import pandas
import sys
from vertexai.evaluation import EvalTask
from vertexai.evaluation.metrics import CustomMetric

sys.path.append("../../../../")
from samples.evaluation.vertexai_genai_eval.utils import get_experiment_name, print_eval_result

# Define a custom computation-based metric to check if all the required tools are called
# See: https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-agents#metric_customization

def essential_tools_present(instance, required_tools = ["loc_to_lat_long", "lat_long_to_weather"]):
    trajectory = instance["predicted_trajectory"]
    tools_present = [tool_used['tool_name'] for tool_used in trajectory]
    if len(required_tools) == 0:
      return {"custom_essential_tools_present_metric": 1}
    score = 0
    for tool in required_tools:
      if tool in tools_present:
        score += 1
    return {
        "custom_essential_tools_present_metric": score/len(required_tools),
    }

def main():
    predicted_trajectory = [
        # example 1
        [
            {
                "tool_name": "loc_to_lat_long",
                "tool_input": {
                    "location": "London"
                }
            },
            {
                "tool_name": "lat_long_to_weather",
                "tool_input": {
                    "longitude": "-0.12574",
                    "latitude": "51.50853"
                }
            }
        ],
        # example 2
        [
            {
                "tool_name": "loc_to_lat_long",
                "tool_input": {
                    "location": "Paris"
                }
            },
        ]
    ]

    custom_metric = CustomMetric(
        name="custom_essential_tools_present_metric",
        metric_function=essential_tools_present)

    eval_dataset = pandas.DataFrame(
        {
            "predicted_trajectory": predicted_trajectory,
        }
    )

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[custom_metric],
        experiment=get_experiment_name(__file__)
    )

    eval_result = eval_task.evaluate()
    print_eval_result(eval_result)


if __name__ == "__main__":
    main()
