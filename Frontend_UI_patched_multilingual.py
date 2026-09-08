"""
WeatherGPT — multilingual weather dashboard and rule-based weather assistant.

Features:
- Open-Meteo geocoding and live weather data
- Current conditions + 7-day forecast
- Celsius/Fahrenheit display
- English, Hindi, Telugu, Tamil, Kannada and Malayalam UI
- Weather-aware chat responses
- Optional voice recording input when supported by Streamlit

Run:
    streamlit run Frontend_UI_patched.py
"""

from datetime import datetime
from html import escape

import requests
import streamlit as st


# =============================================================
# PAGE CONFIG — must be the first Streamlit call, and only once
# =============================================================

st.set_page_config(
    page_title="WeatherGPT",
    page_icon="🌤️",
    layout="wide",
)


# =============================================================
# UI TRANSLATIONS
# =============================================================

LANGUAGES = {
    "English": {
        "search_location": "📍 Search location",
        "temperature": "🌡️ Temperature",
        "celsius": "Celsius (°C)",
        "fahrenheit": "Fahrenheit (°F)",
        "current_weather": "CURRENT WEATHER",
        "feels_like": "Feels like",
        "todays_high": "Today's High",
        "todays_low": "Today's Low",
        "weather_details": "📊 Weather Details",
        "humidity": "💧 Humidity",
        "wind": "💨 Wind",
        "rain": "🌧️ Rain",
        "pressure": "🔵 Pressure",
        "forecast": "📅 7-Day Forecast",
        "today": "Today",
        "assistant": "🤖 WeatherGPT",
        "assistant_desc": "Ask me anything about the weather.",
        "chat_placeholder": "Ask about today's weather...",
        "voice_received": "🎙️ Voice recording received. Connect a speech-to-text API to convert this recording into a weather question.",
        "city_not_found": "❌ City not found. Please enter a valid city.",
        "weather_error": "❌ Unable to get weather data. Please try again.",
        "carry_umbrella": "☔ Yes, carry an umbrella.",
        "no_umbrella": "🌤️ You probably don't need an umbrella.",
        "rain_chance": "The chance of rain is",
        "hot": "🔥 It is going to be quite hot today. Stay hydrated and avoid prolonged exposure to the heat.",
        "warm": "🌡️ It will be warm today. Keep yourself hydrated.",
        "comfortable": "🌤️ The temperature looks fairly comfortable today.",
        "good_outdoor": "🚶 Good conditions for outdoor activities.",
        "outdoor_warning": "⚠️ Outdoor plans may need some preparation.",
        "weather_update": "🌤️ Weather Update",
        "condition": "Condition",
        "main_title": "WeatherGPT 🌤️",
        "main_subtitle": "Your intelligent weather companion",
        "footer": "WeatherGPT • AI-powered weather assistant • Hackathon Prototype",
        "enter_city": "Enter city...",
        "language": "🌐 Language",
        "loading_weather": "Loading weather...",
        "hackathon": "Hackathon Prototype",
        "weather_ai": "Weather + AI",
        "unknown": "Unknown",
    },
    "Hindi": {
        "search_location": "📍 स्थान खोजें",
        "temperature": "🌡️ तापमान",
        "celsius": "सेल्सियस (°C)",
        "fahrenheit": "फ़ारेनहाइट (°F)",
        "current_weather": "वर्तमान मौसम",
        "feels_like": "महसूस होने वाला तापमान",
        "todays_high": "आज का अधिकतम",
        "todays_low": "आज का न्यूनतम",
        "weather_details": "📊 मौसम की जानकारी",
        "humidity": "💧 नमी",
        "wind": "💨 हवा",
        "rain": "🌧️ बारिश",
        "pressure": "🔵 वायुदाब",
        "forecast": "📅 7-दिन का मौसम पूर्वानुमान",
        "today": "आज",
        "assistant": "🤖 WeatherGPT",
        "assistant_desc": "मौसम के बारे में कुछ भी पूछें।",
        "chat_placeholder": "आज के मौसम के बारे में पूछें...",
        "voice_received": "🎙️ आवाज़ की रिकॉर्डिंग प्राप्त हुई। इसे मौसम के प्रश्न में बदलने के लिए Speech-to-Text API जोड़ें।",
        "city_not_found": "❌ शहर नहीं मिला। कृपया सही शहर दर्ज करें।",
        "weather_error": "❌ मौसम की जानकारी प्राप्त नहीं हो सकी। कृपया पुनः प्रयास करें।",
        "carry_umbrella": "☔ हाँ, छाता साथ ले जाना अच्छा रहेगा।",
        "no_umbrella": "🌤️ शायद आपको छाते की आवश्यकता नहीं होगी।",
        "rain_chance": "बारिश की संभावना",
        "hot": "🔥 आज काफी गर्मी रहेगी। पर्याप्त पानी पिएँ और लंबे समय तक धूप में रहने से बचें।",
        "warm": "🌡️ आज मौसम गर्म रहेगा। पर्याप्त पानी पीते रहें।",
        "comfortable": "🌤️ आज तापमान काफी आरामदायक रहेगा।",
        "good_outdoor": "🚶 बाहर की गतिविधियों के लिए मौसम अच्छा है।",
        "outdoor_warning": "⚠️ बाहर जाने की योजना में थोड़ी तैयारी की आवश्यकता हो सकती है।",
        "weather_update": "🌤️ मौसम अपडेट",
        "condition": "स्थिति",
        "main_title": "WeatherGPT 🌤️",
        "main_subtitle": "आपका बुद्धिमान मौसम सहायक",
        "footer": "WeatherGPT • AI मौसम सहायक • हैकाथॉन प्रोटोटाइप",
        "enter_city": "शहर दर्ज करें...",
        "language": "🌐 भाषा",
        "loading_weather": "मौसम लोड हो रहा है...",
        "hackathon": "हैकाथॉन प्रोटोटाइप",
        "weather_ai": "मौसम + AI",
        "unknown": "अज्ञात",
    },
    "Telugu": {
        "search_location": "📍 ప్రదేశాన్ని వెతకండి",
        "temperature": "🌡️ ఉష్ణోగ్రత",
        "celsius": "సెల్సియస్ (°C)",
        "fahrenheit": "ఫారెన్‌హీట్ (°F)",
        "current_weather": "ప్రస్తుత వాతావరణం",
        "feels_like": "అనిపించే ఉష్ణోగ్రత",
        "todays_high": "ఈరోజు గరిష్ఠం",
        "todays_low": "ఈరోజు కనిష్ఠం",
        "weather_details": "📊 వాతావరణ వివరాలు",
        "humidity": "💧 తేమ",
        "wind": "💨 గాలి",
        "rain": "🌧️ వర్షం",
        "pressure": "🔵 వాయు పీడనం",
        "forecast": "📅 7 రోజుల వాతావరణ అంచనా",
        "today": "ఈరోజు",
        "assistant": "🤖 WeatherGPT",
        "assistant_desc": "వాతావరణం గురించి ఏదైనా అడగండి.",
        "chat_placeholder": "ఈరోజు వాతావరణం గురించి అడగండి...",
        "voice_received": "🎙️ వాయిస్ రికార్డింగ్ అందింది. దీన్ని వాతావరణ ప్రశ్నగా మార్చడానికి Speech-to-Text APIని కనెక్ట్ చేయండి.",
        "city_not_found": "❌ నగరం కనుగొనబడలేదు. దయచేసి సరైన నగరాన్ని నమోదు చేయండి.",
        "weather_error": "❌ వాతావరణ సమాచారం పొందలేకపోయాము. దయచేసి మళ్లీ ప్రయత్నించండి.",
        "carry_umbrella": "☔ అవును, గొడుగు తీసుకెళ్లడం మంచిది.",
        "no_umbrella": "🌤️ బహుశా గొడుగు అవసరం ఉండకపోవచ్చు.",
        "rain_chance": "వర్షం పడే అవకాశం",
        "hot": "🔥 ఈరోజు చాలా వేడిగా ఉంటుంది. ఎక్కువ నీరు తాగండి మరియు ఎక్కువసేపు ఎండలో ఉండకండి.",
        "warm": "🌡️ ఈరోజు వెచ్చగా ఉంటుంది. తగినంత నీరు తాగుతూ ఉండండి.",
        "comfortable": "🌤️ ఈరోజు ఉష్ణోగ్రత సౌకర్యవంతంగా ఉంటుంది.",
        "good_outdoor": "🚶 బయట కార్యకలాపాలకు వాతావరణం అనుకూలంగా ఉంది.",
        "outdoor_warning": "⚠️ బయట కార్యక్రమాలకు కొంత ముందస్తు జాగ్రత్త అవసరం కావచ్చు.",
        "weather_update": "🌤️ వాతావరణ సమాచారం",
        "condition": "పరిస్థితి",
        "main_title": "WeatherGPT 🌤️",
        "main_subtitle": "మీ తెలివైన వాతావరణ సహాయకుడు",
        "footer": "WeatherGPT • AI వాతావరణ సహాయకుడు • హ్యాకథాన్ ప్రోటోటైప్",
        "enter_city": "నగరాన్ని నమోదు చేయండి...",
        "language": "🌐 భాష",
        "loading_weather": "వాతావరణం లోడ్ అవుతోంది...",
        "hackathon": "హ్యాకథాన్ ప్రోటోటైప్",
        "weather_ai": "వాతావరణం + AI",
        "unknown": "తెలియదు",
    },
    "Tamil": {
        "search_location": "📍 இடத்தைத் தேடுங்கள்",
        "temperature": "🌡️ வெப்பநிலை",
        "celsius": "செல்சியஸ் (°C)",
        "fahrenheit": "ஃபாரன்ஹீட் (°F)",
        "current_weather": "தற்போதைய வானிலை",
        "feels_like": "உணரப்படும் வெப்பநிலை",
        "todays_high": "இன்றைய அதிகபட்சம்",
        "todays_low": "இன்றைய குறைந்தபட்சம்",
        "weather_details": "📊 வானிலை விவரங்கள்",
        "humidity": "💧 ஈரப்பதம்",
        "wind": "💨 காற்று",
        "rain": "🌧️ மழை",
        "pressure": "🔵 காற்றழுத்தம்",
        "forecast": "📅 7 நாள் வானிலை முன்னறிவிப்பு",
        "today": "இன்று",
        "assistant": "🤖 WeatherGPT",
        "assistant_desc": "வானிலை பற்றி எதையும் கேளுங்கள்.",
        "chat_placeholder": "இன்றைய வானிலை பற்றி கேளுங்கள்...",
        "voice_received": "🎙️ குரல் பதிவு பெறப்பட்டது. இதை வானிலை கேள்வியாக மாற்ற Speech-to-Text API-ஐ இணைக்கவும்.",
        "city_not_found": "❌ நகரம் கிடைக்கவில்லை. சரியான நகரத்தை உள்ளிடவும்.",
        "weather_error": "❌ வானிலைத் தகவலைப் பெற முடியவில்லை. மீண்டும் முயற்சிக்கவும்.",
        "carry_umbrella": "☔ ஆம், குடை எடுத்துச் செல்வது நல்லது.",
        "no_umbrella": "🌤️ குடை தேவையில்லை என்று தெரிகிறது.",
        "rain_chance": "மழைக்கான வாய்ப்பு",
        "hot": "🔥 இன்று மிகவும் வெப்பமாக இருக்கும். போதுமான தண்ணீர் குடித்து, அதிக நேரம் வெயிலில் இருப்பதைத் தவிர்க்கவும்.",
        "warm": "🌡️ இன்று வெப்பமாக இருக்கும். போதுமான தண்ணீர் குடிக்கவும்.",
        "comfortable": "🌤️ இன்று வெப்பநிலை சௌகரியமாக இருக்கும்.",
        "good_outdoor": "🚶 வெளிப்புற நடவடிக்கைகளுக்கு வானிலை ஏற்றதாக உள்ளது.",
        "outdoor_warning": "⚠️ வெளிப்புற திட்டங்களுக்கு சில முன்னெச்சரிக்கைகள் தேவைப்படலாம்.",
        "weather_update": "🌤️ வானிலை தகவல்",
        "condition": "நிலை",
        "main_title": "WeatherGPT 🌤️",
        "main_subtitle": "உங்கள் அறிவார்ந்த வானிலை துணை",
        "footer": "WeatherGPT • AI வானிலை உதவியாளர் • ஹேக்கத்தான் முன்மாதிரி",
        "enter_city": "நகரத்தை உள்ளிடவும்...",
        "language": "🌐 மொழி",
        "loading_weather": "வானிலை ஏற்றப்படுகிறது...",
        "hackathon": "ஹேக்கத்தான் முன்மாதிரி",
        "weather_ai": "வானிலை + AI",
        "unknown": "தெரியவில்லை",
    },
    "Kannada": {
        "search_location": "📍 ಸ್ಥಳ ಹುಡುಕಿ",
        "temperature": "🌡️ ತಾಪಮಾನ",
        "celsius": "ಸೆಲ್ಸಿಯಸ್ (°C)",
        "fahrenheit": "ಫ್ಯಾರನ್‌ಹೀಟ್ (°F)",
        "current_weather": "ಪ್ರಸ್ತುತ ಹವಾಮಾನ",
        "feels_like": "ಅನುಭವವಾಗುವ ತಾಪಮಾನ",
        "todays_high": "ಇಂದಿನ ಗರಿಷ್ಠ",
        "todays_low": "ಇಂದಿನ ಕನಿಷ್ಠ",
        "weather_details": "📊 ಹವಾಮಾನ ವಿವರಗಳು",
        "humidity": "💧 ತೇವಾಂಶ",
        "wind": "💨 ಗಾಳಿ",
        "rain": "🌧️ ಮಳೆ",
        "pressure": "🔵 ವಾಯು ಒತ್ತಡ",
        "forecast": "📅 7 ದಿನಗಳ ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ",
        "today": "ಇಂದು",
        "assistant": "🤖 WeatherGPT",
        "assistant_desc": "ಹವಾಮಾನದ ಬಗ್ಗೆ ಏನು ಬೇಕಾದರೂ ಕೇಳಿ.",
        "chat_placeholder": "ಇಂದಿನ ಹವಾಮಾನದ ಬಗ್ಗೆ ಕೇಳಿ...",
        "voice_received": "🎙️ ಧ್ವನಿ ರೆಕಾರ್ಡಿಂಗ್ ಸ್ವೀಕರಿಸಲಾಗಿದೆ. ಇದನ್ನು ಹವಾಮಾನ ಪ್ರಶ್ನೆಯಾಗಿ ಪರಿವರ್ತಿಸಲು Speech-to-Text API ಸಂಪರ್ಕಿಸಿ.",
        "city_not_found": "❌ ನಗರ ಕಂಡುಬಂದಿಲ್ಲ. ದಯವಿಟ್ಟು ಸರಿಯಾದ ನಗರವನ್ನು ನಮೂದಿಸಿ.",
        "weather_error": "❌ ಹವಾಮಾನ ಮಾಹಿತಿಯನ್ನು ಪಡೆಯಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "carry_umbrella": "☔ ಹೌದು, ಛತ್ರಿ ತೆಗೆದುಕೊಂಡು ಹೋಗುವುದು ಉತ್ತಮ.",
        "no_umbrella": "🌤️ ಬಹುಶಃ ಛತ್ರಿಯ ಅಗತ್ಯವಿಲ್ಲ.",
        "rain_chance": "ಮಳೆಯ ಸಾಧ್ಯತೆ",
        "hot": "🔥 ಇಂದು ತುಂಬಾ ಬಿಸಿಯಾಗಿರುತ್ತದೆ. ಸಾಕಷ್ಟು ನೀರು ಕುಡಿಯಿರಿ ಮತ್ತು ಹೆಚ್ಚು ಸಮಯ ಬಿಸಿಲಿನಲ್ಲಿ ಇರಬೇಡಿ.",
        "warm": "🌡️ ಇಂದು ಬೆಚ್ಚಗಿರುತ್ತದೆ. ಸಾಕಷ್ಟು ನೀರು ಕುಡಿಯಿರಿ.",
        "comfortable": "🌤️ ಇಂದು ತಾಪಮಾನ ಆರಾಮದಾಯಕವಾಗಿರುತ್ತದೆ.",
        "good_outdoor": "🚶 ಹೊರಾಂಗಣ ಚಟುವಟಿಕೆಗಳಿಗೆ ಹವಾಮಾನ ಉತ್ತಮವಾಗಿದೆ.",
        "outdoor_warning": "⚠️ ಹೊರಾಂಗಣ ಯೋಜನೆಗಳಿಗೆ ಸ್ವಲ್ಪ ಮುನ್ನೆಚ್ಚರಿಕೆ ಅಗತ್ಯವಿರಬಹುದು.",
        "weather_update": "🌤️ ಹವಾಮಾನ ಮಾಹಿತಿ",
        "condition": "ಸ್ಥಿತಿ",
        "main_title": "WeatherGPT 🌤️",
        "main_subtitle": "ನಿಮ್ಮ ಬುದ್ಧಿವಂತ ಹವಾಮಾನ ಸಹಾಯಕ",
        "footer": "WeatherGPT • AI ಹವಾಮಾನ ಸಹಾಯಕ • ಹ್ಯಾಕಥಾನ್ ಪ್ರೋಟೋಟೈಪ್",
        "enter_city": "ನಗರವನ್ನು ನಮೂದಿಸಿ...",
        "language": "🌐 ಭಾಷೆ",
        "loading_weather": "ಹವಾಮಾನ ಲೋಡ್ ಆಗುತ್ತಿದೆ...",
        "hackathon": "ಹ್ಯಾಕಥಾನ್ ಪ್ರೋಟೋಟೈಪ್",
        "weather_ai": "ಹವಾಮಾನ + AI",
        "unknown": "ತಿಳಿದಿಲ್ಲ",
    },
    "Malayalam": {
        "search_location": "📍 സ്ഥലം തിരയുക",
        "temperature": "🌡️ താപനില",
        "celsius": "സെൽഷ്യസ് (°C)",
        "fahrenheit": "ഫാരൻഹീറ്റ് (°F)",
        "current_weather": "നിലവിലെ കാലാവസ്ഥ",
        "feels_like": "അനുഭവപ്പെടുന്ന താപനില",
        "todays_high": "ഇന്നത്തെ ഉയർന്ന താപനില",
        "todays_low": "ഇന്നത്തെ കുറഞ്ഞ താപനില",
        "weather_details": "📊 കാലാവസ്ഥാ വിവരങ്ങൾ",
        "humidity": "💧 ഈർപ്പം",
        "wind": "💨 കാറ്റ്",
        "rain": "🌧️ മഴ",
        "pressure": "🔵 മർദ്ദം",
        "forecast": "📅 7 ദിവസത്തെ കാലാവസ്ഥാ പ്രവചനം",
        "today": "ഇന്ന്",
        "assistant": "🤖 WeatherGPT",
        "assistant_desc": "കാലാവസ്ഥയെക്കുറിച്ച് എന്തും ചോദിക്കാം.",
        "chat_placeholder": "ഇന്നത്തെ കാലാവസ്ഥയെക്കുറിച്ച് ചോദിക്കുക...",
        "voice_received": "🎙️ ശബ്ദ റെക്കോർഡിംഗ് ലഭിച്ചു. ഇത് കാലാവസ്ഥാ ചോദ്യമാക്കി മാറ്റാൻ Speech-to-Text API ബന്ധിപ്പിക്കുക.",
        "city_not_found": "❌ നഗരം കണ്ടെത്താനായില്ല. സാധുവായ നഗരം നൽകുക.",
        "weather_error": "❌ കാലാവസ്ഥാ വിവരങ്ങൾ ലഭ്യമാക്കാൻ കഴിഞ്ഞില്ല. വീണ്ടും ശ്രമിക്കുക.",
        "carry_umbrella": "☔ അതെ, കുട കൊണ്ടുപോകുന്നത് നല്ലതാണ്.",
        "no_umbrella": "🌤️ ഒരുപക്ഷേ കുട ആവശ്യമില്ല.",
        "rain_chance": "മഴയ്ക്കുള്ള സാധ്യത",
        "hot": "🔥 ഇന്ന് വളരെ ചൂടായിരിക്കും. ധാരാളം വെള്ളം കുടിക്കുകയും കൂടുതൽ സമയം വെയിലത്ത് നിൽക്കുന്നത് ഒഴിവാക്കുകയും ചെയ്യുക.",
        "warm": "🌡️ ഇന്ന് ചൂടുള്ള കാലാവസ്ഥയായിരിക്കും. ആവശ്യത്തിന് വെള്ളം കുടിക്കുക.",
        "comfortable": "🌤️ ഇന്ന് താപനില സുഖകരമായിരിക്കും.",
        "good_outdoor": "🚶 പുറം പ്രവർത്തനങ്ങൾക്ക് കാലാവസ്ഥ നല്ലതാണ്.",
        "outdoor_warning": "⚠️ പുറം പ്രവർത്തനങ്ങൾക്ക് ചില മുൻകരുതലുകൾ ആവശ്യമായി വരാം.",
        "weather_update": "🌤️ കാലാവസ്ഥാ അപ്‌ഡേറ്റ്",
        "condition": "അവസ്ഥ",
        "main_title": "WeatherGPT 🌤️",
        "main_subtitle": "നിങ്ങളുടെ ബുദ്ധിമാനായ കാലാവസ്ഥാ സഹായി",
        "footer": "WeatherGPT • AI കാലാവസ്ഥാ സഹായി • ഹാക്കത്തോൺ പ്രോട്ടോടൈപ്പ്",
        "enter_city": "നഗരം നൽകുക...",
        "language": "🌐 ഭാഷ",
        "loading_weather": "കാലാവസ്ഥ ലോഡ് ചെയ്യുന്നു...",
        "hackathon": "ഹാക്കത്തോൺ പ്രോട്ടോടൈപ്പ്",
        "weather_ai": "കാലാവസ്ഥ + AI",
        "unknown": "അജ്ഞാതം",
    },
}


# =============================================================
# WEATHER-CODE TRANSLATIONS (Open-Meteo WMO codes)
# =============================================================

WEATHER_TRANSLATIONS = {
    "English": {
        0: ("☀️", "Clear Sky"), 1: ("🌤️", "Mainly Clear"),
        2: ("⛅", "Partly Cloudy"), 3: ("☁️", "Cloudy"),
        45: ("🌫️", "Foggy"), 48: ("🌫️", "Foggy"),
        51: ("🌦️", "Light Drizzle"), 53: ("🌦️", "Drizzle"),
        55: ("🌧️", "Heavy Drizzle"), 61: ("🌧️", "Light Rain"),
        63: ("🌧️", "Rain"), 65: ("🌧️", "Heavy Rain"),
        71: ("🌨️", "Light Snow"), 73: ("❄️", "Snow"),
        75: ("❄️", "Heavy Snow"), 80: ("🌦️", "Rain Showers"),
        81: ("🌧️", "Rain Showers"), 82: ("⛈️", "Heavy Rain Showers"),
        95: ("⛈️", "Thunderstorm"), 96: ("⛈️", "Thunderstorm"),
        99: ("⛈️", "Thunderstorm"),
    },
    "Hindi": {
        0: ("☀️", "साफ आसमान"), 1: ("🌤️", "मुख्यतः साफ"),
        2: ("⛅", "आंशिक बादल"), 3: ("☁️", "बादल छाए हुए"),
        45: ("🌫️", "कोहरा"), 48: ("🌫️", "कोहरा"),
        51: ("🌦️", "हल्की बूंदाबांदी"), 53: ("🌦️", "बूंदाबांदी"),
        55: ("🌧️", "तेज़ बूंदाबांदी"), 61: ("🌧️", "हल्की बारिश"),
        63: ("🌧️", "बारिश"), 65: ("🌧️", "तेज़ बारिश"),
        71: ("🌨️", "हल्की बर्फबारी"), 73: ("❄️", "बर्फबारी"),
        75: ("❄️", "तेज़ बर्फबारी"), 80: ("🌦️", "बारिश की बौछारें"),
        81: ("🌧️", "बारिश की बौछारें"), 82: ("⛈️", "तेज़ बारिश की बौछारें"),
        95: ("⛈️", "आंधी-तूफान"), 96: ("⛈️", "आंधी-तूफान"),
        99: ("⛈️", "आंधी-तूफान"),
    },
    "Telugu": {
        0: ("☀️", "ఆకాశం నిర్మలంగా ఉంది"), 1: ("🌤️", "ప్రధానంగా నిర్మలంగా ఉంది"),
        2: ("⛅", "పాక్షికంగా మేఘావృతం"), 3: ("☁️", "మేఘావృతం"),
        45: ("🌫️", "పొగమంచు"), 48: ("🌫️", "పొగమంచు"),
        51: ("🌦️", "తేలికపాటి జల్లులు"), 53: ("🌦️", "జల్లులు"),
        55: ("🌧️", "భారీ జల్లులు"), 61: ("🌧️", "తేలికపాటి వర్షం"),
        63: ("🌧️", "వర్షం"), 65: ("🌧️", "భారీ వర్షం"),
        71: ("🌨️", "తేలికపాటి మంచు"), 73: ("❄️", "మంచు"),
        75: ("❄️", "భారీ మంచు"), 80: ("🌦️", "వర్షపు జల్లులు"),
        81: ("🌧️", "వర్షపు జల్లులు"), 82: ("⛈️", "భారీ వర్షపు జల్లులు"),
        95: ("⛈️", "ఉరుములతో కూడిన వర్షం"), 96: ("⛈️", "ఉరుములతో కూడిన వర్షం"),
        99: ("⛈️", "ఉరుములతో కూడిన వర్షం"),
    },
    "Tamil": {
        0: ("☀️", "தெளிவான வானம்"), 1: ("🌤️", "பெரும்பாலும் தெளிவு"),
        2: ("⛅", "ஓரளவு மேகமூட்டம்"), 3: ("☁️", "மேகமூட்டம்"),
        45: ("🌫️", "மூடுபனி"), 48: ("🌫️", "மூடுபனி"),
        51: ("🌦️", "லேசான தூறல்"), 53: ("🌦️", "தூறல்"),
        55: ("🌧️", "கனமான தூறல்"), 61: ("🌧️", "லேசான மழை"),
        63: ("🌧️", "மழை"), 65: ("🌧️", "கனமழை"),
        71: ("🌨️", "லேசான பனிப்பொழிவு"), 73: ("❄️", "பனிப்பொழிவு"),
        75: ("❄️", "கனமான பனிப்பொழிவு"), 80: ("🌦️", "மழைத்தூறல்"),
        81: ("🌧️", "மழைத்தூறல்"), 82: ("⛈️", "கனமான மழைத்தூறல்"),
        95: ("⛈️", "இடியுடன் கூடிய மழை"), 96: ("⛈️", "இடியுடன் கூடிய மழை"),
        99: ("⛈️", "இடியுடன் கூடிய மழை"),
    },
    "Kannada": {
        0: ("☀️", "ಸ್ವಚ್ಛ ಆಕಾಶ"), 1: ("🌤️", "ಮುಖ್ಯವಾಗಿ ಸ್ವಚ್ಛ"),
        2: ("⛅", "ಭಾಗಶಃ ಮೋಡ ಕವಿದಿದೆ"), 3: ("☁️", "ಮೋಡ ಕವಿದಿದೆ"),
        45: ("🌫️", "ಮಂಜು"), 48: ("🌫️", "ಮಂಜು"),
        51: ("🌦️", "ಲಘು ತುಂತುರು ಮಳೆ"), 53: ("🌦️", "ತುಂತುರು ಮಳೆ"),
        55: ("🌧️", "ಭಾರಿ ತುಂತುರು ಮಳೆ"), 61: ("🌧️", "ಲಘು ಮಳೆ"),
        63: ("🌧️", "ಮಳೆ"), 65: ("🌧️", "ಭಾರಿ ಮಳೆ"),
        71: ("🌨️", "ಲಘು ಹಿಮಪಾತ"), 73: ("❄️", "ಹಿಮಪಾತ"),
        75: ("❄️", "ಭಾರಿ ಹಿಮಪಾತ"), 80: ("🌦️", "ಮಳೆಯ ತುಂತುರು"),
        81: ("🌧️", "ಮಳೆಯ ತುಂತುರು"), 82: ("⛈️", "ಭಾರಿ ಮಳೆಯ ತುಂತುರು"),
        95: ("⛈️", "ಗುಡುಗು ಸಹಿತ ಮಳೆ"), 96: ("⛈️", "ಗುಡುಗು ಸಹಿತ ಮಳೆ"),
        99: ("⛈️", "ಗುಡುಗು ಸಹಿತ ಮಳೆ"),
    },
    "Malayalam": {
        0: ("☀️", "തെളിഞ്ഞ ആകാശം"), 1: ("🌤️", "പ്രധാനമായും തെളിഞ്ഞത്"),
        2: ("⛅", "ഭാഗികമായി മേഘാവൃതം"), 3: ("☁️", "മേഘാവൃതം"),
        45: ("🌫️", "മൂടൽമഞ്ഞ്"), 48: ("🌫️", "മൂടൽമഞ്ഞ്"),
        51: ("🌦️", "നേരിയ ചാറ്റൽമഴ"), 53: ("🌦️", "ചാറ്റൽമഴ"),
        55: ("🌧️", "ശക്തമായ ചാറ്റൽമഴ"), 61: ("🌧️", "നേരിയ മഴ"),
        63: ("🌧️", "മഴ"), 65: ("🌧️", "ശക്തമായ മഴ"),
        71: ("🌨️", "നേരിയ മഞ്ഞുവീഴ്ച"), 73: ("❄️", "മഞ്ഞുവീഴ്ച"),
        75: ("❄️", "ശക്തമായ മഞ്ഞുവീഴ്ച"), 80: ("🌦️", "മഴച്ചാറ്റൽ"),
        81: ("🌧️", "മഴച്ചാറ്റൽ"), 82: ("⛈️", "ശക്തമായ മഴച്ചാറ്റൽ"),
        95: ("⛈️", "ഇടിമിന്നലോടുകൂടിയ മഴ"), 96: ("⛈️", "ഇടിമിന്നലോടുകൂടിയ മഴ"),
        99: ("⛈️", "ഇടിമിന്നലോടുകൂടിയ മഴ"),
    },
}

DAY_TRANSLATIONS = {
    "English": {
        "Monday": "Monday", "Tuesday": "Tuesday", "Wednesday": "Wednesday",
        "Thursday": "Thursday", "Friday": "Friday", "Saturday": "Saturday", "Sunday": "Sunday",
    },
    "Hindi": {
        "Monday": "सोमवार", "Tuesday": "मंगलवार", "Wednesday": "बुधवार",
        "Thursday": "गुरुवार", "Friday": "शुक्रवार", "Saturday": "शनिवार", "Sunday": "रविवार",
    },
    "Telugu": {
        "Monday": "సోమవారం", "Tuesday": "మంగళవారం", "Wednesday": "బుధవారం",
        "Thursday": "గురువారం", "Friday": "శుక్రవారం", "Saturday": "శనివారం", "Sunday": "ఆదివారం",
    },
    "Tamil": {
        "Monday": "திங்கள்", "Tuesday": "செவ்வாய்", "Wednesday": "புதன்",
        "Thursday": "வியாழன்", "Friday": "வெள்ளி", "Saturday": "சனி", "Sunday": "ஞாயிறு",
    },
    "Kannada": {
        "Monday": "ಸೋಮವಾರ", "Tuesday": "ಮಂಗಳವಾರ", "Wednesday": "ಬುಧವಾರ",
        "Thursday": "ಗುರುವಾರ", "Friday": "ಶುಕ್ರವಾರ", "Saturday": "ಶನಿವಾರ", "Sunday": "ಭಾನುವಾರ",
    },
    "Malayalam": {
        "Monday": "തിങ്കളാഴ്ച", "Tuesday": "ചൊവ്വാഴ്ച", "Wednesday": "ബുധനാഴ്ച",
        "Thursday": "വ്യാഴാഴ്ച", "Friday": "വെള്ളിയാഴ്ച", "Saturday": "ശനിയാഴ്ച", "Sunday": "ഞായറാഴ്ച",
    },
}

RAIN_KEYWORDS = [
    "rain", "umbrella", "बारिश", "छाता", "వర్షం", "గొడుగు",
    "மழை", "குடை", "ಮಳೆ", "ಛತ್ರಿ", "മഴ", "കുട",
]
HOT_KEYWORDS = ["hot", "गर्म", "వేడి", "வெப்பம்", "ಬಿಸಿ", "ചൂട്"]
OUTDOOR_KEYWORDS = [
    "trip", "outdoor", "यात्रा", "बाहर", "బయట", "ప్రయాణం",
    "வெளியே", "பயணம்", "ಹೊರಗೆ", "ಪ್ರಯಾಣ", "പുറത്ത്", "യാത്ര",
]


# =============================================================
# CSS
# =============================================================

st.markdown(
    """
    <style>
    .stApp { background-color: #0f172a; }
    .block-container { padding-top: 1.5rem; }

    .top-chat {
        background: linear-gradient(135deg, #172554, #1e3a8a);
        padding: 18px;
        border-radius: 20px;
        border: 1px solid #2563eb;
    }

    .top-chat h2 { margin: 0; color: white; }
    .top-chat p { color: #dbeafe; margin-top: 5px; }


    .forecast-icon {
        font-size: 48px;
        line-height: 1.2;
        margin: 8px 0 10px 0;
    }

    .big-temperature {
        font-size: 52px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================
# WEATHER API HELPERS — Open-Meteo, no API key required
# =============================================================

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# WeatherGPT FastAPI backend
BACKEND_URL = "http://127.0.0.1:8000"

BACKEND_LANGUAGE_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
}


@st.cache_data(ttl=3600, show_spinner=False)
def get_coordinates(city: str):
    """Resolve a city name to coordinates."""
    city = (city or "").strip()
    if not city:
        return None

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    try:
        response = requests.get(GEOCODE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return None

    results = data.get("results") or []
    if not results:
        return None

    result = results[0]

    try:
        return {
            "latitude": float(result["latitude"]),
            "longitude": float(result["longitude"]),
            "name": str(result["name"]),
            "country": str(result.get("country", "")),
        }
    except (KeyError, TypeError, ValueError):
        return None


@st.cache_data(ttl=600, show_spinner=False)
def get_weather(latitude: float, longitude: float):
    """Fetch current conditions and a 7-day forecast."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,relative_humidity_2m,apparent_temperature,"
            "precipitation,weather_code,surface_pressure,wind_speed_10m"
        ),
        "daily": (
            "weather_code,temperature_2m_max,temperature_2m_min,"
            "precipitation_probability_max,wind_speed_10m_max"
        ),
        "forecast_days": 7,
        "timezone": "auto",
    }

    try:
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return None

    if not isinstance(data, dict) or "current" not in data or "daily" not in data:
        return None

    return data


def weather_description(code, language: str):
    """Return (icon, translated label) for a WMO weather code."""
    table = WEATHER_TRANSLATIONS.get(
        language,
        WEATHER_TRANSLATIONS["English"],
    )
    fallback = (
        "🌤️",
        LANGUAGES.get(language, LANGUAGES["English"])["unknown"],
    )
    try:
        normalized_code = int(float(code))
    except (TypeError, ValueError):
        normalized_code = -1

    return table.get(normalized_code, fallback)


def safe_float(value, default=0.0):
    """Convert an API value to float without crashing the UI."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value, default=0):
    """Convert an API value to int without crashing the UI."""
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def convert_temperature(value, unit_is_fahrenheit: bool):
    """Convert Celsius to the selected display unit."""
    value = safe_float(value)
    return value * 9 / 5 + 32 if unit_is_fahrenheit else value


# =============================================================
# BACKEND RESPONSE TRANSLATIONS
# =============================================================

BACKEND_DETAIL_LABELS = {
    "English": {
        "details": "📊 WeatherGPT Details",
        "location": "Location",
        "date": "Date",
        "temperature": "Temperature",
        "rainfall": "Rainfall",
        "precip_probability": "Precipitation probability",
        "humidity": "Humidity",
        "wind": "Wind",
        "condition": "Condition",
        "risk": "⚠️ Risk Assessment",
        "hazard": "Hazard",
        "level": "Level",
        "reason": "Reason",
        "action": "Recommended action",
        "advisory": "🌾 Crop Advisory",
        "crop": "Crop",
        "recommendation": "Recommendation",
        "none": "None",
        "low": "Low",
        "moderate": "Moderate",
        "high": "High",
        "critical": "Critical",
        "extreme_rain": "Extreme rain",
        "very_heavy_rain": "Very heavy rain",
        "heavy_rain": "Heavy rain",
        "severe_heat": "Severe heat",
        "heatwave": "Heatwave",
        "coldwave": "Coldwave",
        "damaging_wind": "Damaging wind",
        "high_wind": "High wind",
    },
    "Hindi": {
        "details": "📊 WeatherGPT विवरण",
        "location": "स्थान", "date": "तारीख", "temperature": "तापमान",
        "rainfall": "वर्षा", "precip_probability": "वर्षा की संभावना",
        "humidity": "नमी", "wind": "हवा", "condition": "स्थिति",
        "risk": "⚠️ जोखिम आकलन", "hazard": "खतरा", "level": "स्तर",
        "reason": "कारण", "action": "अनुशंसित कार्रवाई",
        "advisory": "🌾 फसल सलाह", "crop": "फसल", "recommendation": "सिफारिश",
        "none": "कोई नहीं", "low": "कम", "moderate": "मध्यम",
        "high": "उच्च", "critical": "गंभीर",
        "extreme_rain": "अत्यधिक वर्षा", "very_heavy_rain": "बहुत भारी वर्षा",
        "heavy_rain": "भारी वर्षा", "severe_heat": "भीषण गर्मी",
        "heatwave": "लू", "coldwave": "शीत लहर",
        "damaging_wind": "हानिकारक तेज़ हवा", "high_wind": "तेज़ हवा",
    },
    "Telugu": {
        "details": "📊 WeatherGPT వివరాలు",
        "location": "ప్రదేశం", "date": "తేదీ", "temperature": "ఉష్ణోగ్రత",
        "rainfall": "వర్షపాతం", "precip_probability": "వర్షపాతం సంభావ్యత",
        "humidity": "తేమ", "wind": "గాలి", "condition": "పరిస్థితి",
        "risk": "⚠️ ప్రమాద అంచనా", "hazard": "ప్రమాదం", "level": "స్థాయి",
        "reason": "కారణం", "action": "సిఫార్సు చేసిన చర్య",
        "advisory": "🌾 పంట సలహా", "crop": "పంట", "recommendation": "సిఫార్సు",
        "none": "ఏదీ లేదు", "low": "తక్కువ", "moderate": "మధ్యస్థం",
        "high": "అధికం", "critical": "తీవ్రమైనది",
        "extreme_rain": "అత్యంత భారీ వర్షం", "very_heavy_rain": "చాలా భారీ వర్షం",
        "heavy_rain": "భారీ వర్షం", "severe_heat": "తీవ్రమైన వేడి",
        "heatwave": "వడగాలులు", "coldwave": "చలి గాలులు",
        "damaging_wind": "నష్టకరమైన బలమైన గాలి", "high_wind": "బలమైన గాలి",
    },
    "Tamil": {
        "details": "📊 WeatherGPT விவரங்கள்",
        "location": "இடம்", "date": "தேதி", "temperature": "வெப்பநிலை",
        "rainfall": "மழைப்பொழிவு", "precip_probability": "மழைக்கான வாய்ப்பு",
        "humidity": "ஈரப்பதம்", "wind": "காற்று", "condition": "நிலை",
        "risk": "⚠️ ஆபத்து மதிப்பீடு", "hazard": "ஆபத்து", "level": "நிலை",
        "reason": "காரணம்", "action": "பரிந்துரைக்கப்பட்ட நடவடிக்கை",
        "advisory": "🌾 பயிர் ஆலோசனை", "crop": "பயிர்", "recommendation": "பரிந்துரை",
        "none": "எதுவுமில்லை", "low": "குறைவு", "moderate": "மிதமான",
        "high": "அதிகம்", "critical": "மிகவும் தீவிரம்",
        "extreme_rain": "மிகவும் கனமழை", "very_heavy_rain": "மிக கனமழை",
        "heavy_rain": "கனமழை", "severe_heat": "கடுமையான வெப்பம்",
        "heatwave": "வெப்ப அலை", "coldwave": "குளிர் அலை",
        "damaging_wind": "சேதம் ஏற்படுத்தும் பலத்த காற்று", "high_wind": "பலத்த காற்று",
    },
    "Kannada": {
        "details": "📊 WeatherGPT ವಿವರಗಳು",
        "location": "ಸ್ಥಳ", "date": "ದಿನಾಂಕ", "temperature": "ತಾಪಮಾನ",
        "rainfall": "ಮಳೆ", "precip_probability": "ಮಳೆಯ ಸಾಧ್ಯತೆ",
        "humidity": "ತೇವಾಂಶ", "wind": "ಗಾಳಿ", "condition": "ಸ್ಥಿತಿ",
        "risk": "⚠️ ಅಪಾಯದ ಮೌಲ್ಯಮಾಪನ", "hazard": "ಅಪಾಯ", "level": "ಮಟ್ಟ",
        "reason": "ಕಾರಣ", "action": "ಶಿಫಾರಸು ಮಾಡಿದ ಕ್ರಮ",
        "advisory": "🌾 ಬೆಳೆ ಸಲಹೆ", "crop": "ಬೆಳೆ", "recommendation": "ಶಿಫಾರಸು",
        "none": "ಯಾವುದೂ ಇಲ್ಲ", "low": "ಕಡಿಮೆ", "moderate": "ಮಧ್ಯಮ",
        "high": "ಹೆಚ್ಚು", "critical": "ತೀವ್ರ",
        "extreme_rain": "ಅತ್ಯಂತ ಭಾರಿ ಮಳೆ", "very_heavy_rain": "ತುಂಬಾ ಭಾರಿ ಮಳೆ",
        "heavy_rain": "ಭಾರಿ ಮಳೆ", "severe_heat": "ತೀವ್ರ ಬಿಸಿ",
        "heatwave": "ಬಿಸಿಗಾಳಿ", "coldwave": "ಚಳಿಗಾಳಿ",
        "damaging_wind": "ಹಾನಿಕಾರಕ ಬಲವಾದ ಗಾಳಿ", "high_wind": "ಬಲವಾದ ಗಾಳಿ",
    },
    "Malayalam": {
        "details": "📊 WeatherGPT വിശദാംശങ്ങൾ",
        "location": "സ്ഥലം", "date": "തീയതി", "temperature": "താപനില",
        "rainfall": "മഴ", "precip_probability": "മഴയ്ക്കുള്ള സാധ്യത",
        "humidity": "ഈർപ്പം", "wind": "കാറ്റ്", "condition": "അവസ്ഥ",
        "risk": "⚠️ അപകട വിലയിരുത്തൽ", "hazard": "അപകടം", "level": "നില",
        "reason": "കാരണം", "action": "ശുപാർശ ചെയ്യുന്ന നടപടി",
        "advisory": "🌾 വിള ഉപദേശം", "crop": "വിള", "recommendation": "ശുപാർശ",
        "none": "ഒന്നുമില്ല", "low": "കുറവ്", "moderate": "മിതമായ",
        "high": "ഉയർന്ന", "critical": "ഗുരുതരം",
        "extreme_rain": "അതിശക്തമായ മഴ", "very_heavy_rain": "വളരെ ശക്തമായ മഴ",
        "heavy_rain": "ശക്തമായ മഴ", "severe_heat": "കടുത്ത ചൂട്",
        "heatwave": "ഉഷ്ണതരംഗം", "coldwave": "ശീതതരംഗം",
        "damaging_wind": "നാശനഷ്ടമുണ്ടാക്കുന്ന ശക്തമായ കാറ്റ്", "high_wind": "ശക്തമായ കാറ്റ്",
    },
}


def ask_weathergpt_backend(question: str, city: str, language: str):
    """Send the user's question to the real WeatherGPT FastAPI backend."""
    payload = {
        "message": question,
        "location": city,
        "language": BACKEND_LANGUAGE_CODES.get(language, "en"),
    }

    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload,
            timeout=180,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        return {"error": str(exc)}
    except ValueError:
        return {"error": "Backend returned an invalid response."}


def _backend_text(language, key):
    return BACKEND_DETAIL_LABELS.get(
        language,
        BACKEND_DETAIL_LABELS["English"],
    ).get(key, key)


def _backend_value(language, value):
    if value is None:
        return ""
    key = str(value).strip().lower()
    return BACKEND_DETAIL_LABELS.get(
        language,
        BACKEND_DETAIL_LABELS["English"],
    ).get(key, value)


def _translate_backend_free_text(text, language):
    """
    Translate backend free-text fields through the same IndicTrans2
    service used by the FastAPI backend. The UI only needs this for
    structured risk/advisory text; the main reply is already translated.
    """
    if not text or language == "English":
        return text

    try:
        from pathlib import Path as _Path
        import sys as _sys

        project_root = _Path(__file__).resolve().parent
        if str(project_root) not in _sys.path:
            _sys.path.insert(0, str(project_root))

        from translation_service import translation_service as _ts
        return _ts.translate_from_english(
            text,
            BACKEND_LANGUAGE_CODES.get(language, "en"),
        )
    except Exception:
        return text


def answer_weather_question(
    question: str,
    t: dict,
    current_temp: float,
    rain_chance: int,
    humidity: float,
    wind_speed: float,
    condition: str,
    symbol: str,
    location: dict,
) -> str:
    """Return a small rule-based weather response."""
    q = (question or "").casefold().strip()

    if any(word.casefold() in q for word in RAIN_KEYWORDS):
        verdict = t["carry_umbrella"] if rain_chance >= 50 else t["no_umbrella"]
        return f"{verdict} {t['rain_chance']} **{rain_chance}%**."

    if any(word.casefold() in q for word in HOT_KEYWORDS):
        if current_temp >= 35:
            return t["hot"]
        if current_temp >= 30:
            return t["warm"]
        return t["comfortable"]

    if any(word.casefold() in q for word in OUTDOOR_KEYWORDS):
        if rain_chance < 30 and current_temp < 35:
            return f"{t['good_outdoor']} {t['rain_chance']} {rain_chance}%."
        return f"{t['outdoor_warning']} {t['rain_chance']} {rain_chance}%."

    return (
        f"{t['weather_update']}\n\n"
        f"{t['temperature']}: **{current_temp:.1f}{symbol}**\n\n"
        f"{t['condition']}: **{condition}**\n\n"
        f"{t['humidity']}: **{humidity:.0f}%**\n\n"
        f"{t['wind']}: **{wind_speed:.1f} km/h**"
    )


# =============================================================
# SESSION STATE
# =============================================================

if "language" not in st.session_state:
    st.session_state.language = "English"

if "last_question" not in st.session_state:
    st.session_state.last_question = None


# =============================================================
# LANGUAGE SELECTOR
# =============================================================

_, lang_col = st.columns([8, 2])

with lang_col:
    language_options = list(LANGUAGES.keys())
    selected_language = st.selectbox(
        "🌐 Language",
        language_options,
        index=language_options.index(st.session_state.language),
        key="language_selector",
    )

if selected_language != st.session_state.language:
    st.session_state.language = selected_language
    st.rerun()

language = st.session_state.language
t = LANGUAGES[language]


# =============================================================
# SIDEBAR
# =============================================================

with st.sidebar:
    st.title("🌤️ WeatherGPT")
    st.caption(t["assistant_desc"])
    st.divider()

    city = st.text_input(
        t["search_location"],
        value="Hyderabad",
        placeholder=t["enter_city"],
    ).strip()

    unit = st.selectbox(
        t["temperature"],
        [t["celsius"], t["fahrenheit"]],
    )

    st.divider()
    st.caption(t["hackathon"])
    st.caption(t["weather_ai"])


# =============================================================
# FETCH LOCATION + WEATHER
# =============================================================

with st.spinner(t["loading_weather"]):
    location = get_coordinates(city)

if location is None:
    st.error(t["city_not_found"])
    st.stop()

with st.spinner(t["loading_weather"]):
    weather = get_weather(location["latitude"], location["longitude"])

if weather is None:
    st.error(t["weather_error"])
    st.stop()

current = weather.get("current", {})
daily = weather.get("daily", {})

daily_times = daily.get("time") or []
daily_codes = daily.get("weather_code") or []
daily_highs_raw = daily.get("temperature_2m_max") or []
daily_lows_raw = daily.get("temperature_2m_min") or []
daily_rain_raw = daily.get("precipitation_probability_max") or []
daily_wind_raw = daily.get("wind_speed_10m_max") or []

forecast_count = min(
    7,
    len(daily_times),
    len(daily_codes),
    len(daily_highs_raw),
    len(daily_lows_raw),
    len(daily_rain_raw),
    len(daily_wind_raw),
)

if forecast_count == 0:
    st.error(t["weather_error"])
    st.stop()


# =============================================================
# TEMPERATURE UNIT CONVERSION
# =============================================================

unit_is_fahrenheit = unit == t["fahrenheit"]
symbol = "°F" if unit_is_fahrenheit else "°C"

current_temp = convert_temperature(
    current.get("temperature_2m"),
    unit_is_fahrenheit,
)
feels_like = convert_temperature(
    current.get("apparent_temperature"),
    unit_is_fahrenheit,
)

highs = [
    convert_temperature(value, unit_is_fahrenheit)
    for value in daily_highs_raw[:forecast_count]
]
lows = [
    convert_temperature(value, unit_is_fahrenheit)
    for value in daily_lows_raw[:forecast_count]
]


# =============================================================
# TOP SECTION — TITLE + CHAT INPUT
# =============================================================

title_col, chatbot_col = st.columns([5, 3])

with title_col:
    st.title(t["main_title"])
    st.write(t["main_subtitle"])

    location_name = escape(location["name"])
    country_name = escape(location["country"])
    st.caption(f"📍 {location_name}, {country_name}")

with chatbot_col:
    st.markdown(
        f"""
        <div class="top-chat">
            <h2>{escape(t["assistant"])}</h2>
            <p>{escape(t["assistant_desc"])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    chat_col, voice_col = st.columns([5, 1])

    with chat_col:
        question = st.chat_input(t["chat_placeholder"])

    with voice_col:
        # audio_input was introduced in newer Streamlit releases.
        # Keep the app usable on older installations instead of crashing.
        if hasattr(st, "audio_input"):
            audio = st.audio_input(
                "🎙️",
                label_visibility="collapsed",
            )
        else:
            audio = None
            st.caption("🎙️")

if audio:
    st.info(t["voice_received"])

if question:
    st.session_state.last_question = question


# =============================================================
# CURRENT WEATHER
# =============================================================

current_code = safe_int(current.get("weather_code"))
icon, condition = weather_description(current_code, language)

current_humidity = safe_float(current.get("relative_humidity_2m"))
current_wind = safe_float(current.get("wind_speed_10m"))
current_precipitation = safe_float(current.get("precipitation"))
current_pressure = safe_float(current.get("surface_pressure"))

with st.container(border=True):
    st.subheader(f"📍 {location_name}, {country_name}")
    st.divider()

    left, right = st.columns([2, 1])

    with left:
        st.caption(t["current_weather"])
        st.markdown(
            f'<div class="big-temperature">{current_temp:.1f}{symbol}</div>',
            unsafe_allow_html=True,
        )
        st.subheader(f"{icon} {condition}")
        st.write(f"{t['feels_like']} **{feels_like:.1f}{symbol}**")

    with right:
        if highs and lows:
            st.metric(t["todays_high"], f"{highs[0]:.1f}{symbol}")
            st.metric(t["todays_low"], f"{lows[0]:.1f}{symbol}")
        else:
            st.caption(t["weather_error"])

    st.divider()
    st.subheader(t["weather_details"])

    d1, d2, d3, d4 = st.columns(4)
    d1.metric(t["humidity"], f"{current_humidity:.0f}%")
    d2.metric(t["wind"], f"{current_wind:.1f} km/h")
    d3.metric(t["rain"], f"{current_precipitation:.1f} mm")
    d4.metric(t["pressure"], f"{current_pressure:.0f} hPa")


# =============================================================
# 7-DAY FORECAST
# =============================================================

st.write("")
st.subheader(t["forecast"])

forecast_columns = st.columns(forecast_count)
try:
    first_forecast_date = datetime.strptime(
        daily_times[0],
        "%Y-%m-%d",
    ).date()
except (TypeError, ValueError):
    st.error(t["weather_error"])
    st.stop()

for i, col in enumerate(forecast_columns):

    forecast_date = datetime.strptime(
        daily_times[i],
        "%Y-%m-%d",
    ).date()

    if forecast_date == first_forecast_date:
        day = t["today"]
    else:
        english_day = forecast_date.strftime("%A")
        day = DAY_TRANSLATIONS[language].get(
            english_day,
            english_day,
        )

    formatted_date = forecast_date.strftime("%d %b %Y")

    day_icon, day_condition = weather_description(
        daily_codes[i],
        language,
    )

    day_high = safe_float(highs[i])
    day_low = safe_float(lows[i])
    day_rain = safe_int(daily_rain_raw[i])
    day_wind = safe_float(daily_wind_raw[i])

    with col:

        # Use Streamlit's native container
        with st.container(border=True):

            st.markdown(
                f"### {day}"
            )

            st.caption(formatted_date)

            st.markdown(
                f"<div class='forecast-icon'>{escape(day_icon)}</div>",
                unsafe_allow_html=True,
            )

            st.write(day_condition)

            st.markdown(
                f"**{day_high:.1f}{symbol}**"
            )

            st.caption(
                f"{t['todays_low']}: {day_low:.1f}{symbol}"
            )

            st.write(
                f"☔ {t['rain']}: {day_rain}%"
            )

            st.write(
                f"💨 {t['wind']}: {day_wind:.1f} km/h"
            )


# =============================================================
# CHATBOT RESPONSE
# =============================================================

if st.session_state.last_question:
    st.write("")
    st.chat_message("user").write(st.session_state.last_question)

    backend_result = ask_weathergpt_backend(
        st.session_state.last_question,
        city,
        language,
    )

    with st.chat_message("assistant"):
        if "error" in backend_result:
            st.error(
                "❌ " + (
                    "WeatherGPT backend is unavailable. "
                    "Please make sure the FastAPI server is running."
                    if language == "English"
                    else t["weather_error"]
                )
            )
        else:
            # Main AI reply is already translated by the backend.
            st.write(
                backend_result.get(
                    "reply",
                    t["weather_error"],
                )
            )

            backend_weather = backend_result.get("weather") or {}
            backend_risk = backend_result.get("risk") or {}
            backend_advisory = backend_result.get("advisory")

            if backend_weather:
                with st.expander(_backend_text(language, "details")):
                    st.write(
                        f"**{_backend_text(language, 'location')}:** "
                        f"{backend_weather.get('location', city)}"
                    )
                    st.write(
                        f"**{_backend_text(language, 'date')}:** "
                        f"{backend_weather.get('date', 'N/A')}"
                    )
                    st.write(
                        f"**{_backend_text(language, 'temperature')}:** "
                        f"{backend_weather.get('temp_min_c', 0):.1f}°C – "
                        f"{backend_weather.get('temp_max_c', 0):.1f}°C"
                    )
                    st.write(
                        f"**{_backend_text(language, 'rainfall')}:** "
                        f"{backend_weather.get('rainfall_mm', 0):.1f} mm"
                    )
                    st.write(
                        f"**{_backend_text(language, 'precip_probability')}:** "
                        f"{backend_weather.get('precipitation_probability_pct', 0):.0f}%"
                    )
                    st.write(
                        f"**{_backend_text(language, 'humidity')}:** "
                        f"{backend_weather.get('humidity_pct', 0):.0f}%"
                    )
                    st.write(
                        f"**{_backend_text(language, 'wind')}:** "
                        f"{backend_weather.get('wind_kmph', 0):.1f} km/h"
                    )
                    st.write(
                        f"**{_backend_text(language, 'condition')}:** "
                        f"{backend_weather.get('condition', 'Unknown')}"
                    )

            if backend_risk:
                with st.expander(_backend_text(language, "risk")):
                    hazard = backend_risk.get("hazard", "none")
                    level = backend_risk.get("level", "low")

                    reason = _translate_backend_free_text(
                        backend_risk.get("reason", ""),
                        language,
                    )
                    action = _translate_backend_free_text(
                        backend_risk.get("recommended_action", ""),
                        language,
                    )

                    st.write(
                        f"**{_backend_text(language, 'hazard')}:** "
                        f"{_backend_value(language, hazard)}"
                    )
                    st.write(
                        f"**{_backend_text(language, 'level')}:** "
                        f"{_backend_value(language, level)}"
                    )
                    st.write(
                        f"**{_backend_text(language, 'reason')}:** "
                        f"{reason}"
                    )
                    st.write(
                        f"**{_backend_text(language, 'action')}:** "
                        f"{action}"
                    )

            if backend_advisory:
                with st.expander(_backend_text(language, "advisory")):
                    advisory_recommendation = _translate_backend_free_text(
                        backend_advisory.get("recommendation", ""),
                        language,
                    )

                    st.write(
                        f"**{_backend_text(language, 'crop')}:** "
                        f"{backend_advisory.get('crop', '')}"
                    )
                    st.write(
                        f"**{_backend_text(language, 'hazard')}:** "
                        f"{_backend_value(language, backend_advisory.get('hazard', ''))}"
                    )
                    st.write(
                        f"**{_backend_text(language, 'recommendation')}:** "
                        f"{advisory_recommendation}"
                    )


# =============================================================
# FOOTER
# =============================================================

st.divider()
st.caption(t["footer"])


# =============================================================
# DEVELOPMENT VALIDATION
# =============================================================

# This file is intentionally kept as a normal Streamlit script.
# Run:
#     python -m py_compile weathergpt_app_patched.py
# then:
#     streamlit run Frontend_UI_patched.py
