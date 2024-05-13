import streamlit as st
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from googletrans import Translator
import os

# Fungsi untuk membaca teks dalam bahasa Inggris
def read_english(text):
    english_tts = gTTS(text=text, lang='en')
    english_tts.save("english.mp3")
    if os.path.exists("english.mp3"):
        st.success("English audio file successfully created.")
        sound = AudioSegment.from_mp3("english.mp3")
        play(sound)
    else:
        st.error("Error: Failed to create English audio file.")
        
# Fungsi untuk membaca teks dalam bahasa Indonesia
def read_indonesian(text):
    indonesian_tts = gTTS(text=text, lang='id')
    indonesian_tts.save("indonesian.mp3")
    sound = AudioSegment.from_mp3("indonesian.mp3")
    play(sound)

# Fungsi untuk menerjemahkan teks dari bahasa Inggris ke bahasa Indonesia
def translate_to_indonesian(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='id').text
    return translated_text

# Konten Streamlit
st.title("Text-to-Speech Translator")

english_text = "This company was founded in 2010 by the infamous movie star, Graeme Alexander. Currently, the company worths USD 1 billion according to Forbes report in 2023. What an achievement in just 13 years."

translated_text = translate_to_indonesian(english_text)

st.header("English Text")
st.write(english_text)
if st.button("Read English"):
    read_english(english_text)

st.header("Indonesian Translation")
st.write(translated_text)
if st.button("Read Indonesian"):
    read_indonesian(translated_text)
