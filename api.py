from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from Kutuphane import Kutuphane
from Kitap import Kitap

app = FastAPI(title="Kütüphane API")
kutuphane = Kutuphane()

class Book(BaseModel):
    title: str
    author: str
    isbn: str

class ISBNRequest(BaseModel):
    isbn: str

@app.get("/books", response_model=List[Book])
def get_books():
    return kutuphane.list_books()

@app.post("/books", response_model=Book)
def add_book(isbn_request: ISBNRequest):
    success = kutuphane.add_book_by_isbn(isbn_request.isbn)
    if not success:
        raise HTTPException(status_code=400, detail="Kitap eklenemedi veya bulunamadı.")
    kitap = kutuphane.find_book(isbn_request.isbn)
    return kitap

@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    success = kutuphane.remove_book(isbn)
    if not success:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı.")
    return {"message": f"{isbn} ISBN numaralı kitap silindi."}