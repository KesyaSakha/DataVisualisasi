import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Memuat data dari file CSV
df = pd.read_csv('film_data_2024.csv')

# Membersihkan kolom 'Pendapatan' agar hanya berisi angka
df['Pendapatan'] = df['Pendapatan'].replace('-', 0)

# Mengonversi kolom 'Pendapatan' ke tipe data float
df['Pendapatan'] = df['Pendapatan'].replace('[\$,]', '', regex=True).astype(float)

# Menghitung total pendapatan per distributor
revenue_by_distributor = df.groupby('Distributor')['Pendapatan'].sum().sort_values(ascending=False)

# Fungsi untuk menampilkan deskripsi film dari distributor yang dipilih
def display_movie_description(selected_distributor):
    selected_movies = df[df['Distributor'] == selected_distributor]
    if not selected_movies.empty:
        st.write(selected_movies)
    else:
        st.write("Tidak ada film yang didistribusikan oleh", selected_distributor)

# Dropdown menu untuk memilih distributor
dropdown_options = list(revenue_by_distributor.index)
dropdown_options.sort()  # Mengurutkan nama distributor
dropdown_options.insert(0, 'Pilih Distributor')

# Dropdown menu di Streamlit
selected_distributor = st.selectbox('Pilih Distributor:', dropdown_options)
if selected_distributor != 'Pilih Distributor':
    display_movie_description(selected_distributor)

# Menampilkan pie chart menggunakan matplotlib di Streamlit
st.write('## Persentase Pendapatan per Distributor pada Tahun 2024')
colors = ['#FFC0CB', '#FF69B4', '#DDA0DD', '#9370DB', '#ADD8E6', '#87CEFA', '#B0C4DE', '#00BFFF', '#1E90FF', '#6495ED']
plt.figure(figsize=(10, 6))
plt.pie(revenue_by_distributor, labels=revenue_by_distributor.index, autopct='%1.1f%%', startangle=140, colors=colors)
plt.axis('equal')
st.pyplot(plt)
