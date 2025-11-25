# FinSight Agent – Autonomous AI Financial Analyst

## 1. Overview
FinSight Agent fetches market + news data, analyzes assets using AI and quant logic, and generates PDF investment reports automatically.

## 2. Features
✔ Multi-agent workflow
✔ Tool calling (market API, news API, email)
✔ Strategy configuration via web UI
✔ PDF report with ratings and rationale
✔ Supports scheduling and manual runs

## 3. System Architecture
```
┌──────────────────────────┐
│        Web Frontend      │  (Next.js - user creates strategy & views reports)
└────────────┬─────────────┘
             │  HTTP Request
             ▼
┌──────────────────────────┐
│        FastAPI Backend    │  Receives run request / returns report
└────────────┬─────────────┘
             │ Calls Orchestrator
             ▼
┌──────────────────────────┐
│    Agent Orchestrator     │  (LangGraph / Agent framework)
└────────────┬─────────────┘
   ┌─────────┼──────────┬──────────┐
   ▼         ▼          ▼          ▼
Market   Analysis     Report   Notification
Data     Agent        Agent        Agent
Agent                 (PDF)      (Email)
```

**Data Sources/Tools connected**

* Market Data API
* News API
* Indicators Calculator
* Email Sending Service
* Database

**Final Outputs**

* Report in PDF/HTML + Dataset for dashboard
* Email/web notification

## 4. Implementation Details
### List of agents:
- PlannerAgent – creates workflow plan
- MarketDataAgent – fetches live data via tools
- AnalysisAgent – evaluates and rates assets
- ReportAgent – generates PDF/HTML report
- NotificationAgent – sends email

### List of tools:
- `market_api.py`
- `news_api.py`
- `indicators.py`
- `email_service.py`

## 5. How to Run
### Backend
1.  **Create a `.env` file** in the `backend` directory with your API keys (see `notebooks/demo_run.ipynb` for the required variables).
2.  **Install dependencies:** `pip install -r backend/requirements.txt`
3.  **Run the FastAPI server:** `uvicorn app.main:app --reload --ws-ping-interval 20 --ws-ping-timeout 20 --host 0.0.0.0 --port 8000`

### Database
For production, it is recommended to use a PostgreSQL database. The included `render.yaml` file will automatically provision a free PostgreSQL database on Render.

## 6. Deployment
### Backend (Render)
1.  Create a new "Blueprint Instance" on Render.
2.  Connect your GitHub repository.
3.  Render will automatically detect the `render.yaml` file and configure the services.
4.  Add your secret environment variables (API keys) in the Render dashboard.
5.  Deploy the service.

### Frontend (Vercel)
1.  Create a new project on Vercel.
2.  Connect your GitHub repository.
3.  Vercel will automatically detect the Next.js framework.
4.  Set the `NEXT_PUBLIC_API_URL` environment variable to the URL of your deployed backend on Render.
5.  Deploy the project.
