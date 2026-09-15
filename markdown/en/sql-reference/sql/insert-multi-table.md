# INSERT (multi-table)

Updates multiple tables by inserting one or more rows with column values (from a query) into the tables. Supports both unconditional and
conditional inserts.

See also:
:   [INSERT](/sql-reference/sql/insert)

## Syntax

Copy code

```
-- Unconditional multi-table insert
INSERT [ OVERWRITE ] ALL
  intoClause [ ... ]
<subquery>

-- Conditional multi-table insert
INSERT [ OVERWRITE ] { FIRST | ALL }
  { WHEN <condition> THEN intoClause [ ... ] }
  [ ... ]
  [ ELSE intoClause ]
<subquery>
```

Where:

> Copy code
>
> ```
> intoClause ::=
>   INTO <target_table> [ ( <target_col_name> [ , ... ] ) ] [ VALUES ( { <source_col_name> | DEFAULT | NULL } [ , ... ] ) ]
> ```

## Required parameters

`ALL`
:   Unconditional multi-table insert only

    Specifies that each row executes every `INTO` clause in the INSERT statement.

    Note

    If the `FIRST` keyword is specified in an unconditional multi-table insert (or the `ALL` keyword is not specified),
    Snowflake returns a syntax error.

`FIRST` or `ALL`
:   Conditional multi-table insert only

    `FIRST`
    :   Specifies that each row executes only the first `WHEN` clause for which the condition evaluates to TRUE. If no `WHEN`
        clause evaluates to TRUE, then the `ELSE` clause, if present, executes.

    `ALL`
    :   Specifies that each row executes all `WHEN` clauses. If no `WHEN` clause evaluates to TRUE, then the `ELSE`
        clause, if present, executes.

    Note

    - A conditional multi-table insert must contain at least one `WHEN` clause.
    - Each `WHEN` clause can contain multiple `INTO` clauses and the `INTO` clauses can insert into the same target
      table.
    - To always execute a `WHEN` clause, use:
      `WHEN 1=1 THEN ...`

`condition`
:   Conditional multi-table insert only

    Specifies the condition that must evaluate to TRUE in order for the values specified in the `INTO` clause to be inserted. The
    condition can be a [SELECT](/sql-reference/sql/select) list.

`target_table`
:   Specifies a target table into which to insert rows. The same table may be referenced more than once (in separate `WHEN` clauses).

    Multiple tables can be targeted by including a `INTO` clause for each table.

`subquery`
:   Specifies the [SELECT](/sql-reference/sql/select) list that determines the source of the values to be inserted into the target tables.

## Optional parameters

`OVERWRITE`
:   Specifies to truncate the target tables before inserting into the tables, while retaining access control privileges on the tables.

    INSERT statements with `OVERWRITE` can be processed within the scope of the current transaction, which avoids DDL statements that
    commit a transaction, such as:

    > Copy code
    >
    > ```
    > DROP TABLE t;
    > CREATE TABLE t AS SELECT * FROM ... ;
    > ```

    Default: No value (the target tables are not truncated before performing the inserts)

`( target_col_name [ , ... ] )`
:   Specifies one or more columns in the target table into which the values from the corresponding column in the source is inserted. The
    number of target columns specified must match the number of values specified in the source.

    Default: No value (all the columns in the target table are updated)

`VALUES ( source_col_name | DEFAULT | NULL [ , ... ] )`
:   Specifies one or more values to insert into the corresponding columns in the target table. The values can be:

    - `source_col_name`: Specifies the column in the source that contains the value to be inserted into the corresponding column in
      the target table.
    - `DEFAULT`: Inserts the default value for the corresponding column in the target table.
    - `NULL`: Inserts a `NULL` value.

    Each value in the clause must be separated by a comma. Also, the number of values specified must match the number of columns specified
    for the target table.

    Default: No value (values from all the columns in the source are inserted into the corresponding columns in the target table)

## Usage notes

- In an `INTO` clause, the `VALUES` clause is optional. If it is omitted, the values from the [SELECT](/sql-reference/sql/select) list are inserted
  into the target table in their natural order.
- Expressions in `WHEN` clauses (for conditional multi-table inserts) and `VALUES` clauses can only reference the subquery
  via an alias. The alias must be one of the following:

  - Explicit alias specified for a [SELECT](/sql-reference/sql/select) expression.
  - Default alias for an expression.
  - Positional alias ($1, $2, etc.).

  In addition, columns and expressions of the subquery that are not in the outermost [SELECT](/sql-reference/sql/select) list can not be referenced in
  `WHEN` and `VALUES` clauses. For details, see [Examples](#examples) (in this topic).
- In each row produced by the `subquery`, the value in `source_col_name` must be compatible with the data type of the
  corresponding `target_col_name`. This rule applies even to rows that would be filtered out by the `condition` in the
  `WHEN` clause. The order of operations does not guarantee that the filter in the `WHEN` clause is applied before the value in
  `source_col_name` is evaluated for data type compatibility.

## Examples

### Unconditional multi-table inserts

Insert each row in the `src` table twice into tables `t1` and `t2`. In this example, the inserted rows are not
identical; each of the inserted rows has different values/orders because we use the VALUES clause to vary the data:

> Copy code
>
> ```
> INSERT ALL
>   INTO t1
>   INTO t1 (c1, c2, c3) VALUES (n2, n1, DEFAULT)
>   INTO t2 (c1, c2, c3)
>   INTO t2 VALUES (n3, n2, n1)
> SELECT n1, n2, n3 from src;
>
> -- If t1 and t2 need to be truncated before inserting, OVERWRITE must be specified
> INSERT OVERWRITE ALL
>   INTO t1
>   INTO t1 (c1, c2, c3) VALUES (n2, n1, DEFAULT)
>   INTO t2 (c1, c2, c3)
>   INTO t2 VALUES (n3, n2, n1)
> SELECT n1, n2, n3 from src;
> ```

### Conditional multi-table inserts

The next two examples show how to create conditional multi-table inserts by
using `WHEN` clauses and an `ELSE` clause to decide which table(s), if any, each row is inserted into.

These examples also show the difference between using `INSERT ALL` and
`INSERT FIRST`.

Execute all `WHEN` clauses with an `ELSE` clause:

- Rows where `n1 > 100` also satisfy the condition `n1 > 10` and are therefore inserted in `t1` twice when the
  `ALL` keyword is used.
- Rows where `n1 <= 10` satisfy the `ELSE` case and are inserted in `t2`.

  Copy code

  ```
  INSERT ALL
    WHEN n1 > 100 THEN
   INTO t1
    WHEN n1 > 10 THEN
   INTO t1
   INTO t2
    ELSE
   INTO t2
  SELECT n1 from src;
  ```

If the table src contains 3 rows, in which n1 has the values 1, 11, and 101,
then after the INSERT statement the tables t1 and t2 will hold the values shown
below:

t1:

| 101 | 101 > 100, so the first `WHEN` clause inserts into t1 |
| --- | --- |
| 101 | 101 > 10, so the second `WHEN` clause also inserts into t1 |
| 11 | 11 > 10, so the second `WHEN` clause inserts into t1 |

Expand

Show lessSee more

The row with `n1 = 1` is not inserted into t1 because it does not satisfy
any `WHEN` clause that inserts into t1, and because the `ELSE`
clause does not insert into t1.

t2:

| 101 | 101 > 10, so the second `WHEN` clause inserts into t2. (The row also qualifies for the clause `WHEN n1 > 100`; however, that clause does not insert into t2.) |
| --- | --- |
| 11 | 11 > 10, so the second `WHEN` clause inserts into t2 |
| 1 | the row didn’t satisfy any of the `WHEN` clauses, so it’s inserted into t2 by the `ELSE` clause |

Expand

Show lessSee more

The next example is similar to the previous example, except with a `FIRST` clause.

> Copy code
>
> ```
> INSERT FIRST
>   WHEN n1 > 100 THEN
>     INTO t1
>   WHEN n1 > 10 THEN
>     INTO t1
>     INTO t2
>   ELSE
>     INTO t2
> SELECT n1 from src;
> ```

If the table src contains 3 rows, in which n1 has the values 1, 11, and 101, then after the INSERT statement the tables t1 and t2 will
hold the values shown below:

t1:

| 101 | 101 > 100, so the first `WHEN` clause inserts into t1 |
| --- | --- |
| 11 | 11 > 10, so the second `WHEN` clause inserts into t1 |

Expand

Show lessSee more

The row with `n1 = 1` is not inserted into t1 because it does not satisfy any `WHEN` clause that inserts into t1, and because
the `ELSE` clause does not insert into t1.

Unlike in the previous example, which used `ALL`, the row with `n1 = 101` is inserted into t1 only once because the first
`WHEN` clause evaluates to TRUE so the second `WHEN` clause is ignored.

t2:

| 11 | 11 > 10, so the second `WHEN` clause inserts into t2 |
| --- | --- |
| 1 | the row didn’t satisfy any of the `WHEN` clauses, so it’s inserted into t2 by the `ELSE` clause |

Expand

Show lessSee more

The row `n1 = 101` is not inserted into t2 because 101 is greater than 100, so it matches the first `WHEN` clause, but the
first `WHEN` clause doesn’t insert into t2, and the statement doesn’t check any of the other `WHEN` clauses or use the
`ELSE` clause because the row already qualified for the first `WHEN` clause.

### Multi-table inserts with aliases and references

Insert values using a positional alias (`$1`), an explicit alias (`an_alias`), and a default alias (`"10 + 20"`);
this example inserts a single row with values `(1, 50, 30)` into table `t1`:

> Copy code
>
> ```
> INSERT ALL
>   INTO t1 VALUES ($1, an_alias, "10 + 20")
> SELECT 1, 50 AS an_alias, 10 + 20;
> ```

Illustrate inserting values from columns that must be selected to be referenced (`b` and `c` in table `src`):

> Copy code
>
> ```
> -- Returns error
>   INSERT ALL
>     WHEN c > 10 THEN
>       INTO t1 (col1, col2) VALUES (a, b)
>   SELECT a FROM src;
>
> -- Completes successfully
>   INSERT ALL
>     WHEN c > 10 THEN
>       INTO t1 (col1, col2) VALUES (a, b)
>   SELECT a, b, c FROM src;
> ```

Illustrate inserting values from a column that cannot be referenced (`src1.key`); instead, it must be selected and aliased:

> Copy code
>
> ```
> -- Returns error
>   INSERT ALL
>     INTO t1 VALUES (src1.key, a)
>   SELECT src1.a AS a
>   FROM src1, src2 WHERE src1.key = src2.key;
>
> -- Completes successfully
>   INSERT ALL
>     INTO t1 VALUES (key, a)
>   SELECT src1.key AS key, src1.a AS a
>   FROM src1, src2 WHERE src1.key = src2.key;
> ```
