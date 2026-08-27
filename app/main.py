from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, authors, books, members, loans
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="API REST para gestão de acervo, membros e empréstimos de uma biblioteca.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(authors.router)
app.include_router(books.router)
app.include_router(members.router)
app.include_router(loans.router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
