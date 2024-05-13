from gtts import gTTS
import os

# Teks yang akan diterjemahkan dan diubah menjadi suara
text = "This company was founded in 2010 by the infamous movie star, \
          Graeme Alexander. Currently, the company worths USD 1 billion \
          according to Forbes report in 2023. What an achievement in just \
          13 years."

# Terjemahkan teks ke bahasa Indonesia
translator = gTTS(text=text, lang='en')
translation = translator.get_urls(lang='id')[0]

# Putar terjemahan
os.system("mpv " + translation)
