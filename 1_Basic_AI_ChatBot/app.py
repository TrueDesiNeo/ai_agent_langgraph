# Import required libraries
import streamlit as st  # Streamlit is used to build interactive web UIs
from dataclasses import dataclass  # Provides a decorator and functions for creating data classes
from langchain.schema import HumanMessage  # Represents user message input for the LangChain agent
from agent import chat_agent  # Import the pre-compiled LangGraph chat agent from a local module

# Define a simple data structure for storing chat messages
@dataclass
class Message:
    actor: str    # Either "user" or "ai"
    payload: str  # Text content of the message

# Constants for message keys and actors
USER = "user"
ASSISTANT = "ai"
MESSAGES = "messages"

# ✅ Set Streamlit page title and icon
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

# Display page header
st.title("🤖 First AI Chatbot")

# ✅ Initialize chat history in session state if it doesn't exist
# This ensures message history persists across reruns in the same session
if MESSAGES not in st.session_state:
    st.session_state[MESSAGES] = [
        Message(actor=ASSISTANT, payload="Hi! How can I help you?")
    ]

# Render all previous chat messages (both user and assistant) to the UI
for msg in st.session_state[MESSAGES]:
    st.chat_message(msg.actor).write(msg.payload)

# ✅ Input area for the user to type new messages
if prompt := st.chat_input("Type your message..."):
    # Append user's message to the chat history
    st.session_state[MESSAGES].append(Message(actor=USER, payload=prompt))
    st.chat_message(USER).write(prompt)

    # Call the backend chat agent with the user input wrapped in a HumanMessage
    result = chat_agent.invoke({
        "messages": [HumanMessage(content=prompt)]
    })

    # Extract assistant response from result and display it
    response: str = result["messages"][-1].content
    st.session_state[MESSAGES].append(Message(actor=ASSISTANT, payload=response))
    st.chat_message(ASSISTANT).write(response)
