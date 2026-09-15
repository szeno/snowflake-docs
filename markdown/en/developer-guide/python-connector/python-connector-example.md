# Using the Python Connector

This topic provides a series of examples that illustrate how to use the Snowflake Connector to perform standard Snowflake operations such as user login, database and table creation, warehouse creation,
data insertion/loading, and querying.

The sample code at the end of this topic combines the examples into a single, working Python program.

Note

Snowflake now provides first-class Python APIs for managing core Snowflake resources including databases, schemas, tables, tasks, and
warehouses, without using SQL. For more information, see [Snowflake Python APIs: Managing Snowflake objects with Python](/developer-guide/snowflake-python-api/snowflake-python-overview).

## Creating a database, schema, and warehouse

After you log in, create a database, schema, and warehouse if they don’t yet exist, using the
[CREATE DATABASE](/sql-reference/sql/create-database), [CREATE SCHEMA](/sql-reference/sql/create-schema), and
[CREATE WAREHOUSE](/sql-reference/sql/create-warehouse) commands.

The example below shows how to create a warehouse named `tiny_warehouse`, database named `testdb`, and a
schema named `testschema`. Note that when you create the schema, you must either specify the name of the
database in which to create the schema, or you must already be connected to the database in which to create the
schema. The example below executes a `USE DATABASE` command before the `CREATE SCHEMA` command to ensure
that the schema is created in the correct database.

> Copy code
>
> ```
> conn.cursor().execute("CREATE WAREHOUSE IF NOT EXISTS tiny_warehouse_mg")
> conn.cursor().execute("CREATE DATABASE IF NOT EXISTS testdb_mg")
> conn.cursor().execute("USE DATABASE testdb_mg")
> conn.cursor().execute("CREATE SCHEMA IF NOT EXISTS testschema_mg")
> ```

## Using the database, schema, and warehouse

Specify the database and schema in which you want to create tables. Also specify the warehouse that will provide
resources for executing DML statements and queries.

For example, to use the database `testdb`, schema `testschema` and warehouse `tiny_warehouse` (created earlier):

> Copy code
>
> ```
> conn.cursor().execute("USE WAREHOUSE tiny_warehouse_mg")
> conn.cursor().execute("USE DATABASE testdb_mg")
> conn.cursor().execute("USE SCHEMA testdb_mg.testschema_mg")
> ```

## Creating tables and inserting data

Use the [CREATE TABLE](/sql-reference/sql/create-table) command to create tables and the [INSERT](/sql-reference/sql/insert) command to populate the tables with data.

For example, create a table named `testtable` and insert two rows into the table:

> Copy code
>
> ```
> conn.cursor().execute(
>     "CREATE OR REPLACE TABLE "
>     "test_table(col1 integer, col2 string)")
>
> conn.cursor().execute(
>     "INSERT INTO test_table(col1, col2) VALUES " +
>     "    (123, 'test string1'), " +
>     "    (456, 'test string2')")
> ```

## Loading data

Instead of inserting data into tables using individual [INSERT](/sql-reference/sql/insert) commands, you can bulk load data from files staged in either an internal or external location.

### Copying data from an internal location

To load data from files on your host machine into a table, first use the [PUT](/sql-reference/sql/put) command to stage the file in an internal location, then use the
[COPY INTO <table>](/sql-reference/sql/copy-into-table) command to copy the data in the files into the table.

For example:

> Copy code
>
> ```
> # Putting Data
> con.cursor().execute("PUT file:///tmp/data/file* @%testtable")
> con.cursor().execute("COPY INTO testtable")
> ```
>
> Where your CSV data is stored in a local directory named `/tmp/data` in a Linux or macOS environment, and the directory contains files named `file0`, `file1`, … `file100`.

### Copying data from an external location

To load data from files already staged in an external location (i.e. your S3 bucket) into a table, use the [COPY INTO <table>](/sql-reference/sql/copy-into-table) command.

For example:

> Copy code
>
> ```
> # Copying Data
> con.cursor().execute("""
> COPY INTO testtable FROM s3://<s3_bucket>/data/
>     STORAGE_INTEGRATION = myint
>     FILE_FORMAT=(field_delimiter=',')
> """.format(
>     aws_access_key_id=AWS_ACCESS_KEY_ID,
>     aws_secret_access_key=AWS_SECRET_ACCESS_KEY))
> ```
>
> Where:
>
> - `s3://<s3_bucket>/data/` specifies the name of your S3 bucket
> - The files in the bucket are prefixed with `data`.
> - The bucket is accessed using a storage integration created using [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration) by an account administrator (i.e. a user with the ACCOUNTADMIN role) or a role with the global CREATE INTEGRATION privilege. A storage integration allows users to avoid supplying credentials to access a private storage location.

Note

This example uses the format() function to compose the statement. If your environment has a risk of SQL injection
attacks, you might prefer to bind values rather than use format().

## Querying data

With the Snowflake Connector for Python, you can submit:

- a [synchronous query](#label-python-connector-querying-data-synchronous), which returns control to your application after
  the query completes.
- an [asynchronous query](#label-python-connector-querying-data-asynchronous), which returns control to your application
  before the query completes.

After the query has completed, you use the `Cursor` object to
[fetch the values in the results](#label-python-connector-cursor-fetch-values). By default, the Snowflake Connector for
Python converts the values from [Snowflake data types](/sql-reference-data-types) to native Python data types. (Note that
you can choose to return the values as strings and perform the type conversions in your application.
See [Improving query performance by bypassing data conversion](#label-python-connector-bypass-data-conversion).)

Note

By default, values from NUMBER columns are returned as double-precision floating-point values (`float64`). To return these
as decimal values (`decimal.Decimal`) in the `fetch_pandas_all()` and `fetch_pandas_batches()` methods, set
the `arrow_number_to_decimal` parameter in the `connect()` method to `True`.

### Performing a synchronous query

To perform a synchronous query, call the `execute()` method in the `Cursor` object. For example:

Copy code

```
conn = snowflake.connector.connect( ... )
cur = conn.cursor()
cur.execute('select * from products')
```

Use the `Cursor` object to fetch the values in the results, as explained in
[Using to fetch values](#label-python-connector-cursor-fetch-values).

### Performing an asynchronous query

The Snowflake Connector for Python supports asynchronous queries (i.e. queries that return control to the user before the query
completes). You can submit an asynchronous query and use polling to determine when the query has completed. After the query
completes, you can get the results.

Note

To perform asynchronous queries, you must ensure the `ABORT_DETACHED_QUERY` configuration parameter is `FALSE` (default value).

If the connection to client is lost:

- For synchronous queries, all in-progress synchronous queries are aborted immediately regardless of the parameter value.
- For asynchronous queries:
  - If ABORT\_DETACHED\_QUERY is set to `FALSE`, in-progress asynchronous queries continue to run until they end normally.
  - If ABORT\_DETACHED\_QUERY is set to `TRUE`, Snowflake automatically aborts all in-progress asynchronous queries when a client connection is not re-established after five minutes.

    You can prevent the asynchronous query from being aborted at the five minute mark by calling `cursor.query_result(queryId)`. While this call does not retrieve the actual query result as the query is still running, it does prevent the query from being canceled. Invoking `query_result` is a synchronous operation, which might or might not be appropriate for your particular use case.

With this feature, you can submit multiple queries in parallel without waiting for each query to complete. You can also run a
combination of synchronous and asynchronous queries during the same session.

Note

Executing multiple statements in a single query requires that a valid warehouse is available in a session.

Finally, you can submit an asynchronous query from one connection and check the results from a different connection. For example,
a user can initiate a long-running query from your application, exit the application, and restart the application at a later time
to check the results.

To better understand the hierarchy of the drivers’ business logic and the ABORT\_DETACHED\_QUERY parameter’s interaction, see the following flowchart:

![Asynchronous query flowchart](/static/images/async_flow_li.drawio.png)

#### Submitting an asynchronous query

Note

Asynchronous queries don’t support PUT/GET statements.

When `cursor.execute_async(query)` is used, the Snowflake Python driver automatically keeps track of the queries submitted asynchronously. When the connection is explicitly closed with `connection.close()` or the context manager is used with `connect()...`, the list of async queries is examined and, if any of them are still running, the Snowflake-side session is not deleted.

If no async queries are running within the same connection, the Snowflake session belonging to the connection is logged out when `connection.close()` is called, which implicitly cancels all other queries running in the same session.

This behavior also depends on the SQL [ABORT\_DETACHED\_QUERY](/sql-reference/parameters#label-abort-detached-query) parameter.

As a best practice, isolate all long-running async tasks (especially those intended to continue after the connection is closed) into a separate connection.

You can use the `server_session_keep_alive` (default: `False`) connection parameter to override this automatic behavior. By default, the Snowflake session is logged out when `connection.close()` is called *only* when no async queries are running in it. The default behavior doesn’t consider or track sync queries.

When `server_session_keep_alive=True`, `connection.close()` won’t log out the Snowflake session, regardless of the status of any queries. For connections designed to issue long-running asynchronous queries, enabling this setting can reduce CPU overhead and accelerate the connection-closing process.

Important

Enabling this parameter might have unexpected, billable effects (for example, it might leave queries running up to the configured value of [STATEMENT\_TIMEOUT\_IN\_SECONDS](/sql-reference/parameters#label-statement-timeout-in-seconds)). Snowflake strongly recommends that you carefully decide whether changing the value of `server_session_keep_alive` from the default is needed and, if possible, thoroughly test the change in non-production environments before implementing it in production.

To submit an asynchronous query, call the `execute_async()` method in the `Cursor` object. For example:

Copy code

```
conn = snowflake.connector.connect( ... )
cur = conn.cursor()
# Submit an asynchronous query for execution.
cur.execute_async('select count(*) from table(generator(timeLimit => 25))')
```

After submitting the query:

- To determine if the query is still running, see [Checking the status of a query](#label-python-connector-check-query-status).
- To retrieve the results of the query, see [Using the query ID to retrieve the results of a query](#label-python-connector-retrieve-results).

For examples of performing asynchronous queries, see [Examples of asynchronous queries](#label-python-connector-asynchronous-query-examples).

#### Best practices for asynchronous queries

When submitting an asynchronous query, follow these best practices:

- Ensure that you know which queries are dependent upon other queries before you run any queries in parallel. Some queries are
  interdependent and order sensitive, and therefore not suitable for parallelizing. For example, obviously an INSERT statement
  should not start until after the corresponding CREATE TABLE statement has finished.
- Ensure that you do not run too many queries for the memory that you have available. Running multiple queries in parallel
  typically consumes more memory, especially if more than one set of results is stored in memory at the same time.
- When polling, handle the rare cases where a query does not succeed.
- Ensure that transaction control statements (BEGIN, COMMIT, and ROLLBACK) do not execute in parallel with other statements.
- Be aware that asynchronous queries are not guaranteed to return ordered results, even if the SQL itself has an ORDER BY clause. Consequently, the `result_scan` function does not guarantee ordered results.

### Retrieving the Snowflake query ID

A query ID identifies each query executed by Snowflake. When you use the Snowflake Connector for Python to execute a query, you
can access the query ID through the `sfqid` attribute in the `Cursor` object:

> Copy code
>
> ```
> # Retrieving a Snowflake Query ID
> cur = con.cursor()
> cur.execute("SELECT * FROM testtable")
> print(cur.sfqid)
> ```

You can use the query ID to:

- Check the status of the query in the web interface.

  In the Snowsight, query IDs are displayed in the **Query History** page.
  See [Monitor query activity with Query History](/user-guide/ui-snowsight-activity).
- Programmatically check the status of the query (e.g. to determine if an asynchronous query has completed).

  See [Checking the status of a query](#label-python-connector-check-query-status).
- Retrieve the results of an asynchronous query or a previously submitted synchronous query.

  See [Using the query ID to retrieve the results of a query](#label-python-connector-retrieve-results).
- Cancel a running query.

  See [Canceling a query by query ID](#label-python-connector-cancel-query-by-id).

### Checking the status of a query

To check the status of a query:

1. Get the query ID from the `sfqid` field in the `Cursor` object.
2. Pass the query ID to the `get_query_status()` method of the `Connection` object to return the
   `QueryStatus` enum constant that represents the status of the query.

   By default, `get_query_status()` does not raise an error if the query resulted in an error. If you want an error raised,
   call `get_query_status_throw_if_error()` instead.
3. Use the `QueryStatus` enum constant to check the status of the query.

   - To determine if the query is still running (for example, if this is an asynchronous query), pass the constant to the
     `is_still_running()` method of the `Connection` object.
   - To determine if an error occurred, pass the constant to the `is_an_error()` method.

   For the full list of enum constants, see `QueryStatus`.

The following example executes an asynchronous query and checks the status of the query:

Copy code

```
import time
...
# Execute a long-running query asynchronously.
cur.execute_async('select count(*) from table(generator(timeLimit => 25))')
...
# Wait for the query to finish running.
query_id = cur.sfqid
while conn.is_still_running(conn.get_query_status(query_id)):
  time.sleep(1)
```

The following example raises an error if the query has resulted in an error:

Copy code

```
from snowflake.connector import ProgrammingError
import time
...
# Wait for the query to finish running and raise an error
# if a problem occurred with the execution of the query.
try:
  query_id = cur.sfqid
  while conn.is_still_running(conn.get_query_status_throw_if_error(query_id)):
    time.sleep(1)
except ProgrammingError as err:
  print('Programming Error: {0}'.format(err))
```

### Using the query ID to retrieve the results of a query

Note

If you [performed a synchronous query](#label-python-connector-querying-data-synchronous) by calling the `execute()`
method on a `Cursor` object, you don’t need to use the query ID to retrieve the results. You can just fetch the values
from the results, as explained in [Using to fetch values](#label-python-connector-cursor-fetch-values).

If you want to retrieve the results of an asynchronous query or a previously submitted synchronous query, follow these steps:

1. Get the query ID of the query. See [Retrieving the Snowflake query ID](#label-python-connector-retrieve-query-id).
2. Call the `get_results_from_sfqid()` method in the `Cursor` object to retrieve the results.
3. Use the `Cursor` object to fetch the values in the results, as explained in
   [Using to fetch values](#label-python-connector-cursor-fetch-values).

Note that if the query is still running, the fetch methods (`fetchone()`, `fetchmany()`, `fetchall()`, etc.)
will wait for the query to complete.

For example:

Copy code

```
# Get the results from a query.
cur.get_results_from_sfqid(query_id)
results = cur.fetchall()
print(f'{results[0]}')
```

### Using `cursor` to fetch values

Fetch values from a table using the cursor object iterator method.

For example, to fetch columns named “col1” and “col2” from the table
named `testtable`, which was created earlier
(in [Creating tables and inserting data](#label-creating-tables-and-inserting-data-in-python)),
use code similar to the following:

> Copy code
>
> ```
> cur = conn.cursor()
> try:
>     cur.execute("SELECT col1, col2 FROM test_table ORDER BY col1")
>     for (col1, col2) in cur:
>         print('{0}, {1}'.format(col1, col2))
> finally:
>     cur.close()
> ```

Alternatively, the Snowflake Connector for Python provides a convenient shortcut:

> Copy code
>
> ```
> for (col1, col2) in con.cursor().execute("SELECT col1, col2 FROM testtable"):
>     print('{0}, {1}'.format(col1, col2))
> ```

If you need to get a single result (i.e. a single row), use the `fetchone` method:

> Copy code
>
> ```
> col1, col2 = con.cursor().execute("SELECT col1, col2 FROM testtable").fetchone()
> print('{0}, {1}'.format(col1, col2))
> ```

If you need to get the specified number of rows at a time, use the `fetchmany` method with the number of rows:

> Copy code
>
> ```
> cur = con.cursor().execute("SELECT col1, col2 FROM testtable")
> ret = cur.fetchmany(3)
> print(ret)
> while len(ret) > 0:
>     ret = cur.fetchmany(3)
>     print(ret)
> ```
>
> Note
>
> Use `fetchone` or `fetchmany` if the result set is too large
> to fit into memory.

If you need to get all results at once:

> Copy code
>
> ```
> results = con.cursor().execute("SELECT col1, col2 FROM testtable").fetchall()
> for rec in results:
>     print('%s, %s' % (rec[0], rec[1]))
> ```

To set a timeout for a query, execute a “begin” command and include a timeout parameter on the query. If the query exceeds the length of the parameter value, an error is produced and a rollback occurs.

In the following code, error 604 means the query was canceled. The timeout parameter starts `Timer()` and cancels if the query does not finish within the specified time.

> Copy code
>
> ```
> conn.cursor().execute("create or replace table testtbl(a int, b string)")
>
> conn.cursor().execute("begin")
> try:
>    conn.cursor().execute("insert into testtbl(a,b) values(3, 'test3'), (4,'test4')", timeout=10) # long query
>
> except ProgrammingError as e:
>    if e.errno == 604:
>       print("timeout")
>       conn.cursor().execute("rollback")
>    else:
>       raise e
> else:
>    conn.cursor().execute("commit")
> ```

### Using `DictCursor` to fetch values by column name

If you want to fetch a value by column name, create a `cursor` object of type `DictCursor`.

For example:

> Copy code
>
> ```
> # Querying data by DictCursor
> from snowflake.connector import DictCursor
> cur = con.cursor(DictCursor)
> try:
>     cur.execute("SELECT col1, col2 FROM testtable")
>     for rec in cur:
>         print('{0}, {1}'.format(rec['COL1'], rec['COL2']))
> finally:
>     cur.close()
> ```

### Examples of asynchronous queries

The following is a simple example of an asynchronous query:

Copy code

```
from snowflake.connector import ProgrammingError
import time

conn = snowflake.connector.connect( ... )
cur = conn.cursor()

# Submit an asynchronous query for execution.
cur.execute_async('select count(*) from table(generator(timeLimit => 25))')

# Retrieve the results.
cur.get_results_from_sfqid(query_id)
results = cur.fetchall()
print(f'{results[0]}')
```

The next example submits an asynchronous query from one connection and retrieves the results from a different connection:

Copy code

```
from snowflake.connector import ProgrammingError
import time

conn = snowflake.connector.connect( ... )
cur = conn.cursor()

# Submit an asynchronous query for execution.
cur.execute_async('select count(*) from table(generator(timeLimit => 25))')

# Get the query ID for the asynchronous query.
query_id = cur.sfqid

# Close the cursor and the connection.
cur.close()
conn.close()

# Open a new connection.
new_conn = snowflake.connector.connect( ... )

# Create a new cursor.
new_cur = new_conn.cursor()

# Retrieve the results.
new_cur.get_results_from_sfqid(query_id)
results = new_cur.fetchall()
print(f'{results[0]}')
```

### Canceling a query by query ID

Cancel a query by [query ID](#label-python-connector-retrieve-query-id):

> Copy code
>
> ```
> cur = cn.cursor()
>
> try:
>   cur.execute(r"SELECT SYSTEM$CANCEL_QUERY('queryID')")
>   result = cur.fetchall()
>   print(len(result))
>   print(result[0])
> finally:
>   cur.close()
> ```

Replace the string “queryID” with the actual query ID. To get the ID for a query, see
[Retrieving the Snowflake query ID](#label-python-connector-retrieve-query-id).

### Improving query performance by bypassing data conversion

To improve query performance, use the `SnowflakeNoConverterToPython` class in the `snowflake.connector.converter_null` module to bypass
data conversions from the Snowflake internal data type to the native Python data type, e.g.:

> Copy code
>
> ```
> from snowflake.connector.converter_null import SnowflakeNoConverterToPython
>
> con = snowflake.connector.connect(
>     ...
>     converter_class=SnowflakeNoConverterToPython
> )
> for rec in con.cursor().execute("SELECT * FROM large_table"):
>     # rec includes raw Snowflake data
> ```

As a result, all data is represented in string form such that the application is responsible for
converting it to the native Python data types. For example, `TIMESTAMP_NTZ` and `TIMESTAMP_LTZ`
data are the epoch time represented in string form, and `TIMESTAMP_TZ` data is the epoch time followed by a space
followed by the offset to UTC in minutes represented in string form.

No impact is made to binding data; Python native data can still be bound for updates.

## Downloading data

Snowflake Connector for Python version 3.14.0 introduced the `unsafe_file_write` connection parameter that specifies how the connector should set file permissions when downloading files for a Snowflake stage with the GET command. These files are always owned by the same user who runs the Python process.

By default, the `unsafe_file_write` parameter is `False` to provide a more secure and strict `600` file permission, which means that only the owner has read and write permissions of the downloaded files.
Other groups and users have no permissions for the files downloaded with the GET command.

If your organization requires less restrictive file permissions for the files, you can set the `unsafe_file_write` parameter to `True`.
Enabling this parameter sets the file permissions for the files downloaded from a stage to `644`, which allows the owner to read and write the files, but allows others only to read them.
This setting might be necessary, for example, for some ETL tools that run under a different system user who needs to be able to read and process the downloaded files.

If you are unsure of which value to use, consult with the team responsible for your organization’s applicable security policy.

## Binding data

To specify values to be used in a SQL statement, you can include literals in the statement, or you can
[bind variables](/sql-reference/bind-variables). When you bind variables, you put one or more
placeholders in the text of the SQL statement, and then specify the variable (the value to be used)
for each placeholder.

The following example contrasts the use of literals and binding:

> Literals:
>
> Copy code
>
> ```
> con.cursor().execute("INSERT INTO testtable(col1, col2) VALUES(789, 'test string3')")
> ```
>
> Binding:
>
> Copy code
>
> ```
> con.cursor().execute(
>     "INSERT INTO testtable(col1, col2) "
>     "VALUES(%s, %s)", (
>         789,
>         'test string3'
>     ))
> ```

Note

There is an upper limit to the size of data that you can bind, or that you can combine in a batch. For details, see [Limits on Query Text Size](/user-guide/query-size-limits).

Snowflake supports the following types of binding:

- `pyformat` and `format`, which [bind data on the client](#label-python-connector-binding-data-client).
- `qmark` and `numeric`, which [bind data on the server](#label-python-connector-binding-data-server).

Each of these is explained below.

### `pyformat` or `format` binding

Both `pyformat` binding and `format` binding bind data on the client side rather than on the server side.

By default, the Snowflake Connector for Python supports both `pyformat` and `format`, so you can use `%(name)s` or `%s` as the
placeholder. For example:

- Using `%(name)s` as the placeholder:

  > Copy code
  >
  > ```
  > conn.cursor().execute(
  >  "INSERT INTO test_table(col1, col2) "
  >  "VALUES(%(col1)s, %(col2)s)", {
  >      'col1': 789,
  >      'col2': 'test string3',
  >      })
  > ```
- Using `%s` as the placeholder:

  Copy code

  ```
  con.cursor().execute(
   "INSERT INTO testtable(col1, col2) "
   "VALUES(%s, %s)", (
       789,
       'test string3'
   ))
  ```

With `pyformat` and `format`, you can also use a list object to bind data for the IN operator:

> Copy code
>
> ```
> # Binding data for IN operator
> con.cursor().execute(
>     "SELECT col1, col2 FROM testtable"
>     " WHERE col2 IN (%s)", (
>         ['test string1', 'test string3'],
>     ))
> ```

The percent character (“%”) is both a wildcard character for SQL LIKE and a format binding character for Python. If you
use format binding, and if your SQL command contains the percent character, you might need to escape the percent
character. For example, if your SQL statement is:

> Copy code
>
> ```
> SELECT col1, col2
>     FROM test_table
>     WHERE col2 ILIKE '%York' LIMIT 1;  -- Find York, New York, etc.
> ```

then your Python code should look like the following (note the extra percent sign to escape the original percent sign):

> Copy code
>
> ```
> sql_command = "select col1, col2 from test_table "
> sql_command += " where col2 like '%%York' limit %(lim)s"
> parameter_dictionary = {'lim': 1 }
> cur.execute(sql_command, parameter_dictionary)
> ```

### `qmark` or `numeric` binding

Both `qmark` binding and `numeric` binding bind data on the server side rather than on the client side:

- For `qmark` binding, use a question mark character (`?`) to indicate where in the string you want a variable’s value
  inserted.
- For `numeric` binding, use a colon (`:`) followed by a number to indicate the position of the variable that you want
  substituted at that position. For example, `:2` specifies the second variable.

  Use numeric binding to bind the same value more than once in the same query. For example, if you have a long VARCHAR or BINARY
  or [semi-structured](/sql-reference/data-types-semistructured) value that you want to use more than once, then `numeric`
  binding allows you to send the value to the server once and use it multiple times.

The next sections explain how to use `qmark` and `numeric` binding:

- [Using or binding](#label-python-connector-binding-using-qmark)
- [Using or binding with objects](#label-python-connector-binding-timestmamp-qmark)
- [Using bind variables with the IN operator](#label-python-connector-binding-in-operator-qmark)

#### Using `qmark` or `numeric` binding

To use `qmark` or `numeric` style binding, you can either execute one of the following or set `paramstyle` as part of the connection parameters when calling `connect()`.

- `snowflake.connector.paramstyle='qmark'`
- `snowflake.connector.paramstyle='numeric'`

If you set `paramstyle` to `qmark` or `numeric`, you must use `?` or `:N` (where `N` is replaced
with a number) as the placeholders, respectively.

For example:

- Using `?` as the placeholder:

  Copy code

  ```
  from snowflake.connector import connect

  connection_parameters = {
   'account': 'xxxxx',
   'user': 'xxxx',
   'password': 'xxxxxx',
   "host": "xxxxxx",
   "port": 443,
   'protocol': 'https',
   'warehouse': 'xxx',
   'database': 'xxx',
   'schema': 'xxx',
   'paramstyle': 'qmark'  # note paramstyle setting here at connection level
  }

  con = connect(**connection_parameters)

  con.cursor().execute(
   "INSERT INTO testtable2(col1,col2,col3) "
   "VALUES(?,?,?)", (
       987,
       'test string4',
       ("TIMESTAMP_LTZ", datetime.now())
   )
  )
  ```
- Using `:N` as the placeholder:

  Copy code

  ```
  import snowflake.connector

  snowflake.connector.paramstyle='numeric'

  con = snowflake.connector.connect(...)

  con.cursor().execute(
   "INSERT INTO testtable(col1, col2) "
   "VALUES(:1, :2)", (
       789,
       'test string3'
   ))
  ```

  The following query shows how to use `numeric` binding to reuse a variable:

  Copy code

  ```
  con.cursor().execute(
   "INSERT INTO testtable(complete_video, short_sample_of_video) "
   "VALUES(:1, SUBSTRING(:1, :2, :3))", (
       binary_value_that_stores_video,          # variable :1
       starting_offset_in_bytes_of_video_clip,  # variable :2
       length_in_bytes_of_video_clip            # variable :3
   ))
  ```

#### Using `qmark` or `numeric` binding with `datetime` objects

When using `qmark` or `numeric` binding to bind data to a Snowflake TIMESTAMP data type, set the bind variable to a tuple that
specifies the Snowflake timestamp data type (`TIMESTAMP_LTZ` or `TIMESTAMP_TZ`) and the value. For example:

> Copy code
>
> ```
> import snowflake.connector
>
> snowflake.connector.paramstyle='qmark'
>
> con = snowflake.connector.connect(...)
>
> con.cursor().execute(
>     "CREATE OR REPLACE TABLE testtable2 ("
>     "   col1 int, "
>     "   col2 string, "
>     "   col3 timestamp_ltz"
>     ")"
> )
>
> con.cursor().execute(
>     "INSERT INTO testtable2(col1,col2,col3) "
>     "VALUES(?,?,?)", (
>         987,
>         'test string4',
>         ("TIMESTAMP_LTZ", datetime.now())
>     )
>  )
> ```

Unlike client side binding, the server side binding requires the Snowflake data type for the column. Most common Python data types
already have implicit mappings to Snowflake data types (e.g. `int` is mapped to `FIXED`). However, because the Python
`datetime` data can be bound to one of multiple Snowflake data types (`TIMESTAMP_NTZ`, `TIMESTAMP_LTZ`,
or `TIMESTAMP_TZ`), and the default mapping is `TIMESTAMP_NTZ`, you must specify the Snowflake data type to use.

#### Using bind variables with the IN operator

`qmark` and `numeric` (server side binding) do not support the use of bind variables with the IN operator.

If you need to use bind variables with the IN operator, use
[client side binding](#label-python-connector-binding-data-client) (`pyformat` or `format`).

### Binding parameters to variables for batch inserts

In your application code, you can insert multiple rows in a single batch. To do this, use parameters for values in an INSERT
statement. For example, the following statement uses placeholders for `qmark` binding in an INSERT statement:

> Copy code
>
> ```
> insert into grocery (item, quantity) values (?, ?)
> ```

Then, to specify the data that should be inserted, define a variable that is a sequence of sequences (for example, a list of
tuples):

> Copy code
>
> ```
> rows_to_insert = [('milk', 2), ('apple', 3), ('egg', 2)]
> ```

As shown in the example above, each item in the list is a tuple that contains the column values for a row to be inserted.

To perform the binding, call the `executemany()` method, passing the variable as the second argument. For example:

> Copy code
>
> ```
> conn = snowflake.connector.connect( ... )
> rows_to_insert = [('milk', 2), ('apple', 3), ('egg', 2)]
> conn.cursor().executemany(
>     "insert into grocery (item, quantity) values (?, ?)",
>     rows_to_insert)
> ```

If you are [binding data on the server](#label-python-connector-binding-data-server) (i.e. by using `qmark` or
`numeric` binding), the connector can optimize the performance of batch inserts through binding.

When you use this technique to insert a large number of values, the driver can improve performance by streaming the data (without
creating files on the local machine) to a temporary stage for ingestion. The driver automatically does this when the number of
values exceeds a threshold.

In addition, the current database and schema for the session must be set. If these are not set, the CREATE TEMPORARY STAGE command
executed by the driver can fail with the following error:

Copy code

```
CREATE TEMPORARY STAGE SYSTEM$BIND file_format=(type=csv field_optionally_enclosed_by='"')
Cannot perform CREATE STAGE. This session does not have a current schema. Call 'USE SCHEMA', or use a qualified name.
```

Note

For alternative ways to load data into the Snowflake database (including bulk loading using the COPY command), see
[Load data into Snowflake](/guides-overview-loading-data).

### Avoid SQL injection attacks

Avoid binding data using Python’s formatting function because you risk SQL injection. For example:

> Copy code
>
> ```
> # Binding data (UNSAFE EXAMPLE)
> con.cursor().execute(
>     "INSERT INTO testtable(col1, col2) "
>     "VALUES(%(col1)d, '%(col2)s')" % {
>         'col1': 789,
>         'col2': 'test string3'
>     })
> ```
>
> Copy code
>
> ```
> # Binding data (UNSAFE EXAMPLE)
> con.cursor().execute(
>     "INSERT INTO testtable(col1, col2) "
>     "VALUES(%d, '%s')" % (
>         789,
>         'test string3'
>     ))
> ```
>
> Copy code
>
> ```
> # Binding data (UNSAFE EXAMPLE)
> con.cursor().execute(
>     "INSERT INTO testtable(col1, col2) "
>     "VALUES({col1}, '{col2}')".format(
>         col1=789,
>         col2='test string3')
>     )
> ```

Instead, store the values in variables and then bind those variables using qmark or numeric binding style.

## Retrieving column metadata

To retrieve metadata about each column in the result set (e.g. the name, type, precision, scale, etc. of each column), use one of
the following approaches:

- To access the metadata after calling the `execute()` method to execute the query, use the `description`
  attribute of the `Cursor` object.
- To access the metadata without having to execute the query, call the `describe()` method.

  The `describe` method is available in the Snowflake Connector for Python 2.4.6 and more recent versions.

The `description` attribute is set to one of the following values:

- **Version 2.4.5 and earlier:** A list of tuples.
- **Version 2.4.6 and later:** A list of [ResultMetadata](/developer-guide/python-connector/python-connector-api#label-python-connector-resultmetadata-object) objects. (The
  `describe` method also returns this list.)

Each tuple and `ResultMetadata` object contains the metadata for a column (the column name, data type, etc.). You can
[access the metadata by index](/developer-guide/python-connector/python-connector-api#label-python-connector-metadata-fields) or, in 2.4.6 and later versions, by
`ResultMetadata` attribute.

The following examples demonstrate how to access the metadata from the returned tuples and `ResultMetadata` objects.

**Example: Getting the column name metadata by index (versions 2.4.5 and earlier):**

The following example uses the `description` attribute to retrieve the list of column names after executing a query. The
attribute is a list of tuples, and the
example accesses the column name from the first value in each tuple.

> Copy code
>
> ```
> cur = conn.cursor()
> cur.execute("SELECT * FROM test_table")
> print(','.join([col[0] for col in cur.description]))
> ```

**Example: Getting the column name metadata by attribute (versions 2.4.6 and later):**

The following example uses the `description` attribute to retrieve the list of column names after executing a query. The
attribute is a list of [ResultMetaData](/developer-guide/python-connector/python-connector-api#label-python-connector-resultmetadata-object) objects, and the
example accesses the column name from the `name` attribute of each `ResultMetadata` object.

> Copy code
>
> ```
> cur = conn.cursor()
> cur.execute("SELECT * FROM test_table")
> print(','.join([col.name for col in cur.description]))
> ```

**Example: Getting the column name metadata without executing the query (versions 2.4.6 and later):**

The following example uses the `describe` method to retrieve the list of column names without executing a query.
The `describe()` method returns a list of [ResultMetaData](/developer-guide/python-connector/python-connector-api#label-python-connector-resultmetadata-object) objects, and the
example accesses the column name from the `name` attribute of each `ResultMetadata` object.

> Copy code
>
> ```
> cur = conn.cursor()
> result_metadata_list = cur.describe("SELECT * FROM test_table")
> print(','.join([col.name for col in result_metadata_list]))
> ```

## Handling errors

The application must handle exceptions raised from Snowflake Connector properly and decide to continue or stop running the code.

> Copy code
>
> ```
> # Catching the syntax error
> cur = con.cursor()
> try:
>     cur.execute("SELECT * FROM testtable")
> except snowflake.connector.errors.ProgrammingError as e:
>     # default error message
>     print(e)
>     # customer error message
>     print('Error {0} ({1}): {2} ({3})'.format(e.errno, e.sqlstate, e.msg, e.sfqid))
> finally:
>     cur.close()
> ```

## Using `execute_stream` to execute SQL scripts

The `execute_stream` function enables you to run one or more SQL scripts in a stream:

> Copy code
>
> ```
> from codecs import open
> with open(sqlfile, 'r', encoding='utf-8') as f:
>     for cur in con.execute_stream(f):
>         for ret in cur:
>             print(ret)
> ```

Note

Additional configuration might be required if `sql_stream` contains comments. See [Using execute\_stream to execute SQL scripts](/developer-guide/python-connector/python-connector-api#label-python-execute-stream).

## Closing the connection

As a best practice, close the connection by calling the `close` method:

> Copy code
>
> ```
> connection.close()
> ```

This ensures the collected client metrics are submitted to the server and the session is deleted. Also, `try-finally` blocks help ensure the connection is closed even if an exception is raised in the middle:

> Copy code
>
> ```
> # Connecting to Snowflake
> con = snowflake.connector.connect(...)
> try:
>     # Running queries
>     con.cursor().execute(...)
>     ...
> finally:
>     # Closing the connection
>     con.close()
> ```

Caution

Multiple non-closed connections can exhaust your system resources and eventually cause an application crash.

## Using context manager to connect and control transactions

The Snowflake Connector for Python supports a context manager that allocates and releases resources as required. The context manager is useful for committing or rolling back transactions based on the statement status when `autocommit` is disabled.

> Copy code
>
> ```
> # Connecting to Snowflake using the context manager
> with snowflake.connector.connect(
>   user=USER,
>   password=PASSWORD,
>   account=ACCOUNT,
>   autocommit=False,
> ) as con:
>     con.cursor().execute("INSERT INTO a VALUES(1, 'test1')")
>     con.cursor().execute("INSERT INTO a VALUES(2, 'test2')")
>     con.cursor().execute("INSERT INTO a VALUES(not numeric value, 'test3')") # fail
> ```

In the above example, when the third statement fails, the context manager rolls back the changes in the transaction and closes the connection. If all statements were successful, the context manager would commit the changes and close the connection.

An equivalent code with `try` and `except` blocks is as follows:

> Copy code
>
> ```
> # Connecting to Snowflake using try and except blocks
> con = snowflake.connector.connect(
>   user=USER,
>   password=PASSWORD,
>   account=ACCOUNT,
>   autocommit=False)
> try:
>     con.cursor().execute("INSERT INTO a VALUES(1, 'test1')")
>     con.cursor().execute("INSERT INTO a VALUES(2, 'test2')")
>     con.cursor().execute("INSERT INTO a VALUES(not numeric value, 'test3')") # fail
>     con.commit()
> except Exception as e:
>     con.rollback()
>     raise e
> finally:
>     con.close()
> ```

## Using the VECTOR data type

Support for the [VECTOR data type](/sql-reference/data-types-vector) was introduced in version 3.6.0 of the
Snowflake Python Connector. You can use the VECTOR data type with the [vector similarity functions](/sql-reference/functions-vector)
to implement applications based on vector search or retrieval-augmented-generation (RAG).

The following code example shows how to use the Python Connector to create tables with VECTOR columns and call the
[VECTOR\_INNER\_PRODUCT](/sql-reference/functions/vector_inner_product) function:

Copy code

```
import snowflake.connector

conn = ... # Set up connection
cur = conn.cursor()

# Create a table and insert some vectors
cur.execute("CREATE OR REPLACE TABLE vectors (a VECTOR(FLOAT, 3), b VECTOR(FLOAT, 3))")
values = [([1.1, 2.2, 3], [1, 1, 1]), ([1, 2.2, 3], [4, 6, 8])]
for row in values:
    cur.execute(f"""
        INSERT INTO vectors(a, b)
          SELECT {row[0]}::VECTOR(FLOAT,3), {row[1]}::VECTOR(FLOAT,3)
    """)

# Compute the pairwise inner product between columns a and b
cur.execute("SELECT VECTOR_INNER_PRODUCT(a, b) FROM vectors")
print(cur.fetchall())
```

```
[(6.30...,), (41.2...,)]
```

The following code example shows how to use the Python Connector to call the [VECTOR\_COSINE\_SIMILARITY](/sql-reference/functions/vector_cosine_similarity) in order to find the closest vectors to `[1,2,3]`:

Copy code

```
cur.execute(f"""
    SELECT a, VECTOR_COSINE_SIMILARITY(a, {[1,2,3]}::VECTOR(FLOAT, 3))
      AS similarity
      FROM vectors
      ORDER BY similarity DESC
      LIMIT 1;
""")
print(cur.fetchall())
```

```
[([1.0, 2.2..., 3.0], 0.9990...)]
```

Note

Variable binds are not supported for VECTOR data types.

## Logging

The Snowflake Connector for Python leverages the standard Python `logging` module to log status at regular intervals so that the application can trace its activity working behind the scenes. The
simplest way to enable logging is call `logging.basicConfig()` in the beginning of the application.

For example, to set the logging level to `INFO` and store the logs in a file named `/tmp/snowflake_python_connector.log`:

> Copy code
>
> ```
> logging.basicConfig(
>     filename=file_name,
>     level=logging.INFO)
> ```

More comprehensive logging can be enabled by setting the logging level to `DEBUG` as follows:

> Copy code
>
> ```
> # Logging including the timestamp, thread and the source code location
> import logging
> for logger_name in ['snowflake.connector', 'botocore', 'boto3']:
>     logger = logging.getLogger(logger_name)
>     logger.setLevel(logging.DEBUG)
>     ch = logging.FileHandler('/tmp/python_connector.log')
>     ch.setLevel(logging.DEBUG)
>     ch.setFormatter(logging.Formatter('%(asctime)s - %(threadName)s %(filename)s:%(lineno)d - %(funcName)s() - %(levelname)s - %(message)s'))
>     logger.addHandler(ch)
> ```
>
> The optional but recommended SecretDetector formatter class ensures that a certain set of known sensitive
> information is masked before being written to Snowflake Python Connector log files. To use SecretDetector, use
> code similar to the following:
>
> Copy code
>
> ```
> # Logging including the timestamp, thread and the source code location
> import logging
> from snowflake.connector.secret_detector import SecretDetector
> for logger_name in ['snowflake.connector', 'botocore', 'boto3']:
>     logger = logging.getLogger(logger_name)
>     logger.setLevel(logging.DEBUG)
>     ch = logging.FileHandler('/tmp/python_connector.log')
>     ch.setLevel(logging.DEBUG)
>     ch.setFormatter(SecretDetector('%(asctime)s - %(threadName)s %(filename)s:%(lineno)d - %(funcName)s() - %(levelname)s - %(message)s'))
>     logger.addHandler(ch)
> ```
>
> Note
>
> `botocore` and `boto3` are available through the AWS (Amazon Web Services) SDK for Python.

### Logging configuration file

Alternatively, you can easily specify the log level and the directory in which to save log files in the `config.toml` configuration file. For more information about the this file, see [Connecting using the `connections.toml` file](/developer-guide/python-connector/python-connector-connect#label-python-connection-toml).

Note

This logging configuration feature supports log levels as defined in the Python logging document.

For more information about logging levels, see the Python [Basic Logging Tutorial](https://docs.python.org/3/howto/logging.html#basic-logging-tutorial).

This logging configuration file uses toml to define the `save_logs`, `level`, and `path` logging parameters, as follows:

Copy code

```
[log]
save_logs = true
level = "INFO"
path = "<directory to store logs>"
```

where:

- `save_logs` determines whether to save logs.
- `level` specifies the logging level. If not defined, the driver defaults to `INFO`.
- `path` identifies the directory in which to save the log files. If not defined, the driver saves the logs in the default `$SNOWFLAKE_HOME/logs/` directory.

Note

If your `config.toml` file does not contain a `[log]` section, log messages are not saved.

Log message from a single day are appended to the `python-connector.log` file, which is later renamed to `python-connector.log.YYYY-MM-DD`.

## Sample program

The following sample code combines many of the examples described in the previous sections into a working python
program. This example contains two parts:

- A parent class (“python\_veritas\_base”) contains the code for many common operations, such as connecting to the server.
- A child class (“python\_connector\_example”) represents the custom portions of a particular client, for example,
  querying a table.

This sample code is imported directly from one of our tests to help ensure that it is has been executed on a recent
build of the product.

Because this is taken from a test, it includes a small amount of code to set an alternative port and protocol used in
some tests. Users should not set the protocol or port number; instead, omit these and use the defaults.

This also contains some section markers (sometimes called “snippet tags”) to identify code that can be imported
independently into the documentation. Section markers typically look similar to:

Copy code

```
# -- (> ---------------------- SECTION=import_connector ---------------------
...
# -- <) ---------------------------- END_SECTION ----------------------------
```

These section markers are not required in user code.

The first part of the code sample contains the common subroutines to:

- Read command-line arguments (for example, “–warehouse MyWarehouse”) that contain connection information.
- Connect to the server.
- Create and use a warehouse, database, and schema.
- Drop the schema, database, and warehouse when you are done with them.

Copy code

```
import logging
import os
import sys

# -- (> ---------------------- SECTION=import_connector ---------------------
import snowflake.connector
# -- <) ---------------------------- END_SECTION ----------------------------

class python_veritas_base:

    """
    PURPOSE:
        This is the Base/Parent class for programs that use the Snowflake
        Connector for Python.
        This class is intended primarily for:
            * Sample programs, e.g. in the documentation.
            * Tests.
    """

    def __init__(self, p_log_file_name = None):

        """
        PURPOSE:
            This does any required initialization steps, which in this class is
            basically just turning on logging.
        """

        file_name = p_log_file_name
        if file_name is None:
            file_name = '/tmp/snowflake_python_connector.log'

        # -- (> ---------- SECTION=begin_logging -----------------------------
        logging.basicConfig(
            filename=file_name,
            level=logging.INFO)
        # -- <) ---------- END_SECTION ---------------------------------------

    # -- (> ---------------------------- SECTION=main ------------------------
    def main(self, argv):

        """
        PURPOSE:
            Most tests follow the same basic pattern in this main() method:
               * Create a connection.
               * Set up, e.g. use (or create and use) the warehouse, database,
                 and schema.
               * Run the queries (or do the other tasks, e.g. load data).
               * Clean up. In this test/demo, we drop the warehouse, database,
                 and schema. In a customer scenario, you'd typically clean up
                 temporary tables, etc., but wouldn't drop your database.
               * Close the connection.
        """

        # Read the connection parameters (e.g. user ID) from the command line
        # and environment variables, then connect to Snowflake.
        connection = self.create_connection(argv)

        # Set up anything we need (e.g. a separate schema for the test/demo).
        self.set_up(connection)

        # Do the "real work", for example, create a table, insert rows, SELECT
        # from the table, etc.
        self.do_the_real_work(connection)

        # Clean up. In this case, we drop the temporary warehouse, database, and
        # schema.
        self.clean_up(connection)

        print("\nClosing connection...")
        # -- (> ------------------- SECTION=close_connection -----------------
        connection.close()
        # -- <) ---------------------------- END_SECTION ---------------------

    # -- <) ---------------------------- END_SECTION=main --------------------

    def args_to_properties(self, args):

        """
        PURPOSE:
            Read the command-line arguments and store them in a dictionary.
            Command-line arguments should come in pairs, e.g.:
                "--user MyUser"
        INPUTS:
            The command line arguments (sys.argv).
        RETURNS:
            Returns the dictionary.
        DESIRABLE ENHANCEMENTS:
            Improve error detection and handling.
        """

        connection_parameters = {}

        i = 1
        while i < len(args) - 1:
            property_name = args[i]
            # Strip off the leading "--" from the tag, e.g. from "--user".
            property_name = property_name[2:]
            property_value = args[i + 1]
            connection_parameters[property_name] = property_value
            i += 2

        return connection_parameters

    def create_connection(self, argv):

        """
        PURPOSE:
            This gets account identifier and login information from the
            environment variables and command-line parameters, connects to the
            server, and returns the connection object.
        INPUTS:
            argv: This is usually sys.argv, which contains the command-line
                  parameters. It could be an equivalent substitute if you get
                  the parameter information from another source.
        RETURNS:
            A connection.
        """

        # Get account identifier and login information from environment variables and command-line parameters.
        # For information about account identifiers, see
        # https://docs.snowflake.com/en/user-guide/admin-account-identifier.html .
        # -- (> ----------------------- SECTION=set_login_info ---------------

        # Get the password from an appropriate environment variable, if
        # available.
        PASSWORD = os.getenv('SNOWSQL_PWD')

        # Get the other login info etc. from the command line.
        if len(argv) < 11:
            msg = "ERROR: Please pass the following command-line parameters:\n"
            msg += "--warehouse <warehouse> --database <db> --schema <schema> "
            msg += "--user <user> --account <account_identifier> "
            print(msg)
            sys.exit(-1)
        else:
            connection_parameters = self.args_to_properties(argv)
            USER = connection_parameters["user"]
            ACCOUNT = connection_parameters["account"]
            WAREHOUSE = connection_parameters["warehouse"]
            DATABASE = connection_parameters["database"]
            SCHEMA = connection_parameters["schema"]
            # Optional: for internal testing only.
            try:
                PORT = connection_parameters["port"]
            except:
                PORT = ""
            try:
                PROTOCOL = connection_parameters["protocol"]
            except:
                PROTOCOL = ""

        # If the password is set by both command line and env var, the
        # command-line value takes precedence over (is written over) the
        # env var value.

        # If the password wasn't set either in the environment var or on
        # the command line...
        if PASSWORD is None or PASSWORD == '':
            print("ERROR: Set password, e.g. with SNOWSQL_PWD environment variable")
            sys.exit(-2)
        # -- <) ---------------------------- END_SECTION ---------------------

        # Optional diagnostic:
        #print("USER:", USER)
        #print("ACCOUNT:", ACCOUNT)
        #print("WAREHOUSE:", WAREHOUSE)
        #print("DATABASE:", DATABASE)
        #print("SCHEMA:", SCHEMA)
        #print("PASSWORD:", PASSWORD)
        #print("PROTOCOL:" "'" + PROTOCOL + "'")
        #print("PORT:" + "'" + PORT + "'")

        print("Connecting...")
        # If the PORT is set but the protocol is not, we ignore the PORT (bug!!).
        if PROTOCOL is None or PROTOCOL == "" or PORT is None or PORT == "":
            # -- (> ------------------- SECTION=connect_to_snowflake ---------
            conn = snowflake.connector.connect(
                user=USER,
                password=PASSWORD,
                account=ACCOUNT,
                warehouse=WAREHOUSE,
                database=DATABASE,
                schema=SCHEMA
                )
            # -- <) ---------------------------- END_SECTION -----------------
        else:

            conn = snowflake.connector.connect(
                user=USER,
                password=PASSWORD,
                account=ACCOUNT,
                warehouse=WAREHOUSE,
                database=DATABASE,
                schema=SCHEMA,
                # Optional: for internal testing only.
                protocol=PROTOCOL,
                port=PORT
                )

        return conn

    def set_up(self, connection):

        """
        PURPOSE:
            Set up to run a test. You can override this method with one
            appropriate to your test/demo.
        """

        # Create a temporary warehouse, database, and schema.
        self.create_warehouse_database_and_schema(connection)

    def do_the_real_work(self, conn):

        """
        PURPOSE:
            Your sub-class should override this to include the code required for
            your documentation sample or your test case.
            This default method does a very simple self-test that shows that the
            connection was successful.
        """

        # Create a cursor for this connection.
        cursor1 = conn.cursor()
        # This is an example of an SQL statement we might want to run.
        command = "SELECT PI()"
        # Run the statement.
        cursor1.execute(command)
        # Get the results (should be only one):
        for row in cursor1:
            print(row[0])
        # Close this cursor.
        cursor1.close()

    def clean_up(self, connection):

        """
        PURPOSE:
            Clean up after a test. You can override this method with one
            appropriate to your test/demo.
        """

        # Create a temporary warehouse, database, and schema.
        self.drop_warehouse_database_and_schema(connection)

    def create_warehouse_database_and_schema(self, conn):

        """
        PURPOSE:
            Create the temporary schema, database, and warehouse that we use
            for most tests/demos.
        """

        # Create a database, schema, and warehouse if they don't already exist.
        print("\nCreating warehouse, database, schema...")
        # -- (> ------------- SECTION=create_warehouse_database_schema -------
        conn.cursor().execute("CREATE WAREHOUSE IF NOT EXISTS tiny_warehouse_mg")
        conn.cursor().execute("CREATE DATABASE IF NOT EXISTS testdb_mg")
        conn.cursor().execute("USE DATABASE testdb_mg")
        conn.cursor().execute("CREATE SCHEMA IF NOT EXISTS testschema_mg")
        # -- <) ---------------------------- END_SECTION ---------------------

        # -- (> --------------- SECTION=use_warehouse_database_schema --------
        conn.cursor().execute("USE WAREHOUSE tiny_warehouse_mg")
        conn.cursor().execute("USE DATABASE testdb_mg")
        conn.cursor().execute("USE SCHEMA testdb_mg.testschema_mg")
        # -- <) ---------------------------- END_SECTION ---------------------

    def drop_warehouse_database_and_schema(self, conn):

        """
        PURPOSE:
            Drop the temporary schema, database, and warehouse that we create
            for most tests/demos.
        """

        # -- (> ------------- SECTION=drop_warehouse_database_schema ---------
        conn.cursor().execute("DROP SCHEMA IF EXISTS testschema_mg")
        conn.cursor().execute("DROP DATABASE IF EXISTS testdb_mg")
        conn.cursor().execute("DROP WAREHOUSE IF EXISTS tiny_warehouse_mg")
        # -- <) ---------------------------- END_SECTION ---------------------

# ----------------------------------------------------------------------------

if __name__ == '__main__':
    pvb = python_veritas_base()
    pvb.main(sys.argv)
```

The second part of the code sample creates a table, inserts rows into it, etc.:

Copy code

```
import sys

# -- (> ---------------------- SECTION=import_connector ---------------------
import snowflake.connector
# -- <) ---------------------------- END_SECTION ----------------------------

# Import the base class that contains methods used in many tests and code
# examples.
from python_veritas_base import python_veritas_base

class python_connector_example (python_veritas_base):

  """
  PURPOSE:
      This is a simple example program that shows how to use the Snowflake
      Python Connector to create and query a table.
  """

  def __init__(self):
    pass

  def do_the_real_work(self, conn):

    """
    INPUTS:
        conn is a Connection object returned from snowflake.connector.connect().
    """

    print("\nCreating table test_table...")
    # -- (> ----------------------- SECTION=create_table ---------------------
    conn.cursor().execute(
        "CREATE OR REPLACE TABLE "
        "test_table(col1 integer, col2 string)")

    conn.cursor().execute(
        "INSERT INTO test_table(col1, col2) VALUES " +
        "    (123, 'test string1'), " +
        "    (456, 'test string2')")
    # -- <) ---------------------------- END_SECTION -------------------------

    print("\nSelecting from test_table...")
    # -- (> ----------------------- SECTION=querying_data --------------------
    cur = conn.cursor()
    try:
        cur.execute("SELECT col1, col2 FROM test_table ORDER BY col1")
        for (col1, col2) in cur:
            print('{0}, {1}'.format(col1, col2))
    finally:
        cur.close()
    # -- <) ---------------------------- END_SECTION -------------------------

# ============================================================================

if __name__ == '__main__':

    test_case = python_connector_example()
    test_case.main(sys.argv)
```

To run this sample, do the following:

> 1. Copy the first piece of code to a file named “python\_veritas\_base.py”.
> 2. Copy the second piece of code to a file named “python\_connector\_example.py”
> 3. Set the SNOWSQL\_PWD environment variable to your password, for example:
>
>    Copy code
>
>    ```
>    export SNOWSQL_PWD='MyPassword'
>    ```
> 4. Execute the program using a command line similar to the following (replace the user and account information
>    with your own user and account information, of course).
>
>    Warning
>
>    This deletes the warehouse, database, and schema at the end of the program! Do not use
>    the name of an existing database because you will lose it!
>
>    Copy code
>
>    ```
>    python3 python_connector_example.py --warehouse <unique_warehouse_name> --database <new_warehouse_zzz_test> --schema <new_schema_zzz_test> --account myorganization-myaccount --user MyUserName
>    ```

Here is the output:

Copy code

```
Connecting...

Creating warehouse, database, schema...

Creating table test_table...

Selecting from test_table...
123, test string1
456, test string2

Closing connection...
```

Here is a longer example:

> Note
>
> In the section where you set your account and login information, make sure to replace the variables as needed to match your Snowflake login information (name, password, etc.).

This example uses the format() function to compose the statement. If your environment has a risk of SQL injection
attacks, you might prefer to bind values rather than use format().

Copy code

```
#!/usr/bin/env python
#
# Snowflake Connector for Python Sample Program
#

# Logging
import logging
logging.basicConfig(
    filename='/tmp/snowflake_python_connector.log',
    level=logging.INFO)

import snowflake.connector

# Set ACCOUNT to your account identifier.
# See https://docs.snowflake.com/en/user-guide/gen-conn-config.
ACCOUNT = '<my_organization>-<my_account>'
# Set your login information.
USER = '<login_name>'
PASSWORD = '<password>'

import os

# Only required if you copy data from your S3 bucket
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Connecting to Snowflake
con = snowflake.connector.connect(
  user=USER,
  password=PASSWORD,
  account=ACCOUNT,
)

# Creating a database, schema, and warehouse if none exists
con.cursor().execute("CREATE WAREHOUSE IF NOT EXISTS tiny_warehouse")
con.cursor().execute("CREATE DATABASE IF NOT EXISTS testdb")
con.cursor().execute("USE DATABASE testdb")
con.cursor().execute("CREATE SCHEMA IF NOT EXISTS testschema")

# Using the database, schema and warehouse
con.cursor().execute("USE WAREHOUSE tiny_warehouse")
con.cursor().execute("USE SCHEMA testdb.testschema")

# Creating a table and inserting data
con.cursor().execute(
    "CREATE OR REPLACE TABLE "
    "testtable(col1 integer, col2 string)")
con.cursor().execute(
    "INSERT INTO testtable(col1, col2) "
    "VALUES(123, 'test string1'),(456, 'test string2')")

# Copying data from internal stage (for testtable table)
con.cursor().execute("PUT file:///tmp/data0/file* @%testtable")
con.cursor().execute("COPY INTO testtable")

# Copying data from external stage (S3 bucket -
# replace <s3_bucket> with the name of your bucket)
con.cursor().execute("""
COPY INTO testtable FROM s3://<s3_bucket>/data/
     STORAGE_INTEGRATION = myint
     FILE_FORMAT=(field_delimiter=',')
""".format(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY))

# Querying data
cur = con.cursor()
try:
    cur.execute("SELECT col1, col2 FROM testtable")
    for (col1, col2) in cur:
        print('{0}, {1}'.format(col1, col2))
finally:
    cur.close()

# Binding data
con.cursor().execute(
    "INSERT INTO testtable(col1, col2) "
    "VALUES(%(col1)s, %(col2)s)", {
        'col1': 789,
        'col2': 'test string3',
        })

# Retrieving column names
cur = con.cursor()
cur.execute("SELECT * FROM testtable")
print(','.join([col[0] for col in cur.description]))

# Catching syntax errors
cur = con.cursor()
try:
    cur.execute("SELECT * FROM testtable")
except snowflake.connector.errors.ProgrammingError as e:
    # default error message
    print(e)
    # user error message
    print('Error {0} ({1}): {2} ({3})'.format(e.errno, e.sqlstate, e.msg, e.sfqid))
finally:
    cur.close()

# Retrieving the Snowflake query ID
cur = con.cursor()
cur.execute("SELECT * FROM testtable")
print(cur.sfqid)

# Closing the connection
con.close()
```
