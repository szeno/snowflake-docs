# Calling Functions and Stored Procedures in Snowpark Python

To process data in a DataFrame, you can call system-defined SQL functions, user-defined functions, and stored procedures. This
topic explains how to call these in Snowpark.

To process data in a DataFrame, you can call system-defined SQL functions, user-defined functions,
and stored procedures.

## Calling System-Defined Functions

If you need to call [system-defined SQL functions](/sql-reference-functions), use the equivalent functions in the
`snowflake.snowpark.functions` module.

The following example calls the `upper` function in the `functions` module (the equivalent of the system-defined
[UPPER](/sql-reference/functions/upper) function) to return the values in the name column of the
[sample\_product\_data](/developer-guide/snowpark/python/working-with-dataframes#label-snowpark-python-dataframe-example-setup) table with the letters in uppercase:

Copy code

```
# Import the upper function from the functions module.
from snowflake.snowpark.functions import upper, col
session.table("sample_product_data").select(upper(col("name")).alias("upper_name")).collect()
```

```
[Row(UPPER_NAME='PRODUCT 1'), Row(UPPER_NAME='PRODUCT 1A'), Row(UPPER_NAME='PRODUCT 1B'), Row(UPPER_NAME='PRODUCT 2'),
Row(UPPER_NAME='PRODUCT 2A'), Row(UPPER_NAME='PRODUCT 2B'), Row(UPPER_NAME='PRODUCT 3'), Row(UPPER_NAME='PRODUCT 3A'),
Row(UPPER_NAME='PRODUCT 3B'), Row(UPPER_NAME='PRODUCT 4'), Row(UPPER_NAME='PRODUCT 4A'), Row(UPPER_NAME='PRODUCT 4B')]
```

If a system-defined SQL function is not available in the functions module, you can use one of the following approaches:

- Use the `call_function` function to call the system-defined function.
- Use the `function` function to create a function object that you can use to call the system-defined function.

`call_function` and `function` are defined in the `snowflake.snowpark.functions` module.

For `call_function`, pass the name of the system-defined function as the first argument. If you need
to pass the values of columns to the system-defined function, define and pass
[Column](/developer-guide/snowpark/python/working-with-dataframes#label-snowpark-python-dataframe-cols-and-expressions) objects as additional arguments to the `call_function` function.

The following example calls the system-defined function [RADIANS](/sql-reference/functions/radians), passing in the value from the
column `col1`:

Copy code

```
# Import the call_function function from the functions module.
from snowflake.snowpark.functions import call_function
df = session.create_dataframe([[1, 2], [3, 4]], schema=["col1", "col2"])
# Call the system-defined function RADIANS() on col1.
df.select(call_function("radians", col("col1"))).collect()
```

```
[Row(RADIANS("COL1")=0.017453292519943295), Row(RADIANS("COL1")=0.05235987755982988)]
```

The `call_function` function returns a `Column`, which you can pass to the
[DataFrame transformation methods](/developer-guide/snowpark/python/working-with-dataframes#label-snowpark-python-dataframe-transform) (e.g. `filter`, `select`, etc.).

For `function`, pass the name of the system-defined function, and use the returned function object to call the
system-defined function. For example:

Copy code

```
# Import the call_function function from the functions module.
from snowflake.snowpark.functions import function

# Create a function object for the system-defined function RADIANS().
radians = function("radians")
df = session.create_dataframe([[1, 2], [3, 4]], schema=["col1", "col2"])
# Call the system-defined function RADIANS() on col1.
df.select(radians(col("col1"))).collect()
```

```
[Row(RADIANS("COL1")=0.017453292519943295), Row(RADIANS("COL1")=0.05235987755982988)]
```

## Calling User-Defined Functions (UDFs)

To call UDFs that you [registered by name](/developer-guide/snowpark/python/creating-udfs#label-snowpark-python-udf-inline-named) and UDFs that you created by executing CREATE
FUNCTION, use the `call_udf` function in the `snowflake.snowpark.functions` module. Pass the name of the UDF as the
first argument and any UDF parameters as additional arguments.

The following example calls the UDF function `minus_one`, passing in the values from the columns `col1` and `col2`. The
example passes the return value from `minus_one` to the `select` method of the DataFrame.

Copy code

```
# Import the call_udf function from the functions module.
from snowflake.snowpark.functions import call_udf

# Runs the scalar function 'minus_one' on col1 of df.
df = session.create_dataframe([[1, 2], [3, 4]], schema=["col1", "col2"])
df.select(call_udf("minus_one", col("col1"))).collect()
```

```
[Row(MINUS_ONE("COL1")=0), Row(MINUS_ONE("COL1")=2)]
```

## Calling User-Defined Table Functions (UDTFs)

To call UDTFs that you registered by name and UDTFs that you created by executing CREATE FUNCTION, use one of the functions listed below.
Both return a `DataFrame` representing a lazily-evaluated relational dataset.

Note that you can use these to also call other table functions, including the
[system-defined table functions](/sql-reference/functions-table#label-list-of-system-defined-table-functions).

For more information on registering a UDTF, see [Registering a UDTF](/developer-guide/snowpark/python/creating-udtfs#label-snowpark-python-udtf-register).

- To call the UDTF without specifying a lateral join, call the `table_function` function in the `snowflake.snowpark.Session` class.

  For the function reference and examples, see
  [Session.table\_function](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.Session.table_function).

  Code in the following example uses `table_function` to call the `generator_udtf` function registered with the `udtf`
  function.

  Copy code

  ```
  from snowflake.snowpark.types import IntegerType, StructField, StructType
  from snowflake.snowpark.functions import udtf, lit
  class GeneratorUDTF:
   def process(self, n):
       for i in range(n):
           yield (i, )
  generator_udtf = udtf(GeneratorUDTF, output_schema=StructType([StructField("number", IntegerType())]), input_types=[IntegerType()])
  session.table_function(generator_udtf(lit(3))).collect()
  ```

  ```
  [Row(NUMBER=0), Row(NUMBER=1), Row(NUMBER=2)]
  ```
- To make a call to the UDTF in which your call specifies a lateral join, use the `join_table_function` function in the
  `snowflake.snowpark.DataFrame` class.

  When you lateral join a UDTF, you can specify the PARTITION BY and ORDER BY clauses.

  For the function reference and examples, see
  [DataFrame.join\_table\_function](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.DataFrame.join_table_function.html#snowflake.snowpark.DataFrame.join_table_function).

  Code in the following example performs a lateral join, specifying the `partition_by` and `order_by` parameters. Code in this
  example first calls the `snowflake.snowpark.functions.table_function` function to create a function object representing the system-defined
  `SPLIT_TO_TABLE` function. It is this function object that `join_table_function` then calls.

  For the `snowflake.snowpark.functions.table_function` function reference, see
  [table\_function](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.functions.table_function.html#snowflake.snowpark.functions.table_function).
  For the `SPLIT_TO_TABLE` function reference, see [SPLIT\_TO\_TABLE](/sql-reference/functions/split_to_table).

  Copy code

  ```
  from snowflake.snowpark.functions import table_function
  split_to_table = table_function("split_to_table")
  df = session.create_dataframe([
    ["John", "James", "address1 address2 address3"],
    ["Mike", "James", "address4 address5 address6"],
    ["Cathy", "Stone", "address4 address5 address6"],
  ],
  schema=["first_name", "last_name", "addresses"])
  df.join_table_function(split_to_table(df["addresses"], lit(" ")).over(partition_by="last_name", order_by="first_name")).show()
  ```

  ```
  ----------------------------------------------------------------------------------------
  |"FIRST_NAME"  |"LAST_NAME"  |"ADDRESSES"                 |"SEQ"  |"INDEX"  |"VALUE"   |
  ----------------------------------------------------------------------------------------
  |John          |James        |address1 address2 address3  |1      |1        |address1  |
  |John          |James        |address1 address2 address3  |1      |2        |address2  |
  |John          |James        |address1 address2 address3  |1      |3        |address3  |
  |Mike          |James        |address4 address5 address6  |2      |1        |address4  |
  |Mike          |James        |address4 address5 address6  |2      |2        |address5  |
  |Mike          |James        |address4 address5 address6  |2      |3        |address6  |
  |Cathy         |Stone        |address4 address5 address6  |3      |1        |address4  |
  |Cathy         |Stone        |address4 address5 address6  |3      |2        |address5  |
  |Cathy         |Stone        |address4 address5 address6  |3      |3        |address6  |
  ----------------------------------------------------------------------------------------
  ```

## Calling Stored Procedures

To call a stored procedure, use the call method of the `Session` class.

Copy code

```
session.call("your_proc_name", 1)
```

```
0
```
