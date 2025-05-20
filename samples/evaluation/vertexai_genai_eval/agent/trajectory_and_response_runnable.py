import pandas
import sys
from vertexai.preview.evaluation import EvalTask, MetricPromptTemplateExamples
from vertexai.preview.evaluation.constants import Metric

sys.path.append("../../../../")
from samples.evaluation.vertexai_genai_eval.utils import get_experiment_name, print_eval_result

# This example shows how to evaluate the trajectory and also the final response by calling the agent with the runnable
# interface. The exact details of how to call the agent and parse the response/trajectory depends on the agent framework
# used. See here for an Agent Development Kit (ADT) example:
# See: https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/evaluation/evaluating_adk_agent.ipynb

def parse_agent_output_to_dictionary():
    # TODO: Parse agent response and trajectory and convert into the format the eval service expects

    # Returning dummy response here
    final_output = {
        "response": "It's rainy and 10 degrees",
        "predicted_trajectory":
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
            ]
    }
    return final_output


def agent_parsed_outcome(prompt):
    print(f"Prompt: {prompt}")

    # TODO: Setup and run your agent code here

    # TODO: Parse the agent response and trajectory
    return parse_agent_output_to_dictionary()


def main():
    prompts = [
        "How's the weather in London?",
        "How's the weather in Tokyo?",
    ]

    reference_trajectory = [
        # London
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
        # Tokyo
        [
            {
                "tool_name": "loc_to_lat_long",
                "tool_input": {
                    "location": "Tokyo"
                }
            },
            {
                "tool_name": "lat_long_to_weather",
                "tool_input": {
                    "longitude": "35.6764",
                    "latitude": "139.6500"
                }
            }
        ],
    ]

    eval_dataset = pandas.DataFrame(
        {
            "prompt": prompts,
            "reference_trajectory": reference_trajectory,
        }
    )


    metrics = [
        # Fluency metric needs 'prompt' and 'response' columns and used for response evaluation
        MetricPromptTemplateExamples.Pointwise.FLUENCY,

        # Exact match for trajectory evaluation
        Metric.TRAJECTORY_EXACT_MATCH,
    ]

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=metrics,
        experiment=get_experiment_name(__file__)
    )

    eval_result = eval_task.evaluate(
        runnable=agent_parsed_outcome
    )
    print_eval_result(eval_result)


if __name__ == "__main__":
    main()
