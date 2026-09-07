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

    response = chatbot.invoke({'messages':[HumanMessage(content=user_input)]}, config=CONFIG)
    ai_message = response['messages'][-1].content
    st.session_state['messages_history'].append({"role": "assistant", "content": ai_message })
    with st.chat_message("assistant"):
        st.text(ai_message)  # Echo the user's input for demonstration purposes