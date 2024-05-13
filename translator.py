import streamlit as st
from gtts import gTTS
import os

# Function to speak text
def speak(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    os.system("ffplay -nodisp -autoexit output.mp3")

# Main function
def main():
    st.title("Text-to-Speech with Streamlit")

    # Text input
    text = st.text_area("Enter text", "Type here...")

    # Language selection
    language = st.radio("Select language", ["English", "Indonesian"])

    # Text-to-Speech button
    if st.button("Listen"):
        if text:
            lang_code = "en" if language == "English" else "id"
            speak(text, lang_code)

if __name__ == "__main__":
    main()
