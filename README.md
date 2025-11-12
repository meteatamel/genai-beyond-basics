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
* [RAG with a PDF using LlamaIndex and SimpleVectorStore on Vertex AI](./samples/grounding/llamaindex-vertexai)
* [LlamaIndex on Vertex AI with RAG API](./samples/grounding/llamaindex-vertexai-ragapi)
* [RAG with a PDF using File Search Tool in Gemini API](./samples/grounding/file-search-tool)

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

* [Gen AI evaluation service in Vertex AI](./samples/evaluation/vertexai_genai_eval)
* [DeepEval and Gemini](./samples/evaluation/deepeval)
* [Promptfoo and Vertex AI](./samples/evaluation/promptfoo)

### Guardrails

* [Model Armor](./samples/guardrails/model_armor)
* [LLM Guard and Vertex AI](./samples/guardrails/llmguard)

### Tracing

* [Tracing with Langtrace and Gemini](./samples/tracing/langtrace)

### Protocols

* [Model Context Protocol (MCP)](./samples/protocols/mcp/)
* [Agent2Agent Protocol (A2A)](./samples/protocols/a2a/)