import os
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient

# API ve global lib nesnesi
from api import app, lib

def setup_module(module):
    # Her test modülü için geçici JSON dosyası kullan
    module.tmpdir = tempfile.TemporaryDirectory()
    # >>> ÖNEMLİ: storage_path str değil, Path olmalı
    lib.storage_path = Path(module.tmpdir.name) / "library.json"
    # Temiz başlangıç
    lib.books = []
    lib.save_books()  # boş dosya oluştur

def teardown_module(module):
    module.tmpdir.cleanup()

def test_get_books_initial():
    client = TestClient(app)
    r = client.get("/books")
    assert r.status_code == 200
    assert r.json() == []

def test_post_and_delete_with_mock(monkeypatch):
    # Open Library çağrısını mock’la → internet gerekmesin
    async def fake_fetch(isbn: str):
        if isbn == "9780140449136":
            return {"title": "Crime and punishment", "author": "Fyodor Dostoevsky", "isbn": isbn}
        return None

    from services import openlibrary as ol
    monkeypatch.setattr(ol, "fetch_book_by_isbn", fake_fetch)

    client = TestClient(app)

    # POST /books (başarılı)
    r = client.post("/books", json={"isbn": "9780140449136"})
    assert r.status_code == 201
    body = r.json()
    assert body["isbn"] == "9780140449136"

    # POST /books (duplicate → 409)
    r2 = client.post("/books", json={"isbn": "9780140449136"})
    assert r2.status_code == 409

    # GET /books → 1 kayıt var
    r3 = client.get("/books")
    assert r3.status_code == 200
    assert len(r3.json()) == 1

    # DELETE /books/{isbn} → silinsin
    r4 = client.delete("/books/9780140449136")
    assert r4.status_code == 200
    assert r4.json()["message"] == "Silindi."

    # DELETE tekrar → 404
    r5 = client.delete("/books/9780140449136")
    assert r5.status_code == 404
