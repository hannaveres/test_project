from fastapi import FastAPI, Query
from app.search import search_google

app = FastAPI()

@app.get("/search")
def search(q: str = Query(..., min_length=1)):
    """
    Přijme klíčové slovo z HTML formuláře,
    zavolá funkci pro vyhledávání
    a uloží výsledky do JSON souboru.
    """
    return search_google(q)