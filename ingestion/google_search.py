# ingestion/google_search.py
import requests
from config import SERPAPI_KEY, TOP_N


def fetch_google_results(keyword: str, top_n: int = TOP_N):
    """
    Fetch top Google results for a given keyword using SerpAPI.
    """
    if not SERPAPI_KEY:
        raise ValueError("SERPAPI_KEY is missing. Add it to .env")

    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": SERPAPI_KEY,
        "num": top_n,
    }

    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()

    organic_results = data.get("organic_results", [])[:top_n]

    results = []
    for r in organic_results:
        results.append({
            "platform": "google",
            "keyword": keyword,
            "rank": r.get("position"),
            "title": r.get("title", "") or "",
            "snippet": r.get("snippet", "") or "",
            "url": r.get("link", "") or "",
        })

    return results
