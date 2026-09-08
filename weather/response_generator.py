class WeatherResponseGenerator:

    def generate(self, parsed_query, weather_data):

        location = parsed_query["location"]
        intent = parsed_query["intent"]
        date = parsed_query["date"]

        daily = weather_data["daily"]

        # Find the correct forecast day
        if date == "today":
            index = 0
        elif date == "tomorrow":
            index = 1
        elif date == "day_after_tomorrow":
            index = 2
        else:
            index = 0

        temperature_max = daily["temperature_2m_max"][index]
        temperature_min = daily["temperature_2m_min"][index]
        precipitation_probability = daily["precipitation_probability_max"][index]

        # -------------------------
        # Rain query
        # -------------------------

        if intent == "rain":

            if precipitation_probability >= 70:
                rain_status = "Yes, there is a high chance of rain"

            elif precipitation_probability >= 40:
                rain_status = "There is a moderate chance of rain"

            else:
                rain_status = "There is a low chance of rain"

            return (
                f"{rain_status} in {location} {date}. "
                f"The probability of precipitation is "
                f"{precipitation_probability}%. "
                f"The temperature is expected to range from "
                f"{temperature_min}°C to {temperature_max}°C."
            )

        # -------------------------
        # Temperature query
        # -------------------------

        if intent == "temperature":

            return (
                f"In {location} {date}, the temperature is expected "
                f"to range from {temperature_min}°C to "
                f"{temperature_max}°C."
            )

        # -------------------------
        # General forecast
        # -------------------------

        return (
            f"The weather forecast for {location} {date} shows "
            f"a temperature range of {temperature_min}°C to "
            f"{temperature_max}°C, with a "
            f"{precipitation_probability}% chance of precipitation."
        )


if __name__ == "__main__":

    generator = WeatherResponseGenerator()

    parsed_query = {
        "intent": "rain",
        "location": "Hyderabad",
        "date": "tomorrow",
        "weather_parameter": "precipitation"
    }

    weather_data = {
        "daily": {
            "temperature_2m_max": [32.3, 32.2, 31.1],
            "temperature_2m_min": [24.6, 24.5, 24.1],
            "precipitation_probability_max": [60, 92, 90]
        }
    }

    response = generator.generate(
        parsed_query,
        weather_data
    )

    print(response)
