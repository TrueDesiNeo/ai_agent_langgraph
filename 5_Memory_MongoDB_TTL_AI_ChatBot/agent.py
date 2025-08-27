from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END, add_messages
from dotenv import load_dotenv
from mongo_checkpoint import mongodb_memory
import logging

# -------------------- Setup Logging --------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------- Load Environment Variables --------------------
load_dotenv()
openai_api_model = "gpt-4-turbo"
logger.info("Environment variables loaded. Using OpenAI model: %s", openai_api_model)

# -------------------- Initialize OpenAI Chat Model --------------------
llm = ChatOpenAI(model=openai_api_model)
logger.info("OpenAI Chat model initialized.")

# -------------------- Define Chat State --------------------
class BasicChatState(TypedDict):
    # The state holds a list of messages, which will be passed between nodes
    messages: Annotated[list, add_messages]

# -------------------- Define Chatbot Node --------------------
def chatbot(state: BasicChatState):
    """
    This function represents a node in the LangGraph.
    It takes the current state (messages) and returns the updated state
    after invoking the LLM.
    """
    logger.info("Invoking LLM with current messages.")
    response = llm.invoke(state["messages"])
    logger.info("LLM response received.")
    return {
        "messages": [response]
    }

# -------------------- Build LangGraph --------------------
logger.info("Creating LangGraph...")
graph = StateGraph(BasicChatState)

# Add chatbot node to the graph
graph.add_node("chatbot", chatbot)
logger.info("Node 'chatbot' added to the graph.")

# Define the edge from chatbot to END (terminal node)
graph.add_edge("chatbot", END)
logger.info("Edge from 'chatbot' to END added.")

# Set the entry point of the graph
graph.set_entry_point("chatbot")
logger.info("Entry point set to 'chatbot'.")

# Compile the graph with MongoDB-based checkpointing
chat_agent = graph.compile(checkpointer= mongodb_memory)
logger.info("LangGraph compiled with MongoDB checkpointing.")
