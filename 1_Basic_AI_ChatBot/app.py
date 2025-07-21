import streamlit as st
from dataclasses import dataclass
from langchain.schema import HumanMessage
from agent import chat_agent

@dataclass
class Message:
    actor: str
    payload: str

USER = "user"
ASSISTANT = "ai"
MESSAGES = "messages"

# Setting up the UI page title and config 
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 First AI Chatbot")

# ✅ Initialize chat history if not already present
# Initialize chat history
if MESSAGES not in st.session_state:
    st.session_state[MESSAGES] = [Message(actor=ASSISTANT, payload="Hi! How can I help you?")]

msg: Message
for msg in st.session_state[MESSAGES]:
    st.chat_message(msg.actor).write(msg.payload)

# Input box for user message
if prompt := st.chat_input("Type your message..."):
    st.session_state[MESSAGES].append(Message(actor=USER, payload=prompt))
    st.chat_message(USER).write(prompt)
    result = chat_agent.invoke({
        "messages": [HumanMessage(content=prompt)]
    })
    response: str = result["messages"][-1].content
    st.session_state[MESSAGES].append(Message(actor= ASSISTANT, payload= response))
    st.chat_message(ASSISTANT).write(response)
