# BEGIN … END (Snowflake Scripting)

`BEGIN` and `END` define a Snowflake Scripting block.

For more information on blocks, see [Understanding blocks in Snowflake Scripting](/developer-guide/snowflake-scripting/blocks).

## Syntax

Copy code

```
BEGIN
    <statement>;
    [ <statement>; ... ]
[ EXCEPTION <exception_handler> ]
END;
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
> `exception_handler`
> :   Specifies how exceptions should be handled. Refer to [Handling exceptions](/developer-guide/snowflake-scripting/exceptions) and
>     [EXCEPTION (Snowflake Scripting)](/sql-reference/snowflake-scripting/exception).

## Usage notes

- The keyword `END` must be followed immediately by a semicolon, or followed immediately by a label that is
  immediately followed by a semicolon.
- The keyword `BEGIN` must not be followed immediately by a semicolon.
- `BEGIN` and `END` are usually used inside another language construct, such as a looping or branching construct,
  or inside a stored procedure. However, this is not required. A BEGIN/END block can be the top-level construct inside
  an anonymous block.
- Blocks can be nested.

## Examples

This is a simple example of using `BEGIN` and `END` to group related statements. This example creates two
related tables.

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

The next example is similar; the statements are grouped into a block and are also inside a transaction within
that block:

Copy code

```
EXECUTE IMMEDIATE $$
BEGIN
    BEGIN TRANSACTION;
    TRUNCATE TABLE child;
    TRUNCATE TABLE parent;
    COMMIT;
    RETURN '';
END;
$$
;
```

In this example, the statements are inside a [branching](/developer-guide/snowflake-scripting/branch) construct.

Copy code

```
IF (both_rows_are_valid) THEN
    BEGIN
        BEGIN TRANSACTION;
        INSERT INTO parent ...;
        INSERT INTO child ...;
        COMMIT;
    END;
END IF;
```
