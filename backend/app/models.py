from typing import Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    location: str
    language: str = "en"
    crop: Optional[str] = None
    user_id: Optional[str] = None


class WeatherData(BaseModel):
    location: str
    date: str
    temp_min_c: float
    temp_max_c: float
    rainfall_mm: float
    precipitation_probability_pct: float
    humidity_pct: float
    wind_kmph: float
    condition: str
    source: str
    confidence: float


class RiskAssessment(BaseModel):
    hazard: str
    level: str
    reason: str
    recommended_action: str


class Advisory(BaseModel):
    crop: str
    hazard: str
    recommendation: str


class ChatResponse(BaseModel):
    reply: str
    reply_language: str
    weather: WeatherData
    risk: RiskAssessment
    advisory: Optional[Advisory] = None
    sources: list[str] = []
    disclaimer: str = ""
