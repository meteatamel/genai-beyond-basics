# Gen AI evaluation service in Vertex AI 

The [Gen AI evaluation service](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview) in 
Vertex AI lets you evaluate any generative model or application against a set of criteria or your own custom criteria 
using metrics.

There are 2 classes of metrics:

* **Computation-based**: These metrics are computed using mathematical formulas such as ROUGE, BLEU or tool use and 
compare the model's output against a ground truth or reference.  
* **Model-based**: These metrics assess a candidate model with a judge model. The judge model for most use cases is 
Gemini but you can also use models such as MetricX or COMET for translation use cases. Model-based metrics can further 
be measured in 2 ways:
  * **Pointwise**: The judge model assesses the candidate model's output based on the evaluation criteria. 
  * **Pairwise**:  The judge model compares the two models (candidate and baseline) and pick the better one.

There are also metrics on:

* **Tool-use**: Technically computation-based, these metrics help you to see if a tool (function) call and name are 
valid and it the parameter names and value match to what you expect. 
* **Agent**: Mostly computation-based (but can be model-based too), these metrics help you to see if the agent's tool
(function) use matches with the trajectory of tool use you expect against a reference. 

## Samples

Before you start, make sure to follow the [setup](setup.md) page. 

Follow the following sub-pages for detailed samples:

* [Computation-based metrics](./computation_based/README.md)
* [Model-based metrics](./model_based/README.md)
* [Tool-use metrics](./tool_use/README.md)
* [Agent metrics](./agent/README.md)

## References

* [Documentation: Gen AI evaluation service overview](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview)
* [GitHub: GenAI evaluation service code](https://github.com/googleapis/python-aiplatform/tree/main/vertexai/evaluation)
* [Notebooks: GenAI evaluation service samples](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/evaluation)