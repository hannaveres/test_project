import os
import json
import requests

def search_google(query):
    
    """Vyhledá klíčové slovo na Googlu pomocí SERP API
    a uloží organické výsledky první stranky dp JSON souboru.
    """
    
    # načtení API klíče z proměnné prostředí
    api_key = os.getenv("SERPAPI_KEY")
    if api_key is None:
        print("Chyba: proměnná SERPAPI_KEY není nastavena.")
        return []

    # odeslání požadavku na SERP API
    response = requests.get(
        "https://serpapi.com/search",
        params={
            "engine": "google",         # použití Google vyhledávače
            "q": query,                 # klíčove slovo zadané uživatelem
            "api_key": api_key,         # API klíč
            "num": 10,                  # první stránka výsledků (cca 10)
        },
        timeout=10,                     # ochrana proti nekonečnému čekání
    )

    # kontrola HTTP chyb (4xx/ 5xx)
    response.raise_for_status()
    # převod odpovědi na JSON
    data = response.json()

    results = []
    
    # zpracování pouze organických výsledků výhledávání
    for item in data.get("organic_results", []):
        results.append({
            "title": item.get("title"),
            "url": item.get("link"),
            "description": item.get("snippet"),
        })
    
    # uložení výsledků do strukturovaného  JSON souboru na PC
    with open("results.json", "w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=2)

    return results

    #přiklad použití funkce
    if __name__ == "__main__":
        search_query = input("Zadejte klíčové slovo: ")
        search_google(search_query)
