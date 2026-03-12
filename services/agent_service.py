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