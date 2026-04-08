import os
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_analysis_agent():
    """
    Initializes and returns the analysis agent.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0.0)

    prompt_template = """
    You are a financial analysis agent. Your role is to analyze market data and news to provide a summary of the findings.

    Market Data:
    {market_data}

    News Articles:
    {news_articles}

    Based on the provided data, provide a brief analysis and a market sentiment (Positive, Negative, or Neutral).
    """

    prompt = PromptTemplate(
        input_variables=["market_data", "news_articles"],
        template=prompt_template,
    )

    return prompt | llm | StrOutputParser()

if __name__ == '__main__':
    # Example usage
    if OPENAI_API_KEY:
        # This is a simplified example. In a real run, the data would be fetched by the other agents.
        market_data_example = pd.DataFrame({
            'close': [150.0, 152.5, 151.0, 153.0, 155.0],
            'volume': [100000, 110000, 105000, 120000, 125000]
        })

        news_articles_example = [
            {'title': 'Tech Giant Announces Record Profits', 'description': 'Shares soar after the company releases its quarterly earnings report.'},
            {'title': 'New Product Launch Met with Enthusiasm', 'description': 'The latest gadget from the company is receiving positive reviews.'}
        ]

        analysis_agent = get_analysis_agent()
        analysis = analysis_agent.invoke({
            "market_data": market_data_example.to_string(),
            "news_articles": str(news_articles_example)
        })
        print(analysis)
    else:
        print("Please set the OPENAI_API_KEY environment variable.")
