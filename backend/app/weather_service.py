from datetime import date, timedelta

import requests

from app.models import WeatherData


HYDERABAD_LAT = 17.3850
HYDERABAD_LON = 78.4867


def _get_coordinates(location: str):

    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name": location,
            "count": 1,
            "language": "en",
            "format": "json"
        },
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    results = data.get("results", [])

    if not results:
        raise ValueError(
            f"Could not find location: {location}"
        )

    return (
        results[0]["latitude"],
        results[0]["longitude"]
    )


def _weather_code_to_condition(code: int) -> str:

    if code == 0:
        return "Clear"

    if code in [1, 2]:
        return "Partly Cloudy"

    if code == 3:
        return "Cloudy"

    if code in [45, 48]:
        return "Foggy"

    if code in [51, 53, 55, 56, 57]:
        return "Drizzle"

    if code in [61, 63, 65, 66, 67]:
        return "Rain"

    if code in [71, 73, 75, 77]:
        return "Snow"

    if code in [80, 81, 82]:
        return "Rain Showers"

    if code in [85, 86]:
        return "Snow Showers"

    if code in [95, 96, 99]:
        return "Thunderstorm"

    return "Unknown"


def get_forecast(location: str, days: int = 3):

    latitude, longitude = _get_coordinates(location)

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,

            "daily": ",".join([
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "rain_sum",
                "precipitation_probability_max",
                "weather_code",
                "wind_speed_10m_max",
                "relative_humidity_2m_mean",
            ]),

            "timezone": "auto",

            "forecast_days": days,
        },

        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    daily = data["daily"]

    results = []

    for i, day in enumerate(daily["time"]):

        humidity = daily.get(
            "relative_humidity_2m_mean",
            [0] * len(daily["time"])
        )[i]

        weather = WeatherData(

            location=location,

            date=day,

            temp_min_c=float(
                daily["temperature_2m_min"][i]
            ),

            temp_max_c=float(
                daily["temperature_2m_max"][i]
            ),

            rainfall_mm=float(
   		 daily["precipitation_sum"][i]
	    ),

	    precipitation_probability_pct=float(
   		 daily["precipitation_probability_max"][i]
	    ),

            humidity_pct=float(humidity),

            wind_kmph=float(
                daily["wind_speed_10m_max"][i]
            ),

            condition=_weather_code_to_condition(
                int(daily["weather_code"][i])
            ),

            source="Open-Meteo",

            confidence=0.90,
        )

        results.append(weather)

    return results


def get_current_weather(
    location: str,
    target_date: str = "today"
) -> WeatherData:

    forecasts = get_forecast(
        location,
        days=3
    )

    today = date.today()

    if target_date == "tomorrow":

        desired_date = today + timedelta(days=1)

    elif target_date == "day_after_tomorrow":

        desired_date = today + timedelta(days=2)

    else:

        desired_date = today

    desired_date_str = desired_date.isoformat()

    for weather in forecasts:

        if weather.date == desired_date_str:

            return weather

    return forecasts[0]
