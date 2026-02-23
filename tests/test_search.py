# tests/test_search.py
from app.search import search_google
import requests

def test_search_google_returns_structured_results(monkeypatch):
    # nastavíme proměnnou prostředí, aby funkce nepadala kvůli chybějícímu API klíči
    monkeypatch.setenv("SERPAPI_KEY", "dummy_key")

    # vytvoříme falešnou odpověď, kterou vrátí requests.get
    class MockResponse:
        def json(self):
            # tohle je struktura, kterou očekáváme od SerpAPI
            return {
                "organic_results": [
                    {
                        "title": "Example title",
                        "link": "https://example.com",
                        "snippet": "Description"
                    }
                ]
            }

    # přepíšeme requests.get tak, aby vracel naši falešnou odpověd
    def mock_get(*args, **kwargs):
        return MockResponse()

    # použijeme monkeypatch k nahrazení requests.get naši funkci 
    monkeypatch.setattr(requests, "get", mock_get)

    # zavoléme testovanou funkci
    results = search_google("python")

    # ověříme, že výsledek je seznam
    assert isinstance(results, list)
    # ověříme, že seznam obsahuje jeden prvek
    assert len(results) == 1
    # ověříme obsah prvního výsledku
    assert results[0]["title"] == "Example title"
    assert results[0]["url"] == "https://example.com"
    assert results[0]["description"] == "Description"