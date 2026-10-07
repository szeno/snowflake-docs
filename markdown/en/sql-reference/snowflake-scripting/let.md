# LET (Snowflake Scripting)

Assigns an expression to a Snowflake Scripting variable, cursor, or RESULTSET.

For more information on variables, cursors, and RESULTSETs, see:

- [Working with variables](/developer-guide/snowflake-scripting/variables)
- [Working with cursors](/developer-guide/snowflake-scripting/cursors)
- [Working with RESULTSETs](/developer-guide/snowflake-scripting/resultsets)

Note

This [Snowflake Scripting](/developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](/developer-guide/snowflake-scripting/blocks).

If you run a `LET` statement outside a block (for example, directly in a worksheet), you get an error
similar to `syntax error ... unexpected 'LET'`. To fix this, wrap the statement in a
`BEGIN ... END` block. For details, see
[Understanding Snowflake Scripting blocks](/developer-guide/snowflake-scripting/blocks).

See also:
:   [DECLARE](/sql-reference/snowflake-scripting/declare)

## Syntax

Copy code

```
LET { <variable_assignment> | <cursor_assignment> | <resultset_assignment> }
```

The syntax for each type of assignment is described below in more detail.

- [Variable assignment syntax](#label-snowscript-let-syntax-variable)
- [Cursor assignment syntax](#label-snowscript-let-syntax-cursor)
- [RESULTSET assignment syntax](#label-snowscript-let-syntax-resultset)

### Variable assignment syntax

Use the following syntax to assign an expression to a [variable](/developer-guide/snowflake-scripting/variables).

Copy code

```
LET <variable_name> <type> { DEFAULT | := } <expression> ;

LET <variable_name> { DEFAULT | := } <expression> ;
```

Where:

> `variable_name`
> :   The name of the variable. The name must follow the naming rules for [object identifiers](/sql-reference/identifiers).
>
> `type`
> > A [SQL data type](/sql-reference-data-types).
>
> `DEFAULT expression` or `:= expression`
> :   Assigns the value of `expression` to the variable.
>
>     If both `type` and `expression` are specified, the expression must evaluate to a data type that matches.

For example, the following block declares three variables of type [NUMBER](/sql-reference/data-types-numeric#label-data-type-number),
with precision set to `38` and scale set to `2`, computes a result, and returns it.
The variables use either `DEFAULT` or `:=` to specify a value.

Copy code

```
BEGIN
  LET revenue NUMBER(38, 2) DEFAULT 110.0;
  LET cost NUMBER(38, 2) := 100.0;
  LET profit NUMBER(38, 2) := :revenue - :cost;
  RETURN :profit;
END;
```

For more examples, see:

- [Working with variables](/developer-guide/snowflake-scripting/variables)
- [IF statements](/developer-guide/snowflake-scripting/branch#label-snowscript-branch-if)
- [Working with loops](/developer-guide/snowflake-scripting/loops)
- [Examples for common use cases of Snowflake Scripting](/developer-guide/snowflake-scripting/use-cases)

### Cursor assignment syntax

Use one of the following syntaxes to assign an expression to a [cursor](/developer-guide/snowflake-scripting/cursors).

Copy code

```
LET <cursor_name> CURSOR FOR <query> ;
```

Copy code

```
LET <cursor_name> CURSOR FOR <resultset_name> ;
```

Where:

> `cursor_name`
> :   The name to give the cursor. This can be any valid Snowflake [identifier](/sql-reference/identifiers)
>     that is not already in use in this block. The identifier is used by other cursor-related commands, such as [FETCH (Snowflake Scripting)](/sql-reference/snowflake-scripting/fetch).
>
> `query`
> :   The query that defines the result set that the cursor iterates over.
>
>     This can be almost any valid SELECT statement.
>
> `resultset_name`
> :   The name of the [RESULTSET](/developer-guide/snowflake-scripting/resultsets) for the cursor to operate on.

The following examples use this table:

Copy code

```
CREATE OR REPLACE TABLE invoices (price NUMBER);
INSERT INTO invoices (price) VALUES (11.11), (22.22), (33.33);
```

For example, the following block declares a cursor for a query, opens it, fetches each row, and
accumulates a total:

Copy code

```
DECLARE
  total_price FLOAT DEFAULT 0.0;
  c1 CURSOR FOR SELECT price FROM invoices;
BEGIN
  OPEN c1;
  FOR record IN c1 DO
    total_price := total_price + record.price;
  END FOR;
  CLOSE c1;
  RETURN total_price;
END;
```

You can also declare a cursor that iterates over a RESULTSET:

Copy code

```
DECLARE
  res RESULTSET DEFAULT (SELECT price FROM invoices);
  c1 CURSOR FOR res;
BEGIN
  FOR record IN c1 DO
    RETURN record.price;
  END FOR;
END;
```

For more examples, see [Working with cursors](/developer-guide/snowflake-scripting/cursors).

### RESULTSET assignment syntax

Use the following syntax to assign an expression to a [RESULTSET](/developer-guide/snowflake-scripting/resultsets).

Copy code

```
LET <resultset_name> RESULTSET { DEFAULT | := } ( <query> ) ;
```

Where:

> `resultset_name`
> :   The name to give the RESULTSET.
>
>     The name should be unique within the current scope.
>
>     The name must follow the naming rules for [Object identifiers](/sql-reference/identifiers).
>
> `DEFAULT query` or `:= query`
> :   Assigns the value of `query` to the RESULTSET.

For example, the following block declares a RESULTSET and returns it as a table result:

Copy code

```
BEGIN
  LET res RESULTSET := (SELECT price FROM invoices WHERE price > 20);
  RETURN TABLE(res);
END;
```

For more examples, see [Working with RESULTSETs](/developer-guide/snowflake-scripting/resultsets).
