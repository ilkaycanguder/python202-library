import os
import tempfile
import pytest
from library.library import Library, Book

# Testler, services.openlibrary.fetch_book_by_isbn'i mock'layacak
# Böylece internet gerekmez, deterministik sonuç alırız.

@pytest.mark.asyncio
async def test_add_book_via_isbn_with_mock(monkeypatch):
    # 1) Mock (sahte) fonksiyon hazırla
    async def fake_fetch(isbn: str):
        if isbn == "9780140449136":
            return {"title": "Crime and punishment", "author": "Fyodor Dostoevsky", "isbn": isbn}
        return None

    # 2) Hedef fonksiyonu mock'la
    from services import openlibrary as ol
    monkeypatch.setattr(ol, "fetch_book_by_isbn", fake_fetch)

    # 3) Geçici storage ile Library oluştur
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "library.json")
        lib = Library(path)

        data = await ol.fetch_book_by_isbn("9780140449136")
        assert data is not None
        lib.add_book(Book(**data))

        # Kayıt gerçekleşti mi?
        assert len(lib.list_books()) == 1
        assert lib.find_book("9780140449136").title.startswith("Crime")

        # Geçersiz ISBN → None döner
        data2 = await ol.fetch_book_by_isbn("0000000000")
        assert data2 is None
