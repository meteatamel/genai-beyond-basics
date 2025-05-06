# Gen AI evaluation service - agent metrics (computation-based)

## Introduction 

In [agent evaluation](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-agents), you can evaluate
agent's final response and/or agent's tool trajectory with computation-based or model-based metrics. 

Final response evaluation follows the same process as model response evaluation.

This covers the computation-based agent metrics. See [model_based/agent](../../model_based/agent) 
for model-based agent metrics.

These are the standard computation-based trajectory metrics:

* `trajectory_exact_match`
* `trajectory_in_order_match`
* `trajectory_any_order_match`
* `trajectory_precision`
* `trajectory_recall`
* `trajectory_single_tool_use`

## Standard trajectory metrics

See [agent_trajectory.py](agent_trajectory.py) on how you'd use these metrics in Gen AI evaluation service 
with saved responses.

Run the evaluation:

```python
python agent_trajectory.py
```

## Custom trajectory metrics

You can define custom computational metrics for trajectory evaluation (e.g. check if all the required tools are called).

See [agent_trajectory_custom.py](agent_trajectory_custom.py) for details.

Run the evaluation:

```python
python agent_trajectory_custom.py
```


