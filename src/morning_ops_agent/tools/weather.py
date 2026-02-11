import requests
from typing import Dict, Any

def get_weather_summary(city: str) -> Dict[str, Any]:
    try:
        geo = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": city, "format": "json", "limit": 1},
            headers={"User-Agent": "morning-ops-agent/0.1"},
        ).json()

        if not geo:
            return {
                "ok": False,
                "data": None,
                "error": "City not found"
            }

        lat = geo[0]["lat"]
        lon = geo[0]["lon"]

        weather = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current_weather": True}
        ).json()["current_weather"]

        summary = f"Temperature: {weather['temperature']}°C\nWind: {weather['windspeed']} km/h"
        return {
            "ok": True,
            "data": summary,
            "error": None
        }

    except Exception as e:
        return {"ok": False, "data": None, "error": str(e)}
