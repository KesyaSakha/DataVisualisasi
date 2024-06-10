import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Database connection configuration
config = {
  'user': 'root',
  'password': '',
  'host': 'localhost',
  'port': '3306',
  'database': 'aw'
}

# Connect to the database
try:
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
    # ...
except Exception as e:
    st.error(f"An error occurred: {e}")
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

# Definisikan palet warna kustom sebagai daftar string
custom_palette = ['pink', 'purple', 'skyblue', 'lightblue', 'lavender', 'thistle', 'lightpink', 'lightgreen', 'lightskyblue', 'violet']

# Atur palet warna kustom
sns.set_palette(custom_palette)

# Visualisasi 1: Bar Chart (Horizontal)
plt.figure(figsize=(10, 6))
plt.barh(sales_df['EnglishProductName'], sales_df['TotalSales'])
plt.xlabel('Total Sales')
plt.ylabel('Product Name')
plt.title('Top 10 Products by Total Sales (Bar Chart)')
plt.tight_layout()
plt.show()

# Visualisasi 2: Pie Chart
plt.figure(figsize=(8, 8))
plt.pie(sales_df['TotalSales'], labels=sales_df['EnglishProductName'], autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Memastikan pie chart berbentuk lingkaran
plt.title('Top 10 Products by Total Sales (Pie Chart)')
plt.tight_layout()
plt.show()

# Connection string
connection_string = f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(connection_string)

# Query untuk mengambil data StandardCost dan ListPrice
query = """
    SELECT StandardCost, ListPrice
    FROM dimproduct
"""

# Baca data ke dalam DataFrame
product_df = pd.read_sql_query(query, engine)

# Atur palet warna kustom
custom_palette = ['pink', 'purple', 'skyblue', 'lightblue', 'lavender', 'thistle', 'lightpink', 'lightcoral', 'lightskyblue', 'violet']
sns.set_palette(custom_palette)

# Visualisasi: Scatter Plot dengan Garis Regresi
plt.figure(figsize=(10, 6))
sns.regplot(x='StandardCost', y='ListPrice', data=product_df, scatter_kws={'color': 'skyblue'}, line_kws={'color': 'red'})
plt.title('Relationship between Standard Cost and List Price')
plt.xlabel('Standard Cost')
plt.ylabel('List Price')
plt.grid(True)
plt.tight_layout()
plt.show()

# Visualisasi: Pair Plot untuk eksplorasi hubungan antara variabel
sns.pairplot(product_df)
plt.title('Pair Plot of Product Variables')
plt.tight_layout()
plt.show()


# Query untuk mengambil data komposisi produk berdasarkan ProductLine
query = """
    SELECT ProductLine, COUNT(*) AS TotalProducts
    FROM dimproduct
    GROUP BY ProductLine
"""

# Baca data ke dalam DataFrame
product_line_df = pd.read_sql_query(query, engine)

# Visualisasi: Bar Chart
plt.figure(figsize=(10, 6))
plt.bar(product_line_df['ProductLine'], product_line_df['TotalProducts'], color='lightpink')
plt.title('Composition of Products by Product Line')
plt.xlabel('Product Line')
plt.ylabel('Total Products')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Query untuk mengambil data komposisi produk berdasarkan warna (Color)
query_color = """
    SELECT Color, COUNT(*) AS TotalProducts
    FROM dimproduct
    GROUP BY Color
"""

# Baca data ke dalam DataFrame
color_df = pd.read_sql_query(query_color, engine)

# Visualisasi: Pie Chart
plt.figure(figsize=(8, 8))
plt.pie(color_df['TotalProducts'], labels=color_df['Color'], autopct='%1.1f%%', startangle=140, colors=['pink', 'purple', 'skyblue', 'lightblue', 'lavender', 'thistle', 'lightpink', 'lightcoral', 'lightskyblue', 'violet'])
plt.axis('equal')  # Memastikan pie chart berbentuk lingkaran
plt.title('Composition of Products by Color')
plt.tight_layout()
plt.show()

# Query untuk mengambil data yang akan divisualisasikan
query = """
    SELECT ListPrice
    FROM dimproduct
    WHERE ListPrice IS NOT NULL
"""

# Baca data ke dalam DataFrame dengan Pandas
data_df = pd.read_sql_query(query, engine)

# Visualisasi: Histogram
plt.figure(figsize=(10, 6))
plt.hist(data_df['ListPrice'], bins=20, color='pink', edgecolor='black')
plt.xlabel('List Price')
plt.ylabel('Frequency')
plt.title('Distribution of Product List Prices')
plt.grid(True)
plt.tight_layout()
plt.show()

# Visualisasi: KDE Plot
plt.figure(figsize=(10, 6))
sns.kdeplot(list_price_df['ListPrice'], fill=True, color='purple')
plt.xlabel('List Price')
plt.ylabel('Density')
plt.title('Kernel Density Estimate of Product List Prices')
plt.grid(True)
plt.tight_layout()
plt.show()

# Read CSV files into dataframes
df = pd.read_csv('imdb_combined_data2.csv')
# df.astype("string")

# df.keys()

df['Rating'] = df['Rating'].astype("string")
# df['Rating']

df['Name'] = df['Name'].astype("string")
# df['Name']

df['Year'] = pd.to_numeric(df['Year'])
# df['Year']

# 1. COMPARISON CHART - BAR CHART
# Raw Data Preparation
# Take 3 columns from panda dataframe, sorted by Rating
st.write("1. COMPARISON CHART - BAR CHART")
df_sel = df[['Rating','Gross_US', 'Gross_World']].sort_values(by=['Rating'])

# Drop rows with all zeros
hsl = df_sel.loc[(df_sel[['Gross_US', 'Gross_World']] != 0).all(axis=1)]
# df_sel

# Prepare the chart data from panda dataframe for BAR CHART
# X axis = Rating
# Y1 axis= Gross US, Y2 axis = Gross World
chart_data = pd.DataFrame(
    {
        "Rating": hsl['Rating'], "Gross US": hsl['Gross_US'], "Gross World":hsl['Gross_World']}
)

# BAR CHART (call the bar_chart using the chart_data, while defining label)
st.bar_chart(
   chart_data, x="Rating", y=["Gross US", "Gross World"], color=["#FF0000", "#0000FF"]  # Optional
)

# 2. RELATIONSHIP CHART - SCATTER PLOT
# Raw Data Preparation
# Take 4 columns from panda dataframe, sorted by Rating
st.write("2. RELATIONSHIP CHART - SCATTER PLOT")
df_sel2 = df[['Gross_US','Gross_World','Durasi(Menit)','Budget','Rating']].sort_values(by=['Durasi(Menit)'])

# Drop rows with all zeros
hsl = df_sel2.loc[(df_sel2[['Gross_US', 'Gross_World']] != 0).all(axis=1)]

# Scale down the numbers in 3 columns, dividing it by 1 million
hsl['Gross_US'] = hsl['Gross_US']/1000000
hsl['Gross_World'] = hsl['Gross_World']/1000000
hsl['Budget'] = hsl['Budget']/1000000

# Prepare the data for plotting
chart_data2 = pd.DataFrame(hsl, columns=["Gross_US", "Gross_World", "Durasi(Menit)", "Budget", "Rating"])

# In this case, I wanted to know the relation between X = Durasi(Menit) and Y = (Budget and Gross Sales in US). Sementara Gross_World digunakan untuk ukuran lingkaran yang akan ditampilkan
st.scatter_chart(
    chart_data2, 
    x='Durasi(Menit)',
    y=['Budget','Gross_US'],
    size='Gross_World',
    color=['#FF0000', '#0000FF'],  # Optional
    # color = ['Rating']
)

# 3. COMPOSITION CHART - DONUT CHART
# Raw Data Preparation
# Take 4 columns from panda dataframe, sorted by Rating
st.write("3. COMPOSITION CHART - DONUT CHART")
df_sel3 = df[['Gross_US','Gross_World','Budget','Rating']].sort_values(by=['Rating'])

# Drop rows with all zeros
hsl = df_sel3.loc[(df_sel3[['Gross_US', 'Gross_World']] != 0).all(axis=1)]
hsl = hsl.groupby(['Rating']).sum()

# Creating plot
fig = plt.figure(figsize=(10, 7))
explode = [0,0.1,0,0.1]
plt.pie(hsl['Gross_US'], labels = hsl.index, explode = explode, autopct='%1.1f%%',
        shadow=False, startangle=90)
plt.axis('equal')
 
# show plot
st.pyplot(fig)

# 4. DISTRIBUTION - LINE CHART
st.write("4. DISTRIBUTION - LINE CHART")
st.line_chart(
    chart_data2, 
    x='Durasi(Menit)',
    y=['Budget','Gross_US'],
    color=['#FF0000', '#0000FF'],  # Optional
    # color = ['Rating']
)
