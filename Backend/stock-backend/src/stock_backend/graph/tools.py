import yfinance as yf
from langchain_core.tools import tool


@tool
def get_stock_price(stock: str) -> float:
    """Get the latest closing price for a stock ticker symbol."""
    ticker = yf.Ticker(stock)
    history = ticker.history(period="1d")  # Get the last day's data
    if history.empty:
        raise ValueError(f"No stock data found for {stock}")

    return round(float(history["Close"].iloc[-1]), 2)
