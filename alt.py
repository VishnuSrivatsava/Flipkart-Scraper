import streamlit as st
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to perform web scraping
def scrape_data(url):
    driver = webdriver.Chrome()
    driver.get(url)

    # Web scraping code here to extract data
    # In this example, we'll scrape product names and prices
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    
    products = []

    names = soup.find_all('div', class_='_4rR01T')
    prices = soup.find_all('div', class_='_30jeq3')

    for name, price in zip(names, prices):
        products.append({
            'Product Name': name.text,
            'Price': price.text,
        })

    driver.quit()
    return products

# Create a Streamlit app
st.title("Product Information")

# Input text box for the Flipkart link
url = st.text_input("Enter Flipkart Product Page Link:")
if st.button("Scrape Data") and url:
    st.info("Scraping data... Please wait.")
    scraped_data = scrape_data(url)
    st.success("Data scraped successfully!")

    # Display the scraped data in a Streamlit table
    if scraped_data:
        df = pd.DataFrame(scraped_data)
        st.subheader("Scraped Data")

        # Preprocess the "Price" column to remove non-numeric characters
        df['Price'] = df['Price'].str.replace('[₹,]', '', regex=True).astype(float)

        st.dataframe(df)

        # Visualize data side by side
        st.subheader("Visualizations")

        # Bar Chart: Price vs. Product
        st.subheader("Bar Chart: Price vs. Product")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="Price", y="Product Name", data=df, ax=ax)
        ax.set_xlabel("Price (in INR)")
        ax.set_ylabel("Product Name")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Histogram: Price Distribution
        st.subheader("Histogram: Price Distribution")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data=df, x="Price", bins=20, ax=ax, kde=True)  # Added kde=True for smoother histogram
        ax.set_xlabel("Price (in INR)")
        ax.set_ylabel("Count")
        st.pyplot(fig)

# Run the Streamlit app
if __name__ == '__main__':
    st.write("")

