from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import VertexAIEmbeddings, ChatVertexAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

PROJECT_ID = "genai-atamel"
LOCATION = "us-central1"
PDF_PATH = "cymbal-starlight-2024.pdf"

EMBEDDING_MODEL_NAME_1 = "textembedding-gecko@003"
EMBEDDING_MODEL_NAME_2 = "text-embedding-005"
EMBEDDING_MODEL_NAME = EMBEDDING_MODEL_NAME_1

CHUNK_SIZE_1 = 500
CHUNK_SIZE_2 = 200
CHUNK_SIZE = CHUNK_SIZE_2

CHUNK_OVERLAP_1 = 100
CHUNK_OVERLAP_2 = 0
CHUNK_OVERLAP = CHUNK_OVERLAP_2

SYSTEM_PROMPT_1 = """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer 
the question. If you don't know the answer, say that you 
don't know. Use three sentences maximum and keep the 
answer concise.

{context}"""
SYSTEM_PROMPT_2 = """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer 
the question. Only answer the question and if you don't know the answer, 
just say I don't know.

{context}"""
SYSTEM_PROMPT = SYSTEM_PROMPT_1

MODEL_NAME="gemini-1.5-flash-002"
TEMPERATURE=1

def setup_rag_chain():
    print(f"Setting up RAG chain")

    print(f"Load and parse the PDF: {PDF_PATH}")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    print("Split the document into chunks")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    texts = text_splitter.split_documents(documents)

    print(f"Initialize the embedding model: {EMBEDDING_MODEL_NAME}")
    embeddings_model = VertexAIEmbeddings(
        project=PROJECT_ID,
        model_name=EMBEDDING_MODEL_NAME
    )

    print("Create a vector store")
    vector_store = InMemoryVectorStore.from_documents(
        texts,
        embedding=embeddings_model,
    )

    #retriever = vector_store.as_retriever()
    retriever = vector_store.as_retriever(search_kwargs={"k": 1})

    print(f"Initialize the model: {MODEL_NAME}")
    model = ChatVertexAI(
        project=PROJECT_ID,
        location=LOCATION,
        model=MODEL_NAME,
        temperature=TEMPERATURE
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

