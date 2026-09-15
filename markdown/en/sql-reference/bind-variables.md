# Bind variables

Applications can accept data from users and use that data in SQL statements. For
example, an application might ask a user to enter contact information, such as an
address and phone number.

To specify this user input in a SQL statement, you can programmatically construct
a string for the SQL statement by concatenating the user input with the other parts of the
statement. Alternatively, you can use *bind variables*. To use bind variables,
put one or more placeholders in the text of the SQL statement, then specify the
variable (the value to be used) for each placeholder.

## Overview of bind variables

With bind variables, you replace literals in SQL statements with placeholders. For
example, the following SQL statement uses literals for the inserted values:

Copy code

```
INSERT INTO t (c1, c2) VALUES (1, 'Test string');
```

The following SQL statement uses placeholders for the inserted values:

Copy code

```
INSERT INTO t (c1, c2) VALUES (?, ?);
```

Your application code binds data with each placeholder in the SQL statement. The
technique for binding data with a placeholder depends on the programming language.
The syntax of the placeholder also varies by programming language. It is either
`?`, `:varname`, or `%varname`.

## Use bind variables in JavaScript stored procedures

You can use [JavaScript](/developer-guide/stored-procedure/stored-procedures-javascript) to create
stored procedures that run SQL.

To specify bind variables in JavaScript code, use `?` placeholders. For example,
the following INSERT statement specifies bind variables for the values inserted into
a table row:

Copy code

```
INSERT INTO t (col1, col2) VALUES (?, ?)
```

In JavaScript code, you can use bind variables for the values in most SQL statements.
For information about limitations, see [Limitations for bind variables](#label-bind-variables-limitations).

For more information about using bind variables in JavaScript, see
[Binding variables](/developer-guide/stored-procedure/stored-procedures-javascript#label-stored-procedures-binding-variables).

## Use bind variables with Snowflake Scripting

You can use [Snowflake Scripting](/developer-guide/snowflake-scripting/index) to create procedural code
that runs SQL, such as code blocks and stored procedures. To specify bind variables in Snowflake Scripting
code, prefix the variable name with a colon. For example, the following INSERT statement specifies a bind variable
named `variable1`:

Copy code

```
INSERT INTO t (c1) VALUES (:variable1)
```

When you run SQL in an [EXECUTE IMMEDIATE](/sql-reference/sql/execute-immediate) command or an
[OPEN command for a cursor](/developer-guide/snowflake-scripting/cursors#label-snowscript-cursors-open), you can bind variables with the USING clause.

This example binds variables in an EXECUTE IMMEDIATE command with a USING clause:

Copy code

```
EXECUTE IMMEDIATE :query USING (minimum_price, maximum_price);
```

For the full example that includes this code, see
[Executing a statement that contains bind variables](/sql-reference/sql/execute-immediate#label-execute-immediate-example-snowflake-scripting-bind-variables).

When you declare a cursor, you can specify bind parameters (`?` characters) in a SELECT statement. You can then
bind these parameters to variables in the USING clause when you open the cursor.

The following example declares a cursor and specifies bind parameters, then opens the cursor with the USING clause:

Copy code

```
LET c1 CURSOR FOR SELECT id FROM invoices WHERE price > ? AND price < ?;
OPEN c1 USING (minimum_price, maximum_price);
```

Snowflake Scripting also supports numbering bind variables by position and reusing a bind variable in a SQL statement.
For numbered bind variables, each variable declaration is assigned an index, and you can refer to the nth declared
variable with `:n`. For example, the following Snowflake Scripting block specifies bind variable `:1` for
the `i` variable and `:2` for the `v` variable, and it reuses the `:1` bind variable in a SQL statement:

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  i INTEGER DEFAULT 1;
  v VARCHAR DEFAULT 'SnowFlake';
  r RESULTSET;
BEGIN
  CREATE OR REPLACE TABLE snowflake_scripting_bind_demo (id INTEGER, value VARCHAR);
  EXECUTE IMMEDIATE 'INSERT INTO snowflake_scripting_bind_demo (id, value)
    SELECT :1, (:2 || :1)' USING (i, v);
  r := (SELECT * FROM snowflake_scripting_bind_demo);
  RETURN TABLE(r);
END;
$$
;
```

```
+----+------------+
| ID | VALUE      |
|----+------------|
|  1 | SnowFlake1 |
+----+------------+
```

In Snowflake Scripting code, you can use bind variables for the values in most SQL statements.
For information about limitations, see [Limitations for bind variables](#label-bind-variables-limitations).

For more information about using bind variables in Snowflake Scripting, see
[Using a variable in a SQL statement (binding)](/developer-guide/snowflake-scripting/variables#label-snowscript-variables-binding) and [Using an argument in a SQL statement (binding)](/developer-guide/stored-procedure/stored-procedures-snowflake-scripting#label-stored-procedure-snowscript-arguments-binding).

## Use bind variables with the SQL API

You can use the [Snowflake SQL API](/developer-guide/sql-api/index) to access and update data in a Snowflake
database. You can create applications that use the SQL API to submit SQL statements and manage
deployments.

When you submit a request that runs a SQL statement, you can use bind variables for values
in the statement. For more information, see [Using bind variables in a statement](/developer-guide/sql-api/submitting-requests#label-sql-api-bind-variables).

## Use bind variables with drivers

Using Snowflake [drivers](/developer-guide/drivers), you can write applications that
perform operations on Snowflake. The drivers support programming languages such as Go, Java,
and Python. For information about using bind variables in an application for a specific driver,
follow the link for the driver:

- [Go](https://pkg.go.dev/github.com/snowflakedb/gosnowflake#hdr-Binding_Parameters)
- [JDBC](/developer-guide/jdbc/jdbc-using#label-jdbc-binding)
- [.NET](https://github.com/snowflakedb/snowflake-connector-net/blob/master/doc/QueryingData.md#bind-parameter)
- [Node.js](/developer-guide/node-js/nodejs-driver-execute#label-nodejs-binding)
- [ODBC](/developer-guide/odbc/odbc-using#label-odbc-using-binding-parameters)
- [Python](/developer-guide/python-connector/python-connector-example#label-python-connector-binding-data)

Note

The PHP driver does not support bind variables.

## Use bind variables with arrays of values

You can bind an array of values to variables in SQL statements. Using this technique, you
can improve performance by inserting multiple rows in a single batch, which avoids network
round trips and compilations. The use of an array bind is also called a “bulk insert” or
“batch insert.”

Note

Snowflake supports other data loading methods that are recommended instead of using array binds.
For more information, see [Load data into Snowflake](/guides-overview-loading-data) and
[Data loading and unloading commands](/sql-reference/commands-data-loading).

The following is an example of an array bind in Python code:

Copy code

```
conn = snowflake.connector.connect( ... )
rows_to_insert = [('milk', 2), ('apple', 3), ('egg', 2)]
conn.cursor().executemany(
            "insert into grocery (item, quantity) values (?, ?)",
            rows_to_insert)
```

This example specifies the following bind list: `[('milk', 2), ('apple', 3), ('egg', 2)]`.
The way an application specifies a bind list depends on the programming language.

This code inserts three rows into the table:

```
+-------+----+
| C1    | C2 |
|-------+----|
| milk  |  2 |
| apple |  3 |
| egg   |  2 |
+-------+----+
```

For information about using array binds in an application for a specific driver,
follow the link for the driver:

- [Go](https://pkg.go.dev/github.com/snowflakedb/gosnowflake#hdr-Batch_Inserts_and_Binding_Parameters)
- [JDBC](/developer-guide/jdbc/jdbc-using#label-jdbc-batch-updates)
- [.NET](https://github.com/snowflakedb/snowflake-connector-net/blob/master/doc/QueryingData.md#bind-array-variables)
- [Node.js](/developer-guide/node-js/nodejs-driver-execute#label-nodejs-array-binding)
- [ODBC](/developer-guide/odbc/odbc-using#label-odbc-using-binding-parameters)
- [Python](/developer-guide/python-connector/python-connector-example#label-python-connector-binding-batch-inserts)

Note

The PHP driver doesn’t support array binds.

### Limitations of using array binds

The following limitations apply to array binds:

- Only INSERT INTO … VALUES statements can contain array bind variables.
- The VALUES clause must be a single-row list of bind variables. For example, the following
  VALUES clause is not allowed:

  Copy code

  ```
  VALUES (?,?), (?,?)
  ```

### Insert multiple rows without using array binds

An INSERT statement might use bind variables to insert multiple rows without using
an array bind. The following example inserts values into two rows, but it doesn’t use an array bind.

Copy code

```
INSERT INTO t VALUES (?,?), (?,?);
```

For example, your application can specify a bind list that’s equivalent to the following values, in order,
for the placeholders: `[1,'String1',2,'String2']`. Because the VALUES clause specifies more
than one row, the statement only inserts the exact number of values (four in the example), rather
than a dynamic number of rows.

## Use bind variables with semi-structured data

To bind variables with semi-structured data, bind the variable as a string type, and use functions
such as [PARSE\_JSON](/sql-reference/functions/parse_json) or [ARRAY\_CONSTRUCT](/sql-reference/functions/array_construct).

The following example creates a table with one [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) column and then calls
the PARSE\_JSON function to insert semi-structured data into the table with a bind variable:

Copy code

```
CREATE TABLE t (a VARIANT);
-- Code that supplies a bind value for ? of '{'a': 'abc', 'x': 'xyz'}'
INSERT INTO t SELECT PARSE_JSON(a) FROM VALUES (?);
```

The following example queries the table:

Copy code

```
SELECT * FROM t;
```

The query returns the following output:

```
+---------------+
| A             |
|---------------|
| {             |
|   "a": "abc", |
|   "x": "xyz"  |
| }             |
+---------------+
```

The following statement calls the ARRAY\_CONSTRUCT function to insert an array of semi-structured
data into a VARIANT column with a bind variable:

Copy code

```
INSERT INTO t SELECT ARRAY_CONSTRUCT(column1) FROM VALUES (?);
```

Both of these examples can insert a single row, or they can use an array bind to insert multiple rows
in one batch. You can use this technique to insert any type of semi-structured data that is valid in a
VARIANT column.

## Retrieve bind variable values

To retrieve the values of bind variables in a query that has been executed, you can use the
[BIND\_VALUES](/sql-reference/functions/bind_values) table function in the INFORMATION\_SCHEMA schema.
With this function, you can retrieve bind variable values from any code that supports bind variables,
including JavaScript and Snowflake Scripting code.

You can also access these bind variable values from the `bind_values` column in the output for
the [QUERY\_HISTORY Account Usage view](/sql-reference/account-usage/query_history),
the [QUERY\_HISTORY Organization Usage view](/sql-reference/organization-usage/query_history),
or the [QUERY\_HISTORY function](/sql-reference/functions/query_history).

To prevent bind values from being accessible to users, set the [ALLOW\_BIND\_VALUES\_ACCESS](/sql-reference/parameters#label-allow-bind-values-access)
account-level parameter to `FALSE`.

You might want to retrieve bind variable values for the following cases:

- **Troubleshooting queries** - When you know the exact bind values used in queries, it’s easier to optimize
  the queries and debug the following types of issues:

  - A query fails to run.
  - A query’s performance is poor.
  - A query isn’t using caches or expected execution plans.
- **Recreating queries for testing** - Developers and DBAs can recreate user-generated queries with bind variable
  values to replicate problems and for stress testing.
- **Auditing and compliance** - For security and compliance purposes, organizations must audit the data that users
  are accessing. They can use bind variable values to determine the exact data retrieved by users.

### Examples that retrieve bind variable values

The following queries return the bind variable values for a previous query:

Copy code

```
SELECT * FROM TABLE(
  INFORMATION_SCHEMA.BIND_VALUES('<query_id_value>'));
```

Copy code

```
SELECT bind_values
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
  WHERE query_id = '<query_id_value>';
```

Replace `query_id_value` with the query ID. You can use the [LAST\_QUERY\_ID](/sql-reference/functions/last_query_id)
function to return the ID of a previous query.

Note

The latency for the QUERY\_HISTORY view might be up to 45 minutes.

The following examples use the BIND\_VALUES function:

- [Snowflake Scripting example that retrieves named bind variables](#label-retrieving-bind-variable-values-example-snowflake-scripting-named)
- [Python Connector example that retrieves positional bind variables](#label-retrieving-bind-variable-values-example-python-connector-positional)

#### Snowflake Scripting example that retrieves named bind variables

Run the following Snowflake Scripting anonymous block, which includes a statement that uses bind variables:

Copy code

```
DECLARE
  name STRING;
  temperature FLOAT;
  res RESULTSET;
BEGIN
  name := 'Snowman';
  temperature := -20.14;
  res := (
    SELECT
      CONCAT('Hello ', :NAME, '!') as greeting,
      CONCAT('It is ', :TEMPERATURE, 'deg C today.') as weather
  );
  RETURN LAST_QUERY_ID();
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE
$$
DECLARE
  name STRING;
  temperature FLOAT;
  res RESULTSET;
BEGIN
  name := 'Snowman';
  temperature := -20.14;
  res := (
    SELECT
      CONCAT('Hello ', :NAME, '!') as greeting,
      CONCAT('It is ', :TEMPERATURE, 'deg C today.') as weather
  );
  RETURN LAST_QUERY_ID();
END;
$$
;
```

The block returns the query ID of the statement that uses bind variables.

Note

Your statement will return a different query ID than the one shown here.

```
+--------------------------------------+
| anonymous block                      |
|--------------------------------------|
| 01bbe3d6-0109-0863-0000-a99502ffa062 |
+--------------------------------------+
```

To retrieve the bind variables used in the anonymous block, run the following query. Replace
`01bbe3d6-0109-0863-0000-a99502ffa062` with the query ID in your output after running the
anonymous block.

Copy code

```
SELECT * FROM TABLE(
  INFORMATION_SCHEMA.BIND_VALUES('01bbe3d6-0109-0863-0000-a99502ffa062'));
```

```
+--------------------------------------+----------+-------------+------+---------+
| QUERY_ID                             | POSITION | NAME        | TYPE | VALUE   |
|--------------------------------------+----------+-------------+------+---------|
| 01bbe3d6-0109-0863-0000-a99502ffa062 |     NULL | TEMPERATURE | REAL | -20.14  |
| 01bbe3d6-0109-0863-0000-a99502ffa062 |     NULL | NAME        | TEXT | Snowman |
+--------------------------------------+----------+-------------+------+---------+
```

#### Python Connector example that retrieves positional bind variables

The following Python Connector code uses the BIND\_VALUES function to display the values of the
positional bind variables in the output:

Copy code

```
cursor = conn.cursor()
print(cursor.execute(
          """
          SELECT
              CONCAT('Hello ', ?, '!') as greeting,
              CONCAT('It is ', ?, 'deg C today.') as weather
          """,
          params=["Snowman", -20.14],
      ).fetch_pandas_all())

query_id = cursor.sfqid
print(f"Bind values for query {query_id} are:")
print(cursor.execute("SELECT * FROM TABLE(INFORMATION_SCHEMA.BIND_VALUES(?))", params=[query_id]).fetch_pandas_all())
```

```
        GREETING                   WEATHER
0  Hello Snowman!  It is -20.14deg C today.

Bind values for query 01bbe918-0200-0001-0000-000000101145 are:

                               QUERY_ID POSITION  NAME  TYPE    VALUE
0  01bbe918-0200-0001-0000-000000101145        1  None  TEXT  Snowman
1  01bbe918-0200-0001-0000-000000101145        2  None  REAL   -20.14
```

## Limitations for bind variables

The following limitations apply to bind variables:

- Limitations for SELECT statements:

  - Bind variables can’t replace numbers that are part of a data type definition (for example,
    `NUMBER(?)`) or [collation specification](/sql-reference/collation#label-collation-specification) (for example,
    `COLLATE ?`).
  - Bind variables can’t be used for the source in a SELECT statement that queries files on a stage.
- Limitations for DDL commands:

  - Bind variables can’t be used in the following DDL commands:

    - CREATE/ALTER INTEGRATION
    - CREATE/ALTER REPLICATION GROUP
    - CREATE/ALTER PIPE
    - CREATE TABLE … USING TEMPLATE
  - Bind variables can’t be used in the following clauses:

    - ALTER COLUMN
    - COMMENT ON CONSTRAINT
  - In CREATE/ALTER commands, bind variables can’t be used for the values of the following parameters:

    - CREDENTIALS
    - DIRECTORY
    - ENCRYPTION
    - IMPORTS
    - PACKAGES
    - REFRESH
    - TAG
    - Parameters that are specific to external tables
  - Bind variables can’t be used for properties that are part of a [FILE FORMAT](/sql-reference/sql/create-file-format)
    value.
- In COPY INTO commands, bind variables can’t be used for the values of the following parameters:

  - CREDENTIALS
  - ENCRYPTION
  - FILE\_FORMAT
- In SHOW commands, bind variables can’t be used in the STARTS WITH parameter.
- Bind variables can’t be used in an EXECUTE IMMEDIATE FROM command.
- Bind variable values can’t be converted automatically from one data type to another when bind variables are used in:

  - Snowflake Scripting code that specifies the data type explicitly
  - DDL statements
  - Stage names

## Security considerations for bind variables

Bind variables don’t mask sensitive data in all cases. For example, the values of bind variables might appear
in error messages and other artifacts.

Bind variables can help to prevent SQL injection attacks when you construct SQL statements with user input. However,
bind variables can present potential security risks. If inputs to SQL statements come from external sources, make sure
they are validated. For more information, see [SQL injection](/developer-guide/stored-procedure/stored-procedures-usage#label-sql-injection).
