import pandas
import sys
from vertexai.evaluation import EvalTask
from vertexai.evaluation.metrics import CustomMetric
from vertexai.evaluation import PointwiseMetric, PointwiseMetricPromptTemplate

sys.path.append("../../../../")
from samples.evaluation.vertexai_genai_eval.utils import print_eval_result

# Custom metrics to evaluate agents
# See: https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-agents#metric_customization

# Define a custom trajectory metric with the prompt template
def custom_trajectory_metric():
    # prompt = [
    #     "How's the weather in London?",
    #     "How's the weather in Paris",
    # ]

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
            {
                "tool_name": "lat_long_to_weather",
                "tool_input": {
                    "longitude": "2.3488",
                    "latitude": "48.85341"
                }
            }
        ],
    ]

    response = [
        "Rainy and cold",
        "Sunny and cold",
    ]

    custom_trajectory_prompt_template = PointwiseMetricPromptTemplate(
        criteria={
            "Follows trajectory": (
                "Evaluate whether the agent's response logically follows from the "
                "sequence of actions it took. Consider these sub-points:\n"
                "  - Does the response reflect the information gathered during the trajectory?\n"
                "  - Is the response consistent with the goals and constraints of the task?\n"
                "  - Are there any unexpected or illogical jumps in reasoning?\n"
                "Provide specific examples from the trajectory and response to support your evaluation."
            )
        },
        rating_rubric={
            "1": "Follows trajectory",
            "0": "Does not follow trajectory",
        },
        input_variables=["predicted_trajectory"],
    )
    print(f"custom_trajectory_prompt_template: {custom_trajectory_prompt_template}")

    custom__metric = PointwiseMetric(
        metric="custom_trajectory_metric",
        metric_prompt_template=custom_trajectory_prompt_template,
    )

    eval_dataset = pandas.DataFrame(
        {
            #"prompt": prompt,
            "predicted_trajectory": predicted_trajectory,
            "response": response,
        }
    )

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[custom__metric],
        experiment="agents-custom-trajectory"
    )

    eval_result = eval_task.evaluate()
    print_eval_result(eval_result)


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

# Define a custom computational-metric to check if all the required tools are called
def custom_essential_tools_present_metric():

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
        experiment="agents-custom-essential-tools-present"
    )

    eval_result = eval_task.evaluate()
    print_eval_result(eval_result)


if __name__ == "__main__":
    globals()[sys.argv[1]]()
