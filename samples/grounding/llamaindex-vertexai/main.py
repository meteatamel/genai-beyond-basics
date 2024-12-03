from llama_index.core import SimpleDirectoryReader
from llama_index.core import Document
from llama_index.core import VectorStoreIndex
from llama_index.llms.vertex import Vertex
from llama_index.embeddings.vertex import VertexTextEmbedding
import google.auth

def main():

    print("Read PDF into documents")
    documents = SimpleDirectoryReader(
        input_files=["./cymbal-starlight-2024.pdf"]
    ).load_data()

    print("Combine document for each page back into a single document")
    document = Document(text="\n\n".join([doc.text for doc in documents]))

    print("Initialize embedding model")
    credentials, project_id = google.auth.default()
    embed_model = VertexTextEmbedding(credentials=credentials)

    print("Index document")
    index = VectorStoreIndex.from_documents(
        [document], embed_model=embed_model
    )

    print("Initialize query engine with the model")
    llm = Vertex(model="gemini-1.5-flash-002", temperature=0.1)
    query_engine = index.as_query_engine(llm=llm)

    question = "What is the cargo capacity of Cymbal Starlight?"
    response = query_engine.query(
        "What is the cargo capacity of Cymbal Starlight?"
    )
    print(f"Question: {question}")
    print(f"Response: {str(response)}")


if __name__ == '__main__':
    main()
