from pypdf import PdfReader
from chainlit.types import AskFileResponse

async def process_file(file: AskFileResponse):
    return process(file.path)
    
def process(path: str):
    reader = PdfReader(path)
    return " ".join([page.extract_text() for page in reader.pages])