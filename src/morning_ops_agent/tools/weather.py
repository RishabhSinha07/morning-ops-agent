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

        # Fetch forecast with hourly and daily data
        forecast = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
                "hourly": "temperature_2m,apparent_temperature,weathercode",
                "daily": "sunrise,sunset,uv_index_max",
                "timezone": "auto",
                "forecast_days": 1,
            },
        ).json()

        current = forecast["current_weather"]
        hourly = forecast["hourly"]
        daily = forecast["daily"]

        # Fetch air quality
        aqi_val = "N/A"
        try:
            aqi_resp = requests.get(
                "https://air-quality-api.open-meteo.com/v1/air-quality",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "us_aqi",
                    "timezone": "auto",
                },
            ).json()
            aqi_val = aqi_resp.get("current", {}).get("us_aqi", "N/A")
        except Exception:
            pass

        # Build hourly windows — summarise each as a single temp range
        def hourly_window(label, start_hour, end_hour):
            temps, feels = [], []
            for h in range(start_hour, end_hour + 1):
                if h < len(hourly["temperature_2m"]):
                    temps.append(hourly["temperature_2m"][h])
                    feels.append(hourly["apparent_temperature"][h])
            if not temps:
                return f"{label}: N/A"
            t_lo, t_hi = min(temps), max(temps)
            f_lo, f_hi = min(feels), max(feels)
            t_range = f"{t_lo}–{t_hi}°C" if t_lo != t_hi else f"{t_lo}°C"
            f_range = f"{f_lo}–{f_hi}°C" if f_lo != f_hi else f"{f_lo}°C"
            return f"{label}: {t_range} (feels {f_range})"

        morning = hourly_window("Morning (7–9 AM)", 7, 9)
        midday = hourly_window("Midday (11 AM–1 PM)", 11, 13)
        evening = hourly_window("Evening (4–6 PM)", 16, 18)

        # Find current feels-like from hourly data
        current_hour = int(current["time"].split("T")[1].split(":")[0])
        feels_like = current["temperature"]
        if current_hour < len(hourly["apparent_temperature"]):
            feels_like = hourly["apparent_temperature"][current_hour]

        sunrise = daily["sunrise"][0].split("T")[1] if daily.get("sunrise") else "N/A"
        sunset = daily["sunset"][0].split("T")[1] if daily.get("sunset") else "N/A"
        uv_max = daily.get("uv_index_max", [None])[0]
        uv_str = f"{uv_max}" if uv_max is not None else "N/A"

        summary = (
            f"Current: {current['temperature']}°C (feels like {feels_like}°C)\n"
            f"Wind: {current['windspeed']} km/h\n"
            f"Sunrise: {sunrise} | Sunset: {sunset}\n"
            f"UV Index (max): {uv_str}\n"
            f"Air Quality (US AQI): {aqi_val}\n"
            f"\nHourly Breakdown:\n{morning}\n{midday}\n{evening}"
        )

        return {
            "ok": True,
            "data": summary,
            "error": None
        }

    except Exception as e:
        return {"ok": False, "data": None, "error": str(e)}
