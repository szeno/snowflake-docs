# Local testing framework

This topic explains how to test your code locally when working with the Snowpark Python library.

The Snowpark Python local testing framework is an emulator that allows you to create and operate on Snowpark Python DataFrames locally without
connecting to a Snowflake account. You can use the local testing framework to test your DataFrame operations on your development
machine or in a CI (continuous integration) pipeline before deploying code changes to your account. The API is the same,
so you can run your tests either locally or against a Snowflake account without making code changes.

## Prerequisites

To use the local testing framework:

You must use version 1.18.0 or later of the Snowpark Python library with the optional dependency `localtest`. The supported versions of Python are:

Generally available versions:

- 3.9 (deprecated)
- 3.10
- 3.11
- 3.12
- 3.13
- 3.14

### Install the Snowpark Python library

- To install the library with the optional dependency, run the following command:

  Copy code

  ```
  pip install "snowflake-snowpark-python[localtest]"
  ```

## Create a session and enable local testing

1. Create a Snowpark `Session` and set the local testing configuration to `True`:

   Copy code

   ```
   from snowflake.snowpark import Session

   session = Session.builder.config('local_testing', True).create()
   ```
2. Use the session to create and operate on DataFrames:

   Copy code

   ```
   df = session.create_dataframe([[1,2],[3,4]],['a','b'])
   df.with_column('c', df['a']+df['b']).show()
   ```

## Loading data

You can create Snowpark DataFrames from Python primitives, files, and pandas DataFrames.
This is useful for specifying the input and expected output of test cases. With this method,
the data is in source control, which makes it easier to keep the test data in sync with the test cases.

### Load CSV data

- To load CSV files into a Snowpark DataFrame, first call `Session.file.put()` to load the file to the in-memory stage, and then use `Session.read()` to read the contents.

**Example**

Assume there is a file, `data.csv`, with the following contents:

Copy code

```
col1,col2,col3,col4
1,a,true,1.23
2,b,false,4.56
```

You can use the following code to load `data.csv` into a Snowpark DataFrame.
You need to put the file onto a stage first; If you do not, you will receive a “file cannot be found” error.

Copy code

```
from snowflake.snowpark.types import StructType, StructField, IntegerType, BooleanType, StringType, DoubleType

# Put file onto stage
session.file.put("data.csv", "@mystage", auto_compress=False)
schema = StructType(
    [
        StructField("col1", IntegerType()),
        StructField("col2", StringType()),
        StructField("col3", BooleanType()),
        StructField("col4", DoubleType()),
    ]
)

# with option SKIP_HEADER set to 1, the header will be skipped when the csv file is loaded
dataframe = session.read.schema(schema).option("SKIP_HEADER", 1).csv("@mystage/data.csv")
dataframe.show()
```

Expected output:

```
-------------------------------------
|"COL1"  |"COL2"  |"COL3"  |"COL4"  |
-------------------------------------
|1       |a       |True    |1.23    |
|2       |b       |False   |4.56    |
-------------------------------------
```

### Load pandas data

- To create a Snowpark Python DataFrame from a pandas DataFrame, call the `create_dataframe` method and pass the data as a pandas DataFrame.

**Example**

Copy code

```
import pandas as pd

pandas_df = pd.DataFrame(
    data={
        "col1": pd.Series(["value1", "value2"]),
        "col2": pd.Series([1.23, 4.56]),
        "col3": pd.Series([123, 456]),
        "col4": pd.Series([True, False]),
    }
)

dataframe = session.create_dataframe(data=pandas_df)
dataframe.show()
```

Expected output:

```
-------------------------------------
|"col1"  |"col2"  |"col3"  |"col4"  |
-------------------------------------
|value1  |1.23    |123     |True    |
|value2  |4.56    |456     |False   |
-------------------------------------
```

- To convert a Snowpark Python DataFrame to a pandas DataFrame, call the `to_pandas` method on the DataFrame.

**Example**

Copy code

```
from snowflake.snowpark.types import StructType, StructField, StringType, DoubleType, LongType, BooleanType

dataframe = session.create_dataframe(
    data=[
        ["value1", 1.23, 123, True],
        ["value2", 4.56, 456, False],
    ],
    schema=StructType([
        StructField("col1", StringType()),
        StructField("col2", DoubleType()),
        StructField("col3", LongType()),
        StructField("col4", BooleanType()),
    ])
)

pandas_dataframe = dataframe.to_pandas()
print(pandas_dataframe.to_string())
```

Expected output:

```
    COL1  COL2  COL3   COL4
0  value1  1.23   123   True
1  value2  4.56   456  False
```

## Create a PyTest Fixture for a session

[PyTest fixtures](https://docs.pytest.org/en/6.2.x/fixture.html) are functions that are executed before a test (or module of tests),
typically to provide data or connections to tests. In this procedure, you create a fixture that returns a Snowpark `Session` object.

1. If you do not already have a `test` directory, create one.
2. In the `test` directory, create a file named `conftest.py` with the following contents, where `connection_parameters` is a dictionary with your Snowflake account credentials:

   Copy code

   ```
   # test/conftest.py
   import pytest
   from snowflake.snowpark.session import Session

   def pytest_addoption(parser):
    parser.addoption("--snowflake-session", action="store", default="live")

   @pytest.fixture(scope='module')
   def session(request) -> Session:
    if request.config.getoption('--snowflake-session') == 'local':
        return Session.builder.config('local_testing', True).create()
    else:
        return Session.builder.configs(CONNECTION_PARAMETERS).create()
   ```

For more information about the dictionary format, see [Creating a Session](/developer-guide/snowpark/python/creating-session#label-snowpark-python-creating-session).

The call to `pytest_addoption` adds a command-line option named `snowflake-session` to the `pytest` command.
The `Session` fixture checks this command-line option and creates a local or live `Session`, depending on its value.
This lets you easily switch between local and live modes for testing, as shown in the following command-line examples:

Copy code

```
# Using local mode:
pytest --snowflake-session local

# Using live mode
pytest
```

## SQL operations

`Session.sql(...)` is not supported in the local testing framework. Use Snowpark’s DataFrame APIs whenever possible,
and in cases where you must use `Session.sql(...)`, you can mock the tabular return value by using Python’s
`unittest.mock.patch` to patch the expected response from a given `Session.sql()` call.

In the following example, `mock_sql()` maps the SQL query text to the desired DataFrame response.
The conditional statement checks whether the current session is using local testing, and if so, applies the patch to the `Session.sql()` method.

Copy code

```
from unittest import mock
from functools import partial

def test_something(pytestconfig, session):

    def mock_sql(session, sql_string):  # patch for SQL operations
        if sql_string == "select 1,2,3":
            return session.create_dataframe([[1,2,3]])
        else:
            raise RuntimeError(f"Unexpected query execution: {sql_string}")

    if pytestconfig.getoption('--snowflake-session') == 'local':
        with mock.patch.object(session, 'sql', wraps=partial(mock_sql, session)): # apply patch for SQL operations
            assert session.sql("select 1,2,3").collect() == [Row(1,2,3)]
    else:
        assert session.sql("select 1,2,3").collect() == [Row(1,2,3)]
```

When local testing is enabled, all tables created by `DataFrame.save_as_table()` are saved as temporary tables in memory and can be
retrieved using `Session.table()`. You can use the supported DataFrame operations on the table as usual.

## Patching built-in functions

Some of the built-in functions under `snowflake.snowpark.functions` are not supported in the local testing framework.
If you use a function that is not supported, you can use the `@patch` decorator from `snowflake.snowpark.mock` to create a patch.

For the patched function to be defined and implemented, the signature (parameter list) must align with the built-in function’s parameters. The local testing framework passes parameters to the patched function using the following rules:

- For parameters of type `ColumnOrName` in the signature of built-in functions, `ColumnEmulator` is passed as the parameter of the patched functions.
  `ColumnEmulator` is similar to a `pandas.Series` object that contains the column data.
- For parameters of type `LiteralType` in the signature of built-in functions, the literal value is passed as the parameter of the patched functions.
- Otherwise, the raw value is passed as the parameter of the patched functions.

As for the returning type of the patched functions, returning an instance of `ColumnEmulator` is expected in correspondence with the returning type of `Column` of built-in functions.

For example, the built-in function `to_timestamp()` could be patched like this:

Copy code

```
import datetime
from snowflake.snowpark.mock import patch, ColumnEmulator, ColumnType
from snowflake.snowpark.functions import to_timestamp
from snowflake.snowpark.types import TimestampType

@patch(to_timestamp)
def mock_to_timestamp(column: ColumnEmulator, format = None) -> ColumnEmulator:
    ret_column = ColumnEmulator(data=[datetime.datetime.strptime(row, '%Y-%m-%dT%H:%M:%S%z') for row in column])
    ret_column.sf_type = ColumnType(TimestampType(), True)
    return ret_column
```

## Skipping test cases

If your PyTest test suite contains a test case that is not well supported by local testing, you can skip those cases by using PyTest’s `mark.skipif` decorator.
The following example assumes that you configured your session and parameters as described earlier. The condition checks whether the `local_testing_mode` is set to `local`; if so, the test case is skipped with an explanatory message.

Copy code

```
import pytest

@pytest.mark.skipif(
    condition="config.getvalue('local_testing_mode') == 'local'",
reason="Test case disabled for local testing"
)
def test_case(session):
    ...
```

## Registering UDFs and stored procedures

You can create and call user-defined functions (UDFs) and stored procedures in the local testing framework. To create the objects, you can
use the following syntax options:

| Syntax | UDF | Stored procedure |
| --- | --- | --- |
| Decorators | `@udf` | `@sproc` |
| Register methods | `udf.register()` | `sproc.register()` |
| Register-from-file methods | `udf.register_from_file()` | `sproc.register_from_file()` |

Expand

Show lessSee more

**Example**

The following code example creates a UDF and stored procedure using the decorators, and then calls both by name:

Copy code

```
from snowflake.snowpark.session import Session
from snowflake.snowpark.dataframe import col, DataFrame
from snowflake.snowpark.functions import udf, sproc, call_udf
from snowflake.snowpark.types import IntegerType, StringType

# Create local session
session = Session.builder.config('local_testing', True).create()

# Create local table
table = 'example'
session.create_dataframe([[1,2],[3,4]],['a','b']).write.save_as_table(table)

# Register a UDF, which is called from the stored procedure
@udf(name='example_udf', return_type=IntegerType(), input_types=[IntegerType(), IntegerType()])
def example_udf(a, b):
    return a + b

# Register stored procedure
@sproc(name='example_proc', return_type=IntegerType(), input_types=[StringType()])
def example_proc(session, table_name):
    return session.table(table_name)\
        .with_column('c', call_udf('example_udf', col('a'), col('b')))\
        .count()

# Call the stored procedure by name
output = session.call('example_proc', table)

print(output)
```

## Limitations

The following list contains the known limitations and behavior gaps in the local testing framework. **Snowflake currently has no plans to address these
items.**

- Raw SQL strings and operations that require parsing SQL strings, such as `session.sql` and `DataFrame.filter("col1 > 12")`,
  are not supported.
- Asynchronous operations are not supported.
- Database objects such as tables, stored procedures, and UDFs are not persisted beyond the session level, and all operations are performed
  in memory. For example, permanent stored procedures registered in one mock session are not visible to other mock sessions.
- [String collation](/sql-reference/collation) related features, such as `Column.collate`, are not supported.
- `Variant`, `Array`, and `Object` data types are only supported with standard JSON encoding and decoding. Expressions
  like [1,2,,3,] are considered valid JSON in Snowflake but not in local testing, where Python’s built-in JSON functionalities are used. You
  can specify the module-level variables `snowflake.snowpark.mock.CUSTOM_JSON_ENCODER` and
  `snowflake.snowpark.mock.CUSTOM_JSON_DECODER` to override the default settings.
- Only a subset of Snowflake’s functions (including window functions) are implemented. To learn how to inject your own function definition,
  see [Patching built-in functions](#label-snowpark-python-local-testing-patching).

  - Patching rank-related functions is currently not supported.
- [SQL format models](/sql-reference/sql-format-models) are not supported. For example, the mock implementation of `to_decimal` does not handle the
  optional parameter `format`.
- The Snowpark Python library does not have a built-in Python API to create or drop stages, so the local testing framework assumes that every
  incoming stage has already been created.
- The current implementation of UDFs and stored procedures does not perform any package validation. All packages referenced in your code
  need to be installed before the program is executed.
- Query tags are not supported.
- Query history is not supported.
- Lineage is not supported.
- When a UDF or stored procedure is registered, optional parameters such as `parallel`, `execute_as`, `statement_params`,
  `source_code_display`, `external_access_integrations`, `secrets`, and `comment` are ignored.
- For `Table.sample`, SYSTEM or BLOCK sampling is the same as ROW sampling.
- Snowflake does not officially support running the local testing framework inside stored procedures. Sessions of local testing mode inside
  stored procedures might encounter or trigger unexpected errors.

## Unsupported features

The following is a list of features that are currently not implemented in the local testing framework. **Snowflake is actively working to address
these items.**

In general, any reference to these functionalities should raise a `NotImplementedError`:

- UDTFs (user-defined table functions)
- UDAFs (user-defined aggregate functions)
- Vectorized UDFs and UDTFs
- Built-in table functions
- Table stored procedures
- `Geometry`, `Geography`, and `Vector` data types
- Interval expressions
- Read file formats other than JSON and CSV
  - For a supported file format, not all read options are supported. For example, `infer_schema` is not supported for the CSV format.

For any features not listed here as unsupported or as a known limitation, check the latest list of [feature requests for local testing](https://github.com/snowflakedb/snowpark-python/issues?q=is%3Aopen+label%3A%22local+testing%22+label%3A%22feature%22+), or
[create a feature request](https://github.com/snowflakedb/snowpark-python/issues/new/choose) in the `snowpark-python` GitHub repository.

## Known issues

The following is a list of known issues or behavior gaps that exist in the local testing framework. **Snowflake is actively planning to address
these issues.**

- Using window functions inside `DataFrame.groupby` or other aggregation operations is not supported.

  Copy code

  ```
  # Selecting window function expressions is supported
  df.select("key", "value", sum_("value").over(), avg("value").over())

  # Aggregating window function expressions is NOT supported
  df.group_by("key").agg([sum_("value"), sum_(sum_("value")).over(window) - sum_("value")])
  ```
- Selecting columns with the same name will only return one column. As a workaround, use
  `Column.alias` to rename the columns to have distinct names.

  Copy code

  ```
  df.select(lit(1), lit(1)).show() # col("a"), col("a")
  #---------
  #|"'1'"  |
  #---------
  #|1      |
  #|...    |
  #---------

  # Workaround: Column.alias
  DataFrame.select(lit(1).alias("col1_1"), lit(1).alias("col1_2"))
  # "col1_1", "col1_2"
  ```
- For `Table.merge` and `Table.update`, the session parameters `ERROR_ON_NONDETERMINISTIC_UPDATE` and
  `ERROR_ON_NONDETERMINISTIC_MERGE` must be set to `False`. This means that for multi-joins, one of the matched rows is updated.
- Fully qualified stage names in GET and PUT file operations are not supported. Database and schema names are treated as part of the stage name.
- The `mock_to_char` implementation only supports timestamps in a format that has separators between different time parts.
- `DataFrame.pivot` has a parameter called `values` that allows a pivot to be limited to specific values. Only statistically
  defined values can be used at this time. Values that are provided using a subquery will raise an error.
- Creating a `DataFrame` from a pandas `DataFrame` that contains a timestamp with timezone information is not supported.

For any issues not mentioned in this list, check the [latest list of open issues](https://github.com/snowflakedb/snowpark-python/issues?q=is%3Aopen+is%3Aissue+label%3A%22local+testing%22), or
[create a bug report](https://github.com/snowflakedb/snowpark-python/issues/new/choose) in the `snowpark-python` GitHub repository.
