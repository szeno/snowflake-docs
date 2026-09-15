# Creating User-Defined Table Functions (UDTFs) for DataFrames in Python

The Snowpark API provides methods that you can use to create a user-defined table function with a handler written in Python.
This topic explains how to create these types of functions.

## Introduction

You can create a user-defined table function (UDTF) using the Snowpark API.

You do this in a way similar to creating a scalar user-defined function (UDF) with the API, as described in
[Creating User-Defined Functions (UDFs) for DataFrames in Python](/developer-guide/snowpark/python/creating-udfs). Key differences include UDF handler requirements and parameter values required when registering
the UDTF.

To create and register a UDTF with Snowpark, you must:

- Implement a UDTF handler.

  The handler contains the UDTF’s logic. A UDTF handler must implement functions that Snowflake will invoke at runtime when the UDTF is
  called. For more information, see [Implementing a UDTF Handler](#label-snowpark-python-udtf-handler).
- Register the UDTF and its handler in the Snowflake database.

  You can use the Snowpark API to register the UDTF and its handler. Once you’ve registered the UDTF, you can call it from SQL or by using
  the Snowpark API. For more information about registering, see [Registering a UDTF](#label-snowpark-python-udtf-register).

For information on calling a UDTF, see [Calling User-Defined Table Functions (UDTFs)](/developer-guide/snowpark/python/calling-functions#label-snowpark-python-udtf-calling).

## Implementing a UDTF Handler

As described in detail in [Writing a UDTF in Python](/developer-guide/udf/python/udf-python-tabular-functions), a UDTF handler class must implement methods that
Snowflake invokes when the UDTF is called. You can use the class you write as a handler whether you’re registering the UDTF with the
Snowpark API or creating it with SQL using the CREATE FUNCTION statement.

Methods of a handler class are designed to process rows and partitions received by the UDTF.

A UDTF handler class implements the following, which Snowflake invokes at runtime:

- An `__init__` method. Optional. Invoked to initialize stateful processing of input partitions.
- A `process` method. Required. Invoked for each input row. The method returns a tabular value as tuples.
- An `end_partition` method. Optional. Invoked to finalize processing of input partitions.

  While Snowflake supports large partitions with timeouts tuned to process them successfully, especially large partitions can cause
  processing to time out (such as when `end_partition` takes too long to complete). Contact [Snowflake Support](/user-guide/contacting-support) if you need the
  timeout threshold adjusted for specific usage scenarios.

For handler details and examples, see [Writing a UDTF in Python](/developer-guide/udf/python/udf-python-tabular-functions).

## Registering a UDTF

Once you’ve implemented a UDTF handler, you can use the Snowpark API to register the UDTF on the Snowflake database. Registering the UDTF
creates the UDTF so that it can be called.

You can register the UDTF as a named or anonymous function, as you can for a scalar UDF. For related information about registering a scalar
UDF, see [Creating an Anonymous UDF](/developer-guide/snowpark/python/creating-udfs#label-snowpark-python-udf-inline-anonymous) and [Creating and Registering a Named UDF](/developer-guide/snowpark/python/creating-udfs#label-snowpark-python-udf-inline-named).

When you register a UDTF, you specify parameter values that Snowflake needs to create the UDTF. (Many of these parameters correspond
functionally to clauses of the CREATE FUNCTION statement in SQL. For more information, see [CREATE FUNCTION](/sql-reference/sql/create-function).)

Most of these parameters are the same as those you specify when you create a scalar UDF (for more information,
see [Creating User-Defined Functions (UDFs) for DataFrames in Python](/developer-guide/snowpark/python/creating-udfs)). The primary differences are due to the fact that a UDTF returns a tabular
value and the fact that its handler is a class, rather than a function. For a complete list of parameters, see the documentation for the
APIs linked below.

To register a UDTF with Snowpark, you use one of the following, specifying parameter values required to create the UDTF in the
database. For information that differentiates these options, see
[UDFRegistration](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.udf.UDFRegistration),
which describes similar options for registering a scalar UDF.

- Use the `register` or `udtf` function, pointing to a runtime Python function. You can also use the `udtf` function as
  a decorator on the handler class.

  For reference on these functions, see:

  - [snowflake.snowpark.functions.udtf](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.functions.udtf)
  - [snowflake.snowpark.udtf.UDTFRegistration.register](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.udtf.UDTFRegistration)
- Use the `register_from_file` function, pointing to a Python file or zip file containing Python source code.

  For the function reference, see [snowflake.snowpark.udtf.UDTFRegistration.register\_from\_file](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.udtf.UDTFRegistration.register_from_file).

### Defining a UDTF’s Input Types and Output Schema

When you register a UDTF, you specify details about the function’s parameters and output value. You do this so that the function itself
declares types that accurately correspond to those for the function’s underlying handler.

For examples, see [Examples](#label-snowpark-python-udtf-register-examples) in this topic and in the
[snowflake.snowpark.udtf.UDTFRegistration](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.udtf.UDTFRegistration)
reference.

You specify the following for the UDTF when registering it:

- Types of its input parameters as a value of the registering function’s `input_types` parameter. The `input_types` parameter is
  optional if you provide type hints in the `process` method’s declaration.

  Specify this value as a list of types based on
  [snowflake.snowpark.types.DataType](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/types).
  For example, you might specify `input_types=[StringType(), IntegerType()]`.
- Schema of its tabular output as a value of the registering function’s `output_schema` parameter.

  The `output_schema` value can be one of the following:

  - A list of the names for columns in the UDTF’s return value.

    The list will include column names only, so you must also provide type hints in the `process` method’s declaration.
  - A [StructType](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.types.StructType)
    that represents the output table’s column names *and* types.

    Code in the following example assigns a schema as a value to an `output` variable, then uses the variable when registering the UDTF.

    Copy code

    ```
    from snowflake.snowpark.types import StructField, StructType, StringType, IntegerType, FloatType
    from snowflake.snowpark.functions import udtf, table_function
    schema = StructType([
      StructField("symbol", StringType()),
      StructField("cost", IntegerType()),
    ])
    @udtf(output_schema=schema,input_types=[StringType(), IntegerType(), FloatType()],stage_location="straut_udf",is_permanent=True,name="test_udtf",replace=True)
    class StockSale:
      def process(self, symbol, quantity, price):
        cost = quantity * price
        yield (symbol, cost)
    ```

## Examples

The following is a brief list of examples. For more examples, see [snowflake.snowpark.udtf.UDTFRegistration](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.udtf.UDTFRegistration).

**Registering a UDTF with the udtf Function**

Register the function.

Copy code

```
from snowflake.snowpark.types import IntegerType, StructField, StructType
from snowflake.snowpark.functions import udtf, lit
class GeneratorUDTF:
    def process(self, n):
        for i in range(n):
            yield (i, )
generator_udtf = udtf(GeneratorUDTF, output_schema=StructType([StructField("number", IntegerType())]), input_types=[IntegerType()])
```

Call the function.

Copy code

```
session.table_function(generator_udtf(lit(3))).collect()  # Query it by calling it
```

```
[Row(NUMBER=0), Row(NUMBER=1), Row(NUMBER=2)]
```

Copy code

```
session.table_function(generator_udtf.name, lit(3)).collect()  # Query it by using the name
```

```
[Row(NUMBER=0), Row(NUMBER=1), Row(NUMBER=2)]
```

**Registering a UDTF with the register Function**

Register the function.

Copy code

```
from collections import Counter
from typing import Iterable, Tuple
from snowflake.snowpark.functions import lit
class MyWordCount:
      def __init__(self):
          self._total_per_partition = 0

      def process(self, s1: str) -> Iterable[Tuple[str, int]]:
        words = s1.split()
        self._total_per_partition = len(words)
        counter = Counter(words)
        yield from counter.items()

      def end_partition(self):
          yield ("partition_total", self._total_per_partition)
udtf_name = "word_count_udtf"
word_count_udtf = session.udtf.register(
    MyWordCount, ["word", "count"], name=udtf_name, is_permanent=False, replace=True
)
```

Call the function.

Copy code

```
# Call it by its name
df1 = session.table_function(udtf_name, lit("w1 w2 w2 w3 w3 w3"))
df1.show()
```

```
-----------------------------
|"WORD"           |"COUNT"  |
-----------------------------
|w1               |1        |
|w2               |2        |
|w3               |3        |
|partition_total  |6        |
-----------------------------
```

**Registering a UDTF with the register\_from\_file Function**

Register the function.

Copy code

```
from snowflake.snowpark.types import IntegerType, StructField, StructType
from snowflake.snowpark.functions import udtf, lit
_ = session.sql("create or replace stage mystage").collect()
_ = session.file.put("tests/resources/test_udtf_dir/test_udtf_file.py", "@mystage", auto_compress=False)
generator_udtf = session.udtf.register_from_file(
    file_path="@mystage/test_udtf_file.py",
    handler_name="GeneratorUDTF",
    output_schema=StructType([StructField("number", IntegerType())]),
    input_types=[IntegerType()]
  )
```

Call the function.

Copy code

```
session.table_function(generator_udtf(lit(3))).collect()
```

```
[Row(NUMBER=0), Row(NUMBER=1), Row(NUMBER=2)]
```
