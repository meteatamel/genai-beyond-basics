# Gen AI evaluation service - model-based metrics 

## Introduction 

There are 2 classes of [model-based metrics](https://cloud.google.com/vertex-ai/generative-ai/docs/models/determine-eval#model-based-metrics). 

First, metrics used specifically for translation related tasks. These are the supported translation metrics:

* [Comet](https://huggingface.co/Unbabel/wmt22-comet-da)
* [MetricX](https://github.com/google-research/metricx)

Second, more generic metrics where the judge model uses a metric prompt template to judge a candidate model. 
These are the metrics with the [prebuilt metric prompt templates](https://cloud.google.com/vertex-ai/generative-ai/docs/models/metrics-templates):
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

Note: Each metric has 2 templates (1 for pointwise and 1 for pairwise, 
details in [metric_prompt_template_examples.py](https://github.com/googleapis/python-aiplatform/blob/main/vertexai/evaluation/metrics/metric_prompt_template_examples.py)).

Additionally, you can [define your own metrics](https://cloud.google.com/vertex-ai/generative-ai/docs/models/determine-eval)
with a metric prompt template or define a free-form metric prompt for full flexibility  (see [metric_prompt_template.py](https://github.com/googleapis/python-aiplatform/blob/main/vertexai/evaluation/metrics/metric_prompt_template.py)).  

## Translation metrics

See [translation.py](./translation.py) on how you'd use these metrics in Gen AI evaluation service.

Run the evaluation:

```python
python translation.py
```

After a few seconds, you should see the results:
```console
==Summary metrics==
row_count: 2
comet/mean: 0.90514195
comet/std: 0.09416372713647334
metricx/mean: 3.5140458499999996
metricx/std: 0.6293740377559635
==Metrics table==
                                      source                             response                            reference  comet/score  metricx/score
0    Dem Feuer konnte Einhalt geboten werden            The fire could be stopped  They were able to control the fire.     0.838558       3.069011
1  Schulen und Kindergärten wurden eröffnet.  Schools and kindergartens were open     Schools and kindergartens opened     0.971726       3.959080
```


