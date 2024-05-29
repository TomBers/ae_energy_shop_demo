import os

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.openai_tools import PydanticToolsParser

from langchain_core.pydantic_v1 import BaseModel, Field

from energy_shop_interface import get_tariffs
from dotenv import load_dotenv

load_dotenv()

class tariffs(BaseModel):
    """Obtains a list of tariffs available for a given service type"""
    serviceTypeToCompare: str = Field(..., description="Service type to compare")
    paymentMethod: str = Field(..., description="Payment method to compare it should always be MDD")
    mpan: str = Field(..., description="1610027165020")
    gasUsage: int = Field(..., description="Gas usage")
    gasAnnualBill: float = Field(..., description="Gas annual bill")
    elecUsage: int = Field(..., description="Electricity usage")
    elecAnnualBill: float = Field(..., description="Electricity annual bill")
    eSevenUsage: int = Field(..., description="E7 usage")
    
    def all_tariffs(self):
        return get_tariffs(self.dict())




llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
tools = [tariffs]

llm_with_tools = llm.bind_tools(tools)

query = "What are the tariffs available for a service type of electricity, with a payment method MDD, an MPAN of 1610027165020, a gas usage of 1000, a gas annual bill of 1000, an electricity usage of 1000, an electricity annual bill of 1000, and an E7 usage of 1000?"

chain = llm_with_tools | PydanticToolsParser(first_tool_only=True, tools=tools)
res = chain.invoke(query)
# print(res)
print(res.all_tariffs())
    



# print(llm_with_tools.invoke(query).tool_calls)
