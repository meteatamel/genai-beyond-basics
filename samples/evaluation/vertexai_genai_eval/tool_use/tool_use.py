import json
import pandas
import sys
from vertexai.evaluation import EvalTask
from vertexai.evaluation.constants import Metric

sys.path.append("../../../../")
from samples.evaluation.vertexai_genai_eval.utils import print_eval_result

# An example to show how you'd use tool-use metrics in Gen AI evaluation service with saved responses.
# See: https://cloud.google.com/vertex-ai/generative-ai/docs/models/determine-eval#tool-use
def main():
    responses = [
        {
            "content": "",
            "tool_calls": [
                # no tool call - fails Metric.TOOL_CALL_VALID
            ]
        },
        {
            "content": "",
            "tool_calls": [
                {
                    # name (loc_to_lat_long) does not match - fails Metric.TOOL_NAME_MATCH
                    "name": "loc_to_lat_long",
                    "arguments": {
                        "location": "London"
                    }
                }
            ]
        },
        {
            "content": "",
            "tool_calls": [
                {
                    "name": "location_to_lat_long",
                    "arguments": {
                        # key (city) does not match - fails Metric.TOOL_PARAMETER_KEY_MATCH
                        "city": "London"
                    }
                }
            ]
        },
        {
            "content": "",
            "tool_calls": [
                {
                    "name": "location_to_lat_long",
                    "arguments": {
                        # value (Paris) does not match - fails Metric.TOOL_PARAMETER_KV_MATCH
                        "location": "Paris"
                    }
                }
            ]
        },
        {
            "content": "",
            # Everything matches
            "tool_calls": [
                {
                    "name": "location_to_lat_long",
                    "arguments": {
                        "location": "London"
                    }
                }
            ]
        }
    ]

    references = [
        {
            "content": "",
            "tool_calls": [
                {
                    "name": "location_to_lat_long",
                    "arguments": {
                        "location": "London"
                    }
                }
            ]
        }
    ] * 5

    eval_dataset = pandas.DataFrame(
        {
            "response": [json.dumps(response) for response in responses],
            "reference": [json.dumps(reference) for reference in references],
        }
    )

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=[
            Metric.TOOL_CALL_VALID,
            Metric.TOOL_NAME_MATCH,
            Metric.TOOL_PARAMETER_KEY_MATCH,
            Metric.TOOL_PARAMETER_KV_MATCH
        ],
        experiment="tool-use"
    )

    eval_result = eval_task.evaluate()
    print_eval_result(eval_result)


if __name__ == "__main__":
    main()
