
import json
import requests
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Language Translation Tool",
    page_icon="🌍",
    layout="centered"
)

LANGUAGES = {
    "Auto Detect": "autodetect",
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Punjabi": "pa",
    "Marathi": "mr",
    "Tamil": "ta",
    "Telugu": "te",
    "Gujarati": "gu",
    "Urdu": "ur",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh-CN",
    "Arabic": "ar",
    "Portuguese": "pt",
    "Russian": "ru"
}


def translate_text(text, source, target):
    # MyMemory's anonymous endpoint requires explicit language pairs.
    # For auto-detection, try the likely source languages.
    sources = (
        ["en", "hi", "fr", "es", "de"]
        if source == "autodetect"
        else [source]
    )

    last_error = None

    for source_code in sources:
        try:
            response = requests.get(
                "https://api.mymemory.translated.net/get",
                params={
                    "q": text,
                    "langpair": f"{source_code}|{target}"
                },
                timeout=15
            )
            response.raise_for_status()
            data = response.json()

            if data.get("responseStatus") == 200:
                result = data.get(
                    "responseData", {}
                ).get("translatedText", "")

                if result:
                    return result

            last_error = data.get(
                "responseDetails",
                "No translation returned."
            )

            if source != "autodetect":
                break

        except requests.RequestException as error:
            last_error = str(error)
            break

    raise RuntimeError(str(last_error))


def show_copy_button(text):
    safe_text = json.dumps(text, ensure_ascii=True)

    components.html(
        f"""
        <button id="copy" style="
            width:100%; padding:12px; border:0;
            border-radius:8px; background:#2563eb;
            color:white; cursor:pointer; font-size:15px;
        ">📋 Copy Translation</button>

        <script>
        const text = {safe_text};
        document.getElementById("copy").onclick = async () => {{
            try {{
                await navigator.clipboard.writeText(text);
                document.getElementById("copy").innerText =
                    "Copied successfully!";
            }} catch (e) {{
                document.getElementById("copy").innerText =
                    "Copy unavailable — select the text manually";
            }}
        }};
        </script>
        """,
        height=52
    )


def show_speech_button(text, language):
    safe_text = json.dumps(text, ensure_ascii=True)
    safe_language = json.dumps(language)

    components.html(
        f"""
        <button id="speak" style="
            width:100%; padding:12px; border:0;
            border-radius:8px; background:#15803d;
            color:white; cursor:pointer; font-size:15px;
        ">🔊 Listen to Translation</button>

        <script>
        const text = {safe_text};
        const lang = {safe_language};

        document.getElementById("speak").onclick = () => {{
            if (!window.speechSynthesis) {{
                alert("Speech is not supported by this browser.");
                return;
            }}

            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = lang;
            window.speechSynthesis.speak(utterance);
        }};
        </script>
        """,
        height=52
    )


st.title("🌍 Language Translation Tool")
st.write("Translate text between different languages.")

st.info("Enter your text, select languages, and click Translate.")

with st.form("translation_form"):
    input_text = st.text_area(
        "Enter text to translate",
        placeholder="Example: How are you today?",
        height=150
    )

    col1, col2 = st.columns(2)

    with col1:
        source = st.selectbox(
            "Translate from",
            list(LANGUAGES.keys())
        )

    with col2:
        targets = [
            name for name in LANGUAGES
            if name != "Auto Detect"
        ]
        target = st.selectbox(
            "Translate into",
            targets,
            index=1
        )

    submitted = st.form_submit_button(
        "🌐 Translate",
        use_container_width=True
    )

if submitted:
    if not input_text.strip():
        st.warning("Please enter some text.")

    elif source == target:
        st.warning("Select two different languages.")

    elif len(input_text.encode("utf-8")) > 450:
        st.warning(
            "Please shorten your text to 450 UTF-8 bytes "
            "or less for this demo."
        )

    else:
        try:
            with st.spinner("Translating..."):
                result = translate_text(
                    input_text.strip(),
                    LANGUAGES[source],
                    LANGUAGES[target]
                )

            st.subheader("Translated Text")
            st.text_area(
                "Translation result",
                value=result,
                height=150
            )

            left, right = st.columns(2)

            with left:
                show_copy_button(result)

            with right:
                show_speech_button(
                    result,
                    LANGUAGES[target]
                )

            st.success("Translation completed!")

        except Exception as error:
            st.error(
                "Translation failed. The service may be "
                "unavailable or may have rejected the request."
            )
            with st.expander("Technical details"):
                st.code(str(error))

st.divider()
st.caption(
    "Built with Python, Streamlit and MyMemory Translation API. "
    "Requires an internet connection. Free service availability "
    "and translation quality are not guaranteed."
)
