# CONTINUE (Snowflake Scripting)

`CONTINUE` (or `ITERATE`) skips the rest of the statements in the iteration of a loop and starts the next iteration of
the loop.

For more information on terminating the current iteration of a loop, see [Terminating an iteration without terminating the loop](/developer-guide/snowflake-scripting/loops#label-snowscript-loop-continue).

Note

This [Snowflake Scripting](/developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](/developer-guide/snowflake-scripting/blocks).

See also:
:   [BREAK](/sql-reference/snowflake-scripting/break)

## Syntax

Copy code

```
{ CONTINUE | ITERATE } [ <label> ] ;
```

Where:

> `label`
> :   An optional label. If the label is specified, the `CONTINUE` will start at the first statement in the loop with
>     the label.
>
>     You can use this to continue more than one level higher in a nested loop or a nested branch.

## Usage notes

- `CONTINUE` and `ITERATE` are synonymous.
- If the loop is embedded in another loop(s), you can break out of not only the current loop and start from the first statement in
  the enclosing loop by including the enclosing loop’s label as part of the `CONTINUE`. For an example, see the examples
  section below.

## Examples

The following loop iterates 3 times. Because the code after the `CONTINUE` statement is not executed, the variable
named `counter2` will be 0 rather than 3.

> Copy code
>
> ```
> DECLARE
>   counter1 NUMBER(8, 0);
>   counter2 NUMBER(8, 0);
> BEGIN
>   counter1 := 0;
>   counter2 := 0;
>   WHILE (counter1 < 3) DO
>     counter1 := counter1 + 1;
>     CONTINUE;
>     counter2 := counter2 + 1;
>   END WHILE;
>   RETURN counter2;
> END;
> ```
>
> Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
> `execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
> code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):
>
> Copy code
>
> ```
> EXECUTE IMMEDIATE $$
> DECLARE
>     counter1 NUMBER(8, 0);
>     counter2 NUMBER(8, 0);
> BEGIN
>     counter1 := 0;
>     counter2 := 0;
>     WHILE (counter1 < 3) DO
>         counter1 := counter1 + 1;
>         CONTINUE;
>         counter2 := counter2 + 1;
>     END WHILE;
>     RETURN counter2;
> END;
> $$;
> ```

Here is the output of executing the example:

Copy code

```
+-----------------+
| anonymous block |
|-----------------|
|               0 |
+-----------------+
```
