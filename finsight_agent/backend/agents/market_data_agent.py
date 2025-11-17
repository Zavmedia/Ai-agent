from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from .tools.market_data_tools import get_price_history, get_news_sentiment

class MarketDataAgent:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0, model="gpt-4-0125-preview")
        self.tools = [get_price_history, get_news_sentiment]

    def run(self, plan: str):
        # This is a simplified execution model. In a real scenario,
        # we'd use a more sophisticated tool-calling agent.
        # For now, we'll just execute the first tool mentioned in the plan.

        if "price history" in plan.lower():
            # a simple parser to get the symbol
            symbol = plan.split("price history for ")[1].split()[0]
            return get_price_history(symbol)

        if "news sentiment" in plan.lower():
            query = plan.split("news sentiment for ")[1]
            return get_news_sentiment(query)

        return "No appropriate tool found for the task."
