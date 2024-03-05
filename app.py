
import os
from openai import AsyncOpenAI

from operator import itemgetter

from packages.func_call.funcs import tools, call_tool
from packages.rag.rag import get_docsearch

from chainlit.playground.providers.openai import stringify_function_call
import chainlit as cl

from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ChatMessageHistory, ConversationBufferMemory

api_key = os.environ.get("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=api_key)

MAX_ITER = 5


# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API


@cl.on_chat_start
async def start_chat():
    # cl.user_session.set(
    #     "message_history",
    #     [{"role": "system", "content": "You are a helpful assistant helping people to understand their energy bill."}],
    # )

    files = None
    while files is None:
        files = await cl.AskFileMessage(
            content="Please upload your energy bill to get started. We can compare your bill to other tariffs",
            accept=["application/pdf"],
            max_size_mb=5,
            timeout=180,
        ).send()

    file = files[0]
    msg = cl.Message(content=f"Processing `{file.name}`", author="System", disable_feedback=True)
    await msg.send()
    
    docsearch = await get_docsearch(file)
    message_history = ChatMessageHistory()
    # message_history.add_message({"role": "system", "content": "You are a helpful assistant helping people to understand their energy bill."})

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True,
    )
    
    llm = ChatOpenAI(model_name="gpt-4-0125-preview", temperature=0, streaming=True)
    llm_with_tools = llm.bind_tools(tools)
    chain = ConversationalRetrievalChain.from_llm(
        llm_with_tools,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        memory=memory,
        return_source_documents=True,
    )
    # print("Chain created")
    # print(chain)
    
    
    cl.user_session.set("message_history", message_history)
    cl.user_session.set("chain", chain)

    msg.content = f"`{file.name}` processed. You can now ask questions!"
    await msg.update()


@cl.step(type="llm")
async def call_gpt4(message_history):
    chain = cl.user_session.get("chain")
    # cb = cl.AsyncLangchainCallbackHandler()
    

    # response = await chain.acall(message_history, callbacks=[cb])
    print(message_history)
    response = chain.invoke(message_history)
    print(response)

    message = response.choices[0].message

    for tool_call in message.tool_calls or []:
        if tool_call.type == "function":
            await call_tool(tool_call, message_history)

    if message.content:
        cl.context.current_step.generation.completion = message.content
        cl.context.current_step.output = message.content

    elif message.tool_calls:
        completion = stringify_function_call(message.tool_calls[0].function)

        cl.context.current_step.generation.completion = completion
        cl.context.current_step.language = "json"
        cl.context.current_step.output = completion

    return message


@cl.on_message
async def run_conversation(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    msg = ChatPromptTemplate(message.content, role="user")
    message_history.add_user_message(msg)
    print(message_history)

    res = await call_gpt4(message_history)
    print(res)

    await cl.Message(content="Done", author="Answer").send()
    # cur_iter = 0

    # while cur_iter < MAX_ITER:
    #     message = await call_gpt4(message_history)
    #     if not message.tool_calls:
    #         await cl.Message(content=message.content, author="Answer").send()
    #         break

    #     cur_iter += 1
