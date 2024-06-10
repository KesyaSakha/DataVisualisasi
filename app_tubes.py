import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
import toml
# Read database connection info from secrets.toml
secrets = toml.load('secrets.toml')
db_config = secrets['connections']['mysql']

# Function to execute MySQL query
def execute_query_mysql(query):
    # Membuat koneksi ke database
    db_connection = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['username'],
        password=db_config['password'],
        database=db_config['database']
    )

    # Creating a cursor object
    cursor = db_connection.cursor()

    # Executing the query
    cursor.execute(query)

    # Fetching the results
    result = cursor.fetchall()

    # Closing the cursor
    cursor.close()

    # Closing the connection
    db_connection.close()

    return result

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
