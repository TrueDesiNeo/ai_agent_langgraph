# Import necessary modules and classes
from typing import TypedDict, Annotated  # For defining structured state with type annotations
from langgraph.graph import StateGraph, END, add_messages  # For creating and managing LangGraph state machines
from langgraph.checkpoint.memory import MemorySaver  # For in-memory checkpointing (no disk persistence)
from langchain_openai import ChatOpenAI  # OpenAI LLM wrapper for LangChain
from dotenv import load_dotenv  # To load environment variables from a .env file
from os import getenv  # For accessing environment variables

# Load environment variables from .env file (e.g., OpenAI API key)
load_dotenv()

# Define the model to use; gpt-4-turbo is more efficient and cheaper than regular GPT-4
openai_api_model = "gpt-4-turbo"

# Initialize the OpenAI language model with the specified model name
llm = ChatOpenAI(model=openai_api_model)

# Initialize a memory-based checkpoint system (does not persist data between sessions)
memory = MemorySaver()

# Define the shape of the chat state using TypedDict
# The `messages` key will hold a list of messages, and `add_messages` will help LangGraph track changes
class BasicChatState(TypedDict):
    messages: Annotated[list, add_messages]

# Define the main chatbot function (LangGraph node)
# It takes in the current state and returns the updated messages after LLM invocation
def chatbot(state: BasicChatState):
    return {
        "messages": [llm.invoke(state["messages"])]  # Generate response based on current conversation
    }

# Create a stateful graph using LangGraph to represent the chat flow
graph = StateGraph(BasicChatState)

# Add a single node named "chatbot" that runs the chatbot function
graph.add_node("chatbot", chatbot)

# Define that after "chatbot" node runs, the graph ends (no further transitions)
graph.add_edge("chatbot", END)

# Set the entry point of the graph to the "chatbot" node
graph.set_entry_point("chatbot")

# Compile the graph into a runnable agent, providing the in-memory checkpointing mechanism
chat_agent = graph.compile(checkpointer=memory)
