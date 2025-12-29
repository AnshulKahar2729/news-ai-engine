import feedparser

RSS_FEEDS = [
    "https://feeds.reuters.com/reuters/INbusinessNews",
    "https://www.moneycontrol.com/rss/latestnews.xml",
    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms"
]

def fetch_all_news():
    news = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for e in feed.entries:
            news.append({
                "title": e.get("title", ""),
                "summary": e.get("summary", ""),
                "link": e.get("link", "")
            })
    return news
