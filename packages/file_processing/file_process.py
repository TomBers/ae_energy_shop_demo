from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=5000, chunk_overlap=200)

# TODO - Test other PDF Loaders to see if they work any better
# https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf


def process_file(path: str):

    loader = PyPDFLoader(path, extract_images=True)

    docs = loader.load_and_split()
    for i, doc in enumerate(docs):
        doc.metadata["source"] = f"source_{i}"
    return docs


print(process_file("test2.pdf"))
