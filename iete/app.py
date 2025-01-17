import streamlit as st
import requests


# Function to fetch news from NewsAPI
def fetch_news(query, api_key):
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={api_key}&pageSize=5'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['articles']
    else:
        st.error("Failed to fetch news")
        return []


# Streamlit UI
def main():
    st.title('Finance, Stocks, Crypto, ESG, and IPO News')

    # Input for API Key (you can replace it with your own)
    api_key = st.text_input('Enter your NewsAPI key:', type="password")

    # Select category for news
    category = st.radio(
        'Choose a news category:',
        ('Finance', 'Stocks', 'Crypto', 'ESG', 'IPO')
    )

    # Fetch news based on selected category
    if api_key:
        if st.button('Fetch News'):
            query = category.lower()
            articles = fetch_news(query, api_key)

            if articles:
                for idx, article in enumerate(articles):
                    st.subheader(f"Article {idx + 1}: {article['title']}")
                    st.write(f"**Source**: {article['source']['name']}")
                    st.write(f"**Published**: {article['publishedAt']}")
                    st.write(f"[Read more]({article['url']})")
                    st.write(f"Summary: {article['description']}\n")
            else:
                st.write("No articles found.")
        else:
            st.warning('Please enter a valid API key and click "Fetch News"')


if __name__ == "__main__":
    main()
