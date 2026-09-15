# Creating User-Defined Aggregate Functions (UDAFs) for DataFrames in Python

You can use Snowpark Python APIs to create and call user-defined aggregate functions (UDAFs). A UDAF takes one or more rows as input and
produces a single row of output. It operates on values across multiple rows to perform mathematical calculations such as sum, average,
counting, finding minimum or maximum values, standard deviation, and estimation, as well as some non-mathematical operations.

To create and register a UDAF with Snowpark, you need to:

- Implement a UDAF handler.

  The handler contains the UDAF’s logic. A UDAF handler must implement functions that Snowflake will invoke at runtime when the UDAF is
  called. For more information, see [Implementing a handler](#label-snowpark-python-udaf-handler).
- Register the UDAF and its handler in the Snowflake database.

  Once you’ve registered the UDAF, you can call it from SQL or by using the Snowpark API. You can use the Snowpark API to register the
  UDAF and its handler. For more information about registering, see [Registering a UDAF](#label-snowpark-python-udaf-register).

You can also create your own UDAFs using SQL as described in [Python user-defined aggregate functions](/developer-guide/udf/python/udf-python-aggregate-functions).

## Implementing a handler

As described in [Interface for aggregate function handler](/developer-guide/udf/python/udf-python-aggregate-functions#label-snowpark-python-udaf-handler-interface), a UDAF handler class must implement methods that Snowflake invokes
when the UDAF is called. You can use the class you write as a handler whether you’re registering the UDAF with the Snowpark API or
[creating it with SQL using the CREATE FUNCTION statement](/developer-guide/udf/python/udf-python-aggregate-functions).

Your UDAF handler class implements methods listed in the following table, which Snowflake invokes at run time. See
[examples in this topic](#label-snowpark-python-udaf-examples).

| Method | Requirement | Description |
| --- | --- | --- |
| `__init__` | Required | Initializes the internal state of an aggregate. |
| `aggregate_state` | Required | Returns the internal state of an aggregate.   - The method must have a [@property decorator](https://docs.python.org/3.12/library/functions.html#property). - An aggregate state object can be any Python data type serializable by the   [Python pickle library](https://docs.python.org/3/library/pickle.html#what-can-be-pickled-and-unpickled). - For simple aggregate states, use a primitive Python data type. For more complex aggregate states, use   [Python data classes](https://docs.python.org/3/library/dataclasses.html). |
| `accumulate` | Required | Accumulates the state of the aggregate based on the new input row. |
| `merge` | Required | Combines two intermediate aggregated states. |
| `finish` | Required | Produces the final result based on the aggregated state. |

Expand

Show lessSee more

## Registering a UDAF

Once you’ve implemented a UDAF handler, you can use the Snowpark API to register the UDAF on the Snowflake database. Registering the UDAF
creates the UDAF so that it can be called.

You can register the UDAF as a named or anonymous function, as you can for a scalar UDF. For related information about registering a scalar
UDF, see [Creating an Anonymous UDF](/developer-guide/snowpark/python/creating-udfs#label-snowpark-python-udf-inline-anonymous) and [Creating and Registering a Named UDF](/developer-guide/snowpark/python/creating-udfs#label-snowpark-python-udf-inline-named). When you register a UDAF,
you specify parameter values that Snowflake needs to create the UDAF.

You can register the function using the following functions and methods:

- Use the `register` method or `udaf` function, specifying the name of your handler class, along with arguments to define the
  function. You can also use `udaf` as a `@udaf` decorator on the handler class.

  For reference information on these, see the following:

  - [snowflake.snowpark.functions.udaf](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.udaf)
  - [snowflake.snowpark.udaf.UDAFRegistration.register](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.udaf.UDAFRegistration)
- Use the `register_from_file` function, pointing to a Python file or zip file containing Python source code.

  For the function reference, see [snowflake.snowpark.udaf.UDAFRegistration.register\_from\_file](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.udaf.UDAFRegistration.register_from_file#snowflake.snowpark.udaf.UDAFRegistration.register_from_file).

## Examples

### Create a UDAF with a return value and a single parameter

Python code in the following handler example supports a `sum_int` UDAF that receives a single integer argument, adds the value
across rows and returns the result.

#### Register the function

Copy code

```
import snowflake.snowpark as snowpark
from snowflake.snowpark.types import IntegerType
from snowflake.snowpark.functions import udaf
def main(session: snowpark.Session):
  class PythonSumUDAF:
    def __init__(self):
      # This aggregate state is a primitive Python data type.
      self._partial_sum = 0

    @property
    def aggregate_state(self):
      return self._partial_sum

    def accumulate(self, input_value):
      self._partial_sum += input_value

    def merge(self, other_partial_sum):
      self._partial_sum += other_partial_sum

    def finish(self):
      return self._partial_sum
  sum_udaf = udaf(PythonSumUDAF, name="sum_int", replace=True, return_type=IntegerType(), input_types=[IntegerType()])
```

#### Call the function

Python code in the following example invokes the `sum_int` UDAF with a DataFrame.

Copy code

```
df = session.create_dataframe([[1, 3], [1, 4], [2, 5], [2, 6]]).to_df("a", "b")
result = df.agg(sum_udaf("a")).collect()
print(result)
```

### Create a UDAF with a return value and two parameters

#### Register the function

Python code in the following handler example supports a `sum_int` UDAF that receives two integer arguments, adds the argument
values together across rows and returns the result.

Copy code

```
import snowflake.snowpark as snowpark
from snowflake.snowpark.types import IntegerType
from snowflake.snowpark.functions import udaf
def main(session: snowpark.Session):
  class PythonSumUDAF:
    def __init__(self):
      self._partial_sum = 0

    @property
    def aggregate_state(self):
      return self._partial_sum

    def accumulate(self, input_value, input_value2):
      self._partial_sum += input_value + input_value2

    def merge(self, other_partial_sum):
      self._partial_sum += other_partial_sum

    def finish(self):
      return self._partial_sum
  sum_udaf = udaf(PythonSumUDAF, name="sum_int", replace=True, return_type=IntegerType(), input_types=[IntegerType(), IntegerType()])
```

#### Call the function

Python code in the following example invokes the `sum_int` UDAF with a DataFrame.

Copy code

```
df = session.create_dataframe([[1, 3], [1, 4], [2, 5], [2, 6]]).to_df("a", "b")
result = df.agg(sum_udaf("a", "b"))
print(result.collect())
```
