
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Testy pro vyhledávací funkci.
"""

import os
import sys
import pytest
import requests
from pathlib import Path

# Přidáme cestu k projektu (funguje vždy)
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Nyní můžeme importovat
from app.search import search_google

def test_search_google_returns_structured_results(monkeypatch):
    """
    Testuje, že search_google vrací strukturovaná data.
    """
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
        
        def raise_for_status(self):
            # přidáme tuto metodu - nic nedělá, jen existuje
            pass
    
    # přepíšeme requests.get tak, aby vracel naši falešnou odpověď
    def mock_get(*args, **kwargs):
        return MockResponse()
    
    # použijeme monkeypatch k nahrazení requests.get naší funkcí
    monkeypatch.setattr(requests, "get", mock_get)
    
    # zavoláme testovanou funkci
    results = search_google("python")
    
    # ověříme, že výsledky nejsou prázdné
    assert results is not None
    assert len(results) > 0
    assert results[0]["title"] == "Example title"
    assert results[0]["link"] == "https://example.com"
    assert results[0]["snippet"] == "Description"

def test_search_google_no_api_key(monkeypatch):
    """
    Testuje chování když chybí API klíč.
    """
    # odstraníme API klíč z prostředí
    monkeypatch.delenv("SERPAPI_KEY", raising=False)
    
    # zavoláme testovanou funkci
    results = search_google("python")
    
    # měla by vrátit None nebo prázdný seznam
    assert results is None or results == []