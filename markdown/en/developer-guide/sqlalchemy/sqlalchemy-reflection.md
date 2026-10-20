# Schema reflection in SQLAlchemy

## Auto-increment behavior

Snowflake SQLAlchemy supports two ways to generate primary key values automatically:

- **`AUTOINCREMENT` columns.** The dialect renders a column as `AUTOINCREMENT` when it’s the table’s autoincrement column and has no other server default. SQLAlchemy’s standard `autoincrement=True` controls this.
- **`Sequence` objects.** SQLAlchemy fetches the next value with a separate `SELECT <sequence>.nextval` before the `INSERT`. This is the recommended approach for ORM primary keys, because the generated value is available to the ORM after the insert.

For why `Identity()` doesn’t work as an ORM primary key, see [Known limitations: Identity columns as primary keys](/developer-guide/sqlalchemy/sqlalchemy-limitations#label-identity-columns-as-primary-keys).

Copy code

```
from sqlalchemy import Column, Integer, MetaData, Sequence, String, Table, create_engine

engine = create_engine('snowflake://...')
metadata = MetaData()

# Rendered as: id INTEGER NOT NULL AUTOINCREMENT
my_table = Table(
    'my_table',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
)

# Uses the id_seq sequence
seq_table = Table(
    'seq_table',
    metadata,
    Column('id', Integer, Sequence('id_seq'), primary_key=True),
    Column('name', String),
)

metadata.create_all(engine)
```

## Object name case handling

Snowflake stores case-insensitive object names in uppercase. SQLAlchemy treats lowercase names as case-insensitive. Snowflake SQLAlchemy converts between the two during reflection and DDL, so use lowercase names on the SQLAlchemy side:

- Lowercase names are case-insensitive (for example, `my_table` refers to `MY_TABLE`).
- Uppercase and mixed-case names are treated as case-sensitive and are quoted. Use them only for identifiers that were created with quotes, such as `"MixedCase"`.

Copy code

```
from sqlalchemy import Column, Integer, MetaData, Table
from sqlalchemy.sql.elements import quoted_name

metadata = MetaData()

# Case-insensitive: refers to MY_TABLE
Table('my_table', metadata, Column('id', Integer))

# Case-sensitive: refers to "MixedCase"
Table(quoted_name('MixedCase', True), metadata, Column('id', Integer))
```

By default, a reflected mixed-case name such as `"MixedCase"` is returned as a plain `str`. If your code needs to distinguish case-sensitive names by type, set `case_sensitive_identifiers=True`. Reflected case-sensitive names are then returned as `quoted_name(..., True)`:

Copy code

```
from sqlalchemy import create_engine

engine = create_engine('snowflake://...', case_sensitive_identifiers=True)
```

## Index support

Indexes are supported only for [Hybrid Tables](/user-guide/tables-hybrid). Creating an index on a standard table raises an error.

### Single-column indexes

Create a single-column index by setting `index=True` on the column, or by defining an `Index` object:

Copy code

```
from snowflake.sqlalchemy import HybridTable
from sqlalchemy import Column, Integer, MetaData, String

metadata = MetaData()

my_table = HybridTable(
    'my_table',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), index=True),
)
```

### Multi-column indexes

Create a multi-column (composite) index by passing several columns to `Index`:

Copy code

```
from snowflake.sqlalchemy import HybridTable
from sqlalchemy import Column, Index, Integer, MetaData, String

metadata = MetaData()

my_table = HybridTable(
    'my_table',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name', String(50)),
    Column('last_name', String(50)),
    Index('idx_full_name', 'first_name', 'last_name'),
)
```

Snowflake builds only one index on a table at a time. If a table defines more than one index, `metadata.create_all()` can fail with `Another index is being built on table`. In that case, create the additional indexes after the first index is built.

## Inspector methods

In addition to columns and constraints, the inspector supports the following methods:

- `get_table_names()`, `get_view_names()`, `get_temp_table_names()`, `get_sequence_names()`, `get_schema_names()`
- `get_view_definition()`
- `get_table_comment()`
- `get_indexes()` and `get_multi_indexes()`, which return indexes for Hybrid Tables.
- `get_check_constraints()`, which returns an empty list because Snowflake doesn’t support check constraints

Copy code

```
from sqlalchemy import inspect

inspector = inspect(engine)
print(inspector.get_table_comment('my_table'))   # {'text': '...'}
print(inspector.get_view_definition('my_view'))
print(inspector.get_sequence_names())
print(inspector.get_indexes('my_hybrid_table'))
```

Reflected types include Snowflake’s resolved default sizes, such as `VARCHAR(16777216)` instead of `VARCHAR`. The type objects work the same way, but their `str()` output differs, so use `isinstance()` rather than string comparison:

Copy code

```
from sqlalchemy import String

name_type = next(c['type'] for c in inspector.get_columns('my_table') if c['name'] == 'name')
print(str(name_type))                # VARCHAR(16777216)
print(isinstance(name_type, String)) # True
```

The dialect’s reflection methods use SQLAlchemy’s `@reflection.cache` mechanism, so repeated calls with the same arguments on one `Inspector` object can reuse earlier results.

## Cache column metadata

Column metadata is cached during reflection for performance. The caching behavior differs between single-table and multi-table reflection:

- **Bulk reflection** (`MetaData.reflect()`): One schema-wide query per metadata type, cached for all tables
- **Single-table inspection** (`inspector.get_columns()`): One `DESC TABLE` query per table

### Single-table vs multi-table reflection performance

For best performance, choose the appropriate reflection method:

Copy code

```
from sqlalchemy import inspect, MetaData, create_engine

engine = create_engine('snowflake://...')

# Bulk reflection: efficient for many tables
metadata = MetaData()
metadata.reflect(bind=engine, schema='public')

# Single-table inspection: efficient for one table
inspector = inspect(engine)
columns = inspector.get_columns('my_table', schema='public')
```

Snowflake SQLAlchemy automatically routes each to the appropriate query path:

- `MetaData.reflect()` and `autoload_with=` use bulk schema queries
- `inspector.get_columns()` uses single `DESC TABLE` queries

## Cross-database reflection

Reflect tables from multiple databases by specifying the schema parameter:

Copy code

```
from sqlalchemy import MetaData, create_engine

engine = create_engine('snowflake://user:password@account/db1/')

metadata = MetaData()

# Reflect from a different database
metadata.reflect(bind=engine, schema='db2.public')

# or when inspecting
from sqlalchemy import inspect
inspector = inspect(engine)
columns = inspector.get_columns('my_table', schema='db2.public')
```

## Reflecting large schemas (10,000+ objects)

Snowflake `SHOW` commands return at most 10,000 rows per call. Snowflake SQLAlchemy automatically pages through the object-listing commands, so the following methods work regardless of the number of objects, and so do `MetaData.reflect()` and `autoload_with=`, which call them:

- `get_table_names()` (`SHOW TABLES`)
- `get_view_names()` (`SHOW VIEWS`)
- `get_sequence_names()` (`SHOW SEQUENCES`)
- `get_schema_names()` (`SHOW SCHEMAS`)
- `get_temp_table_names()`

The schema-wide constraint and index commands aren’t paged. When you use bulk reflection (`MetaData.reflect()`) on a schema with more than 10,000 rows for any of them, the following commands can fail:

- `SHOW PRIMARY KEYS IN SCHEMA`
- `SHOW UNIQUE KEYS IN SCHEMA`
- `SHOW IMPORTED KEYS IN SCHEMA`
- `SHOW INDEXES IN SCHEMA`

Reflecting a single table’s keys and indexes isn’t affected, because it uses the bounded `SHOW ... IN TABLE` form. For very large schemas, limit reflection to the tables you need:

Copy code

```
from sqlalchemy import MetaData, Table, create_engine, inspect

engine = create_engine('snowflake://...')

# Reflect only specific tables
metadata = MetaData()
metadata.reflect(bind=engine, schema='public', only=['orders', 'customers'])

# Or reflect a single table
orders = Table('orders', MetaData(), autoload_with=engine, schema='public')

# Or inspect a single table
inspector = inspect(engine)
columns = inspector.get_columns('orders', schema='public')
pk = inspector.get_pk_constraint('orders', schema='public')
```

When you reflect a subset of tables, also consider `resolve_fks=False`. By default, SQLAlchemy also reflects every table referenced by a foreign key, which can pull in tables outside your `only` list.
