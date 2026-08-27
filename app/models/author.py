from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    nationality: Mapped[str | None] = mapped_column(String(80), nullable=True)

    # Sem cascade delete: remover um autor com livros cadastrados deve falhar
    # de forma controlada (ver IntegrityError tratado nas rotas), não apagar
    # o histórico silenciosamente.
    books: Mapped[list["Book"]] = relationship(back_populates="author")
