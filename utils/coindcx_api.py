import requests
import pandas as pd

def fetch_live_prices():
    url = "https://api.coindcx.com/exchange/ticker"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    return df

