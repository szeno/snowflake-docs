# Data type support in SQLAlchemy

## Snowflake types and their SQLAlchemy equivalents

Snowflake-specific types are importable from `snowflake.sqlalchemy`. When Snowflake SQLAlchemy reflects a column, it maps the Snowflake type name to a SQLAlchemy type as follows:

| Snowflake type names | SQLAlchemy type |
| --- | --- |
| `NUMBER`, `DECIMAL`, `DEC`, `FIXED` | `DECIMAL` (`NUMBER` with precision and scale) |
| `INT`, `INTEGER`, `BIGINT`, `SMALLINT`, `TINYINT`, `BYTEINT` | `INTEGER`, `BIGINT`, `SMALLINT` |
| `FLOAT`, `DOUBLE`, `REAL` | `FLOAT`, `DOUBLE`, `REAL` |
| `DECFLOAT` | `snowflake.sqlalchemy.DECFLOAT` |
| `VARCHAR`, `STRING`, `TEXT`, `CHAR`, `CHARACTER` | `VARCHAR`, `CHAR` |
| `BINARY`, `VARBINARY` | `BINARY` |
| `BOOLEAN` | `BOOLEAN` |
| `DATE`, `TIME`, `DATETIME`, `TIMESTAMP` | `DATE`, `TIME`, `DATETIME`, `TIMESTAMP` |
| `TIMESTAMP_TZ`, `TIMESTAMP_LTZ`, `TIMESTAMP_NTZ` | `snowflake.sqlalchemy.TIMESTAMP_TZ`, `TIMESTAMP_LTZ`, `TIMESTAMP_NTZ` |
| `VARIANT`, `OBJECT`, `ARRAY`, `MAP` | `snowflake.sqlalchemy.VARIANT`, `OBJECT`, `ARRAY`, `MAP` |
| `GEOGRAPHY`, `GEOMETRY` | `snowflake.sqlalchemy.GEOGRAPHY`, `GEOMETRY` |
| `VECTOR` | `snowflake.sqlalchemy.VECTOR` |
| `UUID` | `sqlalchemy.UUID` |

Expand

Show lessSee more

## Numpy data type support

Snowflake SQLAlchemy can bind the following NumPy types as parameter values:

- `numpy.int64`
- `numpy.float64`
- `numpy.datetime64`

To fetch timestamp values as `numpy.datetime64`, add `numpy=True` to the connection parameters:

Copy code

```
import numpy as np
from sqlalchemy import Column, DateTime, Integer, MetaData, Table, create_engine, select

engine = create_engine('snowflake://...', connect_args={'numpy': True})
metadata = MetaData()
events = Table(
    'events',
    metadata,
    Column('id', Integer),
    Column('ts', DateTime),
)
metadata.create_all(engine)

with engine.begin() as connection:
    connection.execute(events.insert().values(id=1, ts=np.datetime64('2023-01-01T12:00:00')))
    row = connection.execute(select(events.c.ts)).one()
    print(type(row.ts))  # <class 'numpy.datetime64'>
```

## DECFLOAT data type support

Snowflake SQLAlchemy supports the [DECFLOAT](/sql-reference/data-types-numeric#label-data-type-decfloat) data type, which provides decimal floating-point values with up to 38 significant digits. Use `snowflake.sqlalchemy.DECFLOAT`. The SQLAlchemy `Numeric` type creates a `NUMBER` column, not a `DECFLOAT` column.

Copy code

```
from snowflake.sqlalchemy import DECFLOAT
from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MyTable(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    amount = Column(DECFLOAT())  # DECFLOAT(38)
```

`DECFLOAT` has the following restrictions:

- The precision is fixed at 38 digits and can’t be customized.
- It isn’t supported in Iceberg tables or Hybrid Tables.
- It doesn’t support the special values `inf`, `-inf`, and `NaN`.

To store `DECFLOAT` values inside semi-structured data, see [Decimal and DECFLOAT values in semi-structured data](#label-sqlalchemy-decimal-in-variant).

### DECFLOAT precision

The Snowflake Connector for Python converts `DECFLOAT` values to Python `Decimal` objects using the current `decimal` context. The default context precision is 28 digits, so values with more digits are truncated. To preserve all 38 digits, set `enable_decfloat=True`:

Copy code

```
from sqlalchemy import create_engine

engine = create_engine('snowflake://...?enable_decfloat=True')
# or: create_engine('snowflake://...', enable_decfloat=True)
```

This option isn’t enabled by default because it sets `decimal.getcontext().prec = 38`, which changes the thread-local decimal context for all `Decimal` operations in that thread, not just database queries.

## Returning float instead of Decimal

By default, numeric columns are returned as Python `Decimal` objects to preserve precision. If you prefer floating-point numbers, you can convert them explicitly:

Copy code

```
row = connection.execute(select(my_table.c.amount)).fetchone()
amount_float = float(row[0])  # Convert Decimal to float
```

Alternatively, use the `cast()` function for type conversion in queries:

Copy code

```
from sqlalchemy import cast, Float, select

query = select(cast(my_table.c.amount, Float))
result = connection.execute(query).fetchone()
```

## VECTOR data type support

Snowflake SQLAlchemy supports the [VECTOR](/sql-reference/data-types-vector) data type for storing vector embeddings. `VECTOR(element_type, dimension)` requires both arguments:

- `element_type`: `Integer()` or `Float()`, or the string `'INT'` or `'FLOAT'`.
- `dimension`: The length of the vector, as a positive integer.

Copy code

```
from snowflake.sqlalchemy import VECTOR
from sqlalchemy import Column, Float, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class EmbeddingTable(Base):
    __tablename__ = 'embeddings'
    id = Column(Integer, primary_key=True)
    embedding = Column(VECTOR(Float(), 1536))  # VECTOR(FLOAT, 1536)
    counts = Column(VECTOR('INT', 3))          # VECTOR(INT, 3)
```

Vector values are returned as Python lists.

## UUID data type support

By default, SQLAlchemy’s generic `Uuid` type (and the ORM annotation `Mapped[uuid.UUID]`) creates a `CHAR(32)` column, not a native Snowflake `UUID` column. Use `as_uuid` to choose whether values are returned as strings or as `uuid.UUID` objects:

Copy code

```
from sqlalchemy import Column, Integer, Uuid
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MyTable(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    token = Column(Uuid(as_uuid=False))       # Returns strings
    request_id = Column(Uuid(as_uuid=True))   # Returns uuid.UUID objects (default)
```

### Native UUID columns

To create native `UUID` columns from `Uuid` and `Mapped[uuid.UUID]`, set `enable_native_uuid=True`. This option also allows `uuid.UUID` objects inside semi-structured payloads, where they’re serialized as JSON strings.

Copy code

```
from sqlalchemy import create_engine

engine = create_engine('snowflake://...?enable_native_uuid=true')
# or: create_engine('snowflake://...', enable_native_uuid=True)
```

This option isn’t enabled by default because it changes the DDL of existing `Uuid` columns from `CHAR(32)` to `UUID`, so tables created earlier no longer match their model definitions. The explicit `sqlalchemy.UUID` type always creates a native `UUID` column, regardless of this option.

With `enable_native_uuid=True`, `uuid.UUID` values are bound to `Uuid` columns as strings, and reads honor `as_uuid`: `True` returns `uuid.UUID` objects and `False` returns hyphenated strings. Reflected `UUID` columns have `as_uuid=False`.

## Timestamp and timezone support

SQLAlchemy’s `DateTime` type maps to Snowflake timestamp types as follows:

- `DateTime(timezone=False)` (the default) creates a `DATETIME` column, which is `TIMESTAMP_NTZ`.
- `DateTime(timezone=True)` creates a `TIMESTAMP_TZ` column.

To choose a Snowflake timestamp type directly, use `TIMESTAMP_TZ`, `TIMESTAMP_LTZ`, or `TIMESTAMP_NTZ`:

Copy code

```
from snowflake.sqlalchemy import TIMESTAMP_LTZ, TIMESTAMP_NTZ, TIMESTAMP_TZ
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MyTable(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=False))  # TIMESTAMP_NTZ
    updated_at = Column(DateTime(timezone=True))   # TIMESTAMP_TZ
    tz_col = Column(TIMESTAMP_TZ)
    ltz_col = Column(TIMESTAMP_LTZ)
    ntz_col = Column(TIMESTAMP_NTZ)
```

Insert timezone-aware `datetime` values into `TIMESTAMP_TZ` and `TIMESTAMP_LTZ` columns, and naive values into `TIMESTAMP_NTZ` columns:

Copy code

```
import datetime
from datetime import timezone

naive_dt = datetime.datetime(2023, 1, 1, 12, 0, 0)
aware_dt = datetime.datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
```

Snowflake’s `TIME` data type doesn’t support time zones, so `Time(timezone=True)` creates a plain `TIME` column.

## VARIANT, ARRAY and OBJECT support

Snowflake SQLAlchemy supports the semi-structured data types `VARIANT`, `ARRAY`, and `OBJECT`. When you use `ARRAY()` or `OBJECT()` without element or field types, the column is semi-structured. With types, the column is a [structured type](#label-structured-data-types-support).

Copy code

```
from snowflake.sqlalchemy import ARRAY, OBJECT, VARIANT
from sqlalchemy import Column, Integer, MetaData, Table

metadata = MetaData()
my_table = Table(
    'my_table',
    metadata,
    Column('id', Integer),
    Column('data', VARIANT),
    Column('ob', OBJECT),
    Column('ar', ARRAY),
)
```

### Automatic JSON handling with `enable_structured_type_json`

In Snowflake SQLAlchemy 2.x, `enable_structured_type_json` defaults to `True`. For semi-structured `VARIANT`, `OBJECT`, and `ARRAY` columns, and for [structured columns](#label-structured-data-types-support), this means:

- **Reads** return Python objects (`dict` or `list`) instead of JSON strings.
- **Writes** accept a `dict` or `list` directly. The dialect serializes the value and wraps it in `PARSE_JSON()`. Because Snowflake doesn’t allow functions in a `VALUES` clause, inserts are rendered as `INSERT ... SELECT`, and multi-row inserts as `SELECT ... UNION ALL SELECT ...`.

Copy code

```
from sqlalchemy import select

# Writes: pass the dict or list directly (no manual json.dumps needed)
connection.execute(my_table.insert().values(id=1, data={'key': 'value'}))

# Multi-row insert, rendered as SELECT ... UNION ALL
connection.execute(my_table.insert().values([
    {'id': 2, 'data': {'key': 'a'}},
    {'id': 3, 'data': {'key': 'b'}},
]))

# Reads: values are already dict or list
result = connection.execute(select(my_table.c.data)).fetchone()
print(type(result[0]))  # <class 'dict'>
```

The following limitations apply while this option is on:

- `executemany` isn’t supported for semi-structured columns. Passing a list of two or more parameter sets, such as `connection.execute(my_table.insert(), [row1, row2])`, or an ORM flush that batches several new objects, raises `252001: Failed to rewrite multi-row insert`. Use single-row inserts or the multi-row `insert().values([...])` form shown earlier.
- `RETURNING` isn’t supported for inserts into semi-structured columns.
- `literal_binds` isn’t supported for semi-structured writes. Execute statements with bound parameters instead.
- Statements are limited by Snowflake’s statement size limit. For large data volumes, stage the data and use [COPY INTO](/sql-reference/sql/copy-into-table) instead.

To restore the previous behavior, where reads return JSON strings and you write pre-serialized values, set `enable_structured_type_json=False`. This option is deprecated and emits a `DeprecationWarning`:

Copy code

```
from sqlalchemy import create_engine

engine = create_engine(
    'snowflake://...',
    enable_structured_type_json=False
)
```

### Subscript access

Python subscript syntax works on `VARIANT`, `OBJECT`, `ARRAY`, and `MAP` columns, in the `SELECT` list and in clauses such as `WHERE`:

Copy code

```
from sqlalchemy import Integer, select

# Extract a field from a VARIANT column
query = select(my_table.c.data['nested_key'])

# Filter on a field
query = select(my_table.c.id).where(my_table.c.ob['status'] == 'active')

# Cast an extracted value to a SQL type
query = select(my_table.c.ob['age'].cast(Integer))
```

Negative array indexes aren’t supported.

### Custom JSON serializer

To customize JSON serialization and deserialization, pass the standard SQLAlchemy `json_serializer` and `json_deserializer` arguments to `create_engine()`:

Copy code

```
import decimal
import json
from sqlalchemy import create_engine

engine = create_engine(
    'snowflake://...',
    json_serializer=lambda obj: json.dumps(obj, default=str),
    json_deserializer=lambda value: json.loads(value, parse_float=decimal.Decimal),
)
```

### Decimal and DECFLOAT values in semi-structured data

When you write a `decimal.Decimal` value into a semi-structured column, it’s serialized as a JSON string so that all 38 `DECFLOAT` digits are preserved. To read it back as `DECFLOAT`, cast it to `VARCHAR` first, because Snowflake doesn’t allow a direct cast from the JSON text to `DECFLOAT`:

Copy code

```
from snowflake.sqlalchemy import DECFLOAT
from sqlalchemy import VARCHAR, cast, select

# payload:amt::VARCHAR::DECFLOAT
query = select(cast(cast(my_table.c.data['amt'], VARCHAR), DECFLOAT))
```

Also set `enable_decfloat=True` to avoid truncation to 28 digits. See [DECFLOAT precision](#label-sqlalchemy-decfloat-precision).

## GEOGRAPHY and GEOMETRY support

Snowflake SQLAlchemy supports the [geospatial data types](/sql-reference/data-types-geospatial) `GEOGRAPHY` and `GEOMETRY`:

Copy code

```
from snowflake.sqlalchemy import GEOGRAPHY, GEOMETRY
from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Places(Base):
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True)
    location = Column(GEOGRAPHY)
    shape = Column(GEOMETRY)
```

By default, geospatial values are returned as GeoJSON strings.

## Structured data types support

Snowflake SQLAlchemy supports the [structured data types](/sql-reference/data-types-structured) `MAP`, `OBJECT`, and `ARRAY` with element, key, and field types.

With [`enable_structured_type_json`](#label-sqlalchemy-structured-type-json) (the default), structured columns accept a Python `dict` or `list` on insert and update, and return a `dict` or `list` on read. The dialect writes the value as `CAST(PARSE_JSON(...) AS <declared type>)`:

Copy code

```
connection.execute(my_table.insert().values(id=1, properties={1: 'a'}, tags=['x', 'y']))
# INSERT INTO my_table (id, properties, tags)
#   SELECT ?, CAST(PARSE_JSON(?) AS MAP(...)), CAST(PARSE_JSON(?) AS ARRAY(...))
```

The same limitations as for semi-structured columns apply: no `RETURNING`, no `executemany`, and no `literal_binds`. Read values are decoded from JSON and aren’t converted to the declared element types. For example, `MAP(NUMBER, ...)` keys are returned as strings, and `DATE` elements as ISO strings.

### MAP

`MAP(key_type, value_type, not_null=False)` represents key-value pairs. Both `key_type` and `value_type` are required:

Copy code

```
from snowflake.sqlalchemy import MAP, NUMBER, TEXT
from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MyTable(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    properties = Column(MAP(NUMBER(10, 0), TEXT()))  # MAP(NUMBER(10,0), VARCHAR)
```

### OBJECT

`OBJECT(**items)` represents an object with named fields. Pass each field as a keyword argument whose value is a type, or a `(type, not_null)` tuple:

Copy code

```
from snowflake.sqlalchemy import NUMBER, OBJECT, TEXT
from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MyTable(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    user_info = Column(OBJECT(name=(TEXT(), False), age=NUMBER(10, 0)))
```

### ARRAY

`ARRAY(value_type, not_null=False)` represents a list of values of the same type:

Copy code

```
from snowflake.sqlalchemy import ARRAY, TEXT
from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MyTable(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    tags = Column(ARRAY(TEXT()))  # ARRAY(VARCHAR)
```

In a standard table, Snowflake rejects `ARRAY(..., not_null=True)` because a non-nullable field can’t be contained within an array or map.
