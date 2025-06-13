import csv
import os
from datetime import datetime

import requests


NASDAQ_API_URL = "https://api.nasdaq.com/api/quote/{symbol}/info?assetclass=stocks"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch_price(symbol: str) -> str:
    """Fetch the latest stock price for `symbol` from Nasdaq."""
    url = NASDAQ_API_URL.format(symbol=symbol)
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data["data"]["primaryData"]["lastSalePrice"].replace("$", "")


def write_price(symbol: str, price: str, filename: str) -> None:
    new_file = not os.path.exists(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["time", "symbol", "price"])
        writer.writerow([datetime.now().isoformat(), symbol, price])


def main() -> None:
    symbols = os.environ.get("STOCK_SYMBOLS", "AAPL,MSFT").split(",")
    symbols = [s.strip().upper() for s in symbols if s.strip()]
    os.makedirs("result", exist_ok=True)
    filename = os.path.join("result", datetime.now().strftime("%y%m%d") + "-stocks.csv")
    for symbol in symbols:
        try:
            price = fetch_price(symbol)
            write_price(symbol, price, filename)
        except Exception as exc:
            print(f"Failed to fetch {symbol}: {exc}")


if __name__ == "__main__":
    main()
