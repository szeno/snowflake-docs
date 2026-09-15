# Working with DataFrames in Snowpark Python

In Snowpark, the main way in which you query and process data is through a DataFrame. This topic explains how to work with
DataFrames.

To retrieve and manipulate data, you use the `DataFrame` class. A
DataFrame represents a relational dataset that is evaluated lazily: it only executes when a specific action is triggered. In a
sense, a DataFrame is like a query that needs to be evaluated in order to retrieve data.

To retrieve data into a DataFrame:

1. [Construct a DataFrame, specifying the source of the data for the dataset](#label-snowpark-python-dataframe-construct).

   For example, you can create a DataFrame to hold data from a table, an external CSV file, from local data, or the execution of a SQL statement.
2. [Specify how the dataset in the DataFrame should be transformed](#label-snowpark-python-dataframe-transform).

   For example, you can specify which columns should be selected, how the rows should be filtered, how the results should be
   sorted and grouped, etc.
3. [Execute the statement to retrieve the data into the DataFrame](#label-snowpark-python-dataframe-action-method).

   In order to retrieve the data into the DataFrame, you must invoke a method that performs an action (for example, the
   `collect()` method).

The next sections explain these steps in more detail.

## Setting up the Examples for this Section

Some of the examples of this section use a DataFrame to query a table named `sample_product_data`. If you want to run these
examples, you can create this table and fill the table with some data by executing the following SQL statements.

You can run the SQL statements using Snowpark Python:

Copy code

```
session.sql('CREATE OR REPLACE TABLE sample_product_data (id INT, parent_id INT, category_id INT, name VARCHAR, serial_number VARCHAR, key INT, "3rd" INT)').collect()
```

```
[Row(status='Table SAMPLE_PRODUCT_DATA successfully created.')]
```

Copy code

```
session.sql("""
INSERT INTO sample_product_data VALUES
(1, 0, 5, 'Product 1', 'prod-1', 1, 10),
(2, 1, 5, 'Product 1A', 'prod-1-A', 1, 20),
(3, 1, 5, 'Product 1B', 'prod-1-B', 1, 30),
(4, 0, 10, 'Product 2', 'prod-2', 2, 40),
(5, 4, 10, 'Product 2A', 'prod-2-A', 2, 50),
(6, 4, 10, 'Product 2B', 'prod-2-B', 2, 60),
(7, 0, 20, 'Product 3', 'prod-3', 3, 70),
(8, 7, 20, 'Product 3A', 'prod-3-A', 3, 80),
(9, 7, 20, 'Product 3B', 'prod-3-B', 3, 90),
(10, 0, 50, 'Product 4', 'prod-4', 4, 100),
(11, 10, 50, 'Product 4A', 'prod-4-A', 4, 100),
(12, 10, 50, 'Product 4B', 'prod-4-B', 4, 100)
""").collect()
```

```
[Row(number of rows inserted=12)]
```

To verify that the table was created, run:

Copy code

```
session.sql("SELECT count(*) FROM sample_product_data").collect()
```

```
[Row(COUNT(*)=12)]
```

### Setting up the Examples in a Python Worksheet

To set up and run these examples in a [Python worksheet](/developer-guide/snowpark/python/python-worksheets),
create the sample table and set up your Python worksheet.

1. Create a SQL worksheet and run the following:

> Copy code
>
> ```
> CREATE OR REPLACE TABLE sample_product_data
>   (id INT, parent_id INT, category_id INT, name VARCHAR, serial_number VARCHAR, key INT, "3rd" INT);
>
> INSERT INTO sample_product_data VALUES
>   (1, 0, 5, 'Product 1', 'prod-1', 1, 10),
>   (2, 1, 5, 'Product 1A', 'prod-1-A', 1, 20),
>   (3, 1, 5, 'Product 1B', 'prod-1-B', 1, 30),
>   (4, 0, 10, 'Product 2', 'prod-2', 2, 40),
>   (5, 4, 10, 'Product 2A', 'prod-2-A', 2, 50),
>   (6, 4, 10, 'Product 2B', 'prod-2-B', 2, 60),
>   (7, 0, 20, 'Product 3', 'prod-3', 3, 70),
>   (8, 7, 20, 'Product 3A', 'prod-3-A', 3, 80),
>   (9, 7, 20, 'Product 3B', 'prod-3-B', 3, 90),
>   (10, 0, 50, 'Product 4', 'prod-4', 4, 100),
>   (11, 10, 50, 'Product 4A', 'prod-4-A', 4, 100),
>   (12, 10, 50, 'Product 4B', 'prod-4-B', 4, 100);
>
> SELECT count(*) FROM sample_product_data;
> ```

1. [Create a Python worksheet](/developer-guide/snowpark/python/python-worksheets#label-snowsight-py-worksheets-start), setting the same database and schema context as the
   SQL worksheet that you used to create the `sample_product_data` table.

If you want to use the examples in this topic in a Python worksheet, use the example within the handler function (e.g. `main`),
and use the `Session` object that is passed into the function to create DataFrames.

For example, call the `table` method of the `session` object to create a DataFrame for a table:

Copy code

```
import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import col

def main(session: snowpark.Session):
  df_table = session.table("sample_product_data")
```

To review the output produced by the function, such as by calling the `show` method of the DataFrame object, use the **Output** tab.

To examine the value returned by the function, choose the data type of the return value from **Settings** » **Return type**,
and use the **Results** tab:

- If your function returns a DataFrame, use the default return type of **Table**.
- If your function returns the `list` of `Row` from the `collect` method of a DataFrame object,
  use **Variant** for the return type.
- If your function returns any other value that can be cast to a string, or if your function does not return a value, use **String**
  as the return type.

Refer to [Running Python Worksheets](/developer-guide/snowpark/python/python-worksheets#label-snowsight-py-worksheets-run) for more details.

## Constructing a DataFrame

To construct a DataFrame, you can use the methods and properties of the `Session` class. Each of the following
methods constructs a DataFrame from a different type of data source.

You can run these examples in your local development environment
or call them within the `main` function defined in a [Python worksheet](/developer-guide/snowpark/python/python-worksheets).

- To create a DataFrame from data in a table, view, or stream, call the `table` method:

  Copy code

  ```
  # Create a DataFrame from the data in the "sample_product_data" table.
  df_table = session.table("sample_product_data")

  # To print out the first 10 rows, call df_table.show()
  ```
- To create a DataFrame from specified values, call the `create_dataframe` method:

  Copy code

  ```
  # Create a DataFrame with one column named a from specified values.
  df1 = session.create_dataframe([1, 2, 3, 4]).to_df("a")
  df1.show()
  # To return the DataFrame as a table in a Python worksheet use return instead of show()
  # return df1
  ```

  ```
  -------
  |"A"  |
  -------
  |1    |
  |2    |
  |3    |
  |4    |
  -------
  ```

  Create a DataFrame with 4 columns, “a”, “b”, “c” and “d”:

  Copy code

  ```
  # Create a DataFrame with 4 columns, "a", "b", "c" and "d".
  df2 = session.create_dataframe([[1, 2, 3, 4]], schema=["a", "b", "c", "d"])
  df2.show()
  # To return the DataFrame as a table in a Python worksheet use return instead of show()
  # return df2
  ```

  ```
  -------------------------
  |"A"  |"B"  |"C"  |"D"  |
  -------------------------
  |1    |2    |3    |4    |
  -------------------------
  ```

  Create another DataFrame with 4 columns, “a”, “b”, “c” and “d”:

  Copy code

  ```
  # Create another DataFrame with 4 columns, "a", "b", "c" and "d".
  from snowflake.snowpark import Row
  df3 = session.create_dataframe([Row(a=1, b=2, c=3, d=4)])
  df3.show()
  # To return the DataFrame as a table in a Python worksheet use return instead of show()
  # return df3
  ```

  ```
  -------------------------
  |"A"  |"B"  |"C"  |"D"  |
  -------------------------
  |1    |2    |3    |4    |
  -------------------------
  ```

  Create a DataFrame and specify a schema:

  Copy code

  ```
  # Create a DataFrame and specify a schema
  from snowflake.snowpark.types import IntegerType, StringType, StructType, StructField
  schema = StructType([StructField("a", IntegerType()), StructField("b", StringType())])
  df4 = session.create_dataframe([[1, "snow"], [3, "flake"]], schema)
  df4.show()
  # To return the DataFrame as a table in a Python worksheet use return instead of show()
  # return df4
  ```

  ```
  ---------------
  |"A"  |"B"    |
  ---------------
  |1    |snow   |
  |3    |flake  |
  ---------------
  ```
- To create a DataFrame containing a range of values, call the `range` method:

  Copy code

  ```
  # Create a DataFrame from a range
  # The DataFrame contains rows with values 1, 3, 5, 7, and 9 respectively.
  df_range = session.range(1, 10, 2).to_df("a")
  df_range.show()
  # To return the DataFrame as a table in a Python worksheet use return instead of show()
  # return df_range
  ```

  ```
  -------
  |"A"  |
  -------
  |1    |
  |3    |
  |5    |
  |7    |
  |9    |
  -------
  ```
- To create a DataFrame to hold the data from a file in a stage, use the `read` property to get a
  `DataFrameReader` object. In the `DataFrameReader` object, call the method corresponding to the
  format of the data in the file:

  Copy code

  ```
  from snowflake.snowpark.types import StructType, StructField, StringType, IntegerType

  # Create DataFrames from data in a stage.
  df_json = session.read.json("@my_stage2/data1.json")
  df_catalog = session.read.schema(StructType([StructField("name", StringType()), StructField("age", IntegerType())])).csv("@stage/some_dir")
  ```
- To create a DataFrame to hold the results of a SQL query, call the `sql` method:

  Copy code

  ```
  # Create a DataFrame from a SQL query
  df_sql = session.sql("SELECT name from sample_product_data")
  df_sql.show()
  # To return the DataFrame as a table in a Python worksheet use return instead of show()
  # return df_sql
  ```

  ```
  --------------
  |"NAME"      |
  --------------
  |Product 1   |
  |Product 1A  |
  |Product 1B  |
  |Product 2   |
  |Product 2A  |
  |Product 2B  |
  |Product 3   |
  |Product 3A  |
  |Product 3B  |
  |Product 4   |
  --------------
  ```

It is possible to use the `sql` method to execute SELECT statements that retrieve data from tables and staged files,
but using the `table` method and `read` property offer better syntax highlighting, error highlighting, and
intelligent code completion in development tools.

## Specifying How the Dataset Should Be Transformed

To specify which columns to select and how to filter, sort, group, etc. results, call the DataFrame methods that transform the dataset.
To identify columns in these methods, use the `col` function or an expression that
evaluates to a column. Refer to [Specifying Columns and Expressions](#label-snowpark-python-dataframe-cols-and-expressions).

For example:

- To specify which rows should be returned, call the `filter` method:

  Copy code

  ```
  # Import the col function from the functions module.
  # Python worksheets import this function by default
  from snowflake.snowpark.functions import col

  # Create a DataFrame for the rows with the ID 1
  # in the "sample_product_data" table.

  # This example uses the == operator of the Column object to perform an
  # equality check.
  df = session.table("sample_product_data").filter(col("id") == 1)
  df.show()
  # To return the DataFrame as a table in a Python worksheet use return instead of show()
  return df
  ```

  ```
  ------------------------------------------------------------------------------------
  |"ID"  |"PARENT_ID"  |"CATEGORY_ID"  |"NAME"     |"SERIAL_NUMBER"  |"KEY"  |"3rd"  |
  ------------------------------------------------------------------------------------
  |1     |0            |5              |Product 1  |prod-1           |1      |10     |
  ------------------------------------------------------------------------------------
  ```
- To specify the columns that should be selected, call the `select` method:

  Copy code

  ```
  # Import the col function from the functions module.
  from snowflake.snowpark.functions import col

  # Create a DataFrame that contains the id, name, and serial_number
  # columns in the "sample_product_data" table.
  df = session.table("sample_product_data").select(col("id"), col("name"), col("serial_number"))
  df.show()
  # To return the DataFrame as a table in a Python worksheet use return instead of show()
  return df
  ```

  ```
  ---------------------------------------
  |"ID"  |"NAME"      |"SERIAL_NUMBER"  |
  ---------------------------------------
  |1     |Product 1   |prod-1           |
  |2     |Product 1A  |prod-1-A         |
  |3     |Product 1B  |prod-1-B         |
  |4     |Product 2   |prod-2           |
  |5     |Product 2A  |prod-2-A         |
  |6     |Product 2B  |prod-2-B         |
  |7     |Product 3   |prod-3           |
  |8     |Product 3A  |prod-3-A         |
  |9     |Product 3B  |prod-3-B         |
  |10    |Product 4   |prod-4           |
  ---------------------------------------
  ```
- You can also reference columns like this:

  Copy code

  ```
  # Import the col function from the functions module.
  from snowflake.snowpark.functions import col

  df_product_info = session.table("sample_product_data")
  df1 = df_product_info.select(df_product_info["id"], df_product_info["name"], df_product_info["serial_number"])
  df2 = df_product_info.select(df_product_info.id, df_product_info.name, df_product_info.serial_number)
  df3 = df_product_info.select("id", "name", "serial_number")
  ```

Each method returns a new DataFrame object that has been transformed. The method does not affect the original DataFrame object.
If you want to apply multiple transformations, you can [chain method calls](#label-snowpark-python-dataframe-chaining-method-calls),
calling each subsequent transformation method on the new DataFrame object returned by the previous method call.

These transformation methods specify how to construct the SQL statement and do not retrieve data from the Snowflake database.
The action methods described in [Performing an Action to Evaluate a DataFrame](#label-snowpark-python-dataframe-action-method) perform the data retrieval.

### Joining DataFrames

To join DataFrame objects, call the `join` method:

Copy code

```
# Create two DataFrames to join
df_lhs = session.create_dataframe([["a", 1], ["b", 2]], schema=["key", "value1"])
df_rhs = session.create_dataframe([["a", 3], ["b", 4]], schema=["key", "value2"])
# Create a DataFrame that joins the two DataFrames
# on the column named "key".
df_lhs.join(df_rhs, df_lhs.col("key") == df_rhs.col("key")).select(df_lhs["key"].as_("key"), "value1", "value2").show()
# To return the DataFrame as a table in a Python worksheet use return instead of show()
return df_lhs.join(df_rhs, df_lhs.col("key") == df_rhs.col("key")).select(df_lhs["key"].as_("key"), "value1", "value2")
```

```
-------------------------------
|"KEY"  |"VALUE1"  |"VALUE2"  |
-------------------------------
|a      |1         |3         |
|b      |2         |4         |
-------------------------------
```

If both DataFrames have the same column to join on, you can use the following example syntax:

Copy code

```
# Create two DataFrames to join
df_lhs = session.create_dataframe([["a", 1], ["b", 2]], schema=["key", "value1"])
df_rhs = session.create_dataframe([["a", 3], ["b", 4]], schema=["key", "value2"])
# If both dataframes have the same column "key", the following is more convenient.
df_lhs.join(df_rhs, ["key"]).show()
# To return the DataFrame as a table in a Python worksheet use return instead of show()
return df_lhs.join(df_rhs, ["key"])
```

```
-------------------------------
|"KEY"  |"VALUE1"  |"VALUE2"  |
-------------------------------
|a      |1         |3         |
|b      |2         |4         |
-------------------------------
```

You can also use the & operator to connect join expressions:

Copy code

```
# Create two DataFrames to join
df_lhs = session.create_dataframe([["a", 1], ["b", 2]], schema=["key", "value1"])
df_rhs = session.create_dataframe([["a", 3], ["b", 4]], schema=["key", "value2"])
# Use & operator connect join expression. '|' and ~ are similar.
df_joined_multi_column = df_lhs.join(df_rhs, (df_lhs.col("key") == df_rhs.col("key")) & (df_lhs.col("value1") < df_rhs.col("value2"))).select(df_lhs["key"].as_("key"), "value1", "value2")
df_joined_multi_column.show()
# To return the DataFrame as a table in a Python worksheet use return instead of show()
return df_joined_multi_column
```

```
-------------------------------
|"KEY"  |"VALUE1"  |"VALUE2"  |
-------------------------------
|a      |1         |3         |
|b      |2         |4         |
-------------------------------
```

If you want to perform a self-join, you must copy the DataFrame:

Copy code

```
# copy the DataFrame if you want to do a self-join
from copy import copy

# Create two DataFrames to join
df_lhs = session.create_dataframe([["a", 1], ["b", 2]], schema=["key", "value1"])
df_rhs = session.create_dataframe([["a", 3], ["b", 4]], schema=["key", "value2"])
df_lhs_copied = copy(df_lhs)
df_self_joined = df_lhs.join(df_lhs_copied, (df_lhs.col("key") == df_lhs_copied.col("key")) & (df_lhs.col("value1") == df_lhs_copied.col("value1")))
```

When there are overlapping columns in the DataFrames, Snowpark prepends a randomly generated prefix to the columns in the join result:

Copy code

```
# Create two DataFrames to join
df_lhs = session.create_dataframe([["a", 1], ["b", 2]], schema=["key", "value1"])
df_rhs = session.create_dataframe([["a", 3], ["b", 4]], schema=["key", "value2"])
df_lhs.join(df_rhs, df_lhs.col("key") == df_rhs.col("key")).show()
# To return the DataFrame as a table in a Python worksheet use return instead of show()
return df_lhs.join(df_rhs, df_lhs.col("key") == df_rhs.col("key"))
```

```
-----------------------------------------------------
|"l_av5t_KEY"  |"VALUE1"  |"r_1p6k_KEY"  |"VALUE2"  |
-----------------------------------------------------
|a             |1         |a             |3         |
|b             |2         |b             |4         |
-----------------------------------------------------
```

You can rename the overlapping columns using `Column.alias`:

Copy code

```
# Create two DataFrames to join
df_lhs = session.create_dataframe([["a", 1], ["b", 2]], schema=["key", "value1"])
df_rhs = session.create_dataframe([["a", 3], ["b", 4]], schema=["key", "value2"])
df_lhs.join(df_rhs, df_lhs.col("key") == df_rhs.col("key")).select(df_lhs["key"].alias("key1"), df_rhs["key"].alias("key2"), "value1", "value2").show()
# To return the DataFrame as a table in a Python worksheet use return instead of show()
return df_lhs.join(df_rhs, df_lhs.col("key") == df_rhs.col("key")).select(df_lhs["key"].alias("key1"), df_rhs["key"].alias("key2"), "value1", "value2")
```

```
-----------------------------------------
|"KEY1"  |"KEY2"  |"VALUE1"  |"VALUE2"  |
-----------------------------------------
|a       |a       |1         |3         |
|b       |b       |2         |4         |
-----------------------------------------
```

To avoid random prefixes, you can also specify a suffix to append to the overlapping columns:

Copy code

```
# Create two DataFrames to join
df_lhs = session.create_dataframe([["a", 1], ["b", 2]], schema=["key", "value1"])
df_rhs = session.create_dataframe([["a", 3], ["b", 4]], schema=["key", "value2"])
df_lhs.join(df_rhs, df_lhs.col("key") == df_rhs.col("key"), lsuffix="_left", rsuffix="_right").show()
# To return the DataFrame as a table in a Python worksheet use return instead of show()
return df_lhs.join(df_rhs, df_lhs.col("key") == df_rhs.col("key"), lsuffix="_left", rsuffix="_right")
```

```
--------------------------------------------------
|"KEY_LEFT"  |"VALUE1"  |"KEY_RIGHT"  |"VALUE2"  |
--------------------------------------------------
|a           |1         |a            |3         |
|b           |2         |b            |4         |
--------------------------------------------------
```

These examples use `DataFrame.col` to specify the columns to use in the join.
Refer to [Specifying Columns and Expressions](#label-snowpark-python-dataframe-cols-and-expressions) for more ways to specify columns.

If you need to join a table with itself on different columns, you cannot perform the self-join with a single DataFrame. The
following examples use a single DataFrame to perform a self-join, which fails because the column expressions for `"id"` are
present in the left and right sides of the join:

Copy code

```
from snowflake.snowpark.exceptions import SnowparkJoinException

df = session.table("sample_product_data")
# This fails because columns named "id" and "parent_id"
# are in the left and right DataFrames in the join.
try:
  df_joined = df.join(df, col("id") == col("parent_id")) # fails
except SnowparkJoinException as e:
  print(e.message)
```

```
You cannot join a DataFrame with itself because the column references cannot be resolved correctly. Instead, create a copy of the DataFrame with copy.copy(), and join the DataFrame with this copy.
```

Copy code

```
# This fails because columns named "id" and "parent_id"
# are in the left and right DataFrames in the join.
try:
  df_joined = df.join(df, df["id"] == df["parent_id"])   # fails
except SnowparkJoinException as e:
  print(e.message)
```

```
You cannot join a DataFrame with itself because the column references cannot be resolved correctly. Instead, create a copy of the DataFrame with copy.copy(), and join the DataFrame with this copy.
```

Instead, use Python’s builtin `copy()` method to create a clone of the DataFrame object, and use the two DataFrame
objects to perform the join:

Copy code

```
from copy import copy

# Create a DataFrame object for the "sample_product_data" table for the left-hand side of the join.
df_lhs = session.table("sample_product_data")
# Clone the DataFrame object to use as the right-hand side of the join.
df_rhs = copy(df_lhs)

# Create a DataFrame that joins the two DataFrames
# for the "sample_product_data" table on the
# "id" and "parent_id" columns.
df_joined = df_lhs.join(df_rhs, df_lhs.col("id") == df_rhs.col("parent_id"))
df_joined.count()
```

### Specifying Columns and Expressions

When calling these transformation methods, you might need to specify columns or expressions that use columns. For example, when
calling the `select` method, you need to specify the columns to select.

To refer to a column, create a `Column` object by calling the `col` function in the
`snowflake.snowpark.functions` module.

Copy code

```
# Import the col function from the functions module.
from snowflake.snowpark.functions import col

df_product_info = session.table("sample_product_data").select(col("id"), col("name"))
df_product_info.show()
# To return the DataFrame as a table in a Python worksheet use return instead of show()
return df_product_info
```

```
---------------------
|"ID"  |"NAME"      |
---------------------
|1     |Product 1   |
|2     |Product 1A  |
|3     |Product 1B  |
|4     |Product 2   |
|5     |Product 2A  |
|6     |Product 2B  |
|7     |Product 3   |
|8     |Product 3A  |
|9     |Product 3B  |
|10    |Product 4   |
---------------------
```

Note

To create a `Column` object for a literal, refer to [Using Literals as Column Objects](#label-snowpark-python-dataframe-cols-lit).

When specifying a filter, projection, join condition, etc., you can use `Column` objects in an expression. For example:

- You can use `Column` objects with the `filter` method to specify a filter condition:

  Copy code

  ```
  # Specify the equivalent of "WHERE id = 20"
  # in a SQL SELECT statement.
  df_filtered = df.filter(col("id") == 20)
  ```

  Copy code

  ```
  df = session.create_dataframe([[1, 3], [2, 10]], schema=["a", "b"])
  # Specify the equivalent of "WHERE a + b < 10"
  # in a SQL SELECT statement.
  df_filtered = df.filter((col("a") + col("b")) < 10)
  df_filtered.show()
  # To return the DataFrame as a table in a Python worksheet use return instead of show()
  return df_filtered
  ```

  ```
  -------------
  |"A"  |"B"  |
  -------------
  |1    |3    |
  -------------
  ```
- You can use `Column` objects with the `select` method to define an alias:

  Copy code

  ```
  df = session.create_dataframe([[1, 3], [2, 10]], schema=["a", "b"])
  # Specify the equivalent of "SELECT b * 10 AS c"
  # in a SQL SELECT statement.
  df_selected = df.select((col("b") * 10).as_("c"))
  df_selected.show()
  # To return the DataFrame as a table in a Python worksheet use return instead of show()
  return df_selected
  ```

  ```
  -------
  |"C"  |
  -------
  |30   |
  |100  |
  -------
  ```
- You can use `Column` objects with the `join` method to define a join condition:

  Copy code

  ```
  dfX = session.create_dataframe([[1], [2]], schema=["a_in_X"])
  dfY = session.create_dataframe([[1], [3]], schema=["b_in_Y"])
  # Specify the equivalent of "X JOIN Y on X.a_in_X = Y.b_in_Y"
  # in a SQL SELECT statement.
  df_joined = dfX.join(dfY, col("a_in_X") == col("b_in_Y")).select(dfX["a_in_X"].alias("the_joined_column"))
  df_joined.show()
  # To return the DataFrame as a table in a Python worksheet use return instead of show()
  return df_joined
  ```

  ```
  -----------------------
  |"THE_JOINED_COLUMN"  |
  -----------------------
  |1                    |
  -----------------------
  ```

When referring to columns in two different DataFrame objects that have the same name (for example, joining the DataFrames on that
column), you can use the `DataFrame.col` method in one DataFrame object to refer to a column in that object (for example,
`df1.col("name")` and `df2.col("name")`).

The following example demonstrates how to use the `DataFrame.col` method to refer to a column in a specific DataFrame. The
example joins two DataFrame objects that both have a column named `key`. The example uses the `Column.as` method to change
the names of the columns in the newly created DataFrame.

Copy code

```
# Create two DataFrames to join
df_lhs = session.create_dataframe([["a", 1], ["b", 2]], schema=["key", "value"])
df_rhs = session.create_dataframe([["a", 3], ["b", 4]], schema=["key", "value"])
# Create a DataFrame that joins two other DataFrames (df_lhs and df_rhs).
# Use the DataFrame.col method to refer to the columns used in the join.
df_joined = df_lhs.join(df_rhs, df_lhs.col("key") == df_rhs.col("key")).select(df_lhs.col("key").as_("key"), df_lhs.col("value").as_("L"), df_rhs.col("value").as_("R"))
df_joined.show()
# To return the DataFrame as a table in a Python worksheet use return instead of show()
return df_joined
```

```
---------------------
|"KEY"  |"L"  |"R"  |
---------------------
|a      |1    |3    |
|b      |2    |4    |
---------------------
```

#### Using Double Quotes Around Object Identifiers (Table Names, Column Names, etc.)

The names of databases, schemas, tables, and stages that you specify must conform to the
[Snowflake identifier requirements](/sql-reference/identifiers-syntax).

Create a table that has case-sensitive columns:

Copy code

```
session.sql("""
  create or replace temp table "10tablename"(
  id123 varchar, -- case insensitive because it's not quoted.
  "3rdID" varchar, -- case sensitive.
  "id with space" varchar -- case sensitive.
)""").collect()
# Add return to the statement to return the collect() results in a Python worksheet
```

```
[Row(status='Table 10tablename successfully created.')]
```

Then add values to the table:

Copy code

```
session.sql("""insert into "10tablename" (id123, "3rdID", "id with space") values ('a', 'b', 'c')""").collect()
# Add return to the statement to return the collect() results in a Python worksheet
```

```
[Row(number of rows inserted=1)]
```

Then create a DataFrame for the table and query the table:

Copy code

```
df = session.table('"10tablename"')
df.show()
# To return the DataFrame as a table in a Python worksheet use return instead of show()
return df
```

```
---------------------------------------
|"ID123"  |"3rdID"  |"id with space"  |
---------------------------------------
|a        |b        |c                |
---------------------------------------
```

When you specify a name, Snowflake considers the
name to be in upper case. For example, the following calls are equivalent:

Copy code

```
df.select(col("id123")).collect()
# Prepend a return statement to return the collect() results in a Python worksheet
```

```
[Row(ID123='a')]
```

If the name does not conform to the identifier requirements, you must use double quotes (`"`) around the name. Use a backslash
(`\`) to escape the double quote character within a string literal. For example, the following table name does not start
with a letter or an underscore, so you must use double quotes around the name:

Copy code

```
df = session.table("\"10tablename\"")
```

Alternatively, you can use single quotes instead of backslashes to escape the double quote character within a string literal.

Copy code

```
df = session.table('"10tablename"')
```

Note that when specifying the name of a Column, you don’t need to use double quotes around the name. The Snowpark library
automatically encloses the column name in double quotes for you if the name does not comply with the identifier requirements:

Copy code

```
df.select(col("3rdID")).collect()
# Prepend a return statement to return the collect() results in a Python worksheet
```

```
[Row(3rdID='b')]
```

As another example, the following calls are equivalent:

Copy code

```
df.select(col("id with space")).collect()
# Prepend a return statement to return the collect() results in a Python worksheet
```

```
[Row(id with space='c')]
```

Copy code

```
df.select(col("\"id with space\"")).collect()
# Prepend a return statement to return the collect() results in a Python worksheet
```

```
[Row(id with space='c')]
```

If you have already added double quotes around a column name, the library does not insert additional double quotes around the
name.

In some cases, the column name might contain double quote characters:

Copy code

```
session.sql('''
  create or replace temp table quoted(
  "name_with_""air""_quotes" varchar,
  """column_name_quoted""" varchar
)''').collect()
# Prepend a return statement to return the collect() results in a Python worksheet
```

```
[Row(status='Table QUOTED successfully created.')]
```

Copy code

```
session.sql('''insert into quoted ("name_with_""air""_quotes", """column_name_quoted""") values ('a', 'b')''').collect()
# Prepend a return statement to return the collect() results in a Python worksheet
```

```
[Row(number of rows inserted=1)]
```

As explained in [Identifier requirements](/sql-reference/identifiers-syntax), for each double quote character within a double-quoted identifier, you
must use two double quote characters (e.g. `"name_with_""air""_quotes"` and `"""column_name_quoted"""`):

Copy code

```
df_table = session.table("quoted")
df_table.select("\"name_with_\"\"air\"\"_quotes\"").collect()
# Prepend a return statement to return the collect() results in a Python worksheet
```

```
[Row(name_with_"air"_quotes='a')]
```

Copy code

```
df_table.select("\"\"\"column_name_quoted\"\"\"").collect()
# Prepend a return statement to return the collect() results in a Python worksheet
```

```
[Row("column_name_quoted"='b')]
```

When an identifier is enclosed in double quotes (whether you explicitly added the quotes or the library added
the quotes for you), [Snowflake treats the identifier as case-sensitive](/sql-reference/identifiers-syntax):

Copy code

```
# The following calls are NOT equivalent!
# The Snowpark library adds double quotes around the column name,
# which makes Snowflake treat the column name as case-sensitive.
df.select(col("id with space")).collect()
# Prepend a return statement to return the collect() results in a Python worksheet
```

```
[Row(id with space='c')]
```

Compared with this example:

Copy code

```
from snowflake.snowpark.exceptions import SnowparkSQLException
try:
  df.select(col("ID WITH SPACE")).collect()
except SnowparkSQLException as e:
  print(e.message)
```

```
000904 (42000): SQL compilation error: error line 1 at position 7
invalid identifier '"ID WITH SPACE"'
```

### Using Literals as Column Objects

To use a literal in a method that takes a `Column` object as an argument, create a `Column` object for the literal by passing
the literal to the `lit` function in the `snowflake.snowpark.functions` module. For example:

Copy code

```
# Import for the lit and col functions.
from snowflake.snowpark.functions import col, lit

# Show the first 10 rows in which num_items is greater than 5.
# Use `lit(5)` to create a Column object for the literal 5.
df_filtered = df.filter(col("num_items") > lit(5))
```

### Casting a Column Object to a Specific Type

To cast a `Column` object to a specific type, call the `cast` method, and pass in a type object from the
`snowflake.snowpark.types` module. For example, to cast a literal
as a [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) with a precision of 5 and a scale of 2:

Copy code

```
# Import for the lit function.
from snowflake.snowpark.functions import lit

 # Import for the DecimalType class.
from snowflake.snowpark.types import DecimalType

decimal_value = lit(0.05).cast(DecimalType(5,2))
```

### Chaining Method Calls

Because each [method that transforms a DataFrame object](#label-snowpark-python-dataframe-transform) returns a new DataFrame object
that has the transformation applied, you can [chain method calls](https://en.wikipedia.org/wiki/Method_chaining) to produce a
new DataFrame that is transformed in additional ways.

The following example returns a DataFrame that is configured to:

- Query the `sample_product_data` table.
- Return the row with `id = 1`.
- Select the `name` and `serial_number` columns.

  Copy code

  ```
  df_product_info = session.table("sample_product_data").filter(col("id") == 1).select(col("name"), col("serial_number"))
  df_product_info.show()
  # To return the DataFrame as a table in a Python worksheet use return instead of show()
  return df_product_info
  ```

  ```
  -------------------------------
  |"NAME"     |"SERIAL_NUMBER"  |
  -------------------------------
  |Product 1  |prod-1           |
  -------------------------------
  ```

In this example:

- `session.table("sample_product_data")` returns a DataFrame for the `sample_product_data` table.

  Although the DataFrame does not yet contain the data from the table, the object does contain the definitions of the columns in
  the table.
- `filter(col("id") == 1)` returns a DataFrame for the `sample_product_data` table that is set up to return the row with
  `id = 1`.

  Note that the DataFrame does not yet contain the matching row from the table. The matching row is not retrieved until you
  [call an action method](#label-snowpark-python-dataframe-action-method).
- `select(col("name"), col("serial_number"))` returns a DataFrame that contains the `name` and `serial_number` columns
  for the row in the `sample_product_data` table that has `id = 1`.

The order of calls is important when you chain method calls. Each method call returns a DataFrame that has been
transformed. Make sure that subsequent calls work with the transformed DataFrame.

When using Snowpark Python, you might need to make the `select` and `filter` method calls in a different order than you would
use the equivalent keywords (SELECT and WHERE) in a SQL statement.

### Retrieving Column Definitions

To retrieve the definition of the columns in the dataset for the DataFrame, call the `schema` property. This method returns
a `StructType` object that contains an `list` of `StructField` objects. Each `StructField` object
contains the definition of a column.

Copy code

```
# Import the StructType
from snowflake.snowpark.types import *
# Get the StructType object that describes the columns in the
# underlying rowset.
table_schema = session.table("sample_product_data").schema
table_schema
StructType([StructField('ID', LongType(), nullable=True), StructField('PARENT_ID', LongType(), nullable=True), StructField('CATEGORY_ID', LongType(), nullable=True), StructField('NAME', StringType(), nullable=True), StructField('SERIAL_NUMBER', StringType(), nullable=True), StructField('KEY', LongType(), nullable=True), StructField('"3rd"', LongType(), nullable=True)])
```

In the returned `StructType` object, the column names are always normalized. Unquoted identifiers are returned in uppercase,
and quoted identifiers are returned in the exact case in which they were defined.

The following example creates a DataFrame containing the columns named `ID` and `3rd`. For the column name `3rd`, the
Snowpark library automatically encloses the name in double quotes (`"3rd"`) because
[the name does not comply with the requirements for an identifier](#label-snowpark-python-dataframe-cols-identifiers).

The example calls the `schema` property and then calls the `names` property on the returned `StructType` object to
get a `list` of column names. The names are normalized in the `StructType` returned by the `schema` property.

Copy code

```
# Create a DataFrame containing the "id" and "3rd" columns.
df_selected_columns = session.table("sample_product_data").select(col("id"), col("3rd"))
# Print out the names of the columns in the schema.
# This prints List["ID", "\"3rd\""]
df_selected_columns.schema.names
```

```
['ID', '"3rd"']
```

## Performing an Action to Evaluate a DataFrame

As mentioned earlier, the DataFrame is lazily evaluated, which means the SQL statement isn’t sent to the server for execution
until you perform an action. An action causes the DataFrame to be evaluated and sends the corresponding SQL statement to the
server for execution.

The following methods perform an action:

| Class | Method | Description |
| --- | --- | --- |
| `DataFrame` | `collect` | Evaluates the DataFrame and returns the resulting dataset as an `list` of `Row` objects. |
| `DataFrame` | `count` | Evaluates the DataFrame and returns the number of rows. |
| `DataFrame` | `show` | Evaluates the DataFrame and prints the rows to the console. This method limits the number of rows to 10 (by default). |
| `DataFrameWriter` | `save_as_table` | Saves the data in the DataFrame to the specified table. Refer to [Saving Data to a Table](#label-snowpark-python-dataframe-save-table). |

Expand

Show lessSee more

For example, to execute a query against a table and return the results, call the `collect` method:

Copy code

```
# Create a DataFrame with the "id" and "name" columns from the "sample_product_data" table.
# This does not execute the query.
df = session.table("sample_product_data").select(col("id"), col("name"))

# Send the query to the server for execution and
# return a list of Rows containing the results.
results = df.collect()
# Use a return statement to return the collect() results in a Python worksheet
# return results
```

To execute the query and return the number of results, call the `count` method:

Copy code

```
# Create a DataFrame for the "sample_product_data" table.
df_products = session.table("sample_product_data")

# Send the query to the server for execution and
# print the count of rows in the table.
print(df_products.count())
12
```

To execute a query and print the results to the console, call the `show` method:

Copy code

```
# Create a DataFrame for the "sample_product_data" table.
df_products = session.table("sample_product_data")

# Send the query to the server for execution and
# print the results to the console.
# The query limits the number of rows to 10 by default.
df_products.show()
# To return the DataFrame as a table in a Python worksheet use return instead of show()
return df_products
```

```
-------------------------------------------------------------------------------------
|"ID"  |"PARENT_ID"  |"CATEGORY_ID"  |"NAME"      |"SERIAL_NUMBER"  |"KEY"  |"3rd"  |
-------------------------------------------------------------------------------------
|1     |0            |5              |Product 1   |prod-1           |1      |10     |
|2     |1            |5              |Product 1A  |prod-1-A         |1      |20     |
|3     |1            |5              |Product 1B  |prod-1-B         |1      |30     |
|4     |0            |10             |Product 2   |prod-2           |2      |40     |
|5     |4            |10             |Product 2A  |prod-2-A         |2      |50     |
|6     |4            |10             |Product 2B  |prod-2-B         |2      |60     |
|7     |0            |20             |Product 3   |prod-3           |3      |70     |
|8     |7            |20             |Product 3A  |prod-3-A         |3      |80     |
|9     |7            |20             |Product 3B  |prod-3-B         |3      |90     |
|10    |0            |50             |Product 4   |prod-4           |4      |100    |
-------------------------------------------------------------------------------------
```

To limit the number of rows to 20:

Copy code

```
# Create a DataFrame for the "sample_product_data" table.
df_products = session.table("sample_product_data")

# Limit the number of rows to 20, rather than 10.
df_products.show(20)
# All rows are returned when you use return in a Python worksheet to return the DataFrame as a table
return df_products
```

```
-------------------------------------------------------------------------------------
|"ID"  |"PARENT_ID"  |"CATEGORY_ID"  |"NAME"      |"SERIAL_NUMBER"  |"KEY"  |"3rd"  |
-------------------------------------------------------------------------------------
|1     |0            |5              |Product 1   |prod-1           |1      |10     |
|2     |1            |5              |Product 1A  |prod-1-A         |1      |20     |
|3     |1            |5              |Product 1B  |prod-1-B         |1      |30     |
|4     |0            |10             |Product 2   |prod-2           |2      |40     |
|5     |4            |10             |Product 2A  |prod-2-A         |2      |50     |
|6     |4            |10             |Product 2B  |prod-2-B         |2      |60     |
|7     |0            |20             |Product 3   |prod-3           |3      |70     |
|8     |7            |20             |Product 3A  |prod-3-A         |3      |80     |
|9     |7            |20             |Product 3B  |prod-3-B         |3      |90     |
|10    |0            |50             |Product 4   |prod-4           |4      |100    |
|11    |10           |50             |Product 4A  |prod-4-A         |4      |100    |
|12    |10           |50             |Product 4B  |prod-4-B         |4      |100    |
-------------------------------------------------------------------------------------
```

Note

If you call the `schema` property to get the definitions of the columns in the DataFrame, you do not need to
call an action method.

## Saving Data to a Table

To save the contents of a DataFrame to a table:

1. Call the `write` property to get a `DataFrameWriter` object.
2. Call the `mode` method in the `DataFrameWriter` object and specify the mode.
   For more information, see [the API documentation](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.DataFrameWriter.mode#snowflake.snowpark.DataFrameWriter.mode).
   This method returns a new `DataFrameWriter` object that is configured with the specified mode.
3. Call the `save_as_table` method in the `DataFrameWriter` object to save the contents of the DataFrame to a
   specified table.

Note that you do not need to call a separate method (e.g. `collect`) to execute the SQL statement that saves the data to the
table.

For example:

Copy code

```
df.write.mode("overwrite").save_as_table("table1")
```

## Creating a View From a DataFrame

To create a view from a DataFrame, call the `create_or_replace_view` method, which immediately creates the new view:

Copy code

```
import os
database = os.environ["snowflake_database"]  # use your own database and schema
schema = os.environ["snowflake_schema"]
view_name = "my_view"
df.create_or_replace_view(f"{database}.{schema}.{view_name}")
```

```
[Row(status='View MY_VIEW successfully created.')]
```

In a Python worksheet, because you run the worksheet in the context of a database and schema, you can run the following to create a view:

Copy code

```
# Define a DataFrame
df_products = session.table("sample_product_data")
# Define a View name
view_name = "my_view"
# Create the view
df_products.create_or_replace_view(f"{view_name}")
# return the view name
return view_name + " successfully created"
my_view successfully created
```

Views that you create by calling `create_or_replace_view` are persistent. If you no longer need that view, you can
[drop the view manually](/sql-reference/sql/drop-view).

Alternatively, use the `create_or_replace_temp_view` method, which creates a temporary view.
The temporary view is only available in the session in which it is created.

## Working With Files in a Stage

This section explains how to query data in a file in a Snowflake stage. For other operations on files,
[use SQL statements](#label-snowpark-python-dataframe-execute-sql).

To query data in files in a Snowflake stage, use the `DataFrameReader` class:

1. Call the `read` method in the `Session` class to access a `DataFrameReader` object.
2. If the files are in CSV format, describe the fields in the file. To do this:

   1. Create a `StructType` object that consists of a `list` of `StructField` objects that describe the fields in
      the file.
   2. For each `StructField` object, specify the following:

      - The name of the field.
      - The data type of the field (specified as an object in the `snowflake.snowpark.types` module).
      - Whether or not the field is nullable.

      For example:

      Copy code

      ```
      from snowflake.snowpark.types import *

      schema_for_data_file = StructType([
                          StructField("id", StringType()),
                          StructField("name", StringType())
                       ])
      ```
   3. Call the `schema` property in the `DataFrameReader` object, passing in the `StructType` object.

      For example:

      Copy code

      ```
      df_reader = session.read.schema(schema_for_data_file)
      ```

      The `schema` property returns a `DataFrameReader` object that is configured to read files containing the specified
      fields.

      Note that you do not need to do this for files in other formats (such as JSON). For those files, the
      `DataFrameReader` treats the data as a single field of the VARIANT type with the field name `$1`.
3. If you need to specify additional information about how the data should be read (for example, that the data is compressed or
   that a CSV file uses a semicolon instead of a comma to delimit fields), call the `option` or `options` methods of the
   `DataFrameReader` object.

   The `option` method takes a name and a value of the option that you want to set and lets you combine multiple chained calls
   whereas the `options` method takes a dictionary of the names of options and their corresponding values.

   For the names and values of the file format options, see the
   [documentation on CREATE FILE FORMAT](/sql-reference/sql/create-file-format).

   You can also set the copy options described in the [COPY INTO TABLE documentation](/sql-reference/sql/copy-into-table).
   Note that setting copy options can result in a more expensive execution strategy when you
   [retrieve the data into the DataFrame](#label-snowpark-python-dataframe-action-method).

   The following example sets up the `DataFrameReader` object to query data in a CSV file that is not compressed and that
   uses a semicolon for the field delimiter.

   Copy code

   ```
   df_reader = df_reader.option("field_delimiter", ";").option("COMPRESSION", "NONE")
   ```

   The `option` and `options` methods return a `DataFrameReader` object that is configured with the specified options.
4. Call the method corresponding to the format of the file (e.g. the `csv` method), passing in the location of the file.

   Copy code

   ```
   df = df_reader.csv("@s3_ts_stage/emails/data_0_0_0.csv")
   ```

   The methods corresponding to the format of a file return a DataFrame object that is configured to hold the data in that file.
5. Use the DataFrame object methods to [perform any transformations](#label-snowpark-python-dataframe-transform) needed on the
   dataset (for example, selecting specific fields, filtering rows, etc.).

   For example, to extract the `color` element from a JSON file in the stage named `my_stage`:

   Copy code

   ```
   # Import the sql_expr function from the functions module.
   from snowflake.snowpark.functions import sql_expr

   df = session.read.json("@my_stage").select(sql_expr("$1:color"))
   ```

   As explained earlier, for files in formats other than CSV (e.g. JSON), the `DataFrameReader` treats the data in the file
   as a single VARIANT column with the name `$1`.

   This example uses the `sql_expr` function in the `snowflake.snowpark.functions` module to specify the path to
   the `color` element.

   Note that the `sql_expr` function does not interpret or modify the input argument. The function just allows you to
   construct expressions and snippets in SQL that are not yet supported by the Snowpark API.
6. [Call an action method](#label-snowpark-python-dataframe-action-method) to query the data in the file.

   As is the case with DataFrames for tables, the data is not retrieved into the DataFrame until you call an action method.

## Working with Semi-Structured Data

Using a DataFrame, you can query and access [semi-structured data](/user-guide/semistructured-intro) (e.g JSON data). The
next sections explain how to work with semi-structured data in a DataFrame.

- [Traversing Semi-Structured Data](#label-snowpark-python-dataframe-semistructured-traverse)
- [Explicitly Casting Values in Semi-Structured Data](#label-snowpark-python-dataframe-semistructured-cast)
- [Flattening an Array of Objects into Rows](#label-snowpark-python-dataframe-semistructured-flatten)

Note

The examples in these sections use the sample data in [Sample Data Used in Examples](/user-guide/querying-semistructured#label-sample-data-semistructured-data).

### Traversing Semi-Structured Data

To refer to a specific field or element in semi-structured data, use the following methods of the `Column` object:

- Get attribute `col_object["<field_name>"]` to return a `Column` object for a field in an OBJECT (or a VARIANT that contains an
  OBJECT).
- Use `col_object[<index>]` to return a `Column` object for an element in an ARRAY (or a VARIANT that contains an ARRAY).

Note

If the field name or elements in the path are irregular and make it difficult to use the indexing described above, you can
use `get`, `get_ignore_case`, or `get_path` as an alternative.

For example, the following code selects the `dealership` field in objects in the `src` column of the
[sample data](/user-guide/querying-semistructured#label-sample-data-semistructured-data):

Copy code

```
from snowflake.snowpark.functions import col

df = session.table("car_sales")
df.select(col("src")["dealership"]).show()
```

The code prints the following output:

```
----------------------------
|"""SRC""['DEALERSHIP']"   |
----------------------------
|"Valley View Auto Sales"  |
|"Tindel Toyota"           |
----------------------------
```

Note

The values in the DataFrame are surrounded by double quotes because these values are returned as string literals. To cast these
values to a specific type, see [Explicitly Casting Values in Semi-Structured Data](#label-snowpark-python-dataframe-semistructured-cast).

You can also [chain method calls](#label-snowpark-python-dataframe-chaining-method-calls) to traverse a path to a specific
field or element.

For example, the following code selects the `name` field in the `salesperson` object:

Copy code

```
df = session.table("car_sales")
df.select(df["src"]["salesperson"]["name"]).show()
```

The code prints the following output:

```
------------------------------------
|"""SRC""['SALESPERSON']['NAME']"  |
------------------------------------
|"Frank Beasley"                   |
|"Greg Northrup"                   |
------------------------------------
```

As another example, the following code selects the first element of `vehicle` field, which holds an array of vehicles. The
example also selects the `price` field from the first element.

Copy code

```
df = session.table("car_sales")
df.select(df["src"]["vehicle"][0]).show()
df.select(df["src"]["vehicle"][0]["price"]).show()
```

The code prints the following output:

```
---------------------------
|"""SRC""['VEHICLE'][0]"  |
---------------------------
|{                        |
|  "extras": [            |
|    "ext warranty",      |
|    "paint protection"   |
|  ],                     |
|  "make": "Honda",       |
|  "model": "Civic",      |
|  "price": "20275",      |
|  "year": "2017"         |
|}                        |
|{                        |
|  "extras": [            |
|    "ext warranty",      |
|    "rust proofing",     |
|    "fabric protection"  |
|  ],                     |
|  "make": "Toyota",      |
|  "model": "Camry",      |
|  "price": "23500",      |
|  "year": "2017"         |
|}                        |
---------------------------

------------------------------------
|"""SRC""['VEHICLE'][0]['PRICE']"  |
------------------------------------
|"20275"                           |
|"23500"                           |
------------------------------------
```

As an alternative to access fields in aforementioned way, you can use `get`, `get_ignore_case`, or
`get_path` functions if the field name or elements in the path are irregular.

For example, the following lines of code both print the value of a specified field in an object:

Copy code

```
from snowflake.snowpark.functions import get, get_path, lit

df.select(get(col("src"), lit("dealership"))).show()
df.select(col("src")["dealership"]).show()
```

Similarly, the following lines of code both print the value of a field at a specified path in an object:

Copy code

```
df.select(get_path(col("src"), lit("vehicle[0].make"))).show()
df.select(col("src")["vehicle"][0]["make"]).show()
```

### Explicitly Casting Values in Semi-Structured Data

By default, the values of fields and elements are returned as string literals (including the double quotes), as shown in the
examples above.

To avoid unexpected results, call the [cast](#label-snowpark-python-dataframe-cols-cast) method to cast the value to a specific
type. For example, the following code prints out the values without and with casting:

Copy code

```
# Import the objects for the data types, including StringType.
from snowflake.snowpark.types import *

df = session.table("car_sales")
df.select(col("src")["salesperson"]["id"]).show()
df.select(col("src")["salesperson"]["id"].cast(StringType())).show()
```

The code prints the following output:

```
----------------------------------
|"""SRC""['SALESPERSON']['ID']"  |
----------------------------------
|"55"                            |
|"274"                           |
----------------------------------

---------------------------------------------------
|"CAST (""SRC""['SALESPERSON']['ID'] AS STRING)"  |
---------------------------------------------------
|55                                               |
|274                                              |
---------------------------------------------------
```

### Flattening an Array of Objects into Rows

If you need to “flatten” semi-structured data into a DataFrame (e.g. producing a row for every object in an array), call the
`flatten` using the `join_table_function` method. This method is equivalent to the [FLATTEN](/sql-reference/functions/flatten) SQL function. If you pass in
a path to an object or array, the method returns a DataFrame that contains a row for each field or element in the object or array.

For example, in the [sample data](/user-guide/querying-semistructured#label-sample-data-semistructured-data), `src:customer` is an array of objects that
contain information about a customer. Each object contains a `name` and `address` field.

If you pass this path to the `flatten` function:

Copy code

```
df = session.table("car_sales")
df.join_table_function("flatten", col("src")["customer"]).show()
```

the method returns a DataFrame:

```
----------------------------------------------------------------------------------------------------------------------------------------------------------
|"SRC"                                      |"SEQ"  |"KEY"  |"PATH"  |"INDEX"  |"VALUE"                            |"THIS"                               |
----------------------------------------------------------------------------------------------------------------------------------------------------------
|{                                          |1      |NULL   |[0]     |0        |{                                  |[                                    |
|  "customer": [                            |       |       |        |         |  "address": "San Francisco, CA",  |  {                                  |
|    {                                      |       |       |        |         |  "name": "Joyce Ridgely",         |    "address": "San Francisco, CA",  |
|      "address": "San Francisco, CA",      |       |       |        |         |  "phone": "16504378889"           |    "name": "Joyce Ridgely",         |
|      "name": "Joyce Ridgely",             |       |       |        |         |}                                  |    "phone": "16504378889"           |
|      "phone": "16504378889"               |       |       |        |         |                                   |  }                                  |
|    }                                      |       |       |        |         |                                   |]                                    |
|  ],                                       |       |       |        |         |                                   |                                     |
|  "date": "2017-04-28",                    |       |       |        |         |                                   |                                     |
|  "dealership": "Valley View Auto Sales",  |       |       |        |         |                                   |                                     |
|  "salesperson": {                         |       |       |        |         |                                   |                                     |
|    "id": "55",                            |       |       |        |         |                                   |                                     |
|    "name": "Frank Beasley"                |       |       |        |         |                                   |                                     |
|  },                                       |       |       |        |         |                                   |                                     |
|  "vehicle": [                             |       |       |        |         |                                   |                                     |
|    {                                      |       |       |        |         |                                   |                                     |
|      "extras": [                          |       |       |        |         |                                   |                                     |
|        "ext warranty",                    |       |       |        |         |                                   |                                     |
|        "paint protection"                 |       |       |        |         |                                   |                                     |
|      ],                                   |       |       |        |         |                                   |                                     |
|      "make": "Honda",                     |       |       |        |         |                                   |                                     |
|      "model": "Civic",                    |       |       |        |         |                                   |                                     |
|      "price": "20275",                    |       |       |        |         |                                   |                                     |
|      "year": "2017"                       |       |       |        |         |                                   |                                     |
|    }                                      |       |       |        |         |                                   |                                     |
|  ]                                        |       |       |        |         |                                   |                                     |
|}                                          |       |       |        |         |                                   |                                     |
|{                                          |2      |NULL   |[0]     |0        |{                                  |[                                    |
|  "customer": [                            |       |       |        |         |  "address": "New York, NY",       |  {                                  |
|    {                                      |       |       |        |         |  "name": "Bradley Greenbloom",    |    "address": "New York, NY",       |
|      "address": "New York, NY",           |       |       |        |         |  "phone": "12127593751"           |    "name": "Bradley Greenbloom",    |
|      "name": "Bradley Greenbloom",        |       |       |        |         |}                                  |    "phone": "12127593751"           |
|      "phone": "12127593751"               |       |       |        |         |                                   |  }                                  |
|    }                                      |       |       |        |         |                                   |]                                    |
|  ],                                       |       |       |        |         |                                   |                                     |
|  "date": "2017-04-28",                    |       |       |        |         |                                   |                                     |
|  "dealership": "Tindel Toyota",           |       |       |        |         |                                   |                                     |
|  "salesperson": {                         |       |       |        |         |                                   |                                     |
|    "id": "274",                           |       |       |        |         |                                   |                                     |
|    "name": "Greg Northrup"                |       |       |        |         |                                   |                                     |
|  },                                       |       |       |        |         |                                   |                                     |
|  "vehicle": [                             |       |       |        |         |                                   |                                     |
|    {                                      |       |       |        |         |                                   |                                     |
|      "extras": [                          |       |       |        |         |                                   |                                     |
|        "ext warranty",                    |       |       |        |         |                                   |                                     |
|        "rust proofing",                   |       |       |        |         |                                   |                                     |
|        "fabric protection"                |       |       |        |         |                                   |                                     |
|      ],                                   |       |       |        |         |                                   |                                     |
|      "make": "Toyota",                    |       |       |        |         |                                   |                                     |
|      "model": "Camry",                    |       |       |        |         |                                   |                                     |
|      "price": "23500",                    |       |       |        |         |                                   |                                     |
|      "year": "2017"                       |       |       |        |         |                                   |                                     |
|    }                                      |       |       |        |         |                                   |                                     |
|  ]                                        |       |       |        |         |                                   |                                     |
|}                                          |       |       |        |         |                                   |                                     |
----------------------------------------------------------------------------------------------------------------------------------------------------------
```

From this DataFrame, you can select the `name` and `address` fields from each object in the `VALUE` field:

Copy code

```
df.join_table_function("flatten", col("src")["customer"]).select(col("value")["name"], col("value")["address"]).show()
```

```
-------------------------------------------------
|"""VALUE""['NAME']"   |"""VALUE""['ADDRESS']"  |
-------------------------------------------------
|"Joyce Ridgely"       |"San Francisco, CA"     |
|"Bradley Greenbloom"  |"New York, NY"          |
-------------------------------------------------
```

The following code adds to the previous example by
[casting the values to a specific type](#label-snowpark-python-dataframe-semistructured-cast) and changing the names of the columns:

Copy code

```
df.join_table_function("flatten", col("src")["customer"]).select(col("value")["name"].cast(StringType()).as_("Customer Name"), col("value")["address"].cast(StringType()).as_("Customer Address")).show()
```

```
-------------------------------------------
|"Customer Name"     |"Customer Address"  |
-------------------------------------------
|Joyce Ridgely       |San Francisco, CA   |
|Bradley Greenbloom  |New York, NY        |
-------------------------------------------
```

## Executing SQL Statements

To execute a SQL statement that you specify, call the `sql` method in the `Session` class, and pass in the statement
to be executed. The method returns a DataFrame.

Note that the SQL statement won’t be executed until you [call an action method](#label-snowpark-python-dataframe-action-method).

Copy code

```
# Get the list of the files in a stage.
# The collect() method causes this SQL statement to be executed.
session.sql("create or replace temp stage my_stage").collect()
```

```
# Prepend a return statement to return the collect() results in a Python worksheet
[Row(status='Stage area MY_STAGE successfully created.')]
```

Copy code

```
stage_files_df = session.sql("ls @my_stage").collect()
# Prepend a return statement to return the collect() results in a Python worksheet
# Resume the operation of a warehouse.
# Note that you must call the collect method to execute
# the SQL statement.
session.sql("alter warehouse if exists my_warehouse resume if suspended").collect()
```

```
# Prepend a return statement to return the collect() results in a Python worksheet
[Row(status='Statement executed successfully.')]
```

Copy code

```
# Set up a SQL statement to copy data from a stage to a table.
session.sql("copy into sample_product_data from @my_stage file_format=(type = csv)").collect()
# Prepend a return statement to return the collect() results in a Python worksheet
```

```
[Row(status='Copy executed with 0 files processed.')]
```

If you want to [call methods to transform the DataFrame](#label-snowpark-python-dataframe-transform)
(e.g. `filter`, `select`, etc.),
note that these methods work only if the underlying SQL statement is a SELECT statement. The transformation methods are not
supported for other kinds of SQL statements.

Copy code

```
df = session.sql("select id, parent_id from sample_product_data where id < 10")
# Because the underlying SQL statement for the DataFrame is a SELECT statement,
# you can call the filter method to transform this DataFrame.
results = df.filter(col("id") < 3).select(col("id")).collect()
# Prepend a return statement to return the collect() results in a Python worksheet

# In this example, the underlying SQL statement is not a SELECT statement.
df = session.sql("ls @my_stage")
# Calling the filter method results in an error.
try:
  df.filter(col("size") > 50).collect()
except SnowparkSQLException as e:
  print(e.message)
```

```
000904 (42000): SQL compilation error: error line 1 at position 104
invalid identifier 'SIZE'
```

## Submit Snowpark queries concurrently

Note

This feature requires Snowpark Library for Python version of 1.24 or greater and server version 8.46 or greater.

Thread-safe session objects allow different parts of your Snowpark Python code to run concurrently while using the same session. This enables multiple operations - such as transformations on multiple DataFrames - to be executed concurrently. This is particularly useful when you’re working with queries that can be processed independently on the Snowflake server and it aligns with a more traditional multithreading approach.

The Global Interpreter Lock (GIL) in Python is a mutex that protects access to Python objects, preventing multiple native threads from executing Python bytecode simultaneously. While I/O-bound operations can still benefit from Python’s threading model due to the GIL being released during I/O operations, CPU-bound threads will not achieve true parallelism because only one thread can execute at a time.

Moreover, when used inside Snowflake (e.g. in a stored procedure), the Snowpark Python server manages the Global Interpreter Lock (GIL) by releasing it before submitting queries to Snowflake. This ensures that true concurrency can be achieved when enqueuing multiple queries from separate threads. With this management, Snowpark allows multiple threads to submit queries concurrently, ensuring optimal parallel execution.

### Benefits of Using Thread-Safe Session Objects in Snowpark

The ability to run multiple DataFrame operations concurrently can bring the following benefits to Snowpark users:

- Improved Performance: Thread-safe session objects allow you to run multiple Snowpark Python queries concurrently, reducing overall runtime. For example, if you need to process several tables independently, this feature significantly cuts down the time it takes to complete the job, as you no longer need to wait for each table’s processing to finish before starting the next one.
- Efficient Compute Utilization: Submitting queries concurrently ensures that Snowflake’s compute resources are used efficiently, reducing idle times.
- Usability: Thread-safe session objects integrate seamlessly with Python’s native multithreading APIs, which allows developers to leverage Python’s built-in tools to control thread behavior and optimize parallel execution.

Thread-safe session objects and async jobs can complement each other depending on your use case. Async jobs are useful when you don’t need to wait for your jobs to finish, allowing for non-blocking execution without thread pool management. Thread-safe session objects, on the other hand, are useful when you want to submit multiple queries concurrently from the client side. In some cases, the code blocks can also contain async jobs, allowing both methods to be used together effectively.

Following are some examples where thread-safe session objects can enhance your data pipeline.

#### Example 1: Concurrent Loading of Multiple Tables

This example demonstrates loading data from three different CSV files into three separate tables using three threads to run the `COPY INTO` command concurrently.

Copy code

```
import threading
from snowflake.snowpark import Session

# Define the list of tables
tables = ["customers", "orders", "products"]

# Function to copy data from stage to tables
def execute_copy(table_name):
    try:
        # Read data from the stage using DataFrameReader
        df = (
            session.read.option("SKIP_HEADER", 1)
            .option("PATTERN", f"{table_name}[.]csv")
            .option("FORCE", True)
            .csv(f"@my_stage")
        )

        # Copy data into the target table
        df.copy_into_table(
            table_name=table_name, target_columns=session.table(table_name).columns
        )

    except Exception as e:
        print(f"Failed to copy data into {table_name}, Error: {e}")

# Create an empty list of threads
threads = []

# Loop through and start a thread for each table
for table in tables:
    thread = threading.Thread(target=execute_copy, args=(table,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()
```

#### Example 2: Concurrent Processing of Multiple Tables

This example demonstrates how you can use multiple threads to concurrently filter, aggregate, and insert data into a result table from each customer transaction table (transaction\_customer1, transaction\_customer2, and transaction\_customer3).

Copy code

```
from concurrent.futures import ThreadPoolExecutor
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, month, sum, lit

# List of customers
customers = ["customer1", "customer2", "customer3"]

# Define a function to process each customer transaction table
def process_customer_table(customer_name):
    table_name = f"transaction_{customer_name}"

    try:
        # Load the customer transaction table
        df = session.table(table_name)
        print(f"Processing {table_name}...")

        # Filter data by positive values and non null categories
        df_filtered = df.filter((col("value") > 0) & col("category").is_not_null())

        # Perform aggregation: Sum of value by category and month
        df_aggregated = df_filtered.with_column("month", month(col("date"))).with_column("customer_name", lit(customer_name)).group_by(col("category"), col("month"), col("customer_name")).agg(sum("value").alias("total_value"))

        # Save the processed data into a new result table
        df_aggregated.show()
        df_aggregated.write.save_as_table("aggregate_customers", mode="append")
        print(f"Data from {table_name} processed and saved")

    except Exception as e:
        print(f"Error processing {table_name}: {e}")

# Using ThreadPoolExecutor to handle concurrency
with ThreadPoolExecutor(max_workers=3) as executor:
    # Submit tasks for each customer table
    executor.map(process_customer_table, customers)

# Display the results from the aggregate table
session.table("aggregate_customers").show()
```

#### Limitations of Using Thread-Safe Session Objects

- If you need to manage multiple transactions concurrently, it’s important to use multiple session objects because multiple threads of a single session do not support concurrent transactions.
- Changing session runtime configurations (including Snowflake session variables like database, schema, warehouse, and client side configurations like cte\_optimization\_enabled, sql\_simplifier\_enabled) while other threads are active can lead to unexpected behavior. To avoid conflicts, it’s best to use separate session objects if different threads require distinct configurations. For example, if you need to perform operations on different databases in parallel, ensure each thread has its own session object rather than sharing the same session.

## Return the Contents of a DataFrame as a Pandas DataFrame

To return the contents of a DataFrame as a Pandas DataFrame, use the `to_pandas` method.

For example:

Copy code

```
python_df = session.create_dataframe(["a", "b", "c"])
pandas_df = python_df.to_pandas()
```

## Snowpark DataFrames vs Snowpark pandas DataFrame: Which should I choose?

By installing the Snowpark Python library, you have the option of using the [DataFrames API](/developer-guide/snowpark/python/working-with-dataframes) or [pandas on Snowflake](/developer-guide/snowpark/python/pandas-on-snowflake).

Snowpark DataFrames are modeled after PySpark, while Snowpark pandas is intended to extend the [Snowpark DataFrame](/developer-guide/snowpark/python/working-with-dataframes) functionality and provide a familiar interface to pandas users to facilitate easy migration and adoption. We recommend using the different APIs depending on your use case and preference:

| Use Snowpark pandas if you …. | Use Snowpark DataFrames if you … |
| --- | --- |
| Prefer working with or have existing code written in pandas | Prefer working with or have existing code written in Spark |
| Have workflow that involves interactive analysis and iterative exploration | Have workflow that involves batch processing and limited iterative development |
| Are familiar with working with DataFrame operations that get executed immediately | Are familiar with working with DataFrame operations that are lazily evaluated |
| Prefer data being consistent and ordered during the operations | Are Ok with data not being ordered |
| Are Ok with slightly slower performance compared to Snowpark DataFrames in favor of easier to use API | Performance is more important to you than ease of use |

Expand

Show lessSee more

From an implementation perspective, Snowpark DataFrames and pandas DataFrames are semantically different. Since Snowpark DataFrames are modeled after PySpark, it operates on the original data source, gets the most recent updated data, so it does not maintain order for operations. Snowpark pandas are modeled after pandas, which operate on a snapshot of the data, maintain order during the operation, and allow for order-based positional indexing. Order maintenance is useful for visual inspection of data in interactive data analysis.

For more information, see [Using pandas on Snowflake with Snowpark DataFrames](/developer-guide/snowpark/python/pandas-on-snowflake#label-snowpark-pandas-with-dataframes).
