from dataclasses import dataclass

@dataclass
class Book:
    """Tek bir kitabı temsil eder."""
    title: str
    author: str
    isbn: str  # benzersiz kimlik

    def __str__(self) -> str:
        # PDF örneğine uygun okunaklı çıktı
        return f'{self.title} by {self.author} (ISBN: {self.isbn})'
