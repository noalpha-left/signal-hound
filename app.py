# alt_data_sentiment_dashboard/app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fetch_data import fetch_headlines
from sentiment import analyze_sentiment

st.set_page_config(page_title="Sentiment Tracker", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #eaeaea;
    }
    .stApp {
        background-color: #121212;
    }
    .block-container {
        padding: 2rem 1rem;
    }
    .css-1d391kg, .css-1v0mbdj, .css-ffhzg2, .stTextInput, .stButton>button {
        background-color: #1e1e1e !important;
        color: #eaeaea !important;
        border: none !important;
        border-radius: 10px !important;
    }
    .stButton>button:hover {
        background-color: #2a2a2a !important;
        border: 1px solid #444 !important;
    }
    .css-1v0mbdj .stTextInput>div>div>input {
        color: #eaeaea;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Sentiment Tracker")

# --- Sidebar ---
st.sidebar.title("Configuration")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL)", "AAPL")

if st.sidebar.button("Analyze"):
    with st.spinner("Processing headlines..."):
        headlines = fetch_headlines(ticker)
        if not headlines:
            st.error("No headlines found. Try another ticker.")
        else:
            sentiments = analyze_sentiment(headlines)
            df = pd.DataFrame({"Headline": headlines, "Sentiment Score": sentiments})

            st.subheader(f"Sentiment Overview for {ticker}")
            st.write(df)

            # Metrics
            avg_sent = round(df["Sentiment Score"].mean(), 3)
            pos_count = (df["Sentiment Score"] > 0).sum()
            neg_count = (df["Sentiment Score"] < 0).sum()

            col1, col2, col3 = st.columns(3)
            col1.metric("Average Sentiment", avg_sent)
            col2.metric("Positive Headlines", pos_count)
            col3.metric("Negative Headlines", neg_count)

            # Plot
            st.subheader("Sentiment Score Distribution")
            fig, ax = plt.subplots(facecolor='#121212')
            df["Sentiment Score"].hist(bins=20, ax=ax, color='#007ACC', edgecolor='#eaeaea')
            ax.set_title("Sentiment Distribution", color='white')
            ax.set_xlabel("Sentiment Score", color='white')
            ax.set_ylabel("Frequency", color='white')
            ax.tick_params(colors='white')
            st.pyplot(fig)
else:
    st.info("Enter a ticker and click 'Analyze' to begin.")

# --- fetch_data.py ---
import requests
from bs4 import BeautifulSoup

def fetch_headlines(ticker):
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    news_table = soup.find(id='news-table')
    headlines = []

    if news_table:
        for row in news_table.findAll('tr'):
            if row.a:
                title = row.a.get_text()
                headlines.append(title)

    return headlines

# --- sentiment.py ---
from textblob import TextBlob

def analyze_sentiment(texts):
    sentiment_scores = [TextBlob(text).sentiment.polarity for text in texts]
    return sentiment_scores

streamlit run app.py
