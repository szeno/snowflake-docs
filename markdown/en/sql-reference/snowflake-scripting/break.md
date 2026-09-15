# BREAK (Snowflake Scripting)

`BREAK` (or `EXIT`) terminates a loop.

For more information on terminating loops, see [Terminating a loop](/developer-guide/snowflake-scripting/loops#label-snowscript-loop-terminate).

Note

This [Snowflake Scripting](/developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](/developer-guide/snowflake-scripting/blocks).

See also:
:   [CONTINUE](/sql-reference/snowflake-scripting/continue)

## Syntax

Copy code

```
{ BREAK | EXIT } [ <label> ] ;
```

Where:

> `label`
> :   An optional label. If the label is specified, the `BREAK` will jump to the statement immediately after
>     the label.
>
>     You can use this to break out of more than one level of a nested loop or a nested branch.

## Usage notes

- `BREAK` and `EXIT` are synonymous.
- If the loop is embedded in another loop(s), you can exit out of not only the current loop, but also an
  enclosing loop, by including the enclosing loop’s label as part of the `BREAK`. For an example, see the examples
  section below.

## Examples

Here is an example of using BREAK to exit not only the current loop, but also an enclosing loop:

Copy code

```
DECLARE
  i INTEGER;
  j INTEGER;
BEGIN
  i := 1;
  j := 1;
  WHILE (i <= 4) DO
    WHILE (j <= 4) DO
      -- Exit when j is 3, even if i is still 1.
      IF (j = 3) THEN
        BREAK outer_loop;
      END IF;
      j := j + 1;
    END WHILE inner_loop;
    i := i + 1;
  END WHILE outer_loop;
  -- Execution resumes here after the BREAK executes.
  RETURN i;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
    DECLARE
        i INTEGER;
        j INTEGER;
    BEGIN
        i := 1;
        j := 1;
        WHILE (i <= 4) DO
            WHILE (j <= 4) DO
                -- Exit when j is 3, even if i is still 1.
                IF (j = 3) THEN
                     BREAK outer_loop;
                END IF;
                j := j + 1;
            END WHILE inner_loop;
            i := i + 1;
        END WHILE outer_loop;
        -- Execution resumes here after the BREAK executes.
        RETURN i;
    END;
$$;
```

```
+-----------------+
| anonymous block |
|-----------------|
|               1 |
+-----------------+
```
