import os
from typing import Optional

import google
from google.cloud import storage
from google.cloud.firestore_v1 import CollectionReference, Client
from google.cloud.firestore_v1.base_query import BaseFilter
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from google.cloud.firestore_v1.vector import Vector
from langchain_core.embeddings import Embeddings
from langchain_google_firestore import FirestoreVectorStore
from vertexai.vision_models import MultiModalEmbeddingModel, Image
from vertexai.generative_models import GenerationConfig, GenerativeModel, Part


class ImageEnabledFirestoreVectorStore(FirestoreVectorStore):
    """Extends FirestoreVectorStore to add image handling capabilities."""

    def __init__(self,
                 project_id: str,
                 bucket_name: str,
                 collection: CollectionReference | str,
                 embedding_service: Embeddings,
                 client: Optional[Client] = None,
                 content_field: str = "content",
                 metadata_field: str = "metadata",
                 embedding_field: str = "embedding",
                 distance_strategy: Optional[DistanceMeasure] = DistanceMeasure.COSINE,
                 filters: Optional[BaseFilter] = None
                 ):
        super().__init__(collection, embedding_service, client, content_field,
                         metadata_field, embedding_field, distance_strategy, filters)
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.storage_client = storage.Client(project_id)

    def add_images(self, image_uris):
        """Adds images to the Firestore vector store.

        Args:
            image_uris: A list of image URIs (e.g., URLs or paths to local images).
        """
        image_gcs_uris = self._upload_images_to_gcs_storage(image_uris)
        self._add_image_embeddings_to_firestore(image_uris, image_gcs_uris)

    def _upload_images_to_gcs_storage(self, image_uris):
        """Uploads images to Google Cloud Storage."""
        print(f"Upload images to bucket: {self.bucket_name}")
        try:
            bucket = self.storage_client.get_bucket(self.bucket_name)
        except google.cloud.exceptions.NotFound:
            print(f"Create bucket: {self.bucket_name}")
            bucket = self.storage_client.create_bucket(self.bucket_name)

        image_gcs_uris = []
        for image_uri in image_uris:
            file_name = os.path.basename(image_uri)
            blob = bucket.blob(file_name)
            print(f"Uploading {image_uri} to bucket {self.bucket_name}")
            blob.upload_from_filename(os.path.join(image_uri))
            image_gcs_uris.append( f"gs://{self.bucket_name}/{blob.name}")

        return image_gcs_uris

    def _add_image_embeddings_to_firestore(self, image_uris, image_gcs_uris):
        """Adds image embeddings to Firestore, deleting any existing document with the same source first."""
        print("Add image embeddings to Firestore")
        embeddings_llm = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")

        for index, image_uri in enumerate(image_uris):
            image_gcs_uri = image_gcs_uris[index]
            print(f"Adding {image_uri}...")

            # Query for existing documents with the same source
            query = self.collection.where("metadata.source", "==", image_gcs_uri)
            docs = query.stream()

            # Delete existing documents if found
            for doc in docs:
                print(f"Deleting existing document with gcs uri: {image_gcs_uri}")
                doc.reference.delete()

            # Optional but get a description for the image from an LLM and add as content
            description = self._get_image_description(image_gcs_uri)
            print(f"Generated description for the image: {description}...")

            # Now add the new document
            image = Image.load_from_file(image_uri)
            embeddings = embeddings_llm.get_embeddings(image=image)
            print("Generated embeddings for the image...")

            doc = {
                "content": description,
                "embedding": Vector(embeddings.image_embedding),
                "metadata": {
                    "source": image_gcs_uri
                }
            }
            self.collection.add(doc)

    @staticmethod
    def _get_image_description(image_gcs_uri):
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

        image_file = Part.from_uri(image_gcs_uri, mime_type="image/png")

        contents = [
            image_file,
            prompt,
        ]

        response = model.generate_content(contents)
        return response.text