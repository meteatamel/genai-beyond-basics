# Gen AI evaluation service - agent metrics (model-based)

## Introduction 

In [agent evaluation](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-agents), you can evaluate
agent's final response and/or agent's tool trajectory with computation-based or model-based metrics. 

Final response evaluation follows the same process as model response evaluation.

This covers the model-based agent metrics. See [computation_based/agent](../../computation_based/agent) 
for computation-based agent metrics.

## Custom trajectory metrics

Instead of relying on standard computation-based agent trajectory metrics, you can define model-based custom trajectory metrics.

See [agent_trajectory_custom.py](agent_trajectory_custom.py) for details.

Run the evaluation:

```python
python agent_trajectory_custom.py
```

## Final response evaluation 

TODO


