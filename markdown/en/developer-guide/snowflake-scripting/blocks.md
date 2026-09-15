# Understanding blocks in Snowflake Scripting

In Snowflake Scripting, you write procedural code in a Snowflake Scripting block. This topic explains how to write procedural
code in a block.

## Understanding the structure of a block

A block has the following basic structure:

Copy code

```
DECLARE
  -- (variable declarations, cursor declarations, etc.) ...
BEGIN
  -- (Snowflake Scripting and SQL statements) ...
EXCEPTION
  -- (statements for handling exceptions) ...
END;
```

A block consists of required and optional sections that are delimited by keywords. Each section serves a different purpose:

- [DECLARE](/sql-reference/snowflake-scripting/declare): If you need to use any variables, cursors, RESULTSETs, or exceptions
  in the block, you can either declare these in the DECLARE section of the block or in the BEGIN … END section
  of the block.

  You can declare:

  - [Variables](/developer-guide/snowflake-scripting/variables)
  - [Cursors](/developer-guide/snowflake-scripting/cursors)
  - [RESULTSETs](/developer-guide/snowflake-scripting/resultsets)
  - [Exceptions](/developer-guide/snowflake-scripting/exceptions)

  This section of the block is optional.
- [BEGIN … END](/sql-reference/snowflake-scripting/begin): Write SQL statements and Snowflake Scripting constructs in the
  section of the block between BEGIN and END.
- [EXCEPTION](/sql-reference/snowflake-scripting/exception): If you need to add exception handling code, add this to the
  EXCEPTION section of the block.

  This section of the block is optional.

A simple block only requires the keywords BEGIN and END. For example:

Copy code

```
BEGIN
  CREATE TABLE employee (id INTEGER, ...);
  CREATE TABLE dependents (id INTEGER, ...);
END;
```

Important

The keyword BEGIN that starts a block is different from the keyword BEGIN that starts a transaction.
To minimize confusion, Snowflake strongly recommends starting transactions with BEGIN TRANSACTION (or the older form
BEGIN WORK), rather than BEGIN.

Any database objects that you create in a block (e.g. the tables in the example above) can be used outside of the block.

If the code uses variables, you can [declare those variables](/developer-guide/snowflake-scripting/variables#label-snowscript-declare-variable) in the block. One way to do
this is in the [DECLARE](/sql-reference/snowflake-scripting/declare) section of the block. For example:

Copy code

```
DECLARE
  radius_of_circle FLOAT;
  area_of_circle FLOAT;
BEGIN
  radius_of_circle := 3;
  area_of_circle := pi() * radius_of_circle * radius_of_circle;
  RETURN area_of_circle;
END;
```

This example declares a variable, uses the variable, and returns the value of the variable. For details on how values are
returned from a block, see [Returning a value](/developer-guide/snowflake-scripting/return).

These variables cannot be used outside of the block. See [Understanding the scope of declarations](/developer-guide/snowflake-scripting/variables#label-snowscript-scope).

You can also declare a variable in the BEGIN … END section of the block by using
[LET](/sql-reference/snowflake-scripting/let). For details, see [Declaring a variable](/developer-guide/snowflake-scripting/variables#label-snowscript-declare-variable).

## Using a block in a stored procedure

You can use a block in the definition of a stored procedure. The following is an example that you can run in
[Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) to create a stored procedure containing a Snowflake Scripting block:

Copy code

```
CREATE OR REPLACE PROCEDURE area()
RETURNS FLOAT
LANGUAGE SQL
AS
DECLARE
  radius FLOAT;
  area_of_circle FLOAT;
BEGIN
  radius := 3;
  area_of_circle := PI() * radius * radius;
  RETURN area_of_circle;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE area()
RETURNS FLOAT
LANGUAGE SQL
AS
$$
DECLARE
  radius FLOAT;
  area_of_circle FLOAT;
BEGIN
  radius := 3;
  area_of_circle := PI() * radius * radius;
  RETURN area_of_circle;
END;
$$
;
```

You can call a stored procedure using the [CALL](/sql-reference/sql/call) command. The following example calls
the stored procedure `area` in the previous example:

Copy code

```
CALL area();
```

The stored procedure returns the following output:

```
+--------------+
|         AREA |
|--------------|
| 28.274333882 |
+--------------+
```

For more information, see [Writing stored procedures in Snowflake Scripting](/developer-guide/stored-procedure/stored-procedures-snowflake-scripting).

## Using a block in a user-defined function (UDF)

You can use a block in the definition of a Snowflake Scripting UDF. The following example shows code that you can run in
[Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) to create a UDF that contains a Snowflake Scripting block:

Copy code

```
CREATE OR REPLACE FUNCTION area()
RETURNS FLOAT
LANGUAGE SQL
AS
DECLARE
  radius FLOAT;
  area_of_circle FLOAT;
BEGIN
  radius := 3;
  area_of_circle := PI() * radius * radius;
  RETURN area_of_circle;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE FUNCTION area()
RETURNS FLOAT
LANGUAGE SQL
AS
$$
DECLARE
  radius FLOAT;
  area_of_circle FLOAT;
BEGIN
  radius := 3;
  area_of_circle := PI() * radius * radius;
  RETURN area_of_circle;
END;
$$;
```

You can call the function in a SQL statement, such as a SELECT or INSERT statement. The following example calls
the Snowflake Scripting UDF `area` in the previous example in a SELECT statement:

Copy code

```
SELECT area();
```

```
+--------------+
|       AREA() |
|--------------|
| 28.274333882 |
+--------------+
```

For more information, see [Snowflake Scripting UDFs](/developer-guide/udf/sql/udf-sql-procedural-functions).

## Using an anonymous block

If you want to run procedural code outside of a stored procedure or UDF, you can define and use an *anonymous block*. An
anonymous block is a block that is not part of a stored procedure or UDF. You define the block as a separate, standalone SQL statement.

The [BEGIN](/sql-reference/snowflake-scripting/begin) statement that defines the block also executes the block. (You don’t
run a separate CALL command to execute the block.)

The following is an example of an anonymous block that you can run in
[Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in):

Copy code

```
DECLARE
  radius_of_circle FLOAT;
  area_of_circle FLOAT;
BEGIN
  radius_of_circle := 3;
  area_of_circle := PI() * radius_of_circle * radius_of_circle;
  RETURN area_of_circle;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  radius_of_circle FLOAT;
  area_of_circle FLOAT;
BEGIN
  radius_of_circle := 3;
  area_of_circle := PI() * radius_of_circle * radius_of_circle;
  RETURN area_of_circle;
END;
$$
;
```

The example produces the following output:

```
+-----------------+
| anonymous block |
|-----------------|
|    28.274333882 |
+-----------------+
```

The column header in the output is `anonymous block`. If the code had been executed in a stored procedure, the
column header would have been the name of the stored procedure.

The following example defines an anonymous block that creates two tables that are related. In this example, the block of
procedural code does not need to use variables, so the DECLARE section of the block is omitted.

Copy code

```
BEGIN
  CREATE TABLE parent (ID INTEGER);
  CREATE TABLE child (ID INTEGER, parent_ID INTEGER);
  RETURN 'Completed';
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
BEGIN
    CREATE TABLE parent (ID INTEGER);
    CREATE TABLE child (ID INTEGER, parent_ID INTEGER);
    RETURN 'Completed';
END;
$$
;
```

```
+-----------------+
| anonymous block |
|-----------------|
| Completed       |
+-----------------+
```
