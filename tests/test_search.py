# tests/test_search.py
from app.search import search_google
import requests

def test_search_google_returns_structured_results(monkeypatch):
    # Мокаем переменную окружения, чтобы функция не падала
    monkeypatch.setenv("SERPAPI_KEY", "dummy_key")

    # Создаем мок-ответ для requests.get
    class MockResponse:
        def json(self):
            return {
                "organic_results": [
                    {
                        "title": "Example title",
                        "link": "https://example.com",
                        "snippet": "Description"
                    }
                ]
            }

    # Мокаем requests.get через monkeypatch
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    # Вызываем функцию
    results = search_google("python")

    # Проверяем структуру результата
    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0]["title"] == "Example title"
    assert results[0]["url"] == "https://example.com"
    assert results[0]["description"] == "Description"