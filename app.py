import streamlit as st
from components.layout import (
    init_page_config,
    inject_global_style,
    render_sidebar,
    render_header,
    render_right_panel,
    render_home_page,
    render_orchestrator_page,
    render_investor_page,
    render_enterprise_page,
    render_regulator_page,
    render_reports_page,
    render_about_page,
)

# 1. 页面基础配置
init_page_config()

# 2. 全局样式
inject_global_style()

# 3. 初始化页面状态
if "current_page" not in st.session_state:
    st.session_state.current_page = "首页"

# 4. 左侧导航
render_sidebar()

# 5. 顶部标题
render_header(st.session_state.current_page)

# 6. 主体布局：中间主区域 + 右侧信息栏
main_col, right_col = st.columns([4, 1])

with main_col:
    if st.session_state.current_page == "首页":
        render_home_page()
    elif st.session_state.current_page == "总控智能体":
        render_orchestrator_page()
    elif st.session_state.current_page == "投资者":
        render_investor_page()
    elif st.session_state.current_page == "企业":
        render_enterprise_page()
    elif st.session_state.current_page == "监管者":
        render_regulator_page()
    elif st.session_state.current_page == "报告中心":
        render_reports_page()
    elif st.session_state.current_page == "系统说明":
        render_about_page()

with right_col:
    render_right_panel()