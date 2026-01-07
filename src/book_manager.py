from dataclasses import dataclass, asdict
from typing import List, Optional
import json
from pathlib import Path


@dataclass
class Book:
    isbn: str
    title: str
    author: str
    year: Optional[int] = None

    def to_dict(self):
        return asdict(self)


class Library:
    def __init__(self):
        self._books: List[Book] = []

    def add_book(self, book: Book) -> bool:
        if any(b.isbn == book.isbn for b in self._books):
            return False
        self._books.append(book)
        return True

    def remove_by_isbn(self, isbn: str) -> bool:
        for i, b in enumerate(self._books):
            if b.isbn == isbn:
                del self._books[i]
                return True
        return False

    def find_by_title(self, query: str) -> List[Book]:
        q = query.lower()
        return [b for b in self._books if q in b.title.lower()]

    def list_books(self) -> List[Book]:
        return list(self._books)

    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        for b in self._books:
            if b.isbn == isbn:
                return b
        return None

    def save(self, path: str = "books.json") -> None:
        p = Path(path)
        data = [b.to_dict() for b in self._books]
        p.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def load(self, path: str = "books.json") -> None:
        p = Path(path)
        if not p.exists():
            return
        data = json.loads(p.read_text())
        self._books = [Book(**item) for item in data]
