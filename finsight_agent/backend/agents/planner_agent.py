from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

class PlannerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0, model="gpt-4-0125-preview")
        self.prompt = ChatPromptTemplate.from_template(
            """You are a master financial planning agent.
            Given a user request, create a detailed, step-by-step execution plan.
            Your plan should be a list of tasks for other agents to complete.

            User request: {request}

            Your plan:"""
        )
        self.chain = self.prompt | self.llm | StrOutputParser()

    def run(self, request: str):
        return self.chain.invoke({"request": request})
