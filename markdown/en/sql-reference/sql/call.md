# CALL

Calls a [stored procedure](/developer-guide/stored-procedure/stored-procedures-overview).

See also:
:   [CREATE PROCEDURE](/sql-reference/sql/create-procedure) , [SHOW PROCEDURES](/sql-reference/sql/show-procedures)

## Syntax

Copy code

```
CALL <procedure_name> ( [ [ <arg_name> => ] <arg> , ... ] )
  [ INTO :<snowflake_scripting_variable> ]
```

## Required parameters

`procedure_name ( [ [ arg_name => ] arg , ... ] )`
:   Specifies the identifier (`procedure_name`) for the procedure to call and any input arguments.

    You can either specify the input arguments by name (`arg_name => arg`) or by position (`arg`).

    Note

    - You must either specify all arguments by name or by position. You can’t specify some of the arguments by name and other
      arguments by position.
    - When you specify an argument by name, you can’t use double quotes around the argument name.
    - If two procedures have the same name but different argument types, you can use the argument names to specify
      which procedure to execute, if the argument names are different. For more information, see
      [Overloading procedures and functions](/developer-guide/udf-stored-procedure-naming-conventions#label-procedure-function-name-overloading).

## Optional parameters

`INTO :snowflake_scripting_variable`
:   Sets the specified [Snowflake Scripting variable](/developer-guide/snowflake-scripting/variables) to the return value of
    the stored procedure.

## Examples

For more extensive examples of creating and calling stored procedures, see [Working with stored procedures](/developer-guide/stored-procedure/stored-procedures-usage).

Copy code

```
CALL stproc1(5.14::FLOAT);
```

Each argument to a stored procedure can be a general expression:

Copy code

```
CALL stproc1(2 * 5.14::FLOAT);
```

An argument can be a subquery:

Copy code

```
CALL stproc1(SELECT COUNT(*) FROM stproc_test_table1);
```

You can call only one stored procedure per CALL statement. For example, the following statement fails:

Copy code

```
CALL proc1(1), proc2(2);                          -- Not allowed
```

Also, you cannot use a stored procedure CALL as part of an expression. For example, all the following statements fail:

Copy code

```
CALL proc1(1) + proc1(2);                         -- Not allowed
CALL proc1(1) + 1;                                -- Not allowed
CALL proc1(proc2(x));                             -- Not allowed
SELECT * FROM (call proc1(1));                    -- Not allowed
```

However, inside a stored procedure, the stored procedure can call
another stored procedure, or call itself recursively.

Caution

Nested calls can exceed the maximum allowed stack depth, so be careful when nesting calls,
especially when using recursion.

The following example calls a stored procedure named `sv_proc1` and passes in a string literal and number as input arguments.
The example specifies the arguments by position:

Copy code

```
CALL sv_proc1('Manitoba', 127.4);
```

You can also specify the arguments by their names:

Copy code

```
CALL sv_proc1(province => 'Manitoba', amount => 127.4);
```

The following example demonstrates how to set and pass a [session variable](/sql-reference/session-variables) as an input
argument to a stored procedure:

Copy code

```
SET Variable1 = 49;
CALL sv_proc2($Variable1);
```

The following is an example of a Snowflake Scripting block that captures the return value of a stored procedure in a Snowflake
Scripting variable.

Copy code

```
DECLARE
  ret1 NUMBER;
BEGIN
  CALL sv_proc1('Manitoba', 127.4) into :ret1;
  RETURN ret1;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  ret1 NUMBER;
BEGIN
  CALL sv_proc1('Manitoba', 127.4) into :ret1;
  RETURN ret1;
END;
$$
;
```
