# Using Alembic with Snowflake SQLAlchemy

## Alembic support overview

Snowflake SQLAlchemy supports [Alembic](https://alembic.sqlalchemy.org/), a lightweight database migration tool for SQLAlchemy. Alembic lets you manage schema changes over time using revision files.

Alembic migrations must use a synchronous engine. There’s no async-aware Alembic runner for the Snowflake dialect.

### Installing Alembic

Copy code

```
pip install alembic
```

### Initializing an Alembic repository

Copy code

```
alembic init migrations
```

### Configuring Alembic for Snowflake

Alembic doesn’t ship a built-in implementation for the `snowflake` dialect. You must register one in `migrations/env.py` by subclassing `DefaultImpl`. Without it, every Alembic command that connects fails with `KeyError: 'snowflake'`.

Edit `migrations/env.py`:

Copy code

```
from alembic import context
from alembic.ddl.impl import DefaultImpl
from sqlalchemy import engine_from_config, pool
from snowflake.sqlalchemy.alembic_util import render_item as snowflake_render_item

from myapp.models import Base  # your declarative base or MetaData

class SnowflakeImpl(DefaultImpl):
    __dialect__ = "snowflake"

config = context.config
target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_item=snowflake_render_item,
        )
        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
```

Set `sqlalchemy.url` in `alembic.ini` to your Snowflake connection URL. For URL formats and parameters, see [Connection parameters](/developer-guide/sqlalchemy/sqlalchemy-connect).

## Hand-written migrations

Create manual migrations for fine-grained control:

Copy code

```
alembic revision -m "add_user_table"
```

This creates a migration file. Edit it to add your changes:

Copy code

```
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.elements import quoted_name

def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column(quoted_name("mycol", True), sa.String()),  # quoted: "mycol" in Snowflake
        sa.PrimaryKeyConstraint("id"),
    )

def downgrade():
    op.drop_table("users")
```

Use `quoted_name` for case-sensitive column names. Snowflake stores unquoted names in uppercase, so the table above has the columns `ID`, `NAME`, and `mycol`.

Pass `quoted_name` everywhere a migration refers to a case-sensitive column, including `op.drop_column` and `op.alter_column`. A plain string such as `op.drop_column("users", "mycol")` targets `MYCOL` and fails:

Copy code

```
op.drop_column("users", quoted_name("mycol", True))
```

Run migrations:

Copy code

```
alembic upgrade head
```

## Case-sensitive schema configuration

When the migrations or the Alembic version table live in a case-sensitive (quoted, lowercase) schema, pass the schema as `quoted_name(..., True)`:

Copy code

```
from sqlalchemy.sql.elements import quoted_name

def include_name(name, type_, parent_names):
    if type_ == "schema":
        return name == "myschema"
    return True

context.configure(
    connection=connection,
    target_metadata=target_metadata,
    include_schemas=True,
    include_name=include_name,
    version_table_schema=quoted_name("myschema", True),
    render_item=snowflake_render_item,
)
```

To make the case-sensitive schema the connection’s default schema, percent-encode the quotes in `sqlalchemy.url`, for example `snowflake://<user_login_name>:<password>@<account_identifier>/mydb/%22myschema%22`. For other ways to set it, see [Connection parameters](/developer-guide/sqlalchemy/sqlalchemy-connect).

Keep the following in mind:

- Don’t pass `"%22myschema%22"` as `version_table_schema`. Percent-encoding applies only to URLs. Here, Snowflake treats the value as a literal schema name and fails with a `002003` SQL compilation error.
- The quoted-string form `version_table_schema='"myschema"'` works only when the engine is created with `case_sensitive_identifiers=True`. Without that flag the quotes are stripped and Snowflake resolves the name to `MYSCHEMA`.

Note

With `include_schemas=True`, Alembic passes each result of `inspector.get_schema_names()` to `include_name`. A schema that was created quoted in lowercase (`"myschema"`) is returned as `quoted_name("myschema", True)`. A schema created unquoted (stored as `MYSCHEMA`) is returned as the plain lowercase string `"myschema"`. Both compare equal to `"myschema"` because `quoted_name` is a `str` subclass, so filter against the lowercase value.

## Alembic autogenerate with case-sensitive columns

Alembic’s default renderer writes a `quoted_name("mycol", True)` column as the plain string `'mycol'`, so the generated migration creates a case-insensitive `MYCOL` column. To preserve case, register the `render_item` hook in `env.py` (as shown in [Configuring Alembic for Snowflake](#label-alembic-configuring)):

Copy code

```
from snowflake.sqlalchemy.alembic_util import render_item as snowflake_render_item

context.configure(
    connection=connection,
    target_metadata=target_metadata,
    render_item=snowflake_render_item,
)
```

With the hook, a new case-sensitive column is rendered as:

Copy code

```
op.add_column("users", sa.Column(sa.sql.elements.quoted_name("extra", True), sa.Integer(), nullable=True))
```

Keep the following in mind:

- The hook is opt-in for each project. Alembic has no dialect-level rendering hook, so `env.py` is the only place to register it.
- The hook only affects column rendering. The generated `downgrade()` still contains `op.drop_column("users", "extra")`, which fails against the case-sensitive column. Change it to `op.drop_column("users", quoted_name("extra", True))` before you run it.
- Autogenerate can report type differences between your model types and the types that Snowflake reflects. For example, an `sa.Integer()` column reflects as `NUMBER(38,0)`, which produces an `op.alter_column(..., type_=sa.Integer())` on every run. Review these operations, or pass `compare_type=False` to `context.configure()` if you don’t need type comparison.

## Patterns that do not work

### Plain unquoted strings as case-sensitive schemas

Using a plain lowercase string as a schema name doesn’t preserve case:

Copy code

```
# WRONG: "myschema" is denormalized to MYSCHEMA
Table("my_table", metadata, schema="myschema")

class MyModel(Base):
    __tablename__ = "my_table"
    __table_args__ = {"schema": "myschema"}  # Also wrong
```

A plain lowercase string has no `quote` attribute, so the dialect converts it to `MYSCHEMA` before it reaches Snowflake. If a schema named `MYSCHEMA` exists, the query succeeds silently against the wrong schema.

Instead, use `quoted_name("myschema", True)`:

Copy code

```
from sqlalchemy.sql.elements import quoted_name

Table("my_table", metadata, schema=quoted_name("myschema", True))

# Or set it once on the metadata
metadata = MetaData(schema=quoted_name("myschema", True))
Table("my_table", metadata)
```

The quoted-string form `schema='"myschema"'` gives the same result only when the engine is created with `case_sensitive_identifiers=True`. For details, see [Case-sensitive identifiers](/developer-guide/sqlalchemy/sqlalchemy-limitations#label-case-sensitive-identifiers).

## Best practices

- Always register `SnowflakeImpl` and the `snowflake_render_item` hook in `env.py`.
- Use `quoted_name` for case-sensitive identifiers in models and in every migration operation; avoid plain lowercase strings.
- Review autogenerated migrations before applying them, especially `downgrade()` operations on case-sensitive columns and type changes.
- Test migrations in a development environment before applying them to production.
- Keep migration files in version control for a full audit trail and rollback capability.
- Snowflake commits the open transaction before each DDL statement, so a failed migration can’t roll back DDL that already ran. For details, see [Known limitations](/developer-guide/sqlalchemy/sqlalchemy-limitations#label-sqlalchemy-transactions-limitations).
