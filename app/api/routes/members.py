from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.deps import CurrentUser, DbSession
from app.crud import member as member_crud
from app.schemas.member import MemberCreate, MemberRead, MemberUpdate

router = APIRouter(prefix="/members", tags=["members"])


@router.get("", response_model=list[MemberRead])
def list_members(db: DbSession, current_user: CurrentUser, skip: int = 0, limit: int = 100):
    return member_crud.list_members(db, skip=skip, limit=limit)


@router.post("", response_model=MemberRead, status_code=status.HTTP_201_CREATED)
def create_member(member_in: MemberCreate, db: DbSession, current_user: CurrentUser):
    if member_crud.get_member_by_email(db, member_in.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail já cadastrado.")
    return member_crud.create_member(db, member_in)


@router.get("/{member_id}", response_model=MemberRead)
def get_member(member_id: int, db: DbSession, current_user: CurrentUser):
    member = member_crud.get_member(db, member_id)
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membro não encontrado.")
    return member


@router.put("/{member_id}", response_model=MemberRead)
def update_member(member_id: int, member_in: MemberUpdate, db: DbSession, current_user: CurrentUser):
    member = member_crud.get_member(db, member_id)
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membro não encontrado.")
    return member_crud.update_member(db, member, member_in)


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: int, db: DbSession, current_user: CurrentUser):
    member = member_crud.get_member(db, member_id)
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membro não encontrado.")
    try:
        member_crud.delete_member(db, member)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível remover um membro que possui histórico de empréstimos.",
        )
