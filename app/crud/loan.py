from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.loan import Loan
from app.schemas.loan import LoanCreate


class LoanError(Exception):
    """Erro base para violações de regra de negócio em empréstimos."""


class BookUnavailableError(LoanError):
    pass


def get_loan(db: Session, loan_id: int) -> Loan | None:
    return db.get(Loan, loan_id)


def list_loans(db: Session, member_id: int | None = None, skip: int = 0, limit: int = 100) -> list[Loan]:
    query = db.query(Loan)
    if member_id is not None:
        query = query.filter(Loan.member_id == member_id)
    return query.offset(skip).limit(limit).all()


def create_loan(db: Session, loan_in: LoanCreate, book: Book) -> Loan:
    if book.available_copies < 1:
        raise BookUnavailableError("Não há cópias disponíveis para empréstimo.")

    loan = Loan(
        book_id=loan_in.book_id,
        member_id=loan_in.member_id,
        due_date=date.today() + timedelta(days=loan_in.loan_days),
    )
    book.available_copies -= 1

    db.add(loan)
    db.add(book)
    db.commit()
    db.refresh(loan)
    return loan


def return_loan(db: Session, loan: Loan, book: Book) -> Loan:
    loan.return_date = date.today()
    book.available_copies = min(book.total_copies, book.available_copies + 1)

    db.add(loan)
    db.add(book)
    db.commit()
    db.refresh(loan)
    return loan
