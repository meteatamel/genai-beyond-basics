# Gen AI evaluation service - agent metrics (computation-based)

## Introduction 

In [agent evaluation](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-agents), you can evaluate agent's final response and/or agent's tool trajectory. 

Final response evaluation follows the same process as model response evaluation.

Trajectory evaluation can be done with computation-based (standard or custom) or model-based metrics. 

These are the standard computation-based trajectory metrics:

* `trajectory_exact_match`
* `trajectory_in_order_match`
* `trajectory_any_order_match`
* `trajectory_precision`
* `trajectory_recall`
* `trajectory_single_tool_use`

## Trajectory evaluation

### Computation-based

For standard computation-based trajectory metrics with saved responses, see [trajectory_computation_based.py](./trajectory_computation_based.py).

Run the evaluation:

```python
python trajectory_computation_based.py
```

For custom computation-based trajectory metrics (e.g. check if all the required tools are called), 
see [trajectory_computation_based_custom.py](trajectory_computation_based_custom.py).

Run the evaluation:

```python
python trajectory_computation_based_custom.py
```

### Model-based

Instead of relying on computation-based agent trajectory metrics, you can also define model-based custom trajectory
metrics. See [trajectory_model_based_custom.py](trajectory_model_based_custom.py) for details.

Run the evaluation:

```python
python trajectory_model_based_custom.py
```

## Final response evaluation 

TODO
