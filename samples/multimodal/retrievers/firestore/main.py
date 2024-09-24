import argparse
import io
import os

from PIL import Image
from google.cloud import firestore
from langchain_google_firestore import FirestoreVectorStore
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_vertexai._image_utils import ImageBytesLoader
# Monkey patch FirestoreVectorStore with add_images
from firestore_vectorstore_add_images import add_images, similarity_search_image, _images_embedding_helper, \
    _encode_image

FirestoreVectorStore.add_images = add_images
FirestoreVectorStore.similarity_search_image = similarity_search_image
FirestoreVectorStore._encode_image = _encode_image
FirestoreVectorStore._images_embedding_helper = _images_embedding_helper

FIRESTORE_DATABASE = "image-database"
FIRESTORE_COLLECTION = "ImageCollection"


def retrieve_and_display_image(vector_store, keyword):
    """Retrieves and displays an image based on a keyword."""
    print(f"Retrieving image for input: {keyword}")
    retriever = vector_store.as_retriever()
    docs = retriever.invoke(keyword)
    image_uri = docs[0].metadata['metadata']['image_uri']
    print(f"Retrieved image: {image_uri}")
    display_image(image_uri)


def main():
    args = parse_args()

    vector_store = FirestoreVectorStore(
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
        metadatas = None  # [{"image_uri": image_path} for image_path in args.image_paths]
        vector_store.add_images(args.image_paths, ids=ids, metadatas=metadatas)
    if args.search_by_keyword:
        image_uri = search_by_keyword(args.search_by_keyword, vector_store)
        display_image(image_uri)
    if args.search_by_image:
        image_uri = search_by_image(args.search_by_image, vector_store)
        display_image(image_uri)


def parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description='Firestore and Cloud Storage image embedding save and retrieval')
    parser.add_argument('--project_id', type=str, required=True, help='Google Cloud project id')
    parser.add_argument('--image_paths', type=str, nargs='+', help='Paths to the images to upload to vector store')
    parser.add_argument('--search_by_keyword', type=str, help='Search by keyword for the image retrieval')
    parser.add_argument('--search_by_image', type=str, help='Search by image path for the image retrieval')
    return parser.parse_args()


def search_by_keyword(keyword, vector_store):
    print(f"Searching by keyword: {keyword}")
    doc = vector_store.similarity_search(keyword, k=1)[0]
    image_uri = doc.metadata['metadata']['image_uri']
    print(f"Retrieved image: {image_uri}")
    return image_uri


def search_by_image(image_path, vector_store):
    print(f"Searching by image path: {image_path}")
    doc = vector_store.similarity_search_image(image_path, k=1)[0]
    image_uri = doc.metadata['metadata']['image_uri']
    print(f"Retrieved image: {image_uri}")
    return image_uri


def display_image(image_uri):
    image_loader = ImageBytesLoader()
    bytes_image = image_loader.load_bytes(image_uri)
    image = Image.open(io.BytesIO(bytes_image))
    image.show()


if __name__ == '__main__':
    main()
