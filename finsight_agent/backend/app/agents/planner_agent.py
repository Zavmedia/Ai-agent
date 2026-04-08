import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_planner_agent():
    """
    Initializes and returns the planner agent.

    This agent uses a ChatOpenAI model to create a plan based on a user's query.
    It structures its output in JSON format, which includes the plan, the extracted
    stock symbol, and a query for news articles.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0.0)

    prompt_template = """
    You are a financial planning agent. Your role is to take a user's query and create a step-by-step plan,
    while also extracting the key financial symbol (e.g., stock ticker) and a search query for news.

    User Query: {query}

    Based on this query, provide a JSON object with the following keys:
    - "plan": A list of strings representing the steps to take.
    - "symbol": The stock symbol or ticker (e.g., "AAPL", "GOOGL"). If no symbol is found, return null.
    - "news_query": A concise query for fetching relevant news articles.

    Example:
    User Query: "Weekly Nifty50 insights for moderate risk"
    Output: {{
        "plan": [
            "Gather relevant market data for Nifty50.",
            "Fetch recent financial news about the Indian market.",
            "Analyze the gathered data and news.",
            "Generate a report with insights and recommendations for a moderate risk profile.",
            "Send the report to the user."
        ],
        "symbol": "^NSEI",
        "news_query": "Nifty50 India market"
    }}
    """

    prompt = PromptTemplate(
        input_variables=["query"],
        template=prompt_template,
    )

    return prompt | llm | JsonOutputParser()

if __name__ == '__main__':
    # Example usage (requires OPENAI_API_KEY to be set)
    if OPENAI_API_KEY:
        planner = get_planner_agent()
        query = "Weekly Nifty50 insights for moderate risk"
        plan = planner.invoke({"query": query})
        print(plan)
    else:
        print("Please set the OPENAI_API_KEY environment variable.")
