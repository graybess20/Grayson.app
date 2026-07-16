import streamlit as st


def _get_openai_client():
    try:
        from openai import OpenAI
    except Exception:
        return None

    try:
        api_key = st.secrets.get("OpenAI_Key", "")
    except Exception:
        api_key = ""

    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def render_translation_app() -> None:
    st.subheader("🌎 AI Language Translator")
    st.write("Translate English text into a few common languages.")

    languages = {
        "French": "fr",
        "German": "de",
        "Spanish": "es",
        "Italian": "it",
    }

    target_language = st.selectbox("Select Language", list(languages.keys()))
    text = st.text_area("Enter English Text", placeholder="Hello, how are you today?")

    if st.button("Translate"):
        if not text.strip():
            st.warning("Please enter some text to translate.")
            return

        client = _get_openai_client()
        if client is None:
            st.info("Set the OpenAI_Key secret for AI translation, or use the built-in fallback.")
            fallback = {
                "French": "Bonjour, comment allez-vous aujourd'hui ?",
                "German": "Hallo, wie geht es Ihnen heute?",
                "Spanish": "Hola, ¿cómo estás hoy?",
                "Italian": "Ciao, come stai oggi?",
            }
            st.success(fallback[target_language])
            return

        with st.spinner("Translating..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You translate English text into the requested language and return only the translation.",
                        },
                        {
                            "role": "user",
                            "content": f"Translate this text to {target_language}: {text}",
                        },
                    ],
                )
                result = response.choices[0].message.content.strip()
            except Exception as exc:
                st.error(f"Translation failed: {exc}")
                return

        st.success(result)
