from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

from .planner_agent import PlannerAgent
from .market_data_agent import MarketDataAgent
from .analysis_agent import AnalysisAgent
from .report_agent import ReportAgent
from .notification_agent import NotificationAgent

class AgentState(TypedDict):
    request: str
    plan: str
    market_data: str
    analysis: dict
    report: str
    notification_status: str

class AgentGraph:
    def __init__(self):
        self.planner_agent = PlannerAgent()
        self.market_data_agent = MarketDataAgent()
        self.analysis_agent = AnalysisAgent()
        self.report_agent = ReportAgent()
        self.notification_agent = NotificationAgent()
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("planner", self._run_planner)
        workflow.add_node("market_data", self._run_market_data)
        workflow.add_node("analysis", self._run_analysis)
        workflow.add_node("report", self._run_report)
        workflow.add_node("notification", self._run_notification)

        workflow.set_entry_point("planner")
        workflow.add_edge("planner", "market_data")
        workflow.add_edge("market_data", "analysis")
        workflow.add_edge("analysis", "report")
        workflow.add_edge("report", "notification")
        workflow.add_edge("notification", END)

        return workflow.compile()

    def _run_planner(self, state):
        plan = self.planner_agent.run(state["request"])
        return {"plan": plan}

    def _run_market_data(self, state):
        market_data = self.market_data_agent.run(state["plan"])
        return {"market_data": str(market_data)}

    def _run_analysis(self, state):
        analysis = self.analysis_agent.run(state["market_data"])
        return {"analysis": analysis}

    def _run_report(self, state):
        report = self.report_agent.run(state["analysis"])
        return {"report": report}

    def _run_notification(self, state):
        notification_status = self.notification_agent.run(state["report"])
        return {"notification_status": notification_status}

    def run(self, request: str):
        return self.graph.invoke({"request": request})
