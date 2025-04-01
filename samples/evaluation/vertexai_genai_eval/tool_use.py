import json
import pandas
import sys
from vertexai.evaluation import EvalTask
from vertexai.evaluation.constants import Metric

sys.path.append("../../../")
from samples.evaluation.vertexai_genai_eval.utils import print_eval_result

def main():
    response1 = json.dumps(
    {
        "content": "",
        "tool_calls": [
            # no tool call - fails Metric.TOOL_CALL_VALID
        ]
    })

    response2 = json.dumps(
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
    })

    response3 = json.dumps(
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
    })

    response4 = json.dumps(
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
    })

    reference = json.dumps(
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
    })


    eval_dataset = pandas.DataFrame(
        {
            "response": [response1, response2, response3, response4],
            "reference": [reference, reference, reference, reference],
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
