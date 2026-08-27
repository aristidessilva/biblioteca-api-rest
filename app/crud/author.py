from sqlalchemy.orm import Session

from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate


def get_author(db: Session, author_id: int) -> Author | None:
    return db.get(Author, author_id)


def list_authors(db: Session, skip: int = 0, limit: int = 100) -> list[Author]:
    return db.query(Author).offset(skip).limit(limit).all()


def create_author(db: Session, author_in: AuthorCreate) -> Author:
    author = Author(**author_in.model_dump())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def update_author(db: Session, author: Author, author_in: AuthorUpdate) -> Author:
    for field, value in author_in.model_dump(exclude_unset=True).items():
        setattr(author, field, value)
    db.commit()
    db.refresh(author)
    return author


def delete_author(db: Session, author: Author) -> None:
    db.delete(author)
    db.commit()
