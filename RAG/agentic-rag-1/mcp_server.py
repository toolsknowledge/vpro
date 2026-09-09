import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather Server")

@mcp.tool()
def get_weather(city: str) -> str:          # city - Bangalore,Hyderabad,Chennai,......
    """Get current weather for a city."""

    # City name -> latitude/longitude
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1}
    ).json()

    if "results" not in geo:
        return f"City '{city}' not found"

    loc = geo["results"][0]
    lat, lon = loc["latitude"], loc["longitude"]

    # Get weather
    data = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,weather_code",
            "timezone": "auto"
        }
    ).json()["current"]

    return f"{city}: {data['temperature_2m']}°C, weather code {data['weather_code']}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
