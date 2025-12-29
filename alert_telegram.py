import requests

def send_telegram(text, cfg):
    url = f"https://api.telegram.org/bot{cfg.TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": cfg.TELEGRAM_CHAT_ID,
        "text": text
    })
