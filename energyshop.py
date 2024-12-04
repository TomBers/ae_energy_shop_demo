import os

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.openai_tools import PydanticToolsParser

from langchain_core.prompts import PromptTemplate

from packages.file_uploads.file_uploads import process_file_from_path

from langchain_core.pydantic_v1 import BaseModel, Field

from energy_shop_interface import get_tariffs
from dotenv import load_dotenv

load_dotenv()

class tariffs(BaseModel):
    """Obtains a list of tariffs available for a given service type"""
    serviceTypeToCompare: str = Field(..., description="Service type to compare")
    paymentMethod: str = Field(..., description="Payment method to compare it should always be MDD")
    mpan: str = Field(..., description="Meter Point Administration Number (MPAN) a unique reference number for your electricity supply point. It is a unique 13-digit reference that identifies each electricity supply point and can be found on your electricity bill.")
    gasUsage: int = Field(..., description="Gas usage")
    gasAnnualBill: float = Field(..., description="Gas annual bill")
    elecUsage: int = Field(..., description="Electricity usage")
    elecAnnualBill: float = Field(..., description="Electricity annual bill")
    eSevenUsage: int = Field(..., description="E7 usage")
    
    def all_tariffs(self):
        return get_tariffs(self.dict())



def get_tariffs_from_bill(context):
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
    tools = [tariffs]

    llm_with_tools = llm.bind_tools(tools)

    file_path = "bill.pdf"
    doc_as_string = process_file_from_path(file_path)

    prompt = PromptTemplate(
        template="Extract the following parameters: service type, payment method, MPAN, gas usage, gas annual bill, electricity usage, electricity annual bill, E7 usage from {context} and use them to get all tariffs available for the service type",
        input_variables=["context"],
    )
    chain = prompt | llm_with_tools | PydanticToolsParser(first_tool_only=True, tools=tools)
    res = chain.invoke({"context": context})

    return res.all_tariffs()
    

def tst_get_tariffs():
    file_path = "bill.pdf"
    context = process_file_from_path(file_path)
    print(get_tariffs_from_bill(context))
 
 
# print(tst_get_tariffs())


# print(llm_with_tools.invoke(query).tool_calls)
