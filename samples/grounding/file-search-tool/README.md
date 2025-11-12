# RAG with a PDF using File Search Tool in Gemini API

In this sample, you'll learn how to use a PDF as a RAG backend using File Search Tool in Gemini API.

You can see the full sample in [main.py](main.py).

> [!NOTE]
> File Search Tool is only supported by Gemini API right now (not Vertex AI API)

## Without file search tool

First, let's run the sample without the file search tool.

Make sure you get and set your Gemini API key:

```shell
export GEMINI_API_KEY=your-gemini-api-key
```

```sh
python main.py generate "What's the cargo capacity of Cymbal Starlight?"
```

You get a response where the LLM does not really know what Cymbal is:

```sh
Generating content with file search store 'None'
Response: I couldn't find any information about a vessel named "Cymbal Starlight" with a publicly listed cargo capacity.

It's possible:
*   It's a very obscure or private vessel.
*   It's a fictional vessel.
*   The name might be slightly different.

Could you provide more context or verify the name?
```

## Create a file search store

Now, let's create a file search store:

```shell
python main.py create my-file-search-store

Created a file search store:
  my-file-search-store - fileSearchStores/myfilesearchstore-xainjwkp2jhy
```

## Upload the PDF

Upload the PDF file to the file search store:

```shell
python main.py upload fileSearchStores/myfilesearchstore-xainjwkp2jhy cymbal-starlight-2024.pdf

Uploading file 'cymbal-starlight-2024.pdf' to file search store 'fileSearchStores/myfilesearchstore-xainjwkp2jhy'
Waiting for upload to complete...
Upload completed.
```

## With file search tool

We're ready to ask questions about the vehicle with file search tool enabled:

```sh
python main.py generate "What's the cargo capacity of Cymbal Starlight?" fileSearchStores/myfilesearchstore-xainjwkp2jhy
```

```shell
Generating content with file search store 'fileSearchStores/myfilesearchstore-xainjwkp2jhy'
Response: The Cymbal Starlight 2024 has a cargo capacity of 13.5 cubic feet, which is located in the trunk of the vehicle. It is important to distribute the weight evenly and not overload the trunk, as this could impact the vehicle's handling and stability. The vehicle can also accommodate up to two suitcases in the trunk, and it is recommended to use soft-sided luggage to maximize space and cargo straps to secure it while driving.
Grounding sources:  cymbal-starlight-2024.pdf
```

Yay, it works!

## References

* [Blog: Introducing the File Search Tool in Gemini API](https://blog.google/technology/developers/file-search-gemini-api/)
* [Docs: File Search](https://ai.google.dev/gemini-api/docs/file-search)
