# Choosing whether to write a stored procedure or a user-defined function

This topic describes key differences between stored procedures and UDFs, including differences in how each may be invoked and in what
they may do.

At a high level, stored procedures and UDFs differ in how they are typically used, as described below.

| Stored Procedure Purpose | User-Defined Function Purpose |
| --- | --- |
| Generally to perform administrative operations by executing SQL statements. The body of a stored procedure is allowed, but not required, to explicitly return a value (such as an error indicator). | Calculate and return a value. A function always returns a value explicitly by specifying an expression. For example, the body of a JavaScript UDF must have a `return` statement that returns a value. |

Expand

Show lessSee more

## When to create a stored procedure or a UDF

In general, when deciding whether to create a stored procedure or UDF, consider the following recommendations:

| Create a Stored Procedure When… | Create a UDF When… |
| --- | --- |
| - You’re migrating an existing stored procedure from another application/system. - You need to perform DDL or DML database operations:   - Administrative tasks, including DDL such as deleting temporary tables, deleting data older than `N` days, or adding users.   - DML statements (UPDATE statements, for example) | - You’re migrating an existing UDF from another application/system. - You need a function that can be called as part of a SQL statement and that must return a value that will be used in the statement. - Your output needs to include a value for every input row or every group. For example:   Copy code  ``` SELECT MyFunction(col1) FROM table1; ```   - You need to perform simple queries with SQL, such as SELECT statements. |

Expand

Show lessSee more

## Supported handler languages

When you write a procedure or UDF, you write its logic as a handler in one of the supported languages. The following table lists the
supported languages.

| Stored Procedures | User-Defined Functions |
| --- | --- |
| [Java](/developer-guide/stored-procedure/java/procedure-java-overview) | [Java](/developer-guide/udf/java/udf-java-introduction) |
| [JavaScript](/developer-guide/stored-procedure/stored-procedures-javascript) | [JavaScript](/developer-guide/udf/javascript/udf-javascript-introduction) |
| [Python](/developer-guide/stored-procedure/python/procedure-python-overview) | [Python](/developer-guide/udf/python/udf-python-introduction) |
| [Scala](/developer-guide/stored-procedure/scala/procedure-scala-overview) | [Scala](/developer-guide/udf/scala/udf-scala-introduction) |
| [Snowflake Scripting](/developer-guide/snowflake-scripting/index) | [SQL](/developer-guide/udf/sql/udf-sql-introduction) or [Snowflake Scripting](/developer-guide/snowflake-scripting/index) |

Expand

Show lessSee more

## Usage and behavior differences

The following sections describe specific differences in the behaviors supported by procedures and UDFs.

### UDFs return a value; stored procedures need not

- A UDF always returns a value explicitly by specifying an expression. A UDF’s purpose is to calculate and return a value.
  For example, the body of a JavaScript UDF must have a `return` statement that returns a value.
- A stored procedure is allowed, but not required, to explicitly return a value (such as an error indicator). The purpose of a stored
  procedure generally is to perform administrative operations by executing SQL statements. If a procedure does not explicitly return a
  value, then it implicitly returns NULL.

  Note that every CREATE PROCEDURE statement must include a RETURNS clause that specifies a return type, even if the procedure
  does not explicitly return anything. If a procedure does not explicitly return a value, then it implicitly returns NULL.

  Code in the following example declares a return type for the procedure with a RETURNS clause, but a value is only returned in the
  case of an error. In other words, not every code path returns a value.

  Copy code

  ```
  CREATE OR REPLACE PROCEDURE do_stuff(input NUMBER)
  RETURNS VARCHAR
  LANGUAGE SQL
  AS
  $$
  DECLARE
    ERROR VARCHAR DEFAULT 'Bad input. Number must be less than 10.';

  BEGIN
    IF (input > 10) THEN
   RETURN ERROR;
    END IF;

    -- Perform an operation that doesn't return a value.

  END;
  $$
  ;
  ```

### UDF return values are directly usable in SQL; stored procedure return values may not be

If you are not calling the stored procedure from a Snowflake Scripting block, you cannot use the value returned by a stored
procedure directly in SQL (unlike the value returned by a function). The syntax of the CALL command does not provide a place to
store the returned value or a way to operate on it or pass the value to another operation. In other words, the following statement
is not a valid SQL statement:

Copy code

```
y = stored_procedure1(x);                         -- Not allowed.
```

If you call a stored procedure within a [Snowflake Scripting block](/developer-guide/snowflake-scripting/blocks),
you can [capture the value returned by the stored procedure](/developer-guide/stored-procedure/stored-procedures-snowflake-scripting#label-stored-procedure-snowscript-call-sp-return-value)
in a [Snowflake Scripting variable](/developer-guide/snowflake-scripting/variables).

You can also indirectly use the return value of a stored procedure (outside of a Snowflake Scripting block), as described in the following
list:

- You can call the stored procedure inside another stored procedure. For example, when the stored procedure handler is written in JavaScript,
  the JavaScript in the outer stored procedure can retrieve and store the output of the inner stored procedure. Remember, however, that
  the outer stored procedure (and each inner stored procedure) is still unable to return more than one value to its caller.
- You can call a stored procedure that returns tabular data in the
  [FROM clause of a SELECT statement](/developer-guide/stored-procedure/stored-procedures-selecting-from).
- You can call the stored procedure and then call the [RESULT\_SCAN](/sql-reference/functions/result_scan) function and pass it
  the statement ID generated for the stored procedure.
- You can store a result set in a temporary table or permanent table, and use that table after returning from the
  stored procedure call.
- If the volume of data is not too large, you can store multiple rows and multiple columns in a VARIANT (for
  example, as a JSON value) and return that VARIANT.

### UDFs can be called in the context of another statement; stored procedures are called independently

- A UDF evaluates to a value and can be used in contexts in which a general expression can be used, such as the following:

  Copy code

  ```
  SELECT MyFunction_1(column_1) FROM table1;
  ```
- A stored procedure does not evaluate to a value, and cannot be used in all contexts in which a general expression can be used.
  For example, you cannot execute `SELECT my_stored_procedure()...`.

  You call a stored procedure as an independent statement, as in the following example:

  Copy code

  ```
  CALL MyStoredProcedure_1(argument_1);
  ```

For more details about calling functions and procedures, see the following:

- [Calling a stored procedure](/developer-guide/stored-procedure/stored-procedures-calling)
- [Executing a UDF](/developer-guide/udf/udf-calling-sql)

### Multiple UDFs may be called with one statement; a single stored procedure is called with one statement

- A single SQL statement can call multiple UDFs.
- A single SQL statement can call only one stored procedure.

  Similarly, a stored procedure, unlike a UDF, cannot be called as part of an expression. However, inside a stored procedure, the stored
  procedure can call another stored procedure, or call itself recursively. For example, see the code examples section
  [Examples](/developer-guide/stored-procedure/stored-procedures-javascript#label-stored-procedure-examples).

For more details about calling functions and procedures, see the following:

- [Calling a stored procedure](/developer-guide/stored-procedure/stored-procedures-calling)
- [Executing a UDF](/developer-guide/udf/udf-calling-sql)

### UDFs may access the database with simple queries only; stored procedures can execute DDL and DML statements

- In a UDF, you can use SQL to execute queries only (not DML or DDL statements).
- Within a stored procedure, you can execute database operations, such as SELECT, UPDATE, and CREATE:
  - For example, in a JavaScript stored procedure, you can use the JavaScript API to perform these operations.

    The example below shows how a stored procedure can create and execute a SQL statement that calls another stored
    procedure. The `$$` indicates the beginning and end of the JavaScript handler code in the stored procedure.

    Copy code

    ```
    CREATE PROCEDURE ...
      $$
      // Create a Statement object that can call a stored procedure named
      // MY_PROCEDURE().
      var stmt1 = snowflake.createStatement( { sqlText: "call MY_PROCEDURE(22)" } );
      // Execute the SQL command; in other words, call MY_PROCEDURE(22).
      stmt1.execute();
      // Create a Statement object that executes a SQL command that includes
      // a call to a UDF.
      var stmt2 = snowflake.createStatement( { sqlText: "select MY_UDF(column1) from table1" } );
      // Execute the SQL statement and store the output (the "result set") in
      // a variable named "rs", which we can access later.
      var rs = stmt2.execute();
      // etc.
      $$;
    ```
  - In a [Snowflake Scripting](/developer-guide/snowflake-scripting/index) stored procedure, you can execute SQL statements.

    The example below shows how a stored procedure can create and execute a SQL statement that calls another stored
    procedure. The `$$` indicates the beginning and end of the Snowflake Scripting code in the stored procedure.

    Copy code

    ```
    CREATE PROCEDURE ...
      -- Call a stored procedure named my_procedure().
      CALL my_procedure(22);
      -- Execute a SQL statement that includes a call to a UDF.
      SELECT my_udf(column1) FROM table1;
    ```
