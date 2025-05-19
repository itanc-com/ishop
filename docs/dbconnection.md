## Conceptual diagram
                            ┌────────────┐
                            │  FastAPI   │
                            └────┬───────┘
                                 │
              ┌──────────────────┴──────────────────┐
              │                                     │
     High-Level ORM                        Low-Level SQL
     AsyncSession (ORM)                   AsyncConnection (Core)
              │                                     │
     ┌────────▼────────┐                 ┌──────────▼────────┐
     │ sessionmanager  │                 │ sessionmanager     │
     │ .session()      │                 │ .connect()         │
     └─────────────────┘                 └────────────────────┘
              │                                     │
       Business Logic                     Raw SQL, Migrations, Setup


## describe each method


| Method                                                                 | Defined In                  | Returns         | Level        | Description                                                                 |
|------------------------------------------------------------------------|-----------------------------|------------------|--------------|-----------------------------------------------------------------------------|
| `@contextlib.asynccontextmanager async def connect(...)`              | `database_session_manager.py` | `AsyncConnection` | Low-level SQL | Provides raw DB connection for executing raw SQL or DDL operations.         |
| `@contextlib.asynccontextmanager async def session(...)`              | `database_session_manager.py` | `AsyncSession`    | High-level ORM | Provides a safe ORM session with auto rollback and close handling.          |
| `async def get_db_session() -> AsyncGenerator[AsyncSession, None]`    | `session.py`                | `AsyncSession`    | High-level ORM | FastAPI-compatible dependency that yields a managed async ORM session.      |
