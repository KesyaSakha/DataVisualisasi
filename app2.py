import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Database connection
dialect = "mysql"
driver = "pymysql"
username = "root"
password = ""
host = "localhost"
port = "3306"
database = "aw"

# Connection string
connection_string = f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(connection_string)

# Query untuk mengambil data penjualan produk
query = """
    SELECT DISTINCT dp.EnglishProductName, SUM(fs.SalesAmount) AS TotalSales
    FROM factinternetsales AS fs
    INNER JOIN dimproduct AS dp ON fs.ProductKey = dp.ProductKey
    GROUP BY dp.EnglishProductName
    ORDER BY TotalSales DESC
    LIMIT 10
"""

# Baca data ke dalam DataFrame dengan Pandas
sales_df = pd.read_sql_query(query, engine)

# Tampilkan plot menggunakan Streamlit
st.title('Top 10 Products by Total Sales')

# Visualisasi 1: Bar Chart (Horizontal)
st.subheader('Bar Chart')
st.bar_chart(sales_df.set_index('EnglishProductName'))

# Visualisasi 2: Pie Chart
st.subheader('Pie Chart')
fig, ax = plt.subplots()
ax.pie(sales_df['TotalSales'], labels=sales_df['EnglishProductName'], autopct='%1.1f%%', startangle=140)
ax.axis('equal')  # Memastikan pie chart berbentuk lingkaran
st.pyplot(fig)
