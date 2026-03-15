import requests


# ===============================
# 未来接入 Coze 的位置
# ===============================

def call_coze_agent(message, role):

    """
    未来替换为 Coze API
    """

    # 示例返回
    return f"【{role}智能体】收到问题：{message}\n\n这里将返回真实分析结果。"



# ===============================
# 各角色智能体
# ===============================

def investor_agent(message):

    return call_coze_agent(message, "投资者")


def enterprise_agent(message):

    return call_coze_agent(message, "企业")


def regulator_agent(message):

    return call_coze_agent(message, "监管者")


def orchestrator_agent(message):

    return call_coze_agent(message, "总控")

def detect_role_by_query(message: str):
    """
    根据用户输入，粗略判断更适合哪个角色页面
    这一版先用关键词规则，后续可替换为 Coze / 后端真实分类结果
    """
    if not message:
        return {
            "role": "总控智能体",
            "task_type": "未识别",
            "reason": "请输入任务后再进行识别。"
        }

    text = message.lower()

    investor_keywords = ["投资", "估值", "股价", "回报", "盈利", "风险", "关注", "值不值得", "现金流"]
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