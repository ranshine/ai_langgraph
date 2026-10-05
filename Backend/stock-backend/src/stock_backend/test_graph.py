from stock_backend.graph.graph import graph

result = graph.invoke({
    "stock": "RELIANCE.NS",
    "analysis": "",
    "recommendation": "",
    "risk": "",
    "price": 0.0
})
print(result)
