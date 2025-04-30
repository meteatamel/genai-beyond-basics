# Gen AI evaluation service - agent metrics (computation-based)

## Introduction 

These are the metrics related to [agents](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-agents)

* `trajectory_exact_match`
* `trajectory_in_order_match`
* `trajectory_any_order_match`
* `trajectory_precision`
* `trajectory_recall`
* `trajectory_single_tool_use`

Mostly computation-based (but can be model-based too), these metrics assess if the agent's tool (function) use matches 
with a reference trajectory. 

## Standard metrics

See [agent.py](agent.py) on how you'd use these metrics in Gen AI evaluation service with saved responses.

Run the evaluation:

```python
python agent.py
```

## Custom metrics

You can define custom computational metrics for trajectory evaluation (e.g. check if all the required tools are called).

See [agent_custom.py](agent_custom.py) for details.

Run the evaluation:

```python
python agent_custom.py
```



