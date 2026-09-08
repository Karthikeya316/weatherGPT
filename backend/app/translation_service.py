from pathlib import Path
import sys

# Allow the backend to import the translation modules
# located in the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from translation.indic_to_english import IndicToEnglishTranslator
from translation.english_to_indic import EnglishToIndicTranslator


LANGUAGE_CODES = {
    "en": "eng_Latn",
    "hi": "hin_Deva",
    "mr": "mar_Deva",
    "ta": "tam_Taml",
    "te": "tel_Telu",
    "bn": "ben_Beng",
    "gu": "guj_Gujr",
    "kn": "kan_Knda",
    "pa": "pan_Guru",
    "ml": "mal_Mlym",
    "ur": "urd_Arab",
    "or": "ory_Orya",
}


class TranslationService:

    def __init__(self):
        self.indic_to_english = None
        self.english_to_indic = None

    def _load_indic_to_english(self):
        if self.indic_to_english is None:
            print("Loading Indic → English translator...")
            self.indic_to_english = IndicToEnglishTranslator()

    def _load_english_to_indic(self):
        if self.english_to_indic is None:
            print("Loading English → Indic translator...")
            self.english_to_indic = EnglishToIndicTranslator()

    def translate_to_english(self, text, language):
        language = language.lower().strip()

        if language == "en":
            return text

        if language not in LANGUAGE_CODES:
            raise ValueError(f"Unsupported language: {language}")

        self._load_indic_to_english()

        return self.indic_to_english.translate(
            text,
            LANGUAGE_CODES[language]
        )

    def translate_from_english(self, text, language):
        language = language.lower().strip()

        if language == "en":
            return text

        if language not in LANGUAGE_CODES:
            raise ValueError(f"Unsupported language: {language}")

        self._load_english_to_indic()

        return self.english_to_indic.translate(
            text,
            LANGUAGE_CODES[language]
        )

    def translate(self, text, source_language, target_language):
        source_language = source_language.lower().strip()
        target_language = target_language.lower().strip()

        if source_language == target_language:
            return text

        if source_language == "en":
            return self.translate_from_english(
                text,
                target_language
            )

        if target_language == "en":
            return self.translate_to_english(
                text,
                source_language
            )

        # Indic → Indic:
        # First translate to English, then English → target.
        english_text = self.translate_to_english(
            text,
            source_language
        )

        return self.translate_from_english(
            english_text,
            target_language
        )


# Singleton so the large translation models are loaded
# only once and reused for future requests.
translation_service = TranslationService()


def detect_language(text):
    """
    Basic script-based language detection.

    Returns the backend language code.
    """

    import re

    patterns = {
        "hi": r"[\u0900-\u097F]",
        "ta": r"[\u0B80-\u0BFF]",
        "te": r"[\u0C00-\u0C7F]",
        "kn": r"[\u0C80-\u0CFF]",
        "ml": r"[\u0D00-\u0D7F]",
        "bn": r"[\u0980-\u09FF]",
        "gu": r"[\u0A80-\u0AFF]",
        "pa": r"[\u0A00-\u0A7F]",
        "or": r"[\u0B00-\u0B7F]",
        "ur": r"[\u0600-\u06FF]",
    }

    for language, pattern in patterns.items():
        if re.search(pattern, text):
            return language

    return "en"
