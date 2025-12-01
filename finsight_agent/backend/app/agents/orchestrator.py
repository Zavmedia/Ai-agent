from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List, Optional
import operator
from . import planner_agent, market_data_agent, analysis_agent, report_agent, notification_agent
from ..tools import news_api
import pandas as pd

class AgentState(TypedDict):
    """
    Represents the state of the agent workflow.
    Each field holds the output of a specific agent or tool.
    'operator.add' is used to accumulate string outputs from multiple runs.
    """
    query: str
    plan: List[str]
    symbol: str
    news_query: str
    market_data: Annotated[str, operator.add]
    news_articles: Annotated[str, operator.add]
    analysis: str
    report: str
    user_email: Optional[str]

def run_planner(state):
    """
    Runs the planner agent to create a plan, extract the stock symbol, and generate a news query.
    """
    planner_output = planner_agent.get_planner_agent().invoke({"query": state["query"]})
    return {
        "plan": planner_output["plan"],
        "symbol": planner_output["symbol"],
        "news_query": planner_output["news_query"]
    }

def run_market_data(state):
    symbol = state["symbol"]
    if not symbol:
        return {"market_data": "No stock symbol found in the query."}
    data = market_data_agent.get_market_data_agent(symbol)
    data_str = data.to_string() if isinstance(data, pd.DataFrame) else "No data available"
    return {"market_data": data_str}

def run_news_fetcher(state):
    query = state["news_query"]
    if not query:
        return {"news_articles": "No news query found."}
    articles = news_api.get_financial_news(query)
    articles_str = str(articles) if articles else "No news available"
    return {"news_articles": articles_str}

def run_analysis(state):
    analysis = analysis_agent.get_analysis_agent().invoke({
        "market_data": state["market_data"],
        "news_articles": state["news_articles"]
    })
    return {"analysis": analysis}

def run_report(state):
    report = report_agent.get_report_agent().invoke({"analysis": state["analysis"]})
    return {"report": report}

def run_notification(state):
    """
    (Optional) Runs the notification agent if an email is provided.
    """
    if state.get("user_email"):
        notification_agent.get_notification_agent(
            to_address=state["user_email"],
            subject=f"FinSight Report for {state['query']}",
            body=state["report"]
        )
    return {}

def create_graph():
    """
    Creates the agent workflow graph using langgraph.
    """
    workflow = StateGraph(AgentState)

    # Add nodes for each agent
    workflow.add_node("planner", run_planner)
    workflow.add_node("market_data", run_market_data)
    workflow.add_node("news_fetcher", run_news_fetcher)
    workflow.add_node("analysis", run_analysis)
    workflow.add_node("report", run_report)

    # Define the sequence of execution
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "market_data")
    workflow.add_edge("market_data", "news_fetcher")
    workflow.add_edge("news_fetcher", "analysis")
    workflow.add_edge("analysis", "report")
    workflow.add_edge("report", END)

    return workflow.compile()

if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    load_dotenv(dotenv_path='../../.env')

    if os.getenv("OPENAI_API_KEY"):
        graph = create_graph()
        inputs = {"query": "Financial analysis for Tesla", "user_email": "test@example.com"}
        for output in graph.stream(inputs):
            for key, value in output.items():
                print(f"Output from node '{key}':")
                print("---")
                print(value)
            print("\\n---\\n")
    else:
        print("Please set the required environment variables.")
