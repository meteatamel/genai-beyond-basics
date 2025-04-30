# Gen AI evaluation service - model-based metrics 

## Introduction 

There are 2 classes of [model-based metrics](https://cloud.google.com/vertex-ai/generative-ai/docs/models/determine-eval#model-based-metrics). 

First, metrics used specifically for translation related tasks. [Comet](https://huggingface.co/Unbabel/wmt22-comet-da) 
and [MetricX](https://github.com/google-research/metricx) are the supported translation metrics:

* `comet`
* `metricx`

Second, metrics where the judge model evaluates a candidate model. For this case, there are 3 ways to define
metrics:

1. With pre-built metric prompt templates for pointwise and pairwise evaluation. 
2. With custom metric prompt templates. 
3. With a free-form metric prompt.

These are the metrics with the [pre-built metric prompt templates](https://cloud.google.com/vertex-ai/generative-ai/docs/models/metrics-templates):

* `coherence`
* `fluency`
* `safety`
* `groundedness`
* `instruction_following`
* `verbosity`
* `text_quality`
* `summarization_quality`
* `question_answering_quality`
* `multi_turn_chat_quality`
* `multi_turn_safety`
* `pairwise_coherence`
* `pairwise_fluency`
* `pairwise_safety`
* `pairwise_groundedness`
* `pairwise_instruction_following`
* `pairwise_verbosity`
* `pairwise_text_quality`
* `pairwise_summarization_quality`
* `pairwise_question_answering_quality`
* `pairwise_multi_turn_chat_quality`
* `pairwise_multi_turn_safety`

For custom metric prompt templates, see [metric_prompt_template.py](https://github.com/googleapis/python-aiplatform/blob/main/vertexai/evaluation/metrics/metric_prompt_template.py).

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

Instead of relying on pre-built prompt templates for metrics, you can define your own prompts for custom metrics. 
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

## Implementing the RAG triad with custom metrics

RAG triad is a trio of metrics (answer relevance, context relevance, groundedness) that you can use to evaluate RAG 
pipelines. You can read more about it in [Evaluating RAG pipelines](https://atamel.dev/posts/2025/01-09_evaluating_rag_pipelines/). 

Using custom metrics, you can implement the RAG triad. See [pointwise_rag_triad.py](pointwise_rag_triad.py) for details.

Run the evaluation with each metric:

```python
python pointwise_rag_triad.py answer_relevance
python pointwise_rag_triad.py context_relevance
python pointwise_rag_triad.py groundedness
```

Or all 3 metrics:

```python
python pointwise_rag_triad.py all_metrics
```

