
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fetch_data import fetch_headlines
from sentiment import analyze_sentiment

st.set_page_config(page_title="Alt Data Sentiment Dashboard", layout="wide", initial_sidebar_state="collapsed")
st.title("🧠 Alt Data Sentiment Dashboard")

# --- Sidebar ---
st.sidebar.title("Settings")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL)", "AAPL")

if st.sidebar.button("Analyze"):
    with st.spinner("Fetching and analyzing headlines..."):
        headlines = fetch_headlines(ticker)
        if not headlines:
            st.error("No headlines found. Try another ticker.")
        else:
            sentiments = analyze_sentiment(headlines)
            df = pd.DataFrame({"Headline": headlines, "Sentiment Score": sentiments})

            st.subheader(f"Sentiment Analysis for {ticker}")
            st.write(df)

            # Metrics
            avg_sent = round(df["Sentiment Score"].mean(), 3)
            pos_count = (df["Sentiment Score"] > 0).sum()
            neg_count = (df["Sentiment Score"] < 0).sum()

            col1, col2, col3 = st.columns(3)
            col1.metric("📈 Average Sentiment", avg_sent)
            col2.metric("👍 Positive Headlines", pos_count)
            col3.metric("👎 Negative Headlines", neg_count)

            # Plot
            st.subheader("📊 Sentiment Score Distribution")
            fig, ax = plt.subplots()
            df["Sentiment Score"].hist(bins=20, ax=ax, color='skyblue', edgecolor='black')
            ax.set_title("Sentiment Distribution")
            ax.set_xlabel("Sentiment Score")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)
else:
    st.info("Enter a ticker and press 'Analyze' to begin.")
