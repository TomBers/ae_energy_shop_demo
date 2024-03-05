import os
from pinecone import Pinecone, ServerlessSpec
from langchain.vectorstores.pinecone import Pinecone as PineconeVectorStore
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from chainlit.types import AskFileResponse
import chainlit as cl

pc = Pinecone(
    api_key=os.environ.get("PINECONE_API_KEY")
)

index_name = "ae-chat-demo"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='euclidean',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-west-2'
        )
    )
    
embeddings = OpenAIEmbeddings()

namespaces = set()

def process_file(file: AskFileResponse):

    loader = PyPDFLoader(file.path)

    docs = loader.load_and_split()
    for i, doc in enumerate(docs):
        doc.metadata["source"] = f"source_{i}"
    return docs

async def get_docsearch(file: AskFileResponse):
    docs = process_file(file)

    # Save data in the user session
    cl.user_session.set("docs", docs)

    # Create a unique namespace for the file
    namespace = file.id

    if namespace in namespaces:
        docsearch = PineconeVectorStore.from_existing_index(
            index_name=index_name, embedding=embeddings, namespace=namespace
        )
    else:
        docsearch = PineconeVectorStore.from_documents(
            docs, embeddings, index_name=index_name, namespace=namespace
        )
        namespaces.add(namespace)

    return docsearch