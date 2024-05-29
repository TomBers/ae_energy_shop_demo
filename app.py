
import os
import json
from openai import AsyncOpenAI

from packages.func_call.funcs import tools, call_tool
from packages.file_uploads.file_uploads import process_file

from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import  ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from langchain_openai import ChatOpenAI

# from chainlit.playground.providers.openai import stringify_function_call
import chainlit as cl

from energyshop import get_tariffs_from_bill

api_key = os.environ.get("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=api_key)



@cl.on_chat_start
async def start_chat():
    message_history = [{"role": "system", "content": "You are a helpful assistant helping people to understand their energy bill."}]
    

    files = None
    while files is None:
        files = await cl.AskFileMessage(
           # content="Upload your energy bill to simplify energy price comparison. The assistant will digest your energy details and help you identify other available tariffs via <a href="https://theenergyshop.com/" target="_blank">The Energy Shop&apos;s</a>price comparison service.",
            #content="""Upload your energy bill to simplify energy price comparison. The assistant will digest your energy details and help you identify other available tariffs via <a href="https://theenergyshop.com/" target="_blank">The Energy Shop's</a> price comparison service.""",
            content="""Upload your energy bill to simplify energy price comparison.  
                    I can help you analyse your bill and identify other affordable tariffs via [The Energy Shop's](https://theenergyshop.com/) price comparison service.
                    """,
            # content="Please upload your energy bill to get started. We can compare your bill to other tariffs",
            accept=["application/pdf"],
            max_size_mb=5,
            timeout=180,
        ).send()

    file = files[0]
    msg = cl.Message(content=f"Processing `{file.name}`", author="System", disable_feedback=True)
    await msg.send()
    
    # Extract text from the PDF and store it in the message history
    context = await process_file(file)
    
    # TODO - TypeError: Expected a Runnable, callable or dict.Instead got an unsupported type: <class 'requests.models.Response'>
    # Convert response to a dict
    
    tariffs = get_tariffs_from_bill(context)

    # print(tariffs)
    # message_history.append({"role": "system", "content": tariffs})
    
    # cl.user_session.set(
    #     "message_history",
    #     message_history,
    # )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert on the energy market, you are advising users on new energy tariffs, which you have access to."),
        ("system", "Answer the question based only on the following tariffs: {context}"),
        ("user", "Question: {question}")
    ])


    model = ChatOpenAI(model="gpt-4-0125-preview")
    output_parser = StrOutputParser()

    # TODO Expected a Runnable, callable or dict.Instead got an unsupported type: <class 'str'>
    # Convert the response to a string and add it to the messages
    setup_and_retrieval = RunnableParallel(
        {"context": {f"context_{i}": json.dumps(tariff) for i, tariff in enumerate(tariffs)},
         "question": RunnablePassthrough()}
    )
    # TODO - FIX above
    
    chain = setup_and_retrieval | prompt | model | output_parser
    cl.user_session.set("chain", chain)

    msg.content = f"`{file.name}` processed. You can now ask questions!"
    await msg.update()





@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="")
    await msg.send()
    
    chain = cl.user_session.get("chain")
    for chunk in chain.stream(message.content):  
        await msg.stream_token(chunk)
    

