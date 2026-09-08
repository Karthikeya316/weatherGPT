import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "claude-sonnet-4-6")

WEATHER_PROVIDER = os.getenv("WEATHER_PROVIDER", "mock")
TRANSLATION_PROVIDER = os.getenv("TRANSLATION_PROVIDER", "stub")

SQLITE_PATH = os.getenv(
    "SQLITE_PATH",
    str(BASE_DIR / "data" / "weather_gpt.db"),
)

CHROMA_PATH = os.getenv(
    "CHROMA_PATH",
    str(BASE_DIR / "data" / "chroma"),
)

HEAVY_RAIN_MM = float(os.getenv("HEAVY_RAIN_MM", "64.5"))
VERY_HEAVY_RAIN_MM = float(os.getenv("VERY_HEAVY_RAIN_MM", "115.6"))
EXTREME_RAIN_MM = float(os.getenv("EXTREME_RAIN_MM", "204.5"))

HEATWAVE_TEMP_C = float(os.getenv("HEATWAVE_TEMP_C", "40"))
SEVERE_HEAT_TEMP_C = float(os.getenv("SEVERE_HEAT_TEMP_C", "45"))

COLDWAVE_TEMP_C = float(os.getenv("COLDWAVE_TEMP_C", "4"))

HIGH_WIND_KMPH = float(os.getenv("HIGH_WIND_KMPH", "40"))
DAMAGING_WIND_KMPH = float(os.getenv("DAMAGING_WIND_KMPH", "62"))
