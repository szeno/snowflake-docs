# User-defined functions overview

You can write user-defined functions (UDFs) to extend the system to perform operations that are not available through the
[built-in system-defined functions](/sql-reference/intro-summary-operators-functions) provided by Snowflake. Once you create a UDF,
you can reuse it multiple times. A function always returns a value explicitly by specifying an expression, so it’s a good choice for
calculating and return a value.

You can use UDFs to extend built-in functions or to encapsulate calculations that are standard for your organization. UDFs you create
can be called in a way similar to built-in functions.

You write a UDF’s logic – its handler – in one of the [supported languages](#label-udf-supported-languages). Once you have a handler,
you can [create a UDF](/developer-guide/udf/udf-creating-sql) using any of several tools included in Snowflake, then
[execute the UDF](/developer-guide/udf/udf-calling-sql).

A UDF is like a stored procedure, but the two differ in important ways. For more information, see
[Choosing whether to write a stored procedure or a user-defined function](/developer-guide/stored-procedures-vs-udfs).

A UDF is just one way to extend Snowflake. For others, see the following:

- [Stored procedures overview](/developer-guide/stored-procedure/stored-procedures-overview)
- [Writing external functions](/sql-reference/external-functions)
- [Snowpark API](/developer-guide/snowpark/index)

## User-defined function variations

You can write a UDF in one of several variations, depending on the input and output requirements your function must meet.

| Variation | Description |
| --- | --- |
| User-defined function (UDF) | Also known as a *scalar function*, returns one output row for each input row. The returned row consists of a single column/value. |
| User-defined aggregate function (UDAF) | Operates on values across multiple rows to perform mathematical calculations such as sum, average, counting, finding minimum or maximum values, standard deviation, and estimation, as well as some non-mathematical operations. |
| User-defined table function (UDTF) | Returns a tabular value for each input row. |
| Vectorized user-defined function (UDF) | Receive batches of input rows as [Pandas DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) and return batches of results as [Pandas arrays](https://pandas.pydata.org/docs/reference/api/pandas.array.html) or [Series](https://pandas.pydata.org/docs/reference/series.html). |
| Vectorized user-defined table function (UDTF) | Receive batches of input rows as [Pandas DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) and return tabular results. |

Expand

Show lessSee more

## Supported languages and tools

You can [create](/developer-guide/udf/udf-creating-sql) and manage UDFs (and other Snowflake entities) by using any of multiple
tools, depending on how you prefer to work.

| Language | Approach | Support |
| --- | --- | --- |
| **SQL**  With handler in Java, JavaScript, Python, Scala, or SQL | Write SQL code in Snowflake to create and manage Snowflake entities. Write the function’s logic in one of the supported handler languages. | Java:  [UDF](/developer-guide/udf/java/udf-java-introduction), [UDTF](/developer-guide/udf/java/udf-java-tabular-functions)  JavaScript:  [UDF](/developer-guide/udf/javascript/udf-javascript-introduction), [UDTF](/developer-guide/udf/javascript/udf-javascript-tabular-functions)  Python:  [UDF](/developer-guide/udf/python/udf-python-introduction), [UDAF](/developer-guide/udf/python/udf-python-aggregate-functions), [UDTF](/developer-guide/udf/python/udf-python-tabular-functions), [Vectorized UDF](/developer-guide/udf/python/udf-python-batch), [Vectorized UDTF](/developer-guide/udf/python/udf-python-tabular-vectorized)  Scala:  [UDF](/developer-guide/udf/scala/udf-scala-introduction)  SQL:  [UDF](/developer-guide/udf/sql/udf-sql-introduction), [UDTF](/developer-guide/udf/sql/udf-sql-tabular-functions) |
| **Java, Python, or Scala**  [Snowpark API](/developer-guide/snowpark/index) | On the client, write code for operations that are pushed to Snowflake for processing. | Java:  [UDF](/developer-guide/snowpark/java/creating-udfs), [UDTF](/developer-guide/snowpark/java/creating-udfs#label-snowpark-java-udtf)  Python:  [UDF](/developer-guide/snowpark/python/creating-udfs), [UDAF](/developer-guide/snowpark/python/creating-udafs), [UDTF](/developer-guide/snowpark/python/creating-udtfs), [Vectorized UDF or UDTF](/developer-guide/snowpark/python/creating-udfs#label-snowpark-python-udf-vectorized)  Scala:  [UDF](/developer-guide/snowpark/scala/creating-udfs), [UDTF](/developer-guide/snowpark/scala/creating-udfs#label-snowpark-udtf) |
| **Command-line Interface**  [Snowflake CLI](/developer-guide/snowflake-cli/index) | Use the command line to create and manage Snowflake entities, specifying properties as properties of JSON objects. | [Managing Snowflake objects](/developer-guide/snowflake-cli/objects/manage-objects) |
| **Python**  [Snowflake Python API](/developer-guide/snowflake-python-api/snowflake-python-overview) | On the client, Execute commands to create the function with Python, writing the function’s handler in one of the supported handler languages. | [Managing user-defined functions (UDFs)](/developer-guide/snowflake-python-api/snowflake-python-managing-functions-procedures#label-snowflake-python-udfs) |
| **REST**  [Snowflake REST API](/developer-guide/snowflake-rest-api/snowflake-rest-api) | Make requests of RESTful endpoints to create and manage Snowflake entities. | [Manage user-defined functions](/developer-guide/snowflake-rest-api/user-defined-function/user-defined-function-introduction) |

Expand

Show lessSee more

When choosing a language, consider also the following:

- **Handler locations supported.** Not all languages support referring to the handler on a stage (the handler code must instead be in-line).
  For more information, see [Keeping handler code in-line or on a stage](/developer-guide/inline-or-staged).
- **Whether the handler results in a UDF that’s sharable.** A sharable UDF can be used with the Snowflake
  [Secure Data Sharing](/user-guide/data-sharing-intro) feature.

| Language | Handler Location | Sharable |
| --- | --- | --- |
| Java | In-line or staged | No [[1]](#footnote-1) |
| JavaScript | In-line | Yes |
| Python | In-line or staged | No [[2]](#footnote-2) |
| Scala | In-line or staged | No [[3]](#footnote-3) |
| SQL | In-line | Yes |

Expand

Show lessSee more

[1]
For more information about limits on sharing Java UDFs, see [General limitations](/developer-guide/udf/java/udf-java-limitations#label-limitations-on-java-udfs).

[2]
For more information about limits on sharing Python UDFs, see [General limitations](/developer-guide/udf/python/udf-python-limitations#label-limitations-on-python-udfs).

[3]
For more information about limits on sharing Scala UDFs, see [Scala UDF limitations](/developer-guide/udf/scala/udf-scala-limitations).

## Considerations

- If a query calls a UDF to access staged files, the operation fails with a user error if the SQL statement also queries a view that
  calls any UDF or UDTF, regardless of whether the function in the view accesses staged files or not.
- UDTFs can process multiple files in parallel; however, UDFs currently process files serially. As a workaround,
  group rows in a subquery using the [GROUP BY](/sql-reference/constructs/group-by) clause. See [Process a CSV with a UDTF](/user-guide/unstructured-data-java#label-unstructured-udtf-examples)
  for an example.
- Currently, if staged files referenced in a query are modified or deleted while the query is running, the function call fails with an
  error.
- If you specify the [CURRENT\_DATABASE](/sql-reference/functions/current_database) or [CURRENT\_SCHEMA](/sql-reference/functions/current_schema) function in the
  handler code of the UDF, the function returns the database or schema that contains the UDF, not the database or schema in use for
  the session.

## UDF example

Code in the following example creates a UDF called `addone` with a handler written in Python. The handler function is
`addone_py`. This UDF returns an `int`.

Copy code

```
CREATE OR REPLACE FUNCTION addone(i INT)
  RETURNS INT
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.12'
  HANDLER = 'addone_py'
AS $$
def addone_py(i):
 return i+1
$$;
```

Code in the following example executes the `addone` UDF.

Copy code

```
SELECT addone(3);
```

## Guidelines and constraints

Snowflake constraints:
:   You can ensure stability within the Snowflake environment by developing within Snowflake constraints. For
    more information, see [Designing Handlers that Stay Within Snowflake-Imposed Constraints](/developer-guide/udf-stored-procedure-constraints).

Naming:
:   Be sure to name functions in a way that avoids collisions with other functions. For more information, see
    [Naming and overloading procedures and UDFs](/developer-guide/udf-stored-procedure-naming-conventions).

Arguments:
:   Specify the arguments and indicate which arguments are optional. For more information, see
    [Defining arguments for UDFs and stored procedures](/developer-guide/udf-stored-procedure-arguments).

Data type mappings:
:   For each handler language, there’s a separate set of mappings between the language’s data types and the SQL types
    used for arguments and return values. For more about the mappings for each language, see [Data Type Mappings Between SQL and Handler Languages](/developer-guide/udf-stored-procedure-data-type-mapping).

## Handler writing

Handler languages:
:   For language-specific content on writing a handler, see [Supported languages and tools](#label-udf-supported-languages).

External network access:
:   You can access external network locations with
    [external network access](/developer-guide/external-network-access/external-network-access-overview). You can create secure
    access to specific network locations external to Snowflake, then use that access from within the handler code.

Logging, tracing, and metrics:
:   You can record code activity by
    [capturing log messages, trace events, and metrics data](/developer-guide/logging-tracing/logging-tracing-overview),
    storing the data in a database you can query later.

## Security

You can grant privileges on objects needed for them to perform specific SQL actions with a UDF or UDTF. For more information, see
[Granting privileges for user-defined functions](/developer-guide/udf/udf-access-control)

Functions share certain security concerns with stored procedures. For more information, see the following:

- You can help a procedure’s handler code execute securely by following the best practices described in
  [Security Practices for UDFs and Procedures](/developer-guide/udf-stored-procedure-security-practices)
- Ensure that sensitive information is concealed from users who should not have access to it. For more information, see
  [Protecting Sensitive Information with Secure UDFs and Stored Procedures](/developer-guide/secure-udf-procedure)

## Handler code deployment

When creating a function, you can specify its handler – which implements the function’s logic – as code in-line with the function
definition or as code external to the definition, such as code packaged and copied to a stage.

For more information, see [Keeping handler code in-line or on a stage](/developer-guide/inline-or-staged).
