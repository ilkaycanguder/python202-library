from __future__ import annotations
from library.library import Library
from library.models import Book
import asyncio
from services.openlibrary import fetch_book_by_isbn

def print_menu():
    print("\n===== Kütüphane Uygulaması =====")
    print("1. Kitap Ekle (ISBN ile otomatik)")
    print("2. Kitap Sil (ISBN)")
    print("3. Kitapları Listele")
    print("4. Kitap Ara (ISBN)")
    print("5. Çıkış")

def add_book_flow(lib: Library):
    isbn = input("ISBN: ").strip()
    if not isbn:
        print("⚠️  ISBN zorunludur.")
        return

    # Open Library çağrısı (Aşama 2)
    data = asyncio.run(fetch_book_by_isbn(isbn))
    if not data:
        print("⚠️  Kitap bulunamadı veya bağlantı hatası.")
        return

    try:
        book = Book(**data)
        lib.add_book(book)
        print(f"✅ Eklendi: {book}")
    except ValueError as e:
        print(f"⚠️  {e}")

def remove_book_flow(lib: Library):
    isbn = input("Silinecek ISBN: ").strip()
    print("✅ Silindi." if lib.remove_book(isbn) else "⚠️  Kitap bulunamadı.")

def list_books_flow(lib: Library):
    books = lib.list_books()
    if not books:
        print("📭 Kütüphane boş.")
        return
    for i, b in enumerate(books, start=1):
        print(f"{i}. {b}")

def find_book_flow(lib: Library):
    isbn = input("ISBN: ").strip()
    b = lib.find_book(isbn)
    print(b if b else "⚠️  Bulunamadı.")

def main():
    lib = Library("library.json")
    while True:
        print_menu()
        choice = input("Seçim: ").strip()
        if choice == "1":
            add_book_flow(lib)
        elif choice == "2":
            remove_book_flow(lib)
        elif choice == "3":
            list_books_flow(lib)
        elif choice == "4":
            find_book_flow(lib)
        elif choice == "5":
            print("Görüşürüz! 💪")
            break
        else:
            print("⚠️  Geçersiz seçim.")

if __name__ == "__main__":
    main()
