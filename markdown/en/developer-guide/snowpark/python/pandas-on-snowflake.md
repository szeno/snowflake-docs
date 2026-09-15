# pandas on Snowflake

pandas on Snowflake lets you run your pandas code directly on your data in Snowflake.
By simply changing the import statement and a few lines of code, you can get the familiar
pandas experience to develop robust pipelines, while seamlessly benefiting from Snowflake’s performance and scalability as your pipelines scale.

pandas on Snowflake intelligently determines whether to run pandas code locally or use the Snowflake engine to scale and enhance performance through [Hybrid execution](#label-pandas-hybrid-execution). When working with large datasets in Snowflake, it runs workloads natively in Snowflake through transpilation to SQL, enabling it to take advantage of parallelization and the data governance and security benefits of Snowflake.

pandas on Snowflake is delivered through the Snowpark pandas API as part of the [Snowpark Python library](/developer-guide/snowpark/python/index), which enables scalable data processing of Python code within the Snowflake platform.

## Benefits of using pandas on Snowflake

- **Meeting Python developers where they are:** pandas on Snowflake offers a familiar interface to Python developers by providing a
  pandas-compatible layer that can run natively in Snowflake.
- **Scalable distributed pandas:** pandas on Snowflake bridges the convenience of pandas with the scalability of Snowflake by leveraging existing query optimization techniques in Snowflake. Minimal code rewrites are required, simplifying the migration journey, so you can seamlessly move from prototype to production.
- **No additional compute infrastructure to manage and tune:** pandas on Snowflake leverages the Snowflake’s powerful compute engine, so you do not need to set
  up or manage any additional compute infrastructure.

## Getting started with pandas on Snowflake

Note

For a hands-on example of how to use pandas on Snowflake, check out this [Notebook](https://github.com/Snowflake-Labs/snowflake-python-recipes/blob/main/pandas%20on%20Snowflake%20101/pandas%20on%20Snowflake%20101.ipynb) and watch this [video](https://www.youtube.com/watch?v=p9eX0QQGiZE).

To install pandas on Snowflake, you can use conda or pip to install the package. For detailed instructions, see [Installation](#label-snowpark-pandas-installation).

Copy code

```
pip install "snowflake-snowpark-python[modin]"
```

Once pandas on Snowflake is installed, instead of importing pandas as `import pandas as pd`, use the following two lines:

Copy code

```
import modin.pandas as pd
import snowflake.snowpark.modin.plugin
```

Here is an example of how you can start using pandas on Snowflake through the pandas on Snowpark Python library with Modin:

Copy code

```
import modin.pandas as pd
import snowflake.snowpark.modin.plugin

# Create a Snowpark session with a default connection.
from snowflake.snowpark.session import Session
session = Session.builder.create()

# Create a Snowpark pandas DataFrame from existing Snowflake table
df = pd.read_snowflake('SNOWFALL')

# Inspect the DataFrame
df
```

```
      DAY  LOCATION  SNOWFALL
0       1  Big Bear       8.0
1       2  Big Bear      10.0
2       3  Big Bear       NaN
3       1     Tahoe       3.0
4       2     Tahoe       NaN
5       3     Tahoe      13.0
6       1  Whistler       NaN
7  Friday  Whistler      40.0
8       3  Whistler      25.0
```

Copy code

```
# In-place point update to fix data error.
df.loc[df["DAY"]=="Friday","DAY"]=2

# Inspect the columns after update.
# Note how the data type is updated automatically after transformation.
df["DAY"]
```

```
0    1
1    2
2    3
3    1
4    2
5    3
6    1
7    2
8    3
Name: DAY, dtype: int64
```

Copy code

```
# Drop rows with null values.
df.dropna()
```

```
  DAY  LOCATION  SNOWFALL
0   1  Big Bear       8.0
1   2  Big Bear      10.0
3   1     Tahoe       3.0
5   3     Tahoe      13.0
7   2  Whistler      40.0
8   3  Whistler      25.0
```

Copy code

```
# Compute the average daily snowfall across locations.
df.groupby("LOCATION").mean()["SNOWFALL"]
```

```
LOCATION
Big Bear     9.0
Tahoe        8.0
Whistler    32.5
Name: SNOWFALL, dtype: float64
```

`read_snowflake` supports reading from Snowflake views, dynamic tables, Iceberg tables, and more. You can also pass in a SQL query directly and get back a pandas on Snowflake DataFrame, making it easy to move seamlessly between SQL and pandas on Snowflake.

Copy code

```
summary_df = pd.read_snowflake("SELECT LOCATION, AVG(SNOWFALL) AS avg_snowfall FROM SNOWFALL GROUP BY LOCATION")
summary_df
```

## How hybrid execution works

Note

Starting with Snowpark Python version 1.40.0, hybrid execution is enabled by default when using pandas on Snowflake.

pandas on Snowflake uses hybrid execution to determine whether to run pandas code locally or use the Snowflake engine to scale and enhance performance. This allows you to continue writing familiar pandas code to develop robust pipelines, without having to think about the most optimal and efficient way to run your code, while seamlessly benefiting from Snowflake’s performance and scalability as your pipelines scale.

![hybrid execution](/static/images/snowpark-hybrid-execution.png)

**Example 1**: Create a small, 11-row DataFrame inline. With hybrid execution, Snowflake selects local, in-memory pandas backend for executing the operation:

Copy code

```
# Create a basic dataframe with 11 rows
df = pd.DataFrame([
    ("New Year's Day", "2025-01-01"),
    ("Martin Luther King Jr. Day", "2025-01-20"),
    ("Presidents' Day", "2025-02-17"),
    ("Memorial Day", "2025-05-26"),
    ("Juneteenth National Independence Day", "2025-06-19"),
    ("Independence Day", "2025-07-04"),
    ("Labor Day", "2025-09-01"),
    ("Columbus Day", "2025-10-13"),
    ("Veterans Day", "2025-11-11"),
    ("Thanksgiving Day", "2025-11-27"),
    ("Christmas Day", "2025-12-25")
], columns=["Holiday", "Date"])
# Print out the backend used for this dataframe
df.get_backend()
# >> Output: 'Pandas'
```

**Example 2**: Seed a table with 10 million rows of transactions

Copy code

```
# Create a 10M row table in Snowflake and populate with sythentic data
session.sql('''CREATE OR REPLACE TABLE revenue_transactions (Transaction_ID STRING, Date DATE, Revenue FLOAT);''').collect()
session.sql('''SET num_days = (SELECT DATEDIFF(DAY, '2024-01-01', CURRENT_DATE));''').collect()
session.sql('''INSERT INTO revenue_transactions (Transaction_ID, Date, Revenue) SELECT UUID_STRING() AS Transaction_ID, DATEADD(DAY, UNIFORM(0, $num_days, RANDOM()), '2024-01-01') AS Date, UNIFORM(10, 1000, RANDOM()) AS Revenue FROM TABLE(GENERATOR(ROWCOUNT => 10000000));''').collect()

# Read Snowflake table as Snowpark pandas dataframe
df_transactions = pd.read_snowflake("REVENUE_TRANSACTIONS")
```

You can see that the table leverages Snowflake as the backend since this is a large table that resides in Snowflake.

Copy code

```
print(f"The dataset size is {len(df_transactions)} and the data is located in {df_transactions.get_backend()}.")
# >> Output: The dataset size is 10000000 and the data is located in Snowflake.

#Perform some operations on 10M rows with Snowflake
df_transactions["DATE"] = pd.to_datetime(df_transactions["DATE"])
df_transactions.groupby("DATE").sum()["REVENUE"]
```

**Example 3**: Filter data and perform a `groupby` aggregation resulting in 7 rows of data.

When data is filtered, Snowflake implicitly recognizes the backend choice of engine changes from Snowflake to pandas, since the output is only 7 rows of data.

Copy code

```
# Filter to data in last 7 days
df_transactions_filter1 = df_transactions[(df_transactions["DATE"] >= pd.Timestamp.today().date() - pd.Timedelta('7 days')) & (df_transactions["DATE"] < pd.Timestamp.today().date())]

# Since filter is not yet evaluated, data stays in Snowflake
assert df_transactions_filter1.get_backend() == "Snowflake"
# After groupby operation, result is transferred from Snowflake to Pandas
df_transactions_filter1.groupby("DATE").sum()["REVENUE"]
```

## Notes and limitations

- The DataFrame type will always be `modin.pandas.DataFrame/Series/etc` even when the backend changes, to ensure interoperability/compatibility with downstream code.
- To determine what backend to use, Snowflake sometimes uses an estimate of the row size instead of computing the exact length of the DataFrame at each step. This means that Snowflake may not always switch to the optimal backend immediately after an operation when the dataset gets larger/smaller (e.g. filter, aggregation).
- When there is an operation that combines two or more DataFrames across different backends, Snowflake determines where to move the data based on the lowest data transfer cost.
- Filter operations may not result in the movement of data, because Snowflake may not be able to estimate the size of the underlying filtered data.
- Any DataFrames comprised of in-memory Python data will use the pandas backend, such as the following:

  Copy code

  ```
  pd.DataFrame([1])
  ```

  Copy code

  ```
  pd.DataFrame(pandas.DataFrame([1]))
  ```

  Copy code

  ```
  pd.Series({'a': [4]})
  ```

  An empty DataFrame:

  Copy code

  ```
  pd.DataFrame()
  ```
- DataFrames will automatically move from the Snowflake engine to the pandas engine on a limited set of operations. These operations include `df.apply`, `df.plot`, `df.iterrows`, `df.itertuples`, `series.items`, and reduction operations where the size of the data is guaranteed to be smaller. Not all operations are points where data migration can occur.
- Hybrid execution does not automatically move a DataFrame from the pandas engine back to Snowflake, except in cases where an operation like `pd.concat` acts on multiple DataFrames.

## When you should use pandas on Snowflake

You should use pandas on Snowflake if any of the following is true:

- You are familiar with the pandas API and the broader PyData ecosystem.
- You work on a team with others who are familiar with pandas and want to collaborate on the same codebase.
- You have existing code written in pandas.
- You prefer more accurate code completion from AI-based copilot tools.

For more information, see [Snowpark DataFrames vs Snowpark pandas DataFrame: Which should I choose?](/developer-guide/snowpark/python/working-with-dataframes#label-compare-pandas-dataframes)

## Using pandas on Snowflake with Snowpark DataFrames

The pandas on Snowflake and DataFrame API is highly interoperable, so you can build a pipeline that leverages both APIs. For more information, see [Snowpark DataFrames vs Snowpark pandas DataFrame: Which should I choose?](/developer-guide/snowpark/python/working-with-dataframes#label-compare-pandas-dataframes)

You can use the following operations to do conversions between Snowpark DataFrames and Snowpark pandas DataFrames:

| Operation | Input | Output |
| --- | --- | --- |
| [to\_snowpark\_pandas](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrame.to_snowpark_pandas) | Snowpark DataFrame | Snowpark pandas DataFrame |
| [to\_snowpark](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/modin/pandas_api/modin.pandas.to_snowpark) | Snowpark pandas DataFrame or Snowpark pandas Series | Snowpark DataFrame |

Expand

Show lessSee more

## How pandas on Snowflake compares to native pandas

pandas on Snowflake and native pandas have similar DataFrame APIs with matching signatures and similar semantics.
pandas on Snowflake provides the same API signature as native pandas and provides scalable computation with Snowflake.
pandas on Snowflake respects the semantics described in the native pandas documentation as much as possible, but it uses the Snowflake
computation and type system. However, when native pandas executes on a client machine, it uses the Python computation and type system.
For information about the type mapping between pandas on Snowflake and Snowflake, see
[Data types](#label-snowpark-pandas-data-types).

Starting with Snowpark Python 1.40.0, pandas on Snowflake is best used with data which is already in Snowflake. To convert between native pandas and pandas on Snowflake type, use the following operations:

| Operation | Input | Output |
| --- | --- | --- |
| [to\_pandas](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/pandas_api/snowflake.snowpark.modin.pandas.to_pandas) | Snowpark pandas DataFrame | Native pandas DataFrame - Materialize all data to the local environment. If the dataset is large, this may result in an out-of-memory error. |
| [pd.DataFrame(…)](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/pandas_api/snowflake.snowpark.modin.pandas.DataFrame) | Native pandas DataFrame, raw data, Snowpark pandas object | Snowpark pandas DataFrame |

Expand

Show lessSee more

### Execution environment

- `pandas`: Operates on a single machine and processes in-memory data.
- `pandas on Snowflake`: Integrates with Snowflake, which allows for distributed computing across a cluster of machines for large datasets, while leveraging in memory pandas for processing small datasets. This integration enables handling of much larger datasets that exceed the memory capacity of a single machine. Note that using the Snowpark
  pandas API requires a connection to Snowflake.

### Lazy versus eager evaluation

- `pandas`: Executes operations immediately and materializes results fully in memory after each operation. This eager
  evaluation of operations might lead to increased memory pressure because data must be moved extensively within a machine.
- `pandas on Snowflake`: Provides the same API experience as pandas. It mimics the eager evaluation model of pandas, but internally
  builds a lazily-evaluated query graph to enable optimization across operations.

  Fusing and transpiling operations through a query graph enables additional optimization opportunities for the underlying distributed
  Snowflake compute engine, which decreases both cost and end-to-end pipeline runtime compared to running pandas directly within Snowflake.

  Note

  I/O-related APIs and APIs whose return value is not a Snowpark pandas object (that is, `DataFrame`, `Series` or `Index`) always evaluate eagerly. For example:

  - `read_snowflake`
  - `to_snowflake`
  - `to_pandas`
  - `to_dict`
  - `to_list`
  - `__repr__`
  - The dunder method, `__array__` which can be called automatically by some third-party libraries such as scikit-learn.
    Calls to this method will materialize results to the local machine.

### Data source and storage

- `pandas`: Supports the various readers and writers listed in the pandas documentation in
  [IO tools (text, CSV, HDF5, …)](https://pandas.pydata.org/docs/user_guide/io.html).
- `pandas on Snowflake`: Can read and write from Snowflake tables and read local or staged CSV, JSON, or Parquet files.
  For more information, see [IO (Read and Write)](#label-snowpark-pandas-io-examples).

### Data types

- `pandas`: Has a rich set of data types, such as integers, floats, strings, `datetime` types, and categorical types. It also
  supports user-defined data types. Data types in pandas are typically derived from the underlying data and are enforced strictly.
- `pandas on Snowflake`: Is constrained by Snowflake type system, which maps pandas objects to SQL by translating the pandas data types to the SQL types in Snowflake. A majority
  of pandas types have a natural equivalent in Snowflake, but the mapping is not always one to one. In some cases, multiple pandas types
  are mapped to the same SQL type.

The following table lists the type mappings between pandas and Snowflake SQL:

| pandas type | Snowflake type |
| --- | --- |
| All signed/unsigned integer types, including pandas extended integer types | NUMBER(38, 0) |
| All float types, including pandas extended float data types | FLOAT |
| `bool`, `BooleanDtype` | BOOLEAN |
| `str`, `StringDtype` | STRING |
| `datetime.time` | TIME |
| `datetime.date` | DATE |
| All timezone-naive `datetime` types | TIMESTAMP\_NTZ |
| All timezone-aware `datetime` types | TIMESTAMP\_TZ |
| `list`, `tuple`, `array` | ARRAY |
| `dict`, `json` | MAP |
| Object column with mixed data types | VARIANT |
| Timedelta64[ns] | NUMBER(38, 0) |

Expand

Show lessSee more

Note

Categorical, period, interval, sparse, and user-defined data types are not supported. Timedelta is only supported on the pandas on Snowpark client today. When writing Timedelta back to Snowflake, it will be stored as Number type.

The following table provides the mapping of Snowflake SQL types back to pandas on Snowflake types using `df.dtypes`:

| Snowflake type | pandas on Snowflake type (`df.dtypes`) |
| --- | --- |
| NUMBER (`scale = 0`) | `int64` |
| NUMBER (`scale > 0`), REAL | `float64` |
| BOOLEAN | `bool` |
| STRING, TEXT | `object (str)` |
| VARIANT, BINARY, GEOMETRY, GEOGRAPHY | `object` |
| ARRAY | `object (list)` |
| OBJECT | `object (dict)` |
| TIME | `object (datetime.time)` |
| TIMESTAMP, TIMESTAMP\_NTZ, TIMESTAMP\_LTZ, TIMESTAMP\_TZ | `datetime64[ns]` |
| DATE | `object (datetime.date)` |

Expand

Show lessSee more

When you convert from the Snowpark pandas DataFrame to the native pandas DataFrame with `to_pandas()`, the native pandas DataFrame will
have refined data types compared to the pandas on Snowflake types, which are compatible with the [SQL-Python Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-python-data-type-mappings) for
functions and procedures.

### Casting and type inference

- `pandas`: Relies on [NumPy](https://numpy.org/) and by default follows the NumPy and Python type system for implicit type casting
  and inference. For example, it treats booleans as integer types, so `1 + True` returns `2`.
- `pandas on Snowflake`: Maps NumPy and Python types to Snowflake types according to the preceding table, and uses the underlying
  Snowflake type system for implicit [type casting and inference](/sql-reference/data-type-conversion). For example, in accordance
  with the [Logical data types](/sql-reference/data-types-logical), it does not implicitly convert booleans to integer types, so `1 + True` results in a
  type conversion error.

### Null value handling

- `pandas`: In pandas versions 1.x, pandas was flexible when
  [handling missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html#values-considered-missing), so it treated all of
  Python `None`, `np.nan`, `pd.NaN`, `pd.NA`, and `pd.NaT` as missing values.
  In later versions of pandas (2.2.x) these values are treated as different values.
- `pandas on Snowflake`: Adopts a similar approach to earlier pandas versions that treats all of the preceding values listed as missing values.
  Snowpark reuses `NaN`, `NA`, and `NaT` from pandas. But note that all these missing values are treated interchangeably and stored as SQL NULL in the Snowflake table.

### Offset/frequency aliases

- `pandas`: Date offsets in pandas changed in version 2.2.1. The single-letter aliases `'M'`, `'Q'`, `'Y'`, and others have been deprecated in favor of two-letter offsets.
- `pandas on Snowflake`: Exclusively uses the new offsets described in the [pandas time series documentation](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects).

## Install the pandas on Snowflake library

**Prerequisites**

The following package versions are required:

- Python 3.9 (deprecated), 3.10, 3.11, 3.12 or 3.13
- Modin version 0.32.0
- pandas version 2.2.\*

Tip

To use pandas on Snowflake in Snowflake Notebooks, see the setup instructions in [pandas on Snowflake in notebooks](/user-guide/ui-snowsight/notebooks-use-with-snowflake#label-notebooks-snowpark-pandas).

To install pandas on Snowflake in your development environment, follow these steps:

1. Change to your project directory and activate your Python virtual environment.

   Note

   The API is under active development, so we recommend installing it in a Python virtual environment instead of
   system-wide. This practice allows each project you create to use a specific version, which insulates you from changes
   in future versions.

   You can create a Python virtual environment for a particular Python version by using tools like
   [Anaconda](https://www.anaconda.com/),
   [Miniconda](https://docs.conda.io/en/latest/miniconda.html), or
   [virtualenv](https://docs.python.org/3/tutorial/venv.html).

   For example, to use conda to create a Python 3.12 virtual environment, run these commands:

   Copy code

   ```
   conda create --name snowpark_pandas python=3.12
   conda activate snowpark_pandas
   ```

   Note

   If you previously installed an older version of pandas on Snowflake using Python 3.9 and pandas 1.5.3, you will need to upgrade your Python and pandas
   versions as described above. Follow the steps to create a new environment with Python 3.10 to 3.13.
2. Install the Snowpark Python library with Modin:

   Copy code

   ```
   pip install "snowflake-snowpark-python[modin]"
   ```

   or

   Copy code

   ```
   conda install snowflake-snowpark-python modin==0.28.1
   ```

> Note
>
> Confirm that `snowflake-snowpark-python` version 1.17.0 or later is installed.

## Authenticating to Snowflake

Before using pandas on Snowflake, you must establish a session with the Snowflake database.
You can use a config file to choose the connection parameters for your session, or you can enumerate them in your code.
For more information, see [Creating a Session for Snowpark Python](/developer-guide/snowpark/python/creating-session#label-snowpark-python-creating-session).
If a unique active Snowpark Python session exists, pandas on Snowflake will automatically use it. For example:

Copy code

```
import modin.pandas as pd
import snowflake.snowpark.modin.plugin
from snowflake.snowpark import Session

CONNECTION_PARAMETERS = {
    'account': '<myaccount>',
    'user': '<myuser>',
    'password': '<mypassword>',
    'role': '<myrole>',
    'database': '<mydatabase>',
    'schema': '<myschema>',
    'warehouse': '<mywarehouse>',
}
session = Session.builder.configs(CONNECTION_PARAMETERS).create()

# pandas on Snowflake will automatically pick up the Snowpark session created above.
# It will use that session to create new DataFrames.
df = pd.DataFrame([1, 2])
df2 = pd.read_snowflake('CUSTOMER')
```

The `pd.session` is a Snowpark session, so you can do anything with it that you can do with any other Snowpark session. For example, you can use it to execute an arbitrary SQL query,
which results in a Snowpark DataFrame as per the [Session API](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.Session.sql), but note that
the result is a Snowpark DataFrame, not a Snowpark pandas DataFrame.

Copy code

```
# pd.session is the session that pandas on Snowflake is using for new DataFrames.
# In this case it is the same as the Snowpark session that we've created.
assert pd.session is session

# Run SQL query with returned result as Snowpark DataFrame
snowpark_df = pd.session.sql('select * from customer')
snowpark_df.show()
```

Alternatively, you can configure your Snowpark connection parameters in a [configuration file](/developer-guide/python-connector/python-connector-connect#label-python-connection-toml).
This eliminates the need to enumerate connection parameters in your code, which allows you to write your pandas on Snowflake code almost as you would normally write pandas code.

1. Create a configuration file located at `~/.snowflake/connections.toml` that looks something like this:

   Copy code

   ```
   default_connection_name = "default"

   [default]
   account = "<myaccount>"
   user = "<myuser>"
   password = "<mypassword>"
   role="<myrole>"
   database = "<mydatabase>"
   schema = "<myschema>"
   warehouse = "<mywarehouse>"
   ```
2. To create a session using these credentials, use `snowflake.snowpark.Session.builder.create()`:

   Copy code

   ```
   import modin.pandas as pd
   import snowflake.snowpark.modin.plugin
   from snowflake.snowpark import Session

   # Session.builder.create() will create a default Snowflake connection.
   Session.builder.create()
   # create a DataFrame.
   df = pd.DataFrame([[1, 2], [3, 4]])
   ```

You can also create multiple Snowpark sessions, then assign one of them to pandas on Snowflake. pandas on Snowflake only uses one session, so you have to explicitly assign one
of the sessions to pandas on Snowflake with `pd.session = pandas_session`:

Copy code

```
import modin.pandas as pd
import snowflake.snowpark.modin.plugin
from snowflake.snowpark import Session

pandas_session = Session.builder.configs({"user": "<user>", "password": "<password>", "account": "<account1>"}).create()
other_session = Session.builder.configs({"user": "<user>", "password": "<password>", "account": "<account2>"}).create()
pd.session = pandas_session
df = pd.DataFrame([1, 2, 3])
```

The following example shows that trying to use pandas on Snowflake when there is no active Snowpark session will raise a `SnowparkSessionException` with an
error like “pandas on Snowflake requires an active snowpark session, but there is none.” After you create a session, you can use pandas on Snowflake. For example:

Copy code

```
import modin.pandas as pd
import snowflake.snowpark.modin.plugin

df = pd.DataFrame([1, 2, 3])
```

The following example shows that trying to use pandas on Snowflake when there are multiple active Snowpark sessions will cause
a `SnowparkSessionException` with a message like, “There are multiple active snowpark sessions, but you need to choose one for pandas on Snowflake.”

Copy code

```
import modin.pandas as pd
import snowflake.snowpark.modin.plugin
from snowflake.snowpark import Session

pandas_session = Session.builder.configs({"user": "<user>", "password": "<password>", "account": "<account1>"}).create()
other_session = Session.builder.configs({"user": "<user>", "password": "<password>", "account": "<account2>"}).create()
df = pd.DataFrame([1, 2, 3])
```

Note

You must set the session used for a new pandas on Snowflake DataFrame or Series via `modin.pandas.session`.
However, joining or merging DataFrames created with different sessions is not supported, so you should avoid repeatedly setting different sessions
and creating DataFrames with different sessions in a workflow.

## API reference

See [the pandas on Snowflake API reference](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/index) for the full list of currently implemented APIs and methods available.

For a full list of supported operations, see the following tables in pandas on Snowflake reference:

- [pandas general utilities supported APIs](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/general_supported)
- [Series supported APIs](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/series_supported)
- [DataFrame supported APIs](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/dataframe_supported)
- [Index supported APIs](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/index_supported)
- [Windows supported APIs](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/window_supported)
- [GroupBy supported APIs](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/groupby_supported)
- [Resampler supported APIs](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/resampling_supported)
- [DatetimeProperties supported APIs](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/series_dt_supported)
- [StringMethods supported APIs](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/supported/series_str_supported)

## APIs and configuration parameter for hybrid execution

Hybrid execution uses a combination of the dataset size estimate and the operations being applied to the DataFrame to determine the choice of backend. In general, datasets under 100k rows will tend to use local pandas; those over 100k rows will tend to use Snowflake, unless the dataset is loaded from local files.

### Configuring transfer costs

To change the default switching threshold to another row limit value, you can modify the environment variable before initializing a DataFrame:

Copy code

```
# Change row transfer threshold to 500k
from modin.config.envvars import SnowflakePandasTransferThreshold
SnowflakePandasTransferThreshold.put(500_000)
```

Setting this value will penalize transferring rows out of Snowflake.

### Configuring local execution limits

Once a DataFrame is local it will generally stay local unless there is a need to move it back to Snowflake for a merge, but there is an upper bound considered for the maximum size of data than can be processed locally. Currently this boundary is 10M rows.

### Checking and setting backend

To check the current backend of choice, you can use the [df.get\_backend()](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/pandas_api/modin.pandas.DataFrame.get_backend#modin.pandas.DataFrame.get_backend) command, which returns `Pandas` for local execution, or `Snowflake` for pushdown execution.

To set the current backend of choice with either `set_backend` or its alias `move_to`:

Copy code

```
df_local = df.set_backend('Pandas')
```

Copy code

```
df_local = df.move_to('Pandas')
```

Copy code

```
df_snow = df.set_backend('Snowflake')
```

You can also set the backend in place:

Copy code

```
df.set_backend('Pandas', inplace=True)
```

To inspect and display information about *why* data was moved:

Copy code

```
pd.explain_switch()
```

### Manual override backend selection by pinning backend

By default, Snowflake automatically chooses the best backend for a given DataFrame and operation. If you would like to override the automatic engine selection, you can disable automatic switching on an object and all resulting data produced by it, using the [pin\_backend()](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/pandas_api/modin.pandas.DataFrame.pin_backend#modin.pandas.DataFrame.pin_backend) method:

Copy code

```
pinned_df_snow = df.move_to('Snowflake').pin_backend()
```

To re-enable automatic backend switching, call [unpin\_backend()](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/pandas_api/modin.pandas.DataFrame.unpin_backend#modin.pandas.DataFrame.unpin_backend):

Copy code

```
unpinned_df_snow = pinned_df_snow.unpin_backend()
```

## Using Snowpark pandas in Snowflake notebooks

To use pandas on Snowflake in Snowflake notebooks, see [pandas on Snowflake in notebooks](/user-guide/ui-snowsight/notebooks-use-with-snowflake#label-notebooks-snowpark-pandas).

## Using Snowpark pandas in Python Worksheets

To use Snowpark pandas, you need to install Modin by selecting `modin` from **Packages** in the Python Worksheet environment.

You can select the Return type of the Python function under **Settings > Return type**. By default, this is set as a Snowpark table. To display the Snowpark pandas DataFrame as a result, you can convert a Snowpark pandas DataFrame to a Snowpark DataFrame by calling [to\_snowpark()](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/modin/pandas_api/modin.pandas.to_snowpark). No I/O cost will be incurred in this conversion.

Here is an example of using Snowpark pandas with Python Worksheets:

Copy code

```
import snowflake.snowpark as snowpark

def main(session: snowpark.Session):
  import modin.pandas as pd
  import snowflake.snowpark.modin.plugin

  df = pd.DataFrame([[1, 'Big Bear', 8],[2, 'Big Bear', 10],[3, 'Big Bear', None],
                  [1, 'Tahoe', 3],[2, 'Tahoe', None],[3, 'Tahoe', 13],
                  [1, 'Whistler', None],['Friday', 'Whistler', 40],[3, 'Whistler', 25]],
                  columns=["DAY", "LOCATION", "SNOWFALL"])

  # Print a sample of the dataframe to standard output.
  print(df)

  snowpark_df = df.to_snowpark(index=None)
  # Return value will appear in the Results tab.
  return snowpark_df
```

## Using pandas on Snowflake in stored procedures

You can use pandas on Snowflake in a [stored procedure](/developer-guide/stored-procedure/python/procedure-python-overview) to build a data pipeline and schedule the execution of the stored procedure with [tasks](/user-guide/tasks-intro).

Here is how you can create a stored procedure using SQL:

Copy code

```
CREATE OR REPLACE PROCEDURE run_data_transformation_pipeline_sp()
RETURNS VARCHAR
LANGUAGE PYTHON
RUNTIME_VERSION = 3.12
PACKAGES = ('snowflake-snowpark-python','modin')
HANDLER='data_transformation_pipeline'
AS $$
def data_transformation_pipeline(session):
  import modin.pandas as pd
  import snowflake.snowpark.modin.plugin
  from datetime import datetime
  # Create a Snowpark pandas DataFrame with sample data.
  df = pd.DataFrame([[1, 'Big Bear', 8],[2, 'Big Bear', 10],[3, 'Big Bear', None],
                    [1, 'Tahoe', 3],[2, 'Tahoe', None],[3, 'Tahoe', 13],
                    [1, 'Whistler', None],['Friday', 'Whistler', 40],[3, 'Whistler', 25]],
                      columns=["DAY", "LOCATION", "SNOWFALL"])
  # Drop rows with null values.
  df = df.dropna()
  # In-place point update to fix data error.
  df.loc[df["DAY"]=="Friday","DAY"]=2
  # Save Results as a Snowflake Table
  timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
  save_path = f"OUTPUT_{timestamp}"
  df.to_snowflake(name=save_path, if_exists="replace", index=False)
  return f'Transformed DataFrame saved to {save_path}.'
$$;
```

Here is how you can create a stored procedure using the [Snowflake Python API](/developer-guide/snowflake-python-api/snowflake-python-managing-functions-procedures#label-snowflake-python-procedures):

Copy code

```
from snowflake.snowpark.context import get_active_session
session = get_active_session()

from snowflake.snowpark import Session

def data_transformation_pipeline(session: Session) -> str:
  import modin.pandas as pd
  import snowflake.snowpark.modin.plugin
  from datetime import datetime
  # Create a Snowpark pandas DataFrame with sample data.
  df = pd.DataFrame([[1, 'Big Bear', 8],[2, 'Big Bear', 10],[3, 'Big Bear', None],
                     [1, 'Tahoe', 3],[2, 'Tahoe', None],[3, 'Tahoe', 13],
                     [1, 'Whistler', None],['Friday', 'Whistler', 40],[3, 'Whistler', 25]],
                      columns=["DAY", "LOCATION", "SNOWFALL"])
  # Drop rows with null values.
  df = df.dropna()
  # In-place point update to fix data error.
  df.loc[df["DAY"]=="Friday","DAY"]=2
  # Save Results as a Snowflake Table
  timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
  save_path = f"OUTPUT_{timestamp}"
  df.to_snowflake(name=save_path, if_exists="replace", index=False)
  return f'Transformed DataFrame saved to {save_path}.'

dt_pipeline_sproc = session.sproc.register(name="run_data_transformation_pipeline_sp",
                             func=data_transformation_pipeline,
                             replace=True,
                             packages=['modin', 'snowflake-snowpark-python'])
```

To call the stored procedure, you can run `dt_pipeline_sproc()` in Python or `CALL run_data_transformation_pipeline_sp()` in SQL.

## Using pandas on Snowflake with third-party libraries

pandas is commonly used with third-party library APIs for visualization and machine learning applications. pandas on Snowflake is interoperable with most of these libraries, so they can be used without converting to pandas DataFrames explicitly. However, note that distributed execution is not often supported in most third-party libraries except in limited use cases. Therefore, this can lead to slower performance on large datasets.

### Supported third-party libraries

The libraries listed below accept pandas on Snowflake DataFrames as input, but not all their methods have been tested. For an in-depth interoperability status on an API level, see [Interoperability with third party libraries](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/interoperability).

- Plotly
- Altair
- Seaborn
- Matplotlib
- Numpy
- Scikit-learn
- XGBoost
- NLTK
- Streamlit

pandas on Snowflake currently has limited compatibility for certain [NumPy](https://numpy.org/) and [Matplotlib](https://matplotlib.org/) APIs, such as distributed implementation for `np.where` and interoperability with `df.plot`. Converting Snowpark pandas DataFrames via `to_pandas()` when working with these third-party libraries will avoid multiple I/O calls.

Here is an example with [Altair](https://altair-viz.github.io/) for visualization and [scikit-learn](https://scikit-learn.org/stable/) for machine learning.

Copy code

```
# Create a Snowpark session with a default connection.
session = Session.builder.create()

train = pd.read_snowflake('TITANIC')

train[['Pclass', 'Parch', 'Sex', 'Survived']].head()
```

```
    Pclass  Parch     Sex       Survived
0       3      0     male               0
1       1      0   female               1
2       3      0   female               1
3       1      0   female               1
4       3      0     male               0
```

Copy code

```
import altair as alt

survived_per_age_plot = alt.Chart(train).mark_bar(
).encode(
    x=alt.X('Age', bin=alt.Bin(maxbins=25)),
    y='count()',
    column='Survived:N',
    color='Survived:N',
).properties(
    width=300,
    height=300
).configure_axis(
    grid=False
)
```

![survived_per_age_plot](/static/images/snowpark-1.png)

You can also analyze survival based on gender.

Copy code

```
# Perform groupby aggregation with Snowpark pandas
survived_per_gender = train.groupby(['Sex','Survived']).agg(count_survived=('Survived', 'count')).reset_index()

survived_per_gender_pandas = survived_per_gender
survived_per_gender_plot = alt.Chart(survived_per_gender).mark_bar().encode(
   x='Survived:N',
   y='Survived_Count',
   color='Sex',
   column='Sex'
).properties(
   width=200,
   height=200
).configure_axis(
   grid=False
)
```

![survived_per_gender_plot](/static/images/snowpark-2.png)

You can now use scikit-learn to train a simple model.

Copy code

```
feature_cols = ['Pclass', 'Parch']
X_pandas = train.loc[:, feature_cols]
y_pandas = train["Survived"]

from sklearn.linear_model import LogisticRegression

logreg = LogisticRegression()
logreg.fit(X_pandas, y_pandas)
y_pred_pandas = logreg.predict(X_pandas)
acc_eval = accuracy_score(y_pandas, y_pred_pandas)
```

Note

For greater performance, we recommend converting to pandas DataFrames via [to\_pandas()](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.21.0/modin/pandas_api/snowflake.snowpark.modin.pandas.to_pandas), particularly when using machine learning libraries such as scikit-learn. The `to_pandas()` function collects all rows, however, so it may be better to reduce the dataframe size first with `sample(frac=0.1)` or `head(10)`.

### Unsupported libraries

When using unsupported third-party libraries with a pandas on Snowflake DataFrame, we recommend converting the pandas on Snowflake DataFrame to a pandas DataFrame by calling [to\_pandas()](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.21.0/modin/pandas_api/snowflake.snowpark.modin.pandas.to_pandas) before passing the DataFrame to the third-party library method.

Note

Calling [to\_pandas()](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.21.0/modin/pandas_api/snowflake.snowpark.modin.pandas.to_pandas) pulls your data out of Snowflake and into memory, so consider that for large datasets and sensitive use cases.

## Using Snowflake Cortex LLM functions with Snowpark pandas

You can use [Snowflake Cortex LLM functions](/user-guide/snowflake-cortex/aisql) via the [Snowpark pandas apply function](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/pandas_api/modin.pandas.DataFrame.apply).

You apply the function with special keyword arguments. Currently, the following Cortex functions are supported:

- [SENTIMENT (SNOWFLAKE.CORTEX)](/sql-reference/functions/sentiment-snowflake-cortex)
- [AI\_SUMMARIZE](/sql-reference/functions/ai_summarize)
- [TRANSLATE](/sql-reference/functions/translate)
- [AI\_CLASSIFY](/sql-reference/functions/ai_classify)
- [AI\_EXTRACT](/sql-reference/functions/ai_extract)

The following example uses the [TRANSLATE](/sql-reference/functions/translate) function across multiple records in a Snowpark pandas DataFrame:

Copy code

```
import modin.pandas as pd
import snowflake.snowpark.modin.plugin

from snowflake.cortex import Translate
content_df = pd.DataFrame(["good morning","hello", "goodbye"], columns=["content"])
result = content_df.apply(Translate, from_language="en", to_language="de")
result["content"]
```

Output:

```
Guten Morgen
Hallo
Auf Wiedersehen
Name: content, dtype: object
```

The following example uses the [SENTIMENT (SNOWFLAKE.CORTEX)](/sql-reference/functions/sentiment-snowflake-cortex) function on a Snowflake table named `reviews`:

Copy code

```
from snowflake.cortex import Sentiment

s = pd.read_snowflake("reviews")["content"]
result = s.apply(Sentiment)
result
```

The following example uses the [AI\_EXTRACT](/sql-reference/functions/ai_extract) to answer a question:

Copy code

```
from snowflake.cortex import ExtractAnswer
content = "The Snowflake company was co-founded by Thierry Cruanes, Marcin Zukowski, and Benoit Dageville in 2012 and is headquartered in Bozeman, Montana."

df = pd.DataFrame([content])
result = df.apply(ExtractAnswer, question="When was Snowflake founded?")
result[0][0][0]["answer"]
```

Output:

```
'2012'
```

Note

The [snowflake-ml-python](https://pypi.org/project/snowflake-ml-python/) package must be installed to use Cortex LLM functions.

## Limitations

pandas on Snowflake has the following limitations:

- pandas on Snowflake provides no guarantee of compatibility with OSS third-party libraries. Starting with version 1.14.0a1, however, Snowpark
  pandas introduces limited compatibility for NumPy, specifically for `np.where` usage. For more information, see
  [NumPy Interoperability](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/numpy).

  When you call third-party library APIs with a Snowpark pandas DataFrame,
  Snowflake recommends that you convert the Snowpark pandas DataFrame to a pandas DataFrame by calling `to_pandas()` before passing the DataFrame to
  the third-party library call. For more information, see [Using pandas on Snowflake with third-party libraries](#label-snowpark-pandas-third-party-libraries).
- pandas on Snowflake is not integrated with [Snowpark ML](/developer-guide/snowflake-ml/overview). When you use Snowpark ML, we recommend that you convert the Snowpark
  pandas DataFrame to a Snowpark DataFrame using [to\_snowpark()](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/modin/pandas_api/modin.pandas.to_snowpark) before calling Snowpark ML.
- Lazy `MultiIndex` objects are not supported. When `MultiIndex` is used, it returns a native pandas `MultiIndex` object,
  which requires pulling all data to the client side.
- Not all pandas APIs have a distributed implementation in pandas on Snowflake, although some are being added. For unsupported APIs,
  `NotImplementedError` is thrown.
  For information about supported APIs, see the API reference documentation.
- pandas on Snowflake provides compatibility with any patch version of pandas 2.2.
- Snowpark pandas cannot be referenced within Snowpark pandas `apply` function. You can only use native pandas inside `apply`.

  - Following is an example:

    Copy code

    ```
    import modin.pandas as pd
    import pandas

    df.apply(lambda row: pandas.to_datetime(f"{row.date} {row.time}"), axis=1)
    ```

## Troubleshooting

This section describes troubleshooting tips for using pandas on Snowflake.

- When troubleshooting, try running the same operation on a native pandas DataFrame (or a sample) to see whether the same error persists.
  This approach might provide hints on how to fix your query. For example:

  Copy code

  ```
  df = pd.DataFrame({"a": [1,2,3], "b": ["x", "y", "z"]})
  # Running this in Snowpark pandas throws an error
  df["A"].sum()
  # Convert a small sample of 10 rows to pandas DataFrame for testing
  pandas_df = df.head(10).to_pandas()
  # Run the same operation. KeyError indicates that the column reference is incorrect
  pandas_df["A"].sum()
  # Fix the column reference to get the Snowpark pandas query working
  df["a"].sum()
  ```
- If you have a long-running notebook opened, note that by default Snowflake sessions time out after the session is idle for 240 minutes (4 hours).
  When the session expires, if you run additional pandas on Snowflake queries, the following message appears: “Authentication token has expired. The user must authenticate again.”
  At this point, you must re-establish the connection to Snowflake. This might cause the loss of any unpersisted session variables.
  For more information about how to configure the session idle timeout parameter, see [Session policies](/user-guide/session-policies#label-session-policy-policies).

## Best practices

This section describes best practices to follow when using pandas on Snowflake.

- Avoid using iterative code patterns, such as `for` loops, `iterrows`, and `iteritems`. Iterative code patterns quickly increase
  the generated query complexity. Let pandas on Snowflake, not the client code, perform the data distribution and computation parallelization. With regard to iterative code patterns, look for operations that can be performed on the whole DataFrame, and use the corresponding operations instead.

Copy code

```
for i in np.arange(0, 50):
  if i % 2 == 0:
    data = pd.concat([data, pd.DataFrame({'A': i, 'B': i + 1}, index=[0])], ignore_index=True)
  else:
    data = pd.concat([data, pd.DataFrame({'A': i}, index=[0])], ignore_index=True)

# Instead of creating one DataFrame per row and concatenating them,
# try to directly create the DataFrame out of the data, like this:

data = pd.DataFrame(
      {
          "A": range(0, 50),
          "B": [i + 1 if i % 2 == 0 else None for i in range(50)],
      },
)
```

- Avoid calling `apply`, `applymap`, and `transform`, which are eventually implemented with
  [UDFs](/developer-guide/udf/python/udf-python-introduction) or
  [UDTFs](/developer-guide/udf/python/udf-python-tabular-functions), which might not be as performant as
  regular SQL queries. If the function applied has an equivalent DataFrame or series operation, use that operation instead.
  For example, instead of `df.groupby('col1').apply('sum')`, directly call `df.groupby('col1').sum()`.
- Call `to_pandas()` before passing the DataFrame or series to a third-party library call. pandas on Snowflake does not provide a
  compatibility guarantee with third-party libraries.
- Use a materialized regular Snowflake table to avoid extra I/O overhead. pandas on Snowflake works on top of a data snapshot that
  only works for regular tables. For other types, including external tables, views, and Apache Iceberg™ tables, a temporary table is
  created before the snapshot is taken, which introduces extra materialization overhead.
- pandas on Snowflake provides fast and zero copy clone capability while creating DataFrames from Snowflake tables using `read_snowflake`.
- Double check the result type before proceeding to other operations, and do explicit type casting with `astype` if needed.

  Due to limited type inference capability, if no type hint is given, `df.apply` will return results of object (variant) type even if the result contains all
  integer values. If other operations require the `dtype` to be `int`, you can do an explicit type casting by calling the
  `astype` method to correct the column type before you continue.
- Avoid calling APIs that require evaluation and materialization unless necessary.

  APIs that don’t return `Series` or `Dataframe` require eager evaluation and materialization to produce the result in the
  correct type. Same for plotting methods. Reduce calls to those APIs to minimize unnecessary evaluations and materialization.
- Avoid calling `np.where(<cond>, <scalar>, n)` on large datasets. The `<scalar>` will be broadcast to a DataFrame
  the size of `<cond>`, which may be slow.
- When working with iteratively built queries, `df.cache_result` can be used to materialize intermediate
  results to reduce the repeated evaluation and improve the latency and reduce complexity of the overall query. For example:

  Copy code

  ```
  df = pd.read_snowflake('pandas_test')
  df2 = pd.pivot_table(df, index='index_col', columns='pivot_col') # expensive operation
  df3 = df.merge(df2)
  df4 = df3.where(df2 == True)
  ```

  In the example above, the query to produce `df2` is expensive to compute and is reused in the creation of both `df3` and `df4`.
  Materializing `df2` into a temporary table (making subsequent operations involving `df2` a table scan instead of a pivot) can reduce the
  overall latency of the code block:

  Copy code

  ```
  df = pd.read_snowflake('pandas_test')
  df2 = pd.pivot_table(df, index='index_col', columns='pivot_col') # expensive operation
  df2.cache_result(inplace=True)
  df3 = df.merge(df2)
  df4 = df3.where(df2 == True)
  ```

## Examples

Here is a code example with pandas operations. We start with a Snowpark pandas DataFrame named `pandas_test`, which contains three
columns: `COL_STR`, `COL_FLOAT`, and `COL_INT`. To view the notebook associated with these examples, see the
[pandas on Snowflake examples in the Snowflake-Labs repository](https://github.com/Snowflake-Labs/sf-samples/blob/main/samples/snowpark-pandas/api-examples/api_examples.ipynb).

Copy code

```
import modin.pandas as pd
import snowflake.snowpark.modin.plugin

from snowflake.snowpark import Session

CONNECTION_PARAMETERS = {
    'account': '<myaccount>',
    'user': '<myuser>',
    'password': '<mypassword>',
    'role': '<myrole>',
    'database': '<mydatabase>',
    'schema': '<myschema>',
    'warehouse': '<mywarehouse>',
}
session = Session.builder.configs(CONNECTION_PARAMETERS).create()

df = pd.DataFrame([['a', 2.1, 1],['b', 4.2, 2],['c', 6.3, None]], columns=["COL_STR", "COL_FLOAT", "COL_INT"])

df
```

```
  COL_STR    COL_FLOAT    COL_INT
0       a          2.1        1.0
1       b          4.2        2.0
2       c          6.3        NaN
```

We save the DataFrame as a Snowflake table named `pandas_test`, which we will use throughout our examples.

Copy code

```
df.to_snowflake("pandas_test", if_exists='replace',index=False)
```

Next, we create a DataFrame from the Snowflake table. We drop the column `COL_INT` and then
save the result back to Snowflake with a column named `row_position`.

Copy code

```
# Create a DataFrame out of a Snowflake table.
df = pd.read_snowflake('pandas_test')

df.shape
```

```
(3, 3)
```

Copy code

```
df.head(2)
```

```
    COL_STR  COL_FLOAT  COL_INT
0         a        2.1        1
1         b        4.2        2
```

Copy code

```
df.dropna(subset=["COL_FLOAT"], inplace=True)

df
```

```
    COL_STR  COL_FLOAT  COL_INT
0         a        2.1        1
1         c        6.3        2
```

Copy code

```
df.shape
```

```
(2, 3)
```

Copy code

```
df.dtypes
```

```
COL_STR       object
COL_FLOAT    float64
COL_INT        int64
dtype: object
```

Copy code

```
# Save the result back to Snowflake with a row_pos column.
df.reset_index(drop=True).to_snowflake('pandas_test2', if_exists='replace', index=True, index_label=['row_pos'])
```

The result is a new table, `pandas_test2`, which looks like this:

```
     row_pos  COL_STR  COL_FLOAT  COL_INT
0          1         a       2.0        1
1          2         b       4.0        2
```

### IO (Read and Write)

Copy code

```
# Reading and writing to Snowflake
df = pd.DataFrame({"fruit": ["apple", "orange"], "size": [3.4, 5.4], "weight": [1.4, 3.2]})
df.to_snowflake("test_table", if_exists="replace", index=False )

df_table = pd.read_snowflake("test_table")

# Generate sample CSV file
with open("data.csv", "w") as f:
    f.write('fruit,size,weight\napple,3.4,1.4\norange,5.4,3.2')
# Read from local CSV file
df_csv = pd.read_csv("data.csv")

# Generate sample JSON file
with open("data.json", "w") as f:
    f.write('{"fruit":"apple", "size":3.4, "weight":1.4},{"fruit":"orange", "size":5.4, "weight":3.2}')
# Read from local JSON file
df_json = pd.read_json('data.json')

# Upload data.json and data.csv to Snowflake stage named @TEST_STAGE
# Read CSV and JSON file from stage
df_csv = pd.read_csv('@TEST_STAGE/data.csv')
df_json = pd.read_json('@TEST_STAGE/data.json')
```

For more information, see [Input/Output](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/io).

### Indexing

Copy code

```
df = pd.DataFrame({"a": [1,2,3], "b": ["x", "y", "z"]})
df.columns
```

```
Index(['a', 'b'], dtype='object')
```

Copy code

```
df.index
```

```
Index([0, 1, 2], dtype='int8')
```

Copy code

```
df["a"]
```

```
0    1
1    2
2    3
Name: a, dtype: int8
```

Copy code

```
df["b"]
```

```
0    x
1    y
2    z
Name: b, dtype: object
```

Copy code

```
df.iloc[0,1]
```

```
'x'
```

Copy code

```
df.loc[df["a"] > 2]
```

```
a  b
2  3  z
```

Copy code

```
df.columns = ["c", "d"]
df
```

```
     c  d
0    1  x
1    2  y
2    3  z
```

Copy code

```
df = df.set_index("c")
df
```

```
   d
c
1  x
2  y
3  z
```

Copy code

```
df.rename(columns={"d": "renamed"})
```

```
    renamed
c
1       x
2       y
3       z
```

### Missing values

Copy code

```
import numpy as np
df = pd.DataFrame([[np.nan, 2, np.nan, 0],
                [3, 4, np.nan, 1],
                [np.nan, np.nan, np.nan, np.nan],
                [np.nan, 3, np.nan, 4]],
                columns=list("ABCD"))
df
```

```
     A    B   C    D
0  NaN  2.0 NaN  0.0
1  3.0  4.0 NaN  1.0
2  NaN  NaN NaN  NaN
3  NaN  3.0 NaN  4.0
```

Copy code

```
df.isna()
```

```
       A      B     C      D
0   True  False  True  False
1  False  False  True  False
2   True   True  True   True
3   True  False  True  False
```

Copy code

```
df.fillna(0)
```

```
     A    B    C    D
0   0.0  2.0  0.0  0.0
1   3.0  4.0  0.0  1.0
2   0.0  0.0  0.0  0.0
3   0.0  3.0  0.0  4.0
```

Copy code

```
df.dropna(how="all")
```

```
     A    B   C    D
0   NaN  2.0 NaN  0.0
1   3.0  4.0 NaN  1.0
3   NaN  3.0 NaN  4.0
```

### Type conversion

Copy code

```
df = pd.DataFrame({"int": [1,2,3], "str": ["4", "5", "6"]})
df
```

```
   int str
0    1   4
1    2   5
2    3   6
```

Copy code

```
df_float = df.astype(float)
df_float
```

```
   int  str
0  1.0  4.0
1  2.0  5.0
2  3.0  6.0
```

Copy code

```
df_float.dtypes
```

```
int    float64
str    float64
dtype: object
```

Copy code

```
pd.to_numeric(df.str)
```

```
0    4.0
1    5.0
2    6.0
Name: str, dtype: float64
```

Copy code

```
df = pd.DataFrame({'year': [2015, 2016],
                'month': [2, 3],
                'day': [4, 5]})
pd.to_datetime(df)
```

```
0   2015-02-04
1   2016-03-05
dtype: datetime64[ns]
```

### Binary operations

Copy code

```
df_1 = pd.DataFrame([[1,2,3],[4,5,6]])
df_2 = pd.DataFrame([[6,7,8]])
df_1.add(df_2)
```

```
    0    1     2
0  7.0  9.0  11.0
1  NaN  NaN   NaN
```

Copy code

```
s1 = pd.Series([1, 2, 3])
s2 = pd.Series([2, 2, 2])
s1 + s2
```

```
0    3
1    4
2    5
dtype: int64
```

Copy code

```
df = pd.DataFrame({"A": [1,2,3], "B": [4,5,6]})
df["A+B"] = df["A"] + df["B"]
df
```

```
   A  B  A+B
0  1  4    5
1  2  5    7
2  3  6    9
```

### Aggregation

Copy code

```
df = pd.DataFrame([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
                [np.nan, np.nan, np.nan]],
                columns=['A', 'B', 'C'])
df.agg(['sum', 'min'])
```

```
        A     B     C
sum  12.0  15.0  18.0
min   1.0   2.0   3.0
```

Copy code

```
df.median()
```

```
A    4.0
B    5.0
C    6.0
dtype: float64
```

### Merge

Copy code

```
df1 = pd.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'],
                    'value': [1, 2, 3, 5]})
df1
```

```
  lkey  value
0  foo      1
1  bar      2
2  baz      3
3  foo      5
```

Copy code

```
df2 = pd.DataFrame({'rkey': ['foo', 'bar', 'baz', 'foo'],
                    'value': [5, 6, 7, 8]})
df2
```

```
  rkey  value
0  foo      5
1  bar      6
2  baz      7
3  foo      8
```

Copy code

```
df1.merge(df2, left_on='lkey', right_on='rkey')
```

```
  lkey  value_x rkey  value_y
0  foo        1  foo        5
1  foo        1  foo        8
2  bar        2  bar        6
3  baz        3  baz        7
4  foo        5  foo        5
5  foo        5  foo        8
```

Copy code

```
df = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3', 'K4', 'K5'],
                'A': ['A0', 'A1', 'A2', 'A3', 'A4', 'A5']})
df
```

```
  key   A
0  K0  A0
1  K1  A1
2  K2  A2
3  K3  A3
4  K4  A4
5  K5  A5
```

Copy code

```
other = pd.DataFrame({'key': ['K0', 'K1', 'K2'],
                    'B': ['B0', 'B1', 'B2']})
df.join(other, lsuffix='_caller', rsuffix='_other')
```

```
  key_caller   A key_other     B
0         K0  A0        K0    B0
1         K1  A1        K1    B1
2         K2  A2        K2    B2
3         K3  A3      None  None
4         K4  A4      None  None
5         K5  A5      None  None
```

### Groupby

Copy code

```
df = pd.DataFrame({'Animal': ['Falcon', 'Falcon','Parrot', 'Parrot'],
               'Max Speed': [380., 370., 24., 26.]})

df
```

```
   Animal  Max Speed
0  Falcon      380.0
1  Falcon      370.0
2  Parrot       24.0
3  Parrot       26.0
```

Copy code

```
df.groupby(['Animal']).mean()
```

```
        Max Speed
Animal
Falcon      375.0
Parrot       25.0
```

For more information, see [GroupBy](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/modin/groupby).

### Pivot

Copy code

```
df = pd.DataFrame({"A": ["foo", "foo", "foo", "foo", "foo",
                        "bar", "bar", "bar", "bar"],
                "B": ["one", "one", "one", "two", "two",
                        "one", "one", "two", "two"],
                "C": ["small", "large", "large", "small",
                        "small", "large", "small", "small",
                        "large"],
                "D": [1, 2, 2, 3, 3, 4, 5, 6, 7],
                "E": [2, 4, 5, 5, 6, 6, 8, 9, 9]})
df
```

```
     A    B      C  D  E
0  foo  one  small  1  2
1  foo  one  large  2  4
2  foo  one  large  2  5
3  foo  two  small  3  5
4  foo  two  small  3  6
5  bar  one  large  4  6
6  bar  one  small  5  8
7  bar  two  small  6  9
8  bar  two  large  7  9
```

Copy code

```
pd.pivot_table(df, values='D', index=['A', 'B'],
                   columns=['C'], aggfunc="sum")
```

```
    C    large  small
A   B
bar one    4.0      5
    two    7.0      6
foo one    4.0      1
    two    NaN      6
```

Copy code

```
df = pd.DataFrame({'foo': ['one', 'one', 'one', 'two', 'two', 'two'],
                'bar': ['A', 'B', 'C', 'A', 'B', 'C'],
                'baz': [1, 2, 3, 4, 5, 6],
                'zoo': ['x', 'y', 'z', 'q', 'w', 't']})
df
```

```
   foo bar  baz zoo
0  one   A    1   x
1  one   B    2   y
2  one   C    3   z
3  two   A    4   q
4  two   B    5   w
5  two   C    6   t
```

## Resources

- [Snowpark pandas API](/developer-guide/snowpark/reference/python/latest/modin/index)
- [Quickstart: Getting Started with pandas on Snowflake](https://quickstarts.snowflake.com/guide/getting_started_with_pandas_on_snowflake/index.html)
- [Quickstart: Data Engineering Pipelines with Snowpark Python](https://quickstarts.snowflake.com/guide/data_engineering_pipelines_with_snowpark_pandas/#0)
