import argparse
import io
import os
import textwrap

import google
import matplotlib.pyplot as plt
from PIL import Image as PILImage
from google.cloud import firestore
from google.cloud import storage
from google.cloud.firestore_v1.vector import Vector
from langchain_google_firestore import FirestoreVectorStore
from langchain_google_vertexai import VertexAIEmbeddings
from vertexai.vision_models import Image, MultiModalEmbeddingModel
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    Part
)

FIRESTORE_DATABASE = "image-database"
FIRESTORE_COLLECTION = "ImageCollection"


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


def get_image_description(image_file_uri):
    model = GenerativeModel(
        "gemini-1.5-flash-001",
        system_instruction=[
            "You are a helpful image descriptor.",
        ],
        generation_config=GenerationConfig(
            temperature=0.9,
            top_p=1.0,
            top_k=32,
            candidate_count=1,
            max_output_tokens=8192,
        )
    )

    prompt = """
    Task: Look through the image carefully and provide a detailed description of the image in 3-4 sentences
    """

    image_file_uri = "gs://genai-atamel-firestore-images/landmark2.png"
    image_file = Part.from_uri(image_file_uri, mime_type="image/png")

    contents = [
        image_file,
        prompt,
    ]

    response = model.generate_content(contents)
    return response.text


def add_image_embeddings_to_firestore(args, bucket_name):
    """Adds image embeddings to Firestore, deleting any existing document with the same source first."""
    firestore_client = firestore.Client(project=args.project_id, database=FIRESTORE_DATABASE)
    collection = firestore_client.collection(FIRESTORE_COLLECTION)
    embeddings_llm = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")

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

        # Optional but get a description for the image from an LLM and add as content
        description = get_image_description(source_url)

        doc = {
            "content": description,
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
            location="us-central1",
            model_name="multimodalembedding"
        )
    )

    retriever = vector_store.as_retriever()
    docs = retriever.invoke(args.keyword)
    display_gcs_image(docs[0])


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
