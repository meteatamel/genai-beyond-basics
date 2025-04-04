# Before you start 

Before you run any samples, make sure you follow these steps. 

Set your project id in `gcloud`:

```shell
gcloud config set core/project your-google-cloud-project-id
```

Authenticate:

```shell
gcloud auth application-default login
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
