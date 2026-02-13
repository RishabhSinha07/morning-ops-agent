import os
from tavily import TavilyClient
from morning_ops_agent.tools.types import ToolResult

def get_local_weather_news(city: str) -> ToolResult:
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise RuntimeError("TAVILY_API_KEY not set")

        client = TavilyClient(api_key=api_key)

        query = (
            f"weather alerts warnings advisories severe weather "
            f"flooding snow storm affecting traffic or commute in {city} today"
        )

        result = client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_answer=True
        )

        # If Tavily gives a direct answer, prefer it
        if result.get("answer"):
            return {
                "ok": True,
                "data": result["answer"].strip(),
                "error": None
            }

        results = result.get("results", [])
        if not results:
            return {
                "ok": True,
                "data": "No local weather alerts affecting commute today.",
                "error": None
            }

        summaries = []
        for r in results:
            title = r.get("title")
            if title:
                summaries.append(f"- {title}")

        return {
            "ok": True,
            "data": "\n".join(summaries[:3]),
            "error": None
        }

    except Exception as e:
        return {
            "ok": False,
            "data": None,
            "error": f"Tavily weather news search failed: {str(e)}"
        }


def get_news_headlines(city: str) -> ToolResult:
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise RuntimeError("TAVILY_API_KEY not set")

        client = TavilyClient(api_key=api_key)

        # Local news — top 2
        local_result = client.search(
            query=f"top news headlines {city} today",
            search_depth="basic",
            max_results=3,
        )
        local_items = local_result.get("results", [])[:2]

        # National news — top 1
        national_result = client.search(
            query="top US news headlines today",
            search_depth="basic",
            max_results=2,
        )
        national_items = national_result.get("results", [])[:1]

        # AI / Tech news — top 1
        tech_result = client.search(
            query="top AI artificial intelligence tech news today",
            search_depth="basic",
            max_results=2,
        )
        tech_items = tech_result.get("results", [])[:1]

        headlines = []
        for item in local_items + national_items + tech_items:
            title = item.get("title", "").strip()
            snippet = (item.get("content") or "").strip()
            url = item.get("url", "").strip()
            # Truncate long snippets
            if len(snippet) > 200:
                snippet = snippet[:197] + "..."
            if title:
                line = f"- **{title}**: {snippet}"
                if url:
                    line += f" [Read more]({url})"
                headlines.append(line)

        if not headlines:
            return {
                "ok": True,
                "data": "No notable news headlines found today.",
                "error": None,
            }

        return {
            "ok": True,
            "data": "\n".join(headlines),
            "error": None,
        }

    except Exception as e:
        return {
            "ok": False,
            "data": None,
            "error": f"News headlines search failed: {str(e)}",
        }
