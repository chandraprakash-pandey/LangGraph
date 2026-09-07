import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage


if 'messages_history' not in st.session_state:
    st.session_state['messages_history'] = []

CONFIG = {'configurable': {'thread_id': '1'}}

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