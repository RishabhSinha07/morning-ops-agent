from dotenv import load_dotenv

from prompts.system import SYSTEM_PROMPT
from tools.news import get_local_weather_news
from tools.weather import get_weather_summary

load_dotenv()

from langchain.tools import tool
from typing import Dict, Any


@tool(description="Get current weather of a city")
def get_city_weather(city: str) -> str:
    """
    Fetches current weather and advice for the given city.
    """
    result = get_weather_summary(city)  # now get_weather_summary only needs city
    if result["ok"]:
        return result["data"]
    else:
        return f"Weather unavailable: {result['error']}"

@tool(description="Get weather news for a city")
def get_city_weather_news(city: str) -> str:
    """
    Fetches local weather news for the given city.
    """
    result = get_local_weather_news(city)
    if result["ok"]:
        return result["data"]
    else:
        return f"Weather news unavailable: {result['error']}"


def get_agent():
    from langchain.agents import create_agent

    return create_agent(
        model="gpt-5-nano",
        tools=[get_city_weather, get_city_weather_news],
        system_prompt=SYSTEM_PROMPT
    )


