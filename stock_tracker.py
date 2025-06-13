import argparse
import sys
from typing import Optional

import yfinance as yf


def get_price(ticker: str) -> float:
    """Fetch the latest price for ``ticker`` using yfinance.

    Parameters
    ----------
    ticker: str
        The ticker symbol to query.

    Returns
    -------
    float
        Latest price of the ticker.

    Raises
    ------
    RuntimeError
        If the price cannot be retrieved due to an invalid ticker or
        network-related issues.
    """
    try:
        stock = yf.Ticker(ticker)
        price: Optional[float] = stock.fast_info.get("last_price")
        if price is None:
            hist = stock.history(period="1d")
            if hist.empty:
                raise RuntimeError(f"No price data found for ticker '{ticker}'.")
            price = float(hist["Close"].iloc[-1])
        return float(price)
    except Exception as exc:  # catching broad exceptions to rewrap as RuntimeError
        raise RuntimeError(f"Failed to fetch price for '{ticker}'.") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fetch latest stock price")
    parser.add_argument("ticker", help="Ticker symbol, e.g., AAPL")
    args = parser.parse_args(argv)

    try:
        price = get_price(args.ticker)
        print(f"{args.ticker.upper()}: {price}")
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
