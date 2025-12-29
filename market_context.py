import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

def get_price_change(symbol):
    try:
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=HEADERS)

        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        data = session.get(url, headers=HEADERS).json()

        price = data["priceInfo"]
        last = price["lastPrice"]
        prev = price["previousClose"]

        return round(((last - prev) / prev) * 100, 2)
    except:
        return None


def reaction_bucket(pct):
    if pct is None:
        return "unknown"
    if abs(pct) < 3:
        return "not_priced"
    elif abs(pct) < 7:
        return "partially_priced"
    else:
        return "mostly_priced"
