import requests
from typing import Dict, Any

def get_weather_summary(city: str) -> Dict[str, Any]:
    try:
        geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1").json()
        if not geo.get("results"):
            return {"ok": False, "data": None, "error": "City not found"}
        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

        weather = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current_weather": True}
        ).json()["current_weather"]

        temp = weather["temperature"]
        wind = weather["windspeed"]

        advice = []
        if temp < 5:
            advice.append("Wear a heavy jacket 🧥")
        elif temp < 15:
            advice.append("Light jacket recommended")
        else:
            advice.append("T-shirt weather 😎")
        if wind > 25:
            advice.append("Windy — secure loose items")

        summary = f"Temperature: {temp}°C\nWind: {wind} km/h\nAdvice: {', '.join(advice)}"
        return {"ok": True, "data": summary, "error": None}

    except Exception as e:
        return {"ok": False, "data": None, "error": str(e)}
