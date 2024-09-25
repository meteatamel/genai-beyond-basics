# Multimodal image storage and retrieval with Firestore Vector Store

In this sample, you'll learn how to store image embeddings to Firestore
Vector Store and later retrieve images based on similarity search on a keyword or image.

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

Let's add some images. 

Add an image from a Cloud Storage url:

```shell
python main.py --project_id=genai-atamel --image_paths gs://genai-atamel-firestore-images/landmark1.png
```

Add other images from a local folder:

```shell
python main.py --project_id=genai-atamel --image_paths ../images/landmark2.png ../images/landmark3.png
```

Add another image from an HTTP url:

```shell
python main.py --project_id=genai-atamel --image_paths https://atamel.dev/img/mete-512.jpg
```

At this point, you should see images and their embeddings saved to Firestore:

![Firestore with images](../images/firestore_with_images.png)

## Retrieve images

Now, retrieve and display images with a keyword:

```shell
python main.py --project_id=genai-atamel --search_by_keyword="stadium"
python main.py --project_id=genai-atamel --search_by_keyword="temple"
python main.py --project_id=genai-atamel --search_by_keyword="statue"
python main.py --project_id=genai-atamel --search_by_keyword="man"
```

You can also retrieve by searching similar images:

```shell
python main.py --project_id=genai-atamel --search_by_image="../images/landmark4.png"
```

## References

* [Build LLM-powered applications using LangChain](https://cloud.google.com/firestore/docs/langchain)
* [Firestore VectorStore + LangChain notebook](https://github.com/googleapis/langchain-google-firestore-python/blob/main/docs/vectorstores.ipynb)
