import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool

# 1. Load API key from .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError(
        "Missing GROQ_API_KEY. Copy .env.example to .env and add your Groq API key."
    )


# 2. Create LLM instance
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    groq_api_key=api_key,
)

# 3. Calculator tool
@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        return str(eval(expression))
    except:
        return "Error: Invalid expression."
    
# 4. Weather tool
@tool
def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    weather = {
        "new york": "Sunny, 25°C",
        "london": "Cloudy, 15°C",
        "tokyo": "Rainy, 20°C"
    }
    normalized_city = city.strip().lower()
    return weather.get(normalized_city, "Weather information not available for this city.")

# 5. Word count tool
@tool
def word_count(text: str) -> str:
    """Count the number of words in a given text."""
    return str(len(text.split()))

# 6. Put all tools together
tools = [calculator, get_weather, word_count]

# 7. Give tools to LLM
llm_with_tools = llm.bind_tools(tools)

# 8. Get user questions
question = input("\nAsk a question: ")

# 9. Store conversations
messages = [
    {"role": "user", "content": question}
]

# Agent Loop
while True:
    # Get user input
    response = llm_with_tools.invoke(messages)
    messages.append(response)
    # No tool usage, just print the response
    if not response.tool_calls:
        print("\n Final Answer:")
        print(response.content)
        break
    # If there are tool calls, print the tool usage and continue the loop
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        print(f"\nTool Used: {tool_name}")
        print(f"Arguments: {tool_args}")

        # Find the corresponding tool and execute it
        for current_tool in tools:
            if current_tool.name == tool_name:
                result = current_tool.invoke(tool_args)
                print("Result:", result)

                #send the result back to the LLM for further processing
                messages.append({"role": "tool", "name": tool_name, "content": str(result), "tool_call_id": tool_call["id"]})