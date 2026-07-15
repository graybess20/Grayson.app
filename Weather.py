import streanlit as st
import requests
from gtts import gTTS
from io import BytesIO


st.set_page_config(
    page_title="AI Weather Bot",
    page_icon="🌦️"
)

st.title("🌦️ AI Weather Bot")
st.write("Enter any city and get live weather + AI advice.")


def get_city(city):

    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"

    data = requests.get(url).json()

    if "results" in data:
        return data["results"][0]
    
    return None


def get_weather(lat, lon):

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&current=temperature_2m,wind_speed_10m"
        "&daily=precipitation_probability_max"
    )

    return requests.get(url).json()


def advice(temp, rain):

    if temp > 30:
        return "It is hot today. Drink water and stay cool."
    
    elif temp < 10:
        return "It is cold today. Wear warm clothes."
    
    elif rain > 50:
        return "Rain is likely. Carry an umbrella."
    
    else:
        return "The weather looks good. Enjoy your day!"
    

    def speak(text):
        
        audio = BytesIO()

        tts = gTTs(text)

        tts.write_to_fp(audio)

        return audio
    

    city = st.text_input(
        "Enter city:",
        "New York"
    )


    if st.button("Check Weather"):

        place = get_city(city)


        if place:

            lat = place["latitude"]
            lon = place["longitude"]

            weather = get_weather(
                lat,
                lon
            )


            temp_c = weather["current_weather"]["temperature_2m"]

            temp_f = round(
                temp_c * 9 / 5 + 32,
                1
            )

            wind = weather["current"]_weather"]["wind_speed_10m"]

            rain = weather["daily"]["precipitation_probability_max"][0]


            msg = advice(
                temp_c,
                rain
            )


            st.success(
                f"""
    📍 {city}

🌡️ Temperature:
{temp_c}°C | {temp_f}°F

💨 Wind:
{wind} km/h

☔️ Rain:
{rain}%

🤖 AI Advice:
{msg}
"""
        )
            

        speech = f"""
        The temperature in {city} is
        {temp_c} degrees Celsius,
        or {temp_f} degrees Fahrenheit.
        
        Rain probability is {rain} percent.

        {msg}
        """


        audio = speak(speech)


        st.audio(
            audio,
            format="audio/mp3"
        )

    else:
        st.error("City not found.")