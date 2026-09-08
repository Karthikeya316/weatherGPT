import re


class WeatherQueryParser:

    def parse(self, query):

        query_lower = query.lower().strip()

        result = {
            "intent": "current_weather",
            "location": None,
            "date": "today",
            "weather_parameter": "general"
        }

        # -------------------------
        # Detect weather parameter
        # -------------------------

        if any(word in query_lower for word in [
            "rain", "raining", "rainfall", "precipitation"
        ]):
            result["intent"] = "rain"
            result["weather_parameter"] = "precipitation"

        elif any(word in query_lower for word in [
            "temperature", "hot", "cold", "degree", "degrees"
        ]):
            result["intent"] = "temperature"
            result["weather_parameter"] = "temperature"

        elif any(word in query_lower for word in [
            "humidity", "humid"
        ]):
            result["intent"] = "humidity"
            result["weather_parameter"] = "humidity"

        elif any(word in query_lower for word in [
            "wind", "windy"
        ]):
            result["intent"] = "wind"
            result["weather_parameter"] = "wind"

        elif any(word in query_lower for word in [
            "forecast", "weather"
        ]):
            result["intent"] = "forecast"
            result["weather_parameter"] = "general"

        # -------------------------
        # Detect date
        # -------------------------

        if "day after tomorrow" in query_lower:
            result["date"] = "day_after_tomorrow"

        elif "tomorrow" in query_lower:
            result["date"] = "tomorrow"

        elif "today" in query_lower:
            result["date"] = "today"

        # -------------------------
        # Detect location
        # -------------------------

        location_patterns = [
            r"\bin\s+([a-zA-Z\s]+?)(?:\s+today|\s+tomorrow|\s+tonight|$)",
            r"\bat\s+([a-zA-Z\s]+?)(?:\s+today|\s+tomorrow|\s+tonight|$)",
            r"\bfor\s+([a-zA-Z\s]+?)(?:\s+today|\s+tomorrow|\s+tonight|$)"
        ]

        for pattern in location_patterns:

            match = re.search(pattern, query_lower)

            if match:
                location = match.group(1).strip()

                if location:
                    result["location"] = location.title()
                    break

        return result


if __name__ == "__main__":

    parser = WeatherQueryParser()

    query = "is it going to rain in hyderabad tomorrow"

    result = parser.parse(query)

    print("Query:")
    print(query)

    print("\nParsed result:")
    print(result)
