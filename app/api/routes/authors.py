from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.deps import CurrentUser, DbSession
from app.crud import author as author_crud
from app.schemas.author import AuthorCreate, AuthorRead, AuthorUpdate

router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("", response_model=list[AuthorRead])
def list_authors(db: DbSession, skip: int = 0, limit: int = 100):
    return author_crud.list_authors(db, skip=skip, limit=limit)


@router.post("", response_model=AuthorRead, status_code=status.HTTP_201_CREATED)
def create_author(author_in: AuthorCreate, db: DbSession, current_user: CurrentUser):
    return author_crud.create_author(db, author_in)


@router.get("/{author_id}", response_model=AuthorRead)
def get_author(author_id: int, db: DbSession):
    author = author_crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor não encontrado.")
    return author


@router.put("/{author_id}", response_model=AuthorRead)
def update_author(author_id: int, author_in: AuthorUpdate, db: DbSession, current_user: CurrentUser):
    author = author_crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor não encontrado.")
    return author_crud.update_author(db, author, author_in)


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: DbSession, current_user: CurrentUser):
    author = author_crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor não encontrado.")
    try:
        author_crud.delete_author(db, author)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível remover um autor que possui livros cadastrados.",
        )
