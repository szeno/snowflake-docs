# Snowflake Scripting Developer Guide

Snowflake Scripting is an extension to Snowflake SQL that adds support for procedural logic. You can use Snowflake
Scripting syntax in [stored procedures](/developer-guide/stored-procedure/stored-procedures-overview) and
[user-defined functions (UDFs)](/developer-guide/udf/sql/udf-sql-procedural-functions). You can also use Snowflake
Scripting syntax outside of stored procedures and UDFs and stored procedures. The next topics explain how to use
Snowflake Scripting.

[Understanding blocks in Snowflake Scripting](/developer-guide/snowflake-scripting/blocks)
:   Learn the basic structure of Snowflake Scripting code.

[Working with variables](/developer-guide/snowflake-scripting/variables)
:   Declare and use variables.

[Returning a value](/developer-guide/snowflake-scripting/return)
:   Return values from stored procedures and an anonymous block.

[Working with conditional logic](/developer-guide/snowflake-scripting/branch)
:   Control flow with IF and CASE statements.

[Working with loops](/developer-guide/snowflake-scripting/loops)
:   Control flow with FOR, WHILE, REPEAT, and LOOP.

[Working with cursors](/developer-guide/snowflake-scripting/cursors)
:   Iterate through query results with a cursor.

[Working with RESULTSETs](/developer-guide/snowflake-scripting/resultsets)
:   Iterate over the result set returned by a query.

[Handling exceptions](/developer-guide/snowflake-scripting/exceptions)
:   Handle errors by handling and raising exceptions.

[Determining the number of rows affected by SQL statements](/developer-guide/snowflake-scripting/dml-status)
:   Use global variables to determine the effect of data manipulation language (DML) commands.

[Getting the query ID of the last query](/developer-guide/snowflake-scripting/query-id)
:   Use the global variable SQLID to get the query ID of the last query.

[Examples for common use cases of Snowflake Scripting](/developer-guide/snowflake-scripting/use-cases)
:   Explore examples of Snowflake Scripting code for some common use cases.

[Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)
:   Run the Snowflake Scripting examples in SnowSQL, Snowsight and Python Connector code.
