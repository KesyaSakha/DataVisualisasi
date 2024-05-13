import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import io

# Fungsi untuk mengambil dokumen HTML dari URL
def get_doc(url):
    response = requests.get(url)
    doc = BeautifulSoup(response.text, 'html.parser')
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(response))
    return doc

# Fungsi untuk mendapatkan judul buku
def get_book_titles(doc):
    book_title_tags = doc.find_all('h3')
    book_titles = []
    for tag in book_title_tags:
        book_titles.append(tag.text)
    return book_titles

# Fungsi untuk mendapatkan harga buku
def get_book_price(doc):
    book_price_tags = doc.find_all('p', class_='price_color')
    book_prices = []
    for tag in book_price_tags:
        book_prices.append(tag.text.replace('Â', ''))
    return book_prices

# Fungsi untuk mendapatkan ketersediaan stok buku
def get_stock_availability(doc):
    book_stock_tags = doc.find_all('p', class_='instock availability')
    book_stock = []
    for tag in book_stock_tags:
        book_stock.append(tag.text.strip())
    return book_stock

# Fungsi untuk mendapatkan URL buku
def get_book_url(book_title_tags):
    book_urls = []
    for article in book_title_tags:
        for link in article.find_all('a', href=True):
            url = link['href']
            links = 'https://books.toscrape.com/' + url
            if links not in book_urls:
                book_urls.append(links)
    return book_urls

# Fungsi untuk melakukan scraping data dari beberapa halaman
def scrape_multiple_pages(n):
    base_url = 'https://books.toscrape.com/catalogue/page-'
    titles, prices, stocks_availability, urls = [], [], [], []
    
    for page in range(1, n+1):
        doc = get_doc(base_url + str(page) + '.html')
        titles.extend(get_book_titles(doc))
        prices.extend(get_book_price(doc))
        stocks_availability.extend(get_stock_availability(doc))
        urls.extend(get_book_url(doc.find_all('h3')))
        
    book_dict = {
        'TITLE': titles,
        'PRICE': prices,
        'STOCK AVAILABILITY': stocks_availability,
        'URL': urls
    }
    return pd.DataFrame(book_dict)

# Aplikasi Streamlit
def main():
    st.title('Book Data Analysis')

    # Scraping data dari multiple pages
    df = scrape_multiple_pages(5)

    # Tampilkan histogram dari kolom 'PRICE'
    df['PRICE'] = df['PRICE'].str.replace('£', '').astype(float) # Mengubah harga menjadi tipe data numerik
    fig, ax = plt.subplots()
    ax.hist(df['PRICE'], bins=20, color='skyblue', edgecolor='black')
    ax.set_xlabel('Price (£)')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Book Prices')
    
    # Simpan gambar histogram sebagai BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Tampilkan gambar histogram di Streamlit
    st.image(buffer)

    # Tampilkan histogram dari kolom 'STOCK AVAILABILITY'
    st.subheader('Distribution of Stock Availability')
    fig2, ax2 = plt.subplots()
    df['STOCK AVAILABILITY'].value_counts().plot(kind='bar', color='skyblue', edgecolor='black', ax=ax2)
    ax2.set_xlabel('Stock Availability')
    ax2.set_ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig2)

if __name__ == '__main__':
    main()
