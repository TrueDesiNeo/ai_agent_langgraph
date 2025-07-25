# Import the OpenAI chat model wrapper from LangChain
from langchain_openai import ChatOpenAI

# Import utilities to load environment variables from a `.env` file
from dotenv import load_dotenv
from os import getenv

# Import typing tools for state management
from typing import TypedDict, Annotated

# Import LangGraph classes and helpers
from langgraph.graph import StateGraph, END, add_messages

# ✅ Load environment variables (like OPENAI_API_KEY) from a .env file
load_dotenv()

# Set the desired OpenAI model
openai_api_model = "gpt-4-turbo"

# ✅ Initialize the OpenAI language model
llm = ChatOpenAI(model=openai_api_model)

# ✅ Define the structure of the chat state using a TypedDict
# `messages` holds the conversation history
# `add_messages` is a LangGraph helper to track message updates
class BasicChatState(TypedDict):
    messages: Annotated[list, add_messages]

# ✅ Define the core chatbot node function
# It receives the current state, calls the LLM with the message history,
# and returns the updated list of messages (including the assistant's response)
def chatbot(state: BasicChatState):
    return {
        "messages": [llm.invoke(state["messages"])]
    }

# ✅ Create the LangGraph and define nodes and transitions
graph = StateGraph(BasicChatState)

# Add the chatbot function as a graph node
graph.add_node("chatbot", chatbot)

# Define that after the chatbot node finishes, the graph should end
graph.add_edge("chatbot", END)

# Set the chatbot node as the starting point of the graph
graph.set_entry_point("chatbot")

# ✅ Compile the graph into a runnable chat agent
# This produces an executable agent that can be called with input state
chat_agent = graph.compile()  # 🔧 Fixed typo: 'Compile()' → 'compile()'
