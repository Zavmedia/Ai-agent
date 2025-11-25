import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_report_agent():
    """
    Initializes and returns the report agent.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0.0)

    prompt_template = """
    You are a financial reporting agent. Your role is to take a financial analysis and format it into a clean, professional report.

    Analysis:
    {analysis}

    Format the analysis into a report with the following sections:
    - Executive Summary
    - Market Sentiment
    - Key Findings
    - Disclaimer

    Keep the report concise and easy to read.
    """

    prompt = PromptTemplate(
        input_variables=["analysis"],
        template=prompt_template,
    )

    return prompt | llm | StrOutputParser()

if __name__ == '__main__':
    # Example usage
    if OPENAI_API_KEY:
        analysis_example = """
        The market data shows a consistent upward trend in the stock price, with increasing volume.
        This suggests strong investor confidence. The news is overwhelmingly positive, with reports of record profits and successful product launches.
        Market sentiment is Positive.
        """

        report_agent = get_report_agent()
        report = report_agent.invoke({"analysis": analysis_example})
        print(report)
    else:
        print("Please set the OPENAI_API_KEY environment variable.")
