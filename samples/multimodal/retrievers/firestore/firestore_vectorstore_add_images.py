import inspect
from typing import Optional, List, Iterable, Any
from google.cloud.firestore_v1.vector import Vector


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

    _ids: List[str] = []
    db_batch = self.client.batch()

    images_embeddings = self._images_embedding_helper(uris)

    for i, uri in enumerate(uris):
        doc_id = ids[i] if ids else None
        doc = self.collection.document(doc_id)
        _ids.append(doc.id)

        data = {
            self.content_field: "",
            self.embedding_field: Vector(images_embeddings[i]),
            self.metadata_field: metadatas[i] if metadatas else None,
        }

        db_batch.set(doc, data, merge=True)

    db_batch.commit()
    return _ids


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