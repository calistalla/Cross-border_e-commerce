import streamlit as st
import pandas as pd
import io


def render_metric_panel(metrics: dict):
    """
    渲染顶部指标卡
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


def normalize_chart_data(data):
    """
    统一图表输入格式：
    - DataFrame -> 原样返回
    - list[dict] -> 转 DataFrame
    - dict -> 转单行 DataFrame
    - 其他 -> 返回 None
    """
    if data is None:
        return None

    if isinstance(data, pd.DataFrame):
        return data

    if isinstance(data, list):
        if len(data) == 0:
            return pd.DataFrame()
        if isinstance(data[0], dict):
            return pd.DataFrame(data)

    if isinstance(data, dict):
        return pd.DataFrame([data])

    return None


def render_line_chart(data, x_col: str, y_col: str):
    """
    渲染折线图
    支持 DataFrame 或 list[dict]
    """
    df = normalize_chart_data(data)

    if df is None or df.empty:
        st.info("暂无折线图数据")
        return

    if x_col not in df.columns or y_col not in df.columns:
        st.warning(f"折线图字段不匹配，缺少列：{x_col} 或 {y_col}")
        st.write(df)
        return

    st.line_chart(df.set_index(x_col)[y_col])


def render_bar_chart(data, x_col: str, y_col: str):
    """
    渲染柱状图
    支持 DataFrame 或 list[dict]
    """
    df = normalize_chart_data(data)

    if df is None or df.empty:
        st.info("暂无柱状图数据")
        return

    if x_col not in df.columns or y_col not in df.columns:
        st.warning(f"柱状图字段不匹配，缺少列：{x_col} 或 {y_col}")
        st.write(df)
        return

    st.bar_chart(df.set_index(x_col)[y_col])


def render_analysis_flow(role: str):
    """
    渲染智能体分析流程区
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

def render_table_block(data, title: str = "结构化表格"):
    """
    渲染结构化表格，支持 DataFrame / list[dict] / dict
    """
    df = normalize_chart_data(data)

    st.markdown(f"##### {title}")

    if df is None or df.empty:
        st.info("暂无表格数据")
        return

    st.dataframe(df, use_container_width=True)


def build_excel_bytes(table_dict: dict):
    """
    将多个表格打包为一个 Excel 文件（二进制）
    table_dict 示例：
    {
        "risk_flags": [...],
        "other_table": [...]
    }
    """
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, table_data in table_dict.items():
            df = normalize_chart_data(table_data)

            if df is None or df.empty:
                continue

            safe_sheet_name = str(sheet_name)[:31]
            df.to_excel(writer, index=False, sheet_name=safe_sheet_name)

    output.seek(0)
    return output.getvalue()