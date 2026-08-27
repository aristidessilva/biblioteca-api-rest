from sqlalchemy.orm import Session

from app.models.member import Member
from app.schemas.member import MemberCreate, MemberUpdate


def get_member(db: Session, member_id: int) -> Member | None:
    return db.get(Member, member_id)


def get_member_by_email(db: Session, email: str) -> Member | None:
    return db.query(Member).filter(Member.email == email).first()


def list_members(db: Session, skip: int = 0, limit: int = 100) -> list[Member]:
    return db.query(Member).offset(skip).limit(limit).all()


def create_member(db: Session, member_in: MemberCreate) -> Member:
    member = Member(**member_in.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


def update_member(db: Session, member: Member, member_in: MemberUpdate) -> Member:
    for field, value in member_in.model_dump(exclude_unset=True).items():
        setattr(member, field, value)
    db.commit()
    db.refresh(member)
    return member


def delete_member(db: Session, member: Member) -> None:
    db.delete(member)
    db.commit()
