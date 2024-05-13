import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import io
import asyncio

# Function to get document from URL
def get_doc(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        doc = BeautifulSoup(response.text, 'html.parser')
        return doc
    except Exception as e:
        st.error(f"Failed to load page: {e}")
        return None

# Function to scrape data from a single page
def scrape_single_page(url):
    doc = get_doc(url)
    if doc:
        titles = get_book_titles(doc)
        prices = get_book_price(doc)
        stocks_availability = get_stock_availability(doc)
        urls = get_book_url(doc.find_all('h3'))
        return titles, prices, stocks_availability, urls
    return [], [], [], []

# Function to get book titles
def get_book_titles(doc):
    return [tag.text for tag in doc.find_all('h3')]

# Function to get book prices
def get_book_price(doc):
    return [tag.text.replace('Â', '') for tag in doc.find_all('p', class_='price_color')]

# Function to get stock availability
def get_stock_availability(doc):
    return [tag.text.strip() for tag in doc.find_all('p', class_='instock availability')]

# Function to get book URLs
def get_book_url(book_title_tags):
    book_urls = []
    for article in book_title_tags:
        for link in article.find_all('a', href=True):
            url = link['href']
            links = 'https://books.toscrape.com/' + url
            if links not in book_urls:
                book_urls.append(links)
    return book_urls

# Function to scrape data from multiple pages
async def scrape_multiple_pages(n):
    base_url = 'https://books.toscrape.com/catalogue/page-'
    tasks = [scrape_single_page(base_url + str(page) + '.html') for page in range(1, n+1)]
    return await asyncio.gather(*tasks)

# Streamlit App
def main():
    st.title('Book Data Analysis')
    n_pages = st.sidebar.slider("Select number of pages to scrape", 1, 10, 5)

    # Scrape data from multiple pages
    try:
        scraped_data = asyncio.run(scrape_multiple_pages(n_pages))
        st.write(scraped_data)  # Add this line to inspect the scraped data
    except Exception as e:
        st.error(f"An error occurred while scraping: {e}")
        return

    # Convert scraped data to DataFrame
    try:
        titles, prices, stocks_availability, urls = zip(*scraped_data)
    except Exception as e:
        st.error(f"Error in zipping scraped data: {e}")
        return
        
    # Convert scraped data to DataFrame
    titles, prices, stocks_availability, urls = zip(*scraped_data)
    df = pd.DataFrame({
        'TITLE': [title for sublist in titles for title in sublist],
        'PRICE': [price for sublist in prices for price in sublist],
        'STOCK AVAILABILITY': [stock for sublist in stocks_availability for stock in sublist],
        'URL': [url for sublist in urls for url in sublist]
    })

    # Display histogram of prices
    df['PRICE'] = df['PRICE'].str.replace('£', '').astype(float)
    fig, ax = plt.subplots()
    ax.hist(df['PRICE'], bins=20, color='skyblue', edgecolor='black')
    ax.set_xlabel('Price (£)')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Book Prices')
    st.pyplot(fig)

    # Display histogram of stock availability
    st.subheader('Distribution of Stock Availability')
    fig2, ax2 = plt.subplots()
    df['STOCK AVAILABILITY'].value_counts().plot(kind='bar', color='skyblue', edgecolor='black', ax=ax2)
    ax2.set_xlabel('Stock Availability')
    ax2.set_ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig2)

if __name__ == '__main__':
    main()
