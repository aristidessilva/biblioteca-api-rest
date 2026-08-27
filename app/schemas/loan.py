from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class LoanCreate(BaseModel):
    book_id: int
    member_id: int
    loan_days: int = 14


class LoanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    book_id: int
    member_id: int
    loan_date: datetime
    due_date: date
    return_date: date | None
    is_returned: bool
