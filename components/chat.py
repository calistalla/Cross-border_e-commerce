import streamlit as st


def init_chat(role):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}

    if role not in st.session_state.chat_history:
        st.session_state.chat_history[role] = []


def normalize_agent_result(result):
    """
    兼容两种情况：
    1. 旧版：智能体直接返回字符串
    2. 新版：智能体返回统一协议 dict
    """
    if isinstance(result, dict):
        reply_text = result.get("reply_text", "")
        structured_data = result.get("structured_data", {})
        return reply_text, structured_data

    return str(result), {}


def render_chat(role, agent_function, on_response=None):
    """
    role: 当前角色标识
    agent_function: 智能体函数
    on_response: 回调函数，参数为 (role, user_input, reply_text, structured_data)
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

        result = agent_function(user_input)
        reply_text, structured_data = normalize_agent_result(result)

        st.session_state.chat_history[role].append(
            {"role": "assistant", "content": reply_text}
        )

        if on_response is not None:
            on_response(role, user_input, reply_text, structured_data)

        with st.chat_message("assistant"):
            st.markdown(reply_text)

        st.rerun()