Categories:
:   [Table functions](/sql-reference/functions-table)

# GENERATOR

Creates rows of data based either on a specified number of rows, a specified generation period (in seconds), or both. This system-defined table function enables synthetic row generation.

Note that it is possible to generate virtual tables with 0 columns but possibly many rows. Such virtual tables are useful for queries whose [SELECT](/sql-reference/sql/select) clause consists entirely
of data-generating functions.

## Syntax

Copy code

```
GENERATOR( ROWCOUNT => <count> [ , TIMELIMIT => <sec> ] )

GENERATOR( [ TIMELIMIT => <sec> ] )
```

## Usage notes

- `count` and `sec` must be non-negative integer constants.
- If only the `ROWCOUNT` argument is specified, the resulting table will contain `count` rows.
- If only the `TIMELIMIT` argument is specified, the query runs for `sec` seconds, generating as many
  rows as possible within the time frame. The exact row count depends on the system speed and is not entirely
  deterministic.
- If both the `ROWCOUNT` and `TIMELIMIT` arguments are specified, then:

  - If the `ROWCOUNT` is reached before the `TIMELIMIT`, the resulting table will contain `count`
    rows.
  - If the `TIMELIMIT` is reached before the `ROWCOUNT`, the table will contain the number of rows
    generated within the time frame. The exact row count depends on the system speed and is not entirely deterministic.
- If `ROWCOUNT` or `TIMELIMIT` is null, it will be ignored. So `generator(ROWCOUNT => null)` generates 0 rows.
- If both parameters (`ROWCOUNT` and `TIMELIMIT`) are omitted, the GENERATOR function returns 0 rows.
- The content of the rows is determined by the functions in the projection
  clause, not by the GENERATOR function itself. For more details, see
  the Examples section below. See also the description(s) of the specific
  functions (e.g. SEQ()), that you plan to use in the projection clause;
  not all valid functions produce sequences without gaps.

## Examples

Note

These examples generate sequences that can have gaps. For examples that generate sequences without gaps, refer to
[SEQ1 / SEQ2 / SEQ4 / SEQ8](/sql-reference/functions/seq1) and [ROW\_NUMBER](/sql-reference/functions/row_number).

This example uses the GENERATOR function to generate 10 rows. The content
of the rows is determined by the functions in the projection clause:

- The [SEQ4()](/sql-reference/functions/seq1) column generates a
  sequence of 4-byte integers, starting with 0.
- The [UNIFORM(…)](/sql-reference/functions/uniform) column generates
  values in the range between the first parameter (1) and the second
  parameter (10), based on either a function or a constant passed as the third
  parameter.

This example includes an optional “seed” for the RANDOM() function so that the
output is consistent:

> Copy code
>
> ```
> SELECT seq4(), uniform(1, 10, RANDOM(12))
>   FROM TABLE(GENERATOR(ROWCOUNT => 10)) v
>   ORDER BY 1;
> +--------+----------------------------+
> | SEQ4() | UNIFORM(1, 10, RANDOM(12)) |
> |--------+----------------------------|
> |      0 |                          7 |
> |      1 |                          2 |
> |      2 |                          5 |
> |      3 |                          9 |
> |      4 |                          6 |
> |      5 |                          9 |
> |      6 |                          9 |
> |      7 |                          5 |
> |      8 |                          3 |
> |      9 |                          8 |
> +--------+----------------------------+
> ```

This example is similar to the preceding example, except that it passes a
constant rather than a function as the third parameter to the `UNIFORM`
function. The result is that the output for the `UNIFORM` column is the
same for every row.

> Copy code
>
> ```
> SELECT seq4(), uniform(1, 10, 42)
>   FROM TABLE(GENERATOR(ROWCOUNT => 10)) v
>   ORDER BY 1;
> +--------+--------------------+
> | SEQ4() | UNIFORM(1, 10, 42) |
> |--------+--------------------|
> |      0 |                 10 |
> |      1 |                 10 |
> |      2 |                 10 |
> |      3 |                 10 |
> |      4 |                 10 |
> |      5 |                 10 |
> |      6 |                 10 |
> |      7 |                 10 |
> |      8 |                 10 |
> |      9 |                 10 |
> +--------+--------------------+
> ```

If you omit both the `ROWCOUNT` and `TIMELIMIT` parameters, the output is 0 rows:

> Copy code
>
> ```
> SELECT seq4(), uniform(1, 10, RANDOM(12))
>   FROM TABLE(GENERATOR()) v
>   ORDER BY 1;
> +--------+----------------------------+
> | SEQ4() | UNIFORM(1, 10, RANDOM(12)) |
> |--------+----------------------------|
> +--------+----------------------------+
> ```

The following example uses the `TIMELIMIT` parameter without the `ROWCOUNT` parameter.

Copy code

```
SELECT COUNT(seq4()) FROM TABLE(GENERATOR(TIMELIMIT => 10)) v;

+---------------+
| COUNT(SEQ4()) |
|---------------|
|    3615440896 |
+---------------+
```
