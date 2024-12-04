from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from packages.file_uploads.file_uploads import process_file_from_path

from dotenv import load_dotenv

load_dotenv()

def run():
    file_path = "bill.pdf"
    doc_as_string = process_file_from_path(file_path)
    
    prompt = PromptTemplate(
        template="Extract the following parameters: service type, payment method, MPAN, gas usage, gas annual bill, electricity usage, electricity annual bill, E7 usage from {context}",
        input_variables=["context"],
    )
    
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
    chain = prompt | llm 
    print(chain.invoke({"context": doc_as_string}))
    
    
    
    
    
    
run()