# RAG with a PDF using LangChain and Firestore Vector Store 

In this sample, you'll learn how to use a PDF as a RAG backend using LangChain and Firestore for Vector Store.

You can see the full sample in [main.py](main.py).

## Without RAG

First, let's run the sample without any RAG setup:

```sh
python main.py --project_id your-project-id \
  --prompt "What is the cargo capacity of Cymbal Starlight?"  
```

You get a response where the LLM does not really know what Cymbal is:

```sh
Prompt: What is the cargo capacity of Cymbal Starlight?
Response: Please provide me with more context! "Cymbal Starlight" could refer to many things, such as:

* **A spaceship:**  If it's a fictional spaceship, the cargo capacity would be determined by the story's creator. 
* **A real-world ship:** If it's a real ship, you'd need to specify the type of ship and its name (e.g., "Cymbal Starlight" cargo ship, "Cymbal Starlight" yacht). 
* **A vehicle:**  It could also refer to a truck or other vehicle. 

Once you give me more information, I can help you find the cargo capacity. 
```

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
gcloud firestore databases create --database pdf-database --location=europe-west1
```

Create a Firestore index:

```shell
gcloud alpha firestore indexes composite create --project=your-project-id \
 --database="pdf-database" --collection-group=PdfCollection --query-scope=COLLECTION \
 --field-config=vector-config='{"dimension":"768","flat": "{}"}',field-path=embedding
```

## Setup RAG

Now, you can setup a RAG chain with the [cymbal-starlight-2024.pdf](./cymbal-starlight-2024.pdf) file. 
It is a user’s manual of a fictitious vehicle called Cymbal Starlight.

Checkout `setup_rag_chain` method of [main.py](main.py) on how to set this up.

## With RAG

We're ready to ask questions about the vehicle **with** RAG enabled.

```sh
python main.py --project_id your-project-id \
  --prompt "What is the cargo capacity of Cymbal Starlight?" \
  --pdf_path="cymbal-starlight-2024.pdf"
```

First, you see RAG is setup:

```shell
Load and parse the PDF: cymbal-starlight-2024.pdf
Split the document into chunks
Initialize the embedding model
Create a vector store
Initialize the chat model
Create RAG chain
RAG is ready!
```

Then, you get a response back: 

```sh
Prompt: What is the cargo capacity of Cymbal Starlight?
Response: The Cymbal Starlight 2024 has a cargo capacity of 13.5 cubic feet. The cargo area is located in the trunk of 
the vehicle. To access the cargo area, open the trunk lid using the trunk release lever located in the driver's footwell. 
```

Yay, it works!

## References

* [Build LLM-powered applications using LangChain](https://cloud.google.com/firestore/docs/langchain)
* [Firestore VectorStore + LangChain notebook](https://github.com/googleapis/langchain-google-firestore-python/blob/main/docs/vectorstores.ipynb)
