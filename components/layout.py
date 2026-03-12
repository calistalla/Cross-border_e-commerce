import streamlit as st
from components.chat import render_chat
from services.agent_service import (
    investor_agent,
    enterprise_agent,
    regulator_agent,
    orchestrator_agent,
)
from components.dashboard import (
    render_metric_panel,
    render_analysis_summary,
    render_line_chart,
    render_bar_chart,
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
        .main > div {
            padding-top: 3.2rem;
        }

        .block-container {
            padding-top: 3rem;
            padding-bottom: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        .page-title {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.3rem;
        }

        .page-desc {
            color: #666;
            font-size: 0.95rem;
            margin-bottom: 1.2rem;
        }

        .card {
            border: 1px solid #e6e8eb;
            border-radius: 16px;
            padding: 18px 20px;
            background: #ffffff;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
            margin-bottom: 16px;
        }

        .small-card-title {
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .muted-text {
            color: #7a7a7a;
            font-size: 0.9rem;
        }

        .hero-box {
            padding: 28px;
            border-radius: 20px;
            background: linear-gradient(135deg, #f7f9fc 0%, #eef3ff 100%);
            border: 1px solid #e6ebf5;
            margin-bottom: 20px;
        }

        .hero-title {
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 0.6rem;
        }

        .hero-desc {
            font-size: 1rem;
            color: #4f5660;
        }
        
        .feature-card {
            border: 1px solid #e8ecf3;
            border-radius: 18px;
            padding: 20px;
            background: #ffffff;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
            margin-bottom: 10px;
            min-height: 150px;
        }

        .feature-title {
            font-size: 1.15rem;
            font-weight: 700;
            margin-bottom: 10px;
            color: #111827;
        }

        .feature-desc {
            font-size: 0.95rem;
            color: #5b6470;
            line-height: 1.7;
        }

        .info-card {
            border: 1px solid #e8ecf3;
            border-radius: 16px;
            padding: 18px;
            background: #f9fbff;
            min-height: 130px;
            margin-bottom: 12px;
        }

        .flow-box {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            border: 1px solid #e6ebf5;
            border-radius: 18px;
            padding: 20px;
            background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
            margin-bottom: 12px;
            flex-wrap: wrap;
        }

        .flow-step {
            flex: 1;
            min-width: 180px;
            text-align: center;
            font-weight: 600;
            color: #1f2937;
            background: #eef4ff;
            border-radius: 14px;
            padding: 16px 12px;
        }

        .flow-arrow {
            font-size: 1.4rem;
            font-weight: 700;
            color: #7c8aa5;
        }

        .metric-card {
            border: 1px solid #e8ecf3;
            border-radius: 14px;
            padding: 16px;
            background: #ffffff;
            text-align: center;
        }

        .metric-title {
            font-size: 0.85rem;
            color: #6b7280;
        }

        .metric-value {
            font-size: 1.3rem;
            font-weight: 700;
            margin-top: 6px;
        }

        .chart-box {
            border: 1px dashed #cfd6e6;
            border-radius: 14px;
            padding: 40px;
            text-align: center;
            color: #7a8395;
            margin-bottom: 16px;
        }
        .summary-box {
            border: 1px solid #e8ecf3;
            border-radius: 16px;
            padding: 18px;
            background: #f8fbff;
            margin-bottom: 16px;
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


def render_right_panel():
    st.markdown("### 信息栏")

    st.markdown(
        """
        <div class="card">
            <div class="small-card-title">结论摘要</div>
            <div class="muted-text">后续用于显示智能体输出的关键结论。</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card">
            <div class="small-card-title">数据来源</div>
            <div class="muted-text">后续用于展示财务数据、规则库、外部信息来源。</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card">
            <div class="small-card-title">操作提示</div>
            <div class="muted-text">当前阶段为框架搭建，后续逐步加入对话、图表和报告导出。</div>
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
                面向投资者、企业管理者与监管机构，提供智能问答、数据分析、风险洞察与报告生成能力，
                通过多角色智能体协同，帮助用户完成更高质量的经营分析与辅助决策。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 角色入口")

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-title">投资者工作台</div>
                <div class="feature-desc">
                    面向投资分析、风险识别与价值判断，支持企业筛选、经营质量评估与同业对比分析。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("进入投资者工作台", key="home_investor", use_container_width=True):
            st.session_state.current_page = "投资者"
            st.rerun()

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-title">企业工作台</div>
                <div class="feature-desc">
                    面向经营诊断、指标监测与优化建议，帮助企业识别运营压力并生成改进方案。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("进入企业工作台", key="home_enterprise", use_container_width=True):
            st.session_state.current_page = "企业"
            st.rerun()

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-title">监管者工作台</div>
                <div class="feature-desc">
                    面向异常识别、行业监测与系统性风险分析，支持高风险主体筛查与全局观察。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("进入监管者工作台", key="home_regulator", use_container_width=True):
            st.session_state.current_page = "监管者"
            st.rerun()

    with col4:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-title">总控智能体</div>
                <div class="feature-desc">
                    作为统一入口，负责识别用户问题、推荐最合适的角色工作台，并支持后续多角色联动。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("进入总控智能体", key="home_orchestrator", use_container_width=True):
            st.session_state.current_page = "总控智能体"
            st.rerun()

    st.markdown("### 系统亮点")

    h1, h2, h3 = st.columns(3)

    with h1:
        st.markdown(
            """
            <div class="info-card">
                <div class="small-card-title">多角色协同</div>
                <div class="muted-text">
                    针对投资者、企业、监管者三类核心对象设计差异化功能入口与分析逻辑。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with h2:
        st.markdown(
            """
            <div class="info-card">
                <div class="small-card-title">自然语言交互</div>
                <div class="muted-text">
                    用户可以直接输入问题，系统根据任务类型返回分析结论、建议和结构化结果。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with h3:
        st.markdown(
            """
            <div class="info-card">
                <div class="small-card-title">图表与报告扩展</div>
                <div class="muted-text">
                    当前先完成前端原型，后续可逐步接入图表分析、报告导出与多智能体联动能力。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 演示流程")

    st.markdown(
        """
        <div class="flow-box">
            <div class="flow-step">Step 1　选择角色或输入任务</div>
            <div class="flow-arrow">→</div>
            <div class="flow-step">Step 2　智能体完成分析与推理</div>
            <div class="flow-arrow">→</div>
            <div class="flow-step">Step 3　输出结论、图表与报告</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 当前进度")
    st.success("已完成整体框架搭建，当前正在优化首页展示效果。")

def render_orchestrator_page():
    st.markdown("#### 总控智能体页面占位")
    st.text_area(
        "请输入任务",
        placeholder="例如：请分析某企业是否存在现金流风险，并推荐适合的角色工作台。",
        height=120,
    )
    st.button("开始分析", use_container_width=False)

    st.markdown("#### 总控智能体")
    render_chat("orchestrator", orchestrator_agent)

    st.markdown("### 推荐入口")
    st.success("后续这里将展示角色推荐、任务分解与多角色联动结果。")


def render_investor_page():
    st.markdown("### 投资分析工作台")

    st.markdown("#### 参数选择")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.selectbox("企业选择", ["企业A", "企业B", "企业C"])

    with c2:
        st.selectbox("年份", ["2025", "2024", "2023"])

    with c3:
        st.selectbox("行业", ["家电", "消费", "制造"])

    st.markdown("#### 智能分析对话")
    render_chat("investor", investor_agent)

    st.text_area(
        "请输入问题",
        placeholder="例如：这家公司是否值得关注？",
        height=120,
    )

    st.button("开始分析")

    st.markdown("#### 核心指标")
    render_metric_panel(get_investor_metrics())

    st.markdown("#### 分析摘要")
    render_analysis_summary(get_summary_text("investor"))

    st.markdown("#### 数据分析图表")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("##### 趋势分析")
        render_line_chart(get_trend_data(), "月份", "指标值")

    with chart_col2:
        st.markdown("##### 同业对比")
        render_bar_chart(get_compare_data(), "类别", "评分")

    st.markdown("#### 报告输出")
    col1, col2 = st.columns(2)

    with col1:
        st.button("生成投研简报")

    with col2:
        st.button("导出分析结果")


def render_enterprise_page():
    st.markdown("### 企业运营工作台")

    st.markdown("#### 参数选择")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.selectbox("企业选择", ["企业A", "企业B", "企业C"])

    with c2:
        st.selectbox("时间范围", ["近1年", "近2年", "近3年"])

    with c3:
        st.selectbox("指标类型", ["营收", "成本", "现金流", "综合"])

    st.markdown("#### 智能诊断")

    render_chat("enterprise", enterprise_agent)

    st.markdown("#### 运营指标")
    render_metric_panel(get_enterprise_metrics())

    st.markdown("#### 分析摘要")
    render_analysis_summary(get_summary_text("enterprise"))

    st.markdown("#### 数据分析")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("##### 运营趋势")
        render_line_chart(get_enterprise_trend_data(), "月份", "运营健康度")

    with chart_col2:
        st.markdown("##### 行业对比")
        render_bar_chart(get_enterprise_compare_data(), "类别", "评分")

    st.markdown("#### 建议输出")
    col1, col2 = st.columns(2)

    with col1:
        st.button("生成经营诊断报告")

    with col2:
        st.button("查看优化建议")


def render_regulator_page():
    st.markdown("### 监管监测工作台")

    st.markdown("#### 监测参数")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.selectbox("行业", ["家电", "消费", "制造"])

    with c2:
        st.selectbox("地区", ["全国", "华东", "华南", "华北"])

    with c3:
        st.selectbox("异常等级", ["全部", "高", "中", "低"])

    st.markdown("#### 智能分析")

    render_chat("regulator", regulator_agent)

    st.markdown("#### 风险指标")
    render_metric_panel(get_regulator_metrics())

    st.markdown("#### 分析摘要")
    render_analysis_summary(get_summary_text("regulator"))

    st.markdown("#### 风险分析图")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("##### 异常趋势")
        render_line_chart(get_regulator_trend_data(), "月份", "异常数量")

    with chart_col2:
        st.markdown("##### 风险分层")
        render_bar_chart(get_regulator_compare_data(), "类别", "企业数")

    st.markdown("#### 输出")
    col1, col2 = st.columns(2)

    with col1:
        st.button("生成监管报告")

    with col2:
        st.button("导出异常清单")

def render_reports_page():
    st.markdown("#### 报告中心占位")
    st.write("后续这里用于统一查看和下载投资者、企业、监管者生成的报告。")


def render_about_page():
    st.markdown("#### 系统说明占位")
    st.write("后续这里可以放项目背景、系统架构图、数据来源说明、比赛介绍。")

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