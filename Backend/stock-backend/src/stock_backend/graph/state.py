from langgraph.graph import MessagesState


class StockState(MessagesState):
    stock: str
    analysis: str
    recommendation: str
    risk: str
    price: float
    summary: str
