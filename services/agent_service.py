import json
import re
import streamlit as st
from cozepy import Coze, TokenAuth, Message, ChatEventType


def get_coze_client():
    token = st.secrets["COZE_API_TOKEN"]
    base_url = st.secrets["COZE_BASE_URL"]

    return Coze(
        auth=TokenAuth(token=token),
        base_url=base_url,
    )


def build_agent_result(reply_text: str, structured_data: dict | None = None) -> dict:
    return {
        "reply_text": reply_text,
        "structured_data": structured_data or {
            "metrics": {},
            "summary": "",
            "charts": {},
            "tables": {},
        }
    }


def call_coze_bot(bot_id: str, message: str, user_id: str = "streamlit_user") -> str:
    coze = get_coze_client()
    chunks = []

    if not bot_id or str(bot_id).strip() in {"0", ""}:
        raise ValueError("COZE_BOT_ID_INVESTOR 未正确配置，当前读取到的 bot_id 无效。")

    for event in coze.chat.stream(
        bot_id=str(bot_id).strip(),
        user_id=user_id,
        additional_messages=[
            Message.build_user_question_text(message)
        ],
    ):
        if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
            if hasattr(event.message, "content"):
                if isinstance(event.message.content, str):
                    chunks.append(event.message.content)
                elif hasattr(event.message.content, "text"):
                    chunks.append(event.message.content.text)

        elif event.event == ChatEventType.CONVERSATION_MESSAGE_COMPLETED:
            if hasattr(event.message, "content"):
                if isinstance(event.message.content, str):
                    if not chunks:
                        chunks.append(event.message.content)
                elif hasattr(event.message.content, "text"):
                    if not chunks:
                        chunks.append(event.message.content.text)

    final_text = "".join(chunks).strip()
    return final_text if final_text else "Coze 未返回文本结果。"


def extract_json_text(text: str) -> str:
    """
    尝试从返回文本中提取 JSON：
    1. 直接就是 JSON
    2. 被 ```json ... ``` 包裹
    3. 前后混有说明文字
    """
    text = text.strip()

    # 去掉 markdown code fence
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    # 如果整体就是 JSON
    if text.startswith("{") and text.endswith("}"):
        return text

    # 尝试截取最外层大括号
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start:end + 1]

    return text


def normalize_structured_data(data: dict) -> dict:
    """
    给 structured_data 补默认字段，避免前端报错
    """
    structured = data.get("structured_data", {}) if isinstance(data, dict) else {}

    metrics = structured.get("metrics", {}) or {}
    summary = structured.get("summary", "") or ""
    charts = structured.get("charts", {}) or {}
    tables = structured.get("tables", {}) or {}

    trend_data = charts.get("trend_data", []) or []
    compare_data = charts.get("compare_data", []) or []

    return {
        "metrics": metrics,
        "summary": summary,
        "charts": {
            "trend_data": trend_data,
            "compare_data": compare_data,
        },
        "tables": tables,
    }


def investor_agent(message: str) -> dict:
    """
    投资者智能体：
    1. 调 Coze
    2. 期待 Coze 返回 JSON 文本
    3. 解析为统一协议
    """
    try:
        bot_id = str(st.secrets["COZE_BOT_ID_INVESTOR"]).strip()
        raw_text = call_coze_bot(bot_id=bot_id, message=message, user_id="investor_user")

        json_text = extract_json_text(raw_text)
        parsed = json.loads(json_text)

        reply_text = parsed.get("reply_text", "")
        structured_data = normalize_structured_data(parsed)

        # 如果 reply_text 为空，兜底给 summary
        if not reply_text:
            reply_text = structured_data.get("summary", "") or "已返回结构化结果，但缺少自然语言回复。"

        return build_agent_result(
            reply_text=reply_text,
            structured_data=structured_data
        )

    except json.JSONDecodeError:
        # Coze 没按 JSON 返回时，先兜底显示原始文本
        return build_agent_result(
            reply_text=raw_text if "raw_text" in locals() else "投资者智能体返回结果无法解析为 JSON。",
            structured_data={
                "metrics": {},
                "summary": "当前返回内容不是标准 JSON，页面暂不更新结构化图表与指标。",
                "charts": {},
                "tables": {},
            }
        )
    except Exception as e:
        return build_agent_result(
            reply_text=f"投资者智能体调用失败：{e}",
            structured_data={
                "metrics": {},
                "summary": "当前 Coze 调用失败，暂未生成结构化结果。",
                "charts": {},
                "tables": {},
            }
        )


def enterprise_agent(message: str) -> dict:
    return build_agent_result(
        reply_text=f"【企业智能体待接入】收到问题：{message}",
        structured_data={
            "metrics": {},
            "summary": "",
            "charts": {},
            "tables": {},
        }
    )


def regulator_agent(message: str) -> dict:
    return build_agent_result(
        reply_text=f"【监管者智能体待接入】收到问题：{message}",
        structured_data={
            "metrics": {},
            "summary": "",
            "charts": {},
            "tables": {},
        }
    )


def orchestrator_agent(message: str) -> dict:
    return build_agent_result(
        reply_text=f"【总控智能体待接入】收到问题：{message}",
        structured_data={
            "metrics": {},
            "summary": "",
            "charts": {},
            "tables": {},
        }
    )


def detect_role_by_query(message: str):
    if not message:
        return {
            "role": "总控智能体",
            "task_type": "未识别",
            "reason": "请输入任务后再进行识别。"
        }

    text = message.lower()

    investor_keywords = ["投资", "估值", "股价", "回报", "盈利", "风险", "关注", "值不值得", "现金流", "黄金"]
    enterprise_keywords = ["经营", "运营", "优化", "成本", "诊断", "效率", "库存", "管理", "改进"]
    regulator_keywords = ["监管", "异常", "监测", "风险传播", "高风险企业", "披露", "合规", "行业"]

    if any(word in text for word in investor_keywords):
        return {
            "role": "投资者",
            "task_type": "投资分析 / 风险识别",
            "reason": "当前问题更关注企业价值判断、风险水平或投资关注点。"
        }

    if any(word in text for word in enterprise_keywords):
        return {
            "role": "企业",
            "task_type": "经营诊断 / 优化建议",
            "reason": "当前问题更关注企业内部经营情况、运营压力或改进方向。"
        }

    if any(word in text for word in regulator_keywords):
        return {
            "role": "监管者",
            "task_type": "异常监测 / 监管分析",
            "reason": "当前问题更关注行业监测、异常识别、合规或系统性风险。"
        }

    return {
        "role": "总控智能体",
        "task_type": "综合任务",
        "reason": "当前问题可能涉及多角色协同，建议先由总控智能体进行统筹分析。"
    }