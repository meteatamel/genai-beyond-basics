# GenAI beyond basics

A collection of Generate AI related samples.

## Samples

### Frameworks

#### LangChain

* [Chat with in-memory history](./samples/frameworks/langchain/chat/)
* [Chat with history saved to Firestore](./samples/frameworks/langchain/chat-firestore)

#### Semantic Kernel

* [Chat with in-memory history](./samples/frameworks/semantic-kernel/chat/)

### Grounding & RAG

#### Grounding

* [Grounding with public data with Google Search](./samples/grounding/google-search/)
* [Grounding with your own data with Vertex AI Search](./samples/grounding/vertexai-search/)

#### RAG

* [RAG with a PDF using LangChain and Annoy Vector Store](./samples/grounding/rag-pdf-annoy)
* [RAG with a PDF using LangChain and Firestore Vector Store](./samples/grounding/rag-pdf-firestore)
* [LlamaIndex on Vertex AI with RAG API](./samples/grounding/llamaindex-vertexai-ragapi)
* [Building a RAG pipeline with LlamaIndex and Vertex AI models](./samples/grounding/llamaindex-vertexai)

#### Retrieval

* [Multimodal image storage and retrieval with Chroma](./samples/multimodal/retrievers/chroma)
* [Multimodal image storage and retrieval with Firestore Vector Store](./samples/multimodal/retrievers/firestore)

### Function calling

* [Function calling - Weather](./samples/function-calling/weather)

### Input and output

* [Response type and schema (Vertex AI)](./samples/controlled-generation/vertexai)
* [Response schema and pydantic (LangChain)](./samples/controlled-generation/langchain)
* [Context caching](./samples/context-caching)
* [Batch generation of content](./samples/batch-generation)

### Evaluation

* [DeepEval and Vertex AI](./samples/evaluation/deepeval)
* [Promptfoo and Vertex AI](./samples/evaluation/promptfoo)
* [LLM Guard and Vertex AI](./samples/evaluation/llmguard)

### Tracing

* [Tracing with Langtrace and Gemini](./samples/tracing/langtrace)