import os
from tavily import TavilyClient
from tools.types import ToolResult

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
