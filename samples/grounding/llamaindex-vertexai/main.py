from llama_index.core import SimpleDirectoryReader
from llama_index.core import Document
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.vertex import Vertex
from llama_index.embeddings.vertex import VertexTextEmbedding

import google.auth

def main():

    print("Read PDF into documents")
    documents = SimpleDirectoryReader(
        input_files=["./cymbal-starlight-2024.pdf"]
    ).load_data()

    print("Initialize embedding model")
    credentials, project_id = google.auth.default()
    embed_model = VertexTextEmbedding(
        credentials=credentials,
        model_name= "text-embedding-005",
    )

    # Optional: If you stored index before, you can simply reload it
    # print("Reload index locally")
    # storage_context = StorageContext.from_defaults(persist_dir="index")
    # index = load_index_from_storage(storage_context, embed_model=embed_model)

    # Optional: You can customize chunk_size and chunk_overlap
    text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=20)

    print("Index documents")
    index = VectorStoreIndex.from_documents(
        documents, embed_model=embed_model, transformations=[text_splitter]
    )

    # Optional: You can store the index locally
    # print("Store index locally")
    # index.storage_context.persist(persist_dir="index")

    print("Initialize the query engine with the model")
    llm = Vertex(model="gemini-2.0-flash-001")
    query_engine = index.as_query_engine(llm=llm)

    question = "What is the cargo capacity of Cymbal Starlight?"
    response = query_engine.query(question)
    print(f"Question: {question}")
    print(f"Response: {str(response)}")


if __name__ == '__main__':
    main()
