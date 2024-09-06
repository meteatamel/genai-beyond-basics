# Multimodal image storage and retrieval with Chroma 

In this sample, you'll learn how to use Chroma to store images and their embeddings 
and later retrieve images based on similarity search on a keyword.

You can see the full sample in [main.py](main.py).

## Add images

First, add the images in [images](../images) folder to ChromaDB:

```shell
python main.py --folder_path=../images
```

## Retrieve images

Now, retrieve an image with a keyword:

```shell
python main.py --keyword="stadium"
```

You should now see the picture of Colosseum.


## References

* [Chroma Multimodal](https://docs.trychroma.com/guides/multimodal)
