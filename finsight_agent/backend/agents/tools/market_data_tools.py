import os
from alpha_vantage.timeseries import TimeSeries
from newsapi import NewsApiClient
from dotenv import load_dotenv

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def get_price_history(symbol: str):
    """Fetches the price history for a given stock symbol."""
    try:
        data, _ = ts.get_daily(symbol=symbol, outputsize='compact')
        return data
    except Exception as e:
        return f"Error fetching price history for {symbol}: {e}"

def get_news_sentiment(query: str):
    """Fetches news articles and their sentiment for a given query."""
    try:
        all_articles = newsapi.get_everything(q=query,
                                              language='en',
                                              sort_by='relevancy',
                                              page_size=5)
        return all_articles
    except Exception as e:
        return f"Error fetching news for {query}: {e}"
