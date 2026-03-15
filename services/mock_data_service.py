import pandas as pd
import streamlit as st
from datetime import datetime

def get_investor_metrics():
    return {
        "风险等级": "中等",
        "增长质量": "良好",
        "现金流安全": "稳定",
        "行业位置": "前40%",
    }


def get_enterprise_metrics():
    return {
        "营收健康度": "良好",
        "成本压力": "偏高",
        "现金流状态": "稳定",
        "运营评分": "82",
    }


def get_regulator_metrics():
    return {
        "高风险企业数": "12",
        "异常波动数": "8",
        "披露冲突数": "3",
        "风险传播指数": "中等",
    }


def get_trend_data():
    return pd.DataFrame(
        {
            "月份": ["1月", "2月", "3月", "4月", "5月", "6月"],
            "指标值": [68, 72, 75, 73, 80, 84],
        }
    )


def get_compare_data():
    return pd.DataFrame(
        {
            "类别": ["本企业", "行业均值", "优秀企业"],
            "评分": [82, 74, 91],
        }
    )


def get_summary_text(role: str):
    summary_map = {
        "investor": "当前企业整体经营表现较稳，增长质量较好，但仍需关注局部风险项和外部波动影响。",
        "enterprise": "企业当前运营整体可控，但成本端存在一定压力，建议进一步优化资源配置。",
        "regulator": "当前样本范围内存在部分高风险主体，建议优先关注异常波动较大的企业。",
    }
    return summary_map.get(role, "暂无摘要。")

def get_enterprise_trend_data():
    return pd.DataFrame(
        {
            "月份": ["1月", "2月", "3月", "4月", "5月", "6月"],
            "运营健康度": [78, 80, 79, 81, 83, 82],
        }
    )


def get_enterprise_compare_data():
    return pd.DataFrame(
        {
            "类别": ["本企业", "行业均值", "行业领先"],
            "评分": [82, 76, 90],
        }
    )


def get_regulator_trend_data():
    return pd.DataFrame(
        {
            "月份": ["1月", "2月", "3月", "4月", "5月", "6月"],
            "异常数量": [4, 6, 5, 8, 7, 9],
        }
    )


def get_regulator_compare_data():
    return pd.DataFrame(
        {
            "类别": ["高风险", "中风险", "低风险"],
            "企业数": [12, 20, 35],
        }
    )

def init_analysis_state():
    if "analysis_state" not in st.session_state:
        st.session_state.analysis_state = {
            "investor": {
                "metrics": get_investor_metrics(),
                "summary": get_summary_text("investor"),
                "trend_data": get_trend_data(),
                "compare_data": get_compare_data(),
            },
            "enterprise": {
                "metrics": get_enterprise_metrics(),
                "summary": get_summary_text("enterprise"),
                "trend_data": get_enterprise_trend_data(),
                "compare_data": get_enterprise_compare_data(),
            },
            "regulator": {
                "metrics": get_regulator_metrics(),
                "summary": get_summary_text("regulator"),
                "trend_data": get_regulator_trend_data(),
                "compare_data": get_regulator_compare_data(),
            },
        }


def update_analysis_state(role: str, user_input: str, response: str):
    """
    当前先做前端联动演示：
    根据提问内容，对页面中的指标、摘要做轻量变化。
    后续接入 Coze 后，可以直接用 Coze / 后端返回的结构化数据覆盖这里。
    """
    init_analysis_state()

    text = user_input.lower()

    if role == "investor":
        metrics = get_investor_metrics().copy()
        summary = "当前企业整体经营表现较稳，增长质量较好，但仍需关注局部风险项和外部波动影响。"

        if "风险" in text or "现金流" in text:
            metrics["风险等级"] = "偏高"
            metrics["现金流安全"] = "承压"
            summary = "根据当前提问，系统重点强化了对风险与现金流安全的关注，建议进一步核查偿债能力与资金周转情况。"
        elif "增长" in text or "盈利" in text:
            metrics["增长质量"] = "较强"
            summary = "系统当前更关注增长与盈利表现，显示企业在成长性方面具备一定优势，但仍需结合风险项综合判断。"

        st.session_state.analysis_state["investor"] = {
            "metrics": metrics,
            "summary": summary,
            "trend_data": get_trend_data(),
            "compare_data": get_compare_data(),
        }

    elif role == "enterprise":
        metrics = get_enterprise_metrics().copy()
        summary = "企业当前运营整体可控，但成本端存在一定压力，建议进一步优化资源配置。"

        if "成本" in text or "优化" in text:
            metrics["成本压力"] = "较高"
            metrics["运营评分"] = "78"
            summary = "系统根据当前问题强化了对成本与优化方向的分析，建议优先排查高费用环节和低效率流程。"
        elif "现金流" in text or "库存" in text:
            metrics["现金流状态"] = "波动"
            summary = "当前问题更偏向运营流动性与库存管理，建议关注回款效率和库存周转变化。"

        st.session_state.analysis_state["enterprise"] = {
            "metrics": metrics,
            "summary": summary,
            "trend_data": get_enterprise_trend_data(),
            "compare_data": get_enterprise_compare_data(),
        }

    elif role == "regulator":
        metrics = get_regulator_metrics().copy()
        summary = "当前样本范围内存在部分高风险主体，建议优先关注异常波动较大的企业。"

        if "异常" in text or "高风险" in text:
            metrics["高风险企业数"] = "15"
            metrics["异常波动数"] = "10"
            summary = "系统根据当前问题提高了对异常波动和高风险主体的关注度，建议优先核查异常连续出现的企业。"
        elif "披露" in text or "合规" in text:
            metrics["披露冲突数"] = "5"
            summary = "当前问题更偏向合规与披露一致性，建议进一步检查公告、财报和经营数据之间的匹配程度。"

        st.session_state.analysis_state["regulator"] = {
            "metrics": metrics,
            "summary": summary,
            "trend_data": get_regulator_trend_data(),
            "compare_data": get_regulator_compare_data(),
        }


def get_role_analysis_data(role: str):
    init_analysis_state()
    return st.session_state.analysis_state.get(role, {})

def dataframe_to_text_table(df):
    """
    不依赖 tabulate，把 DataFrame 转成普通文本表格
    """
    if df is None or df.empty:
        return "暂无数据"

    columns = list(df.columns)
    lines = []

    # 表头
    lines.append(" | ".join(str(col) for col in columns))
    lines.append("-|-".join("---" for _ in columns))

    # 数据行
    for _, row in df.iterrows():
        lines.append(" | ".join(str(row[col]) for col in columns))

    return "\n".join(lines)

def build_role_report(role_name: str, analysis_data: dict, chat_history: list):
    """
    生成 markdown 格式报告文本
    后续可替换为 Coze / 后端返回的正式报告内容
    """
    metrics = analysis_data.get("metrics", {})
    summary = analysis_data.get("summary", "暂无摘要")
    trend_data = analysis_data.get("trend_data")
    compare_data = analysis_data.get("compare_data")

    report_lines = []
    report_lines.append(f"# {role_name}分析报告")
    report_lines.append("")
    report_lines.append("## 一、分析摘要")
    report_lines.append(summary)
    report_lines.append("")

    report_lines.append("## 二、核心指标")
    if metrics:
        for k, v in metrics.items():
            report_lines.append(f"- **{k}**：{v}")
    else:
        report_lines.append("- 暂无指标数据")
    report_lines.append("")

    report_lines.append("## 三、图表数据概览")
    if trend_data is not None and not trend_data.empty:
        report_lines.append("### 趋势数据")
        report_lines.append(dataframe_to_text_table(trend_data))
        report_lines.append("")

    if compare_data is not None and not compare_data.empty:
        report_lines.append("### 对比数据")
        report_lines.append(dataframe_to_text_table(compare_data))
        report_lines.append("")

    report_lines.append("## 四、对话记录")
    if chat_history:
        for item in chat_history:
            speaker = "用户" if item["role"] == "user" else "智能体"
            report_lines.append(f"- **{speaker}**：{item['content']}")
    else:
        report_lines.append("- 暂无对话记录")
    report_lines.append("")

    report_lines.append("## 五、说明")
    report_lines.append("本报告为当前前端原型自动生成的结构化分析结果，后续可接入真实 Coze 智能体输出正式报告。")

    return "\n".join(report_lines)


def get_chat_history(role: str):
    if "chat_history" not in st.session_state:
        return []
    return st.session_state.chat_history.get(role, [])

def init_report_state():
    if "report_center" not in st.session_state:
        st.session_state.report_center = []


def save_report_to_center(role: str, report_name: str, report_content: str, report_type: str):
    """
    保存报告到报告中心
    当前使用 session_state，后续可替换为数据库/文件系统
    """
    init_report_state()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report_item = {
        "role": role,
        "name": report_name,
        "type": report_type,
        "content": report_content,
        "timestamp": timestamp,
    }

    st.session_state.report_center.insert(0, report_item)


def get_report_center_items():
    init_report_state()
    return st.session_state.report_center