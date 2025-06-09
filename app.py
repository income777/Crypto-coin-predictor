
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from model import predict_price

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/predict")
def get_prediction(coin_id: str = Query("solana"), horizon_days: int = Query(1, ge=1, le=7)):
    result = predict_price(coin_id, horizon_days)
    return result
