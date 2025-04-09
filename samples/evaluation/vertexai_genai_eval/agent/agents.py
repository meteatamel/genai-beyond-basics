import pandas
import sys
from vertexai.preview.evaluation import EvalTask
from vertexai.preview.evaluation.constants import Metric
from vertexai.preview.evaluation.metrics import TrajectorySingleToolUse

sys.path.append("../../../../")
from samples.evaluation.vertexai_genai_eval.utils import print_eval_result

# Metrics to evaluate agents
# See: https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-agents
def main():
    predicted_trajectory = [
        # example 1 - perfect match
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
        # example 2 - location mismatch
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
        # example 3 - extra tool
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
            },
            {
                "tool_name": "extra_tool",
                "tool_input": {
                    "some_input": "some_value"
                }
            }
        ],
        # example 4 - extra tool and mixed order
        [
            {
                "tool_name": "lat_long_to_weather",
                "tool_input": {
                    "longitude": "-0.12574",
                    "latitude": "51.50853"
                }
            },
            {
                "tool_name": "loc_to_lat_long",
                "tool_input": {
                    "location": "London"
                }
            },
            {
                "tool_name": "extra_tool",
                "tool_input": {
                    "some_input": "some_value"
                }
            }
        ],
    ]

    reference_trajectory = [
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
        # example 3
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
        # example 4
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
    ]

    eval_dataset = pandas.DataFrame(
        {
            "predicted_trajectory": predicted_trajectory,
            "reference_trajectory": reference_trajectory,
        }
    )

    metrics = [
        # If the predicted trajectory contains a specific tool without checking the order of the tool calls or how many
        # times the tool is used.
        # Only requires predicted_trajectory.
        # 0: Tool is absent, 1: Tool is present.
        TrajectorySingleToolUse(tool_name='loc_to_lat_long'),

        # If the predicted trajectory is identical to the reference trajectory, with the exact same tool calls in the
        # exact same order.
        # 0: Not exact match, 1: Exact match.
        Metric.TRAJECTORY_EXACT_MATCH,

        # If the predicted trajectory contains all the tool calls from the reference trajectory in the same order,
        # and may also have extra tool calls.
        # 0: Not in order match, 1: In order match.
        Metric.TRAJECTORY_IN_ORDER_MATCH,

        # If the predicted trajectory contains all the tool calls from the reference trajectory, but the order doesn't
        # matter and may contain extra tool calls.
        # 0: No aray order match, 1: Any order match.
        Metric.TRAJECTORY_ANY_ORDER_MATCH,

        # Measures how many of the tool calls in the predicted trajectory are actually relevant or correct according to
        # the reference trajectory.
        #
        # Precision is calculated as follows: Count how many actions in the predicted trajectory also appear in the
        # reference trajectory. Divide that count by the total number of actions in the predicted trajectory.
        # A float in the range of [0,1]
        Metric.TRAJECTORY_PRECISION,

        # Measures how many of the essential tool calls from the reference trajectory are actually captured in the
        # predicted trajectory.
        #
        # Recall is calculated as follows: Count how many actions in the reference trajectory also appear in the predicted
        # trajectory. Divide that count by the total number of actions in the reference trajectory.
        Metric.TRAJECTORY_RECALL,
    ]

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=metrics,
        experiment="agents"
    )

    eval_result = eval_task.evaluate()
    print_eval_result(eval_result)


if __name__ == "__main__":
    main()
