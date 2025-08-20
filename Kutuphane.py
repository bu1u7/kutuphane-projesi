import json
from typing import List, Optional
from Kitap import Kitap
import httpx

BASE_URL = "https://openlibrary.org/api/books"

class Kutuphane:
    def __init__(self, storage_file: str = "library.json") -> None:
        self.storage_file = storage_file
        self.books: List[Kitap] = []
        self.load_books()

    def add_book(self, book: Kitap) -> bool:
        if any(b.isbn == book.isbn for b in self.books):
            return False
        self.books.append(book)
        self.save_books()
        return True

    def add_book_by_isbn(self, isbn: str) -> bool:
        try:
            url = f"{BASE_URL}?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
            response = httpx.get(url, timeout=10)

            if response.status_code != 200:
                print("Kitap bulunamadı (API hatası).")
                return False

            data = response.json()
            book_data = data.get(f"ISBN:{isbn}")

            if not book_data:
                print("Kitap bulunamadı (ISBN geçersiz veya veri yok).")
                return False

            title = book_data.get("title", "Bilinmeyen Başlık")
            authors = [a.get("name", "Bilinmeyen Yazar") for a in book_data.get("authors", [])]

            if not authors:
                authors = ["Bilinmeyen Yazar"]

            kitap = Kitap(title=title, author=", ".join(authors), isbn=isbn)
            return self.add_book(kitap)

        except Exception as e:
            print("Hata oluştu:", e)
            return False

    def remove_book(self, isbn: str) -> bool:
        for i, b in enumerate(self.books):
            if b.isbn == isbn:
                self.books.pop(i)
                self.save_books()
                return True
        return False

    def list_books(self) -> List[Kitap]:
        return list(self.books)

    def find_book(self, isbn: str) -> Optional[Kitap]:
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def load_books(self) -> None:
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.books = [Kitap(**item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = []

    def save_books(self) -> None:
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump([b.__dict__ for b in self.books], f, ensure_ascii=False, indent=2)
