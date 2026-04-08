import os
from alpha_vantage.timeseries import TimeSeries
import pandas as pd

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

def get_stock_data(symbol: str):
    """
    Fetches daily time series data for a given stock symbol from Alpha Vantage.
    """
    if not ALPHA_VANTAGE_API_KEY:
        raise ValueError("ALPHA_VANTAGE_API_KEY environment variable not set.")

    ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
    try:
        data, meta_data = ts.get_daily(symbol=symbol, outputsize='compact')
        # Rename columns to be more descriptive
        data.rename(columns={
            '1. open': 'open',
            '2. high': 'high',
            '3. low': 'low',
            '4. close': 'close',
            '5. volume': 'volume'
        }, inplace=True)
        return data
    except Exception as e:
        return f"Error fetching stock data for {symbol}: {e}"

if __name__ == '__main__':
    # Example usage (requires ALPHA_VANTAGE_API_KEY to be set)
    if ALPHA_VANTAGE_API_KEY:
        stock_data = get_stock_data("IBM")
        if isinstance(stock_data, pd.DataFrame):
            print(stock_data.head())
        else:
            print(stock_data)
    else:
        print("Please set the ALPHA_VANTAGE_API_KEY environment variable.")
