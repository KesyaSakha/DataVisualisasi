import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
import toml
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
import pymysql
from mysql.connector import Error
from pymysql import Error

# Load database connection info from secrets.toml
secrets = toml.load('secrets.toml')
db_config = secrets['connections']['mydb']

# Function to execute MySQL query
def execute_query_mysql(query):
    try:
        db_connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['username'],
            password=db_config['password'],
            database=db_config['database'],
            port=int(db_config['port'])
        )
        cursor = db_connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return result
    except Error as e:
        st.error(f"Error while connecting to MySQL: {e}")
        return None
# Function to display bar chart
def bar_chart(data, x, y, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(data[x], data[y])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.tight_layout()
    st.pyplot(fig)

# Function to display pie chart
def pie_chart(data, labels, values, title):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(data[values], labels=data[labels], autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    ax.set_title(title)
    plt.tight_layout()
    st.pyplot(fig)

# Function to display scatter plot
def scatter_plot(data, x, y, title, xlabel, ylabel):
    # Convert decimal.Decimal to float
    data[x] = data[x].astype(float)
    data[y] = data[y].astype(float)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(x=x, y=y, data=data, scatter_kws={'color': 'skyblue'}, line_kws={'color': 'red'}, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)


# Function to display bubble plot
def bubble_plot(data, x, y, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(data[x], data[y], alpha=0.5)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    st.pyplot(fig)




# Function to display histogram
def histogram(data, column, bins, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(data[column], bins=bins, color='pink', edgecolor='black')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

# Function to display KDE plot
def kde_plot(data, column, fill, color, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.kdeplot(data[column], fill=fill, color=color, ax=ax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

# Main function
def main():
    st.title('Visualizations from XAMPP Database')

    # Query to retrieve product sales data
    sales_query = """
        SELECT DISTINCT dp.EnglishProductName, SUM(fs.SalesAmount) AS TotalSales
        FROM factinternetsales AS fs
        INNER JOIN dimproduct AS dp ON fs.ProductKey = dp.ProductKey
        GROUP BY dp.EnglishProductName
        ORDER BY TotalSales DESC
        LIMIT 10
    """
    sales_df = pd.DataFrame(execute_query_mysql(sales_query), columns=['EnglishProductName', 'TotalSales'])
    st.subheader('Top 10 Products by Total Sales (Bar Chart)')
    bar_chart(sales_df, 'EnglishProductName', 'TotalSales', 'Top 10 Products by Total Sales (Bar Chart)', 'Total Sales', 'Product Name')

    st.subheader('Top 10 Products by Total Sales (Pie Chart)')
    pie_chart(sales_df, 'EnglishProductName', 'TotalSales', 'Top 10 Products by Total Sales (Pie Chart)')

    # Query to retrieve StandardCost and ListPrice data
    product_query = """
        SELECT StandardCost, ListPrice
        FROM dimproduct
    """
    product_df = pd.DataFrame(execute_query_mysql(product_query), columns=['StandardCost', 'ListPrice'])

    st.subheader('Relationship between Standard Cost and List Price')
    scatter_plot(product_df, 'StandardCost', 'ListPrice', 'Relationship between Standard Cost and List Price', 'Standard Cost', 'List Price')

    st.subheader('Bubble Plot of Product Variables')
    bubble_plot(product_df, 'StandardCost', 'ListPrice',  'Bubble Plot of Product Variables', 'Standard Cost', 'List Price')


    # Query to retrieve product composition data by ProductLine
    product_line_query = """
        SELECT ProductLine, COUNT(*) AS TotalProducts
        FROM dimproduct
        GROUP BY ProductLine
    """
    product_line_df = pd.DataFrame(execute_query_mysql(product_line_query), columns=['ProductLine', 'TotalProducts'])

    st.subheader('Composition of Products by Product Line')
    bar_chart(product_line_df, 'ProductLine', 'TotalProducts', 'Composition of Products by Product Line', 'Product Line', 'Total Products')


    # Query to retrieve data to be visualized
    data_query = """
        SELECT ListPrice
        FROM dimproduct
        WHERE ListPrice IS NOT NULL
    """
    data_df = pd.DataFrame(execute_query_mysql(data_query), columns=['ListPrice'])

    st.subheader('Distribution of Product List Prices (Histogram)')
    histogram(data_df, 'ListPrice', 20, 'Distribution of Product List Prices', 'List Price', 'Frequency')
    st.subheader('Kernel Density Estimate of Product List Prices (KDE Plot)')
    kde_plot(data_df, 'ListPrice', True, 'purple', 'Kernel Density Estimate of Product List Prices', 'List Price', 'Density')

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

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
hsl
# df_sel

# Scale down the numbers in 3 columns, dividing it by 1 million
# df_sel2['Gross_US'] = df_sel2['Gross_US']/1000000
# df_sel2['Gross_World'] = df_sel2['Gross_World']/1000000
# df_sel2['Budget'] = df_sel2['Budget']/1000000

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
# df_sel
hsl = hsl.groupby(['Rating']).sum()
hsl

 
label = df_sel3.Rating.unique()
# label
# Creating plot
fig = plt.figure(figsize=(10, 7))
explode = [0,0.1,0,0.1]
plt.pie(hsl['Gross_US'], labels = hsl.index, explode = explode, autopct='%1.1f%%',
        shadow=False, startangle=90)
plt.axis('equal')
 
# show plot
st.pyplot(fig)


# 4. DISTRIBUTION - LINE CHART


chart_data2
st.line_chart(
    chart_data2, 
    x='Durasi(Menit)',
    y=['Budget','Gross_US'],
    color=['#FF0000', '#0000FF'],  # Optional
    # color = ['Rating']
)



# labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
# sizes = [15, 30, 45, 10]
# explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

# fig1, ax1 = plt.subplots()
# ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
#         shadow=True, startangle=90)
# ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


# plt.show()


# st.bar_chart(df_sel)
# df_sorted
# sorting
