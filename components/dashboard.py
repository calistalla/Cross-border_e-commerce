import streamlit as st


def render_metric_panel(metrics: dict):
    """
    渲染顶部指标卡
    参数示例：
    {
        "风险等级": "中等",
        "增长质量": "良好",
        "现金流安全": "稳定",
        "行业位置": "前40%"
    }
    """
    if not metrics:
        st.info("暂无指标数据")
        return

    cols = st.columns(len(metrics))

    for col, (title, value) in zip(cols, metrics.items()):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">{title}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_analysis_summary(summary_text: str):
    """
    渲染分析摘要区域
    """
    if not summary_text:
        summary_text = "暂无摘要内容。"

    st.markdown(
        f"""
        <div class="summary-box">
            <div class="small-card-title">分析摘要</div>
            <div class="muted-text">{summary_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_line_chart(data, x_col: str, y_col: str):
    """
    渲染折线图
    """
    if data is None or data.empty:
        st.info("暂无折线图数据")
        return

    st.line_chart(data.set_index(x_col)[y_col])


def render_bar_chart(data, x_col: str, y_col: str):
    """
    渲染柱状图
    """
    if data is None or data.empty:
        st.info("暂无柱状图数据")
        return

    st.bar_chart(data.set_index(x_col)[y_col])