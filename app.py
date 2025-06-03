
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fetch_data import fetch_headlines
from sentiment import analyze_sentiment

st.set_page_config(page_title="🦇 Gotham Sentiment Watcher", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    body {
        background-color: #0f0f0f;
        color: #f5f5f5;
    }
    .stApp {
        background-color: #0f0f0f;
    }
    .css-1d391kg, .css-1v0mbdj, .css-ffhzg2 {
        background-color: #1a1a1a !important;
        color: #f5f5f5 !important;
    }
    .css-1v0mbdj:hover {
        background-color: #292929 !important;
    }
    .stButton>button {
        background-color: #222;
        color: #f5f5f5;
        border-radius: 0px;
        border: 1px solid #555;
    }
    .stButton>button:hover {
        background-color: #444;
        border: 1px solid #888;
    }
    .css-1v0mbdj .stTextInput>div>div>input {
        color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🦇 Gotham Sentiment Watcher")

# --- Sidebar ---
st.sidebar.title("Surveillance Feed")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL)", "AAPL")

if st.sidebar.button("Scan Ticker"):
    with st.spinner("Running intelligence sweep..."):
        headlines = fetch_headlines(ticker)
        if not headlines:
            st.error("No signal detected. Try another ticker.")
        else:
            sentiments = analyze_sentiment(headlines)
            df = pd.DataFrame({"Headline": headlines, "Sentiment Score": sentiments})

            st.subheader(f"Sentiment Intel for {ticker}")
            st.write(df)

            # Metrics
            avg_sent = round(df["Sentiment Score"].mean(), 3)
            pos_count = (df["Sentiment Score"] > 0).sum()
            neg_count = (df["Sentiment Score"] < 0).sum()

            col1, col2, col3 = st.columns(3)
            col1.metric("💀 Average Sentiment", avg_sent)
            col2.metric("🔺 Uplifting Intel", pos_count)
            col3.metric("🔻 Grim Headlines", neg_count)

            # Plot
            st.subheader("📊 Distribution of Sentiment")
            fig, ax = plt.subplots(facecolor='#0f0f0f')
            df["Sentiment Score"].hist(bins=20, ax=ax, color='#39ff14', edgecolor='#f5f5f5')
            ax.set_title("Sentiment Distribution", color='white')
            ax.set_xlabel("Sentiment Score", color='white')
            ax.set_ylabel("Frequency", color='white')
            ax.tick_params(colors='white')
            st.pyplot(fig)
else:
    st.info("Input a ticker and activate scan.")
