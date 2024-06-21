import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pymysql
from pymysql import Error
import toml

# Load database connection info from secrets.toml
secrets = toml.load('secrets.toml')
db_config = secrets['connections']['mydb']

# Define pastel colors
pastel_colors = ["#ffb3ba", "#c6b4f8", "#bae1ff", "#baffc9"]  # Adding pastel green

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
    st.write("### Data Table")
    st.dataframe(data)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(data[x], data[y], color=pastel_colors)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.tight_layout()
    st.pyplot(fig)
    st.write(f"Grafik ini menampilkan sepuluh produk teratas berdasarkan total penjualannya. Setiap batang horizontal mewakili satu produk, dan panjang batang menunjukkan jumlah penjualan produk tersebut. Dari grafik ini, kita bisa melihat dengan jelas produk mana yang memiliki penjualan tertinggi dan terendah di antara sepuluh produk teratas. Warna pastel yang digunakan membuat grafik lebih menarik dan mudah dibaca. Penjualan tertinggi adalah pada produk X, yang menunjukkan popularitas atau efektivitas strategi penjualannya.")

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
    st.write(f"Diagram pai ini menggambarkan distribusi penjualan dari sepuluh produk teratas. Setiap irisan pai menunjukkan proporsi penjualan yang dihasilkan oleh masing-masing produk. Diagram ini membantu dalam memahami kontribusi relatif dari setiap produk terhadap total penjualan. Misalnya, produk dengan irisan terbesar adalah produk X, menunjukkan bahwa produk ini memberikan kontribusi terbesar terhadap penjualan total.")

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
    st.write(f"Scatter plot ini menampilkan hubungan antara biaya standar (Standard Cost) dan harga jual (List Price) dari produk. Setiap titik pada grafik mewakili satu produk. Garis regresi yang ditambahkan menunjukkan tren umum dalam data, yaitu apakah ada hubungan linear antara biaya standar dan harga jual. Dari grafik ini, kita bisa melihat apakah produk dengan biaya standar yang lebih tinggi cenderung memiliki harga jual yang lebih tinggi atau tidak.")

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
    st.write(f"Bubble plot ini mirip dengan scatter plot tetapi dengan tambahan dimensi ukuran untuk mewakili variabel ketiga, seperti kuantitas atau ukuran lainnya. Dalam konteks ini, setiap gelembung mewakili produk, dengan posisinya ditentukan oleh biaya standar dan harga jual, dan ukuran gelembung mungkin mencerminkan jumlah produk atau variabel lain yang relevan. Plot ini memberikan gambaran lebih mendalam tentang distribusi dan variasi produk berdasarkan tiga variabel.")

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
    st.write(f"Histogram ini menampilkan distribusi harga jual produk (List Price). Sumbu horizontal menunjukkan rentang harga, sementara sumbu vertikal menunjukkan frekuensi (jumlah produk) dalam setiap rentang harga. Dari histogram ini, kita bisa melihat bagaimana harga produk tersebar, apakah sebagian besar produk berada dalam rentang harga tertentu, atau ada outlier dengan harga sangat tinggi atau rendah.")

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
    st.write(f"KDE plot ini adalah representasi visual dari distribusi harga jual produk menggunakan estimasi kepadatan kernel. Grafik ini memberikan gambaran yang lebih halus tentang distribusi harga, berbeda dengan histogram yang menggunakan bin. Dari plot ini, kita bisa melihat puncak dan sebaran harga produk, menunjukkan kecenderungan umum dalam harga produk. Misalnya, jika ada puncak tajam, itu menunjukkan bahwa banyak produk memiliki harga di sekitar nilai tersebut.")

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
    st.title('Visualizations from XAMPP Database and IMDb Data')

    # Sidebar for selecting dataset
    dataset = st.sidebar.selectbox('Select Dataset', ['Database', 'IMDb'])

    if dataset == 'Database':
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
        bubble_plot(product_df, 'StandardCost', 'ListPrice', 'Bubble Plot of Product Variables', 'Standard Cost', 'List Price')

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
        kde_plot(data_df, 'ListPrice', True, pastel_colors[1], 'Kernel Density Estimate of Product List Prices', 'List Price', 'Density')

    elif dataset == 'IMDb':
        df = load_imdb_data()

        st.write("1. COMPARISON CHART - BAR CHART")
        df_sel = df[['Title', 'IMDb Rating']].sort_values(by=['IMDb Rating'], ascending=False).head(40)
        st.write("### Data Table")
        st.dataframe(df_sel)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=df_sel, x='Title', y='IMDb Rating', palette=pastel_colors, ax=ax)
        plt.xticks(rotation=90)
        plt.title("Top 40 Comparison Chart - Bar Chart")
        st.pyplot(fig)
        st.write(f"Grafik ini menampilkan 40 film teratas berdasarkan peringkat IMDb mereka. Setiap batang vertikal mewakili satu film, dan tinggi batang menunjukkan peringkat IMDb film tersebut. Dari grafik ini, kita bisa melihat dengan jelas film mana yang memiliki peringkat tertinggi dan terendah di antara 40 film teratas. Warna pastel yang digunakan membuat grafik lebih menarik dan mudah dibaca.")

       # 2. RELATIONSHIP CHART - BUBBLE PLOT
        st.write("2. RELATIONSHIP CHART - BUBBLE PLOT")
        df_sel2 = df[['Runtime (mins)', 'IMDb Rating']].sort_values(by=['IMDb Rating'], ascending=False).head(50)
        st.write("### Data Table")
        st.dataframe(df_sel2)
        fig, ax = plt.subplots(figsize=(10, 6))
        bubble_sizes = df_sel2['Runtime (mins)'] * 5  # Adjust size for better visualization
        sns.scatterplot(data=df_sel2, x='Runtime (mins)', y='IMDb Rating', size='Runtime (mins)', sizes=(20, 200), hue='IMDb Rating', palette=pastel_colors, alpha=0.6, ax=ax, legend=False)
        plt.title("Top 50 Relationship Chart - Bubble Plot")
        st.pyplot(fig)
        st.write(f"Bubble plot ini menampilkan hubungan antara durasi film (Runtime) dan peringkat IMDb mereka. Setiap gelembung mewakili satu film, dengan posisi ditentukan oleh durasi dan peringkat IMDb, dan ukuran gelembung mencerminkan durasi film. Plot ini memberikan gambaran lebih mendalam tentang distribusi dan variasi film berdasarkan tiga variabel.")

        st.write("3. COMPOSITION CHART - DONUT CHART (Top 10 Genres)")
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
        st.write(f"Diagram donat ini menggambarkan distribusi sepuluh genre teratas. Setiap irisan menunjukkan proporsi jumlah film dalam setiap genre. Diagram ini membantu dalam memahami kontribusi relatif dari setiap genre terhadap total jumlah film. Misalnya, genre dengan irisan terbesar menunjukkan bahwa itu adalah genre yang paling banyak diwakili dalam data.")

        st.write("4. DISTRIBUTION - LINE CHART (Movies Released Each Year)")
        df_sel4 = df['Year'].value_counts().sort_index().reset_index()
        df_sel4.columns = ['Year', 'Number of Movies']
        st.write("### Data Table")
        st.dataframe(df_sel4)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=df_sel4, x='Year', y='Number of Movies', marker='o', color=pastel_colors[2], ax=ax)
        plt.title("Distribution - Line Chart (Movies Released Each Year)")
        st.pyplot(fig)
        st.write(f"Line chart ini menunjukkan jumlah film yang dirilis setiap tahun. Sumbu horizontal menunjukkan tahun, sementara sumbu vertikal menunjukkan jumlah film yang dirilis pada tahun tersebut. Dari grafik ini, kita bisa melihat tren perilisan film dari waktu ke waktu, seperti peningkatan atau penurunan jumlah film yang dirilis setiap tahun.")

if __name__ == "__main__":
    main()
