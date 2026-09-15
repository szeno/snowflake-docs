# Writing a UDTF in Python

You can implement a user-defined [table function](/sql-reference/functions-table) (UDTF) handler in Python. This handler code
executes when the UDTF is called. This topic describes how to implement a handler in Python and create the UDTF.

A UDTF is a user-defined function (UDF) that returns tabular results. For more about UDF handlers implemented in Python, see
[Creating Python UDFs](/developer-guide/udf/python/udf-python-creating). For more general information about UDFs, see [User-defined functions overview](/developer-guide/udf/udf-overview).

In the handler for a UDTF, you can process input rows (see [Processing rows](#label-udtf-python-process-method) in this topic). You can also have logic
that executes for each input partition (see [Processing partitions](#label-udtf-python-processing-partitions) in this topic).

When you create a Python UDTF, you do the following:

1. Implement a class with methods that Snowflake will invoke when the UDTF is called.

   For more details, see [Implementing a handler](#label-udtf-python-create-handler) in this topic.
2. Create the UDTF in SQL with the CREATE FUNCTION command, specifying your class as the handler. When you create the UDTF, you specify:

   - Data types of UDTF input parameters.
   - Data types of columns returned by the UDTF.
   - Code to execute as a handler when the UDTF is called.
   - The language in which the handler is implemented.

   For more about syntax, see [Creating the UDTF with](#label-udtf-python-create-function) in this topic.

You can call a UDF or UDTF as described in [Executing a UDF](/developer-guide/udf/udf-calling-sql).

Note

Table functions (UDTFs) have a limit of 500 input arguments and 500 output columns.

Snowflake currently supports writing UDTFs in the following versions of Python:

Generally available versions:

- 3.9 (deprecated)
- 3.10
- 3.11
- 3.12
- 3.13
- 3.14

In your CREATE FUNCTION statement, set `runtime_version` to the desired version.

## Implementing a handler

You implement a handler class to process UDTF argument values into tabular results and handle partitioned input. For a handler class
example, see [Handler class example](#label-udtf-python-handler-class-example) in this topic.

When you create the UDTF with CREATE FUNCTION, you specify this class as the UDTF’s handler. For more on the SQL to create the function,
see [Creating the UDTF with](#label-udtf-python-create-function) in this topic.

A handler class implements methods Snowflake will invoke when the UDTF is called. This class contains the UDTF’s logic.

| Method | Requirement | Description |
| --- | --- | --- |
| `__init__` method | Optional | Initializes state for stateful processing of input partitions. For more information, see [Initializing the handler](#label-udtf-python-initializing) in this topic. |
| `process` method | Required | Processes each input row, returning a tabular value as tuples. Snowflake invokes this method, passing input from the UDTF’s arguments. For more information, see [Defining a method](#label-udtf-python-declaring-process) in this topic. |
| `end_partition` method | Optional | Finalizes processing of input partitions, returning a tabular value as tuples. For more information, see [Finalizing partition processing](#label-udtf-python-finalizing) in this topic. |

Expand

Show lessSee more

Note that throwing an exception from any method in the handler class causes processing to stop. The query that called the UDTF fails with
an error message.

Note

If your code doesn’t meet the requirements described here, UDTF creation or execution may fail. Snowflake will detect violations when the
CREATE FUNCTION statement executes.

### Handler class example

Code in the following example creates a UDTF whose handler class processes rows in a partition. The `process` method processes each
input row, returning a row with the total cost for a stock sale. After processing rows in the partition, it returns (from its
`end_partition` method) the total for all sales included in the partition.

Copy code

```
CREATE OR REPLACE FUNCTION stock_sale_sum(symbol VARCHAR, quantity NUMBER, price NUMBER(10,2))
  RETURNS TABLE (symbol VARCHAR, total NUMBER(10,2))
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  HANDLER = 'StockSaleSum'
AS $$
class StockSaleSum:
    def __init__(self):
        self._cost_total = 0
        self._symbol = ""

    def process(self, symbol, quantity, price):
      self._symbol = symbol
      cost = quantity * price
      self._cost_total += cost
      yield (symbol, cost)

    def end_partition(self):
      yield (self._symbol, self._cost_total)
$$;
```

Code in the following example calls the preceding UDF, passing values from columns `symbol`, `quantity`, and `price`
from the `stocks_table` table. For more information about calling a UDTF, refer to [Executing a UDF](/developer-guide/udf/udf-calling-sql).

Copy code

```
SELECT stock_sale_sum.symbol, total
  FROM stocks_table, TABLE(stock_sale_sum(symbol, quantity, price) OVER (PARTITION BY symbol));
```

### Initializing the handler

You can optionally implement an `__init__` method in your handler class that Snowflake will invoke before the handler has begun
processing rows. For example, you can use this method to establish some partition-scoped state for the handler. Your `__init__`
method may not produce output rows.

The method’s signature must be of the following form:

Copy code

```
def __init__(self):
```

For example, you might want to:

- Initialize state for a partition, then use this state in the `process` and `end_partition` methods.
- Execute long-running initialization that needs to be done only once per partition rather than once per row.

Note

You can also execute logic once before partition handling begins by including that code outside the handler class, such as before the
class declaration.

For more about processing partitions, see [Processing partitions](#label-udtf-python-processing-partitions) in this topic.

If you use an `__init__` method, keep in mind that `__init__`:

- Can take only `self` as an argument.
- Cannot produce output rows. Use your `process` method implementation for that.
- Is invoked once for each partition, and before the `process` method is invoked.

### Processing rows

Implement a `process` method that Snowflake will invoke for each input row.

#### Defining a `process` method

Define a `process` method that receives as values the UDTF arguments converted from SQL types, returning data that Snowflake will
use to create the UDTF’s tabular return value.

The method’s signature must be of the following form:

Copy code

```
def process(self, *args):
```

Your `process` method must:

- Have a `self` parameter.
- Declare method parameters corresponding to UDTF parameters.

  Method parameter names needn’t match UDTF parameter names, but the method parameters must be declared *in the same order* as UDTF
  parameters are declared.

  When passing UDTF argument values to your method, Snowflake will convert the values from SQL types to the Python types you use in the
  method. For information about how Snowflake maps between SQL and Python data types, see [SQL-Python Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-python-data-type-mappings).
- Yield one or more tuples (or return an iterable containing tuples), in which the sequence of tuples corresponds to the sequence of UDTF
  return value columns.

  The tuple elements must appear *in the same order* as UDTF return value columns are declared. For more information, see
  [Returning a value](#label-udtf-python-returning-value) in this topic.

  Snowflake will convert values from Python types to SQL types required by the UDTF declaration. For information about how Snowflake maps
  between SQL and Python data types, see [SQL-Python Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-python-data-type-mappings).

If a method in the handler class throws an exception, processing will stop. The query that called the UDTF will fail with an
error message. If the `process` method returns `None`, processing stops. (The `end_partition` method is still invoked even if
the `process` method returns `None`.)

**process Method Example**

Code in the following example shows a `StockSale` handler class with a `process` method that processes three UDTF arguments
(`symbol`, `quantity`, and `price`), returning a single row with two columns (`symbol` and `total`). Note that
`process` method parameters are declared in the same order as `stock_sale` parameters. Arguments in the `process`
method’s `yield` statement are in the same order as columns declared in the `stock_sale` RETURNS TABLE clause.

Copy code

```
CREATE OR REPLACE FUNCTION stock_sale(symbol VARCHAR, quantity NUMBER, price NUMBER(10,2))
  RETURNS TABLE (symbol VARCHAR, total NUMBER(10,2))
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  HANDLER = 'StockSale'
AS $$
class StockSale:
    def process(self, symbol, quantity, price):
      cost = quantity * price
      yield (symbol, cost)
$$;
```

Code in the following example calls the preceding UDF, passing values from columns `symbol`, `quantity`, and `price`
from the `stocks_table` table.

Copy code

```
SELECT stock_sale.symbol, total
  FROM stocks_table, TABLE(stock_sale(symbol, quantity, price) OVER (PARTITION BY symbol));
```

#### Returning a value

When returning output rows, you can use either `yield` or `return` (but not both) to return tuples with the tabular value. If
the method returns or yields `None`, processing for the current row stops.

- When using `yield`, execute a separate `yield` statement for each output row. This is the best practice because the lazy
  evaluation that comes with `yield` enables more efficient processing and can help avoid timeouts.

  Each element in the tuple becomes a column value in the result returned by the UDTF. The order of `yield` arguments must
  match the order of columns declared for the return value in the RETURNS TABLE clause of CREATE FUNCTION.

  Code in the following example returns values representing two rows.

  Copy code

  ```
  def process(self, symbol, quantity, price):
    cost = quantity * price
    yield (symbol, cost)
    yield (symbol, cost)
  ```

  Note that because the yield argument is a tuple, you must include a trailing comma when passing a single value in the tuple, as in the
  following example.

  Copy code

  ```
  yield (cost,)
  ```
- When using `return`, return an iterable with tuples.

  Each value in a tuple becomes a column value in the result returned
  by the UDTF. The order of column values in a tuple must match the order of columns declared for the return value in the RETURNS TABLE
  clause of CREATE FUNCTION.

  Code in the following example returns two rows, each with two columns: symbol and total.

  Copy code

  ```
  def process(self, symbol, quantity, price):
    cost = quantity * price
    return [(symbol, cost), (symbol, cost)]
  ```

#### Skipping rows

To skip an input row and process the next row (such as when you’re validating the input rows), have the `process` method return one
of the following:

- When using `return`, return `None`, a list containing `None`, or an empty list to skip the row.
- When using `yield`, return `None` to skip a row.

  Note that if you have multiple calls to `yield`, any calls after a call that returns `None` will be ignored by Snowflake.

Code in the following example returns only the rows for which `number` is a positive integer. If `number` is not positive, the
method returns `None` to skip the current row and continue processing the next row.

Copy code

```
def process(self, number):
  if number < 1:
    yield None
  else:
    yield (number)
```

#### Stateful and stateless processing

You can implement the handler to process rows in a partition-aware manner or to process them simply row by row.

- In **partition-aware processing**, the handler includes code to manage partition-scoped state. This includes an `__init__` method
  that executes at the start of partition processing and an `end_partition` method that Snowflake invokes after processing the
  partition’s last row. For more information, see [Processing partitions](#label-udtf-python-processing-partitions) in this topic.
- In **partition-unaware processing**, the handler executes statelessly, ignoring partition boundaries.

  To have the handler execute this way, do not include an `__init__` or `end_partition` method.

### Processing partitions

You can process partitions in input with code that executes per partition (such as to manage state) as well as code that executes for each
row in the partition.

Note

For more information on specifying partitions when calling a UDTF, refer to [Table functions and partitions](/developer-guide/udf/udf-calling-sql#label-udf-java-partitions).

When a query includes partitions, it aggregates rows using a specified value, such as the value of a column. The aggregated rows your
handler receives are said to be partitioned by that value. Your code can process these partitions and their rows so that the
processing for each partition includes partition-scoped state.

Code in the following SQL example queries for stock sale information. It executes a `stock_sale_sum` UDTF whose input is
partitioned by the value of the `symbol` column.

Copy code

```
SELECT stock_sale_sum.symbol, total
  FROM stocks_table, TABLE(stock_sale_sum(symbol, quantity, price) OVER (PARTITION BY symbol));
```

Keep in mind that even when incoming rows are partitioned, your code can ignore the partition separation and just process the rows. For
example, you can omit code designed to handle partition-scoped state, such as a handler class `__init__` method and
`end_partition` method, and just implement the `process` method. For more information, see
[Stateful and stateless processing](#label-udtf-python-processing-input) in this topic.

To process each partition as a unit, you would:

- Implement a handler class `__init__` method in which to initialize processing for the partition.

  For more information, see [Initializing the handler](#label-udtf-python-initializing) in this topic.
- Include partition-aware code when processing each row with the `process` method.

  For more information on processing rows, see [Processing rows](#label-udtf-python-process-method) in this topic.
- Implement an `end_partition` method to finalize partition processing.

  For more information, see [Finalizing partition processing](#label-udtf-python-finalizing) in this topic.

The following describes the sequence of invocations to your handler when you’ve included code designed to execute per partition.

1. When processing for a partition starts, and before the first row has been processed, Snowflake uses the `__init__` method of your
   handler class to create an instance of the class.

   Here, you can establish partition-scoped state. For example, you might initialize an instance variable to hold a value
   calculated from rows in the partition.
2. For each row in the partition, Snowflake invokes the `process` method.

   Each time the method executes, it can make changes to state values. For example, you might have the `process` method update the
   value of the instance variable.
3. After your code has processed the last row in the partition, Snowflake invokes your `end_partition` method.

   From this method you can return output rows containing a partition-level value you want to return. For example, you might return the
   value of the instance variable you’ve been updating as you processed rows in the partition.

   Your `end_partition` method won’t receive any arguments from Snowflake, which simply invokes it after you process the last row in the
   partition.

#### Finalizing partition processing

You can optionally implement an `end_partition` method in your handler class that Snowflake will invoke after you have processed all
rows in a partition. In this method, you can execute code for a partition after all of the partition’s rows have been processed.
Your `end_partition` method may produce output rows, such as to return the results of a partition-scoped calculation. For more
information, see [Processing partitions](#label-udtf-python-processing-partitions) in this topic.

The method’s signature must be of the following form:

Copy code

```
def end_partition(self):
```

Snowflake expects the following of your `end_partition` method implementation:

> - It must not be static.
> - It may not have any parameters other than `self`.
> - As an alternative to returning a tabular value, it may produce an empty list or `None`.

Note

While Snowflake supports large partitions with timeouts tuned to process them successfully, especially large partitions can cause
processing to time out (such as when `end_partition` takes too long to complete). Please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) if you need the
timeout threshold adjusted for specific usage scenarios.

#### Partition handling example

Code in the following example calculates the total cost paid across purchases for a stock by first calculating the cost per purchase and
adding purchases together (in the `process` method). The code returns the total in the `end_partition` method.

For an example of a UDTF that includes this handler, along with calling the UDTF, refer to [Handler class example](#label-udtf-python-handler-class-example).

Copy code

```
class StockSaleSum:
  def __init__(self):
    self._cost_total = 0
    self._symbol = ""

  def process(self, symbol, quantity, price):
    self._symbol = symbol
    cost = quantity * price
    self._cost_total += cost
    yield (symbol, cost)

  def end_partition(self):
    yield (self._symbol, self._cost_total)
```

When processing partitions, keep in mind the following:

- Your code may handle partitions that aren’t explicitly specified in a call to the UDTF. Even when a call to the UDTF doesn’t include
  a PARTITION BY clause, Snowflake partitions the data implicitly.
- Your `process` method will receive row data in the order specified by the partition’s ORDER BY clause, if any.

## Examples

### Using an imported package

You can use Python packages that are included in a curated list of third party packages from Anaconda available in Snowflake. To specify
these packages as dependencies in the UDTF, use the PACKAGES clause in CREATE FUNCTION.

You can discover the list of included packages by executing the following SQL in Snowflake:

Copy code

```
SELECT * FROM INFORMATION_SCHEMA.PACKAGES WHERE LANGUAGE = 'python';
```

For more information, see [Using third-party packages](/developer-guide/udf/python/udf-python-packages) and [Creating Python UDFs](/developer-guide/udf/python/udf-python-creating).

Code in the following example uses a function in the [NumPy (Numerical Python)](https://numpy.org/doc/stable/reference/index.html)
package to calculate the average price per share from an array of stock purchases, each with a different price per share.

Copy code

```
CREATE OR REPLACE FUNCTION stock_sale_average(symbol VARCHAR, quantity NUMBER, price NUMBER(10,2))
  RETURNS TABLE (symbol VARCHAR, total NUMBER(10,2))
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  PACKAGES = ('numpy')
  HANDLER = 'StockSaleAverage'
AS $$
import numpy as np

class StockSaleAverage:
    def __init__(self):
      self._price_array = []
      self._quantity_total = 0
      self._symbol = ""

    def process(self, symbol, quantity, price):
      self._symbol = symbol
      self._price_array.append(float(price))
      cost = quantity * price
      yield (symbol, cost)

    def end_partition(self):
      np_array = np.array(self._price_array)
      avg = np.average(np_array)
      yield (self._symbol, avg)
$$;
```

Code in the following example calls the preceding UDF, passing values from columns `symbol`, `quantity`, and `price`
from the `stocks_table` table. For more information about calling a UDTF, refer to [Executing a UDF](/developer-guide/udf/udf-calling-sql).

Copy code

```
SELECT stock_sale_average.symbol, total
  FROM stocks_table,
  TABLE(stock_sale_average(symbol, quantity, price)
    OVER (PARTITION BY symbol));
```

### Running concurrent tasks with worker processes

You can run concurrent tasks using Python worker processes. You might find this useful when you need to run parallel tasks that take
advantage of multiple CPU cores on warehouse nodes.

Note

Snowflake recommends that you not use the built-in Python multiprocessing module.

To work around cases where the [Python Global Interpreter Lock](https://wiki.python.org/moin/GlobalInterpreterLock) prevents a
multi-tasking approach from scaling across all CPU cores, you can execute concurrent tasks using separate worker processes, rather than threads.

You can do this on Snowflake warehouses by using the `joblib` library’s `Parallel` class, as in the following example.

Copy code

```
CREATE OR REPLACE FUNCTION joblib_multiprocessing_udtf(i INT)
  RETURNS TABLE (result INT)
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  HANDLER = 'JoblibMultiprocessing'
  PACKAGES = ('joblib')
AS $$
import joblib
from math import sqrt

class JoblibMultiprocessing:
  def process(self, i):
    pass

  def end_partition(self):
    result = joblib.Parallel(n_jobs=-1)(joblib.delayed(sqrt)(i ** 2) for i in range(10))
    for r in result:
      yield (r, )
$$;
```

Note

The default backend used for `joblib.Parallel` differs between Snowflake standard and Snowpark-optimized warehouses.

- Standard warehouse default: `threading`
- Snowpark-optimized warehouse default: `loky` (multiprocessing)

You can override the default backend setting by calling the `joblib.parallel_backend` function, as in the following example.

Copy code

```
import joblib
joblib.parallel_backend('loky')
```

## Creating the UDTF with `CREATE FUNCTION`

You create a UDTF in SQL using the CREATE FUNCTION command, specifying the code you wrote as the handler. For the command reference, see
[CREATE FUNCTION](/sql-reference/sql/create-function).

Use the following syntax when creating a UDTF.

Copy code

```
CREATE OR REPLACE FUNCTION <name> ( [ <arguments> ] )
  RETURNS TABLE ( <output_column_name> <output_column_type> [, <output_column_name> <output_column_type> ... ] )
  LANGUAGE PYTHON
  [ IMPORTS = ( '<imports>' ) ]
  RUNTIME_VERSION = 3.12
  [ PACKAGES = ( '<package_name>' [, '<package_name>' . . .] ) ]
  [ TARGET_PATH = '<stage_path_and_file_name_to_write>' ]
  HANDLER = '<handler_class>'
  [ AS '<python_code>' ]
```

To associate the handler code you’ve written with the UDTF, you do the following when executing CREATE FUNCTION:

- In RETURNS TABLE, specify output columns in column name and type pairs.
- Set LANGUAGE to PYTHON.
- Set the IMPORTS clause value to the path and name of the handler class if the class is in an external location, such as on a stage.

  For more information, see [Creating Python UDFs](/developer-guide/udf/python/udf-python-creating).
- Set RUNTIME\_VERSION to the version of the Python runtime that your code requires. The supported versions of Python are:

  Generally available versions:

  - 3.9 (deprecated)
  - 3.10
  - 3.11
  - 3.12
  - 3.13
  - 3.14
- Set the PACKAGES clause value to the name of one or more packages, if any, required by the handler class.

  For more information, see [Using third-party packages](/developer-guide/udf/python/udf-python-packages) and [Creating Python UDFs](/developer-guide/udf/python/udf-python-creating).
- Set the HANDLER clause value to the name of the handler class.

  When associating Python handler code with a UDTF, you can either include the code in-line or refer to it at a location on a Snowflake stage. The HANDLER value is case-sensitive and must match the name of the Python class.

  For more information, see [UDFs with in-line code vs. UDFs with code uploaded from a stage](/developer-guide/udf/python/udf-python-creating#label-udf-python-in-line-vs-pre-compiled).

  Important

  For a scalar Python UDF, the HANDLER clause value contains the method name.

  For a Python UDTF, the HANDLER clause value contains the class name but not a method name.

  The reason for the difference is that for a scalar Python UDF, the name of the handler method is chosen by the user and
  therefore not known in advance by Snowflake, but for a Python UDTF, the names of the methods (such as the
  `end_partition` method) are known because they must match the names specified by Snowflake.
- The `AS '<python_code>'` clause is required if the handler code is specified in-line with CREATE FUNCTION.
