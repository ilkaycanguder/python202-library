import os
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient

from api import app, lib

def setup_module(module):
    module.tmpdir = tempfile.TemporaryDirectory()
    lib.storage_path = Path(module.tmpdir.name) / "library.json"
    lib.books = []
    lib.save_books()

def teardown_module(module):
    module.tmpdir.cleanup()

def test_get_books_initial():
    client = TestClient(app)
    r = client.get("/books")
    assert r.status_code == 200
    assert r.json() == []

def test_post_and_delete_with_mock(monkeypatch):
    async def fake_fetch(isbn: str):
        if isbn == "9780140449136":
            return {"title": "Crime and punishment", "author": "Fyodor Dostoevsky", "isbn": isbn}
        return None

    import api as api_module
    monkeypatch.setattr(api_module, "fetch_book_by_isbn", fake_fetch)

    client = TestClient(app)

    r = client.post("/books", json={"isbn": "9780140449136"})
    assert r.status_code == 201
    body = r.json()
    assert body["isbn"] == "9780140449136"

    r2 = client.post("/books", json={"isbn": "9780140449136"})
    assert r2.status_code == 409

    r3 = client.get("/books")
    assert r3.status_code == 200
    assert len(r3.json()) == 1

    r4 = client.delete("/books/9780140449136")
    assert r4.status_code == 200
    assert r4.json()["message"] == "Silindi."

    r5 = client.delete("/books/9780140449136")
    assert r5.status_code == 404


def test_put_update_and_refresh_with_mock(monkeypatch):
    calls = {"n": 0}
    async def fake_fetch(isbn: str):
        if isbn != "9780140449136":
            return None
        calls["n"] += 1
        if calls["n"] == 1:
            return {"title": "Crime and punishment", "author": "Fyodor Dostoevsky", "isbn": isbn}
        else:
            return {"title": "Crime and Punishment (Refreshed)", "author": "F. Dostoevsky", "isbn": isbn}

    import api as api_module
    monkeypatch.setattr(api_module, "fetch_book_by_isbn", fake_fetch)

    client = TestClient(app)

    r1 = client.post("/books", json={"isbn": "9780140449136"})
    assert r1.status_code == 201
    assert r1.json()["title"].lower().startswith("crime and punishment")

    r2 = client.put("/books/9780140449136", json={"title": "My Custom Title"})
    assert r2.status_code == 200
    assert r2.json()["title"] == "My Custom Title"
    # Yazar aynı kalmalı (fake_fetch v1’den)
    assert r2.json()["author"] in ["Fyodor Dostoevsky", "F. Dostoevsky"]

    r3 = client.put("/books/9780140449136", json={})
    assert r3.status_code == 200
    assert r3.json()["title"].endswith("(Refreshed)")
    assert r3.json()["author"] == "F. Dostoevsky"

    r4 = client.put("/books/0000000000", json={"title": "X"})
    assert r4.status_code == 404
