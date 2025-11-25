import os
from newsapi import NewsApiClient

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_financial_news(query: str):
    """
    Fetches financial news articles for a given query from the News API.
    """
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY environment variable not set.")

    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    try:
        articles = newsapi.get_everything(
            q=query,
            language='en',
            sort_by='relevancy',
            page_size=5
        )
        return articles['articles']
    except Exception as e:
        return f"Error fetching news for {query}: {e}"

if __name__ == '__main__':
    # Example usage (requires NEWS_API_KEY to be set)
    if NEWS_API_KEY:
        news = get_financial_news("Apple")
        if isinstance(news, list):
            for article in news:
                print(f"Title: {article['title']}")
                print(f"URL: {article['url']}")
                print("-" * 20)
        else:
            print(news)
    else:
        print("Please set the NEWS_API_KEY environment variable.")
