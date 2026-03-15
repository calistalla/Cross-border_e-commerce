import streamlit as st
from components.chat import render_chat
from services.agent_service import (
    investor_agent,
    enterprise_agent,
    regulator_agent,
    orchestrator_agent,
    detect_role_by_query,
)
from components.dashboard import (
    render_metric_panel,
    render_analysis_summary,
    render_line_chart,
    render_bar_chart,
    render_analysis_flow,
    render_section_header,
)

from services.mock_data_service import (
    get_investor_metrics,
    get_enterprise_metrics,
    get_regulator_metrics,
    get_trend_data,
    get_compare_data,
    get_summary_text,
    get_enterprise_trend_data,
    get_enterprise_compare_data,
    get_regulator_trend_data,
    get_regulator_compare_data,
    init_analysis_state,
    update_analysis_state,
    get_role_analysis_data,
    build_role_report,
    get_chat_history,
    save_report_to_center,
    get_report_center_items,
)


def init_page_config():
    st.set_page_config(
        page_title="企业运营分析与决策支持平台",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def inject_global_style():
    st.markdown(
        """
        <style>
        :root {
            --bg-main: #f3f6fb;
            --bg-card: rgba(255, 255, 255, 0.88);
            --bg-soft: #f8fbff;
            --bg-hero-start: #eef4ff;
            --bg-hero-end: #f7f9ff;

            --border-light: rgba(226, 232, 240, 0.9);
            --border-soft: rgba(219, 226, 239, 0.95);
            --border-accent: rgba(209, 220, 255, 0.95);
            --border-dashed: #cfd8ea;
            
            --divider: rgba(255,255,255,0.7);

            --text-main: #0f172a;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --text-light: #7c8aa5;

            --primary: #5b5bf6;
            --primary-dark: #4747d9;
            --primary-soft: #eef2ff;
            --primary-glow: rgba(91, 91, 246, 0.12);

            --success-soft: #ecfdf3;
            --success-text: #166534;

            --radius-sm: 14px;
            --radius-md: 18px;
            --radius-lg: 22px;
            --radius-xl: 26px;

            --shadow-soft: 0 4px 16px rgba(15, 23, 42, 0.04);
            --shadow-card: 0 10px 30px rgba(15, 23, 42, 0.06);
            --shadow-hover: 0 12px 36px rgba(91, 91, 246, 0.10);
        }

        html, body, [class*="css"] {
            font-feature-settings: "liga" 1, "kern" 1;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(91, 91, 246, 0.05), transparent 28%),
                radial-gradient(circle at top right, rgba(99, 102, 241, 0.05), transparent 22%),
                var(--bg-main);
        }

        .main > div {
            padding-top: 2.2rem;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 1.4rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 1500px;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8faff 0%, #f3f7ff 100%);
            border-right: 1px solid rgba(219, 226, 239, 0.85);
        }

        .page-title {
            font-size: 2.15rem;
            font-weight: 800;
            margin-top: 0.15rem;
            margin-bottom: 0.35rem;
            color: var(--text-main);
            letter-spacing: -0.03em;
        }

        .page-desc {
            color: var(--text-muted);
            font-size: 0.98rem;
            margin-bottom: 1.25rem;
            line-height: 1.7;
        }

        .hero-box {
            padding: 34px;
            border-radius: var(--radius-xl);
            background: linear-gradient(135deg, var(--bg-hero-start) 0%, var(--bg-hero-end) 100%);
            border: 1px solid var(--border-accent);
            margin-bottom: 24px;
            box-shadow: var(--shadow-card);
            position: relative;
            overflow: hidden;
        }

        .hero-box::after {
            content: "";
            position: absolute;
            right: -50px;
            top: -50px;
            width: 180px;
            height: 180px;
            background: radial-gradient(circle, rgba(91, 91, 246, 0.12) 0%, rgba(91, 91, 246, 0.00) 70%);
            pointer-events: none;
        }

        .hero-title {
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 0.75rem;
            color: var(--text-main);
            letter-spacing: -0.03em;
            line-height: 1.2;
        }

        .hero-desc {
            font-size: 1rem;
            color: var(--text-secondary);
            line-height: 1.9;
            max-width: 900px;
        }

        .card {
            border: 1px solid var(--border-light);
            border-radius: var(--radius-md);
            padding: 18px 20px;
            background: var(--bg-card);
            box-shadow: var(--shadow-soft);
            margin-bottom: 16px;
            backdrop-filter: blur(8px);
        }

        .feature-card {
            border: 1px solid var(--border-soft);
            border-radius: var(--radius-lg);
            padding: 22px;
            background: rgba(255, 255, 255, 0.92);
            box-shadow: var(--shadow-card);
            margin-bottom: 10px;
            min-height: 165px;
            transition: all 0.22s ease;
            backdrop-filter: blur(10px);
        }

        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
            border-color: rgba(91, 91, 246, 0.18);
        }

        .role-card {
            position: relative;
            border: 1px solid rgba(219, 226, 239, 0.95);
            border-radius: 24px;
            padding: 24px 22px 20px 22px;
            background: linear-gradient(180deg, rgba(255,255,255,0.96) 0%, rgba(248,251,255,0.98) 100%);
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
            min-height: 220px;
            overflow: hidden;
            transition: all 0.22s ease;
            margin-bottom: 12px;
        }

        .role-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 16px 36px rgba(91, 91, 246, 0.12);
            border-color: rgba(91, 91, 246, 0.16);
        }

        .role-card::after {
            content: "";
            position: absolute;
            right: -35px;
            top: -35px;
            width: 110px;
            height: 110px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(91,91,246,0.12) 0%, rgba(91,91,246,0.00) 70%);
            pointer-events: none;
        }

        .role-icon {
            width: 48px;
            height: 48px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            background: var(--primary-soft);
            color: var(--primary);
            margin-bottom: 16px;
            font-weight: 700;
        }

        .role-title {
            font-size: 1.15rem;
            font-weight: 800;
            color: var(--text-main);
            margin-bottom: 8px;
            letter-spacing: -0.02em;
        }

        .role-subtitle {
            font-size: 0.92rem;
            color: var(--text-muted);
            margin-bottom: 12px;
            line-height: 1.65;
            min-height: 46px;
        }

        .role-tag-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
            margin-bottom: 4px;
        }

        .role-tag {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 999px;
            background: rgba(91, 91, 246, 0.08);
            color: var(--primary);
            font-size: 0.78rem;
            font-weight: 700;
        }

        .orchestrator-hero {
            position: relative;
            border: 1px solid rgba(209, 220, 255, 0.95);
            border-radius: 26px;
            padding: 28px 26px;
            background: linear-gradient(135deg, #eef4ff 0%, #f7f9ff 100%);
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
            margin-bottom: 18px;
            overflow: hidden;
        }

        .orchestrator-hero::after {
            content: "";
            position: absolute;
            right: -45px;
            top: -35px;
            width: 160px;
            height: 160px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(91, 91, 246, 0.14) 0%, rgba(91, 91, 246, 0.00) 70%);
            pointer-events: none;
        }

        .orchestrator-title {
            font-size: 1.7rem;
            font-weight: 800;
            color: var(--text-main);
            letter-spacing: -0.03em;
            margin-bottom: 10px;
        }

        .orchestrator-desc {
            font-size: 0.96rem;
            color: var(--text-secondary);
            line-height: 1.8;
            max-width: 860px;
        }

        .recommend-card {
            border: 1px solid rgba(219, 226, 239, 0.95);
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.94);
            box-shadow: var(--shadow-soft);
            padding: 20px;
            min-height: 150px;
            margin-bottom: 12px;
        }

        .recommend-label {
            font-size: 0.88rem;
            color: var(--text-muted);
            margin-bottom: 8px;
            font-weight: 600;
        }

        .recommend-value {
            font-size: 1.35rem;
            font-weight: 800;
            color: var(--text-main);
            letter-spacing: -0.02em;
            margin-bottom: 8px;
        }

        .recommend-note {
            font-size: 0.92rem;
            color: var(--text-secondary);
            line-height: 1.7;
        }

        .path-preview-box {
            border: 1px dashed rgba(185, 196, 220, 0.95);
            border-radius: 20px;
            background: rgba(251, 253, 255, 0.92);
            padding: 18px;
            margin-bottom: 10px;
        }

        .path-preview-title {
            font-size: 1rem;
            font-weight: 800;
            color: var(--text-main);
            margin-bottom: 10px;
        }

        .path-pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .path-pill {
            display: inline-block;
            padding: 8px 14px;
            border-radius: 999px;
            background: var(--primary-soft);
            color: var(--primary);
            font-size: 0.84rem;
            font-weight: 700;
        }

        .page-topbar {
            border: 1px solid rgba(209, 220, 255, 0.95);
            border-radius: 24px;
            background: linear-gradient(135deg, rgba(238,244,255,0.95) 0%, rgba(247,249,255,0.98) 100%);
            box-shadow: 0 10px 26px rgba(15, 23, 42, 0.05);
            padding: 22px 24px;
            margin-bottom: 18px;
            position: relative;
            overflow: hidden;
        }

        .page-topbar::after {
            content: "";
            position: absolute;
            right: -30px;
            top: -30px;
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(91,91,246,0.12) 0%, rgba(91,91,246,0.00) 70%);
            pointer-events: none;
        }

        .page-topbar-title {
            font-size: 1.35rem;
            font-weight: 800;
            color: var(--text-main);
            letter-spacing: -0.02em;
            margin-bottom: 8px;
        }

        .page-topbar-desc {
            font-size: 0.94rem;
            color: var(--text-secondary);
            line-height: 1.75;
            margin-bottom: 14px;
            max-width: 900px;
        }

        .page-topbar-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .page-topbar-tag {
            display: inline-block;
            padding: 7px 12px;
            border-radius: 999px;
            background: rgba(91, 91, 246, 0.08);
            color: var(--primary);
            font-size: 0.8rem;
            font-weight: 700;
        }

        .home-section-title {
            font-size: 1.28rem;
            font-weight: 800;
            color: var(--text-main);
            margin-top: 10px;
            margin-bottom: 14px;
            letter-spacing: -0.02em;
        }

        .home-highlight-box {
            border: 1px solid var(--border-soft);
            border-radius: 22px;
            background: rgba(255,255,255,0.92);
            box-shadow: var(--shadow-soft);
            padding: 20px;
            margin-top: 6px;
            margin-bottom: 18px;
        }

        .info-card {
            border: 1px solid var(--border-soft);
            border-radius: var(--radius-md);
            padding: 18px;
            background: linear-gradient(180deg, #fbfdff 0%, #f8fbff 100%);
            min-height: 132px;
            margin-bottom: 12px;
            box-shadow: var(--shadow-soft);
        }

        .small-card-title {
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 8px;
            color: var(--text-main);
            letter-spacing: -0.01em;
        }

        .feature-title {
            font-size: 1.12rem;
            font-weight: 700;
            margin-bottom: 10px;
            color: var(--text-main);
            letter-spacing: -0.01em;
        }

        .feature-desc {
            font-size: 0.95rem;
            color: var(--text-secondary);
            line-height: 1.75;
        }

        .muted-text {
            color: var(--text-muted);
            font-size: 0.92rem;
            line-height: 1.75;
        }

        .flow-box {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            border: 1px solid var(--border-accent);
            border-radius: var(--radius-lg);
            padding: 22px;
            background: linear-gradient(135deg, rgba(255,255,255,0.96) 0%, rgba(248,251,255,0.98) 100%);
            margin-bottom: 12px;
            flex-wrap: wrap;
            box-shadow: var(--shadow-soft);
        }

        .flow-step {
            flex: 1;
            min-width: 180px;
            text-align: center;
            font-weight: 700;
            color: var(--text-main);
            background: var(--primary-soft);
            border-radius: var(--radius-sm);
            padding: 16px 12px;
            border: 1px solid rgba(91, 91, 246, 0.08);
        }

        .flow-arrow {
            font-size: 1.4rem;
            font-weight: 700;
            color: #7c8aa5;
        }

        .metric-card {
            border: 1px solid var(--border-soft);
            border-radius: var(--radius-sm);
            padding: 18px 16px;
            background: rgba(255, 255, 255, 0.95);
            text-align: center;
            box-shadow: var(--shadow-soft);
            backdrop-filter: blur(8px);
        }

        .metric-title {
            font-size: 0.86rem;
            color: var(--text-muted);
            letter-spacing: 0.01em;
        }

        .metric-value {
            font-size: 1.34rem;
            font-weight: 800;
            margin-top: 8px;
            color: var(--text-main);
            letter-spacing: -0.02em;
        }

        .summary-box {
            border-top: 3px solid var(--divider);
            border-radius: 0px;
            padding: 14px 0 4px 0;
            background: transparent;
            margin: 18px 0 8px 0;
            box-shadow: none;
        }
        
        .section-header-box {
            border-top: 3px solid var(--divider);
            padding: 12px 0 6px 0;
            margin-top: 18px;
            margin-bottom: 12px;
        }

        .section-title {
            font-size: 1.08rem;
            font-weight: 800;
            color: var(--text-main);
            letter-spacing: -0.02em;
            margin-bottom: 4px;
        }

        .section-desc {
            font-size: 0.9rem;
            color: var(--text-muted);
            line-height: 1.6;
        }

        .module-box {
            border: 1px solid var(--border-soft);
            border-radius: var(--radius-lg);
            background: rgba(255, 255, 255, 0.9);
            box-shadow: var(--shadow-soft);
            padding: 18px;
            margin-bottom: 18px;
            backdrop-filter: blur(10px);
        }

        .chart-box {
            border: 1px dashed var(--border-dashed);
            border-radius: var(--radius-sm);
            padding: 42px;
            text-align: center;
            color: var(--text-light);
            margin-bottom: 16px;
            background: rgba(252, 253, 255, 0.92);
        }

        .flow-step-card {
            border: 1px solid var(--border-soft);
            border-radius: var(--radius-md);
            padding: 16px 12px;
            background: rgba(255, 255, 255, 0.95);
            text-align: center;
            box-shadow: var(--shadow-soft);
            min-height: 92px;
        }

        .flow-step-label {
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 8px;
        }

        .flow-step-status {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 999px;
            background: var(--primary-soft);
            color: var(--primary);
            font-size: 0.82rem;
            font-weight: 700;
        }

        div[data-baseweb="select"] {
            margin-bottom: 2px;
        }

        div[data-baseweb="select"] > div,
        div[data-baseweb="base-input"] > div,
        textarea {
            border-radius: 14px !important;
            border-color: rgba(203, 213, 225, 0.8) !important;
            background: rgba(255, 255, 255, 0.96) !important;
        }

        div[data-testid="stChatMessage"] {
            border-radius: 16px;
            margin-bottom: 0.35rem;
        }

        div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stChatMessage"]) {
            gap: 0.45rem;
        }

        canvas {
            border-radius: 14px;
        }

        div[data-testid="stAlert"] {
            border-radius: 14px;
        }

        h3, h4, h5 {
            letter-spacing: -0.02em;
            color: var(--text-main);
        }
        
        div.stButton > button {
            border-radius: 14px;
            font-weight: 700;
            border: 1px solid rgba(91, 91, 246, 0.10);
            padding-top: 0.62rem;
            padding-bottom: 0.62rem;
            background: linear-gradient(180deg, #ffffff 0%, #f8faff 100%);
            color: var(--text-main);
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
            transition: all 0.18s ease;
        }

        div.stButton > button:hover {
            border-color: rgba(91, 91, 246, 0.28);
            box-shadow: 0 8px 20px rgba(91, 91, 246, 0.10);
            color: var(--primary-dark);
        }

        div[data-testid="stDownloadButton"] > button {
            border-radius: 14px;
            font-weight: 700;
            padding-top: 0.62rem;
            padding-bottom: 0.62rem;
            background: linear-gradient(135deg, var(--primary) 0%, #6f6ff8 100%);
            color: white;
            border: none;
            box-shadow: 0 10px 22px rgba(91, 91, 246, 0.22);
            transition: all 0.18s ease;
        }

        div[data-testid="stDownloadButton"] > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 14px 28px rgba(91, 91, 246, 0.24);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    st.sidebar.title("导航面板")

    page = st.sidebar.radio(
        "请选择页面",
        ["首页", "总控智能体", "投资者", "企业", "监管者", "报告中心", "系统说明"],
        index=["首页", "总控智能体", "投资者", "企业", "监管者", "报告中心", "系统说明"].index(
            st.session_state.current_page
        ),
    )

    st.session_state.current_page = page

    st.sidebar.markdown("---")
    st.sidebar.caption("多角色智能体前端原型")
    st.sidebar.write("当前角色：", st.session_state.current_page)


def render_header(page_name: str):
    page_desc_map = {
        "首页": "系统总览与角色入口",
        "总控智能体": "任务分发、角色推荐与统一调度入口",
        "投资者": "面向投资分析、风险识别与价值判断",
        "企业": "面向运营诊断、经营优化与策略建议",
        "监管者": "面向异常识别、行业监测与风险传播分析",
        "报告中心": "统一管理各角色生成的分析结果与报告",
        "系统说明": "项目背景、系统架构与数据说明",
    }

    st.markdown(f'<div class="page-title">{page_name}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="page-desc">{page_desc_map.get(page_name, "")}</div>',
        unsafe_allow_html=True,
    )

def render_role_topbar(role: str):
    config = {
        "investor": {
            "title": "投资者视角 · 企业价值与风险判断",
            "desc": "适用于企业关注价值判断、增长质量、风险识别与同业对比等分析场景，可输出投研简报与结构化投资结论。",
            "tags": ["价值判断", "风险识别", "同业对比", "投研简报"],
        },
        "enterprise": {
            "title": "企业视角 · 经营诊断与优化建议",
            "desc": "适用于经营压力识别、成本结构观察、运营效率分析与优化建议生成等场景，可输出经营诊断报告与改进建议。",
            "tags": ["经营诊断", "运营优化", "指标监测", "诊断报告"],
        },
        "regulator": {
            "title": "监管视角 · 异常监测与风险观察",
            "desc": "适用于高风险企业筛查、异常波动监测、行业风险分层和系统性风险观察等场景，可输出监管分析报告与异常清单。",
            "tags": ["异常监测", "风险分层", "行业观察", "监管报告"],
        },
    }

    info = config.get(role)
    if not info:
        return

    tags_html = "".join(
        [f'<span class="page-topbar-tag">{tag}</span>' for tag in info["tags"]]
    )

    st.markdown(
        f"""
        <div class="page-topbar">
            <div class="page-topbar-title">{info["title"]}</div>
            <div class="page-topbar-desc">{info["desc"]}</div>
            <div class="page-topbar-tags">{tags_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_right_panel():
    current_page = st.session_state.get("current_page", "首页")

    panel_map = {
        "首页": {
            "title": "首页信息",
            "cards": [
                {
                    "title": "系统定位",
                    "content": "这是一个面向投资者、企业管理者与监管机构的多角色智能体分析平台。"
                },
                {
                    "title": "推荐浏览顺序",
                    "content": "建议先查看首页，再体验总控智能体，最后进入三个角色工作台查看差异化功能。"
                },
                {
                    "title": "当前进度",
                    "content": "当前已完成基础框架、首页升级、角色工作台、聊天区、指标卡和图表区。"
                },
            ]
        },
        "总控智能体": {
            "title": "总控信息栏",
            "cards": [
                {
                    "title": "页面作用",
                    "content": "总控智能体负责识别用户任务、推荐角色入口，并为后续多角色联动提供统一入口。"
                },
                {
                    "title": "推荐任务写法",
                    "content": "可以直接输入完整问题，例如“分析某企业是否存在现金流风险，并说明更适合从哪个角色视角查看”。"
                },
                {
                    "title": "后续扩展",
                    "content": "未来可在这里接入 Coze 顶层工作流，实现统一意图识别与子智能体调度。"
                },
            ]
        },
        "投资者": {
            "title": "投资者信息栏",
            "cards": [
                {
                    "title": "角色目标",
                    "content": "帮助用户进行企业价值判断、风险识别、增长质量分析与投资关注点提炼。"
                },
                {
                    "title": "推荐提问",
                    "content": "例如：这家公司是否值得持续关注？当前最大的经营风险是什么？"
                },
                {
                    "title": "可生成内容",
                    "content": "后续可输出投研简报、风险提示、同业对比分析与情景推演结论。"
                },
            ]
        },
        "企业": {
            "title": "企业信息栏",
            "cards": [
                {
                    "title": "角色目标",
                    "content": "帮助企业识别经营压力、监测核心指标变化，并生成优化建议。"
                },
                {
                    "title": "推荐提问",
                    "content": "例如：当前成本压力主要来自哪里？哪些运营环节最值得优先优化？"
                },
                {
                    "title": "可生成内容",
                    "content": "后续可输出经营诊断报告、指标异常说明、优化建议和阶段性总结。"
                },
            ]
        },
        "监管者": {
            "title": "监管者信息栏",
            "cards": [
                {
                    "title": "角色目标",
                    "content": "帮助识别异常企业、监测行业风险变化，并观察潜在系统性风险传播。"
                },
                {
                    "title": "推荐提问",
                    "content": "例如：当前行业中哪些企业风险较高？异常波动主要集中在哪些主体？"
                },
                {
                    "title": "可生成内容",
                    "content": "后续可输出异常企业清单、监管分析报告、风险分层结果与证据链摘要。"
                },
            ]
        },
        "报告中心": {
            "title": "报告中心信息栏",
            "cards": [
                {
                    "title": "页面作用",
                    "content": "统一管理投资者、企业、监管者三个角色生成的分析报告与结论文件。"
                },
                {
                    "title": "后续功能",
                    "content": "未来可支持预览、下载、按角色筛选，以及按企业或时间进行检索。"
                },
                {
                    "title": "当前状态",
                    "content": "目前为占位页面，后续在接入真实分析结果后逐步完善。"
                },
            ]
        },
        "系统说明": {
            "title": "系统说明信息栏",
            "cards": [
                {
                    "title": "建议内容",
                    "content": "这里后续可以展示项目背景、系统架构图、数据来源说明、技术路线与比赛介绍。"
                },
                {
                    "title": "展示价值",
                    "content": "系统说明页适合在比赛答辩或演示时向评委快速解释整体方案。"
                },
                {
                    "title": "当前状态",
                    "content": "目前先保留页面结构，后续等主要功能完成后再统一补内容。"
                },
            ]
        },
    }

    current_panel = panel_map.get(current_page, panel_map["首页"])

    st.markdown(f"### {current_panel['title']}")

    for card in current_panel["cards"]:
        st.markdown(
            f"""
            <div class="card">
                <div class="small-card-title">{card["title"]}</div>
                <div class="muted-text">{card["content"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_home_page():
    st.markdown(
        """
        <div class="hero-box">
            <div class="hero-title">企业运营分析与决策支持多智能体平台</div>
            <div class="hero-desc">
                面向投资者、企业管理者与监管机构，提供智能问答、数据分析、风险洞察与报告生成能力。
                系统通过多角色智能体协同与总控任务分发，实现更清晰的经营分析、更灵活的视角切换与更高质量的辅助决策支持。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="home-section-title">核心角色入口</div>', unsafe_allow_html=True)

    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    with row1_col1:
        st.markdown(
            """
            <div class="role-card">
                <div class="role-icon">📈</div>
                <div class="role-title">投资者工作台</div>
                <div class="role-subtitle">
                    面向企业价值判断、增长质量评估、风险识别与投资关注点提炼，
                    帮助用户快速形成投研视角下的分析结论。
                </div>
                <div class="role-tag-row">
                    <span class="role-tag">风险识别</span>
                    <span class="role-tag">价值判断</span>
                    <span class="role-tag">同业对比</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("进入投资者工作台", key="home_card_investor", use_container_width=True):
            st.session_state.current_page = "投资者"
            st.rerun()

    with row1_col2:
        st.markdown(
            """
            <div class="role-card">
                <div class="role-icon">🏢</div>
                <div class="role-title">企业工作台</div>
                <div class="role-subtitle">
                    面向经营诊断、指标监测、运营优化与资源配置建议，
                    帮助企业识别压力来源并形成可执行的改进方向。
                </div>
                <div class="role-tag-row">
                    <span class="role-tag">经营诊断</span>
                    <span class="role-tag">运营优化</span>
                    <span class="role-tag">指标监测</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("进入企业工作台", key="home_card_enterprise", use_container_width=True):
            st.session_state.current_page = "企业"
            st.rerun()

    with row2_col1:
        st.markdown(
            """
            <div class="role-card">
                <div class="role-icon">🛡</div>
                <div class="role-title">监管者工作台</div>
                <div class="role-subtitle">
                    面向异常识别、行业监测、风险分层与系统性风险观察，
                    支持高风险主体筛查与监管视角下的动态分析。
                </div>
                <div class="role-tag-row">
                    <span class="role-tag">异常监测</span>
                    <span class="role-tag">风险分层</span>
                    <span class="role-tag">行业观察</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("进入监管者工作台", key="home_card_regulator", use_container_width=True):
            st.session_state.current_page = "监管者"
            st.rerun()

    with row2_col2:
        st.markdown(
            """
            <div class="role-card">
                <div class="role-icon">🧠</div>
                <div class="role-title">总控智能体</div>
                <div class="role-subtitle">
                    作为统一入口，负责识别用户任务、推荐合适的角色工作台，
                    并为后续多角色协同分析与综合报告生成提供总控能力。
                </div>
                <div class="role-tag-row">
                    <span class="role-tag">任务分发</span>
                    <span class="role-tag">角色推荐</span>
                    <span class="role-tag">协同分析</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("进入总控智能体", key="home_card_orchestrator", use_container_width=True):
            st.session_state.current_page = "总控智能体"
            st.rerun()

    st.markdown('<div class="home-section-title">系统亮点</div>', unsafe_allow_html=True)

    h1, h2, h3 = st.columns(3)

    with h1:
        st.markdown(
            """
            <div class="info-card">
                <div class="small-card-title">多角色智能体协同</div>
                <div class="muted-text">
                    针对投资者、企业与监管者三类对象提供差异化分析路径，
                    同时保留总控智能体作为统一调度入口。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with h2:
        st.markdown(
            """
            <div class="info-card">
                <div class="small-card-title">对话与分析联动</div>
                <div class="muted-text">
                    用户输入问题后，聊天结果会同步联动指标卡、分析摘要、图表与报告输出，
                    更接近真实的智能分析工作流。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with h3:
        st.markdown(
            """
            <div class="info-card">
                <div class="small-card-title">可扩展至真实 Coze</div>
                <div class="muted-text">
                    当前已按服务层与页面层分离方式实现，后续可无缝替换为真实 Coze 智能体、
                    工作流接口与结构化数据返回。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="home-section-title">体验路径</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="flow-box">
            <div class="flow-step">Step 1　选择角色或输入任务</div>
            <div class="flow-arrow">→</div>
            <div class="flow-step">Step 2　智能体完成分析与联动展示</div>
            <div class="flow-arrow">→</div>
            <div class="flow-step">Step 3　输出报告并进入报告中心管理</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="home-highlight-box">
            <div class="small-card-title">当前原型完成度</div>
            <div class="muted-text">
                已完成：首页升级、三角色工作台、总控分发页、聊天联动、图表展示、报告生成与报告中心。
                后续可继续升级 UI 细节，并接入真实 Coze 智能体与工作流。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_orchestrator_page():
    st.markdown(
        """
        <div class="orchestrator-hero">
            <div class="orchestrator-title">总控智能体 · AI 调度中枢</div>
            <div class="orchestrator-desc">
                总控智能体负责识别用户任务、匹配合适角色、组织后续协同分析路径，
                是系统中连接投资者、企业与监管者三个工作台的统一入口, 也是任务编排与多智能体协同调度中心。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("任务输入", "输入你的分析目标，系统将识别任务类型并推荐最合适的角色路径。")

    if "orchestrator_query" not in st.session_state:
        st.session_state.orchestrator_query = ""

    query = st.text_area(
        "请输入任务描述",
        value=st.session_state.orchestrator_query,
        placeholder="例如：请分析某企业是否存在现金流风险，并说明更适合从哪个角色视角查看。",
        height=120,
        key="orchestrator_textarea",
    )

    st.session_state.orchestrator_query = query
    st.markdown('</div>', unsafe_allow_html=True)

    if query.strip():
        result = detect_role_by_query(query)

        st.markdown('<div class="module-box">', unsafe_allow_html=True)
        render_section_header("识别结果", "系统基于当前输入，对角色路径和任务类型进行初步判断。")

        result_col1, result_col2 = st.columns(2)

        with result_col1:
            st.markdown(
                f"""
                <div class="recommend-card">
                    <div class="recommend-label">推荐角色</div>
                    <div class="recommend-value">{result["role"]}</div>
                    <div class="recommend-note">
                        建议优先进入该角色工作台继续查看更细的分析结果。
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with result_col2:
            st.markdown(
                f"""
                <div class="recommend-card">
                    <div class="recommend-label">任务类型</div>
                    <div class="recommend-value">{result["task_type"]}</div>
                    <div class="recommend-note">
                        当前问题已被归类到相应分析场景，后续可以继续扩展为真实意图分类工作流。
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div class="summary-box">
                <div class="small-card-title">识别说明</div>
                <div class="muted-text">{result["reason"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="path-preview-box">
                <div class="path-preview-title">推荐分析路径预览</div>
                <div class="path-pill-row">
                    <span class="path-pill">任务识别</span>
                    <span class="path-pill">角色匹配</span>
                    <span class="path-pill">子智能体分析</span>
                    <span class="path-pill">综合结果输出</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        jump_col1, jump_col2, jump_col3, jump_col4 = st.columns(4)

        with jump_col1:
            if st.button("进入投资者页", key="goto_investor_from_orchestrator", use_container_width=True):
                st.session_state.current_page = "投资者"
                st.rerun()

        with jump_col2:
            if st.button("进入企业页", key="goto_enterprise_from_orchestrator", use_container_width=True):
                st.session_state.current_page = "企业"
                st.rerun()

        with jump_col3:
            if st.button("进入监管者页", key="goto_regulator_from_orchestrator", use_container_width=True):
                st.session_state.current_page = "监管者"
                st.rerun()

        with jump_col4:
            if st.button("留在总控页", key="stay_orchestrator_page", use_container_width=True):
                st.session_state.current_page = "总控智能体"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_analysis_flow("orchestrator")
    render_section_header("总控智能体对话", "在这里继续进行统一提问，后续可升级为真实多智能体协同调度对话。")
    render_chat("orchestrator", orchestrator_agent)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("协同分析预留区", "后续可扩展为真实的多角色联动分析与跨角色综合报告生成。")
    st.markdown(
        """
        <div class="path-preview-box">
            <div class="path-preview-title">未来可扩展能力</div>
            <div class="path-pill-row">
                <span class="path-pill">投资者视角结论汇总</span>
                <span class="path-pill">企业诊断结果联动</span>
                <span class="path-pill">监管风险交叉验证</span>
                <span class="path-pill">综合报告自动生成</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)


def render_investor_page():
    st.markdown("### 投资分析工作台")
    render_role_topbar("investor")

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("参数选择", "选择企业、年份和行业，确定当前分析范围。")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.selectbox("企业选择", ["企业A", "企业B", "企业C"], key="investor_company")

    with c2:
        st.selectbox("年份", ["2025", "2024", "2023"], key="investor_year")

    with c3:
        st.selectbox("行业", ["家电", "消费", "制造"], key="investor_industry")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("智能分析对话", "输入你的投资问题，系统会同步刷新分析结果。")
    render_chat("investor", investor_agent, on_response=update_analysis_state)
    st.markdown('</div>', unsafe_allow_html=True)

    investor_data = get_role_analysis_data("investor")

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_analysis_flow("investor")
    render_section_header("核心指标", "展示风险、增长质量、现金流安全和行业位置等关键信息。")
    render_metric_panel(investor_data.get("metrics", {}))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("分析摘要", "基于当前问题生成的阶段性判断与重点提示。")
    render_analysis_summary(investor_data.get("summary", ""))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("数据分析图表", "通过趋势分析和同业对比，辅助投资判断。")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("##### 趋势分析")
        render_line_chart(investor_data.get("trend_data"), "月份", "指标值")

    with chart_col2:
        st.markdown("##### 同业对比")
        render_bar_chart(investor_data.get("compare_data"), "类别", "评分")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("报告输出", "将当前分析结果保存到报告中心，或直接下载结构化报告。")
    col1, col2 = st.columns(2)

    investor_report = build_role_report(
        "投资者",
        investor_data,
        get_chat_history("investor")
    )

    with col1:
        if st.button("保存到报告中心", key="save_investor_report", use_container_width=True):
            save_report_to_center(
                role="投资者",
                report_name="投研简报",
                report_content=investor_report,
                report_type="Markdown",
            )
            st.success("已保存到报告中心。")

    with col2:
        st.download_button(
            label="下载投研简报（Markdown）",
            data=investor_report,
            file_name="investor_report.md",
            mime="text/markdown",
            key="download_investor_report",
            use_container_width=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)


def render_enterprise_page():
    st.markdown("### 企业运营工作台")
    render_role_topbar("enterprise")

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("参数选择", "选择企业、时间范围和指标类型，确定诊断上下文。")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.selectbox("企业选择", ["企业A", "企业B", "企业C"], key="enterprise_company")

    with c2:
        st.selectbox("时间范围", ["近1年", "近2年", "近3年"], key="enterprise_range")

    with c3:
        st.selectbox("指标类型", ["营收", "成本", "现金流", "综合"], key="enterprise_metric_type")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("智能诊断", "输入经营问题，系统将联动刷新诊断结果与建议。")
    render_chat("enterprise", enterprise_agent, on_response=update_analysis_state)
    st.markdown('</div>', unsafe_allow_html=True)

    enterprise_data = get_role_analysis_data("enterprise")

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_analysis_flow("enterprise")
    render_section_header("运营指标", "展示营收健康度、成本压力、现金流状态和运营评分。")
    render_metric_panel(enterprise_data.get("metrics", {}))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("分析摘要", "总结当前运营诊断的重点发现与改进方向。")
    render_analysis_summary(enterprise_data.get("summary", ""))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("数据分析", "通过趋势与行业对比，辅助识别经营压力来源。")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("##### 运营趋势")
        render_line_chart(enterprise_data.get("trend_data"), "月份", "运营健康度")

    with chart_col2:
        st.markdown("##### 行业对比")
        render_bar_chart(enterprise_data.get("compare_data"), "类别", "评分")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("建议输出", "保存经营诊断结果，并导出结构化报告。")
    col1, col2 = st.columns(2)

    enterprise_report = build_role_report(
        "企业",
        enterprise_data,
        get_chat_history("enterprise")
    )

    with col1:
        if st.button("保存到报告中心", key="save_enterprise_report", use_container_width=True):
            save_report_to_center(
                role="企业",
                report_name="经营诊断报告",
                report_content=enterprise_report,
                report_type="Markdown",
            )
            st.success("已保存到报告中心。")

    with col2:
        st.download_button(
            label="下载经营诊断报告（Markdown）",
            data=enterprise_report,
            file_name="enterprise_report.md",
            mime="text/markdown",
            key="download_enterprise_report",
            use_container_width=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)


def render_regulator_page():
    st.markdown("### 监管监测工作台")
    render_role_topbar("regulator")

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("监测参数", "选择行业、地区和异常等级，设置当前监测范围。")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.selectbox("行业", ["家电", "消费", "制造"], key="regulator_industry")

    with c2:
        st.selectbox("地区", ["全国", "华东", "华南", "华北"], key="regulator_region")

    with c3:
        st.selectbox("异常等级", ["全部", "高", "中", "低"], key="regulator_risk_level")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("智能分析", "输入监管任务，系统将联动更新异常识别与风险结果。")
    render_chat("regulator", regulator_agent, on_response=update_analysis_state)
    st.markdown('</div>', unsafe_allow_html=True)

    regulator_data = get_role_analysis_data("regulator")

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_analysis_flow("regulator")
    render_section_header("风险指标", "展示高风险企业数、异常波动数、披露冲突数和风险传播指数。")
    render_metric_panel(regulator_data.get("metrics", {}))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("分析摘要", "总结当前监管视角下的核心发现与优先关注点。")
    render_analysis_summary(regulator_data.get("summary", ""))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("风险分析图", "从异常趋势和风险分层两个角度观察整体变化。")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("##### 异常趋势")
        render_line_chart(regulator_data.get("trend_data"), "月份", "异常数量")

    with chart_col2:
        st.markdown("##### 风险分层")
        render_bar_chart(regulator_data.get("compare_data"), "类别", "企业数")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("输出", "保存监管分析结果，并导出结构化报告。")
    col1, col2 = st.columns(2)

    regulator_report = build_role_report(
        "监管者",
        regulator_data,
        get_chat_history("regulator")
    )

    with col1:
        if st.button("保存到报告中心", key="save_regulator_report", use_container_width=True):
            save_report_to_center(
                role="监管者",
                report_name="监管分析报告",
                report_content=regulator_report,
                report_type="Markdown",
            )
            st.success("已保存到报告中心。")

    with col2:
        st.download_button(
            label="下载监管报告（Markdown）",
            data=regulator_report,
            file_name="regulator_report.md",
            mime="text/markdown",
            key="download_regulator_report",
            use_container_width=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)


def render_about_page():
    st.markdown("### 系统说明")

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("项目定位", "面向投资者、企业管理者与监管机构的多角色智能体分析平台。")
    st.markdown(
        """
        <div class="muted-text">
            本系统以多角色智能体协同为核心，通过统一前端平台实现任务输入、角色切换、分析联动、
            图表展示、报告生成与报告管理。当前原型重点展示前端交互结构与多角色工作台设计，
            后续可进一步接入真实 Coze 智能体与工作流接口。
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("系统结构", "当前前端原型已具备完整的展示闭环。")
    st.markdown(
        """
        <div class="muted-text">
            目前系统已包含：首页入口、总控智能体、投资者工作台、企业工作台、监管者工作台、
            报告中心，以及对话联动、指标展示、图表分析和报告导出等模块。
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("后续扩展方向", "后续可继续完善真实业务能力与比赛展示效果。")
    st.markdown(
        """
        <div class="muted-text">
            后续可以继续接入 Coze 智能体接口、实现真实多角色协同分析、优化 UI 视觉风格、
            增加更丰富的图表类型、支持 PDF/Word 报告导出，并补充完整的数据来源说明与系统架构图。
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

def render_metric_cards():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">风险等级</div>
                <div class="metric-value">中等</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">增长质量</div>
                <div class="metric-value">良好</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">现金流安全</div>
                <div class="metric-value">稳定</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">行业位置</div>
                <div class="metric-value">前40%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_chart_placeholder():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="chart-box">
            图表区域：趋势图 / 雷达图 / 结构图
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="chart-box">
            图表区域：同业对比 / 风险分布
            </div>
            """,
            unsafe_allow_html=True,
        )

def render_reports_page():
    st.markdown("### 报告中心")

    report_items = get_report_center_items()

    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    render_section_header("历史报告列表", "统一查看、预览和下载各角色生成的结构化分析报告。")

    if not report_items:
        st.info("当前还没有保存的报告。请先在投资者、企业或监管者页面生成并保存报告。")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    for idx, item in enumerate(report_items):
        st.markdown(
            f"""
            <div class="card">
                <div class="small-card-title">{item['name']}</div>
                <div class="muted-text">
                    角色来源：{item['role']}<br>
                    报告类型：{item['type']}<br>
                    生成时间：{item['timestamp']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        btn_col1, btn_col2 = st.columns([1, 1])

        with btn_col1:
            st.download_button(
                label="下载该报告",
                data=item["content"],
                file_name=f"report_{idx + 1}.md",
                mime="text/markdown",
                key=f"download_report_center_{idx}",
                use_container_width=True,
            )

        with btn_col2:
            with st.expander("预览报告内容"):
                st.markdown(item["content"])

    st.markdown('</div>', unsafe_allow_html=True)