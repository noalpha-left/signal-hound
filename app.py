# alt_data_sentiment_dashboard/app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import yfinance as yf
from fetch_data import fetch_headlines
from sentiment import analyze_sentiment
from db_utils import init_db, insert_record, load_sentiment_history
import datetime
import snscrape.modules.twitter as sntwitter

st.set_page_config(page_title="Sentiment Tracker", layout="wide", initial_sidebar_state="collapsed")

st.title("📊 Sentiment Tracker")

# Initialize DB
init_db()

# --- Sidebar ---
st.sidebar.title("Configuration")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL)", "AAPL")
days_back = st.sidebar.slider("Days of headlines to analyze", 1, 30, 7)
sentiment_filter = st.sidebar.slider("Minimum Sentiment Score", -100.0, 100.0, -100.0)

if st.sidebar.button("Analyze"):
    with st.spinner("Processing data sources..."):
        headlines = fetch_headlines(ticker)

        twitter_headlines = []
        try:
            for tweet in sntwitter.TwitterSearchScraper(f"{ticker} since:2022-01-01").get_items():
                twitter_headlines.append({"text": tweet.content, "date": tweet.date.date()})
                if len(twitter_headlines) >= 100:
                    break
        except:
            twitter_headlines.append({"text": "Twitter fetch failed", "date": datetime.datetime.now().date()})

        all_text = headlines + twitter_headlines

        if not all_text:
            st.error("No content found. Try another ticker.")
        else:
            today = datetime.datetime.now()
            processed = []
            texts_for_analysis = [t["text"] if isinstance(t, dict) else t for t in all_text]
            sentiments = analyze_sentiment(texts_for_analysis)

            for i, item in enumerate(all_text):
                if isinstance(item, dict):
                    content = item["text"]
                    date = item["date"]
                    source = "Twitter"
                else:
                    content = item
                    date = today.date() - datetime.timedelta(days=i + 1)
                    source = "Finviz"

                score = sentiments[i] * 100  # Convert to percentage
                weight = 1 / (i + 1)
                weighted_score = score * weight

                insert_record(date, ticker, source, content, score, weighted_score)

                processed.append({
                    "Text": content,
                    "Sentiment Score": score,
                    "Weighted Score": weighted_score,
                    "Date": date
                })

            df = pd.DataFrame(processed)
            df = df[df["Sentiment Score"] >= sentiment_filter]

            st.subheader(f"Sentiment Overview for {ticker}")
            st.write(df)

            avg_sent = round(df["Sentiment Score"].mean(), 2)
            avg_weighted = round(df["Weighted Score"].mean(), 2)
            pos_count = (df["Sentiment Score"] > 0).sum()
            neg_count = (df["Sentiment Score"] < 0).sum()

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Avg Sentiment (%)", avg_sent)
            col2.metric("Weighted Avg (%)", avg_weighted)
            col3.metric("Positive Count", pos_count)
            col4.metric("Negative Count", neg_count)

            st.subheader("Sentiment Score Distribution")
            fig, ax = plt.subplots()
            df["Sentiment Score"].hist(bins=20, ax=ax, color='#007ACC', edgecolor='black')
            ax.set_title("Sentiment Distribution")
            ax.set_xlabel("Sentiment Score (%)")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

            st.subheader("Historical Sentiment Over Time")
            sentiment_time_df = df.groupby("Date")["Sentiment Score"].mean().sort_index().reset_index()
            fig, ax = plt.subplots()
            ax.plot(sentiment_time_df["Date"], sentiment_time_df["Sentiment Score"], marker='o', linestyle='-')
            ax.set_title("Average Sentiment Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("Avg Sentiment (%)")
            plt.xticks(rotation=45)
            st.pyplot(fig)

            st.subheader("Most Common Words")
            word_text = " ".join(df["Text"])
            wc = WordCloud(width=800, height=300, background_color='white').generate(word_text)
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.imshow(wc, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)

            st.subheader("Stock Price Performance")
            price_data = yf.download(ticker, period="2y")
            st.line_chart(price_data['Close'])

            st.subheader("Live Trading Signal (Beta)")
            if avg_weighted > 30:
                st.success("Bullish sentiment detected. Consider long position (simulated).")
            elif avg_weighted < -30:
                st.error("Bearish sentiment detected. Consider short position (simulated).")
            else:
                st.warning("Neutral zone. Wait for stronger signal.")
else:
    st.info("Enter a ticker and click 'Analyze' to begin.")

