from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import JsonOutputParser
from pydantic import BaseModel, Field

class AnalysisResult(BaseModel):
    rating: str = Field(description="The rating of the asset (buy/hold/avoid)")
    rationale: str = Field(description="The rationale for the rating")
    risk_level: str = Field(description="The risk level of the asset (low/medium/high)")
    time_horizon: str = Field(description="The recommended time horizon for the investment (short/medium/long)")

class AnalysisAgent:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0, model="gpt-4-0125-preview")
        self.parser = JsonOutputParser(pydantic_object=AnalysisResult)
        self.prompt = ChatPromptTemplate.from_template(
            """You are an expert financial analyst.
            Analyze the following market data and provide a detailed analysis.

            Market data: {data}

            Your analysis should be in the following JSON format:
            {format_instructions}
            """
        )
        self.chain = self.prompt | self.llm | self.parser

    def run(self, data: str):
        return self.chain.invoke({
            "data": data,
            "format_instructions": self.parser.get_format_instructions()
        })
