from ollama import AsyncClient
import chainlit as cl

# Document Loaders
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=100)


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
            return file_content.decode('utf-8')
    # elif file.mime == "application/pdf":
    #     Loader = PyPDFLoader
    else:
        return None


@cl.on_message
async def main(message: cl.Message):
    # Files are attached in the message object and can be accessed using message.elements
    print(message.elements)
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    if message.elements:

        for file in message.elements:
            file_content = process_file(file)
            print(file_content)
            if file_content:
                message_history.append(
                    {"role": "user", "content": f"File Content: {file_content}"})

    msg = cl.Message(content="")
    await msg.send()

    async for part in await AsyncClient().chat(model='mistral', messages=message_history, stream=True):
        if token := part['message']['content'] or "":
            await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
