# Gen AI evaluation service - model-based metrics 

There are 2 classes of model-based metrics. 

First, metrics used specifically for translation related tasks. These are the supported translation metrics:

* [Comet](https://huggingface.co/Unbabel/wmt22-comet-da)
* [MetricX](https://github.com/google-research/metricx)

Second, more generic metrics where the judge model uses a metric prompt template to judge a candidate model. These are the
metrics with the [prebuilt metric prompt templates](https://cloud.google.com/vertex-ai/generative-ai/docs/models/metrics-templates):
* Coherence
* Fluency
* Groundedness
* Instruction Following
* Multi-turn Chat Quality
* Multi-turn Safety
* Safety
* Summarization Quality
* Question Answering Quality
* Text Quality
* Verbosity

Note: Each metric has 2 templates (1 for pointwise and 1 for pairwise).

Additionally, you can [define your own metrics](https://cloud.google.com/vertex-ai/generative-ai/docs/models/determine-eval)
with a metric prompt template (see [metric_prompt_template.py](https://github.com/googleapis/python-aiplatform/blob/main/vertexai/evaluation/metrics/metric_prompt_template.py)) 
or define a free-form metric prompt for full flexibility.  

