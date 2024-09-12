# Multimodal image storage and retrieval with Firestore and Cloud Storage 

In this sample, you'll learn how to store image embeddings to Firestore
and later retrieve images based on similarity search on a keyword.

You can see the full sample in [main.py](main.py).

## Setup Firestore

Make sure you're logged in:

```shell
gcloud auth application-default login
```

Enable Firestore API:

```shell
gcloud services enable firestore.googleapis.com
```

Create a Firestore database:

```shell
gcloud firestore databases create --database image-database --location=europe-west1
```

Create a Firestore index for retrieval later:

```shell
gcloud alpha firestore indexes composite create --project=your-project-id \
 --database="image-database" --collection-group=ImageCollection --query-scope=COLLECTION \
 --field-config=vector-config='{"dimension":"1408","flat": "{}"}',field-path=embedding
```

## Add images

First, add the images in [images](../images) folder to Cloud Storage and image embeddings to Firestore:

```shell
python main.py --project_id=your-project-id --folder_path=../images --bucket_name=your_bucket_to_save_images
```

## Retrieve images

Now, retrieve an image with a keyword:

```shell
python main.py --project_id=your-project-id --keyword="stadium"
```

You should now see the picture of Colosseum.


## References

* [Build LLM-powered applications using LangChain](https://cloud.google.com/firestore/docs/langchain)
* [Firestore VectorStore + LangChain notebook](https://github.com/googleapis/langchain-google-firestore-python/blob/main/docs/vectorstores.ipynb)
