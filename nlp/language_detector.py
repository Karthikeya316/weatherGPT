import re


class LanguageDetector:

    def __init__(self):

        self.language_patterns = {
            "hindi": r"[\u0900-\u097F]",
            "marathi": r"[\u0900-\u097F]",
            "bengali": r"[\u0980-\u09FF]",
            "punjabi": r"[\u0A00-\u0A7F]",
            "gujarati": r"[\u0A80-\u0AFF]",
            "odia": r"[\u0B00-\u0B7F]",
            "tamil": r"[\u0B80-\u0BFF]",
            "telugu": r"[\u0C00-\u0C7F]",
            "kannada": r"[\u0C80-\u0CFF]",
            "malayalam": r"[\u0D00-\u0D7F]",
            "urdu": r"[\u0600-\u06FF]"
        }

    def detect(self, text):

        # Remove spaces, numbers and punctuation
        cleaned_text = re.sub(r"[\s\d\W_]+", "", text)

        if not cleaned_text:
            return "english"

        # Count characters belonging to each script
        scores = {}

        for language, pattern in self.language_patterns.items():

            matches = re.findall(pattern, cleaned_text)

            scores[language] = len(matches)

        # Find language with the highest score
        detected_language = max(
            scores,
            key=scores.get
        )

        # If no Indic script was detected, assume English
        if scores[detected_language] == 0:
            return "english"

        # Devanagari can be Hindi or Marathi.
        # For now, default to Hindi.
        if detected_language == "marathi":
            return "hindi"

        return detected_language


if __name__ == "__main__":

    detector = LanguageDetector()

    test_sentences = [
        "రేపు హైదరాబాద్‌లో వర్షం పడుతుందా?",
        "क्या कल हैदराबाद में बारिश होगी?",
        "நாளை சென்னையில் மழை பெய்யுமா?",
        "ನಾಳೆ ಬೆಂಗಳೂರಿನಲ್ಲಿ ಮಳೆ ಬೀಳುತ್ತದೆಯೇ?",
        "Will it rain in Hyderabad tomorrow?"
    ]

    for sentence in test_sentences:

        language = detector.detect(sentence)

        print(f"Text: {sentence}")
        print(f"Detected language: {language}")
        print()
