# Async support in Snowflake SQLAlchemy

Snowflake SQLAlchemy supports SQLAlchemy’s [`asyncio` extension](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html), letting you use `AsyncEngine` and `AsyncSession` for non-blocking database access.

## Requirements

Async support is opt-in. Install the `async` extra, which installs `SQLAlchemy[asyncio]` and, with it, [`greenlet`](https://pypi.org/project/greenlet/). The base install is sync-only.

Copy code

```
pip install "snowflake-sqlalchemy[async]"
```

SQLAlchemy 2.1 no longer installs `greenlet` by default. SQLAlchemy 2.0 installs it only on some platforms, such as `x86_64`, `aarch64`, and `amd64`, but not on Apple silicon macOS (`arm64`). Install the `async` extra on SQLAlchemy 2.0 too, rather than relying on SQLAlchemy to install `greenlet`.

- Python 3.11 or later. The 5.x connector dropped Python 3.10 support, so `pip` can’t resolve it on 3.10.
- `snowflake-connector-python` 5.x, installed automatically as a base dependency.
- SQLAlchemy 2.0.44 through 2.1.x (`>=2.0.44,<2.2`).
- `greenlet`, which SQLAlchemy’s asyncio extension relies on, installed by the `async` extra. Without it, async engine creation raises an `ImportError`: `create_snowflake_async_engine()` names `snowflake-sqlalchemy[async]` in the message; on SQLAlchemy 2.1, importing `sqlalchemy.ext.asyncio` fails first with SQLAlchemy’s own `sqlalchemy[asyncio]` hint. Installing either extra fixes it.

Note

If you upgrade an async application from Snowflake SQLAlchemy 2.0.0 to 2.1, switch your requirement to `snowflake-sqlalchemy[async]`. Snowflake SQLAlchemy 2.1 allows SQLAlchemy 2.1, which doesn’t install `greenlet`, so an upgrade without the `async` extra installs cleanly but fails when you create the async engine.

## Quick start

Async support uses the same `snowflake://` URL as the sync dialect. There’s no separate `+driver` suffix, unlike, for example, `postgresql+asyncpg://`. SQLAlchemy detects and selects the async dialect automatically when you call `create_async_engine()`:

Copy code

```
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    'snowflake://{user}:{password}@{account}/'.format(
        user='<your_user_login_name>',
        password='<your_password>',
        account='<account_identifier>',
    )
)

async def main():
    async with engine.connect() as connection:
        results = await connection.execute(text('select current_version()'))
        print(results.scalar())
    await engine.dispose()

asyncio.run(main())
```

If you need a case-sensitive schema name, the same edge case the sync [`create_snowflake_engine()`](/developer-guide/sqlalchemy/sqlalchemy-connect#label-sqlalchemy-create-snowflake-engine) helper handles, use its async counterpart instead of building the URL by hand:

Copy code

```
from snowflake.sqlalchemy import create_snowflake_async_engine

engine = create_snowflake_async_engine(
    'user:password@account/database',
    schema='MixedCaseSchema',
    case_sensitive_schema=True,
)
```

## How it works

- **No new URL scheme.** `create_async_engine()` picks the async dialect through SQLAlchemy’s `get_async_dialect_cls()` hook, so the connection string is identical to sync.
- **DBAPI shim over `snowflake.connector.aio`.** Internally, the dialect wraps the connector’s native async driver behind a synchronous-looking PEP 249 facade, bridging blocking calls onto the running event loop with greenlets (`await_only`). This is the same strategy SQLAlchemy’s own `aiomysql`, `asyncmy`, and `aiosqlite` dialects use.

## Usage notes

These notes follow directly from SQLAlchemy’s own asyncio rules. They aren’t Snowflake-specific, but they’re worth restating here:

- **No lazy loading.** Accessing an unloaded ORM relationship or deferred column outside an active greenlet context raises an error. Use eager loading (`selectinload()`, `joinedload()`), the `AsyncAttrs` mixin (`await obj.awaitable_attrs.rel`), or wrap sync-style logic in `AsyncSession.run_sync()`.
- **Set `expire_on_commit=False`** on `async_sessionmaker()` to avoid attribute-expiry-triggered lazy loads after commit. This is a common setting for async sessions.
- **Dispose engines across event loops.** Don’t reuse an `AsyncEngine` (and its pool) across unrelated event loops without calling `await engine.dispose()` first.
- **`?async_fallback=true`** on the URL switches the pool implementation to `FallbackAsyncAdaptedQueuePool` instead of the default `AsyncAdaptedQueuePool`. You only need this for the same edge cases SQLAlchemy documents for other async dialects, where a real running event loop isn’t always guaranteed at pool-checkout time.

## Known limitations

- Test coverage for the async dialect currently covers PUT and GET file transfers and basic ORM operations. Other ORM and session behavior is inherited from SQLAlchemy’s generic asyncio machinery rather than independently verified.
- There’s no async-aware Alembic migration runner. Alembic migrations should continue to use a sync engine or connection.

## Further reading

- [SQLAlchemy: Asynchronous I/O (asyncio)](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Connecting to Snowflake with SQLAlchemy](/developer-guide/sqlalchemy/sqlalchemy-connect)
- [Using Alembic](/developer-guide/sqlalchemy/sqlalchemy-alembic)
