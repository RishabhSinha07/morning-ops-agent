# 🌅 Morning Ops Agent

An **agentic AI workflow** that generates a **personalized morning commute briefing** for any city by combining **live weather**, **local news**, and **LLM-based reasoning**, then publishing the final report directly to **Notion**.

---

## 🚀 What It Does

Given a **user-provided city**, the agent:

1. 🌦️ Fetches **current weather conditions**
2. 📰 Retrieves **local news relevant to commuting**
3. 🧠 Uses **LLMs to reason over all inputs** and identify:
   - Weather impacts (rain, snow, heat, alerts)
   - Transit disruptions
   - Road closures, strikes, events, or emergencies
4. 📝 Generates a concise, human-friendly **morning commute report**
5. 📓 Publishes the report to a **Notion page** for easy daily reference

Think of it as a **daily operations briefing for your commute**.

---

## 🧠 Why Agentic AI?

Instead of hard-coded logic, this project uses an **agent-based architecture**:

- Tools fetch **raw signals** (weather, news)
- The LLM **decides what matters**
- The agent **filters noise**, synthesizes insights, and produces a clear recommendation

This allows the system to adapt to:
- Different cities
- Different types of disruptions
- Evolving news patterns

---

## 🏗️ Architecture Overview

User (City)

↓

Agent

├── Weather Tool

├── Local News Tool

├── LLM Reasoning

↓
Commute Impact Analysis

↓

Formatted Morning Report

↓

Notion Page



---

## 🛠️ Tech Stack

- **Python 3.12**
- **LangChain / LangGraph** — agent orchestration
- **LLMs** — reasoning and summarization
- **Notion API** — report publishing
- **uv** — fast Python dependency management
- **Requests** — external data fetching

---


---

## ⚙️ Setup

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/your-username/morning-ops-agent.git
cd morning-ops-agent

2️⃣ Install Dependencies (using uv)

uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

3️⃣ Environment Variables

Create a .env file:

OPENAI_API_KEY=your_key_here
NOTION_API_KEY=your_notion_key
NOTION_DATABASE_ID=your_database_id

▶️ Run the Agent
python main.py --city "Boston"

This will:

- Generate a commute-focused morning report

- Publish it directly to your Notion workspace

```

📝 Example Output

```
Morning Commute Briefing — Boston

Light rain expected between 8–10 AM — carry a waterproof jacket

Minor delays reported on the Red Line due to signal issues

No major road closures detected
Recommend leaving 10–15 minutes earlier than usual
```
---
🔮 Future Enhancements

⏰ Scheduled daily runs (cron / GitHub Actions)

📱 Push notifications (Pushover, Slack)

📍 Auto-detect user location

🚇 Transit-specific APIs (MBTA, MTA, BART)

📊 Historical commute trend analysis

---
🤝 Contributing

- PRs and ideas are welcome!
- This project is built to explore practical agentic AI patterns for real-world automation.