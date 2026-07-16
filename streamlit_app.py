import importlib.util
import sys
from pathlib import Path

import streamlit as st

APP_ROOT = Path(__file__).resolve().parent
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))


def load_local_module(module_name: str):
    module_path = APP_ROOT / f"{module_name}.py"
    if not module_path.exists():
        raise FileNotFoundError(f"Unable to find module file for {module_name} at {module_path}")

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ModuleNotFoundError(f"Unable to load module {module_name}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


story_module = load_local_module("storygen")
language_module = load_local_module("languagetranslator")
weather_module = load_local_module("Weather")

render_story_app = story_module.render_story_app
render_translation_app = language_module.render_translation_app
render_weather_app = weather_module.render_weather_app

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
