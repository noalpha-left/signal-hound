
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
            title = row.a.get_text()
            headlines.append(title)

    return headlines
