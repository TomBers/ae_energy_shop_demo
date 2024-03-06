from langchain_community.document_loaders import PyPDFLoader
from chainlit.types import AskFileResponse

async def process_file(file: AskFileResponse):

    loader = PyPDFLoader(file.path)

    docs = loader.load_and_split()
    doc_as_string = " ".join([doc.page_content for doc in docs])
    
    return doc_as_string