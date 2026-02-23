from fastapi import FastAPI, Query
from app.search import search_google
import logging

app = FastAPI()

@app.get("/search")
def search(q: str = Query(..., min_length=1)):
    return search_google(q)

logging.basicConfig(level=logging.DEBUG)