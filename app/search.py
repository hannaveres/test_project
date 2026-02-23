import os
import requests

def search_google(query: str):
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        raise RuntimeError("SERPAPI_KEY is not set")

    response = requests.get(
        "https://serpapi.com/search",
        params={
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "num": 5,
        },
        timeout=10,
    )

    data = response.json()

    results = []
    for item in data.get("organic_results", []):
        results.append({
            "title": item.get("title"),
            "url": item.get("link"),
            "description": item.get("snippet"),
        })

    return results
