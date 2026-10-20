# DDL features in SQLAlchemy

Snowflake SQLAlchemy extends SQLAlchemy’s DDL support with Snowflake table types and table options. The examples on this page assume
an `engine` created as described in [Connecting to Snowflake with SQLAlchemy](/developer-guide/sqlalchemy/sqlalchemy-connect).

## Snowflake table classes and options

Import these table classes from `snowflake.sqlalchemy`. Each one is a subclass of SQLAlchemy’s `Table`, so you can use it in SQLAlchemy Core
directly, or in a declarative ORM model by returning it from `__table_cls__`.

| Class | Statement generated | Options |
| --- | --- | --- |
| `SnowflakeTable` | `CREATE TABLE` | `cluster_by`, `row_access_policy`, `as_query` |
| `HybridTable` | `CREATE HYBRID TABLE` | Requires a primary key. Supports `Index`. |
| `IcebergTable` | `CREATE ICEBERG TABLE` | `external_volume`, `base_location`, `as_query` |
| `DynamicTable` | `CREATE DYNAMIC TABLE` | `target_lag`, `warehouse`, `refresh_mode`, `as_query` |

Expand

Show lessSee more

You can pass option values as plain Python values, or as explicit option objects: `AsQueryOption`, `ClusterByOption`, `IdentifierOption`,
`KeywordOption`, `LiteralOption`, `RowAccessPolicyOption`, and `TargetLagOption`. Use the `TimeUnit` and `SnowflakeKeyword` enumerations
for time units and keywords such as `DOWNSTREAM` or `FULL`.

Note

Don’t pass Snowflake table options as `snowflake_*` keyword arguments on a plain `Table`. The only such argument that the dialect accepts is
`snowflake_clusterby`. Other `snowflake_*` table arguments raise an error when the `CREATE TABLE` statement is compiled.

### Creating a table from a query

Pass a `select()` construct (or a SQL string) as `as_query` to generate `CREATE TABLE ... AS SELECT`. When you use `select()`, you don’t
need to define the columns:

Copy code

```
from sqlalchemy import MetaData, Table, select
from snowflake.sqlalchemy import SnowflakeTable

metadata = MetaData()
orders = Table('orders', metadata, autoload_with=engine)

SnowflakeTable(
    'orders_copy',
    metadata,
    as_query=select(orders.c.id, orders.c.customer_id),
)
metadata.create_all(engine)
```

## CLUSTER BY support

Snowflake SQLAlchemy supports the `CLUSTER BY` clause for organizing table data. For a SQLAlchemy Core `Table`, use the `snowflake_clusterby`
argument. It accepts column names and `text()` expressions:

Copy code

```
from sqlalchemy import Column, Date, Integer, MetaData, String, Table

metadata = MetaData()

my_table = Table(
    'my_table',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('region', String),
    Column('order_date', Date),
    snowflake_clusterby=['region', 'order_date'],
)

metadata.create_all(engine)
```

`CLUSTER BY` doesn’t change query semantics. You query a clustered table the same way as any other table.

### Using CLUSTER BY with ORM (declarative)

For declarative models, return a `SnowflakeTable` from `__table_cls__` and pass `cluster_by` in `__table_args__`:

Copy code

```
from sqlalchemy import Column, DateTime, Integer, String, text
from sqlalchemy.orm import declarative_base
from snowflake.sqlalchemy import SnowflakeTable

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'

    @classmethod
    def __table_cls__(cls, name, metadata, *arg, **kw):
        return SnowflakeTable(name, metadata, *arg, **kw)

    __table_args__ = {
        'cluster_by': ['region', text("date_trunc('day', created_at)")],
    }

    id = Column(Integer, primary_key=True)
    region = Column(String)
    created_at = Column(DateTime)
```

### Lowercase column names in CLUSTER BY

To cluster by a case-sensitive (lowercase) column, wrap the name in `quoted_name(..., True)` both in the column definition and in the
clustering key. Otherwise, Snowflake resolves the name as uppercase:

Copy code

```
from sqlalchemy import Column, Integer, MetaData, Table
from sqlalchemy.sql.elements import quoted_name

t = Table(
    'my_table',
    MetaData(),
    Column(quoted_name('mycol', True), Integer),
    snowflake_clusterby=[quoted_name('mycol', True)],
)
# Generates: CLUSTER BY ("mycol")
```

## Row access policy support

Snowflake SQLAlchemy can attach an existing [row access policy](/user-guide/security-row-intro) to a table when it creates the table. Use
`SnowflakeTable` and pass `row_access_policy` as a `(policy_name, [columns])` tuple:

Copy code

```
from sqlalchemy import Column, Integer, MetaData, String
from snowflake.sqlalchemy import SnowflakeTable

metadata = MetaData()

SnowflakeTable(
    'sales',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('region', String),
    row_access_policy=('my_policy', ['region']),
)
metadata.create_all(engine)
# CREATE TABLE sales (...) WITH ROW ACCESS POLICY my_policy ON (region)
```

The policy must already exist in Snowflake. Snowflake SQLAlchemy doesn’t create it.

The policy name can be fully qualified. A string is parsed as `[[database.]schema.]name`. You can also pass a `RowAccessPolicyOption`
with an explicit `FQN`:

Copy code

```
from snowflake.sqlalchemy import FQN, RowAccessPolicyOption

row_access_policy = RowAccessPolicyOption(
    FQN.from_string('gov_db.security.my_policy'), ['region']
)
```

## RELY constraint property

Snowflake doesn’t enforce `PRIMARY KEY`, `UNIQUE`, or `FOREIGN KEY` constraints. The `RELY` property tells the query optimizer that it can
trust a constraint when it rewrites queries. Set `snowflake_rely=True` on each constraint that should have the property:

Copy code

```
from sqlalchemy import (
    Column, ForeignKeyConstraint, Integer, MetaData,
    PrimaryKeyConstraint, String, Table, UniqueConstraint,
)

metadata = MetaData()

customers = Table(
    'customers', metadata,
    Column('id', Integer),
    Column('email', String),
    PrimaryKeyConstraint('id', snowflake_rely=True),
    UniqueConstraint('email', snowflake_rely=True),
)
# ... PRIMARY KEY (id) RELY ... UNIQUE (email) RELY

orders = Table(
    'orders', metadata,
    Column('id', Integer, primary_key=True),
    Column('customer_id', Integer),
    ForeignKeyConstraint(['customer_id'], ['customers.id'], snowflake_rely=True),
)
# ... FOREIGN KEY(customer_id) REFERENCES customers (id) RELY
```

Caution

Snowflake doesn’t verify `RELY` constraints against the data. If the data violates a `RELY` constraint (for example, it contains duplicate
keys or orphaned foreign keys), queries can return incorrect results. Only set `RELY` on constraints that your data loading process
guarantees.

## Auto-incrementing primary keys

By default, an `Integer` primary key column renders as `AUTOINCREMENT`. To generate primary key values for ORM models, use a `Sequence`.
The ORM fetches the next value from the sequence before each insert, so the new object’s primary key is populated:

Copy code

```
from sqlalchemy import Column, Integer, Sequence, String
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    name = Column(String)

Base.metadata.create_all(engine)

with Session(engine) as session:
    item = Item(name='widget')
    session.add(item)
    session.commit()
    print(item.id)
```

Don’t use `Identity()` on a primary key column with the ORM. For details, see
[Identity columns as primary keys](/developer-guide/sqlalchemy/sqlalchemy-limitations#label-identity-columns-as-primary-keys).

## Iceberg table with Snowflake catalog support

Snowflake SQLAlchemy supports creating [Apache Iceberg™ tables](/user-guide/tables-iceberg) that use Snowflake as the catalog. Use
`IcebergTable` with an existing external volume:

Copy code

```
from sqlalchemy import Column, Integer, MetaData, String
from snowflake.sqlalchemy import IcebergTable

metadata = MetaData()

IcebergTable(
    'my_iceberg_table',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    external_volume='my_external_volume',
    base_location='my_iceberg_table',
)
metadata.create_all(engine)
```

Snowflake SQLAlchemy doesn’t validate the options on the client. Snowflake reports an error when the statement runs if, for example, the
external volume doesn’t exist. You can also pass `as_query` to create the table from a query.

For declarative models, return an `IcebergTable` from `__table_cls__`:

Copy code

```
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from snowflake.sqlalchemy import IcebergTable

Base = declarative_base()

class MyUser(Base):
    __tablename__ = 'my_iceberg_table'

    @classmethod
    def __table_cls__(cls, name, metadata, *arg, **kw):
        return IcebergTable(name, metadata, *arg, **kw)

    __table_args__ = {
        'external_volume': 'my_external_volume',
        'base_location': 'my_iceberg_table',
    }

    id = Column(Integer, primary_key=True)
    name = Column(String)
```

The `MAP`, `OBJECT`, and `ARRAY` structured types are intended for Iceberg tables. See
[Structured data types](/developer-guide/sqlalchemy/sqlalchemy-data-types#label-structured-data-types-support).

## Hybrid table support

Use `HybridTable` to create a [hybrid table](/user-guide/tables-hybrid). A hybrid table requires a primary key, and it’s the only table
type that supports indexes. Snowflake SQLAlchemy creates each `Index` with a separate `CREATE INDEX` statement after it creates the table:

Copy code

```
from sqlalchemy import Column, Index, Integer, MetaData, String
from snowflake.sqlalchemy import HybridTable

metadata = MetaData()

HybridTable(
    'my_hybrid_table',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Index('idx_name', 'name'),
)
metadata.create_all(engine)
```

For declarative models, return a `HybridTable` from `__table_cls__`:

Copy code

```
from sqlalchemy import Column, Index, Integer, String
from sqlalchemy.orm import declarative_base
from snowflake.sqlalchemy import HybridTable

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'

    @classmethod
    def __table_cls__(cls, name, metadata, *arg, **kw):
        return HybridTable(name, metadata, *arg, **kw)

    __table_args__ = (Index('idx_account_name', 'name'),)

    id = Column(Integer, primary_key=True)
    name = Column(String)
```

## Dynamic tables support

Use `DynamicTable` to create a [dynamic table](/user-guide/dynamic-tables/overview) with SQLAlchemy Core. Specify the target lag as a
`(value, TimeUnit)` tuple or as `SnowflakeKeyword.DOWNSTREAM`, and specify the warehouse that refreshes the table:

Copy code

```
from sqlalchemy import Column, Date, Integer, MetaData, Table
from snowflake.sqlalchemy import DynamicTable, SnowflakeKeyword, TimeUnit

metadata = MetaData()

orders = Table(
    'orders',
    metadata,
    Column('id', Integer),
    Column('order_date', Date),
    Column('amount', Integer),
)

DynamicTable(
    'order_summary',
    metadata,
    Column('order_date', Date),
    Column('total', Integer),
    target_lag=(1, TimeUnit.HOURS),
    warehouse='my_wh',
    refresh_mode=SnowflakeKeyword.FULL,
    as_query='SELECT order_date, SUM(amount) AS total FROM orders GROUP BY order_date',
)

metadata.create_all(engine)
```

When `as_query` is a `select()` construct, you don’t need to define the columns:

Copy code

```
from sqlalchemy import select

DynamicTable(
    'order_amounts',
    metadata,
    target_lag=SnowflakeKeyword.DOWNSTREAM,
    warehouse='my_wh',
    as_query=select(orders.c.id, orders.c.amount),
)
```

Dynamic tables have these limitations in Snowflake SQLAlchemy:

- When `as_query` is a string, you must define the columns explicitly.
- A dynamic table can’t have a primary key or foreign key. Defining one raises an error. Because declarative ORM models require a primary
  key, you can’t define a dynamic table with the declarative ORM.
- You can’t insert data directly into a dynamic table.

## Stages and file formats

Use `CreateStage` to create an external stage that points to a cloud storage location. Describe the stage with `ExternalStage`, and the
location with `AWSBucket`, `AzureContainer`, or `GCSBucket`:

Copy code

```
from snowflake.sqlalchemy import AWSBucket, CreateStage, ExternalStage

stage = ExternalStage(name='my_stage', namespace='my_db.my_schema')
create_stage = CreateStage(
    container=AWSBucket.from_uri('s3://my-bucket/data'),
    stage=stage,
    replace_if_exists=True,
)

with engine.begin() as connection:
    connection.execute(create_stage)
# CREATE OR REPLACE STAGE my_db.my_schema.my_stage URL='s3://my-bucket/data'
```

To create a named file format, use `CreateFileFormat`. For an example, see
[Creating a named file format](/developer-guide/sqlalchemy/sqlalchemy-dml#label-sqlalchemy-dml-create-file-format).

## Notes

- Always test DDL features in a development environment before deploying to production.
- Some DDL features require specific Snowflake editions or privileges.
- For details about the SQL statements, see [CREATE TABLE](/sql-reference/sql/create-table) and the other linked reference pages.
