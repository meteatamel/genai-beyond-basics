# RAG with a PDF using LangChain and Annoy Vector Store 

In this sample, you'll learn how to use a PDF as a RAG backend using LangChain and Annoy for Vector Store.

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

## Setup RAG

Now, you can setup a RAG chain with the [cymbal-starlight-2024.pdf](./cymbal-starlight-2024.pdf) file. 
It is a user’s manual of a fictitious vehicle called Cymbal Starlight.

Checkout `setup_rag_chain` method of [main.py](main.py) on how to set this up.

## With RAG

Finally, we're ready to ask questions about the vehicle **with** RAG enabled.

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

* [Build a Retrieval Augmented Generation (RAG) App](https://python.langchain.com/v0.2/docs/tutorials/pdf_qa/)
