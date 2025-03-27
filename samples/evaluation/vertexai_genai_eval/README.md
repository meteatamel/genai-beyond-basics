# Gen AI evaluation service in Vertex AI 

The Gen AI evaluation service in Vertex AI lets you evaluate any generative model or application against a benchmark 
or your own evaluation criteria.

## Setup

Make sure your `gcloud` is set up with your Google Cloud project:

```shell
gcloud config set core/project your-google-cloud-project-id
```

You're logged in:

```shell
gcloud auth application-default login
```

Create and activate a virtual environment:

```shell
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```shell
pip install -r requirements.txt
```

## Run

TODO

## References

* [Gen AI evaluation service overview](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview)
* [Define your evaluation metrics](https://cloud.google.com/vertex-ai/generative-ai/docs/models/determine-eval)
* [Metric prompt templates for model-based evaluation](https://cloud.google.com/vertex-ai/generative-ai/docs/models/metrics-templates)