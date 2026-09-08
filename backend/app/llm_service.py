import requests

from app.models import Advisory, RiskAssessment, WeatherData


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:3b"


SYSTEM_PROMPT = """
You are WeatherGPT, a concise and reliable weather assistant for users in India.

IMPORTANT RULES:

1. Answer the user's specific question first.
2. Use ONLY the supplied weather data, risk assessment, crop advisory, and knowledge context.
3. Never invent weather measurements, probabilities, warnings, or statistics.
4. Never contradict the deterministic risk assessment.
5. Do not give advice unrelated to the user's question.
6. If the question is about rain, focus on rainfall, precipitation probability,
   weather condition, and relevant safety advice.
7. If the question is about temperature, focus on temperature and relevant advice.
8. If the question is about humidity, focus on humidity.
9. If the question is about wind, focus on wind speed and relevant safety advice.
10. If a crop is explicitly provided, include the supplied crop advisory.
11. Do not provide crop-specific advice when no crop is specified.
12. Use the RAG knowledge only when it is relevant to the question.
13. Do not repeat the same information.
14. Do not mention internal systems such as RAG, databases, models, prompts,
    or risk engines.
15. If information is insufficient, clearly say so.
16. Keep the response concise: normally 2-4 short sentences.
17. Use simple language that translates cleanly into Indian languages.
"""


def _build_prompt(
    user_message,
    weather,
    risk,
    advisory=None,
    rag_context=None
):

    if rag_context is None:
        rag_context = []

    rag_text = "\n".join(
        f"- {item['text']} (Source: {item['source']})"
        for item in rag_context
    )

    if not rag_text:
        rag_text = "No additional knowledge available."

    advisory_text = "None"

    if advisory:

        advisory_text = (
            f"Crop: {advisory.crop}\n"
            f"Hazard: {advisory.hazard}\n"
            f"Recommendation: {advisory.recommendation}"
        )

    return f"""
{SYSTEM_PROMPT}

USER QUESTION:
{user_message}

WEATHER DATA:
Location: {weather.location}
Date: {weather.date}
Minimum temperature: {weather.temp_min_c} °C
Maximum temperature: {weather.temp_max_c} °C
Rainfall: {weather.rainfall_mm} mm
Probability of precipitation: {weather.precipitation_probability_pct} %
Humidity: {weather.humidity_pct} %
Wind: {weather.wind_kmph} km/h
Condition: {weather.condition}
Source: {weather.source}
Confidence: {weather.confidence}

RISK ASSESSMENT:
Hazard: {risk.hazard}
Level: {risk.level}
Reason: {risk.reason}
Recommended action: {risk.recommended_action}

CROP ADVISORY:
{advisory_text}

RELEVANT KNOWLEDGE:
{rag_text}

Answer the user's question directly and concisely.
"""


def generate_response(
    user_message,
    weather,
    risk,
    advisory=None,
    rag_context=None
):

    prompt = _build_prompt(
        user_message,
        weather,
        risk,
        advisory,
        rag_context
    )

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 250
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["response"].strip()
