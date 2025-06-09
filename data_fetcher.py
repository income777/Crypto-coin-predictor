import requests
import pandas as pd

def fetch_coin_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "90",
        "interval": "daily"
    }

    response = requests.get(url, params=params)
    
    # Add error handling
    if response.status_code != 200:
        raise ValueError(f"CoinGecko API error ({response.status_code}): {response.text}")

    data = response.json()

    prices = data.get("prices")
    if not prices:
        raise ValueError(f"No price data found for coin_id '{coin_id}'")

    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    return df
