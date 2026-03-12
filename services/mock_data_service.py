import pandas as pd


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