import pandas as pd

def calculate_sma(data: pd.DataFrame, window: int):
    """
    Calculates the Simple Moving Average (SMA) for a given dataset.
    """
    if 'close' not in data.columns:
        raise ValueError("Input DataFrame must have a 'close' column.")

    return data['close'].rolling(window=window).mean()

if __name__ == '__main__':
    # Example Usage
    data = {'close': [10, 12, 15, 14, 16, 18, 20, 19, 22, 25]}
    df = pd.DataFrame(data)

    sma_5 = calculate_sma(df, 5)
    print("5-day SMA:")
    print(sma_5)
