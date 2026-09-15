# Designing Python UDFs

This topic helps you design Python UDFs.

Note

Vectorized Python UDFs let you define Python functions that receive batches of input rows
as [Pandas DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) and
return batches of results as [Pandas arrays](https://pandas.pydata.org/docs/reference/api/pandas.array.html)
or [Series](https://pandas.pydata.org/docs/reference/series.html).
The batch interface results in much better performance with machine learning inference scenarios.
For more information, see [Vectorized Python UDFs](/developer-guide/udf/python/udf-python-batch).

## Choosing your data types

Before you write your code:

- Choose the data types your function should accept as arguments and the data
  type your function should return.
- Take into account time-zone related issues.
- Decide how to handle NULL values.

For more information about how Snowflake maps Python and SQL data types, see [SQL-Python Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-python-data-type-mappings).

### TIMESTAMP\_LTZ values and time zones

A Python UDF is largely isolated from the environment in which it is called. However, the timezone is inherited from
the calling environment. If the caller’s session set a default time zone before calling the Python UDF, then the Python
UDF has the same default time zone. For more information about timezones, see [TIMEZONE](/sql-reference/parameters#label-timezone).

### NULL values

For all Snowflake types except Variant, a SQL `NULL` argument to a Python UDF translates to the
Python `None` value and a returned Python `None` value translates back to SQL `NULL`.

A Variant type value can be: SQL `NULL` or a VARIANT JSON `null`. For information about Snowflake
VARIANT NULL, see [NULL values](/user-guide/semistructured-considerations#label-variant-null).

- A VARIANT JSON `null` is translated to Python `None`.
- A SQL `NULL` is translated to a Python object, which has the `is_sql_null` attribute.

For an example, see [NULL Handling in Python UDFs](/developer-guide/udf/python/udf-python-examples#label-udf-python-null-example).

## Designing Python UDFs that stay within Snowflake-imposed constraints

To ensure stability within the Snowflake environment, Snowflake places the following constraints on Python UDFs.
Unless stated otherwise, these limitations are enforced when the UDF is executed, not when it is created.

Training machine learning (ML) models can sometimes be very resource intensive.
Snowpark-optimized warehouses are a type of Snowflake virtual warehouse that can be used for workloads
that require a large amount of memory and compute resources.
For information on machine learning models and Snowpark Python, see [Training Machine Learning Models with Snowpark Python](/developer-guide/snowpark/python/python-snowpark-training-ml).

### Memory

Avoid consuming too much memory.

- Large data values can consume a large amount of memory.
- Excessive stack depth can consume a large amount of memory.

UDFs return an error if they consume too much memory. The specific limit is subject to change.

If UDFs fail due to consuming too much memory, consider using [Snowpark-optimized warehouses](/user-guide/warehouses-snowpark-optimized).

### Time

Avoid algorithms that take a large amount of time per call.

If a UDF takes too long to complete, Snowflake kills the SQL statement and returns an error to the user. This limits
the impact and cost of errors such as infinite loops.

## Designing the module

When a SQL statement calls your Python UDF, Snowflake calls a Python function you have written. Your Python function is called a
“handler function”, or “handler” for short. The handler is a function implemented inside a user-supplied module.

As with any Python function, your function must be declared as part of a module.

The handler is called once for each row passed to the Python UDF.
The module that contains the function is not re-imported for each row. Snowflake can call the same module’s handler function more than once.

To optimize execution of your code, Snowflake assumes that initialization might be slow, while execution of the handler function
is fast. Snowflake sets a longer timeout for executing initialization (including the time to load your UDF and the time
to initialize the module) than for executing the handler
(the time to call your handler with one row of input).

Additional information about designing the module is in [Creating Python UDFs](/developer-guide/udf/python/udf-python-creating).

## Optimizing initialization and controlling global state in scalar UDFs

Most scalar UDFs should follow the guidelines below:

- If you need to initialize shared state that does not change across rows, initialize it in the module instead of the handler function.
- Write your handler function to be thread safe.
- Avoid storing and sharing dynamic state across rows.

If your UDF cannot follow these guidelines, be aware that Snowflake expects scalar UDFs to be processed independently. Relying on state
shared between invocations can result in unexpected behavior, as the system can process rows in any order and spread those invocations
across several instances. In addition, there can be multiple executions of the same handler function within the same Python
interpreter on multiple threads.

UDFs should avoid relying on shared state across calls to the handler function. However, there are two situations in which you might want a
UDF to store shared state:

- Code that contains expensive initialization logic that you do not want to repeat for each row.
- Code that leverages shared state across rows, such as a cache.

When it’s necessary to maintain global state that will be shared across handler invocations, you must protect global state against
data races by using the synchronization primitives described in
[threading - Thread-based parallelism](https://docs.python.org/3.12/library/threading.html).

## Optimizing for scale and performance

### Use vectorized Python UDFs with data science libraries

When your code will use machine learning or data science libraries, use vectorized Python UDFs to
define Python functions that receive input rows in batches on which these libraries are optimized to operate.

For more information, see [Vectorized Python UDFs](/developer-guide/udf/python/udf-python-batch).

### Write single-threaded UDF handlers

Write UDF handlers that are single-threaded. Snowflake will handle partitioning the data and scaling the UDF across the virtual warehouse
compute resources.

### Put expensive initialization in the module

Put expensive initialization code into the module scope. There, it will be performed once when the UDF is initialized.
Avoid rerunning the expensive initialization code on every UDF handler invocation.

## Handling errors

A Python function used as a UDF can use the normal Python exception-handling techniques to catch errors within the
function.

If an exception occurs inside the function and is not caught by the function, Snowflake raises an error that includes the stack trace for the
exception. When [logging of unhandled exceptions](/developer-guide/logging-tracing/unhandled-exception-messages) is enabled,
Snowflake logs data about unhandled exceptions in an event table.

You can explicitly throw an exception without catching it in order to end the query and produce a SQL error. For
example:

Copy code

```
if (x < 0):
  raise ValueError("x must be non-negative.");
```

When debugging, you can include values in the SQL error message text. To do so, place an entire Python function body in a
try-catch block; append argument values to the caught error’s message; and throw an exception with the extended
message. To avoid revealing sensitive data, remove argument values prior to deploying to a production
environment.

## Following good security practices

To help ensure that your handler functions in a secure way, see the best practices described in
[Security Practices for UDFs and Procedures](/developer-guide/udf-stored-procedure-security-practices).
