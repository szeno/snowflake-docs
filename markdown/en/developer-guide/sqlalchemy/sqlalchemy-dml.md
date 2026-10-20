# DML and bulk operations in SQLAlchemy

Snowflake SQLAlchemy provides custom constructs for Snowflake DML statements and for loading and unloading data. The examples on this page
assume an `engine` created as described in [Connecting to Snowflake with SQLAlchemy](/developer-guide/sqlalchemy/sqlalchemy-connect).

## Merge command support

Use the `MergeInto` construct to run a [MERGE](/sql-reference/sql/merge) statement, which inserts, updates, and deletes rows in a single
statement. Add clauses with `when_matched_then_update()`, `when_matched_then_delete()`, and `when_not_matched_then_insert()`. Each clause
accepts an optional `.where()` condition, and the update and insert clauses take `.values()`:

Copy code

```
from sqlalchemy import Boolean, Column, Integer, MetaData, String, Table, true
from snowflake.sqlalchemy import MergeInto

metadata = MetaData()
users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String),
)
user_updates = Table(
    'user_updates', metadata,
    Column('id', Integer),
    Column('name', String),
    Column('email', String),
    Column('deleted', Boolean),
)

merge = MergeInto(target=users, source=user_updates, on=users.c.id == user_updates.c.id)
merge.when_matched_then_delete().where(user_updates.c.deleted == true())
merge.when_matched_then_update().values(name=user_updates.c.name, email=user_updates.c.email)
merge.when_not_matched_then_insert().values(
    id=user_updates.c.id, name=user_updates.c.name, email=user_updates.c.email
)

with engine.begin() as connection:
    connection.execute(merge)
```

### Merging from a VALUES list

The `source` can be any SQLAlchemy selectable. To merge from inline values without a staging table, wrap a `values()` construct in a
subquery:

Copy code

```
from sqlalchemy import Integer, String, column, select, values

src = select(
    values(
        column('id', Integer),
        column('name', String),
        name='src',
    ).data([(1, 'Alice'), (4, 'Dana')])
).subquery()

merge = MergeInto(target=users, source=src, on=users.c.id == src.c.id)
merge.when_matched_then_update().values(name=src.c.name)
merge.when_not_matched_then_insert().values(id=src.c.id, name=src.c.name)

with engine.begin() as connection:
    connection.execute(merge)
```

## Multi-table insert (INSERT ALL / INSERT FIRST)

Use the `InsertMulti` construct to run a [multi-table INSERT](/sql-reference/sql/insert-multi-table) statement. Build it from a source
`select()` and add targets.

For an unconditional `INSERT ALL`, add each target with `.into()`. Optionally, pass `columns` to name the target columns and `values` to map
source columns or expressions. When you omit `values`, the source columns are used in order:

Copy code

```
from sqlalchemy import select
from snowflake.sqlalchemy import InsertMulti

stmt = (
    InsertMulti(select(sales))
    .into(sales_archive)
    .into(sales_backup, columns=['id', 'amount'])
)

with engine.begin() as connection:
    connection.execute(stmt)
# INSERT ALL INTO sales_archive INTO sales_backup (id, amount) SELECT ... FROM sales
```

For a conditional insert, add targets with `.when(condition, table)` and an optional `.else_(table)`. Pass `first=True` to generate
`INSERT FIRST`, which inserts each row into the first matching target only:

Copy code

```
src = select(sales.c.id, sales.c.amount)

stmt = (
    InsertMulti(src, first=True)
    .when(src.selected_columns.amount > 1000, large_sales)
    .else_(small_sales)
)

with engine.begin() as connection:
    connection.execute(stmt)
# INSERT FIRST WHEN amount > 1000 THEN INTO large_sales ELSE INTO small_sales SELECT ...
```

Pass `overwrite=True` to generate `INSERT OVERWRITE`, which truncates the target tables before inserting.

## Bulk insert optimization for ORM models

When you call `Session.bulk_save_objects()` with models that have nullable columns, SQLAlchemy groups objects by which columns are set. Objects
that leave different nullable columns unset end up in separate `INSERT` statements instead of a single batch.

To send one batched `INSERT`, use these two components together:

- `SnowflakeBase`: A declarative base class that sets every nullable column without a default to `None`, or to its scalar Python default,
  when you create an object. Subclass it directly. If your code must also run on SQLAlchemy 1.4, use the `snowflake_declarative_base()` factory
  instead.
- `SnowflakeSession`: A session class whose `bulk_save_objects()` keeps those `None` values, so all objects share the same set of columns.

Copy code

```
from sqlalchemy import Column, Integer, String
from snowflake.sqlalchemy import SnowflakeBase, SnowflakeSession

class User(SnowflakeBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)                       # nullable, no default
    status = Column(String, default='active')   # scalar default

SnowflakeBase.metadata.create_all(engine)

session = SnowflakeSession(bind=engine)
session.bulk_save_objects([
    User(id=1),
    User(id=2, name='Bob'),
    User(id=3, status='inactive'),
])
session.commit()
session.close()
```

The optimization applies only to `bulk_save_objects()`. Columns with a `server_default`, a callable default, or a SQL expression default
aren’t pre-populated, so objects that differ on those columns can still be split into separate batches.

## Bulk array binding for large executemany inserts

For large batch inserts, such as `connection.execute(insert(table), rows)` or `session.bulk_insert_mappings()`, the Snowflake Connector for
Python can upload the bind values to a temporary stage and insert them from there. This bulk array binding is much faster than sending
the values inline.

The connector only uses array binding with the `qmark` (or `numeric`) parameter style. Snowflake SQLAlchemy defaults to `pyformat`, so set
`paramstyle='qmark'` on both the engine and the connector connection. If only one side is set, the placeholders and bind values don’t match
and the statement fails:

Copy code

```
from sqlalchemy import create_engine, insert

engine = create_engine(
    'snowflake://<account_identifier>/<database>/<schema>',
    paramstyle='qmark',                # How SQLAlchemy renders placeholders
    connect_args={
        'paramstyle': 'qmark',         # How the connector binds parameters
        'CLIENT_STAGE_ARRAY_BINDING_THRESHOLD': 65536,  # Optional
    },
)

rows = [{'id': i, 'name': f'user_{i}'} for i in range(20000)]

with engine.begin() as connection:
    connection.execute(insert(users_table), rows)
```

The optional `CLIENT_STAGE_ARRAY_BINDING_THRESHOLD` session parameter sets the total bind size, in bytes, above which the connector uses a
stage. A value of `0` disables array binding. Below the threshold, the connector sends the values inline. Either way, your code doesn’t
change. The `qmark` setting applies to every statement that the engine compiles.

## Writing pandas DataFrames

To write a pandas DataFrame to Snowflake through a SQLAlchemy engine, pass the connector’s `pd_writer` function as the `method` argument to
`DataFrame.to_sql()`. `pd_writer` uploads the data to a stage and loads it with `COPY INTO`:

Copy code

```
import pandas as pd
from snowflake.connector.pandas_tools import pd_writer

df = pd.DataFrame({'ID': [1, 2], 'NAME': ['Alice', 'Bob']})
df.to_sql('pd_users', engine, index=False, method=pd_writer)
```

For more information, including `write_pandas`, see [Using pandas DataFrames with the Python Connector](/developer-guide/python-connector/python-connector-pandas).

## CopyIntoStorage support

Use the `CopyIntoStorage` construct to unload a table or query result to a stage or cloud storage location with
[COPY INTO <location>](/sql-reference/sql/copy-into-location). It takes these arguments:

- `from_`: A table or `select()` construct.
- `into`: An `ExternalStage` (a named internal or external stage), `AWSBucket`, `AzureContainer`, or `GCSBucket`.
- `formatter`: Optional. A `CSVFormatter`, `JSONFormatter`, or `PARQUETFormatter`, configured with chained methods such as `.null_if()` or
  `.field_delimiter()`.
- `partition_by`: Optional. An expression for the `PARTITION BY` clause.

This example unloads a table to a single CSV file on a named stage:

Copy code

```
from snowflake.sqlalchemy import CopyIntoStorage, CSVFormatter, ExternalStage

copy_into = CopyIntoStorage(
    from_=users,
    into=ExternalStage(name='my_stage', path='exports/users.csv'),
    formatter=CSVFormatter().null_if(['NULL']),
)
copy_into.single(True).maxfilesize(10_000_000)

with engine.begin() as connection:
    connection.execute(copy_into)
# COPY INTO @my_stage/exports/users.csv FROM users FILE_FORMAT=(TYPE=csv NULL_IF=('NULL')) SINGLE = true MAX_FILE_SIZE = 10000000
```

To unload directly to cloud storage, create the location with `from_uri()`. Use a [storage integration](/sql-reference/sql/create-storage-integration)
when you can, so that no credentials appear in the SQL:

Copy code

```
from sqlalchemy import select, text
from snowflake.sqlalchemy import AWSBucket, PARQUETFormatter

copy_into = CopyIntoStorage(
    from_=select(users.c.id, users.c.name),
    into=AWSBucket.from_uri('s3://my-bucket/exports'),
    formatter=PARQUETFormatter(),
    partition_by=text("'part_' || id"),
)
copy_into.storage_integration('my_s3_integration')
```

The options available on a `CopyIntoStorage` object are `.single()`, `.maxfilesize()`, `.files()`, `.pattern()`, and `.storage_integration()`.
For inline credentials and encryption, the location classes provide these methods:

- `AWSBucket`: `.credentials(aws_role=...)` or `.credentials(aws_key_id=..., aws_secret_key=..., aws_token=...)`, `.encryption_aws_cse()`,
  `.encryption_aws_sse_s3()`, and `.encryption_aws_sse_kms()`.
- `AzureContainer`: `.credentials(azure_sas_token)` and `.encryption_azure_cse()`.
- `GCSBucket`: `.encryption_gcs_sse_kms()` and `.encryption_none()`. Google Cloud Storage requires a storage integration.

### Securing cloud credentials in logs

Inline credentials (from `.credentials()` or a client-side encryption master key) appear as literal values in the compiled SQL. If you
enable SQLAlchemy engine logging, for example with `create_engine(..., echo=True)`, the full statement, including the secrets, is written to
the log. The connector’s secret masking doesn’t apply to SQLAlchemy’s logger.

To mask secrets in log output, pass the handler that writes the records to `add_secret_redaction_filter()`. Attach the filter to a handler,
not a logger, because logger filters don’t run on records propagated from child loggers:

Copy code

```
import logging
from snowflake.sqlalchemy import add_secret_redaction_filter

handler = logging.StreamHandler()
add_secret_redaction_filter(handler)
logging.getLogger('sqlalchemy.engine').addHandler(handler)
```

To redact a statement string yourself, call `redact_secrets(text)`. The `repr()` of the location classes (`AWSBucket`, `AzureContainer`,
`GCSBucket`) already masks secrets.

### Creating a named file format

To reuse file format settings, create a named file format with `CreateFileFormat` and a formatter. It accepts these arguments:

- `format_name`: The name of the file format, optionally qualified.
- `formatter`: A `CSVFormatter`, `JSONFormatter`, or `PARQUETFormatter`.
- `replace_if_exists`: Generates `CREATE OR REPLACE`.
- `if_not_exists`: Generates `IF NOT EXISTS`. You can’t combine it with `replace_if_exists`. Setting both raises a `ValueError`.
- `comment`: Optional comment.

Copy code

```
from snowflake.sqlalchemy import CreateFileFormat, CSVFormatter

create_format = CreateFileFormat(
    format_name='my_csv_format',
    formatter=CSVFormatter().field_delimiter(','),
    if_not_exists=True,
    comment='CSV format for exports',
)

with engine.begin() as connection:
    connection.execute(create_format)
# CREATE FILE FORMAT IF NOT EXISTS my_csv_format TYPE='csv' FIELD_DELIMITER = ',' COMMENT = 'CSV format for exports'
```

To use the named file format with `CopyIntoStorage`, pass its name to the formatter:

Copy code

```
copy_into = CopyIntoStorage(
    from_=users,
    into=ExternalStage(name='my_stage', path='exports'),
    formatter=CSVFormatter(format_name='my_csv_format'),
)
```

In a SQL `COPY INTO` statement, reference the named file format with `FORMAT_NAME`:

Copy code

```
COPY INTO @my_stage/exports/
  FROM users
  FILE_FORMAT = (FORMAT_NAME = 'my_csv_format');
```

To create the stage itself, see [Stages and file formats](/developer-guide/sqlalchemy/sqlalchemy-ddl#label-sqlalchemy-ddl-stages-file-formats).
