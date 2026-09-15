# Vectorized Python UDFs

This topic introduces vectorized Python UDFs.

## Overview

Vectorized Python UDFs let you define Python functions that receive batches of input rows
as [Pandas DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) and
return batches of results as [Pandas arrays](https://pandas.pydata.org/docs/reference/api/pandas.array.html)
or [Series](https://pandas.pydata.org/docs/reference/series.html).
You call vectorized Python UDFs the same way you call other Python UDFs.

Advantages of using vectorized Python UDFs compared to the default row-by-row processing pattern include:

- The potential for better performance if your Python code operates efficiently on batches of rows.
- Less transformation logic required if you are calling into libraries that operate on Pandas DataFrames or Pandas arrays.

When you use vectorized Python UDFs:

- You do not need to change how you write queries using Python UDFs. All batching is handled by the UDF framework rather than your own code.
- As with non-vectorized UDFs, there is no guarantee of which instances of your handler code will see which batches of input.

## Getting started with vectorized Python UDFs

To create a vectorized Python UDF, use one of the supported mechanisms for annotating your handler function.

### Using the `vectorized` decorator

The `_snowflake` module is exposed to Python UDFs that execute within Snowflake. In your Python code, import the `_snowflake` module,
and use the `vectorized` decorator to specify that your handler expects to receive a Pandas DataFrame by setting the `input` parameter to `pandas.DataFrame`.

Copy code

```
CREATE FUNCTION add_one_to_inputs(x NUMBER(10, 0), y NUMBER(10, 0))
  RETURNS NUMBER(10, 0)
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  PACKAGES = ('pandas')
  HANDLER = 'add_one_to_inputs'
AS $$
import pandas
from _snowflake import vectorized

@vectorized(input=pandas.DataFrame)
def add_one_to_inputs(df):
 return df[0] + df[1] + 1
$$;
```

### Using a function attribute

Rather than importing the \_snowflake module and using the `vectorized` decorator, you can set the special `_sf_vectorized_input` attribute on your handler function.

Copy code

```
CREATE FUNCTION add_one_to_inputs(x NUMBER(10, 0), y NUMBER(10, 0))
  RETURNS NUMBER(10, 0)
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  PACKAGES = ('pandas')
  HANDLER = 'add_one_to_inputs'
AS $$
import pandas

def add_one_to_inputs(df):
 return df[0] + df[1] + 1

add_one_to_inputs._sf_vectorized_input = pandas.DataFrame
$$;
```

## Setting a target batch size

Calls to the Python handler function must execute within a time limit,
which is 180 seconds, and each DataFrame passed as input to the handler function may currently contain
up to a few thousand rows. In order to stay within the time limit, you may want to set the target batch
size for your handler function, which imposes a maximum number of rows per input DataFrame.
Note that setting a larger value does not guarantee that Snowflake will encode batches with the specified number of rows.
You can set the target batch size using either the `vectorized` decorator or an attribute on the function.

Note

Using `max_batch_size` is only meant as a mechanism to limit the number of rows that UDF can handle per single batch.
For example, if the UDF is written in a way that can only process at most 100 rows at a time, then `max_batch_size` should be set to 100.
Setting `max_batch_size` is not meant to be used as a mechanism to specify arbitrary large batch sizes.
If the UDF is able to process batches of any size, it is recommended to leave this parameter unset.

### Using the `vectorized` decorator

To set the target batch size using the `vectorized` decorator, pass a positive integer value for the argument named `max_batch_size`.

As an example, this statement creates a vectorized Python UDF and limits each Dataframe to a maximum of 100 rows:

Copy code

```
CREATE FUNCTION add_one_to_inputs(x NUMBER(10, 0), y NUMBER(10, 0))
  RETURNS NUMBER(10, 0)
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  PACKAGES = ('pandas')
  HANDLER = 'add_one_to_inputs'
AS $$
import pandas
from _snowflake import vectorized

@vectorized(input=pandas.DataFrame, max_batch_size=100)
def add_one_to_inputs(df):
 return df[0] + df[1] + 1
$$;
```

### Using a function attribute

To set the target batch size using a function attribute, set a positive integer value for the `_sf_max_batch_size` attribute on your handler function.

As an example, this statement creates a vectorized Python UDF and limits each DataFrame to a maximum of 100 rows:

Copy code

```
CREATE FUNCTION add_one_to_inputs(x NUMBER(10, 0), y NUMBER(10, 0))
  RETURNS NUMBER(10, 0)
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  PACKAGES = ('pandas')
  HANDLER = 'add_one_to_inputs'
AS $$
import pandas

def add_one_to_inputs(df):
 return df[0] + df[1] + 1

add_one_to_inputs._sf_vectorized_input = pandas.DataFrame
add_one_to_inputs._sf_max_batch_size = 100
$$;
```

## DataFrame encoding

Batches of arguments to the UDF are encoded as arrays in the input Pandas DataFrames, and the number of rows in each
DataFrame may vary. For more information, see [Setting a target batch size](#label-udf-python-batch-size). Arguments can be accessed in the
DataFrame by their index, i.e. the first argument has an index of 0, the second has an index of 1, and so on.
The Pandas array or Series that the UDF handler returns must have the same length as that of the input DataFrame.

To illustrate, suppose that you define a vectorized Python UDF as follows:

Copy code

```
CREATE OR REPLACE FUNCTION add_inputs(x INT, y FLOAT)
  RETURNS FLOAT
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  PACKAGES = ('pandas')
  HANDLER = 'add_inputs'
AS $$
import pandas
from _snowflake import vectorized

@vectorized(input=pandas.DataFrame)
def add_inputs(df):
  return df[0] + df[1]
$$;
```

This UDF uses `df[0]` to access the Pandas array for the first argument, and `df[1]` for the second. `df[0] + df[1]` results in a Pandas array with the pairwise sums of corresponding elements from the two arrays. After creating the UDF, you might call it with some input rows:

Copy code

```
SELECT add_inputs(x, y)
FROM (
  SELECT 1 AS x, 3.14::FLOAT as y UNION ALL
  SELECT 2, 1.59 UNION ALL
  SELECT 3, -0.5
);
```

```
+------------------+
| ADD_INPUTS(X, Y) |
|------------------|
|             4.14 |
|             3.59 |
|             2.5  |
+------------------+
```

Here the `add_inputs` Python function receives a DataFrame analogous to one created with the following Python code:

Copy code

```
>>> import pandas
>>> df = pandas.DataFrame({0: pandas.array([1, 2, 3]), 1: pandas.array([3.14, 1.59, -0.5])})
>>> df
   0     1
0  1  3.14
1  2  1.59
2  3 -0.50
```

The line `return df[0] + df[1]` in the handler function results in an array similar to the following Python code:

Copy code

```
>>> df[0] + df[1]
0    4.14
1    3.59
2    2.50
dtype: float64
```

### Type support

Vectorized Python UDFs support the following [SQL types](/sql-reference-data-types) for arguments and return values. The table reflects how each SQL argument is encoded as a Pandas array of a particular [dtype](https://pandas.pydata.org/docs/user_guide/basics.html#basics-dtypes).

| SQL Type | Pandas dtype | Notes |
| --- | --- | --- |
| NUMBER | `Int16`, `Int32`, or `Int64` for `NUMBER` arguments with a scale of 0 that all fit in a 64-bit or smaller integer type. If the argument is not nullable, `int16`, `int32`, or `int64` is used instead. (For UDTFs, `Int16`, `Int32`, or `Int64` will always be used.)  `object` for arguments with a scale other than 0, or for arguments that do not fit within a 64-bit integer, where array elements are encoded as `decimal.Decimal` values.  To ensure a 16-bit dtype, use a maximum `NUMBER` precision of 4. To ensure a 32-bit dtype, use a maximum `NUMBER` precision of 9. To ensure a 64-bit dtype, use a maximum `NUMBER` precision of 18. | To ensure that an input argument to a UDF is interpreted as not nullable, pass a column from a table created using the `NOT NULL` column constraint, or use a function such as `IFNULL` on the argument. |
| FLOAT | `float64` | NULL values are encoded as NaN values. In the output, NaN values are interpreted as NULLs. |
| BOOLEAN | `boolean` for nullable arguments or `bool` for non-nullable arguments. |  |
| VARCHAR | `string` | Both Snowflake SQL and Pandas represent strings using UTF-8 encoding. |
| BINARY | `bytes` |  |
| DATE | `datetime64` | Each value is encoded as a `datetime64` with no time component. NULL values are encoded as `numpy.timedelta('NaT')`. |
| VARIANT | `object`  Each value is encoded as a `dict`, `list`, `int`, `float`, `str`, or `bool`. | Each variant row is converted to a Python type dynamically for arguments and vice versa for return values. The following types are converted to strings rather than native Python types: `decimal`, `binary`, `date`, `time`, `timestamp_ltz`, `timestamp_ntz`, `timestamp_tz`. |
| OBJECT | `object`  Each element is encoded as a dict. |  |
| ARRAY | `object`  Each element is encoded as a list. |  |
| TIME | `timedelta64` | Each value is encoded as an offset from midnight. NULL values are encoded as `numpy.timedelta64('NaT')`. When used as a return type, elements of the output may be `numpy.timedelta64` or `datetime.time` values in the range `[00:00:00, 23:59:59.999999999]`. |
| TIMESTAMP\_LTZ | `datetime64` | Uses the local time zone to encode each value as a nanosecond-scale `numpy.datetime64` relative to the UTC Unix epoch. NULL values are encoded as `numpy.datetime64('NaT')`. When used as a return type, elements of the output may be `numpy.datetime64` or time zone naive `datetime.datetime` or `pandas.Timestamp` values. |
| TIMESTAMP\_NTZ | `datetime64` | Encodes each value as a nanosecond-scale `numpy.datetime64`. NULL values are encoded as `numpy.datetime64('NaT')`. When used as a return type, elements of the output may be `numpy.datetime64` or time zone naive `datetime.datetime` or `pandas.Timestamp` values. |
| TIMESTAMP\_TZ | `object` | Encodes each value as a nanosecond-scale `pandas.Timestamp`. NULL values are encoded as `pandas.NA`. When used as a return type, elements of the output may be time zone-aware `datetime.datetime` or `pandas.Timestamp` values. |
| GEOGRAPHY | `object` | Formats each value as GeoJSON and then converts it to a Python `dict`. |

Expand

Show lessSee more

The following types are accepted as output: Pandas `Series` or `array`, NumPy `array`, regular
Python `list`, and any iterable sequence that contains the expected types described
in [Type support](#label-udf-python-batch-types). It is efficient to use Pandas `Series` and `array` and NumPy `array`
where the dtype is `bool`, `boolean`,
`int16`, `int32`, `int64`, `Int16`, `Int32`, `Int64`, or `float64`
because they expose their contents as `memoryviews`. This means that the contents can be copied rather than each value
being read sequentially.
