import streamlit as st


def init_chat(role):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}

    if role not in st.session_state.chat_history:
        st.session_state.chat_history[role] = []


def render_chat(role, agent_function):

    init_chat(role)

    chat_container = st.container()

    with chat_container:

        for message in st.session_state.chat_history[role]:

            if message["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(message["content"])

            else:
                with st.chat_message("assistant"):
                    st.markdown(message["content"])

    user_input = st.chat_input("请输入问题")

    if user_input:

        st.session_state.chat_history[role].append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        response = agent_function(user_input)

        st.session_state.chat_history[role].append(
            {"role": "assistant", "content": response}
        )

        with st.chat_message("assistant"):
            st.markdown(response)