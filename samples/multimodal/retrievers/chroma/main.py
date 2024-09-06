import argparse
import os
import base64
import io
from PIL import Image
import matplotlib.pyplot as plt

from langchain_chroma import Chroma
from langchain_experimental.open_clip import OpenCLIPEmbeddings


def display_base64_image(base64_string):
    img_data = base64.b64decode(base64_string)
    img = Image.open(io.BytesIO(img_data))
    plt.imshow(img)
    plt.axis('off')
    plt.show()


def parse_args():
    parser = argparse.ArgumentParser(description='Chroma image embedding save and retrieval')
    parser.add_argument('--folder_path', type=str, help='Path for the images folder')
    parser.add_argument('--keyword', type=str, help='Keyword for the retrieval')
    return parser.parse_args()


def main():
    args = parse_args()

    vector_store = Chroma(
        persist_directory="chroma_db",
        collection_name="images_collection",
        embedding_function=OpenCLIPEmbeddings()
    )

    if args.folder_path:
        add_images(args, vector_store)

    if args.keyword:
        retrieve_and_display_image(args, vector_store)


def retrieve_and_display_image(args, vector_store):
    print(f"Retrieving image for input: {args.keyword}")
    retriever = vector_store.as_retriever()
    docs = retriever.invoke(args.keyword)
    display_base64_image(docs[0].page_content)


def add_images(args, vector_store):
    print(f"Adding image embeddings from {args.folder_path}/ to the vector store")
    image_uris = [args.folder_path + "/" + filename for filename in os.listdir(args.folder_path)]
    vector_store.add_images(uris=image_uris)


if __name__ == '__main__':
    main()
