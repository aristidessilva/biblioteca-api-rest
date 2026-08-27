# 📚 Biblioteca API

API REST para gestão de acervo, membros e empréstimos de uma biblioteca — construída como projeto de portfólio, com foco em boas práticas de backend: arquitetura em camadas, autenticação segura, modelagem relacional e testes automatizados.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)
![License](https://img.shields.io/badge/license-MIT-green)

## Funcionalidades

- Autenticação de bibliotecários via JWT (registro e login)
- CRUD completo de **autores**, **livros** e **membros**
- Empréstimo e devolução de livros com regras de negócio (controle de disponibilidade de cópias)
- Busca de livros por título ou ISBN
- Documentação interativa automática (Swagger UI e ReDoc)
- Suite de testes automatizados (autenticação e fluxo de empréstimo)

## Stack e por que essas escolhas

| Camada | Tecnologia | Motivo |
|---|---|---|
| Framework | FastAPI | Tipagem forte com Pydantic, documentação OpenAPI automática, alta performance assíncrona |
| Banco de dados | PostgreSQL | Banco relacional maduro, ótimo suporte a transações e integridade referencial |
| ORM | SQLAlchemy 2.0 | Padrão de mercado em Python, controle fino sobre queries, evita SQL injection por padrão |
| Migrações | Alembic | Versionamento de schema rastreável, essencial em qualquer time |
| Autenticação | JWT (python-jose) + bcrypt (passlib) | Stateless, escalável horizontalmente, hash de senha com salt |
| Containerização | Docker + Docker Compose | Ambiente reprodutível, sobe API + banco com um comando |

## Arquitetura

Camadas separadas por responsabilidade (inspirado em Clean Architecture, mas sem overengineering para o tamanho do projeto):

```
app/
├── api/          # rotas HTTP (camada de apresentação)
├── core/         # configuração, segurança, conexão com banco
├── crud/         # regras de acesso a dados e regras de negócio
├── models/       # entidades SQLAlchemy (camada de persistência)
├── schemas/      # contratos de entrada/saída (Pydantic)
└── tests/        # testes automatizados
```

Cada camada só conhece a camada abaixo dela — rotas não fazem query direto no banco. Para o porte deste projeto, uma arquitetura hexagonal completa ou microsserviços adicionariam complexidade sem benefício real; um monólito modular bem separado é a escolha certa aqui.

## Segurança implementada

- Senhas nunca armazenadas em texto puro — hash com bcrypt
- Tokens JWT com expiração configurável
- Endpoints de escrita protegidos por autenticação (leitura do catálogo de livros é pública)
- Dados de membros (contêm e-mail) exigem autenticação até para leitura — diferente do catálogo, que é público por design
- Validação de entrada em toda a API via Pydantic, antes de qualquer dado tocar o banco
- Queries sempre parametrizadas via ORM — sem concatenação de SQL, sem risco de SQL Injection
- Violações de integridade referencial (ex: apagar autor com livros) retornam 409 tratado, não um 500 cru
- Segredos (chave JWT, credenciais de banco) via variáveis de ambiente — `.env` está no `.gitignore`
- CORS explicitamente configurado (sem `*` em produção)

**Fora do escopo desta versão (próximos passos naturais):** refresh tokens com revogação, RBAC com papéis granulares (hoje é só "autenticado ou não"), rate limiting, e um pipeline de CI escaneando dependências vulneráveis.

## Como rodar

### Com Docker (recomendado)

```bash
cp .env.example .env
docker compose up --build
```

A API sobe em `http://localhost:8000`. Documentação interativa em `http://localhost:8000/docs`.

### Manualmente

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edite o .env com sua conexão PostgreSQL local

alembic upgrade head
uvicorn app.main:app --reload
```

## Testes

```bash
pytest
```

Os testes usam SQLite em memória — não é necessário um Postgres real para rodar a suíte. Cobrem: registro/login, proteção de rotas, e o fluxo completo de empréstimo (incluindo a regra de não emprestar livro sem cópia disponível).

## Possíveis evoluções

- Cache com Redis para o catálogo de livros (leitura pesada)
- Endpoint de recomendação de livros usando embeddings (ponte com IA)
- RBAC com papéis (bibliotecário / admin)
- Rate limiting nos endpoints de autenticação

## Licença

MIT — veja [LICENSE](LICENSE).
