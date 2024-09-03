# LangChain - Chat with in-memory history

## Introduction

[LangChain](https://www.langchain.com/) is a popular framework to build with LLMs by chaining interoperable components.

In this sample, you'll see how to chat to Gemini on Vertex AI using LangChain with in-memory chat history.

## Build the app

You can take a look at the chat app with history in [chat.py](chat.py). 

## Run the app

Set your Google Cloud project id:

```sh
export PROJECT_ID=your-google-cloud-project-id
```

Run:

```sh
python main.py
```

You can have a chat with Gemini now:

```sh
User > Hello, my name is Mete
Assistant > Hello Mete! 👋 It's nice to meet you. 😊 What can I do for you today? 
User > Do you remember my name?
Assistant > Yes, I do!  I remember your name is Mete. 😊  I'm still learning, but I'm getting better at remembering things.  
What can I help you with today?
```

## References

* [A comparative overview of LangChain, Semantic Kernel, AutoGen and more](https://medium.com/data-science-at-microsoft/harnessing-the-power-of-large-language-models-a-comparative-overview-of-langchain-semantic-c21f5c19f93e).
