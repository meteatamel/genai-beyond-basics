# Gen AI evaluation service - agent metrics

## Introduction 

These are the metrics related to the [agents](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-agents)

* trajectory_single_tool_use
* trajectory_exact_match
* trajectory_in_order_match
* trajectory_any_order_match
* trajectory_precision
* trajectory_recall

These metrics help you to see if the agent's tool (function) use matches with the trajectory of tool use you expect
against a reference. 

## Standard metrics

See [agents.py](agents.py) on how you'd use these metrics in Gen AI evaluation service with saved responses.

Run the evaluation:

```python
python agents.py
```

## Custom metrics

Instead of relying on standard agent metrics, you can define your own prompts for custom trajectory metrics. You can
also define custom computational metrics for trajectory evaluation (e.g. check if all the required tools are called).

See [agents_custom_metric.py](agents_custom_metric.py) for details.

Run the evaluation:

```python
python agents_custom_metric.py custom_trajectory_metric
python agents_custom_metric.py custom_essential_tools_present_metric
```



