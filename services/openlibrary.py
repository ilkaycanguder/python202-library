from __future__ import annotations
from typing import Optional, List
import httpx

BASE = "https://openlibrary.org"

HEADERS = {
    "User-Agent": "python202-library-app/1.0 (+https://openlibrary.org)"
}

async def _fetch_primary(client: httpx.AsyncClient, isbn: str) -> Optional[dict]:
    """
    Primary yol: /api/books?bibkeys=ISBN:<isbn>&format=json&jscmd=data
    Tek istekte title ve authors dönebiliyor.
    """
    url = f"{BASE}/api/books"
    params = {"bibkeys": f"ISBN:{isbn}", "format": "json", "jscmd": "data"}
    r = await client.get(url, params=params, headers=HEADERS)
    r.raise_for_status()
    data = r.json() or {}
    item = data.get(f"ISBN:{isbn}")
    if not item:
        return None
    title = item.get("title")
    authors: List[dict] = item.get("authors") or []
    names = [a.get("name") for a in authors if a.get("name")]
    author = ", ".join(names) if names else "Unknown"
    if not title:
        return None
    return {"title": title, "author": author, "isbn": isbn}

async def _fetch_fallback(client: httpx.AsyncClient, isbn: str) -> Optional[dict]:
    """
    Fallback yol: /isbn/<isbn>.json + (varsa) /authors/<id>.json ile isim çözme
    """
    book_url = f"{BASE}/isbn/{isbn}.json"
    r = await client.get(book_url, headers=HEADERS)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    data = r.json()
    title = data.get("title")
    if not title:
        return None

    authors = data.get("authors", [])
    names = []
    for a in authors:
        key = a.get("key")
        if not key:
            continue
        try:
            ar = await client.get(f"{BASE}{key}.json", headers=HEADERS)
            if ar.status_code == 200:
                nm = ar.json().get("name")
                if nm:
                    names.append(nm)
        except Exception:
            # yazar çözme hatasında geç
            pass
    author = ", ".join(names) if names else "Unknown"
    return {"title": title, "author": author, "isbn": isbn}

async def fetch_book_by_isbn(isbn: str) -> Optional[dict]:
    """
    ISBN ile kitap bilgisi getir.
    1) Primary API yolunu dene
    2) Olmazsa fallback yolu
    Hata/erişim sorununda None dön.
    """
    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            # 1) Primary
            try:
                result = await _fetch_primary(client, isbn)
                if result:
                    return result
            except httpx.HTTPError:
                # primary hata verdiyse fallback'e geç
                pass

            # 2) Fallback
            try:
                result = await _fetch_fallback(client, isbn)
                if result:
                    return result
            except httpx.HTTPError:
                return None

    except (httpx.ConnectError, httpx.ReadTimeout, httpx.ConnectTimeout, httpx.ProxyError):
        # ağ/proxy/timeout sorunları
        return None

    return None
