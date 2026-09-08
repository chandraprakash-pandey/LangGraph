import streamlit as st
from LangGraph_DB_Backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid

# *********************** Utility Functions ***********************
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['messages_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_thread']:
        st.session_state['chat_thread'].append(thread_id)

def load_conversation(thread_id):
    return chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']


# *********************** Session Setup ***********************
if 'messages_history' not in st.session_state:
    st.session_state['messages_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_thread' not in st.session_state:
    st.session_state['chat_thread'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])


# *********************** Sidebar UI ***********************
st.sidebar.title("LangGraph ChatBot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("Chat History")

for thread_id in st.session_state['chat_thread'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for message in messages:
            if isinstance(message, HumanMessage):
                temp_messages.append({"role": "user", "content": message.content})
            else:
                temp_messages.append({"role": "assistant", "content": message.content}) 

        st.session_state['messages_history'] = temp_messages

# *********************** Chat UI ***********************
# CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']},
            "metadata": {
                "thread_id": st.session_state['thread_id']
            },
            "run_name": "chat_turn"
          }

for message in st.session_state['messages_history']:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.text(message["content"])
    else:
        with st.chat_message("assistant"):
            st.text(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:

    st.session_state['messages_history'].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    
    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk , metadata in chatbot.stream({"messages": [HumanMessage(content=user_input)]}, config=CONFIG, stream_mode='messages')
        )

    st.session_state['messages_history'].append({"role": "assistant", "content": ai_message })