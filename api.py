from __future__ import annotations
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import asyncio

from library.library import Library
from library.models import Book
from services.openlibrary import fetch_book_by_isbn

app = FastAPI(title="Python202 Library API", version="1.0.0")

# Kalıcı JSON dosyası (aynı mantık)
lib = Library("library.json")

# ---- Pydantic modeller ----
class BookOut(BaseModel):
    title: str
    author: str
    isbn: str

class ISBNIn(BaseModel):
    isbn: str

# ---- Endpoint'ler ----
@app.get("/books", response_model=List[BookOut])
def get_books():
    return [BookOut(**b.__dict__) for b in lib.list_books()]

@app.post("/books", response_model=BookOut, status_code=201)
async def create_book(payload: ISBNIn):
    # ISBN ile Open Library’den çek
    data = await fetch_book_by_isbn(payload.isbn)
    if not data:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı veya API hatası.")
    book = Book(**data)
    try:
        lib.add_book(book)
    except ValueError:
        raise HTTPException(status_code=409, detail="Bu ISBN zaten mevcut.")
    return BookOut(**book.__dict__)

@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    if not lib.remove_book(isbn):
        raise HTTPException(status_code=404, detail="Kitap bulunamadı.")
    return {"message": "Silindi."}
