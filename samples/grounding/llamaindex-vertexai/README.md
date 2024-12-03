# Building a RAG pipeline with LlamaIndex and Vertex AI models

![LlamaIndex on Vertex AI](images/llamaindex_vertexai.png)

## Introduction

[LlamaIndex](https://www.llamaindex.ai/) is a popular framework for developing context-augmented LLM apps.

Imagine you own the 2024 model of a fictitious vehicle called Cymbal Starlight. It has a user’s manual in PDF format 
([cymbal-starlight-2024.pdf](cymbal-starlight-2024.pdf)) and you want to ask LLM questions about this vehicle from 
the user manual. 

In this tutorial, we'll see how to [Build a RAG pipeline](https://docs.llamaindex.ai/en/stable/understanding/rag/) with
LlamaIndex and Vertex AI models and ask LLM questions about the PDF.

See [main.py](./main.py) for the full sample.

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

```shell
python main.py
```

```shell
Read PDF into documents
Combine document for each page back into a single document
Initialize embedding model
Index document
Initialize query engine with the model
Question: What is the cargo capacity of Cymbal Starlight?
Response: The cargo capacity of the Cymbal Starlight 2024 is 13.5 cubic feet.
```

Yay, it works!

## References

* [Build a RAG pipeline](https://docs.llamaindex.ai/en/stable/understanding/rag/)
* [Building and Evaluating Advanced RAG](https://learn.deeplearning.ai/courses/building-evaluating-advanced-rag)
* [LlamaIndex Vertex AI](https://docs.llamaindex.ai/en/stable/examples/llm/vertex/)