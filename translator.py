import streamlit as st
import pyttsx3
import time
import translators as ts

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Function to get available voices
def get_indonesian_voice():
    voices = engine.getProperty('voices')
    for voice in voices:
        if "indonesia" in voice.name.lower():
            return voice.id
    return None

# Function to speak text
def speak(text, lang='en'):
    engine.setProperty('voice', get_indonesian_voice() if lang == 'id' else None)
    engine.say(text)
    engine.runAndWait()

# Main function
def main():
    st.title("Text Translator & Text-to-Speech")

    # Text input
    text = st.text_area("Enter text in English")

    # Translate button
    if st.button("Translate to Indonesian"):
        if text:
            st.write("Translation in Indonesian:")
            translation = ts.translate(text, to_language="id")
            st.write(translation)
            speak("Translation in Indonesian:", 'en')
            speak(translation, 'id')

    # Text-to-Speech button
    if st.button("Listen to English Text"):
        if text:
            speak(text)

if __name__ == "__main__":
    main()
