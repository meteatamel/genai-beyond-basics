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

> [!NOTE]
> Each metric has 2 templates: 1 for pointwise and 1 for pairwise evaluation. 
> Details in [metric_prompt_template_examples.py](https://github.com/googleapis/python-aiplatform/blob/main/vertexai/evaluation/metrics/metric_prompt_template_examples.py).

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

## Pointwise metrics

See [pointwise.py](./pointwise.py) on other model-based metrics in Gen AI evaluation service for pointwise (single model)
evaluation. 

Pointwise metrics can be used in 2 ways:

1- Bring-your-own-response (BYOR) mode where the model responses are provided rather than calling the model.
2- Bring a model and use that model to get responses from.

Run the evaluation in BYOR mode or with a model:

```python
python pointwise.py byor
python pointwise.py model
```

After a few seconds, you should see the results:
```console
==Summary metrics==
row_count: 4
fluency/mean: 3.25
fluency/std: 1.707825127659933
==Metrics table==
                                              prompt                                           response                                fluency/explanation  fluency/score
0  Summarize the following article: The full cost...  Clean-up operations are continuing across the ...  The response provides very little information ...            1.0
1  Summarize the following article: A fire alarm ...  Two tourist buses have been destroyed by fire ...  The response is fluent, with no grammatical er...            5.0
2  Summarize the following article: Ferrari appea...  Lewis Hamilton stormed to pole position at the...  The response is mostly fluent, with clear word...            4.0
3  Summarize the following article: Gundogan, 26,...  Manchester City midfielder Ilkay Gundogan says...  The response is short and grammatical, but it ...            3.0
```

## Pairwise metrics

If you want to compare two models, you can use pairwise metrics. See [pairwise.py](./pairwise.py) for details.

Run the evaluation in BYOR mode or with a model:

```python
python pairwise.py
```

After a few seconds, you should see the results:
```console
==Summary metrics==
row_count: 4
pairwise_fluency/candidate_model_win_rate: 0.0
pairwise_fluency/baseline_model_win_rate: 1.0
==Metrics table==
                                              prompt                                           response  ...                       pairwise_fluency/explanation pairwise_fluency/pairwise_choice
0  Summarize the following article: The full cost...  Severe flooding has impacted several areas in ...  ...  BASELINE response is slightly more fluent due ...                         BASELINE
1  Summarize the following article: A fire alarm ...  In the early hours of Saturday, a fire alarm a...  ...  Both responses are well-written and follow the...                         BASELINE
2  Summarize the following article: Ferrari appea...  Lewis Hamilton secured pole position for the B...  ...  BASELINE response has slightly better writing ...                         BASELINE
3  Summarize the following article: Gundogan, 26,...  Ilkay Gundogan is recovering from a torn cruci...  ...  BASELINE response has a slightly better flow a...                         BASELINE
```

## Custom metrics

Instead of relying on prebuilt prompt templates for metrics, you can define your own prompts for custom metrics. 
You can do this with a metric prompt template or define a free-form metric prompt for full flexibility. 

See [pointwise_custom_metric.py](./pointwise_custom_metric.py) for details.

Run the evaluation with the metric prompt template or free-form metric prompt:

```python
python pointwise_custom_metric.py template
python pointwise_custom_metric.py free_form
```

```console
==Summary metrics==
row_count: 3
custom_metric/mean: 2.0
custom_metric/std: 1.0
==Metrics table==
                                         response                                                                            custom_metric/explanation  custom_metric/score
0             This is a funny and single sentence  The response fulfills both criteria: it's a single sentence and claims to be funny, implying ent...                  3.0
1  This is a funny sentence. But it's 2 sentences                                   The response is entertaining, but fails the one sentence criteria.                  2.0
2    This is neither funny. Nor a single sentence  The response fails to meet both criteria, as it is not entertaining and consists of more than on...                  1.0
```

