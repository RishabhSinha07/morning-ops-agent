import requests
from typing import Dict, Any

def get_weather_summary(city: str) -> Dict[str, Any]:
    try:
        geoLocation = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1").json()
        
        if not geoLocation.get("results"):
            return {
                "ok": False,
                "data": None,
                "error": "City not found"
            }
        
        lat = geoLocation["results"][0]["latitude"]
        lon = geoLocation["results"][0]["longitude"]

        weather = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current_weather": True}
        ).json()["current_weather"]


        summary = f"Temperature: {weather["temperature"]}°C\nWind: {weather["windspeed"]} km"
        return {
            "ok": True,
            "data": summary,
            "error": None
        }

    except Exception as e:
        return {"ok": False, "data": None, "error": str(e)}
