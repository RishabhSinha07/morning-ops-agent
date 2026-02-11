from dotenv import load_dotenv

from morning_ops_agent.prompts.system import SYSTEM_PROMPT
from morning_ops_agent.tools.news import get_local_weather_news
from morning_ops_agent.tools.weather import get_weather_summary

load_dotenv()

from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool


@tool(description="Get current weather of a city")
def get_city_weather(city: str) -> str:
    """
    Fetches current weather and advice for the given city.
    """
    result = get_weather_summary(city)
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
    llm = init_chat_model("amazon.nova-pro-v1:0", model_provider="bedrock_converse")

    return create_react_agent(
        model=llm,
        tools=[get_city_weather, get_city_weather_news],
        prompt=SYSTEM_PROMPT,
    )
