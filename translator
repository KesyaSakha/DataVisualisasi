import time
from gtts import gTTS
import os

# Teks yang akan diterjemahkan dan diubah menjadi suara
text = "This company was founded in 2010 by the infamous movie star, \
          Graeme Alexander. Currently, the company worths USD 1 billion \
          according to Forbes report in 2023. What an achievement in just \
          13 years."

# Import library untuk terjemahan
import translators as ts

# Terjemahkan teks ke bahasa Indonesia
hasil = ts.translate(text, to_language="id")

# Print terjemahan
print(hasil)

# Inisialisasi mesin Text-to-Speech untuk bahasa Indonesia
engine = gTTS(text=hasil, lang='id', slow=False)

# Simpan terjemahan dalam format audio
engine.save("hasil_terjemahan.mp3")

# Putar terjemahan
os.system("start hasil_terjemahan.mp3")
