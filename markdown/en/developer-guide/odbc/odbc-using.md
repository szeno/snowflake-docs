# Using the ODBC Driver

This topic provides information about how to use the ODBC driver.

## Compiling your code

### Linux

- If a C/C++ application is built with the Snowflake ODBC driver library and loads a non-pthread-compatible
  library, the application could crash due to unsafe concurrent access to shared memory. To prevent this,
  compile the application with the option which ensures that only pthread-compatible libraries are loaded
  with the application.

  For gcc/g++, the option is “-pthread”.

### macOS

- If a C/C++ application is built with the Snowflake ODBC driver library and loads a non-pthread-compatible
  library, the application could crash due to unsafe concurrent access to shared memory. To prevent this,
  compile the application with the option which ensures that only pthread-compatible libraries are loaded
  with the application.

  For clang/clang++, the option is “-pthread”.

## Executing a batch of SQL statements (multi-statement support)

Note

Executing multiple statements in a single query requires that a valid warehouse is available in a session.

In ODBC, you can send a batch of SQL statements (separated by semicolons) to execute in a single request. The following example sends a batch of three SELECT statements:

Copy code

```
// Sending a batch of SQL statements to be executed
rc = SQLExecDirect(hstmt,
      (SQLCHAR *) "select c1 from t1; select c2 from t2; select c3 from t3",
      SQL_NTS);
```

For more information about sending SQL statement batches, see
[Batches of SQL statements](https://docs.microsoft.com/en-us/sql/odbc/reference/develop-app/batches-of-sql-statements?view=sql-server-ver15).

To send a batch of statements with the Snowflake ODBC Driver, you must specify the number of statements in the batch. The Snowflake database requires the exact number of statements in order to guard against SQL injection attacks.

For more information about these types of attacks, see [SQL injection](https://en.wikipedia.org/wiki/SQL_injection).

The next section explains how to specify the number of statements in a batch.

### Specifying the number of statements in a batch

By default, the Snowflake database expects the driver to prepare and send a single statement for execution.

You can override this by specifying the number of statements in a batch for a given request or by enabling multiple statements for
the current session or account:

- To specify the number for a given request, call
  `SqlSetStmtAttr` to set the `SQL_SF_STMT_ATTR_MULTI_STATEMENT_COUNT` attribute to the number of statements in the batch.

  Copy code

  ```
  // Specify that you want to execute a batch of 3 SQL statements
  rc = SQLSetStmtAttr(hstmt, SQL_SF_STMT_ATTR_MULTI_STATEMENT_COUNT, (SQLPOINTER)3, 0);
  ```

  If you want to use the setting for the current session or account (rather than specify the number for the request), set
  `SQL_SF_STMT_ATTR_MULTI_STATEMENT_COUNT` to `-1`.

  For more information, see the [SqlSetStmtAttr](https://docs.microsoft.com/en-us/sql/odbc/reference/syntax/sqlsetstmtattr-function?view=sql-server-ver15) documentation.
- To enable multiple statements for the current session, account, or user, execute the appropriate ALTER command and set the Snowflake
  [MULTI\_STATEMENT\_COUNT](/sql-reference/parameters#label-parameters-multi-statement-count) parameter to `0` as shown in the following examples:

  > Copy code
  >
  > ```
  > alter session set MULTI_STATEMENT_COUNT = 0;
  > ```
  >
  > Copy code
  >
  > ```
  > alter account set MULTI_STATEMENT_COUNT = 0;
  > ```
  >
  > Copy code
  >
  > ```
  > alter user set MULTI_STATEMENT_COUNT = 0;
  > ```
  >
  > By default, `MULTI_STATEMENT_COUNT` is set to `1`, which indicates that only one SQL statement can be executed.
  >
  > Note
  >
  > Setting the `MULTI_STATEMENT_COUNT` parameter at the account level also affects other Snowflake connectors and drivers that use the account (e.g. [the Snowflake JDBC Driver](/developer-guide/jdbc/jdbc-using#label-jdbc-multistatement-support)).

### Preparing a batch of SQL statements

The ODBC Driver supports the ability to prepare a batch of SQL statements (e.g. by calling the `SQLPrepare` function). Note
the following:

- If the statements have parameters, calling the `SQLNumParams` function returns the total number of parameters in all the statements in the batch.

  For more information about parameters and the `SQLNumParams` function, see [Statement Parameters](https://docs.microsoft.com/en-us/sql/odbc/reference/develop-app/statement-parameters?view=sql-server-ver15) and [SQLNumParams Function](https://docs.microsoft.com/en-us/sql/odbc/reference/syntax/sqlnumparams-function?view=sql-server-ver15).
- Column information about the result set (e.g. data returned by `SQLNumResultCols`, `SQLDescribeCol`, `SQLColAttribute`, and
  `SQLColAttributes`) is available when you call `SQLExecute` or `SQLExecDirect`.

  Although some column information is available when you call SQLPrepare, the information might not be completely accurate, and
  subsequent calls to SQLExecute or SQLExecDirect might provide more accurate information.

### Limitations

GET and PUT commands are not supported in batches of SQL statements. When you send a batch of SQL statements with GET and PUT
comments to be executed, the GET and PUT commands are ignored, and no errors are reported.

## Binding parameters to array variables for batch inserts

In your application code, you can insert multiple rows in a single batch by [binding](/sql-reference/bind-variables)
parameters in an INSERT statement to array variables.

As an example, the following code inserts rows into a table that contains an INTEGER column and a VARCHAR column. The example
binds arrays to the parameters in the INSERT statement.

> Copy code
>
> ```
> SQLCHAR * Statement = "INSERT INTO t (c1, c2) VALUES (?, ?)";
>
> SQLSetStmtAttr(hstmt, SQL_ATTR_PARAM_BIND_TYPE, SQL_PARAM_BIND_BY_COLUMN, 0);
> SQLSetStmtAttr(hstmt, SQL_ATTR_PARAMSET_SIZE, ARRAY_SIZE, 0);
> SQLSetStmtAttr(hstmt, SQL_ATTR_PARAM_STATUS_PTR, ParamStatusArray, 0);
> SQLSetStmtAttr(hstmt, SQL_ATTR_PARAMS_PROCESSED_PTR, &ParamsProcessed, 0);
> SQLBindParameter(hstmt, 1, SQL_PARAM_INPUT, SQL_C_ULONG, SQL_INTEGER, 5, 0,
>                  IntValuesArray, 0, IntValuesIndArray);
> SQLBindParameter(hstmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR, STR_VALUE_LEN - 1, 0,
>                  StringValuesArray, STR_VALUE_LEN, StringValuesLenOrIndArray);
> ...
> SQLExecDirect(hstmt, Statement, SQL_NTS);
> ```

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
