# FinSight Agent – Autonomous AI Financial Analyst

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.9-blueviolet)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103-green)
![Next.js](https://img.shields.io/badge/Next.js-14-blue)

*FinSight Agent gives you the decision-making power of a financial analyst without the time, effort, or learning curve.*

---

## 1. Project Vision

In today's fast-paced financial markets, staying ahead requires constant vigilance. Investors, traders, and advisors spend countless hours gathering market data, tracking news, and analyzing complex trends to make informed decisions. This manual process is not only time-consuming but also prone to human error and oversight.

**FinSight Agent** was created to solve this problem. It is an autonomous AI-powered financial analyst designed to automate the entire market research workflow. From fetching real-time data to generating actionable investment insights, FinSight Agent acts as a tireless 24/7 junior analyst. It empowers users by saving them hours of manual work, eliminating the risk of missing critical opportunities, and delivering professional-grade insights in a clear, accessible format. Our vision is to democratize financial analysis, making sophisticated market intelligence available to everyone.

---

## 2. Technology Stack

FinSight Agent is built with a modern, scalable technology stack, carefully chosen for performance and reliability.

| Category      | Technology                                       | Purpose                                            |
|---------------|--------------------------------------------------|----------------------------------------------------|
| **Backend**   | [Python 3.9](https://www.python.org/)            | Core programming language                          |
|               | [FastAPI](https://fastapi.tiangolo.com/)         | High-performance web framework for the API         |
|               | [Uvicorn](https://www.uvicorn.org/)              | ASGI server to run the FastAPI application         |
|               | [Docker](https://www.docker.com/)                | Containerization for consistent deployment       |
| **Frontend**  | [Next.js](https://nextjs.org/) (React)           | Modern web framework for the user interface        |
|               | [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) | Core programming language for the UI           |
| **AI & Agents**| [Langchain](https://www.langchain.com/)          | Framework for developing AI-powered applications |
|               | [LangGraph](https://langchain-ai.github.io/langgraph/) | Building stateful, multi-agent workflows         |
|               | [OpenAI API](https://openai.com/docs)            | Powering the language models for the agents      |

---

## 3. System Architecture

The FinSight Agent operates on a multi-agent system architecture, where each agent has a specialized role. The workflow is orchestrated by a central `langgraph` state machine, ensuring a seamless flow of data and analysis.

```
┌──────────────────────────┐
│        Web Frontend      │  (Next.js - User submits query & views reports)
└────────────┬─────────────┘
             │  HTTP Request
             ▼
┌──────────────────────────┐
│        FastAPI Backend    │  (Receives request, returns report)
└────────────┬─────────────┘
             │ Calls Agent Orchestrator
             ▼
┌──────────────────────────┐
│    Agent Orchestrator     │  (LangGraph - Manages the stateful workflow)
└────────────┬─────────────┘
   ┌─────────┼──────────┐
   ▼         ▼          ▼
Planner   Market    Analysis     Report
Agent     Data &      Agent      Agent
          News Agents
```

### Workflow Explanation:

1.  **User Request:** The user submits a natural language query (e.g., "Analyze the financial health of Apple") through the Next.js web frontend.
2.  **Orchestrator Kick-off:** The FastAPI backend receives the request and invokes the LangGraph orchestrator.
3.  **Planner Agent:** The first agent in the workflow analyzes the user's query to create a plan, extract the stock symbol (e.g., "AAPL"), and formulate a news search query.
4.  **Data Gathering:**
    *   The **Market Data Agent** uses the extracted symbol to call the Alpha Vantage API for the latest stock prices.
    *   The **News Agent** uses the news query to call the News API for relevant financial news.
5.  **Analysis Agent:** This agent receives the market data and news articles. It uses an LLM to perform a sentiment analysis and generate a summary of the financial outlook.
6.  **Report Generation:** The **Report Agent** takes the analysis and formats it into a clean, professional report, which is then sent back to the user via the API.

---

## 4. Folder Structure

The project is organized into a clean, modular structure to separate concerns and improve maintainability.

```
finsight_agent/
│
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes and endpoints
│   │   ├── agents/       # All agent definitions and the orchestrator
│   │   ├── tools/        # External API clients (Alpha Vantage, News API, etc.)
│   │   └── main.py       # Main FastAPI application entrypoint
│   ├── Dockerfile        # Docker configuration for the backend
│   └── requirements.txt  # Python dependencies
│
├── frontend/
│   ├── components/     # Reusable React components
│   ├── pages/          # Next.js pages (routes)
│   ├── services/       # API client for communicating with the backend
│   └── package.json      # Node.js dependencies
│
├── notebooks/
│   └── demo_run.ipynb    # Jupyter notebook for demonstrating the API
│
├── render.yaml           # Deployment configuration for Render
└── README.md             # This file
```

---

## 5. Getting Started (Local Development)

Follow these steps to set up and run the FinSight Agent on your local machine.

### Prerequisites

*   Python 3.9+
*   Node.js 18+ and npm
*   An OpenAI API Key
*   An Alpha Vantage API Key
*   A News API Key

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd finsight_agent/backend
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file:**
    Create a new file named `.env` in the `backend` directory with the following content:
    ```
    OPENAI_API_KEY="your_openai_api_key"
    ALPHA_VANTAGE_API_KEY="your_alpha_vantage_api_key"
    NEWS_API_KEY="your_news_api_key"
    ```

4.  **Run the FastAPI server:**
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    The backend API will now be running at `http://localhost:8000`.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd finsight_agent/frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Create a `.env.local` file:**
    Create a new file named `.env.local` in the `frontend` directory and add the following line:
    ```
    NEXT_PUBLIC_API_URL=http://localhost:8000
    ```

4.  **Run the Next.js development server:**
    ```bash
    npm run dev
    ```
    The frontend will now be running at `http://localhost:3000`.

---

## 6. Backend In-Depth

### API Endpoints

*   `POST /agent`: Runs the agent pipeline with a user's query.

### The Agents

*   **`planner_agent.py`**: The brain of the operation. It interprets the user's natural language query and structures the task for the other agents by extracting key information.
*   **`market_data_agent.py`**: A simple, focused agent that retrieves stock data.
*   **`analysis_agent.py`**: The core analytical agent. It synthesizes market data and news into a coherent analysis.
*   **`report_agent.py`**: Takes the structured analysis and formats it into a human-readable report.
*   **`orchestrator.py`**: The conductor. It uses `langgraph` to ensure each agent performs its task in the correct order and that data flows smoothly between them.

### The Tools

*   **`market_api.py`**: A client for the Alpha Vantage API to fetch time-series stock data.
*   **`news_api.py`**: A client for the News API to fetch relevant financial news.
*   **`indicators.py`**: (Future work) A library for calculating financial indicators like SMA, EMA, etc.

---

## 7. Deployment

The application is configured for easy deployment to modern cloud platforms.

### Backend (Render)

1.  **Create a Blueprint Instance:** Log in to Render and create a new "Blueprint Instance."
2.  **Connect Your Repository:** Connect the GitHub repository containing this project.
3.  **Automatic Detection:** Render will automatically detect the `render.yaml` file and configure the web service.
4.  **Add Environment Variables:** In the Render dashboard, navigate to your service's "Environment" tab and add your secret keys (`OPENAI_API_KEY`, etc.).
5.  **Deploy:** Click "Create" or "Deploy" to launch the service.

### Frontend (Vercel)

1.  **Create a New Project:** Log in to Vercel and create a new project.
2.  **Connect Your Repository:** Connect the same GitHub repository.
3.  **Automatic Detection:** Vercel will automatically detect that it's a Next.js project.
4.  **Add Environment Variable:** In the project settings, add the `NEXT_PUBLIC_API_URL` environment variable and set its value to the URL of your deployed backend on Render.
5.  **Deploy:** Click "Deploy" to launch the frontend.
