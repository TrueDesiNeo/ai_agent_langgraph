# Import Streamlit for building the web UI
import streamlit as st

# Import dataclass for structured message handling
from dataclasses import dataclass

# Import HumanMessage schema from LangChain to wrap user input
from langchain.schema import HumanMessage

# Import the compiled LangGraph agent (defined in agent.py)
from agent import chat_agent

# Define a message structure to track who sent what
@dataclass
class Message:
    actor: str  # Either "user" or "ai"
    payload: str  # Text content of the message

# Constants to represent user and assistant actors
USER = "user"
ASSISTANT = "ai"
MESSAGES = "messages"

# Set Streamlit page configuration
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

# Page title
st.title("🤖 First AI Chatbot")

# ✅ Initialize chat history in session state (Streamlit remembers this per session)
# If it's the first visit or reload, start with a welcome message from the assistant
if MESSAGES not in st.session_state:
    st.session_state[MESSAGES] = [
        Message(actor=ASSISTANT, payload="Hi! How can I help you?")
    ]

# Render all messages from the chat history
for msg in st.session_state[MESSAGES]:
    st.chat_message(msg.actor).write(msg.payload)

# Create a simple static config for the agent
# Here, thread_id is hardcoded to '1' for demo purposes
agent_config = {
    "configurable": {
        "thread_id": 1
    }
}

# Input box for user's new message (bottom of the chat)
if prompt := st.chat_input("Type your message..."):
    # Add user message to the chat history
    st.session_state[MESSAGES].append(Message(actor=USER, payload=prompt))
    st.chat_message(USER).write(prompt)

    # Invoke the chat agent with the new user input
    result = chat_agent.invoke({
        "messages": [HumanMessage(content=prompt)]
    }, config=agent_config)

    # Extract assistant's reply from the agent response
    response: str = result["messages"][-1].content

    # Add assistant response to chat history
    st.session_state[MESSAGES].append(Message(actor=ASSISTANT, payload=response))
    st.chat_message(ASSISTANT).write(response)
