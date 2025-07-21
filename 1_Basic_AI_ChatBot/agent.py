from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from os import getenv
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END, add_messages

# Load enviroment variables 
load_dotenv()
openai_api_model = "gpt-4-turbo"

# Initialize OpenAI model  
llm = ChatOpenAI(model= openai_api_model)

class BasicChatState(TypedDict): 
    messages: Annotated[list, add_messages]

def chatbot(state: BasicChatState): 
    return {
       "messages": [llm.invoke(state["messages"])]
    }

# Create LangGraph nodes and edges 
graph = StateGraph(BasicChatState)
graph.add_node("chatbot", chatbot)
graph.add_edge("chatbot", END)

# Set graph entry point
graph.set_entry_point("chatbot")

# Compile the graph
chat_agent = graph.Compile()
