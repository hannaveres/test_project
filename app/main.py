from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.search import search_google
import os

app = FastAPI(title="Google Search Scraper")

# Nastavení pro HTML šablony
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Hlavní stránka s vyhledávacím formulářem.
    """
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "results": [], 
            "query": ""
        }
    )

@app.get("/search")
async def search(request: Request, q: str = Query(..., min_length=1)):
    """
    Přijme klíčové slovo z HTML formuláře,
    zavolá funkci pro vyhledávání
    a zobrazí výsledky.
    """
    results = search_google(q)
    
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "results": results if results else [],
            "query": q
        }
    )

@app.get("/api/search")
async def api_search(q: str = Query(..., min_length=1)):
    """
    API endpoint pro vyhledávání (vrací JSON).
    """
    results = search_google(q)
    return {
        "query": q,
        "results": results if results else [],
        "count": len(results) if results else 0
    }

@app.get("/health")
async def health():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "message": "Server is running"}