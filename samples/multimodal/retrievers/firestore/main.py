import argparse
import io
import os
import textwrap

import matplotlib.pyplot as plt
from PIL import Image as PILImage
from google.cloud import firestore
from google.cloud import storage
from langchain_google_vertexai import VertexAIEmbeddings

from image_enabled_firestore_vectorstore import ImageEnabledFirestoreVectorStore

FIRESTORE_DATABASE = "image-database"
FIRESTORE_COLLECTION = "ImageCollection"


def retrieve_and_display_image(vector_store, keyword):
    """Retrieves and displays an image based on a keyword."""
    print(f"Retrieving image for input: {keyword}")
    retriever = vector_store.as_retriever()
    docs = retriever.invoke(keyword)
    display_gcs_image(docs[0])


def display_gcs_image(image_doc):
    """Displays an image from Google Cloud Storage with description below."""
    gcs_url = image_doc.metadata['metadata']['source']
    bucket_name, blob_name = parse_gcs_url(gcs_url)
    img_bytes = download_as_bytes(bucket_name, blob_name)
    img = PILImage.open(io.BytesIO(img_bytes))

    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.axis('off')

    fig_width_inches = fig.get_figwidth()
    chars_per_line = int(fig_width_inches * 10)
    wrapped_text = textwrap.fill(image_doc.page_content, chars_per_line)
    ax.text(0.5, -0.1, wrapped_text, transform=ax.transAxes,
            ha='center', va='top')

    plt.tight_layout()
    plt.show()


def parse_gcs_url(gcs_url):
    """Parses a GCS URL into bucket name and blob name."""
    path = gcs_url[5:]  # remove gs://
    bucket_name, blob_name = path.split('/')
    return bucket_name, blob_name


def download_as_bytes(bucket_name, source_blob_name):
    """Downloads a blob from GCS as bytes."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    img_bytes = blob.download_as_bytes()
    print(f"Downloaded {source_blob_name} from bucket {bucket_name}")
    return img_bytes


def main():
    args = parse_args()

    vector_store = ImageEnabledFirestoreVectorStore(
        project_id=args.project_id,
        bucket_name=f"{args.project_id}-firestore-images" if not args.bucket_name else args.bucket_name,
        client=firestore.Client(project=args.project_id, database=FIRESTORE_DATABASE),
        collection=FIRESTORE_COLLECTION,
        embedding_service=VertexAIEmbeddings(
            project=args.project_id,
            location="us-central1",
            model_name="multimodalembedding"
        )
    )

    if args.folder_path:
        image_paths = [os.path.join(args.folder_path, file) for file in os.listdir(args.folder_path)]
        vector_store.add_images(image_paths)
    if args.keyword:
        retrieve_and_display_image(vector_store, args.keyword)


def parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description='Firestore and Cloud Storage image embedding save and retrieval')
    parser.add_argument('--project_id', type=str, required=True, help='Google Cloud project id')
    parser.add_argument('--folder_path', type=str, help='Path for the images folder')
    parser.add_argument('--bucket_name', type=str, help='Optional bucket name to store images to')
    parser.add_argument('--keyword', type=str, help='Keyword for the retrieval')
    return parser.parse_args()


if __name__ == '__main__':
    main()
