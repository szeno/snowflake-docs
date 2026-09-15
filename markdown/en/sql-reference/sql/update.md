# UPDATE

Updates specified rows in the target table with new values.

## Syntax

Copy code

```
UPDATE <target_table>
       SET <col_name> = <value> [ , <col_name> = <value> , ... ]
        [ FROM <additional_tables> ]
        [ WHERE <condition> ]
```

## Required parameters

`target_table`
:   Specifies the table to update.

`col_name`
:   Specifies the name of a column in `target_table`. Do not include the table name. For example, `UPDATE t1 SET t1.col = 1`
    is invalid.

`value`
:   Specifies the new value to set in `col_name`.

## Optional parameters

`FROM additional_tables`
:   Specifies one or more tables to use for selecting rows to update or for setting new values. Note that repeating the target table results
    in a self-join.

`WHERE condition`
:   Expression that specifies the rows in the target table to update.

    Default: No value (all rows of the target table are updated)

## Usage notes

- When a [FROM](/sql-reference/constructs/from) clause contains a [JOIN](/sql-reference/constructs/join) between
  tables (e.g. `t1` and `t2`), a target row in `t1` may join against (i.e. match) more than one row in table `t2`. When
  this occurs, the target row is called a *multi-joined row*. When updating a multi-joined row, the
  [ERROR\_ON\_NONDETERMINISTIC\_UPDATE](/sql-reference/parameters#label-error-on-nondeterministic-update) session parameter controls the outcome of the update:

  - If `FALSE` (default value), no error is returned and one of the joined rows is used to update the target row; however, the
    selected joined row is nondeterministic.
  - IF `TRUE`, an error is returned, including an example of the values of a target row that joins multiple rows.

  To set the parameter:

  Copy code

  ```
  ALTER SESSION SET ERROR_ON_NONDETERMINISTIC_UPDATE=TRUE;
  ```

## Examples

Perform a standard update using two tables:

> Copy code
>
> ```
> UPDATE t1
>   SET number_column = t1.number_column + t2.number_column, t1.text_column = 'ASDF'
>   FROM t2
>   WHERE t1.key_column = t2.t1_key and t1.number_column < 10;
> ```

Update with join that produces nondeterministic results:

> Copy code
>
> ```
> select * from target;
>
> +---+----+
> | K |  V |
> |---+----|
> | 0 | 10 |
> +---+----+
>
> Select * from src;
>
> +---+----+
> | K |  V |
> |---+----|
> | 0 | 11 |
> | 0 | 12 |
> | 0 | 13 |
> +---+----+
>
> -- Following statement joins all three rows in src against the single row in target
> UPDATE target
>   SET v = src.v
>   FROM src
>   WHERE target.k = src.k;
>
> +------------------------+-------------------------------------+
> | number of rows updated | number of multi-joined rows updated |
> |------------------------+-------------------------------------|
> |                      1 |                                   1 |
> +------------------------+-------------------------------------+
> ```
>
> - With [ERROR\_ON\_NONDETERMINISTIC\_UPDATE](/sql-reference/parameters#label-error-on-nondeterministic-update) = FALSE, the statement randomly updates the single row in `target` using
>   values from one of the following rows in `src`:
>   `(0, 11)` , `(0, 12)` , `(0,13)`
> - With [ERROR\_ON\_NONDETERMINISTIC\_UPDATE](/sql-reference/parameters#label-error-on-nondeterministic-update) = TRUE, an error is returned reporting a duplicate DML row `[0, 10]`.

To avoid this nondeterministic behavior and error, use a 1-to-1 join:

> Copy code
>
> ```
> UPDATE target SET v = b.v
>   FROM (SELECT k, MIN(v) v FROM src GROUP BY k) b
>   WHERE target.k = b.k;
> ```
>
> This statement results in the single row in `target` updated to `(0, 11)` (values from the row with the minimum value for
> `v` in `src`) and will never result in an error.
