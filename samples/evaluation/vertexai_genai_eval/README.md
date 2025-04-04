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

## Samples

Follow the following sub-pages for samples and to learn more:

* [Setup](./setup.md)
* [Computation-based metrics](./computation_based/README.md)
* [Model-based metrics](./model_based/README.md)
* [Tool-use metrics](./tool_use/README.md)

## References

* [Documentation: Gen AI evaluation service overview](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview)
* [GitHub: GenAI evaluation service code](https://github.com/googleapis/python-aiplatform/tree/main/vertexai/evaluation)
* [Notebooks: GenAI evaluation service samples](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/evaluation)