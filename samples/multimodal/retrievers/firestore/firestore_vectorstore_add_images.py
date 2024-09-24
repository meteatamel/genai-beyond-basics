import base64
import inspect
import re
import requests
from typing import Optional, List, Iterable, Any
from google.cloud import storage
from google.cloud.firestore_v1.vector import Vector
from google.cloud.firestore_v1.base_query import BaseFilter
from langchain_core.documents import Document
from langchain_google_firestore.document_converter import convert_firestore_document

DEFAULT_TOP_K = 4


def add_images(
        self,
        uris: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        **kwargs: Any,
) -> List[str]:
    """Adds image embeddings to Firestore vector store.

    Args:
        uris: A list of image uris (local, Google Cloud Storage or web)
        metadatas: The metadata to add to the vector store. Defaults to None.
        ids: The document ids to use for the new documents. If not provided, new
        document ids will be generated.

    Returns:
        List[str]: The list of document ids added to the vector store.
    """
    images_len = len(list(uris))
    ids_len_match = not ids or len(ids) == images_len
    metadatas_len_match = not metadatas or len(metadatas) == images_len

    if images_len == 0:
        raise ValueError("No images provided to add to the vector store.")

    if not metadatas_len_match:
        raise ValueError(
            "The length of metadatas must be the same as the length of images or zero."
        )

    if not ids_len_match:
        raise ValueError(
            "The length of ids must be the same as the length of images or zero."
        )

    if metadatas is None:
        metadatas = [{"image_uri": uri} for uri in uris]

    image_encodings = [self._encode_image(uri) for uri in uris]
    image_embeddings = self._images_embedding_helper(uris)

    _ids: List[str] = []
    db_batch = self.client.batch()

    for i, uri in enumerate(uris):
        doc_id = ids[i] if ids else None
        doc = self.collection.document(doc_id)
        _ids.append(doc.id)

        data = {
            self.content_field: image_encodings[i],
            self.embedding_field: Vector(image_embeddings[i]),
            self.metadata_field: metadatas[i] if metadatas else None,
        }

        db_batch.set(doc, data, merge=True)

    db_batch.commit()
    return _ids


def similarity_search_image(
    self,
    image_uri: str,
    k: int = DEFAULT_TOP_K,
    filters: Optional[BaseFilter] = None,
    **kwargs: Any,
) -> List[Document]:
    """Run image similarity search with Firestore.

    Raises:
        FailedPrecondition: If the index is not created.

    Args:
        image_uri: The image uri.
        k: The number of documents to return. Defaults to 4.
        filters: The pre-filter to apply to the query. Defaults to None.

    Returns:
        List[Document]: List of documents most similar to the image.
    """

    embedding = self._images_embedding_helper([image_uri])[0]
    docs = self._similarity_search(
        embedding, k, filters=filters
    )
    return [
        convert_firestore_document(doc, page_content_fields=[self.content_field])
        for doc in docs
    ]


def _encode_image(self, uri: str) -> str:
    """Get base64 string from a image URI."""
    gcs_uri = re.match("gs://(.*?)/(.*)", uri)
    if gcs_uri:
        bucket_name, object_name = gcs_uri.groups()
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(object_name)
        return base64.b64encode(blob.download_as_bytes()).decode('utf-8')

    web_uri = re.match(r"^(https?://).*", uri)
    if web_uri:
        response = requests.get(uri, stream=True)
        response.raise_for_status()
        return base64.b64encode(response.content).decode("utf-8")

    with open(uri, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def _images_embedding_helper(self, image_uris: List[str]) -> List[List[float]]:

    if not hasattr(self.embedding_service, "embed_image"):
        raise ValueError(
            "Please use an embedding model that supports embed_image method."
        )

    method = getattr(self.embedding_service, 'embed_image')
    signature = inspect.signature(method)
    parameters = list(signature.parameters.values())
    first_param = parameters[0]

    if first_param.annotation == List[str] or first_param.annotation == list:
        embeddings = self.embedding_service.embed_image(image_uris)
    elif first_param.annotation == str:
        embeddings = [self.embedding_service.embed_image(uri) for uri in image_uris]
    else:
        raise Exception(
            f"Please use an embedding model that supports embed_image method."
        )

    return embeddings