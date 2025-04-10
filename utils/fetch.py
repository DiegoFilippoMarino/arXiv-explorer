import feedparser
import urllib.parse
import time
import socket
from config import TIMEOUT_PER_REQUEST

def fetch_recent_arxiv(category, max_results=1000, retries=3, sleep_base=4):
    """
    Fetches the most recent arXiv papers for a given category using the arXiv API.
    """
    query = f"search_query=cat:{category}&sortBy=submittedDate&sortOrder=descending&start=0&max_results={max_results}"
    url = "http://export.arxiv.org/api/query?" + urllib.parse.quote(query, safe=":/?&=")

    for attempt in range(1, retries + 1):
        try:
            print(f"🔍 Fetching {category} (Attempt {attempt})")
            socket.setdefaulttimeout(TIMEOUT_PER_REQUEST)
            feed = feedparser.parse(url)
            return feed.entries
        except Exception as e:
            wait = sleep_base * attempt
            print(f"⚠️ Failed attempt {attempt} for {category}: {e} — retrying in {wait}s")
            time.sleep(wait)
    print(f"❌ Skipping {category} after {retries} failed attempts")
    return []