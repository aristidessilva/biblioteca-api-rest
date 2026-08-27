from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


def get_book(db: Session, book_id: int) -> Book | None:
    return db.get(Book, book_id)


def get_book_by_isbn(db: Session, isbn: str) -> Book | None:
    return db.query(Book).filter(Book.isbn == isbn).first()


def list_books(db: Session, search: str | None = None, skip: int = 0, limit: int = 100) -> list[Book]:
    query = db.query(Book)
    if search:
        like = f"%{search}%"
        query = query.filter(or_(Book.title.ilike(like), Book.isbn.ilike(like)))
    return query.offset(skip).limit(limit).all()


def create_book(db: Session, book_in: BookCreate) -> Book:
    book = Book(**book_in.model_dump(), available_copies=book_in.total_copies)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def update_book(db: Session, book: Book, book_in: BookUpdate) -> Book:
    data = book_in.model_dump(exclude_unset=True)
    if "total_copies" in data:
        diff = data["total_copies"] - book.total_copies
        book.available_copies = max(0, book.available_copies + diff)
    for field, value in data.items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book: Book) -> None:
    db.delete(book)
    db.commit()
