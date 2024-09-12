import argparse
import io
import os

from PIL import Image
from google.cloud import firestore
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_vertexai._image_utils import ImageBytesLoader

from image_enabled_firestore_vectorstore import ImageEnabledFirestoreVectorStore

FIRESTORE_DATABASE = "image-database"
FIRESTORE_COLLECTION = "ImageCollection"


def retrieve_and_display_image(vector_store, keyword):
    """Retrieves and displays an image based on a keyword."""
    print(f"Retrieving image for input: {keyword}")
    retriever = vector_store.as_retriever()
    docs = retriever.invoke(keyword)
    image_path = docs[0].metadata['metadata']['source']
    print(f"Retrieved image: {image_path}")
    display_image(image_path)


def display_image(image_path):
    image_loader = ImageBytesLoader()
    bytes_image = image_loader.load_bytes(image_path)
    image = Image.open(io.BytesIO(bytes_image))
    image.show()


def main():
    args = parse_args()

    # TODO: Can we use OpenClipEmbeddings?
    # https://github.com/langchain-ai/langchain/blob/master/cookbook/multi_modal_RAG_chroma.ipynb

    vector_store = ImageEnabledFirestoreVectorStore(
        client=firestore.Client(project=args.project_id, database=FIRESTORE_DATABASE),
        collection=FIRESTORE_COLLECTION,
        embedding_service=VertexAIEmbeddings(
            project=args.project_id,
            location="us-central1",
            model_name="multimodalembedding"
        )
    )

    if args.image_paths:
        ids = [os.path.basename(image_path) for image_path in args.image_paths]
        metadatas = [{"source": image_path} for image_path in args.image_paths]
        vector_store.add_images(args.image_paths, ids=ids, metadatas=metadatas)
    if args.keyword:
        retrieve_and_display_image(vector_store, args.keyword)


def parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description='Firestore and Cloud Storage image embedding save and retrieval')
    parser.add_argument('--project_id', type=str, required=True, help='Google Cloud project id')
    parser.add_argument('--image_paths', type=str, nargs='+', help='Paths to the images to process')
    parser.add_argument('--keyword', type=str, help='Keyword for the image retrieval')
    return parser.parse_args()


if __name__ == '__main__':
    main()
