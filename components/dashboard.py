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

def render_analysis_flow(role: str):
    """
    渲染智能体分析流程区
    后续可替换成真实 Coze 工作流状态
    """
    role_map = {
        "investor": {
            "title": "投资分析流程",
            "steps": ["任务识别", "财务指标分析", "风险判断", "投资结论生成"]
        },
        "enterprise": {
            "title": "经营诊断流程",
            "steps": ["问题识别", "运营指标分析", "优化建议生成", "诊断总结输出"]
        },
        "regulator": {
            "title": "监管分析流程",
            "steps": ["异常识别", "风险筛查", "行业对比分析", "监管结论输出"]
        },
        "orchestrator": {
            "title": "总控任务流程",
            "steps": ["任务解析", "角色匹配", "子智能体分发", "综合结论汇总"]
        },
    }

    flow_info = role_map.get(
        role,
        {
            "title": "分析流程",
            "steps": ["输入任务", "执行分析", "输出结果"]
        }
    )

    st.markdown(f"#### {flow_info['title']}")

    step_cols = st.columns(len(flow_info["steps"]))

    for col, step in zip(step_cols, flow_info["steps"]):
        with col:
            st.markdown(
                f"""
                <div class="flow-step-card">
                    <div class="flow-step-label">{step}</div>
                    <div class="flow-step-status">已准备</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

def render_section_header(title: str, desc: str = ""):
    """
    统一的页面区块标题
    后续可继续升级成更强视觉模块
    """
    st.markdown(
        f"""
        <div class="section-header-box">
            <div class="section-title">{title}</div>
            <div class="section-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )