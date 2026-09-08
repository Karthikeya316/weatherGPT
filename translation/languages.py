LANGUAGE_CODES = {
    "english": "eng_Latn",
    "hindi": "hin_Deva",
    "telugu": "tel_Telu",
    "tamil": "tam_Taml",
    "kannada": "kan_Knda",
    "malayalam": "mal_Mlym",
    "marathi": "mar_Deva",
    "bengali": "ben_Beng",
    "gujarati": "guj_Gujr",
    "punjabi": "pan_Guru",
    "urdu": "urd_Arab",
    "odia": "ory_Orya",
}


def get_language_code(language):
    language = language.lower().strip()

    if language not in LANGUAGE_CODES:
        raise ValueError(f"Unsupported language: {language}")

    return LANGUAGE_CODES[language]
