import argparse
import uuid

from google.cloud import firestore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_google_firestore import FirestoreChatMessageHistory
from langchain_google_vertexai import ChatVertexAI


def get_session_history(session_id, project_id):
    client = firestore.Client(
        project=project_id,
        database="chat-database")

    firestore_chat_history = FirestoreChatMessageHistory(
        session_id=session_id,
        collection="ChatMessages",
        client=client)

    return firestore_chat_history


def main():
    args = get_args_parser()

    llm = ChatVertexAI(
        project=args.project_id,
        location="us-central1",
        model="gemini-1.5-flash-001"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("placeholder", "{history}"),
            ("human", "{input}"),
        ]
    )

    chain = prompt | llm

    with_message_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: get_session_history(session_id, args.project_id),
        input_messages_key="input",
        history_messages_key="history",
    )

    # Read or create a session id
    if args.session_id:
        session_id = args.session_id
        print(f"Using the provided chat session id: {session_id}")
    else:
        session_id = str(uuid.uuid4())
        print(f"Created a new chat session id: {session_id}")

    while True:
        user_input = input("User > ")
        if user_input == "":
            break

        print("Assistant > ", end="")
        for chunk in with_message_history.stream(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}},
        ):
            print(chunk.content, end="", flush=True)


def get_args_parser():
    parser = argparse.ArgumentParser(description="Chat with history saved to Firestore")

    parser.add_argument('--project_id', type=str, required=True, help='Google Cloud project id (required)')
    parser.add_argument("--session_id", type=str, help="The chat session id")

    return parser.parse_args()


if __name__ == '__main__':
    main()
