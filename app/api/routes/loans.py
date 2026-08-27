from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, DbSession
from app.crud import book as book_crud
from app.crud import loan as loan_crud
from app.crud import member as member_crud
from app.schemas.loan import LoanCreate, LoanRead

router = APIRouter(prefix="/loans", tags=["loans"])


@router.get("", response_model=list[LoanRead])
def list_loans(db: DbSession, current_user: CurrentUser, member_id: int | None = None):
    return loan_crud.list_loans(db, member_id=member_id)


@router.post("", response_model=LoanRead, status_code=status.HTTP_201_CREATED)
def create_loan(loan_in: LoanCreate, db: DbSession, current_user: CurrentUser):
    book = book_crud.get_book(db, loan_in.book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado.")
    if not member_crud.get_member(db, loan_in.member_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membro não encontrado.")

    try:
        return loan_crud.create_loan(db, loan_in, book)
    except loan_crud.BookUnavailableError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.put("/{loan_id}/return", response_model=LoanRead)
def return_loan(loan_id: int, db: DbSession, current_user: CurrentUser):
    loan = loan_crud.get_loan(db, loan_id)
    if not loan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empréstimo não encontrado.")
    if loan.is_returned:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este empréstimo já foi devolvido.")
    book = book_crud.get_book(db, loan.book_id)
    return loan_crud.return_loan(db, loan, book)
