import requests
from requests.exceptions import RequestException, Timeout
from tools.types import ToolResult

def get_location(timeout: int = 5) -> ToolResult:
    try:
        response = requests.get(
            "https://ipinfo.io/json",
            timeout=timeout
        )
        response.raise_for_status()
        data = response.json()

        return {
            "ok": True,
            "data": {
                "city": data.get("city"),
                "lat": data.get("latitude"),
                "lon": data.get("longitude"),
                "timezone": data.get("timezone"),
            },
            "error": None
        }

    except Timeout:
        return {
            "ok": False,
            "data": None,
            "error": "Location request timed out"
        }

    except RequestException as e:
        return {
            "ok": False,
            "data": None,
            "error": f"Location request failed: {str(e)}"
        }

    except ValueError:
        return {
            "ok": False,
            "data": None,
            "error": "Invalid JSON from location service"
        }
