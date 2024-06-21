import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pymysql
from pymysql import Error


# Define pastel colors
pastel_colors = ["#ffb3ba", "#c6b4f8", "#bae1ff", "#baffc9"]  # Adding pastel green

def execute_query_mysql(query):
    conn = None
    try:
        conn = pymysql.connect(
            host=st.secrets["connections.mydb"]["host"],
            port=int(st.secrets["connections.mydb"]["port"]),
            user=st.secrets["connections.mydb"]["username"],
            password=st.secrets["connections.mydb"]["password"],
            database=st.secrets["connections.mydb"]["database"]
        )
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Error as e:
        st.error(f"Error: {e}")
        return None
    finally:
        if conn is not None:
            conn.close()
            
# Function to display bar chart
def bar_chart(data, x, y, title, xlabel, ylabel):
    st.write("### Data Table")
    st.dataframe(data)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(data[x], data[y], color=pastel_colors)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.tight_layout()
    st.pyplot(fig)

# Function to display pie chart
def pie_chart(data, labels, values, title):
    st.write("### Data Table")
    st.dataframe(data)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(data[values], labels=data[labels], autopct='%1.1f%%', startangle=140, colors=pastel_colors)
    ax.axis('equal')
    ax.set_title(title)
    plt.tight_layout()
    st.pyplot(fig)

# Function to display scatter plot
def scatter_plot(data, x, y, title, xlabel, ylabel):
    st.write("### Data Table")
    st.dataframe(data)
    data[x] = data[x].astype(float)
    data[y] = data[y].astype(float)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(x=x, y=y, data=data, scatter_kws={'color': pastel_colors[2]}, line_kws={'color': pastel_colors[1]}, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

# Function to display bubble plot
def bubble_plot(data, x, y, title, xlabel, ylabel):
    st.write("### Data Table")
    st.dataframe(data)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(data[x], data[y], alpha=0.5, color=pastel_colors[0])
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    st.pyplot(fig)

# Function to display histogram
def histogram(data, column, bins, title, xlabel, ylabel):
    st.write("### Data Table")
    st.dataframe(data)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(data[column], bins=bins, color=pastel_colors[0], edgecolor='black')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

# Function to display KDE plot
def kde_plot(data, column, fill, color, title, xlabel, ylabel):
    st.write("### Data Table")
    st.dataframe(data)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.kdeplot(data[column], fill=fill, color=color, ax=ax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

# Function to load IMDb CSV data
def load_imdb_data():
    df = pd.read_csv('scraping - top picks.csv')
    df['IMDb Rating'] = df['IMDb Rating'].astype("float")
    df['Title'] = df['Title'].astype("string")
    df['Year'] = pd.to_numeric(df['Year'])
    df['Runtime (mins)'] = pd.to_numeric(df['Runtime (mins)'])
    return df

# Main function
def main():
    st.set_page_config(page_title='Final Project Data Visualization', layout='wide')

    # Custom CSS
    st.markdown(
        """
        <style>
        .main {
            background-color: #ffd1dc;
            color: #000000;
        }
        .css-18e3th9 {
            padding-top: 2rem;
            padding-right: 2rem;
            padding-left: 2rem;
        }
        .css-1d391kg {
            background-color: #ffd1dc;
        }
        .css-1avcm0n {
            color: #000000;
        }
        .st-bh {
            color: #000000;
        }
        .css-15tx938 {
            color: #000000;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    st.title('Final Project Data Visualization')

    # Sidebar for selecting dataset
    dataset = st.sidebar.selectbox('Select Dataset', ['Adventure Works', 'IMDb - Top Picks'])

    if dataset == 'Adventure Works':
        st.subheader('Adventure Works Visualization')
        
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
        
        st.subheader('1. Comparison Chart - Top 10 Products by Total Sales (Bar Chart)')
        bar_chart(sales_df, 'EnglishProductName', 'TotalSales', 'Top 10 Products by Total Sales (Bar Chart)', 'Total Sales', 'Product Name')
        
        with st.expander("About Visualization"):
            st.write("""
            This bar chart displays the top 10 products by total sales. 
            Each horizontal bar represents a product, and the length of the bar indicates the total sales of that product.
            """)

        st.subheader('Top 10 Products by Total Sales (Pie Chart)')
        pie_chart(sales_df, 'EnglishProductName', 'TotalSales', 'Top 10 Products by Total Sales (Pie Chart)')
        
        with st.expander("About Visualization"):
            st.write("""
            This pie chart shows the distribution of total sales for the top 10 products. 
            Each slice represents the proportion of total sales for each product. 
            It helps in understanding the relative contribution of each product to the total sales.
            """)

        # Query to retrieve StandardCost and ListPrice data
        product_query = """
            SELECT StandardCost, ListPrice
            FROM dimproduct
        """
        product_df = pd.DataFrame(execute_query_mysql(product_query), columns=['StandardCost', 'ListPrice'])

        st.subheader('2. Relationship between Standard Cost and List Price')
        scatter_plot(product_df, 'StandardCost', 'ListPrice', 'Relationship between Standard Cost and List Price', 'Standard Cost', 'List Price')
        
        with st.expander("About Visualization"):
            st.write("""
            This scatter plot shows the relationship between standard cost and list price of products. 
            Each point represents a product, with its position determined by standard cost and list price. 
            This plot provides insights into how standard cost and list price are related to each other.
            """)

        st.subheader('Bubble Plot of Product Variables')
        bubble_plot(product_df, 'StandardCost', 'ListPrice', 'Bubble Plot of Product Variables', 'Standard Cost', 'List Price')
        
        with st.expander("About Visualization"):
            st.write("""
            This bubble plot displays product variables with bubble size representing list price and position based on standard cost and list price. 
            It provides a deeper insight into the distribution and variation of products based on these three variables.
            """)

        # Query to retrieve product composition data by ProductLine
        product_line_query = """
            SELECT ProductLine, COUNT(*) AS TotalProducts
            FROM dimproduct
            GROUP BY ProductLine
        """
        product_line_df = pd.DataFrame(execute_query_mysql(product_line_query), columns=['ProductLine', 'TotalProducts'])

        st.subheader('3. Composition of Products by Product Line')
        bar_chart(product_line_df, 'ProductLine', 'TotalProducts', 'Composition of Products by Product Line', 'Product Line', 'Total Products')
        
        with st.expander("About Visualization"):
            st.write("""
            This chart shows the composition of products by product line. 
            Each bar represents a product line, and the height of the bar indicates the total number of products in that line.
            It helps in understanding the distribution of products across different product lines.
            """)

        # Query to retrieve data to be visualized
        data_query = """
            SELECT ListPrice
            FROM dimproduct
            WHERE ListPrice IS NOT NULL
        """
        data_df = pd.DataFrame(execute_query_mysql(data_query), columns=['ListPrice'])

        st.subheader('4. Distribution of Product List Prices (Histogram)')
        histogram(data_df, 'ListPrice', 20, 'Distribution of Product List Prices', 'List Price', 'Frequency')
        
        with st.expander("About Visualization"):
            st.write("""
            This histogram displays the distribution of product list prices. 
            The horizontal axis shows the price range, while the vertical axis shows the frequency of products in that range.
            It provides an overview of how product prices are distributed.
            """)

        st.subheader('Kernel Density Estimate of Product List Prices (KDE Plot)')
        kde_plot(data_df, 'ListPrice', True, pastel_colors[1], 'Kernel Density Estimate of Product List Prices', 'List Price', 'Density')
        
        with st.expander("About Visualization"):
            st.write("""
            This KDE plot shows the kernel density estimate of product list prices. 
            The smooth line represents the probability distribution of list prices, offering a smoother view of the price distribution compared to a histogram.
            """)

    elif dataset == 'IMDb - Top Picks':
        st.subheader('Scrapping and Visualization from IMDb Top Picks')
        st.markdown("[Link to IMDb Dataset](https://www.imdb.com/list/ls539678894/?view=detailed)")

        df = load_imdb_data()

        st.subheader('1. COMPARISON CHART - BAR CHART')
        df_sel = df[['Title', 'IMDb Rating']].sort_values(by=['IMDb Rating'], ascending=False).head(40)
        st.write("### Data Table")
        st.dataframe(df_sel)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=df_sel, x='Title', y='IMDb Rating', palette=pastel_colors, ax=ax)
        plt.xticks(rotation=90)
        plt.title("Top 40 Comparison Chart - Bar Chart")
        st.pyplot(fig)
        
        with st.expander("About Visualization"):
            st.write("""
            This bar chart displays the top 40 movies based on IMDb rating. 
            Each bar represents a movie, and the height of the bar indicates the IMDb rating. 
            This chart facilitates comparison of movie ratings.
            """)

        st.subheader('2. RELATIONSHIP CHART - BUBBLE PLOT')
        df_sel2 = df[['Runtime (mins)', 'IMDb Rating']].sort_values(by=['IMDb Rating'], ascending=False).head(50)
        st.write("### Data Table")
        st.dataframe(df_sel2)
        fig, ax = plt.subplots(figsize=(10, 6))
        bubble_sizes = df_sel2['Runtime (mins)'] * 5  # Adjust size for better visualization
        sns.scatterplot(data=df_sel2, x='Runtime (mins)', y='IMDb Rating', size='Runtime (mins)', sizes=(20, 200), hue='IMDb Rating', palette=pastel_colors, alpha=0.6, ax=ax, legend=False)
        plt.title("Top 40 Relationship Chart - Bubble Plot")
        st.pyplot(fig)
        
        with st.expander("About Visualization"):
            st.write("""
            This bubble plot shows the top 40 movies based on IMDb rating. Each bubble represents a movie, where its position indicates IMDb rating and size corresponds to movie duration (in minutes). 
            This visualization allows for exploring any relationship between movie duration and rating, focusing specifically on the top-ranked films.
            """)

        st.subheader('3. COMPOSITION CHART - DONUT CHART (Top 10 Genres)')
        genres = df['Genres'].str.split(',').explode().str.strip()
        genre_counts = genres.value_counts().reset_index()
        genre_counts.columns = ['Genre', 'Count']
        top_10_genres = genre_counts.head(10)
        st.write("### Data Table")
        st.dataframe(top_10_genres)
        fig, ax = plt.subplots(figsize=(10, 7))
        wedges, texts, autotexts = ax.pie(top_10_genres['Count'], labels=top_10_genres['Genre'], autopct='%1.1f%%', startangle=90, pctdistance=0.85, colors=pastel_colors, wedgeprops=dict(width=0.3))
        plt.setp(autotexts, size=10, weight="bold", color="white")
        plt.setp(texts, size=12)
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig.gca().add_artist(centre_circle)
        ax.set_aspect('equal')
        plt.title("Top 10 Genre Distribution - Donut Chart")
        st.pyplot(fig)
        
        with st.expander("About Visualization"):
            st.write("""
            This donut chart displays the distribution of the top 10 genres of movies in the dataset.
            Each slice represents the proportion of movies included in each genre, 
            providing an overview of the most common genres in the dataset.
            """)

        st.subheader('4. DISTRIBUTION - LINE CHART (Movies Released Each Year)')
        df_sel4 = df['Year'].value_counts().sort_index().reset_index()
        df_sel4.columns = ['Year', 'Number of Movies']
        st.write("### Data Table")
        st.dataframe(df_sel4)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=df_sel4, x='Year', y='Number of Movies', marker='o', color=pastel_colors[2], ax=ax)
        plt.title("Distribution - Line Chart (Movies Released Each Year)")
        st.pyplot(fig)
        
        with st.expander("About Visualization"):
            st.write("""
            This line chart shows the number of movies released each year. 
            The horizontal axis represents the year, while the vertical axis represents the number of movies released. 
            This chart provides insights into the trend of movie releases over time.
            """)

    # Tambahkan informasi data diri di akhir halaman
    st.markdown("""
        <p style='text-align: left; color: black; font-size: 14px;'>Nama : Kesya Sakha Nesya Arimawan <br>
        NPM : 21082010169<br>
        Mata Kuliah : Data Visualisasi<br>
        Paralel : B</p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
