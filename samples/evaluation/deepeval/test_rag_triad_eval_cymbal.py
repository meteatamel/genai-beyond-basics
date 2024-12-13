import os

from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ContextualRelevancyMetric
from deepeval import evaluate
from vertex_ai.google_vertex_ai import GoogleVertexAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_vertexai import VertexAIEmbeddings, ChatVertexAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Using the RAG Triad for RAG evaluation:
# https://docs.confident-ai.com/docs/guides-rag-triad

MODEL = "gemini-1.5-flash-002"
SYSTEM_PROMPT = """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer 
the question. If you don't know the answer, say that you 
don't know. Use three sentences maximum and keep the 
answer concise.

{context}"""
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def get_project_id():
    project_id = os.environ.get("GOOGLE_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_PROJECT_ID environment variable not set")
    return project_id


def setup_rag_chain(model_str):
    print(f"Setting up RAG chain with model: {model_str}")

    pdf_path = "cymbal-starlight-2024.pdf"
    print(f"Load and parse the PDF: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print("Split the document into chunks")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    texts = text_splitter.split_documents(documents)

    print("Initialize the embedding model")
    embeddings_model = VertexAIEmbeddings(
        project=get_project_id(),
        model_name="textembedding-gecko@003"
    )

    print("Create a vector store")
    vector_store = InMemoryVectorStore.from_documents(
        texts,
        embedding=embeddings_model,
    )

    retriever = vector_store.as_retriever()

    print("Initialize the chat model")
    model = ChatVertexAI(
        project=get_project_id(),
        location="us-central1",
        model=MODEL
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{input}"),
        ]
    )

    print("Create RAG chain")
    question_answer_chain = create_stuff_documents_chain(model, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    print("RAG is ready!")
    return rag_chain


def test_with_rag():
    rag_chain = setup_rag_chain(MODEL)

    inputs = [
        "What is the cargo capacity of Cymbal Starlight?",
        "Is there a tire repair kit in Cymbal Starlight?",
        "What's the emergency roadside assistance number for Cymbal?"
    ]

    test_cases = []

    for input in inputs:
        print(f"Input: {input}")

        print("Invoking RAG chain")
        response = rag_chain.invoke({"input": input})

        output = response['answer']
        print(f"Output: {output}")

        retrieval_context = [doc.page_content for doc in response['context']]
        print(f"Retrieval context: {retrieval_context}")

        test_case = LLMTestCase(
            input=input,
            actual_output=output,
            retrieval_context=retrieval_context
        )
        test_cases.append(test_case)


    eval_model = GoogleVertexAI(model_name="gemini-1.5-pro-002",
                           project=get_project_id(),
                           location="us-central1")

    metrics = [
        AnswerRelevancyMetric(model=eval_model),
        FaithfulnessMetric(model=eval_model),
        ContextualRelevancyMetric(model=eval_model)
    ]

    evaluation_result = evaluate(test_cases=test_cases, metrics=metrics)



