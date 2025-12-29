from fetch_news import fetch_all_news
from ai_analyzer import analyze_news
from scorer import final_score
from market_context import get_price_change, reaction_bucket
from alert_email import send_email
from alert_telegram import send_telegram
import config as cfg
import json, hashlib

# ---------- STATE ----------
def load_state():
    with open("state.json") as f:
        return json.load(f)

def save_state(state):
    with open("state.json", "w") as f:
        json.dump(state, f, indent=2)

def hash_news(text):
    return hashlib.md5(text.encode()).hexdigest()

def continuation_override(ai, reaction):
    if ai["continuation_probability"] >= 7:
        return True
    if ai["severity"] >= 8 and reaction != "mostly_priced":
        return True
    return False

# ---------- RUN ----------
state = load_state()
news_items = fetch_all_news()

for n in news_items:
    text = n["title"] + " " + n["summary"]
    h = hash_news(text)

    if h in state["alerted_news"]:
        continue

    ai = analyze_news(text, cfg.OLLAMA_MODEL)
    if not ai:
        continue

    symbol = ai.get("probable_symbol", "").upper()
    if not symbol or len(symbol) > 12:
        continue

    confidence = (
        ai["severity"] +
        ai["permanence"] +
        ai["continuation_probability"]
    ) / 3

    if confidence < 6:
        continue

    pct = get_price_change(symbol)
    reaction = reaction_bucket(pct)
    score = final_score(ai)

    should_alert = (
        score >= cfg.ALERT_THRESHOLDS["strong"]
        or (score >= cfg.ALERT_THRESHOLDS["watch"]
            and continuation_override(ai, reaction))
    )

    if should_alert and symbol not in state["alerted_stocks"]:
        subject = f"🚨 AI NEWS ALERT | {symbol} | {ai['bullish_or_bearish'].upper()}"
        body = f"""
Stock: {symbol}
Price Reaction: {pct}%
Reaction Status: {reaction}

AI Impact Score: {score}

Event Type: {ai['event_type']}

AI Reasoning:
{ai['reason']}
"""
        send_email(subject, body, cfg)
        send_telegram(body, cfg)

        state["alerted_news"].append(h)
        state["alerted_stocks"][symbol] = True

save_state(state)
