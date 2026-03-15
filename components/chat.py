import streamlit as st


def init_chat(role):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}

    if role not in st.session_state.chat_history:
        st.session_state.chat_history[role] = []


def render_chat(role, agent_function, on_response=None):
    """
    role: 当前角色标识
    agent_function: 智能体函数，输入 user_input，输出文本回复
    on_response: 可选回调函数，参数为 (role, user_input, response)
                 用于在收到回复后，同步刷新指标、摘要、图表等状态
    """
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

    user_input = st.chat_input("请输入问题", key=f"chat_input_{role}")

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

        if on_response is not None:
            on_response(role, user_input, response)

        with st.chat_message("assistant"):
            st.markdown(response)

        st.rerun()