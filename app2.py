import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pymysql

# Database connection
dialect = "mysql"
driver = "pymysql"  # sesuaikan driver dengan modul yang diimpor
username = "root"
password = ""
host = "localhost"
port = "3306"
database = "aw"

# Connection string
connection_string = f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(connection_string)

# Function to execute SQL queries
def execute_query(query):
    return pd.read_sql_query(query, engine)

# Function to display bar chart
def bar_chart(data, x, y, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    plt.barh(data[x], data[y])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    st.pyplot()

# Function to display pie chart
def pie_chart(data, labels, values, title):
    plt.figure(figsize=(8, 8))
    plt.pie(data[values], labels=data[labels], autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title(title)
    plt.tight_layout()
    st.pyplot()

# Function to display scatter plot
def scatter_plot(data, x, y, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    sns.regplot(x=x, y=y, data=data, scatter_kws={'color': 'skyblue'}, line_kws={'color': 'red'})
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot()

# Function to display pair plot
def pair_plot(data, title):
    sns.pairplot(data)
    plt.title(title)
    plt.tight_layout()
    st.pyplot()

# Function to display histogram
def histogram(data, column, bins, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    plt.hist(data[column], bins=bins, color='pink', edgecolor='black')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot()

# Function to display KDE plot
def kde_plot(data, column, fill, color, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data[column], fill=fill, color=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot()

# Main function
def main():
    st.title('Visualizations from XAMPP Database')

    # Query untuk mengambil data penjualan produk
    sales_query = """
        SELECT DISTINCT dp.EnglishProductName, SUM(fs.SalesAmount) AS TotalSales
        FROM factinternetsales AS fs
        INNER JOIN dimproduct AS dp ON fs.ProductKey = dp.ProductKey
        GROUP BY dp.EnglishProductName
        ORDER BY TotalSales DESC
        LIMIT 10
    """
    sales_df = execute_query(sales_query)
    st.subheader('Top 10 Products by Total Sales (Bar Chart)')
    bar_chart(sales_df, 'EnglishProductName', 'TotalSales', 'Top 10 Products by Total Sales (Bar Chart)', 'Total Sales', 'Product Name')

    st.subheader('Top 10 Products by Total Sales (Pie Chart)')
    pie_chart(sales_df, 'EnglishProductName', 'TotalSales', 'Top 10 Products by Total Sales (Pie Chart)')

    # Query untuk mengambil data StandardCost dan ListPrice
    product_query = """
        SELECT StandardCost, ListPrice
        FROM dimproduct
    """
    product_df = execute_query(product_query)

    st.subheader('Relationship between Standard Cost and List Price')
    scatter_plot(product_df, 'StandardCost', 'ListPrice', 'Relationship between Standard Cost and List Price', 'Standard Cost', 'List Price')

    st.subheader('Pair Plot of Product Variables')
    pair_plot(product_df, 'Pair Plot of Product Variables')

    # Query untuk mengambil data komposisi produk berdasarkan ProductLine
    product_line_query = """
        SELECT ProductLine, COUNT(*) AS TotalProducts
        FROM dimproduct
        GROUP BY ProductLine
    """
    product_line_df = execute_query(product_line_query)

    st.subheader('Composition of Products by Product Line')
    bar_chart(product_line_df, 'ProductLine', 'TotalProducts', 'Composition of Products by Product Line', 'Product Line', 'Total Products')

    # Query untuk mengambil data komposisi produk berdasarkan warna (Color)
    color_query = """
        SELECT Color, COUNT(*) AS TotalProducts
        FROM dimproduct
        GROUP BY Color
    """
    color_df = execute_query(color_query)

    st.subheader('Composition of Products by Color')
    pie_chart(color_df, 'Color', 'TotalProducts', 'Composition of Products by Color')

    # Query untuk mengambil data yang akan divisualisasikan
    data_query = """
        SELECT ListPrice
        FROM dimproduct
        WHERE ListPrice IS NOT NULL
    """
    data_df = execute_query(data_query)

    st.subheader('Distribution of Product List Prices (Histogram)')
    histogram(data_df, 'ListPrice', 20, 'Distribution of Product List Prices', 'List Price', 'Frequency')

    st.subheader('Kernel Density Estimate of Product List Prices (KDE Plot)')
    kde_plot(data_df, 'ListPrice', True, 'purple', 'Kernel Density Estimate of Product List Prices', 'List Price', 'Density')

if __name__ == "__main__":
    main()
