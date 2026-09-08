from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather Server")


@mcp.tool()
def get_weather(city: str) -> str:
    """Get weather for a city."""
    
    # Simple demo data
    weather = {
        "Hyderabad": "32°C, Sunny",
        "Bangalore": "25°C, Cloudy",
        "Chennai": "34°C, Sunny"
    }

    return weather.get(city, "Weather not available")



if __name__ == "__main__":
    mcp.run(transport="stdio")