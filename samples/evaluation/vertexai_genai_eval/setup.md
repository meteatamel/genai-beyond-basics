# Setup

Before you run any samples, make sure you follow these steps, either from Cloud Shell or your local `gcloud` installation.

First, make sure your project id is set in `gcloud`:

## Set gclodu

Check if your project is set:

```shell
gcloud config list

...
[core]
project = your-google-cloud-project-id
```

If not, set your project id:

```shell
gcloud config set core/project your-google-cloud-project-id
```

If not in Cloud Shell (i.e. running locally), authenticate:

```shell
gcloud auth application-default login
```

Enable required Google Cloud APIs:

```shell
gcloud services enable aiplatform.googleapis.com \
  cloudresourcemanager.googleapis.com
```

## Get the code

Clone the repository:

```shell
git clone https://github.com/meteatamel/genai-beyond-basics.git
```

## Set Python environment

Navigate to the sample:

```shell
cd genai-beyond-basics/samples/evaluation/vertexai_genai_eval/
```

Create and activate a Python virtual environment:

```shell
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```shell
pip install -r requirements.txt
```
