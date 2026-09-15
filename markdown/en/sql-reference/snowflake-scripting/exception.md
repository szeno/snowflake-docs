# EXCEPTION (Snowflake Scripting)

Specifies how to handle exceptions raised in the Snowflake Scripting block.

For more information on exceptions, see [Handling exceptions](/developer-guide/snowflake-scripting/exceptions).

See also:
:   [RAISE](/sql-reference/snowflake-scripting/raise)

## Syntax

Copy code

```
EXCEPTION
    WHEN <exception_name> [ OR <exception_name> ... ] [ { EXIT | CONTINUE } ] THEN
        <statement>;
        [ <statement>; ... ]
    [ WHEN ... ]
    [ WHEN OTHER [ { EXIT | CONTINUE } ] THEN ]
        <statement>;
        [ <statement>; ... ]
```

Where:

> `exception_name`
> :   An exception name defined in the
>     [DECLARE portion of the current block](/developer-guide/snowflake-scripting/variables),
>     or in an enclosing block.
>
> `statement`
> :   A statement can be any of the following:
>
>     - A single SQL statement (including CALL).
>     - A control-flow statement (for example, a [looping](/developer-guide/snowflake-scripting/loops) or
>       [branching](/developer-guide/snowflake-scripting/branch) statement).
>     - A nested [block](/developer-guide/snowflake-scripting/blocks).

## Usage notes

- Each [block](/developer-guide/snowflake-scripting/blocks) can have its own exception handler.
- Snowflake supports no more than one exception handler per block. However, that handler can catch more than one type
  of exception by having more than one `WHEN` clause.
- The `WHEN OTHER [ { EXIT | CONTINUE } ] THEN` clause catches any exception not yet specified.
- An exception handler applies to statements between the BEGIN and EXCEPTION sections of the block in which
  it is declared. It does’t apply to the DECLARE section of the block.
- An exception handler can handle a specified exception only if that specified exception is in
  [scope](/developer-guide/snowflake-scripting/variables#label-snowscript-scope).
- If a stored procedure is intended to return a value, then it should return a value from each possible exit path,
  including each `WHEN` clause of `EXIT` type in the exception handler.
- To use a variable in an exception handler, the variable must be declared in the
  [DECLARE](/sql-reference/snowflake-scripting/declare) section or passed as an argument to a
  stored procedure. It can’t be declared in the [BEGIN … END](/sql-reference/snowflake-scripting/begin)
  section. For more information, see [Passing variables to an exception handler in Snowflake Scripting](/developer-guide/snowflake-scripting/exceptions#label-snowscript-exception-raising-variables).
- When an exception occurs, the handler conditions are checked in order and the first `WHEN` clause that
  matches is used. The order within a block is top to bottom, and the inner blocks are checked before the outer
  blocks. There is no preference in matching `EXIT` or `CONTINUE` handlers, whichever matches first is used.
- Only one handler can be matched for a statement. However, any exceptions encountered inside of an exception
  handler body can trigger outer block exception handlers.
- Each `WHEN` clause in an exception handler can be one of the following types:

  - `EXIT` - The block runs the statements in the handler and then exits the current block. If the block runs an
    exception of this type, and the block contains statements after the exception handler, those statements
    aren’t run.

    If the block is an inner block, and the exception handler doesn’t contain a `RETURN` statement, then
    execution exits the inner block and continues with the code in the outer block.

    `EXIT` is the default.
  - `CONTINUE` - The block executes the statements in the handler and continues with the statement
    immediately following the one that caused the error.

  An `EXCEPTION` clause can have `WHEN` clauses of both types — `EXIT` and `CONTINUE`.

  For a `WHEN` clause of the `CONTINUE` type, the following usage notes apply:

  - If an error is raised in a [branching construct](/developer-guide/snowflake-scripting/branch),
    then the continuing statement is the statement immediately after the branching construct.
  - If an error is raised in the condition of a [loop](/developer-guide/snowflake-scripting/loops), then
    the continuing statement is the statement immediately after the loop.
  - If an error is raised in the body of a loop, then the continuing statement is the statement in the next iteration
    of the loop. For an example, see [Handle an exception and continue](#label-snowscript-exception-handling-example-continue).
  - If an error is raised in a [RETURN](/sql-reference/snowflake-scripting/return) statement, then the
    continuing statement is the statement immediately after the `RETURN` statement.
  - If an error is raised in a
    [nested stored procedure](/developer-guide/stored-procedure/stored-procedures-snowflake-scripting#label-stored-procedure-snowscript-nested-stored-procedures) and the error
    is handled by the outer scope, then the continuing statement is the statement immediately after the stored
    procedure call.
  - Avoid including a `RETURN` statement in a `WHEN` clause of the `CONTINUE` type. If you include a
    `RETURN` statement, then the stored procedure returns without continuing.

  For a `WHEN` clause of the `CONTINUE` type, the following examples show which statement is the statement
  immediately following the one that caused the error for different scenarios. In these examples, the
  `error_expression` is the expression that raised the exception, and the `continue_statement` is the
  statement that the code continues with in the block after the `CONTINUE` handler statements.

  Copy code

  ```
  DECLARE
    ...
  BEGIN
    ...
    LET a := <error_expression>;
    <continue_statement>;
    ...
  EXCEPTION
    WHEN <exception_name> CONTINUE THEN
   ...
  END;
  ```

  Copy code

  ```
  LET x := <valid_expression>;
  x := <error_expression>;
  <continue_statement>
  ```

  Copy code

  ```
  SELECT <statement> INTO <error_expression>;
  <continue_statement>;
  ```

  Copy code

  ```
  IF (<error_expression>) THEN
    <statement>
  ELSEIF (<valid_expression>) THEN
    <statement>
  ELSE
    <statement>
  END IF;
  <continue_statement>;
  ```

  Copy code

  ```
  CASE (<error_expression>)
    WHEN (<valid_expression>) THEN
   <statement>
    ELSE
   <statement>
  END CASE;
  <continue_statement>
  ```

  Copy code

  ```
  CASE (<valid_expression>)
    WHEN (<error_expression>) THEN
   <statement>
    WHEN (<valid_expression>) THEN
   <statement>
    ELSE
   <statement>
  END CASE;
  <continue_statement>
  ```

  Copy code

  ```
  FOR i IN <valid_expression> TO <error_expression> DO
    <statement>
  END FOR
  <continue_statement>
  ```

  Copy code

  ```
  WHILE <error_expression> DO
    <statement>
  END WHILE;
  <continue_statement>
  ```

  Copy code

  ```
  REPEAT
    <statement>
  UNTIL <error_expression>;
  <continue_statement>
  ```

  Copy code

  ```
  RETURN <error_expression>;
  <continue_statement>
  ```

  Copy code

  ```
  DECLARE
    x int := 0;
    myproc PROCEDURE()
   RETURNS STRING
   AS BEGIN
     x := <error_expression>;
     <statement>
   END;
  BEGIN
    CALL myproc();
    <continue_statement>
    ...
  END;
  ```

## Examples

The following examples declare and raise an exceptions, and handle the exceptions
with exception handlers:

- [Handle exceptions of more than one type](#label-snowscript-exception-handling-example-more-than-one-type)
- [Handle an exception and continue](#label-snowscript-exception-handling-example-continue)
- [Handle exceptions in nested blocks](#label-snowscript-exception-handling-example-nested)
- [Handle multiple exceptions in the same clause and unspecified exceptions](#label-snowscript-exception-handling-example-or-other)
- [Handle exceptions by using built-in variables](#label-snowscript-exception-handling-example-built-in-variables)

### Handle exceptions of more than one type

The following example shows an exception handler that is designed to handle more than one type of exception:

Copy code

```
DECLARE
  result VARCHAR;
  exception_1 EXCEPTION (-20001, 'I caught the expected exception.');
  exception_2 EXCEPTION (-20002, 'Not the expected exception!');
BEGIN
  result := 'If you see this, I did not catch any exception.';
  IF (TRUE) THEN
    RAISE exception_1;
  END IF;
  RETURN result;
EXCEPTION
  WHEN exception_2 THEN
    RETURN SQLERRM;
  WHEN exception_1 THEN
    RETURN SQLERRM;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  result VARCHAR;
  exception_1 EXCEPTION (-20001, 'I caught the expected exception.');
  exception_2 EXCEPTION (-20002, 'Not the expected exception!');
BEGIN
  result := 'If you see this, I did not catch any exception.';
  IF (TRUE) THEN
    RAISE exception_1;
  END IF;
  RETURN result;
EXCEPTION
  WHEN exception_2 THEN
    RETURN SQLERRM;
  WHEN exception_1 THEN
    RETURN SQLERRM;
END;
$$;
```

The output shows that the exception handler caught the exception:

```
+----------------------------------+
| anonymous block                  |
|----------------------------------|
| I caught the expected exception. |
+----------------------------------+
```

### Handle an exception and continue

The following example shows an exception handler with a `WHEN` clause of the `CONTINUE` type:

Copy code

```
DECLARE
  exception_1 EXCEPTION (-20001, 'Catch and continue');
BEGIN
  LET counter := 0;
  IF (TRUE) THEN
    RAISE exception_1;
  END IF;
  counter := counter + 10;
  RETURN 'Counter value: ' || counter;
EXCEPTION
  WHEN exception_1 CONTINUE THEN
    counter := counter +1;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  exception_1 EXCEPTION (-20001, 'Catch and continue');
BEGIN
  LET counter := 0;
  IF (TRUE) THEN
    RAISE exception_1;
  END IF;
  counter := counter + 10;
  RETURN 'Counter value: ' || counter;
EXCEPTION
  WHEN exception_1 CONTINUE THEN
    counter := counter +1;
END;
$$;
```

The output shows that the exception handler caught the exception, executed a statement that added
`1` to the counter, and then executed the next statement after the exception was caught, which
added `10` to the counter:

```
+-------------------+
| anonymous block   |
|-------------------|
| Counter value: 11 |
+-------------------+
```

The following example shows how an exception handler with a `WHEN` clause of the `CONTINUE` type works
when an error is raised in a loop. The example raises an error on the first iteration because it tries to
divide the value `10` by zero. The `CONTINUE` handler logs the error in the `error_log_table`, and the block
continues with the next iteration of the loop, which divides `10` by `1`. The loop continues to iterate until
`10` is divided by `5` and the loop ends. The output is `2`:

Copy code

```
CREATE TABLE error_log_table (handler_type VARCHAR, error_message VARCHAR);

DECLARE
  x INT := 0;
BEGIN
  FOR i IN 0 TO 5 DO
    x := 10/i;
  END FOR;
  RETURN x;
EXCEPTION
  WHEN EXPRESSION_ERROR CONTINUE THEN
    INSERT INTO error_log_table SELECT 'continue_type', :SQLERRM;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE TABLE error_log_table (handler_type VARCHAR, error_message VARCHAR);

EXECUTE IMMEDIATE $$
DECLARE
  x INT := 0;
BEGIN
  FOR i IN 0 TO 5 DO
    x := 10/i;
  END FOR;
  RETURN x;
EXCEPTION
  WHEN EXPRESSION_ERROR CONTINUE THEN
    INSERT INTO error_log_table SELECT 'continue_type', :SQLERRM;
END;
$$;
```

```
+-----------------+
| anonymous block |
|-----------------|
|               2 |
+-----------------+
```

### Handle exceptions in nested blocks

This following example demonstrates nested blocks, and shows that an inner block
can raise an exception declared in either the inner block or in an outer block:

Copy code

```
DECLARE
  e1 EXCEPTION (-20001, 'Exception e1');
BEGIN
  -- Inner block.
  DECLARE
    e2 EXCEPTION (-20002, 'Exception e2');
    selector BOOLEAN DEFAULT TRUE;
  BEGIN
    IF (selector) THEN
      RAISE e1;
    ELSE
      RAISE e2;
    END IF;
  END;
EXCEPTION
  WHEN e1 THEN
    RETURN SQLERRM || ' caught in outer block.';
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  e1 EXCEPTION (-20001, 'Exception e1');
BEGIN
  -- Inner block.
  DECLARE
    e2 EXCEPTION (-20002, 'Exception e2');
    selector BOOLEAN DEFAULT TRUE;
  BEGIN
    IF (selector) THEN
      RAISE e1;
    ELSE
      RAISE e2;
    END IF;
  END;
EXCEPTION
  WHEN e1 THEN
    RETURN SQLERRM || ' caught in outer block.';
END;
$$;
```

The output shows that the exception handler caught the exception:

```
+-------------------------------------+
| anonymous block                     |
|-------------------------------------|
| Exception e1 caught in outer block. |
+-------------------------------------+
```

This following example is similar to the previous example, but demonstrates nested blocks, each of which has its
own exception handler:

Copy code

```
DECLARE
  result VARCHAR;
  e1 EXCEPTION (-20001, 'Outer exception e1');
BEGIN
  result := 'No error so far (but there will be).';
  DECLARE
    e1 EXCEPTION (-20101, 'Inner exception e1');
  BEGIN
    RAISE e1;
  EXCEPTION
    WHEN e1 THEN
      result := 'Inner exception raised.';
      RETURN result;
  END;
  RETURN result;
EXCEPTION
  WHEN e1 THEN
    result := 'Outer exception raised.';
    RETURN result;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  result VARCHAR;
  e1 EXCEPTION (-20001, 'Outer exception e1');
BEGIN
  result := 'No error so far (but there will be).';
  DECLARE
    e1 EXCEPTION (-20101, 'Inner exception e1');
  BEGIN
    RAISE e1;
  EXCEPTION
    WHEN e1 THEN
      result := 'Inner exception raised.';
      RETURN result;
  END;
  RETURN result;
EXCEPTION
  WHEN e1 THEN
    result := 'Outer exception raised.';
    RETURN result;
END;
$$;
```

Note

This example uses the same exception name (`e1`) in the outer and inner blocks, which isn’t recommended.

The example does this to illustrate the [scope](/developer-guide/snowflake-scripting/variables#label-snowscript-scope) of exception names. The two exceptions with the
name `e1` are different exceptions.

The `e1` handler in the outer block doesn’t handle the exception e1 that is declared and raised in the inner block.

The output shows that the inner exception handler ran:

```
+-------------------------+
| anonymous block         |
|-------------------------|
| Inner exception raised. |
+-------------------------+
```

### Handle multiple exceptions in the same clause and unspecified exceptions

The following example fragment shows how to perform two tasks:

- Catch more than one exception in the same clause by using `OR`.
- Catch unspecified exceptions by using `WHEN OTHER THEN`.

Copy code

```
EXCEPTION
  WHEN MY_FIRST_EXCEPTION OR MY_SECOND_EXCEPTION OR MY_THIRD_EXCEPTION THEN
    RETURN 123;
  WHEN MY_FOURTH_EXCEPTION THEN
    RETURN 4;
  WHEN OTHER THEN
    RETURN 99;
```

### Handle exceptions by using built-in variables

The following example shows how to return SQLCODE, SQLERRM (SQL error message), and SQLSTATE
[built-in variable values](/developer-guide/snowflake-scripting/exceptions#label-snowscript-exception-handling) when catching an exception:

Copy code

```
DECLARE
  MY_EXCEPTION EXCEPTION (-20001, 'Sample message');
BEGIN
  RAISE MY_EXCEPTION;
EXCEPTION
  WHEN STATEMENT_ERROR THEN
    RETURN OBJECT_CONSTRUCT('Error type', 'STATEMENT_ERROR',
                            'SQLCODE', SQLCODE,
                            'SQLERRM', SQLERRM,
                            'SQLSTATE', SQLSTATE);
  WHEN EXPRESSION_ERROR THEN
    RETURN OBJECT_CONSTRUCT('Error type', 'EXPRESSION_ERROR',
                            'SQLCODE', SQLCODE,
                            'SQLERRM', SQLERRM,
                            'SQLSTATE', SQLSTATE);
  WHEN OTHER THEN
    RETURN OBJECT_CONSTRUCT('Error type', 'Other error',
                            'SQLCODE', SQLCODE,
                            'SQLERRM', SQLERRM,
                            'SQLSTATE', SQLSTATE);
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  MY_EXCEPTION EXCEPTION (-20001, 'Sample message');
BEGIN
  RAISE MY_EXCEPTION;
EXCEPTION
  WHEN STATEMENT_ERROR THEN
    RETURN OBJECT_CONSTRUCT('Error type', 'STATEMENT_ERROR',
                            'SQLCODE', SQLCODE,
                            'SQLERRM', SQLERRM,
                            'SQLSTATE', SQLSTATE);
  WHEN EXPRESSION_ERROR THEN
    RETURN OBJECT_CONSTRUCT('Error type', 'EXPRESSION_ERROR',
                            'SQLCODE', SQLCODE,
                            'SQLERRM', SQLERRM,
                            'SQLSTATE', SQLSTATE);
  WHEN OTHER THEN
    RETURN OBJECT_CONSTRUCT('Error type', 'Other error',
                            'SQLCODE', SQLCODE,
                            'SQLERRM', SQLERRM,
                            'SQLSTATE', SQLSTATE);
END;
$$;
```

Running this example produces the following output:

```
+--------------------------------+
| anonymous block                |
|--------------------------------|
| {                              |
|   "Error type": "Other error", |
|   "SQLCODE": -20001,           |
|   "SQLERRM": "Sample message", |
|   "SQLSTATE": "P0001"          |
| }                              |
+--------------------------------+
```
