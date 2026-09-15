# RETURN (Snowflake Scripting)

Returns the value of a specified expression.

For more information about returning values, see [Returning a value](/developer-guide/snowflake-scripting/return).

Note

This [Snowflake Scripting](/developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](/developer-guide/snowflake-scripting/blocks).

## Syntax

Copy code

```
RETURN <expression>;
```

Where:

> `expression`
> :   An expression that evaluates to the value to return.

## Usage notes

- A RETURN statement can be run in:

  - A block in a [stored procedure](/developer-guide/stored-procedure/stored-procedures-overview) or
    [Snowflake Scripting user-defined function (UDF)](/developer-guide/udf/sql/udf-sql-procedural-functions).
  - An [anonymous block](/developer-guide/snowflake-scripting/blocks#label-snowscript-block-anonymous).
- A RETURN statement returns one of the following types:

  - A [SQL data type](/sql-reference-data-types)

  - A table. Use `TABLE(...)` in the `RETURN` statement.

    If your block is in a stored procedure, you must also specify the `RETURNS TABLE...` clause in the
    [CREATE PROCEDURE](/sql-reference/sql/create-procedure) statement.

    Note

    Currently, in the `RETURNS TABLE(...)` clause, you can’t specify GEOGRAPHY as a column type. This
    applies whether you are creating a stored or anonymous procedure.

    Copy code

    ```
    CREATE OR REPLACE PROCEDURE test_return_geography_table_1()
      RETURNS TABLE(g GEOGRAPHY)
      ...
    ```

    Copy code

    ```
    WITH test_return_geography_table_1() AS PROCEDURE
      RETURNS TABLE(g GEOGRAPHY)
      ...
    CALL test_return_geography_table_1();
    ```

    If you attempt to specify GEOGRAPHY as a column type, calling the stored procedure results in the error:

    Copy code

    ```
    Stored procedure execution error: data type of returned table does not match expected returned table type
    ```

    To work around this issue, you can omit the column arguments and types in `RETURNS TABLE()`.

    Copy code

    ```
    CREATE OR REPLACE PROCEDURE test_return_geography_table_1()
      RETURNS TABLE()
      ...
    ```

    Copy code

    ```
    WITH test_return_geography_table_1() AS PROCEDURE
      RETURNS TABLE()
      ...
    CALL test_return_geography_table_1();
    ```

    If you want to return the data that a RESULTSET points to, pass the RESULTSET to TABLE(…), as shown in the example below:

    Copy code

    ```
    CREATE PROCEDURE ...
    RETURNS TABLE(...)
    ...
        RETURN TABLE(my_result_set);
    ...
    ```

    See [Returning a RESULTSET as a table](/developer-guide/snowflake-scripting/resultsets#label-snowscript-resultsets-use-return-table).
- You can set a variable to the return value of a stored procedure. For more information, see
  [Using the value returned from a stored procedure call](/developer-guide/stored-procedure/stored-procedures-snowflake-scripting#label-stored-procedure-snowscript-call-sp-return-value).

## Examples

This example declares a variable named `my_var` for use in a Snowflake Scripting anonymous block and
then returns the value of the variable:

Copy code

```
DECLARE
  my_var VARCHAR;
BEGIN
  my_var := 'Snowflake';
  RETURN my_var;
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
  my_var VARCHAR;
BEGIN
  my_var := 'Snowflake';
  RETURN my_var;
END;
$$;
```
