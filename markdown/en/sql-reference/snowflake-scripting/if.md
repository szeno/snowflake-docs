# IF (Snowflake Scripting)

An `IF` statement provides a way to execute a set of statements if a condition is met.

For more information on branching constructs, see [Working with conditional logic](/developer-guide/snowflake-scripting/branch).

Note

This [Snowflake Scripting](/developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](/developer-guide/snowflake-scripting/blocks).

## Syntax

Copy code

```
IF ( <condition> ) THEN
    <statement>;
    [ <statement>; ... ]
[
ELSEIF ( <condition> ) THEN
    <statement>;
    [ <statement>; ... ]
]
[
ELSE
    <statement>;
    [ <statement>; ... ]
]
END IF;
```

Where:

> `condition`
> :   An expression that evaluates to a BOOLEAN.
>
> `statement`
> :   A statement can be any of the following:
>
>     - A single SQL statement (including CALL).
>     - A control-flow statement (for example, a [looping](/developer-guide/snowflake-scripting/loops) or
>       [branching](/developer-guide/snowflake-scripting/branch) statement).
>     - A nested [block](/developer-guide/snowflake-scripting/blocks).

## Usage notes

- The keyword `THEN` is required.
- `ELSEIF` is one word (no spaces).
- `END IF` is two words.
- After each `THEN` or `ELSE` clause, the body allows the `BEGIN` and `END` keywords, but does not require
  them, even if the body contains more than one `statement`.
- If the `condition` is NULL, then it is treated as FALSE.

## Examples

Here is an example of a Snowflake Scripting `IF` statement inside a stored procedure:

Copy code

```
CREATE OR REPLACE PROCEDURE example_if(flag INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN
  IF (FLAG = 1) THEN
    RETURN 'one';
  ELSEIF (FLAG = 2) THEN
    RETURN 'two';
  ELSE
    RETURN 'Unexpected input.';
  END IF;
END;
$$
;
```

Here is the command to call the stored procedure, along with the output:

Copy code

```
CALL example_if(3);
```

```
+-------------------+
| EXAMPLE_IF        |
|-------------------|
| Unexpected input. |
+-------------------+
```

For more examples that use the `IF` statement, see:

- [Working with conditional logic](/developer-guide/snowflake-scripting/branch) - Return different values based on IF conditions
  in a simple anonymous block.
- [Examples for common use cases of Snowflake Scripting](/developer-guide/snowflake-scripting/use-cases) - Execute SQL statements based on IF conditions in loops.
- [BREAK](/sql-reference/snowflake-scripting/break), [LOOP](/sql-reference/snowflake-scripting/loop), and [Working with loops](/developer-guide/snowflake-scripting/loops) -
  Execute BREAK statements to terminate a loop based on IF conditions.
- [EXCEPTION](/sql-reference/snowflake-scripting/exception) - Raise exceptions based on IF conditions.
