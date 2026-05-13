# -*- coding: utf-8 -*-
"""Market strategy blueprints for CN/HK/US daily market recap."""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class StrategyDimension:
    """Single strategy dimension used by market recap prompts."""

    name: str
    objective: str
    checkpoints: List[str]


@dataclass(frozen=True)
class MarketStrategyBlueprint:
    """Region specific market strategy blueprint."""

    region: str
    title: str
    positioning: str
    principles: List[str]
    dimensions: List[StrategyDimension]
    action_framework: List[str]

    def to_prompt_block(self) -> str:
        """Render blueprint as prompt instructions."""
        principles_text = "\n".join([f"- {item}" for item in self.principles])
        action_text = "\n".join([f"- {item}" for item in self.action_framework])

        dims = []
        for dim in self.dimensions:
            checkpoints = "\n".join([f"  - {cp}" for cp in dim.checkpoints])
            dims.append(f"- {dim.name}: {dim.objective}\n{checkpoints}")
        dimensions_text = "\n".join(dims)

        return (
            f"## Strategy Blueprint: {self.title}\n"
            f"{self.positioning}\n\n"
            f"### Strategy Principles\n{principles_text}\n\n"
            f"### Analysis Dimensions\n{dimensions_text}\n\n"
            f"### Action Framework\n{action_text}"
        )

    def to_markdown_block(self) -> str:
        """Render blueprint as markdown section for template fallback report."""
        dims = "\n".join([f"- **{dim.name}**: {dim.objective}" for dim in self.dimensions])
        section_title = "### VI. Strategy Framework" if self.region == "us" else "### 六、策略框架"
        return f"{section_title}\n{dims}\n"


CN_BLUEPRINT = MarketStrategyBlueprint(
    region="cn",
    title="A股市场量化技术面与趋势复盘策略",
    positioning="结合量化指标、趋势结构与资金博弈，形成次日硬逻辑交易计划。",
    principles=[
        "先看指数技术指标（RSI/BOLL），再看量能结构，最后看板块持续性。",
        "结论必须映射到具体的支撑压力位、仓位控制与风险止损动作。",
        "判断必须基于量化指标数据与近3日新闻，杜绝主观臆测。",
    ],
    dimensions=[
        StrategyDimension(
            name="趋势结构与量化指标",
            objective="通过价格形态与动能指标判断市场绝对强弱。",
            checkpoints=[
                "分析上证/深证/创业板均线排列，给出当前 20日均线(MA20) 的偏离度",
                "计算并分析 RSI(14) 指标：判断是否进入超买(>70)或超卖(<30)区间",
                "观察布林带(BOLL)形态：价格处于哪条轨道，开口是否出现挤压或扩张",
                "确定关键支撑阻力位：通过近 20 日最高/最低价给出具体数值参考"
            ],
        ),
        StrategyDimension(
            name="资金情绪与博弈",
            objective="识别短线风险偏好与量价背离风险。",
            checkpoints=[
                "涨跌家数与涨跌停结构：分析赚钱效应是否正在发生多空转换",
                "成交额分析：对比 5 日均量，判断当前属于放量攻击还是缩量震荡",
                "高位股表现：是否有核心龙头封板，或出现明显的 A 字顶/高位放量滞涨"
            ],
        ),
        StrategyDimension(
            name="主线板块技术面",
            objective="提炼具备技术面突破特征的可交易主线。",
            checkpoints=[
                "领涨板块形态：是否属于底部放量突破或回踩重要均线支撑",
                "板块联动性：观察是否有 3 只及以上标的涨停形成明显的资金共振",
                "规避方向：处于下降通道、均线空头排列或 MACD 高位死叉的板块"
            ],
        ),
    ],
    action_framework=[
        "进攻：指数站稳 MA20 + RSI 未超买 + 成交额放大 + 主线板块底部突破。",
        "均衡：指数处于 BOLL 中轨震荡或 RSI 在 50 附近，控制仓位，等待方向选择。",
        "防守：指数触碰 BOLL 上轨回落 + RSI 超买 + 领跌扩散，优先止损与减仓。",
    ],
)

US_BLUEPRINT = MarketStrategyBlueprint(
    region="us",
    title="US Market Regime Strategy (Technical Enhanced)",
    positioning="Focus on index technicals (RSI/Levels), macro narratives, and factor rotation.",
    principles=[
        "Read market regime from S&P 500, Nasdaq technical indicators and volume alignment.",
        "Separate quantitative momentum signals from theme-driven macro narratives.",
        "Translate recap into actionable risk-on/risk-off stance with explicit technical invalidation points.",
    ],
    dimensions=[
        StrategyDimension(
            name="Trend & Momentum",
            objective="Classify the market regime using price action and oscillators.",
            checkpoints=[
                "Check RSI(14) and Distance from 50-day SMA for SPX/NDX/DJI",
                "Identify key Fibonacci retracement levels or previous high/low support",
                "Volume confirmation: Is the current move backed by institutional participation",
            ],
        ),
        StrategyDimension(
            name="Macro & Flows",
            objective="Map policy/rates narrative into equity risk appetite.",
            checkpoints=[
                "Treasury yield (10Y) and USD Index technical breakout/breakdown",
                "Market breadth (Advance/Decline line) and leadership concentration",
                "Defensive vs Growth factor rotation in context of VIX levels",
            ],
        ),
        StrategyDimension(
            name="Sector Themes",
            objective="Identify persistent leaders and vulnerable laggards.",
            checkpoints=[
                "AI/Semiconductor trend persistence vs overextended technicals",
                "Energy/Financials sensitivity to macro data and technical support levels",
                "Volatility signals from Skew index and large-cap earnings gaps",
            ],
        ),
    ],
    action_framework=[
        "Risk-on: Indices reclaiming key SMAs + RSI < 70 + positive breadth.",
        "Neutral: Choppy price action near pivot points; focus on selective relative strength.",
        "Risk-off: RSI bearish divergence + failed breakouts + rising VIX; prioritize capital preservation.",
    ],
)

HK_BLUEPRINT = MarketStrategyBlueprint(
    region="hk",
    title="港股市场量化技术面复盘策略",
    positioning="聚焦恒生系列指数技术形态、南向资金动向与关键水位博弈。",
    principles=[
        "先看恒指/恒科技术形态与关键整数关口，再看南向资金流向，最后看板块强度。",
        "所有建议必须基于支撑压力位与 RSI/MACD 等量化反馈。",
        "结合宏观政策面与技术面共振点，寻找高胜率交易机会。",
    ],
    dimensions=[
        StrategyDimension(
            name="技术趋势结构",
            objective="判断市场处于超跌反弹、趋势加速还是受阻回落阶段。",
            checkpoints=[
                "恒指/恒科是否同步站上关键均线，RSI 是否处于背离状态",
                "量价配合情况：上涨是否放量，下跌是否缩量",
                "识别关键水位：如 20000 点关口或前期跳空缺口的压力/支撑"
            ],
        ),
        StrategyDimension(
            name="资金情绪分析",
            objective="识别南向资金与海外流动的博弈强度。",
            checkpoints=[
                "南向资金净流入规模及对权重股的增减持技术点",
                "港元汇率（USD/HKD）所处区间对流动性的暗示",
                "恒生波幅指数 (VHSI) 释放的避险或贪婪信号"
            ],
        ),
        StrategyDimension(
            name="主线板块分析",
            objective="提炼港股特有权重的技术面逻辑。",
            checkpoints=[
                "互联网平台/科网股：是否在关键技术位获得支撑或面临平台突破",
                "高股息/国特估板块：趋势持续性及 RSI 是否过热",
                "政策敏感板块：技术面是否对近期政策利好做出放量反馈"
            ],
        ),
    ],
    action_framework=[
        "进攻：指数技术位突破 + 南向资金持续放量流入 + 主线形态走强。",
        "均衡：指数在狭窄区间震荡，成交低迷，维持轻仓观察。",
        "防守：技术位破位 + 港元汇率走弱 + 波动率飙升，减仓锁利或空仓避险。",
    ],
)


def get_market_strategy_blueprint(region: str) -> MarketStrategyBlueprint:
    """Return strategy blueprint by market region."""
    if region == "us":
        return US_BLUEPRINT
    if region == "hk":
        return HK_BLUEPRINT
    return CN_BLUEPRINT
