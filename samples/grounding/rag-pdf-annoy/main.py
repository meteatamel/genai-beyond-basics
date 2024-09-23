import argparse
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Annoy
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import VertexAIEmbeddings, ChatVertexAI
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Reference: https://python.langchain.com/v0.2/docs/tutorials/pdf_qa/

def run_without_rag(args):
    llm = ChatVertexAI(
        project=args.project_id,
        location="us-central1",
        model="gemini-1.5-flash-001"
    )

    response = llm.invoke(args.prompt)

    print(f"Prompt: {args.prompt}")
    print(f"Response: {response.content}")


def setup_rag_chain(args):
    print(f"Load and parse the PDF: {args.pdf_path}")
    loader = PyPDFLoader(args.pdf_path)
    documents = loader.load()

    print("Split the document into chunks")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)

    print("Initialize the embedding model")
    embeddingsLlm = VertexAIEmbeddings(
        project=args.project_id,
        location="us-central1",
        model_name="textembedding-gecko@003",
        requests_per_minute=150
    )

    print("Create a vector store")
    vector_store = Annoy.from_documents(texts, embeddingsLlm)

    retriever = vector_store.as_retriever()

    print("Initialize the chat model")
    llm = ChatVertexAI(
        project=args.project_id,
        location="us-central1",
        model="gemini-1.5-flash-001"
    )

    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    print("Create RAG chain")
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    print("RAG is ready!")
    return rag_chain


def run_with_rag(args):
    rag_chain = setup_rag_chain(args)

    response = rag_chain.invoke({"input": args.prompt})
    print(f"Prompt: {args.prompt}")
    print(f"Response: {response['answer']}")


def get_args_parser():
    parser = argparse.ArgumentParser(description="PDF RAG with Langchain")

    parser.add_argument('--project_id', type=str, required=True, help='Google Cloud project id (required)')
    parser.add_argument("--prompt", type=str, required=True, help="Prompt for LLM")
    parser.add_argument('--pdf_path', type=str, help='The path to the PDF')

    return parser.parse_args()


def main():
    args = get_args_parser()
    if args.pdf_path:
        run_with_rag(args)
    else:
        run_without_rag(args)


if __name__ == '__main__':
    main()
