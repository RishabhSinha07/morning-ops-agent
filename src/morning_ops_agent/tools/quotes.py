import requests
from morning_ops_agent.tools.types import ToolResult

FALLBACK_QUOTE = {
    "q": "The secret of getting ahead is getting started.",
    "a": "Mark Twain",
}


def get_daily_quote() -> ToolResult:
    try:
        resp = requests.get("https://zenquotes.io/api/today", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list) and data:
            quote = data[0]
        else:
            quote = FALLBACK_QUOTE

        text = quote.get("q", FALLBACK_QUOTE["q"])
        author = quote.get("a", FALLBACK_QUOTE["a"])

        return {
            "ok": True,
            "data": f'"{text}" — {author}',
            "error": None,
        }

    except Exception:
        return {
            "ok": True,
            "data": f'"{FALLBACK_QUOTE["q"]}" — {FALLBACK_QUOTE["a"]}',
            "error": None,
        }
