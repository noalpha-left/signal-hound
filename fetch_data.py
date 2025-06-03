
import requests
from bs4 import BeautifulSoup

def fetch_headlines(ticker):
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    try:
        news_table = soup.find(id='news-table')
        rows = news_table.findAll('tr')
        headlines = [row.a.get_text() for row in rows if row.a]
        return headlines[:15]
    except Exception:
        return []
