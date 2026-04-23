# Import modules and load environment variables
import os
import openai
import streamlit as st
import requests
from dotenv import load_dotenv
from geopy.geocoders import Nominatim

load_dotenv()

# Access API keys from environment variables
API_KEYS = {
    'OPENWEATHER': os.getenv('OPENWEATHER_API_KEY'),
    'CURRENCY': os.getenv('CURRENCY_API_KEY'),
    'TRANSLATE': os.getenv('TRANSLATE_API_KEY'),
    'TOMORROW': os.getenv('TOMORROW_API_KEY'),
    'OPENAI': os.getenv('OPENAI_API_KEY')
}

# Set OpenAI API key
openai.api_key = API_KEYS['OPENAI']

# Set up the Streamlit app layout with styling
st.set_page_config(
    page_title="Voyager: Travel Companion",
    page_icon="🌍",
    layout="wide"
)

# CSS Styling with background image and layout adjustments
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
        background-size: cover;
        background-position: center;
        font-family: Arial, sans-serif;
        color: #FFFFFF;
    }
    .main-container {
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 10px;
        padding: 20px;
        margin: 20px;
    }
    h1, .title {
        color: #FFFFFF;
        text-align: center;
    }
    .title {
        font-size: 48px;
        font-weight: bold;
        color: #4CAF50;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #4CAF50;
        color: white;
        padding: 15px;
        border-radius: 8px;
    }
    .section-title {
        font-size: 24px;
        color: #4CAF50;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    /* Custom styling for highlighted output */
    .output-box {
        background-color: rgba(255, 255, 255, 0.8);
        color: #333;
        padding: 15px;
        border-radius: 10px;
        font-weight: bold;
        margin-top: 10px;
        font-size: 18px;
    }
    .success-box { color: green; }
    .error-box { color: red; }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for navigation
st.sidebar.markdown("<div class='sidebar-content'><h2>Voyager Navigation</h2></div>", unsafe_allow_html=True)
option = st.sidebar.selectbox("Choose a feature:", 
                              ("Language Translation", "Weather Prediction", "Currency Conversion"))

# Main container
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.markdown("<div class='title'>Voyager: Your AI-Powered Travel Companion 🌍</div>", unsafe_allow_html=True)

# Dictionary of language codes
language_codes = {
    'english': 'en', 'telugu': 'te', 'spanish': 'es', 'french': 'fr',
    'german': 'de', 'hindi': 'hi', 'italian': 'it', 'chinese': 'zh',
    'japanese': 'ja', 'korean': 'ko', 'russian': 'ru'
}

# Function to get coordinates of a location
def get_location_coordinates(location_name):
    try:
        geolocator = Nominatim(user_agent="multi_function_app")
        location = geolocator.geocode(location_name)
        return (location.latitude, location.longitude) if location else None
    except Exception as e:
        return f"Error retrieving location: {e}"

# Function to fetch weather data
def get_weather_data(lat, lon):
    url = "https://api.tomorrow.io/v4/timelines"
    params = {
        'location': f"{lat},{lon}",
        'fields': ['temperature', 'windSpeed', 'precipitationType'],
        'timesteps': '1h',
        'units': 'metric',
        'apikey': API_KEYS['TOMORROW']
    }
    try:
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        return f"Error fetching weather data: {e}"

# Function to perform currency conversion
def convert_currency(amount, from_currency, to_currency):
    url = "https://currency-converter18.p.rapidapi.com/api/v1/convert"
    headers = {
        "x-rapidapi-key": API_KEYS['CURRENCY'],
        "x-rapidapi-host": "currency-converter18.p.rapidapi.com"
    }
    params = {
        "from": from_currency,
        "to": to_currency,
        "amount": amount
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.json().get('result') if response.status_code == 200 else None
    except Exception as e:
        return f"Error converting currency: {e}"

# Function to translate text
def translate_text(text, target_language):
    target_language = target_language.lower().strip()
    language_code = language_codes.get(target_language, target_language)
    
    if language_code not in language_codes.values():
        return "Invalid target language."

    url = "https://microsoft-translator-text-api3.p.rapidapi.com/translate"
    payload = [{"text": text}]
    headers = {
        "x-rapidapi-key": API_KEYS['TRANSLATE'],
        "x-rapidapi-host": "microsoft-translator-text-api3.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, params={"to": language_code, "from": "en"})
        if response.status_code == 200:
            translated_text = response.json()[0]["translations"][0]["text"]
            return translated_text if translated_text else "No translation available."
        else:
            return f"Error code: {response.status_code}"
    except Exception as e:
        return f"Error translating text: {e}"

# Main application logic based on the selected option
if option == "Language Translation":
    st.markdown("<div class='section-title'>Language Translation 🌐</div>", unsafe_allow_html=True)
    text = st.text_input("Enter text to translate:")
    target_language = st.text_input("Enter target language (e.g., 'Spanish' or 'es'):")
    if st.button("Translate"):
        if text and target_language:
            translated_text = translate_text(text, target_language)
            st.markdown(f"<div class='output-box success-box'>Translated Text: {translated_text}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='output-box error-box'>Please enter both text and target language.</div>", unsafe_allow_html=True)

elif option == "Weather Prediction":
    st.markdown("<div class='section-title'>Weather Prediction ☁️</div>", unsafe_allow_html=True)
    city = st.text_input("Enter city name:")
    if st.button("Get Weather"):
        if city:
            coordinates = get_location_coordinates(city)
            if coordinates:
                weather_data = get_weather_data(*coordinates)
                if weather_data:
                    values = weather_data['data']['timelines'][0]['intervals'][0]['values']
                    st.markdown(f"<div class='output-box success-box'>Weather in {city}: {values['temperature']}°C, Wind Speed: {values['windSpeed']} m/s, Precipitation: {values['precipitationType']}.</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='output-box error-box'>Failed to retrieve weather data.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='output-box error-box'>Location not found.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='output-box error-box'>Please enter a city name.</div>", unsafe_allow_html=True)

elif option == "Currency Conversion":
    st.markdown("<div class='section-title'>Currency Conversion 💱</div>", unsafe_allow_html=True)
    amount = st.number_input("Enter amount:", min_value=0.0)
    from_currency = st.text_input("From currency (e.g., 'USD'):").upper()
    to_currency = st.text_input("To currency (e.g., 'EUR'):").upper()
    if st.button("Convert"):
        if amount > 0 and from_currency and to_currency:
            converted_amount = convert_currency(amount, from_currency, to_currency)
            if converted_amount:
                st.markdown(f"<div class='output-box success-box'>{amount} {from_currency} = {converted_amount} {to_currency}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='output-box error-box'>Failed to retrieve currency conversion.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='output-box error-box'>Please enter valid amount and currency codes.</div>", unsafe_allow_html=True)

# End main container
st.markdown("</div>", unsafe_allow_html=True)
