# Gen AI evaluation service in Vertex AI 

The [Gen AI evaluation service](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview) in 
Vertex AI lets you evaluate any generative model or application against a set of criteria or your own custom criteria 
using metrics.

These are the main metric classes:

* **Computation-based**: These metrics are computed using mathematical formulas such as ROUGE, BLEU or tool use and 
compare the model's output against a ground truth or reference.  
* **Model-based**: These metrics assess a candidate model with a judge model. The judge model for most use cases is 
Gemini but you can also use models such as MetricX or COMET for translation use cases. Model-based metrics can further 
be measured in pointwise (single model) or pairwise (two models) ways.
* **Tool-use**: These metrics assess if a tool (function) call and name are valid and if the parameter names and values
match to what you expect. They're computation-based. 
* **Agent**: These metrics assess if the agent's tool (function) use matches with a reference trajectory. They can be
computation-based or model-based.

## Samples

Before you start, make sure to follow the [setup](setup.md) page. 

Follow the following sub-pages for detailed samples:

* [Computation-based metrics](./computation_based/README.md)
* [Model-based metrics](./model_based/README.md)
* [Tool-use metrics](./tool_use/README.md)
* [Agent metrics](./agent/README.md)

## Metrics

This is the full list of metrics supported out of the box:

Computation-based:
* `exact_match`
* `bleu`
* `rouge`
* `rouge_1`
* `rouge_2`
* `rouge_l`
* `rouge_l_sum`

Model-based:
* Translation:
  * `comet`
  * `metricx`
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

Tool-use:
  * `tool_call_valid`
  * `tool_name_match`
  * `tool_parameter_key_match`
  * `tool_parameter_kv_match`

Agent:
  * `trajectory_exact_match`
  * `trajectory_in_order_match`
  * `trajectory_any_order_match`
  * `trajectory_precision`
  * `trajectory_recall`
  * `trajectory_single_tool_use`

## References

* [Documentation: Gen AI evaluation service overview](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview)
* [GitHub: GenAI evaluation service code](https://github.com/googleapis/python-aiplatform/tree/main/vertexai/evaluation)
* [Notebooks: GenAI evaluation service samples](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/evaluation)
* [Blog post: LLM Evaluation on GCP](https://medium.com/google-cloud/llms-evaluation-on-gcp-9186fad73f22)