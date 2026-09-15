# RAISE (Snowflake Scripting)

Raises an exception.

For more information about exceptions, see [Handling exceptions](/developer-guide/snowflake-scripting/exceptions).

Note

This [Snowflake Scripting](/developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](/developer-guide/snowflake-scripting/blocks).

See also:
:   [EXCEPTION](/sql-reference/snowflake-scripting/exception)

## Syntax

Copy code

```
RAISE <exception_name> ;
```

Where:

> `exception_name`
> :   The name of the exception to raise.
>
>     If you are handling an exception in an exception handler and you want to raise the same exception again, omit this
>     argument. See [Raising the same exception again in an exception handler in Snowflake Scripting](/developer-guide/snowflake-scripting/exceptions#label-snowscript-exception-raising-same-handled).

## Examples

This creates and raises (but does not catch) a simple exception:

Copy code

```
CREATE PROCEDURE thrower()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
    DECLARE
        MY_EXCEPTION EXCEPTION;
    BEGIN
        RAISE MY_EXCEPTION;
    END;
$$
;
```

Here is the call to the stored procedure that raises the exception:

Copy code

```
CALL thrower();
```

Here is the output of executing the stored procedure that raises the exception:

```
-20000 (P0001): Uncaught exception of type 'MY_EXCEPTION' on line 5 at position 8
```

The next example is similar to the preceding example, but uses an exception for which the user defined a custom
exception number and exception message:

Copy code

```
DECLARE
        MY_EXCEPTION EXCEPTION (-20002, 'Raised MY_EXCEPTION.');
```

Here is the output of executing the stored procedure that raises the exception:

```
-20002 (P0001): Uncaught exception of type 'MY_EXCEPTION' on line 7 at position 8 : Raised MY_EXCEPTION.
```

For more examples, see the examples for
[handling an exception](/sql-reference/snowflake-scripting/exception#label-snowscript-introduction-exceptions-handling-an-exception-examples).
