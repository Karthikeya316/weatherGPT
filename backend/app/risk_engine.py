from app.config import (
    HEAVY_RAIN_MM,
    VERY_HEAVY_RAIN_MM,
    EXTREME_RAIN_MM,
    HEATWAVE_TEMP_C,
    SEVERE_HEAT_TEMP_C,
    COLDWAVE_TEMP_C,
    HIGH_WIND_KMPH,
    DAMAGING_WIND_KMPH,
)
from app.models import RiskAssessment, WeatherData


def assess_risk(weather: WeatherData) -> RiskAssessment:

    # Extreme rainfall
    if weather.rainfall_mm >= EXTREME_RAIN_MM:
        return RiskAssessment(
            hazard="extreme_rain",
            level="critical",
            reason=(
                f"Rainfall of {weather.rainfall_mm} mm "
                "is in the extreme range."
            ),
            recommended_action=(
                "Seek safe shelter and follow official "
                "emergency instructions."
            ),
        )

    # Very heavy rainfall
    if weather.rainfall_mm >= VERY_HEAVY_RAIN_MM:
        return RiskAssessment(
            hazard="very_heavy_rain",
            level="high",
            reason=(
                f"Rainfall of {weather.rainfall_mm} mm "
                "is very heavy."
            ),
            recommended_action=(
                "Avoid flood-prone areas and protect crops, "
                "livestock, and equipment."
            ),
        )

    # Heavy rainfall
    if weather.rainfall_mm >= HEAVY_RAIN_MM:
        return RiskAssessment(
            hazard="heavy_rain",
            level="moderate",
            reason=(
                f"Rainfall of {weather.rainfall_mm} mm "
                "is heavy."
            ),
            recommended_action=(
                "Monitor local conditions and avoid "
                "unnecessary travel."
            ),
        )

    # Severe heat
    if weather.temp_max_c >= SEVERE_HEAT_TEMP_C:
        return RiskAssessment(
            hazard="severe_heat",
            level="high",
            reason=(
                f"Maximum temperature is "
                f"{weather.temp_max_c}°C."
            ),
            recommended_action=(
                "Avoid prolonged heat exposure and stay hydrated."
            ),
        )

    # Heatwave
    if weather.temp_max_c >= HEATWAVE_TEMP_C:
        return RiskAssessment(
            hazard="heatwave",
            level="moderate",
            reason=(
                f"Maximum temperature is "
                f"{weather.temp_max_c}°C."
            ),
            recommended_action=(
                "Limit outdoor exposure during peak heat "
                "and stay hydrated."
            ),
        )

    # Coldwave
    if weather.temp_min_c <= COLDWAVE_TEMP_C:
        return RiskAssessment(
            hazard="coldwave",
            level="moderate",
            reason=(
                f"Minimum temperature is "
                f"{weather.temp_min_c}°C."
            ),
            recommended_action=(
                "Protect people, livestock, and sensitive "
                "crops from cold exposure."
            ),
        )

    # Damaging wind
    if weather.wind_kmph >= DAMAGING_WIND_KMPH:
        return RiskAssessment(
            hazard="damaging_wind",
            level="high",
            reason=(
                f"Wind speed is "
                f"{weather.wind_kmph} km/h."
            ),
            recommended_action=(
                "Secure loose objects and avoid exposed areas."
            ),
        )

    # High wind
    if weather.wind_kmph >= HIGH_WIND_KMPH:
        return RiskAssessment(
            hazard="high_wind",
            level="moderate",
            reason=(
                f"Wind speed is "
                f"{weather.wind_kmph} km/h."
            ),
            recommended_action=(
                "Use caution outdoors and secure vulnerable equipment."
            ),
        )

    # Normal conditions
    return RiskAssessment(
        hazard="none",
        level="low",
        reason=(
            "No major weather hazard threshold "
            "has been exceeded."
        ),
        recommended_action=(
            "Continue normal activities while monitoring "
            "the forecast."
        ),
    )
