# Vectorized Python UDTFs

This topic introduces vectorized Python UDTFs.

## Overview

Vectorized Python UDTFs (user-defined table functions) provide a way to operate over rows in batches.

Snowflake supports two kinds of vectorized UDTFs:

- UDTFs with a vectorized `end_partition` method
- UDTFs with a vectorized `process` method

You must choose one kind because a UDTF can’t have both a vectorized `process` method and a vectorized `end_partition` method.

### UDTFs with a vectorized end\_partition method

UDTFs with a vectorized `end_partition` method enable seamless partition-by-partition processing by operating on
partitions as [pandas DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
and returning results as
[pandas DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
or lists of [pandas arrays](https://pandas.pydata.org/docs/reference/api/pandas.array.html)
or [pandas Series](https://pandas.pydata.org/docs/reference/series.html).
This facilitates integration with libraries that operate on pandas DataFrames or pandas arrays.

Use a vectorized `end_partition` method for the following tasks:

- Process your data on a partition-by-partition basis instead of on a row-by-row basis.
- Return multiple rows or columns for each partition.
- Use libraries that operate on pandas DataFrames for data analysis.

### UDTFs with a vectorized process method

UDTFs with a vectorized `process` method provide a way to operate over rows in batches, when the operation performs a 1-to-1 mapping.
In other words, the method returns one output row for each input row. The number of columns is not restricted.

Use a vectorized `process` method for the following tasks:

- Apply a 1-to-1 transformation with a multi-columnar result in batches.
- Use a library that requires `pandas.DataFrame`.
- Process rows in batches, without explicit partitioning.
- Leverage the [to\_pandas()](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.DataFrame.to_pandas) API to transform the query result directly to a pandas DataFrame.

## Prerequisites

The Snowpark Library for Python version 1.14.0 or later is required.

## Create a UDTF with a vectorized end\_partition method

1. Optional: Define a handler class with an `__init__` method, which will be invoked before each partition is processed.

   Note: Do not define a `process` method.
2. Define an `end_partition` method that takes in a DataFrame argument and returns or yields a `pandas.DataFrame` or a tuple of `pandas.Series` or `pandas.arrays` where each array is a column.

   The column types of the result must match the column types in the UDTF definition.
3. To mark the `end_partition` method as vectorized, use the `@vectorized` decorator or the `_sf_vectorized_input` function attribute.

   For more information, see [Vectorized Python UDFs](/developer-guide/udf/python/udf-python-batch). The `@vectorized` decorator can only be used when the Python UDTF is executed within Snowflake; for example, when using a SQL worksheet. When you are executing using the client or a Python worksheet, you must use the function attribute.

Note

The default column names for the input DataFrame to a UDTF with a vectorized `end_partition` method match the signature of the SQL function.
The column names follow the [SQL identifier requirements](/sql-reference/identifiers-syntax).
That is, if an identifier is unquoted it will be capitalized, and if it is double quoted it will remain unchanged.

The following code block is an example of creating a UDTF with a vectorized `end_partition` method, using the `@vectorized` decorator:

Copy code

```
from _snowflake import vectorized
import pandas

class handler:
  def __init__(self):
    # initialize a state
  @vectorized(input=pandas.DataFrame)
  def end_partition(self, df):
    # process the DataFrame
    return result_df
```

The following code block is an example of creating a UDTF with a vectorized `end_partition` method, using the function attribute:

Copy code

```
import pandas

class handler:
  def __init__(self):
    # initialize a state
  def end_partition(self, df):
    # process the DataFrame
    return result_df

handler.end_partition._sf_vectorized_input = pandas.DataFrame
```

Note

A UDTF with a vectorized `end_partition` method must be called with a PARTITION BY clause to build the partitions.

To call the UDTF with all the data in the same partition:

Copy code

```
SELECT * FROM table(udtf(x,y,z) OVER (PARTITION BY 1));
```

To call the UDTF with the data partitioned by column x:

Copy code

```
SELECT * FROM table(udtf(x,y,z) OVER (PARTITION BY x));
```

### Example: Row collection using a regular UDTF versus using a UDTF with a vectorized end\_partition method

Row collection using a regular UDTF:

Copy code

```
import pandas

class handler:
  def __init__(self):
    self.rows = []
  def process(self, *row):
    self.rows.append(row)
  def end_partition(self):
    df = pandas.DataFrame(self.rows)
    # process the DataFrame
    return result_df
```

Row collection using a UDTF with a vectorized `end_partition` method:

Copy code

```
from _snowflake import vectorized
import pandas

class handler:
  def __init__(self):
    self.rows = []
  @vectorized(input=pandas.DataFrame)
  def end_partition(self, df):
  # process the DataFrame
    return result_df
```

### Example: Calculate the summary statistic for each column in the partition

Here is an example of how to calculate the summary statistic for each column in the partition using
the pandas `describe()` method.

1. Create a table and generate three partitions of five rows each:

   Copy code

   ```
   CREATE OR REPLACE TABLE test_values(id VARCHAR, col1 FLOAT, col2 FLOAT, col3 FLOAT, col4 FLOAT, col5 FLOAT);

   -- generate 3 partitions of 5 rows each
   INSERT INTO test_values
     SELECT 'x',
     UNIFORM(1.5,1000.5,RANDOM(1))::FLOAT col1,
     UNIFORM(1.5,1000.5,RANDOM(2))::FLOAT col2,
     UNIFORM(1.5,1000.5,RANDOM(3))::FLOAT col3,
     UNIFORM(1.5,1000.5,RANDOM(4))::FLOAT col4,
     UNIFORM(1.5,1000.5,RANDOM(5))::FLOAT col5
     FROM TABLE(GENERATOR(ROWCOUNT => 5));

   INSERT INTO test_values
     SELECT 'y',
     UNIFORM(1.5,1000.5,RANDOM(10))::FLOAT col1,
     UNIFORM(1.5,1000.5,RANDOM(20))::FLOAT col2,
     UNIFORM(1.5,1000.5,RANDOM(30))::FLOAT col3,
     UNIFORM(1.5,1000.5,RANDOM(40))::FLOAT col4,
     UNIFORM(1.5,1000.5,RANDOM(50))::FLOAT col5
     FROM TABLE(GENERATOR(ROWCOUNT => 5));

   INSERT INTO test_values
     SELECT 'z',
     UNIFORM(1.5,1000.5,RANDOM(100))::FLOAT col1,
     UNIFORM(1.5,1000.5,RANDOM(200))::FLOAT col2,
     UNIFORM(1.5,1000.5,RANDOM(300))::FLOAT col3,
     UNIFORM(1.5,1000.5,RANDOM(400))::FLOAT col4,
     UNIFORM(1.5,1000.5,RANDOM(500))::FLOAT col5
     FROM TABLE(GENERATOR(ROWCOUNT => 5));
   ```
2. Look at the data:

   Copy code

   ```
   SELECT * FROM test_values;
   ```

   ```
   -----------------------------------------------------
   |"ID"  |"COL1"  |"COL2"  |"COL3"  |"COL4"  |"COL5"  |
   -----------------------------------------------------
   |x     |8.0     |99.4    |714.6   |168.7   |397.2   |
   |x     |106.4   |237.1   |971.7   |828.4   |988.2   |
   |x     |741.3   |207.9   |32.6    |640.6   |63.2    |
   |x     |541.3   |828.6   |844.9   |77.3    |403.1   |
   |x     |4.3     |723.3   |924.3   |282.5   |158.1   |
   |y     |976.1   |562.4   |968.7   |934.3   |977.3   |
   |y     |390.0   |244.3   |952.6   |101.7   |24.9    |
   |y     |599.7   |191.8   |90.2    |788.2   |761.2   |
   |y     |589.5   |201.0   |863.4   |415.1   |696.1   |
   |y     |46.7    |659.7   |571.1   |938.0   |513.7   |
   |z     |313.9   |188.5   |964.6   |435.4   |519.6   |
   |z     |328.3   |643.1   |766.4   |148.1   |596.4   |
   |z     |929.0   |255.4   |915.9   |857.2   |425.5   |
   |z     |612.8   |816.4   |220.2   |879.5   |331.4   |
   |z     |487.1   |704.5   |471.5   |378.9   |481.2   |
   -----------------------------------------------------
   ```
3. Create the function:

   Copy code

   ```
   CREATE OR REPLACE FUNCTION summary_stats(id VARCHAR, col1 FLOAT, col2 FLOAT, col3 FLOAT, col4 FLOAT, col5 FLOAT)
     RETURNS TABLE (column_name VARCHAR, count INT, mean FLOAT, std FLOAT, min FLOAT, q1 FLOAT, median FLOAT, q3 FLOAT, max FLOAT)
     LANGUAGE PYTHON
     RUNTIME_VERSION = 3.12
     PACKAGES = ('pandas')
     HANDLER = 'handler'
   AS $$
   from _snowflake import vectorized
   import pandas

   class handler:
    @vectorized(input=pandas.DataFrame)
    def end_partition(self, df):
      # using describe function to get the summary statistics
      result = df.describe().transpose()
      # add a column at the beginning for column ids
      result.insert(loc=0, column='column_name', value=['col1', 'col2', 'col3', 'col4', 'col5'])
      return result
   $$;
   ```
4. Do one of the following steps:

   - Call the function and partition by `id`:

     Copy code

     ```
     -- partition by id
     SELECT * FROM test_values, TABLE(summary_stats(id, col1, col2, col3, col4, col5)
       OVER (PARTITION BY id))
       ORDER BY id, column_name;
     ```

     ```
     --------------------------------------------------------------------------------------------------------------------------------------------------------------------
     |"ID"  |"COL1"  |"COL2"  |"COL3"  |"COL4"  |"COL5"  |"COLUMN_NAME"  |"COUNT"  |"MEAN"              |"STD"               |"MIN"  |"Q1"   |"MEDIAN"  |"Q3"   |"MAX"  |
     --------------------------------------------------------------------------------------------------------------------------------------------------------------------
     |x     |NULL    |NULL    |NULL    |NULL    |NULL    |col1           |5        |280.25999999999993  |339.5609267863427   |4.3    |8.0    |106.4     |541.3  |741.3  |
     |x     |NULL    |NULL    |NULL    |NULL    |NULL    |col2           |5        |419.25999999999993  |331.72476995244114  |99.4   |207.9  |237.1     |723.3  |828.6  |
     |x     |NULL    |NULL    |NULL    |NULL    |NULL    |col3           |5        |697.62              |384.2964311569911   |32.6   |714.6  |844.9     |924.3  |971.7  |
     |x     |NULL    |NULL    |NULL    |NULL    |NULL    |col4           |5        |399.5               |321.2689294033894   |77.3   |168.7  |282.5     |640.6  |828.4  |
     |x     |NULL    |NULL    |NULL    |NULL    |NULL    |col5           |5        |401.96000000000004  |359.83584173897964  |63.2   |158.1  |397.2     |403.1  |988.2  |
     |y     |NULL    |NULL    |NULL    |NULL    |NULL    |col1           |5        |520.4               |339.16133329139984  |46.7   |390.0  |589.5     |599.7  |976.1  |
     |y     |NULL    |NULL    |NULL    |NULL    |NULL    |col2           |5        |371.84              |221.94799616126298  |191.8  |201.0  |244.3     |562.4  |659.7  |
     |y     |NULL    |NULL    |NULL    |NULL    |NULL    |col3           |5        |689.2               |371.01012789410476  |90.2   |571.1  |863.4     |952.6  |968.7  |
     |y     |NULL    |NULL    |NULL    |NULL    |NULL    |col4           |5        |635.46              |366.6140927460372   |101.7  |415.1  |788.2     |934.3  |938.0  |
     |y     |NULL    |NULL    |NULL    |NULL    |NULL    |col5           |5        |594.64              |359.0334218425911   |24.9   |513.7  |696.1     |761.2  |977.3  |
     |z     |NULL    |NULL    |NULL    |NULL    |NULL    |col1           |5        |534.22              |252.58182238633088  |313.9  |328.3  |487.1     |612.8  |929.0  |
     |z     |NULL    |NULL    |NULL    |NULL    |NULL    |col2           |5        |521.58              |281.4870103574941   |188.5  |255.4  |643.1     |704.5  |816.4  |
     |z     |NULL    |NULL    |NULL    |NULL    |NULL    |col3           |5        |667.72              |315.53336907528495  |220.2  |471.5  |766.4     |915.9  |964.6  |
     |z     |NULL    |NULL    |NULL    |NULL    |NULL    |col4           |5        |539.8199999999999   |318.73025742781306  |148.1  |378.9  |435.4     |857.2  |879.5  |
     |z     |NULL    |NULL    |NULL    |NULL    |NULL    |col5           |5        |470.82              |99.68626786072393   |331.4  |425.5  |481.2     |519.6  |596.4  |
     --------------------------------------------------------------------------------------------------------------------------------------------------------------------
     ```
   - Call the function and treat the whole table as one partition:

     Copy code

     ```
     -- treat the whole table as one partition
     SELECT * FROM test_values, TABLE(summary_stats(id, col1, col2, col3, col4, col5)
       OVER (PARTITION BY 1))
       ORDER BY id, column_name;
     ```

     ```
     ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
     |"ID"  |"COL1"  |"COL2"  |"COL3"  |"COL4"  |"COL5"  |"COLUMN_NAME"  |"COUNT"  |"MEAN"             |"STD"               |"MIN"  |"Q1"                |"MEDIAN"  |"Q3"    |"MAX"  |
     ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
     |NULL  |NULL    |NULL    |NULL    |NULL    |NULL    |col1           |15       |444.96             |314.01110034974425  |4.3    |210.14999999999998  |487.1     |606.25  |976.1  |
     |NULL  |NULL    |NULL    |NULL    |NULL    |NULL    |col2           |15       |437.56             |268.95505944302295  |99.4   |204.45              |255.4     |682.1   |828.6  |
     |NULL  |NULL    |NULL    |NULL    |NULL    |NULL    |col3           |15       |684.8466666666667  |331.87254839915937  |32.6   |521.3               |844.9     |938.45  |971.7  |
     |NULL  |NULL    |NULL    |NULL    |NULL    |NULL    |col4           |15       |524.9266666666666  |327.074780585783    |77.3   |225.6               |435.4     |842.8   |938.0  |
     |NULL  |NULL    |NULL    |NULL    |NULL    |NULL    |col5           |15       |489.14             |288.9176669671038   |24.9   |364.29999999999995  |481.2     |646.25  |988.2  |
     ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
     ```

## Create a UDTF with a vectorized process method

1. Define a handler class, similar to regular UDTFs, with optional `__init__` and `end_partition` methods.
2. Define a `process` method that takes in a DataFrame argument and returns either a `pandas.DataFrame` or a tuple of `pandas.Series` or `pandas.arrays` where each array is a column.

   The column types of the result must match the column types in the UDTF definition.
   The returned result must be exactly one DataFrame or tuple. This is different from a vectorized `end_partition` method where you can yield or return a list.
3. To mark the `process` method as vectorized, use the `@vectorized` decorator or the `_sf_vectorized_input` function attribute.

   For more information, see [Vectorized Python UDFs](/developer-guide/udf/python/udf-python-batch).
   The `@vectorized` decorator can only be used when the Python UDTF is executed within Snowflake; for example, when using a SQL worksheet.
   When you are executing using the client or a Python worksheet, you must use the function attribute.
4. Optional: If your Python handler function is exceeding the execution time limit, [set a target batch size](/developer-guide/udf/python/udf-python-batch#label-udf-python-batch-size).

Note

The default column names for the input DataFrame to a UDTF with a vectorized `process` method match the signature of the SQL function.
The column names follow the [SQL identifier requirements](/sql-reference/identifiers-syntax).
Namely, if an identifier is unquoted it will be capitalized, and if it is double quoted it will remain unchanged.

The handler for a UDTF with a vectorized `process` method can be implemented to process batches in a partition-aware manner or to process them simply batch by batch.
For more information, see [Stateful and Stateless Processing](/developer-guide/udf/python/udf-python-tabular-functions#label-udtf-python-processing-input).

### Example: Use a UDTF with a vectorized process method to apply one hot encoding

Use a UDTF with a vectorized `process` method to apply one hot encoding on a table with ten categories:

Copy code

```
import pandas as pd
from snowflake.snowpark import Session
from snowflake.snowpark.types import PandasDataFrame

class one_hot_encode:
  def process(self, df: PandasDataFrame[str]) -> PandasDataFrame[int,int,int,int,int,int,int,int,int,int]:
      return pd.get_dummies(df)
  process._sf_vectorized_input = pd.DataFrame

one_hot_encode_udtf = session.udtf.register(
  one_hot_encode,
  output_schema=["categ0", "categ1", "categ2", "categ3", "categ4", "categ5", "categ6", "categ7", "categ8", "categ9"],
  input_names=['"categ"']
)

df_table = session.table("categories")
df_table.show()
```

Sample result:

```
-----------
|"CATEG"  |
-----------
|categ1   |
|categ6   |
|categ8   |
|categ5   |
|categ7   |
|categ5   |
|categ1   |
|categ2   |
|categ2   |
|categ4   |
-----------
```

Prepare to print the table:

Copy code

```
res = df_table.select("categ", one_hot_encode_udtf("categ")).to_pandas()
print(res.head())
```

Sample result:

```
    CATEG  CATEG0  CATEG1  CATEG2  CATEG3  CATEG4  CATEG5  CATEG6  CATEG7  CATEG8  CATEG9
0  categ0       1       0       0       0       0       0       0       0       0       0
1  categ0       1       0       0       0       0       0       0       0       0       0
2  categ5       0       0       0       0       0       1       0       0       0       0
3  categ3       0       0       0       1       0       0       0       0       0       0
4  categ8       0       0       0       0       0       0       0       0       1       0
```

You can obtain the same result with a vectorized UDF, although is less convenient.
You need to package the results into one column, and then unpack the column to restore the results to a usable pandas DataFrame.

Example of using a vectorized UDF:

Copy code

```
def one_hot_encode(df: PandasSeries[str]) -> PandasSeries[Variant]:
  return pd.get_dummies(df).to_dict('records')

one_hot_encode._sf_vectorized_input = pd.DataFrame

one_hot_encode_udf = session.udf.register(
  one_hot_encode,
  output_schema=["encoding"],
)

df_table = session.table("categories")
df_table.show()
res = df_table.select(one_hot_encode_udf("categ")).to_df("encoding").to_pandas()
print(res.head())
0  {\n  "categ0": false,\n  "categ1": false,\n  "...
1  {\n  "categ0": false,\n  "categ1": true,\n  "c...
2  {\n  "categ0": false,\n  "categ1": false,\n  "...
3  {\n  "categ0": false,\n  "categ1": false,\n  "...
4  {\n  "categ0": true,\n  "categ1": false,\n  "c...
```

## Type support

Vectorized UDTFs support the same [SQL types](/sql-reference-data-types) as
vectorized UDFs. However, for vectorized UDTFs,
SQL `NUMBER` arguments with a scale of 0 that all fit in a 64-bit
or smaller integer type will always be mapped to `Int16`, `Int32`, or `Int64`.
Unlike scalar UDFs, if the argument of a UDTF is not nullable, it will not be converted to `int16`, `int32`, or `int64`.

To view a table showing how SQL types are mapped to pandas dtypes, see [the type support table](/developer-guide/udf/python/udf-python-batch#label-udf-python-batch-types) in the
vectorized Python UDFs topic.

## Best practices

- If a scalar must be returned with each row, build a list of repeated values instead of unpackaging the `numpy` array to create tuples.
  For example, for a two-column result, instead of:

  Copy code

  ```
  return tuple(map(lambda n: (scalar_value, n[0], n[1]), results))
  ```

  Use this:

  Copy code

  ```
  return tuple([scalar_value] * len(results), results[:, 0], results[:, 1])
  ```
- To improve performance, unpackage semi-structured data into columns.

  For example, if you have a variant column, `obj`, with elements, `x(int)`, `y(float)`, and `z(string)`,
  instead of defining a UDTF with a signature like this, and calling it using `vec_udtf(obj)`:

  Copy code

  ```
  CREATE FUNCTION vec_udtf(variant OBJ)
  ```

  Define the UDTF with a signature like this, and call it using `vec_udtf(obj:x, obj:y, obj:z)`:

  Copy code

  ```
  CREATE FUNCTION vec_udtf(a INTEGER, b FLOAT, c STRING)
  ```
- By default, Snowflake encodes the inputs into pandas dtypes that support NULL values (for example, [Int64](https://pandas.pydata.org/docs/reference/api/pandas.Int64Dtype.html)).
  If you are using a library that requires a primitive type (such as `numpy`) and your input has no NULL values, you should cast the column to a primitive type before using the library. For example:

  Copy code

  ```
  input_df['y'] =  input_df['y'].astype("int64")
  ```

  For more information, see [Type Support](#label-udtf-python-tabular-vectorized-type).
- When using UDTFs with a vectorized `end_partition` method, to improve performance and prevent timeouts, avoid using `pandas.concat` to accumulate partial results. Instead, yield the partial result whenever one is ready.

  For example, instead of:

  Copy code

  ```
  results = []
  while(...):
    partial_result = pd.DataFrame(...)
    results.append(partial_result)
  return pd.concat(results)
  ```

  Do this:

  Copy code

  ```
  while(...):
    partial_result = pd.DataFrame(...)
    yield partial_result
  ```
