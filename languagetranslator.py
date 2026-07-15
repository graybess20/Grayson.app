import streamlit as st
from languagetranslator import pipeline

st.set_page_config(page_title="Language Translator", page_icon="🌎")

st.title("🌎 AI Language Translator")
st.write("Translate English into different languages.")

@st.cache_resource
def load_model():
    return pipeline(
        "translation",
        model="Helsinki-NLP/opus-mt-en-Fr"
    )

translator = load_model()

languages = {
    "French":"Helsinki-NLP/opus-mt-en-fr",
    "German":"Helsinki-NLP/opus-mt-en-de",
    "Spanish":"Helsinki-NLP/opus-mt-en-es",
    "Italian":"Helsinki-NLP/opus-mt-en-it",

}

Language = st.selectbox(
    "Select Language",
    List(languages.keys())
)

text = st.text_area("Enter English Text")

if st.button("Translate"):
    with st.spinner("Loading model..."):

        translator = pipeline(
            "translation",
            model=languages[Language]
        )

        result = translator(text)