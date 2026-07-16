import sys
from pathlib import Path

import streamlit as st

APP_ROOT = str(Path(__file__).resolve().parent)
if APP_ROOT not in sys.path:
    sys.path.insert(0, APP_ROOT)

from storygen import render_story_app
from languagetranslator import render_translation_app
from Weather import render_weather_app

st.set_page_config(page_title="AI Toolkit", page_icon="✨", layout="wide")

st.title("✨ AI Toolkit")
st.write("A single Streamlit home page with three apps: story generation, translation, and weather.")

try:
    api_key = st.secrets.get("OpenAI_Key", "")
except Exception:
    api_key = ""

if api_key:
    st.info("OpenAI is configured. AI features will use your secret key.")
else:
    st.info("Add an OpenAI key to Streamlit secrets as OpenAI_Key to enable AI generation and translation.")

story_tab, translate_tab, weather_tab = st.tabs(["📖 Story Generator", "🌎 Translator", "🌦️ Weather Bot"])

with story_tab:
    render_story_app()

with translate_tab:
    render_translation_app()

with weather_tab:
    render_weather_app()
