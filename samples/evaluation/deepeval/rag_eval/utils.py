import os

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import VertexAIEmbeddings, ChatVertexAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

PDF_PATH = "cymbal-starlight-2024.pdf"
SYSTEM_PROMPT = """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer 
the question. If you don't know the answer, say that you 
don't know. Use three sentences maximum and keep the 
answer concise.

{context}"""
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
EMBEDDING_MODEL_NAME = "text-embedding-005"

def setup_rag_chain(chat_model_name):
    print(f"Setting up RAG chain")

    print(f"Load and parse the PDF: {PDF_PATH}")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    print("Split the document into chunks")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    texts = text_splitter.split_documents(documents)

    print(f"Initialize the embedding model: {EMBEDDING_MODEL_NAME}")
    embeddings_model = VertexAIEmbeddings(
        project=get_project_id(),
        model_name=EMBEDDING_MODEL_NAME
    )

    print("Create a vector store")
    vector_store = InMemoryVectorStore.from_documents(
        texts,
        embedding=embeddings_model,
    )

    retriever = vector_store.as_retriever()

    print(f"Initialize the chat model: {chat_model_name}")
    model = ChatVertexAI(
        project=get_project_id(),
        location="us-central1",
        model=chat_model_name
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


def get_project_id():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set")
    return project_id

