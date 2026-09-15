# Using the Snowflake SQLAlchemy toolkit with the Python Connector

Snowflake SQLAlchemy runs on the top of the Snowflake Connector for Python as a dialect to bridge a Snowflake database and SQLAlchemy applications.

For more information, see the [dialect](http://docs.sqlalchemy.org/en/latest/dialects/) documentation.

## Prerequisites

### Snowflake Connector for Python

The only requirement for Snowflake SQLAlchemy is the Snowflake Connector for Python; however, the connector does not need to be installed because installing Snowflake SQLAlchemy automatically installs
the connector.

### Data analytics and web application frameworks (optional)

Snowflake SQLAlchemy can be used with pandas, Jupyter, and Pyramid, which provide higher levels of application
frameworks for data analytics and web applications. However, building a working environment from scratch is not a trivial task, particularly for novice users. Installing the frameworks requires
C compilers and tools, and choosing the right tools and versions is a hurdle that might deter users from using Python applications.

An easier way to build an environment is through Anaconda, which provides a complete, precompiled technology stack for all users, including non-Python experts
such as data analysts and students. For Anaconda installation instructions, see the Anaconda install documentation. The Snowflake SQLAlchemy package can
then be installed on top of Anaconda using `pip`.

For more information, see the following documentation:

- [pandas](http://pandas.pydata.org/)
- [Jupyter](http://jupyter.org/)
- [Pyramid](http://www.pylonsproject.org/)
- [Anaconda](https://docs.continuum.io/anaconda/)
- [Anaconda install](https://docs.continuum.io/anaconda/install)
- [pip](https://pypi.org/project/pip/)

## Installing Snowflake SQLAlchemy

The Snowflake SQLAlchemy package can be installed from the public PyPI repository using `pip`:

> Copy code
>
> ```
> pip install --upgrade snowflake-sqlalchemy
> ```

`pip` automatically installs all required modules, including the Snowflake Connector for Python.

Note that the developer notes are hosted with the source code on [GitHub](https://github.com/snowflakedb/snowflake-sqlalchemy).

## Verifying your installation

1. Create a file (e.g. `validate.py`) that contains the following Python sample code,
   which connects to Snowflake and displays the Snowflake version:

   Copy code

   ```
   #!/usr/bin/env python
   from sqlalchemy import create_engine

   engine = create_engine(
    'snowflake://{user}:{password}@{account_identifier}/'.format(
        user='<user_login_name>',
        password='<password>',
        account_identifier='<account_identifier>',
    )
   )
   try:
    connection = engine.connect()
    results = connection.execute('select current_version()').fetchone()
    print(results[0])
   finally:
    connection.close()
    engine.dispose()
   ```
2. Replace `<user_login_name>`, `<password>`, and `<account_identifier>` with the appropriate values for your Snowflake account and user. For more details, see
   [Connection Parameters](#connection-parameters) (in this topic).
3. Execute the sample code. For example, if you created a file named `validate.py`:

   Copy code

   ```
   python validate.py
   ```

The Snowflake version (e.g. `1.6.0`) should be displayed.

## Snowflake-specific parameters and behavior

As much as possible, Snowflake SQLAlchemy provides compatible functionality for SQLAlchemy applications.

For information on using SQLAlchemy, see the [SQLAlchemy](http://docs.sqlalchemy.org/en/latest/) documentation.

However, Snowflake SQLAlchemy also provides Snowflake-specific parameters and behavior, which are described in the following sections.

### Connection parameters

#### Required parameters

Snowflake SQLAlchemy uses the following connection string syntax to connect to Snowflake and initiate a session:

Copy code

```
'snowflake://<user_login_name>:<password>@<account_identifier>'
```

Where:

- `<user_login_name>` is the login name for your Snowflake user.
- `<password>` is the password for your Snowflake user.
- `<account_identifier>` is your account identifier. See [Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config).

  Note

  Do not include the `snowflakecomputing.com` domain name as part of your account identifier. Snowflake
  automatically appends the domain name to your account identifier to create the required connection.

#### Additional connection parameters

You can optionally include the following additional information at the end of the connection string (after `<account_name>`):

Copy code

```
'snowflake://<user_login_name>:<password>@<account_identifier>/<database_name>/<schema_name>?warehouse=<warehouse_name>&role=<role_name>'
```

Where:

- `<database_name>` and `<schema_name>` are the initial database and schema for the Snowflake session, separated by forward slashes (`/`).
- `warehouse=<warehouse_name>` and `role=<role_name>'` are the initial warehouse and role for the session, specified as parameter strings, separated by question marks (`?`).

Note

After login, the initial database, schema, warehouse, and role specified in the connection string can always be changed for the session.

#### Proxy server configuration

Proxy server parameters are not supported. Instead, use the supported environment variables to configure a proxy server. For information, see [Using a proxy server](/developer-guide/python-connector/python-connector-connect#label-python-using-a-proxy-server).

#### Connection string examples

The following example calls the `create_engine` method with the user name `testuser1`, password `0123456`, account
identifier `myorganization-myaccount`, database `testdb`, schema `public`, warehouse `testwh`, and role `myrole`:

> Copy code
>
> ```
> from sqlalchemy import create_engine
> engine = create_engine(
>     'snowflake://testuser1:0123456@myorganization-myaccount/testdb/public?warehouse=testwh&role=myrole'
> )
> ```

For convenience, you can use the `snowflake.sqlalchemy.URL` method to construct the connection string and connect to the database. The following example constructs the same connection string
from the previous example:

> Copy code
>
> ```
> from snowflake.sqlalchemy import URL
> from sqlalchemy import create_engine
>
> engine = create_engine(URL(
>     account = 'myorganization-myaccount',
>     user = 'testuser1',
>     password = '0123456',
>     database = 'testdb',
>     schema = 'public',
>     warehouse = 'testwh',
>     role='myrole',
> ))
> ```

### Opening and closing a connection

Open a connection by executing `engine.connect()`; avoid using `engine.execute()`.

> Copy code
>
> ```
> # Avoid this.
> engine = create_engine(...)
> engine.execute(<SQL>)
> engine.dispose()
>
> # Do this.
> engine = create_engine(...)
> connection = engine.connect()
> try:
>     connection.execute(<SQL>)
> finally:
>     connection.close()
>     engine.dispose()
> ```

Note

Make certain to close the connection by executing `connection.close()` before `engine.dispose()`; otherwise, the Python Garbage collector removes the resources required to communicate
with Snowflake, preventing the Python connector from closing the session properly.

If you plan to use explicit transactions, you must disable the AUTOCOMMIT execution option in SQLAlchemy.

For more information, see [AUTOCOMMIT execution option in SQLAlchemy](https://docs.sqlalchemy.org/en/14/core/connections.html#library-level-e-g-emulated-autocommit)..

By default, SQLAlchemy enables this option. When this option is enabled, INSERT, UPDATE, and DELETE statements are committed
automatically upon execution, even when these statements are run within an explicit transaction.

To disable AUTOCOMMIT, pass `autocommit=False` to the `Connection.execution_options()` method. For example:

Copy code

```
# Disable AUTOCOMMIT if you need to use an explicit transaction.
with engine.connect().execution_options(autocommit=False) as connection:

  try:
    connection.execute("BEGIN")
    connection.execute("INSERT INTO test_table VALUES (88888, 'X', 434354)")
    connection.execute("INSERT INTO test_table VALUES (99999, 'Y', 453654654)")
    connection.execute("COMMIT")
  except Exception as e:
    connection.execute("ROLLBACK")
  finally:
    connection.close()

engine.dispose()
```

### Auto-increment behavior

Auto-incrementing a value requires the `Sequence` object. Include the `Sequence` object in the primary key column to automatically increment the value as each new record is inserted.
For example:

> Copy code
>
> ```
> t = Table('mytable', metadata,
>     Column('id', Integer, Sequence('id_seq'), primary_key=True),
>     Column(...), ...
> )
> ```

### Object name case handling

Snowflake stores all case-insensitive object names in uppercase text. In contrast, SQLAlchemy considers all lowercase object names to be case-insensitive. Snowflake SQLAlchemy converts the object
name case during schema-level communication (i.e. during table and index reflection). If you use uppercase object names, SQLAlchemy assumes they are case-sensitive and encloses the names with quotes.
This behavior will cause mismatches against data dictionary data received from Snowflake, so unless identifier names have been truly created as case sensitive using quotes (e.g. `"TestDb"`),
all lowercase names should be used on the SQLAlchemy side.

### Index support

Indexes are supported only for Hybrid Tables in Snowflake SqlAlchemy. For more details on limitations and use cases, refer to
[the usage notes for CREATE INDEX](/sql-reference/sql/create-index#label-create-index-usage-notes). You can create an index using the following methods:

- Single column index

  You can create a single column index by setting the `index=True` parameter on the column or by explicitly defining an `Index` object.

  Copy code

  ```
  hybrid_test_table_1 = HybridTable(
    "table_name",
    metadata,
    Column("column1", Integer, primary_key=True),
    Column("column2", String, index=True),
    Index("index_1","column1", "column2")
  )

  metadata.create_all(engine_testaccount)
  ```
- Multi-column index

  For multi-column indexes, you define the Index object specifying the columns that should be indexed.

  Copy code

  ```
  hybrid_test_table_1 = HybridTable(
    "table_name",
    metadata,
    Column("column1", Integer, primary_key=True),
    Column("column2", String),
    Index("index_1","column1", "column2")
  )

  metadata.create_all(engine_testaccount)
  ```

### Numpy data type support

Snowflake SQLAlchemy supports binding and fetching `NumPy` data types. Binding is always supported. To enable fetching `NumPy` data types, add `numpy=True` to the connection
parameters.

The following `NumPy` data types are supported:

- `numpy.int64`
- `numpy.float64`
- `numpy.datetime64`

The following example shows the round trip of `numpy.datetime64` data:

> Copy code
>
> ```
> import numpy as np
> import pandas as pd
> engine = create_engine(URL(
>     account = 'myorganization-myaccount',
>     user = 'testuser1',
>     password = 'pass',
>     database = 'db',
>     schema = 'public',
>     warehouse = 'testwh',
>     role='myrole',
>     numpy=True,
> ))
>
> specific_date = np.datetime64('2016-03-04T12:03:05.123456789Z')
>
> with engine.connect() as connection:
>     connection.exec_sql_query(
>         "CREATE OR REPLACE TABLE ts_tbl(c1 TIMESTAMP_NTZ)")
>     connection.exec_sql_query(
>         "INSERT INTO ts_tbl(c1) values(%s)", (specific_date,)
>     )
>     df = pd.read_sql_query("SELECT * FROM ts_tbl", connection)
>     assert df.c1.values[0] == specific_date
> ```

### Cache column metadata

SQLAlchemy provides the runtime inspection API to get the runtime information about the various objects. One of the common use case
is get all tables and their column metadata in a schema in order to construct a schema catalog.

For more information, see [runtime inspection API](http://docs.sqlalchemy.org/en/latest/core/inspection.html). For an example managing database schema migrations with SQLAlchemy, [alembic](http://alembic.zzzcomputing.com/) .

A pseudo code flow is as follows:

> Copy code
>
> ```
> inspector = inspect(engine)
> schema = inspector.default_schema_name
> for table_name in inspector.get_table_names(schema):
>     column_metadata = inspector.get_columns(table_name, schema)
>     primary_keys = inspector.get_primary_keys(table_name, schema)
>     foreign_keys = inspector.get_foreign_keys(table_name, schema)
>     ...
> ```

In this flow, a potential problem is it may take quite a while as queries run on each table. The results are cached but getting column metadata is expensive.

To mitigate the problem, Snowflake SQLAlchemy takes a flag `cache_column_metadata=True` such that all of column metadata for all tables are cached when `get_table_names` is called and
the rest of `get_columns`, `get_primary_keys` and `get_foreign_keys` can take advantage of the cache.

> Copy code
>
> ```
> engine = create_engine(URL(
>     account = 'myorganization-myaccount',
>     user = 'testuser1',
>     password = 'pass',
>     database = 'db',
>     schema = 'public',
>     warehouse = 'testwh',
>     role='myrole',
>     cache_column_metadata=True,
> ))
> ```

Note

Memory usage will go up higher as all of column metadata are cached associated with `Inspector` object. Use the flag only if you need to get all of column metadata.

### VARIANT, ARRAY, and OBJECT support

Snowflake SQLAlchemy supports fetching `VARIANT`, `ARRAY` and `OBJECT` data types. All types are converted into `str` in Python so that you can convert them to native data
types using `json.loads`.

This example shows how to create a table including `VARIANT`, `ARRAY`, and `OBJECT` data type columns:

> Copy code
>
> ```
> from snowflake.sqlalchemy import (VARIANT, ARRAY, OBJECT)
> ...
> t = Table('my_semi_structured_datatype_table', metadata,
>     Column('va', VARIANT),
>     Column('ob', OBJECT),
>     Column('ar', ARRAY))
> metadata.create_all(engine)
> ```

In order to retrieve `VARIANT`, `ARRAY`, and `OBJECT` data type columns and convert them to the native Python data types, fetch data and call the `json.loads` method as follows:

> Copy code
>
> ```
> import json
> connection = engine.connect()
> results = connection.execute(select([t]))
> row = results.fetchone()
> data_variant = json.loads(row[0])
> data_object  = json.loads(row[1])
> data_array   = json.loads(row[2])
> ```

### Structured data types support

This module defines custom SQLAlchemy types for Snowflake structured data, specifically for Iceberg tables. The MAP, OBJECT, and ARRAY types allow you to store complex data structures in your SQLAlchemy models. For detailed information, refer to the Snowflake [Structured data types](/sql-reference/data-types-structured) documentation.

#### MAP

The `MAP` type represents a collection of key-value pairs, where each key and value can have different types, as shown:

- **Key Type:** The type of the key, such as `TEXT` or `NUMBER`).
- **Value Type:** The type of the value, such as `TEXT` or `NUMBER`).
- **Not Null:** Whether NULL values are allowed (default is `False`).

Usage example:

Copy code

```
IcebergTable(
  table_name,
  metadata,
  Column("id", Integer, primary_key=True),
  Column("map_col", MAP(NUMBER(10, 0), TEXT(134217728))),
  external_volume="external_volume",
  base_location="base_location",
)
```

#### OBJECT

The `OBJECT` type represents a semi-structured object with named fields. Each field can have a specific type, and you can also specify whether each field is nullable.

- **Items Types:** A dictionary of field names and their types. The type can optionally include a nullable flag (`True` for not nullable or `False` for nullable [default]).

Usage example:

Copy code

```
IcebergTable(
    table_name,
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "object_col",
        OBJECT(key1=(TEXT(134217728), False), key2=(NUMBER(10, 0), False)),
        OBJECT(key1=TEXT(1134217728), key2=NUMBER(10, 0)), # Without nullable flag
    ),
    external_volume="external_volume",
    base_location="base_location",
)
```

#### ARRAY

The `ARRAY` type represents an ordered list of values, where each element has the same type. The type of the elements is defined when the array is created.

- **Value Type:** The type of the elements in the array, such as `TEXT` or `NUMBER`).
- **Not Null:** Whether `NULL` values are allowed (default is `False`).

Usage example:

Copy code

```
IcebergTable(
    table_name,
    metadata,
    Column("id", Integer, primary_key=True),
    Column("array_col", ARRAY(TEXT(134217728))),
    external_volume="external_volume",
    base_location="base_location",
)
```

### CLUSTER BY support

Snowflake SQLAlchemy supports the `CLUSTER BY` parameter for tables. For information about the parameter, see [CREATE TABLE](/sql-reference/sql/create-table).

This example shows how to create a table with two columns, `id` and `name`, as the clustering key:

> Copy code
>
> ```
> t = Table('myuser', metadata,
>     Column('id', Integer, primary_key=True),
>     Column('name', String),
>     snowflake_clusterby=['id', 'name'], ...
> )
> metadata.create_all(engine)
> ```

### Alembic support

Alembic is a database migration tool on top of `SQLAlchemy`. Snowflake SQLAlchemy works by adding the following code to `alembic/env.py` so that Alembic can recognize Snowflake SQLAlchemy.

> Copy code
>
> ```
> from alembic.ddl.impl import DefaultImpl
>
> class SnowflakeImpl(DefaultImpl):
>     __dialect__ = 'snowflake'
> ```

See [Alembic Documentation](http://alembic.zzzcomputing.com/) for general usage.

### Key pair authentication support

Snowflake SQLAlchemy supports key pair authentication by leveraging the functionality of Snowflake Connector for Python.
See [Using key-pair authentication and key-pair rotation](/developer-guide/python-connector/python-connector-connect#label-python-key-pair-authn-rotation) for steps to create the private and public keys.

The private key parameter is passed through `connect_args` as follows:

> Copy code
>
> ```
> ...
> from snowflake.sqlalchemy import URL
> from sqlalchemy import create_engine
>
> from cryptography.hazmat.backends import default_backend
> from cryptography.hazmat.primitives import serialization
>
> with open("rsa_key.p8", "rb") as key:
>     p_key= serialization.load_pem_private_key(
>         key.read(),
>         password=os.environ['PRIVATE_KEY_PASSPHRASE'].encode(),
>         backend=default_backend()
>     )
>
> pkb = p_key.private_bytes(
>     encoding=serialization.Encoding.DER,
>     format=serialization.PrivateFormat.PKCS8,
>     encryption_algorithm=serialization.NoEncryption())
>
> engine = create_engine(URL(
>     account='abc123',
>     user='testuser1',
>     ),
>     connect_args={
>         'private_key': pkb,
>         },
>     )
> ```

Where `PRIVATE_KEY_PASSPHRASE` is a passphrase to decrypt the private key file, `rsa_key.p8`.

The `snowflake.sqlalchemy.URL` method does not support private key parameters.

### Merge command support

Snowflake SQLAlchemy supports performing an upsert with its `MergeInto` custom expression. See [MERGE](/sql-reference/sql/merge) for full documentation.

Use it as follows:

> Copy code
>
> ```
> from sqlalchemy.orm import sessionmaker
> from sqlalchemy import MetaData, create_engine
> from snowflake.sqlalchemy import MergeInto
>
> engine = create_engine(db.url, echo=False)
> session = sessionmaker(bind=engine)()
> connection = engine.connect()
>
> meta = MetaData()
> meta.reflect(bind=session.bind)
> t1 = meta.tables['t1']
> t2 = meta.tables['t2']
>
> merge = MergeInto(target=t1, source=t2, on=t1.c.t1key == t2.c.t2key)
> merge.when_matched_then_delete().where(t2.c.marked == 1)
> merge.when_matched_then_update().where(t2.c.isnewstatus == 1).values(val = t2.c.newval, status=t2.c.newstatus)
> merge.when_matched_then_update().values(val=t2.c.newval)
> merge.when_not_matched_then_insert().values(val=t2.c.newval, status=t2.c.newstatus)
> connection.execute(merge)
> ```

### CopyIntoStorage support

Snowflake SQLAlchemy supports saving tables and query results into different Snowflake stages, Azure Containers, and AWS buckets with
its custom `CopyIntoStorage` expression. See [COPY INTO <location>](/sql-reference/sql/copy-into-location) for full documentation.

Use it as follows:

> Copy code
>
> ```
> from sqlalchemy.orm import sessionmaker
> from sqlalchemy import MetaData, create_engine
> from snowflake.sqlalchemy import CopyIntoStorage, AWSBucket, CSVFormatter
>
> engine = create_engine(db.url, echo=False)
> session = sessionmaker(bind=engine)()
> connection = engine.connect()
>
> meta = MetaData()
> meta.reflect(bind=session.bind)
> users = meta.tables['users']
>
> copy_into = CopyIntoStorage(from_=users,
>                             into=AWSBucket.from_uri('s3://my_private_backup').encryption_aws_sse_kms('1234abcd-12ab-34cd-56ef-1234567890ab'),
>                             formatter=CSVFormatter().null_if(['null', 'Null']))
> connection.execute(copy_into)
> ```

### Iceberg Table with Snowflake Catalog support

Snowflake SQLAlchemy supports Iceberg Tables with the Snowflake Catalog, along with various related parameters. For detailed information about Iceberg Tables, refer to the Snowflake [CREATE ICEBERG](/sql-reference/sql/create-iceberg-table-snowflake) documentation.

To create an Iceberg Table using Snowflake SQLAlchemy, you can define the table using the SQLAlchemy Core syntax as follows:

Copy code

```
table = IcebergTable(
        "myuser",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String),
        external_volume=external_volume_name,
        base_location="my_iceberg_table",
  as_query="SELECT * FROM table"
    )
```

Alternatively, you can define the table using a declarative approach:

Copy code

```
class MyUser(Base):
    __tablename__ = "myuser"

    @classmethod
    def __table_cls__(cls, name, metadata, *arg, **kw):
        return IcebergTable(name, metadata, *arg, **kw)

    __table_args__ = {
        "external_volume": "my_external_volume",
        "base_location": "my_iceberg_table",
  "as_query": "SELECT * FROM table",
    }

    id = Column(Integer, primary_key=True)
    name = Column(String)
```

### Hybrid Table support

Snowflake SQLAlchemy supports Hybrid Tables with indexes. For detailed information refer to the Snowflake [CREATE HYBRID TABLE](/sql-reference/sql/create-hybrid-table) documentation.

To create a Hybrid Table and add an index, you can use the SQLAlchemy Core syntax as follows:

Copy code

```
table = HybridTable(
    "myuser",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Index("idx_name", "name")
```

Alternatively, you can define the table using the declarative approach:

Copy code

```
class MyUser(Base):
    __tablename__ = "myuser"

    @classmethod
    def __table_cls__(cls, name, metadata, *arg, **kw):
        return HybridTable(name, metadata, *arg, **kw)

    __table_args__ = (
        Index("idx_name", "name"),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String)
```

### Dynamic Tables support

Snowflake SQLAlchemy supports Dynamic Tables. For detailed information refer to the Snowflake [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table) documentation.

To create a Dynamic Table, you can use the SQLAlchemy Core syntax as follows:

Copy code

```
 dynamic_test_table_1 = DynamicTable(
       "dynamic_MyUser",
       metadata,
       Column("id", Integer),
       Column("name", String),
       target_lag=(1, TimeUnit.HOURS), # Additionally you can use SnowflakeKeyword.DOWNSTREAM
       warehouse='test_wh',
refresh_mode=SnowflakeKeyword.FULL
       as_query="SELECT id, name from MyUser;"
   )
```

Additionally you can define a table without columns using SqlAlchemy select() construct:

Copy code

```
 dynamic_test_table_1 = DynamicTable(
       "dynamic_MyUser",
       metadata,
       target_lag=(1, TimeUnit.HOURS),
       warehouse='test_wh',
refresh_mode=SnowflakeKeyword.FULL
       as_query=select(MyUser.id, MyUser.name)
   )
```

Note

- Defining a primary key in a Dynamic Table is not supported, meaning declarative tables don’t support Dynamic Tables.
- When using the `as_query` parameter with a string, you must explicitly define the columns. However, if you use the SQLAlchemy `select()` construct, you don’t need to explicitly define the columns.
- Direct data insertion into Dynamic Tables is not supported.
