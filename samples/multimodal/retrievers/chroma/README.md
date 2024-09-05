# Multimodal image storage and retrieval with Chroma 

In this sample, you'll learn how to use Chroma vector database to store and retrieve images with multimodal embeddings.

You can see the full sample in [main.py](main.py).

## Add images

First, add the images in [images](./images) folder to ChromaDB:

```shell
python main.py --folder_path=images
```

## Retrieve images

Now, retrieve an image with a keyword:

```shell
python main.py --input=stadium
```

## References

* [Build LLM-powered applications using LangChain](https://cloud.google.com/firestore/docs/langchain)
* [Firestore VectorStore + LangChain notebook](https://github.com/googleapis/langchain-google-firestore-python/blob/main/docs/vectorstores.ipynb)
