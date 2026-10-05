from langchain_core.messages import HumanMessage, SystemMessage

from stock_backend.graph.state import StockState
from stock_backend.graph.tools import get_stock_price
from stock_backend.services.llm import llm
from stock_backend.services.models import Recommendation, Risk, StockAnalysis, Summary


llm_with_tools = llm.bind_tools([get_stock_price])
structured_llm = llm.with_structured_output(StockAnalysis)


def analyze_stock(state: StockState) -> StockState:
    stock = state["stock"]
    messages = state.get("messages", [])

    if not messages:
        prompt = f"""
        Analyze the stock {stock}.

        First, get the current stock price using the available stock tool.

        After receiving the stock price, provide:
        1. Current stock price
        2. Short business analysis
        3. Key risks
        4. BUY, HOLD, or SELL recommendation

        Use the actual stock price returned by the tool.

        This is only a learning example, not financial advice.
        """

        human_message = HumanMessage(content=prompt)

        response = llm_with_tools.invoke(
            [human_message]
        )

        if response.tool_calls:
            return {"messages": [human_message, response]}

        # If the model answers without calling the price tool, still return
        # the structured fields expected by the API response.
        messages = [human_message, response]

    result = structured_llm.invoke(messages)

    return {
        "messages": messages,
        "analysis": result.analysis,
        "recommendation": result.recommendation,
        "risk": result.risk,
        "price": result.price,
    }


def recommendation(state: StockState):
    structured_llm = llm.with_structured_output(Recommendation)
    # For now, use the analysis + price to ask the LLM
    response = structured_llm.invoke([
        SystemMessage(
            content="""
            Based on the stock analysis and current price,
            give only one recommendation:
            BUY, HOLD, or SELL.
            """
        ),
        HumanMessage(
            content=f"""
            Stock: {state['stock']}
            Price: {state['price']}
            Analysis: {state['analysis']}
            """
        )
    ])

    return {
        "recommendation": response.recommendation
    }


def risk(state: StockState):
    structured_llm = llm.with_structured_output(Risk)
    response = structured_llm.invoke([
        SystemMessage(
            content="""
            Based on the stock analysis and recommendation,
            determine the investment risk level.

            Give only one:
            LOW, MEDIUM, or HIGH.
            """
        ),
        HumanMessage(
            content=f"""
            Stock: {state['stock']}
            Price: {state['price']}
            Analysis: {state['analysis']}
            Recommendation: {state['recommendation']}
            """
        )
    ])

    return {
        "risk": response.risk
    }


def summary(state: StockState):
    structured_llm = llm.with_structured_output(Summary)
    response = structured_llm.invoke([
        SystemMessage(
            content="""
            Summarize the stock analysis in one short sentence.
            """
        ),
        HumanMessage(
            content=f"""
            Stock: {state['stock']}
            Price: {state['price']}
            Analysis: {state['analysis']}
            Recommendation: {state['recommendation']}
            """
        )
    ])

    return {
        "summary": response.summary
    }
