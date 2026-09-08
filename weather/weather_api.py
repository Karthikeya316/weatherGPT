import requests


class WeatherAPI:

    def __init__(self):
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.forecast_url = "https://api.open-meteo.com/v1/forecast"

    def get_coordinates(self, location):

        params = {
            "name": location,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        response = requests.get(
            self.geocoding_url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if "results" not in data or not data["results"]:
            raise ValueError(f"Location not found: {location}")

        result = data["results"][0]

        return {
            "name": result["name"],
            "latitude": result["latitude"],
            "longitude": result["longitude"],
            "country": result.get("country", "")
        }

    def get_forecast(self, location, forecast_days=3):

        coordinates = self.get_coordinates(location)

        params = {
            "latitude": coordinates["latitude"],
            "longitude": coordinates["longitude"],
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "precipitation",
                "rain",
                "weather_code",
                "wind_speed_10m"
            ],
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_probability_max",
                "precipitation_sum",
                "rain_sum",
                "weather_code"
            ],
            "forecast_days": forecast_days,
            "timezone": "auto"
        }

        response = requests.get(
            self.forecast_url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return {
            "location": coordinates,
            "current": data.get("current"),
            "daily": data.get("daily")
        }


if __name__ == "__main__":

    weather = WeatherAPI()

    location = "Hyderabad"

    print("Getting weather for:", location)

    forecast = weather.get_forecast(location)

    print("\nLocation:")
    print(forecast["location"])

    print("\nCurrent weather:")
    print(forecast["current"])

    print("\nDaily forecast:")
    print(forecast["daily"])
