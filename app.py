from translation.indic_to_english import IndicToEnglishTranslator
from translation.english_to_indic import EnglishToIndicTranslator
from nlp.query_parser import WeatherQueryParser
from nlp.language_detector import LanguageDetector
from translation.languages import get_language_code
from weather.weather_api import WeatherAPI
from weather.response_generator import WeatherResponseGenerator


class WeatherGPT:

    def __init__(self):

        print("Initializing Weather GPT...\n")

        self.language_detector = LanguageDetector()

        self.indic_to_english = IndicToEnglishTranslator()
        self.english_to_indic = EnglishToIndicTranslator()

        self.parser = WeatherQueryParser()
        self.weather_api = WeatherAPI()
        self.response_generator = WeatherResponseGenerator()

        print("\nWeather GPT initialized successfully!\n")

    def process(self, user_text):

        print("=" * 60)
        print("USER INPUT")
        print("=" * 60)
        print(user_text)

        # --------------------------------
        # 1. Detect language
        # --------------------------------

        detected_language = self.language_detector.detect(user_text)

        print("\nDetected language:")
        print(detected_language)

        language_code = get_language_code(detected_language)

        print("Language code:")
        print(language_code)

        # --------------------------------
        # 2. Convert query to English
        # --------------------------------

        if detected_language == "english":

            english_query = user_text

        else:

            english_query = self.indic_to_english.translate(
                user_text,
                language_code
            )

        print("\nEnglish translation:")
        print(english_query)

        # --------------------------------
        # 3. Understand the query
        # --------------------------------

        parsed_query = self.parser.parse(english_query)

        print("\nParsed query:")
        print(parsed_query)

        # --------------------------------
        # 4. Get weather data
        # --------------------------------

        location = parsed_query["location"]

        if not location:
            return "I could not determine the location."

        weather_data = self.weather_api.get_forecast(
            location
        )

        print("\nWeather data retrieved successfully.")

        # --------------------------------
        # 5. Generate English response
        # --------------------------------

        english_response = self.response_generator.generate(
            parsed_query,
            weather_data
        )

        print("\nEnglish response:")
        print(english_response)

        # --------------------------------
        # 6. Translate response
        # --------------------------------

        if detected_language == "english":

            final_response = english_response

        else:

            final_response = self.english_to_indic.translate(
                english_response,
                language_code
            )

        print("\nFinal response:")
        print(final_response)

        return final_response


if __name__ == "__main__":

    app = WeatherGPT()

    while True:

        print("\n")
        user_question = input("Ask your weather question (or type 'exit'): ")

        if user_question.lower().strip() == "exit":
            print("Exiting Weather GPT.")
            break

        try:

            response = app.process(user_question)

            print("\n")
            print("=" * 60)
            print("WEATHER GPT ANSWER")
            print("=" * 60)
            print(response)

        except Exception as e:

            print("\nError:")
            print(e)
