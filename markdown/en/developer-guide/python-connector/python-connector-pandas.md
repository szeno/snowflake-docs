# Using pandas DataFrames with the Python Connector

pandas is a library for data analysis. With pandas, you use a data structure called a DataFrame
to analyze and manipulate two-dimensional data (such as data from a database table).

For more information see the [pandas](https://pandas.pydata.org/) documentation.

If you need to get data from a Snowflake database to a pandas DataFrame, you can use the API methods provided with the Snowflake
Connector for Python. The connector also provides API methods for writing data from a pandas DataFrame to a Snowflake database.

Note

Some of these API methods require a specific version of the PyArrow library.
See [Requirements](#requirements) for details.

For more information, see the [PyArrow library](https://arrow.apache.org/docs/python/) documentation.

## Requirements

Currently, the pandas-oriented API methods in the Python connector API work with:

- Snowflake Connector 2.1.2 (or later) for Python.
- PyArrow library version 3.0.x (or later), depending on your connector version.

  If you do not have PyArrow installed, you do not need to install PyArrow yourself;
  installing the Python Connector as documented below automatically installs the appropriate version of PyArrow.

  Caution

  If you already have any version of the PyArrow library other than the recommended version listed above,
  please uninstall PyArrow before installing the Snowflake Connector for Python. Do not re-install a different
  version of PyArrow after installing the Snowflake Connector for Python.

  For more information, see the [PyArrow library](https://arrow.apache.org/docs/python/) documentation.
- pandas 0.25.2 (or later), depending on your connector version. Earlier versions might work, but have not been tested.

## Installation

To install the pandas-compatible version of the Snowflake Connector for Python, execute the command:

Copy code

```
pip install "snowflake-connector-python[pandas]"
```

You must enter the square brackets (`[` and `]`) as shown in the command. The square brackets specify the
extra part of the package to install.

For more information, see the [extras](https://www.python.org/dev/peps/pep-0508/#extras) Python dependency.

Use quotes around the name of the package (as shown) to prevent the square brackets from being interpreted as a wildcard.

If you need to install other extras (for example, `secure-local-storage` for
[caching connections with browser-based SSO](/user-guide/admin-security-fed-auth-use#label-browser-based-sso-connection-caching) or
[caching MFA tokens](/user-guide/security-mfa#label-mfa-token-caching)), use a comma between the extras:

Copy code

```
pip install "snowflake-connector-python[secure-local-storage,pandas]"
```

## Reading data from a Snowflake database to a pandas DataFrame

To read data into a pandas DataFrame, you use a [Cursor](/developer-guide/python-connector/python-connector-api#label-python-connector-cursor-object) to
[retrieve the data](/developer-guide/python-connector/python-connector-example#label-python-connector-querying-data) and then call one of these `Cursor` methods to put the data
into a pandas DataFrame:

- `fetch_pandas_all()`.
- `fetch_pandas_batches()`.

## Writing data from a pandas DataFrame to a Snowflake database

To write data from a pandas DataFrame to a Snowflake database, do one of the following:

- Call the `write_pandas()` function.
- Call the `pandas.DataFrame.to_sql()` method.

  For more information, see the
  [pandas.DataFrame.to\_sql](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html) documentation,
  and specify `pd_writer()` as the method to use to insert the data into the database.

## Snowflake to pandas data mapping

The table below shows the mapping from Snowflake data types to pandas data types:

| Snowflake Data Type | pandas Data Type |
| --- | --- |
| FIXED NUMERIC type (scale = 0) except DECIMAL | `(u)int{8,16,32,64}` or `float64` (for NULL) |
| FIXED NUMERIC type (scale > 0) except DECIMAL | `float64` |
| FIXED NUMERIC type DECIMAL | `decimal` |
| FLOAT/DOUBLE | `float64` |
| VARCHAR | `str` |
| BINARY | `str` |
| VARIANT | `str` |
| DATE | `object` (with `datetime.date` objects) |
| TIME | `pandas.Timestamp(np.datetime64[ns])` |
| TIMESTAMP\_NTZ, TIMESTAMP\_LTZ, TIMESTAMP\_TZ | `pandas.Timestamp(np.datetime64[ns])` |

Expand

Show lessSee more

Notes:

- If the Snowflake data type is FIXED NUMERIC and the scale is zero, and if the value is NULL, then the value is
  converted to `float64`, not an integer type.
- If any conversion causes overflow, the Python connector throws an exception.

## Importing pandas

Customarily, pandas is imported with the following statement:

> Copy code
>
> ```
> import pandas as pd
> ```

You might see references to pandas objects as either `pandas.object` or `pd.object`.

## Migrating to pandas DataFrames

This section is primarily for users who have used pandas (and possibly SQLAlchemy) previously.

Previous pandas users might have code similar to either of the following:

- This example shows the original way to generate a pandas DataFrame from the Python connector:

  Copy code

  ```
  import pandas as pd

  def fetch_pandas_old(cur, sql):
   cur.execute(sql)
   rows = 0
   while True:
       dat = cur.fetchmany(50000)
       if not dat:
           break
       df = pd.DataFrame(dat, columns=cur.description)
       rows += df.shape[0]
   print(rows)
  ```
- This example shows how to use SQLAlchemy to generate a pandas DataFrame:

  Copy code

  ```
  import pandas as pd

  def fetch_pandas_sqlalchemy(sql):
   rows = 0
   for chunk in pd.read_sql_query(sql, engine, chunksize=50000):
       rows += chunk.shape[0]
   print(rows)
  ```

Code that is similar to either of the preceding examples can be converted to use the Python connector pandas
API calls listed in [Reading Data from a Snowflake Database to a pandas DataFrame](#reading-data-from-a-snowflake-database-to-a-pandas-dataframe) (in this topic).

Note

With support for pandas in the Python connector, SQLAlchemy is no longer needed to convert data in a cursor
into a DataFrame.

However, you can continue to use SQLAlchemy if you wish; the Python connector maintains compatibility with
SQLAlchemy.
