from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from stock_backend.graph.graph import graph


app = FastAPI()
# Allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StockRequest(BaseModel):
    stock: str


@app.get("/")
def root():
    return {"message": "Stock Backend is running"}


@app.post("/analyze")
def analyze_stock(request: StockRequest):

    result = graph.invoke({
        "stock": request.stock,
        "price": 0,
        "analysis": "",
        "recommendation": "",
        "risk": "",
        "summary": "",
    })

    return {
        "stock": result["stock"],
        "price": result["price"],
        "analysis": result["analysis"],
        "recommendation": result["recommendation"],
        "risk": result["risk"],
        "summary": result["summary"],
    }
