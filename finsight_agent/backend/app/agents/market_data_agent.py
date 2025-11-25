from ..tools import market_api
import pandas as pd

def get_market_data_agent(symbol: str):
    """
    Agent responsible for fetching market data.
    This is a simple agent that directly calls the market_api tool.
    In a more complex scenario, this agent could have more sophisticated logic.
    """
    print(f"Fetching market data for {symbol}...")
    stock_data = market_api.get_stock_data(symbol)
    return stock_data

if __name__ == '__main__':
    # Example usage (requires ALPHA_VANTAGE_API_KEY to be set)
    # Make sure to set the ALPHA_VANTAGE_API_KEY environment variable
    import os
    if os.getenv("ALPHA_VANTAGE_API_KEY"):
        data = get_market_data_agent("GOOGL")
        if isinstance(data, pd.DataFrame):
            print(data.head())
        else:
            print(data)
    else:
        print("Please set the ALPHA_VANTAGE_API_KEY environment variable.")
