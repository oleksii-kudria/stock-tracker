# Stock Tracker

This repository contains a simple script for fetching real-time stock prices from the Nasdaq API and storing them locally.

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. (Optional) Define the list of stock symbols to track using the `STOCK_SYMBOLS` environment variable. Symbols should be comma separated. Default is `AAPL,MSFT`.

## Usage

Run the script manually:

```bash
python fetch_stocks.py
```

Each execution appends the latest prices to a CSV file located in the `result/` directory. A new file is created every day with the name format `YYMMDD-stocks.csv`.

## Running every minute with cron

To collect prices every minute on a Linux system, add the following line to your crontab (edit with `crontab -e`):

```
* * * * * /usr/bin/python /path/to/stock-tracker/fetch_stocks.py >> /tmp/stock_tracker.log 2>&1
```

Make sure to adjust the path to the Python interpreter and repository location to match your system.
