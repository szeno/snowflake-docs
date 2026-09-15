# REPEAT (Snowflake Scripting)

A `REPEAT` loop iterates until a specified condition is true. A `REPEAT` loop tests the condition at
the end of the loop. This means that the body of a `REPEAT` loop always executes at least once.

For more information on loops, see [Working with loops](/developer-guide/snowflake-scripting/loops).

Note

This [Snowflake Scripting](/developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](/developer-guide/snowflake-scripting/blocks).

See also:
:   [BREAK](/sql-reference/snowflake-scripting/break), [CONTINUE](/sql-reference/snowflake-scripting/continue)

## Syntax

Copy code

```
REPEAT
    <statement>;
    [ <statement>; ... ]
UNTIL ( <condition> )
END REPEAT [ <label> ] ;
```

Where:

> `statement`
> :   A statement can be any of the following:
>
>     - A single SQL statement (including CALL).
>     - A control-flow statement (for example, a [looping](/developer-guide/snowflake-scripting/loops) or
>       [branching](/developer-guide/snowflake-scripting/branch) statement).
>     - A nested [block](/developer-guide/snowflake-scripting/blocks).
>
> `condition`
> :   An expression that evaluates to a BOOLEAN.
>
> `label`
> :   An optional label. Such a label can be a jump target for a [BREAK](/sql-reference/snowflake-scripting/break) or
>     [CONTINUE](/sql-reference/snowflake-scripting/continue) statement. A label must follow the naming rules for
>     [Object identifiers](/sql-reference/identifiers).

## Usage notes

- Put parentheses around the condition in the `REPEAT`. For example: `REPEAT ( <condition> )`.
- If the `condition` never evaluates to TRUE, and the loop does not contain a
  [BREAK](/sql-reference/snowflake-scripting/break) command (or equivalent), then the loop will run and consume credits
  indefinitely.
- If the `condition` is NULL, then it is treated as FALSE.
- A loop can contain multiple statements. You can use, but are not required to use, a [BEGIN … END](/sql-reference/snowflake-scripting/begin)
  [block](/developer-guide/snowflake-scripting/blocks) to contain those statements.

## Examples

This example uses a loop to calculate a power of 2. (This is an inefficient solution, but it does
demonstrate looping.)

Copy code

```
CREATE PROCEDURE power_of_2()
RETURNS NUMBER(8, 0)
LANGUAGE SQL
AS
$$
DECLARE
    counter NUMBER(8, 0);      -- Loop counter.
    power_of_2 NUMBER(8, 0);   -- Stores the most recent power of 2 that we calculated.
BEGIN
    counter := 1;
    power_of_2 := 1;
    REPEAT
        power_of_2 := power_of_2 * 2;
        counter := counter + 1;
    UNTIL (counter > 8)
    END REPEAT;
    RETURN power_of_2;
END;
$$;
```

Here is the output of executing the stored procedure:

Copy code

```
CALL power_of_2();
+------------+
| POWER_OF_2 |
|------------|
|        256 |
+------------+
```

For more examples, see [REPEAT loop](/developer-guide/snowflake-scripting/loops#label-snowscript-loop-repeat).
