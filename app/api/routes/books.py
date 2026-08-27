from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.deps import CurrentUser, DbSession
from app.crud import author as author_crud
from app.crud import book as book_crud
from app.schemas.book import BookCreate, BookRead, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=list[BookRead])
def list_books(db: DbSession, search: str | None = None, skip: int = 0, limit: int = 100):
    return book_crud.list_books(db, search=search, skip=skip, limit=limit)


@router.post("", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(book_in: BookCreate, db: DbSession, current_user: CurrentUser):
    if not author_crud.get_author(db, book_in.author_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Autor informado não existe.")
    if book_crud.get_book_by_isbn(db, book_in.isbn):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ISBN já cadastrado.")
    return book_crud.create_book(db, book_in)


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: DbSession):
    book = book_crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado.")
    return book


@router.put("/{book_id}", response_model=BookRead)
def update_book(book_id: int, book_in: BookUpdate, db: DbSession, current_user: CurrentUser):
    book = book_crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado.")
    return book_crud.update_book(db, book, book_in)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: DbSession, current_user: CurrentUser):
    book = book_crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado.")
    try:
        book_crud.delete_book(db, book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível remover um livro que possui histórico de empréstimos.",
        )
