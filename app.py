
import os
from openai import AsyncOpenAI

from packages.func_call.funcs import tools, call_tool
from packages.file_uploads.file_uploads import process_file

from chainlit.playground.providers.openai import stringify_function_call
import chainlit as cl

api_key = os.environ.get("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=api_key)

MAX_ITER = 5



@cl.on_chat_start
async def start_chat():
    message_history = [{"role": "system", "content": "You are a helpful assistant helping people to understand their energy bill."}]
    

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
    
    # Extract text from the PDF and store it in the message history
    content = await process_file(file)
    message_history.append({"role": "system", "content": content})
    
    cl.user_session.set(
        "message_history",
        message_history,
    )

    msg.content = f"`{file.name}` processed. You can now ask questions!"
    await msg.update()


@cl.step(type="llm")
async def call_gpt4(message_history):
    settings = {
        "model": "gpt-4-0125-preview",
        "tools": tools,
        "tool_choice": "auto",
    }

    cl.context.current_step.generation = cl.ChatGeneration(
        provider="openai-chat",
        messages=[
            cl.GenerationMessage(
                formatted=m["content"], name=m.get("name"), role=m["role"]
            )
            for m in message_history
        ],
        settings=settings,
    )

    response = await client.chat.completions.create(
        messages=message_history, **settings
    )

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
    message_history.append({"role": "user", "content": message.content})

    cur_iter = 0

    while cur_iter < MAX_ITER:
        message = await call_gpt4(message_history)
        if not message.tool_calls:
            await cl.Message(content=message.content, author="Answer").send()
            break

        cur_iter += 1
