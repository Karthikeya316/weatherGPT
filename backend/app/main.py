from fastapi import FastAPI, HTTPException

from app.models import ChatRequest, ChatResponse
from app.weather_service import (
    get_current_weather,
    get_forecast,
)
from app.risk_engine import assess_risk
from app.database import (
    init_db,
    get_advisory,
    list_known_crops,
    log_query,
    get_query_logs,
)
from app.rag_engine import retrieve_context
from app.llm_service import generate_response
from app.translation_service import (
    translation_service,
    detect_language,
)

# Import NLP parser from project root
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from nlp.query_parser import WeatherQueryParser


app = FastAPI(
    title="WeatherGPT",
    description="Multilingual AI weather assistant",
    version="1.0.0",
)


# ---------------------------------------------------------
# STARTUP
# ---------------------------------------------------------

@app.on_event("startup")
def startup():
    init_db()


# ---------------------------------------------------------
# BASIC ENDPOINTS
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "name": "WeatherGPT",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


# ---------------------------------------------------------
# LANGUAGE ENDPOINT
# ---------------------------------------------------------

@app.get("/languages")
def languages():
    return {
        "languages": {
            "en": "English",
            "hi": "Hindi",
            "mr": "Marathi",
            "ta": "Tamil",
            "te": "Telugu",
            "bn": "Bengali",
            "gu": "Gujarati",
            "kn": "Kannada",
            "pa": "Punjabi",
            "ml": "Malayalam",
            "ur": "Urdu",
            "or": "Odia",
        }
    }


# ---------------------------------------------------------
# CROP ENDPOINTS
# ---------------------------------------------------------

@app.get("/crops")
def crops():
    return {
        "crops": list_known_crops(),
    }


@app.get("/advisory/{crop}/{hazard}")
def advisory(crop: str, hazard: str):

    result = get_advisory(
        crop,
        hazard,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No advisory found for crop '{crop}' "
                f"and hazard '{hazard}'."
            ),
        )

    return result


# ---------------------------------------------------------
# LOGGING ENDPOINT
# ---------------------------------------------------------

@app.get("/logs")
def logs(limit: int = 50):

    if limit < 1 or limit > 500:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 500.",
        )

    return {
        "logs": get_query_logs(limit),
    }


# ---------------------------------------------------------
# FORECAST ENDPOINT
# ---------------------------------------------------------

@app.get("/forecast/{location}")
def forecast(
    location: str,
    days: int = 3,
):

    if days < 1 or days > 7:
        raise HTTPException(
            status_code=400,
            detail="Days must be between 1 and 7.",
        )

    try:
        return get_forecast(
            location,
            days,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Weather forecast failed: {str(e)}",
        )


# ---------------------------------------------------------
# ALERT ENDPOINT
# ---------------------------------------------------------

@app.get("/alert/{location}")
def alert(location: str):

    try:
        weather = get_current_weather(
            location
        )

        risk = assess_risk(
            weather
        )

        return {
            "location": location,
            "risk": risk,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Alert generation failed: {str(e)}",
        )


# ---------------------------------------------------------
# CHAT ENDPOINT
# ---------------------------------------------------------

@app.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):

    # -----------------------------------------------------
    # 1. Detect language
    # -----------------------------------------------------

    language = request.language

    if not language or language == "auto":
        language = detect_language(
            request.message
        )

    language = language.lower().strip()


    # -----------------------------------------------------
    # 2. Translate user query to English
    # -----------------------------------------------------

    try:

        english_query = (
            translation_service.translate_to_english(
                request.message,
                language,
            )
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Input translation failed: {str(e)}"
            ),
        )


    # -----------------------------------------------------
    # 3. Parse weather query
    # -----------------------------------------------------

    parser = WeatherQueryParser()

    parsed_query = parser.parse(
        english_query
    )

    target_date = parsed_query[
        "date"
    ]


    # -----------------------------------------------------
    # 4. Get weather for requested date
    # -----------------------------------------------------

    try:

        weather = get_current_weather(
            request.location,
            target_date,
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Weather data retrieval failed: {str(e)}"
            ),
        )


    # -----------------------------------------------------
    # 5. Assess weather risk
    # -----------------------------------------------------

    risk = assess_risk(
        weather
    )


    # -----------------------------------------------------
    # 6. Get crop advisory
    # -----------------------------------------------------

    advisory_result = None

    if request.crop:

        advisory_result = get_advisory(
            request.crop,
            risk.hazard,
        )


    # -----------------------------------------------------
    # 7. Retrieve RAG knowledge
    # -----------------------------------------------------

    rag_query = (
        f"{english_query} "
        f"{risk.hazard}"
    )

    rag_context = retrieve_context(
        rag_query,
        n_results=3,
    )


    # -----------------------------------------------------
    # 8. Generate grounded LLM response
    # -----------------------------------------------------

    try:

        english_reply = generate_response(
            english_query,
            weather,
            risk,
            advisory_result,
            rag_context,
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                f"AI response generation failed: {str(e)}"
            ),
        )


    # -----------------------------------------------------
    # 9. Translate main response
    # -----------------------------------------------------

    try:

        final_reply = (
            translation_service.translate_from_english(
                english_reply,
                language,
            )
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Output translation failed: {str(e)}"
            ),
        )


    # -----------------------------------------------------
    # 10. Translate structured output
    # -----------------------------------------------------

    localized_weather = weather
    localized_risk = risk
    localized_advisory = advisory_result

    if language != "en":

        try:

            # Translate weather condition
            localized_condition = (
                translation_service.translate_from_english(
                    weather.condition,
                    language,
                )
            )

            localized_weather = weather.model_copy(
                update={
                    "condition": localized_condition,
                }
            )


            # Translate risk reason and action
            localized_risk = risk.model_copy(
                update={
                    "reason": (
                        translation_service.translate_from_english(
                            risk.reason,
                            language,
                        )
                    ),
                    "recommended_action": (
                        translation_service.translate_from_english(
                            risk.recommended_action,
                            language,
                        )
                    ),
                }
            )


            # Translate crop recommendation
            if advisory_result:

                localized_advisory = (
                    advisory_result.model_copy(
                        update={
                            "recommendation": (
                                translation_service.translate_from_english(
                                    advisory_result.recommendation,
                                    language,
                                )
                            ),
                        }
                    )
                )

        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=(
                    f"Structured output translation failed: {str(e)}"
                ),
            )


    # -----------------------------------------------------
    # 11. Sources
    # -----------------------------------------------------

    sources = [
        weather.source,
        "WeatherGPT Risk Engine",
        "WeatherGPT ChromaDB Knowledge Base",
    ]

    if advisory_result:

        sources.append(
            "WeatherGPT Crop Advisory Database"
        )


    # -----------------------------------------------------
    # 12. Translate disclaimer
    # -----------------------------------------------------

    disclaimer = (
        "Weather information is provided for "
        "informational purposes. Follow official "
        "weather and emergency advisories when applicable."
    )

    if language != "en":

        try:

            disclaimer = (
                translation_service.translate_from_english(
                    disclaimer,
                    language,
                )
            )

        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=(
                    f"Disclaimer translation failed: {str(e)}"
                ),
            )


    # -----------------------------------------------------
    # 13. Create response
    # -----------------------------------------------------

    response = ChatResponse(
        reply=final_reply,
        reply_language=language,
        weather=localized_weather,
        risk=localized_risk,
        advisory=localized_advisory,
        sources=sources,
        disclaimer=disclaimer,
    )


    # -----------------------------------------------------
    # 14. Log interaction
    # -----------------------------------------------------

    try:

        log_query(
            message=request.message,
            language=language,
            location=request.location,
            crop=request.crop,
            intent=parsed_query["intent"],
            response=final_reply,
            user_id=request.user_id,
        )

    except Exception as e:

        # Logging failure should not prevent
        # the user from receiving the weather response.
        print(
            f"Warning: failed to log query: {e}"
        )


    # -----------------------------------------------------
    # 15. Return response
    # -----------------------------------------------------

    return response
