import os
import tempfile
import pytest
from library.library import Library
from library.models import Book

def test_add_list_find_remove():
    with tempfile.TemporaryDirectory() as tmp:
        store = os.path.join(tmp, "library.json")
        lib = Library(store)
        assert lib.list_books() == []

        b = Book(title="Ulysses", author="James Joyce", isbn="9780199535675")
        lib.add_book(b)
        assert len(lib.list_books()) == 1
        assert lib.find_book(b.isbn) is not None

        # duplicate engeli
        with pytest.raises(ValueError):
            lib.add_book(b)

        # silme
        assert lib.remove_book(b.isbn) is True
        assert lib.remove_book(b.isbn) is False
