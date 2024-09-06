import argparse
import io
import os

import google
import matplotlib.pyplot as plt
from PIL import Image as PILImage
from google.cloud import firestore
from google.cloud import storage
from google.cloud.firestore_v1.vector import Vector
from langchain_google_firestore import FirestoreVectorStore
from langchain_google_vertexai import VertexAIEmbeddings
from vertexai.vision_models import Image, MultiModalEmbeddingModel

FIRESTORE_DATABASE = "image-database"
FIRESTORE_COLLECTION = "ImageCollection"
EMBEDDINGS_MODEL_NAME = "multimodalembedding"
VERTEX_AI_LOCATION = "us-central1"


def display_gcs_image(gcs_url):
    """Displays an image from Google Cloud Storage."""
    bucket_name, blob_name = parse_gcs_url(gcs_url)
    img_bytes = download_as_bytes(bucket_name, blob_name)
    img = PILImage.open(io.BytesIO(img_bytes))
    plt.imshow(img)
    plt.axis('off')
    plt.show()


def parse_gcs_url(gcs_url):
    """Parses a GCS URL into bucket name and blob name."""
    path = gcs_url[5:] # remove gs://
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


def add_image_embeddings_to_firestore(args, bucket_name):
    """Adds image embeddings to Firestore, deleting any existing document with the same source first."""
    firestore_client = firestore.Client(project=args.project_id, database=FIRESTORE_DATABASE)
    collection = firestore_client.collection(FIRESTORE_COLLECTION)
    embeddings_llm = MultiModalEmbeddingModel.from_pretrained(EMBEDDINGS_MODEL_NAME)

    image_files = [f for f in os.listdir(args.folder_path) if os.path.isfile(os.path.join(args.folder_path, f))]

    for image_file in image_files:
        source_url = f"gs://{bucket_name}/{image_file}"
        print(f"Processing {image_file}...")

        # Query for existing documents with the same source
        query = collection.where("metadata.source", "==", source_url)
        docs = query.stream()

        # Delete existing documents if found
        for doc in docs:
            print(f"Deleting existing document with source: {source_url}")
            doc.reference.delete()

        # Now add the new document
        print(f"Uploading embeddings to firestore collection {collection.id}")
        image = Image.load_from_file(os.path.join(args.folder_path, image_file))
        embeddings = embeddings_llm.get_embeddings(image=image)

        doc = {
            "content": "",
            "embedding": Vector(embeddings.image_embedding),
            "metadata": {
                "source": source_url
            }
        }
        collection.add(doc)

    print("Images embeddings uploaded successfully!")


def add_images_to_gcs_storage(args):
    """Uploads images to Google Cloud Storage."""
    storage_client = storage.Client(project=args.project_id)
    bucket_name = f"{args.project_id}-firestore-images"
    try:
        bucket = storage_client.get_bucket(bucket_name)
    except google.cloud.exceptions.NotFound:
        bucket = storage_client.create_bucket(bucket_name)

    image_files = [f for f in os.listdir(args.folder_path) if os.path.isfile(os.path.join(args.folder_path, f))]

    for image_file in image_files:
        blob = bucket.blob(image_file)
        print(f"Uploading {image_file} to bucket {bucket_name}")
        blob.upload_from_filename(os.path.join(args.folder_path, image_file))

    print("Images uploaded successfully!")
    return bucket_name


def retrieve_and_display_image(args):
    """Retrieves and displays an image based on a keyword."""
    print(f"Retrieving image for input: {args.keyword}")

    vector_store = FirestoreVectorStore(
        client=firestore.Client(project=args.project_id, database=FIRESTORE_DATABASE),
        collection=FIRESTORE_COLLECTION,
        embedding_service=VertexAIEmbeddings(
            project=args.project_id,
            location=VERTEX_AI_LOCATION,
            model_name=EMBEDDINGS_MODEL_NAME
        )
    )

    retriever = vector_store.as_retriever()
    docs = retriever.invoke(args.keyword)
    display_gcs_image(docs[0].metadata['metadata']['source'])


def parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description='Firestore and Cloud Storage image embedding save and retrieval')
    parser.add_argument('--project_id', type=str, required=True, help='Google Cloud project id')
    parser.add_argument('--folder_path', type=str, help='Path for the images folder')
    parser.add_argument('--keyword', type=str, help='Keyword for the retrieval')
    return parser.parse_args()


def main():
    """Main execution flow."""
    args = parse_args()

    if args.folder_path:
        bucket_name = add_images_to_gcs_storage(args)
        add_image_embeddings_to_firestore(args, bucket_name)

    if args.keyword:
        retrieve_and_display_image(args)


if __name__ == '__main__':
    main()
