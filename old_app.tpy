from ollama import AsyncClient
import ollama
import chainlit as cl

from chainlit.server import app
from fastapi import Request
from fastapi.responses import (
    HTMLResponse,
)

# Document Loaders
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=100)


@app.get("/hello")
def hello(request: Request):
    return HTMLResponse("Hello World")


@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )


# TODO - Get File Loader tools working
def process_file(file):
    if file.mime == "text/plain":
        with open(file.path, 'rb') as f:
            file_content = f.read()
            # Decode the binary content to a string
            return [file_content.decode('utf-8')]
    elif file.mime == "application/pdf":
        Loader = PyPDFLoader

        loader = Loader(file.path)
        pages = loader.load_and_split(text_splitter)

        return [page.page_content for page in pages]
    else:
        return []


@cl.on_message
async def main(message: cl.Message):
    # Files are attached in the message object and can be accessed using message.elements
    print(message.elements)
    print(message.content)
    embeddings = ollama.embeddings(model="mistral", prompt=message.content)
    print(len(embeddings['embedding']))

    message_history = cl.user_session.get("message_history")

    if message.elements:
        for file in message.elements:
            # TODO - this doesn't work yet, might have to use embeddings
            file_content = process_file(file)

            if file_content:
                for content in file_content:
                    message_history.append(
                        {"role": "user", "content": f"File Content: {content}"})

    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    async for part in await AsyncClient().chat(model='mistral', messages=message_history, stream=True):
        if token := part['message']['content'] or "":
            await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
