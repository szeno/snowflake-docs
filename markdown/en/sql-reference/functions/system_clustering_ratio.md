Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$CLUSTERING\_RATIO — *Deprecated*

Deprecated Feature

This function has been deprecated. It will be obsoleted in a future release (TBD).

Use [SYSTEM$CLUSTERING\_DEPTH](/sql-reference/functions/system_clustering_depth) or [SYSTEM$CLUSTERING\_INFORMATION](/sql-reference/functions/system_clustering_information) instead.

Calculates the clustering ratio for a table, based on one or more columns in the table. The ratio is a number from `0` to `100`. The higher the ratio, the better clustered the table is.

The clustering ratio for a table can be calculated using any columns in the table or columns that have been explicitly defined as a clustering key for the table. A clustering key can be defined for a table
using either [CREATE TABLE](/sql-reference/sql/create-table) or [ALTER TABLE](/sql-reference/sql/alter-table).

For more information about clustering ratio and clustering keys, see [Understanding Snowflake Table Structures](/user-guide/tables-micro-partitions).

## Syntax

Copy code

```
SYSTEM$CLUSTERING_RATIO( '<table_name>' , '( <col1> [ , <col2> ... ] )' [ , '<predicate>' ] )
```

## Arguments

`table_name`
:   Table for which you want to calculate the clustering ratio.

`col1 [ , col2 ... ]`
:   Column(s) in the table used to calculate the clustering ratio:

    - For a table with no clustering key, this argument is required. If this argument is omitted, an error is returned.
    - For a table with a clustering key, this argument is optional; if the argument is omitted, Snowflake uses the defined clustering key to calculate the ratio.

    Note

    You can use this argument to calculate the ratio for any columns in the table, regardless of the clustering key defined for the table.

`predicate`
:   Clause that filters the range of values in the columns on which to calculate the clustering ratio. Note that `predicate` does not utilize a WHERE keyword at the beginning of the clause.

## Usage notes

- All arguments are strings (i.e. they must be enclosed in single quotes).
- If `predicate` contains a string, the string must be enclosed in single quotes, which then must be escaped using single quotes. For example:
  `SYSTEM$CLUSTERING_RATIO( ... , 'col1 = 100 and col2 = ''A''' )`

## Examples

Calculate the clustering ratio for a table using two columns in the table:

> Copy code
>
> ```
> SELECT SYSTEM$CLUSTERING_RATIO('t2', '(col1, col3)');
>
> +-------------------------------+
> | SYSTEM$CLUSTERING_RATIO('T2') |
> |-------------------------------|
> |                          77.1 |
> +-------------------------------+
> ```

Calculate the clustering ratio for a table using two columns in the table and a predicate on one of the columns:

> Copy code
>
> ```
> SELECT SYSTEM$CLUSTERING_RATIO('t2', '(col1, col2)', 'col1 = ''A''');
>
> +-------------------------------+
> | SYSTEM$CLUSTERING_RATIO('T2') |
> |-------------------------------|
> |                          87.7 |
> +-------------------------------+
> ```

Calculate the clustering ratio for a table using the clustering key defined for the table:

> Copy code
>
> ```
> SELECT SYSTEM$CLUSTERING_RATIO('t1');
>
> +-------------------------------+
> | SYSTEM$CLUSTERING_RATIO('T1') |
> |-------------------------------|
> |                         100.0 |
> +-------------------------------+
> ```
