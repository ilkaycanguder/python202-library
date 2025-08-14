from __future__ import annotations
import json
from pathlib import Path
from typing import List, Optional, Union

from library.models import Book

class Library:
    """
    Kütüphane operasyonlarını yönetir.
    - books: Bellekteki kitap listesi
    - storage_path: JSON kalıcılık dosyası (library.json)
    """
    def __init__(self, storage_path: Union[str, Path] = "library.json") -> None:
        self.storage_path = Path(storage_path)
        self.books: List[Book] = []
        self.load_books()

    # --------- Kalıcılık ---------
    def load_books(self) -> None:
        """Uygulama başlarken library.json içeriğini yükler."""
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text(encoding="utf-8"))
                self.books = [Book(**item) for item in data]
            except Exception:
                # Dosya bozuksa veri kaybı yaşamamak için temiz başla
                self.books = []
        else:
            # dosya yoksa oluştur
            self.save_books()

    def save_books(self) -> None:
        """Kitap listesinde değişiklik olduğunda JSON dosyasına yazar."""
        payload = [b.__dict__ for b in self.books]
        self.storage_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    # --------- İşlemler ---------
    def add_book(self, book: Book) -> None:
        """Yeni bir Book nesnesini kütüphaneye ekler ve dosyayı günceller."""
        if self.find_book(book.isbn):
            raise ValueError("Bu ISBN zaten mevcut.")
        self.books.append(book)
        self.save_books()

    def remove_book(self, isbn: str) -> bool:
        """ISBN'e göre kitabı siler ve dosyayı günceller. Başarıyla silerse True döner."""
        before = len(self.books)
        self.books = [b for b in self.books if b.isbn != isbn]
        changed = len(self.books) != before
        if changed:
            self.save_books()
        return changed

    def list_books(self) -> List[Book]:
        """Tüm kitapları listeler."""
        return list(self.books)

    def find_book(self, isbn: str) -> Optional[Book]:
        """ISBN ile kitabı bulur; yoksa None."""
        return next((b for b in self.books if b.isbn == isbn), None)
