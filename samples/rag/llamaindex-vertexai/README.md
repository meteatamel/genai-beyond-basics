# LlamaIndex on Vertex AI with RAG API

LlamaIndex is a data framework for developing context-augmented large language model (LLM) applications.

In this sample, you'll learn how to use LlamaIndex on Vertex AI with RAG API.

More specifically, you'll:

1. Ask the LLM questions about a fictional vehicle, Cymbal Starlight 2024,
   and see that it cannot answer questions.
2. Create a RAG corpus, upload the PDF of user manual for Cymbal Starlight 2024
   to the corpus.
3. Ask the LLM questions about the vehicle with the supplied RAG corpus 
   and see that you get answers back.

Take a look at the sample [main.py](./main.py) on how to implement and use a RAG corpus.

## Without RAG

First, let's ask a question to the LLM about the vehicle without any RAG.

```sh
 python main.py --project your-project-id generate_text \
  --prompt "What is the cargo capacity of Cymbal Starlight?" 
```

You get a response like this:

```sh
Corpus name: None
Prompt: What is the cargo capacity of Cymbal Starlight?
Response text: I do not have access to real-time information, including specific details about ships like the "Cymbal Starlight." 
```

## Create a RAG corpus

First, you need to create a RAG corpus:

```sh
python main.py --project_id your-project-id create_corpus --display_name cymbal-starlight-corpus

Corpus created: projects/207195257545/locations/us-central1/ragCorpora/8935141660703064064
```

## Upload a file

To use a PDF for RAG, you need to either upload corpus directly or host it on Google 
Cloud Storage or Google Drive and point to it. 

In this case, let's upload the fictitious [cymbal-starlight-2024.pdf](cymbal-starlight-2024.pdf) user manual file.

```sh
python main.py --project_id genai-atamel upload_file \
  --corpus_name projects/207195257545/locations/us-central1/ragCorpora/8935141660703064064 \ 
  --path cymbal-starlight-2024.pdf --display_name cymbal-starlight-2024.pdf
  
File upload to corpus: projects/207195257545/locations/us-central1/ragCorpora/8935141660703064064
-name: projects/207195257545/locations/us-central1/ragCorpora/8935141660703064064/ragFiles/8935141660703064064
 display_name: cymbal-starlight-2024.pdf
```

## Direct retrieve

Before asking the LLM, you can do a direct retrieve with top k relevant docs/chunks:

```sh
python main.py --project_id genai-atamel direct_retrieve \
  --corpus_name projects/207195257545/locations/us-central1/ragCorpora/8935141660703064064 \ 
  --text "What is the cargo capacity of Cymbal Starlight?"
```

And you should get back a list of chunks:

```sh
Text: What is the cargo capacity of Cymbal Starlight?
Response: contexts {
  contexts {
    source_uri: "cymbal-starlight-2024.pdf"
    text: "This light may illuminate for a variety of reasons, i
    ...
```

## With grounding

Finally, we're ready to ask questions about the vehicle **with** RAG corpus.

Let's ask the same question but with the RAG corpus this time:

```sh
python main.py --project genai-atamel generate_text \
  --corpus_name projects/207195257545/locations/us-central1/ragCorpora/8935141660703064064 \
  --prompt "What is the cargo capacity of Cymbal Starlight?" 
```
You get a response like this:

```sh
Corpus name: projects/207195257545/locations/us-central1/ragCorpora/8935141660703064064
Prompt: What is the cargo capacity of Cymbal Starlight?
Response text: The Cymbal Starlight has a cargo capacity of 13.5 cubic feet. The cargo area is located in the trunk of the vehicle. 
```

Let's ask another question:

```sh
python main.py --project genai-atamel generate_text \
  --corpus_name projects/207195257545/locations/us-central1/ragCorpora/8935141660703064064 \
  --prompt "What's the emergency roadside assistance phone number?"
```

Response:

```sh
Corpus name: projects/207195257545/locations/us-central1/ragCorpora/8935141660703064064
Prompt: What's the emergency roadside assistance phone number?
Response text: The emergency roadside assistance phone number is 1-800-555-1212. 
```

Yay, it works!

## References

* [LlamaIndex on Vertex AI for RAG overview docs](https://cloud.google.com/vertex-ai/generative-ai/docs/llamaindex-on-vertexai)
* [LlamaIndex on Vertex AI for RAG API](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/rag-api)
* [rag.py sample](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/2cc418ecbd065603585a18935201067182ea3417/generative_ai/rag.py)
* [Grounding decision flowchart](https://cloud.google.com/docs/ai-ml/generative-ai#grounding)
* [Grounding for Gemini with Vertex AI Search and DIY RAG talk](https://youtu.be/v4s5eU2tfd4)
