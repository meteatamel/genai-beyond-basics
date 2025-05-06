# Gen AI evaluation service - tool-use metrics

## Introduction 

These are the metrics related to the [tool use](https://cloud.google.com/vertex-ai/generative-ai/docs/models/determine-eval#tool-use)

* `tool_call_valid`
* `tool_name_match`
* `tool_parameter_key_match`
* `tool_parameter_kv_match`

These metrics assess if a tool (function) call and name are valid and if the parameter names and values 
match to what you expect.

## Tool-use metrics with saved responses

See [tool_use.py](tool_use.py) on how you'd use these metrics in Gen AI evaluation service with saved responses.

Run the evaluation:

```python
python tool_use.py
```

## Tool-use metrics with Gemini function calling

See [tool_use_gemini.py](./tool_use_gemini.py) on how you can setup 2 functions for automatic function calling in Gemini, 
use those functions from a prompt, and then evaluate the function call results with the Gen AI evaluation service. It 
involves getting the function call history, converting it to the format Gen AI evaluation service expects and running 
the evaluation.

Run the evaluation:

```python
python tool_use_gemini.py
```


