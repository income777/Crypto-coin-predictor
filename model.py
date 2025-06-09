from data_fetcher import fetch_coin_data

def predict_price(coin_id, horizon_days):
    try:
        df = fetch_coin_data(coin_id)
    except ValueError as e:
        return {
            "error": str(e),
            "coin_id": coin_id
        }

    df_prophet = df.reset_index().rename(columns={"timestamp": "ds", "price": "y"})

    model = Prophet(
    daily_seasonality=True,
    weekly_seasonality=True,
    yearly_seasonality=False,
    seasonality_mode='multiplicative'  # Better for volatile assets like crypto
)

    model.fit(df_prophet)

    future = model.make_future_dataframe(periods=horizon_days, freq='D')
    forecast = model.predict(future)

    predicted_price = forecast.iloc[-1]["yhat"]
    current_price = df["price"].iloc[-1]

    chart_data = df[-90:].reset_index().to_dict(orient="records")

    return {
        "current_price": round(current_price, 2),
        "predicted_price": round(predicted_price, 2),
        "horizon_days": horizon_days,
        "coin_id": coin_id,
        "chart_data": [
            {"timestamp": row["timestamp"].strftime("%Y-%m-%d"), "price": row["price"]}
            for row in chart_data
        ]
    }

