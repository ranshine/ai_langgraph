from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition

from stock_backend.graph.state import StockState
from stock_backend.graph.nodes import analyze_stock, recommendation, risk, summary
from stock_backend.graph.tools import get_stock_price
from langgraph.types import RetryPolicy


builder = StateGraph(StockState)

builder.add_node("analyze_stock", analyze_stock)
builder.add_node("recommendation", recommendation)
builder.add_node('risk', risk, retry_policy=RetryPolicy(max_attempts=3))
builder.add_node("summary", summary)
builder.add_node("tools", ToolNode([get_stock_price]))

builder.add_edge(START, "analyze_stock")


builder.add_conditional_edges(
    "analyze_stock",
    tools_condition,
    {
        "tools": "tools",
        "__end__": "recommendation",
    },
)

builder.add_edge("tools", "analyze_stock")
builder.add_edge("recommendation", 'risk')
builder.add_edge("recommendation", "summary")
builder.add_edge("risk", END)
builder.add_edge("summary", END)
graph = builder.compile()
