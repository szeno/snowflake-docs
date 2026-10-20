# Known limitations of Snowflake SQLAlchemy

This topic describes SQLAlchemy features that Snowflake SQLAlchemy doesn’t support, or supports with restrictions, and the recommended workarounds.

## Unsupported SQLAlchemy features

Snowflake doesn’t support the following SQLAlchemy features:

| Feature | Notes |
| --- | --- |
| `RETURNING` (`insert().returning()`, `update().returning()`) | The ORM can’t fetch server-generated primary keys. See [Identity columns as primary keys](#label-identity-columns-as-primary-keys). |
| Savepoints (`begin_nested()`) | See [Transactions](#label-sqlalchemy-transactions-limitations). |
| Server-side cursors (`stream_results=True`, `yield_per`) |  |
| Empty inserts (`INSERT INTO t DEFAULT VALUES`) | Supply at least one column value. |
| Computed columns (`Computed()`) |  |
| Check constraint reflection | `inspector.get_check_constraints()` doesn’t return constraints. |
| `DISTINCT ON` | Use `QUALIFY` with a window function, or `GROUP BY`. |
| `IS TRUE` / `IS FALSE` | Compare with `col == true()` or `col == false()` instead. |
| Indexes on standard tables | Indexes are only supported on [hybrid tables](/developer-guide/sqlalchemy/sqlalchemy-ddl#label-sqlalchemy-ddl-hybrid). |

Expand

Show lessSee more

## Identity columns as primary keys

Using SQLAlchemy’s `Identity()` construct on a primary key column isn’t compatible with the SQLAlchemy ORM.

After an `INSERT`, the ORM must retrieve the generated primary key to populate the in-memory object. SQLAlchemy does this with either `RETURNING`, which Snowflake doesn’t support, or `cursor.lastrowid`, which the Snowflake Connector for Python always returns as `None`. Without either one, the flush fails:

Copy code

```
from sqlalchemy import Column, Identity, Integer, String
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class MyModel(Base):
    __tablename__ = "my_model"
    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)  # doesn't work with the ORM
    name = Column(String)

Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add(MyModel(name="test"))
    session.commit()  # raises sqlalchemy.orm.exc.FlushError: ... has a NULL identity key
```

To surface the problem early, the dialect emits a `SnowflakeWarning` when it compiles the DDL for an `Identity()` primary key column. The warning is emitted once for each table and column pair in a Python process. To silence it, use a standard warning filter:

Copy code

```
import warnings
from snowflake.sqlalchemy.exc import SnowflakeWarning

warnings.filterwarnings("ignore", category=SnowflakeWarning)
```

Or set the `PYTHONWARNINGS` environment variable before starting your application:

Copy code

```
PYTHONWARNINGS=ignore::snowflake.sqlalchemy.exc.SnowflakeWarning python my_app.py
```

**Workaround:** Use `Sequence()` instead of `Identity()`. The ORM fetches the next sequence value before the `INSERT`, so the primary key is populated:

Copy code

```
from sqlalchemy import Column, Integer, Sequence, String
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class MyModel(Base):
    __tablename__ = "my_model"
    id = Column(Integer, Sequence("my_model_id_seq"), primary_key=True)
    name = Column(String)

Base.metadata.create_all(engine)

with Session(engine) as session:
    obj = MyModel(name="test")
    session.add(obj)
    session.commit()
    print(obj.id)  # populated, for example 1
```

## Transactions

Connections use the `READ COMMITTED` isolation level with autocommit turned off, so `engine.begin()`, `connection.commit()`, `connection.rollback()`, and ORM `Session` transactions work as documented by SQLAlchemy. Two [Snowflake transaction rules](/sql-reference/transactions) differ from many other databases:

- **DDL commits the open transaction.** Each DDL statement (`CREATE`, `ALTER`, `DROP`, and so on) runs in its own transaction, and any open transaction is committed first. DML issued before the DDL can’t be rolled back afterward:

  Copy code

  ```
  from sqlalchemy import text

  with engine.connect() as conn:
      conn.execute(text("INSERT INTO t VALUES (2)"))
      conn.execute(text("CREATE OR REPLACE TABLE t2 (y INT)"))  # commits the INSERT
      conn.rollback()  # the inserted row is kept
  ```

  This also applies to Alembic migrations: DDL that already ran isn’t rolled back when a later step fails.
- **No savepoints.** `connection.begin_nested()` and `Session.begin_nested()` raise `sqlalchemy.exc.ProgrammingError` when SQLAlchemy emits the `SAVEPOINT` statement, because Snowflake rejects it. The outer transaction stays open and can still be committed or rolled back.

## PUT with a file stream (BytesIO)

The Snowflake Connector for Python accepts an in-memory `file_stream` argument for `PUT`, but SQLAlchemy’s `Connection.execute()` treats every key in the parameters dictionary as a bound SQL parameter. The `file_stream` value never reaches the connector, so the `PUT` fails:

Copy code

```
from io import BytesIO
from sqlalchemy import text

buf = BytesIO(b"file contents")

# WRONG: file_stream isn't passed to the connector's PUT
with engine.connect() as conn:
    conn.execute(text("PUT file://example.txt @my_stage"), {"file_stream": buf})
# snowflake.connector.errors.ProgrammingError: 253006: ... File does not exist: example.txt
```

**Workaround:** Use the raw connector cursor for `PUT` and `GET` with file streams. You can get one from the engine without opening a separate connection:

Copy code

```
from io import BytesIO

buf = BytesIO(b"file contents")

raw = engine.raw_connection()
try:
    cur = raw.cursor()
    cur.execute(
        "PUT file://example.txt @my_stage auto_compress=true",
        file_stream=buf,
    )
finally:
    raw.close()
```

The file name in the `file://` URL becomes the name of the staged file. Regular SQL, including `PUT` from a local file path and `COPY INTO`, works through SQLAlchemy as usual. To upload a local file, build a valid `file://` URL from its path:

Copy code

```
from pathlib import Path
from sqlalchemy import text

local_file = Path("/tmp/myfile.txt")

with engine.begin() as conn:
    conn.execute(text(f"PUT {local_file.as_uri()} @my_stage"))
```

## Async support

[Async support](/developer-guide/sqlalchemy/sqlalchemy-async) (`create_async_engine()`) depends on `snowflake-connector-python` 5.x and requires `greenlet`. There’s no async-aware Alembic runner; run [Alembic migrations](/developer-guide/sqlalchemy/sqlalchemy-alembic) with a synchronous engine.

## Reflecting very large schemas

Snowflake `SHOW` commands return at most 10,000 rows. The dialect pages through the object-listing commands (tables, views, temporary tables, schemas, and sequences) automatically. The schema-wide constraint and index commands used by bulk reflection (`MetaData.reflect()`) aren’t paged, and can fail on schemas with more than 10,000 rows of output:

- `SHOW PRIMARY KEYS IN SCHEMA`
- `SHOW UNIQUE KEYS IN SCHEMA`
- `SHOW IMPORTED KEYS IN SCHEMA`
- `SHOW INDEXES IN SCHEMA`

Reflecting a single table (for example, `inspector.get_pk_constraint("t")`) isn’t affected. For more information, see [Schema reflection](/developer-guide/sqlalchemy/sqlalchemy-reflection).

## Case-sensitive identifiers

Snowflake stores unquoted identifiers in uppercase and treats them as case-insensitive, while quoted identifiers preserve case. SQLAlchemy uses lowercase for case-insensitive names. The dialect maps between the two conventions, but a few cases need explicit handling.

### Object name case handling

By default, plain names are case-insensitive and become uppercase in Snowflake. Use `quoted_name(..., True)` for case-sensitive names:

Copy code

```
from sqlalchemy import Table, Column, Integer, MetaData
from sqlalchemy.sql.elements import quoted_name

metadata = MetaData()

# Case-insensitive: created as MY_TABLE in Snowflake
t1 = Table("my_table", metadata, Column("id", Integer))

# Case-sensitive: created as "my_table" in Snowflake
t2 = Table(quoted_name("my_table", True), metadata, Column("id", Integer))
```

In raw SQL, quote case-sensitive names yourself. Without the quotes, Snowflake resolves the name to uppercase:

Copy code

```
SELECT * FROM "my_table";  -- the case-sensitive table
SELECT * FROM my_table;    -- MY_TABLE
```

For how reflected names map to `str` and `quoted_name`, see [Schema reflection](/developer-guide/sqlalchemy/sqlalchemy-reflection).

### Schema names with case sensitivity

Use `quoted_name` for case-sensitive schema names. A plain lowercase string is converted to uppercase:

Copy code

```
from sqlalchemy import MetaData
from sqlalchemy.sql.elements import quoted_name

# CORRECT: preserves the schema case
metadata = MetaData(schema=quoted_name("myschema", True))

# WRONG: resolves to MYSCHEMA
metadata = MetaData(schema="myschema")
```

A quoted string such as `schema='"myschema"'` preserves case only when the engine is created with `case_sensitive_identifiers=True`. Without the flag, the quotes are stripped and Snowflake resolves the name to `MYSCHEMA`. No error is raised, so if a schema named `MYSCHEMA` exists, queries run silently against the wrong schema.

### Uppercase identifiers that are reserved words

An identifier whose stored form is all uppercase and also a SQL reserved word (for example, a table created as `CREATE TABLE "TABLE" ...`) reflects as the uppercase string `"TABLE"` by default, which doesn’t match the key SQLAlchemy uses for the same name in DDL. To get the standard SQLAlchemy convention, `quoted_name("table", True)`, create the engine with `case_sensitive_identifiers=True`:

Copy code

```
from sqlalchemy import create_engine

engine = create_engine(
    "snowflake://<user_login_name>:<password>@<account_identifier>/<database_name>",
    case_sensitive_identifiers=True,
)
```

Enabling the flag on an existing application changes the lookup keys for these names, so code that accesses `metadata.tables["TABLE"]` by the uppercase key no longer finds the table. Audit string-keyed lookups before enabling it.

### Lowercase column names in CLUSTER BY

To cluster by a case-sensitive lowercase column, pass the column name to `snowflake_clusterby` as `quoted_name(..., True)`. A plain string is treated as case-insensitive and resolves to the uppercase name:

Copy code

```
from sqlalchemy import Column, Integer, MetaData, Table
from sqlalchemy.sql.elements import quoted_name

t = Table(
    "my_table",
    MetaData(),
    Column(quoted_name("mycol", True), Integer),
    snowflake_clusterby=[quoted_name("mycol", True)],
)
# Generates: CLUSTER BY ("mycol")
```

### Alembic and case-sensitive names

Alembic needs extra configuration for case-sensitive schemas and columns: a `version_table_schema` given as `quoted_name`, and the opt-in `snowflake_render_item` hook for autogenerate. The hook must be registered in each project’s `env.py`, because Alembic has no dialect-level rendering hook. For details, see [Using Alembic with Snowflake SQLAlchemy](/developer-guide/sqlalchemy/sqlalchemy-alembic#label-case-sensitive-schema-configuration).

## Best practices

- Always use `quoted_name()` for case-sensitive identifiers.
- Use `Sequence()` instead of `Identity()` for ORM-managed primary keys.
- Keep DDL out of units of work that you might need to roll back.
- Test schema reflection and autogenerated migrations in a development environment before applying them to production.
- Use consistent identifier conventions throughout your application, either all unquoted or all quoted.
