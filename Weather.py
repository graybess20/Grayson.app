import streamlit as st
import requests

try:
    from gtts import gTTS
    from io import BytesIO
except Exception:  # pragma: no cover - optional dependency
    gTTS = None
    BytesIO = None


def get_city(city: str):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    try:
        data = requests.get(url, timeout=10).json()
    except Exception:
        return None

    if "results" in data and data["results"]:
        return data["results"][0]
    return None


def get_weather(lat: float, lon: float):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&current=temperature_2m,wind_speed_10m"
        "&daily=precipitation_probability_max"
    )
    try:
        return requests.get(url, timeout=10).json()
    except Exception:
        return None


def advice(temp: float, rain: float) -> str:
    if temp > 30:
        return "It is hot today. Drink water and stay cool."
    if temp < 10:
        return "It is cold today. Wear warm clothes."
    if rain > 50:
        return "Rain is likely. Carry an umbrella."
    return "The weather looks good. Enjoy your day!"


def extract_weather_metrics(weather: dict):
    if not weather:
        return None

    current = weather.get("current") or weather.get("current_weather") or {}
    daily = weather.get("daily") or {}
    precipitation = daily.get("precipitation_probability_max") or []

    if not current:
        return None

    temp_c = current.get("temperature_2m")
    wind = current.get("wind_speed_10m")
    rain = precipitation[0] if precipitation else None

    if temp_c is None or wind is None or rain is None:
        return None

    return {
        "temp_c": temp_c,
        "temp_f": round(temp_c * 9 / 5 + 32, 1),
        "wind": wind,
        "rain": rain,
    }


def parse_weather_payload(weather: dict):
    return extract_weather_metrics(weather)


def speak(text: str):
    if gTTS is None or BytesIO is None:
        return None
    audio = BytesIO()
    tts = gTTS(text)
    tts.write_to_fp(audio)
    audio.seek(0)
    return audio


def render_weather_app() -> None:
    st.subheader("🌦️ AI Weather Bot")
    st.write("Enter any city and get live weather + AI advice.")

    city = st.text_input("Enter city:", "New York")

    if st.button("Check Weather"):
        if not city.strip():
            st.warning("Please enter a city name.")
            return

        place = get_city(city)
        if not place:
            st.error("City not found.")
            return

        lat = place["latitude"]
        lon = place["longitude"]
        weather = get_weather(lat, lon)
        parsed_weather = parse_weather_payload(weather)
        if not parsed_weather:
            st.error("Unable to fetch weather data right now.")
            return

        temp_c = parsed_weather["temp_c"]
        temp_f = parsed_weather["temp_f"]
        wind = parsed_weather["wind"]
        rain = parsed_weather["rain"]
        msg = advice(temp_c, rain)

        st.success(
            f"""
📍 {city}

🌡️ Temperature: {temp_c}°C | {temp_f}°F
💨 Wind: {wind} km/h
☔️ Rain: {rain}%

🤖 AI Advice: {msg}
"""
        )

        speech = (
            f"The temperature in {city} is {temp_c} degrees Celsius, "
            f"or {temp_f} degrees Fahrenheit. Rain probability is {rain} percent. {msg}"
        )
        audio = speak(speech)
        if audio is not None:
            st.audio(audio, format="audio/mp3")
        else:
            st.caption("Audio playback is unavailable because the optional gTTS package is not installed.")