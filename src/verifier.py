#verifier.py
import requests
from urllib.parse import quote
from src.config import NEWS_API_KEY


def extract_keywords(text):
    text_lower = text.lower()

    non_real_context = ["exam", "life", "movie", "game", "match", "assignment"]
    if any(word in text_lower for word in non_real_context):
        return None

    disaster_keywords = [
        "earthquake",
        "flood",
        "cyclone",
        "fire",
        "landslide",
        "storm",
        "explosion",
        "accident",
        "tsunami",
        "covid",
        "pandemic"
    ]

    for word in disaster_keywords:
        if word in text_lower:
            return word

    return None


def verify_event(text):
    keyword = extract_keywords(text)

    if keyword is None or not NEWS_API_KEY:
        return {"status": "UNVERIFIED", "confidence": 0.0}

    encoded_query = quote(keyword)
    url = f"https://newsapi.org/v2/everything?q={encoded_query}&pageSize=10&apiKey={NEWS_API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        articles = data.get("articles", [])

        if len(articles) >= 3:
            return {"status": "VERIFIED", "confidence": 1.0}
        elif len(articles) > 0:
            return {"status": "UNVERIFIED", "confidence": 0.4}
        else:
            return {"status": "UNVERIFIED", "confidence": 0.2}

    except Exception:
        return {"status": "UNVERIFIED", "confidence": 0.0}