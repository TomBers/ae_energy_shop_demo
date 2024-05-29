from pypdf import PdfReader
from chainlit.types import AskFileResponse

async def process_file(file: AskFileResponse):

    reader = PdfReader(file.path)
    doc_as_string = " ".join([page.extract_text() for page in reader.pages])
    
    return doc_as_string

def process_file_from_path(file_path: str):

    reader = PdfReader(file_path)
    doc_as_string = " ".join([page.extract_text() for page in reader.pages])
    
    return doc_as_string