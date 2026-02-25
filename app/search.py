import os
import json
import requests
from datetime import datetime

def search_google(query):
    """
    Vyhledá klíčové slovo na Googlu pomocí SERP API
    a uloží organické výsledky první stranky do JSON souboru.
    """
    
    # načtení API klíče z proměnné prostředí
    api_key = os.getenv("SERPAPI_KEY")
    if api_key is None:
        print("Chyba: proměnná SERPAPI_KEY není nastavena.")
        return []

    try:
        # odeslání požadavku na SERP API
        print(f"Vyhledávám: '{query}'")
        response = requests.get(
            "https://serpapi.com/search",
            params={
                "engine": "google",
                "q": query,
                "api_key": api_key,
                "num": 10,
            },
            timeout=10,
        )
        print(f"Status kód: {response.status_code}")
        
        # kontrola HTTP chyb
        response.raise_for_status()
        
        # převod odpovědi na JSON
        data = response.json()
        print(f"Klíče v odpovědi: {list(data.keys())}")

        # kontrola chyb od API
        if "error" in data:
            print(f"Chyba API: {data['error']}")
            return []

        # extrahujeme pouze organické výsledky
        results = []

        if "organic_results" in data:
            organic_results = data["organic_results"]
            print(f"Počet výsledků: {len(organic_results)}")

            for item in organic_results:
                results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                })

            # Debug: vytiskneme první výsledky
            if results:
                print(f"První výsledek: {results[0]['title'][:50]}...")
        else:
            print("'organic_results' nenalezeno v odpovědi")
            if "error" in data:
                print(f"Chyba API: {data['error']}")

        # uložíme výsledky do JSON souboru
        if results:
            filename = f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump({
                    "query": query,
                    "timestamp": datetime.now().isoformat(),
                    "results": results
                }, f, ensure_ascii=False, indent=2)
            print(f"Výsledky uloženy do souboru: {filename}")
        else: 
            print("Žádné výsledky k uložení.") 
            
        return results
                
    except requests.exceptions.RequestException as e:
        print(f"Chyba při volání API: {e}")
        return []
    except Exception as e:
        print(f"Neočekávaná chyba: {e}")
        return []

# příklad použití funkce
if __name__ == "__main__":
    search_query = input("Zadejte klíčové slovo: ")
    results = search_google(search_query)
    print(f"Nalezeno {len(results)} výsledků")