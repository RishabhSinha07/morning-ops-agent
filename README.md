# morning-ops-agent

## A daily workflow that
1. Detects your location
2. Fetches:
    - Today’s weather (morning + evening commute)
    - Relevant local news
    - Transit/traffic hints (basic)
3. Uses an LLM to summarize + advise
4. Sends you a morning newsletter
5. Runs automatically every day


## Architecture

CRON (daily)

  ↓

LangChain Workflow (Python)
- Location Resolver
- Weather Tool
- News Tool
- LLM Summarizer
- Newsletter Formatter

  ↓

Delivery (Email / Notion / Slack)

## Tech Stack (All Free-Friendly)
Core
- LangChain (Python)
- OpenAI / Groq / Together (free or cheap LLM tier)
- Requests for APIs

APIs (No credit card required)
1. Weather	Open-Meteo (free, no key)
2. Location	ipapi.co (free, no key)
3. News	GNews / NewsAPI free tier
4. Time	Python datetime
5. Tavily

