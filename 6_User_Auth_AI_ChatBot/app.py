import streamlit as st
from dataclasses import dataclass
from langchain.schema import HumanMessage
from agent import chat_agent
import uuid
import logging
import hashlib

# -------------------- Setup Logging --------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------- Simulated User Database --------------------
USER_DB = {
    "alice": hashlib.sha256("password123".encode()).hexdigest(),
    "bob": hashlib.sha256("securepass".encode()).hexdigest(),
}

# -------------------- Authentication Function --------------------
def login():
    st.title("Login to AI Chatbot")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        if username in USER_DB and USER_DB[username] == hashed_pw:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid credentials")

# -------------------- Message Data Structure --------------------
@dataclass
class Message:
    actor: str
    payload: str

# Constants for message roles
USER = "user"
ASSISTANT = "ai"
MESSAGES = "messages"

# -------------------- Streamlit UI Setup --------------------
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot with User Authentication")

# -------------------- Logoff Button --------------------
if "authenticated" in st.session_state and st.session_state["authenticated"]:
    if st.sidebar.button("Logoff"):
        st.session_state.clear()
        st.rerun()

# -------------------- Authentication Gate --------------------
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    login()
    st.stop()

# -------------------- Session Initialization --------------------
# Check if 'agent_config' exists in session state; if not, create a new session with a unique thread ID
if "agent_config" not in st.session_state:
    st.session_state["agent_config"] = {
        "configurable": {
            "thread_id": st.session_state["username"] + ":" + str(uuid.uuid4())
        }
    }
    logger.info("New session initialized with thread_id: %s", st.session_state["agent_config"]["configurable"]["thread_id"])
else:
    logger.info("Existing session loaded with thread_id: %s", st.session_state["agent_config"]["configurable"]["thread_id"])

# -------------------- Initialize Chat History --------------------
if MESSAGES not in st.session_state:
    st.session_state[MESSAGES] = [Message(actor=ASSISTANT, payload="Hi! How can I help you?")]
    logger.info("Chat history initialized with welcome message.")

# -------------------- Display Chat History --------------------
for msg in st.session_state[MESSAGES]:
    st.chat_message(msg.actor).write(msg.payload)

# -------------------- Handle User Input --------------------
if prompt := st.chat_input("Type your message..."):
    logger.info("User input received: %s", prompt)

    # Append user message to chat history
    st.session_state[MESSAGES].append(Message(actor=USER, payload=prompt))
    st.chat_message(USER).write(prompt)

    # Invoke the LangGraph agent with the user message
    result = chat_agent.invoke({
        "messages": [HumanMessage(content=prompt)]
    }, config=st.session_state["agent_config"])

    # Extract and display the assistant's response
    response: str = result["messages"][-1].content
    logger.info("Assistant response: %s", response)

    st.session_state[MESSAGES].append(Message(actor=ASSISTANT, payload=response))
    st.chat_message(ASSISTANT).write(response)
    