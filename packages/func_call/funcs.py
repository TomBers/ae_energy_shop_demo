import ast
import sys
import chainlit as cl

# from packages.func_call.weather import get_current_weather, weather_schema
from packages.func_call.energy_shop import get_tariffs, tariffs_schema

tools = [
    tariffs_schema(),
]


@cl.step(type="tool")
async def call_tool(tool_call, message_history):
    function_name = tool_call.function.name
    arguments = ast.literal_eval(tool_call.function.arguments)

    current_step = cl.context.current_step
    current_step.name = function_name

    current_step.input = arguments

    # Call naned function
    func = getattr(sys.modules[__name__], function_name)
    function_response = func(**arguments)

    current_step.output = function_response
    current_step.language = "json"

    message_history.add_message(
        {
            "role": "function",
            "name": function_name,
            "content": function_response,
            "tool_call_id": tool_call.id,
        }
    )
