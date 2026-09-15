Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$CLUSTERING\_DEPTH

Computes the average depth of the table according to the specified columns (or the clustering key defined for the table). The average depth of a populated table (i.e. a table containing
data) is always `1` or more. The smaller the average depth, the better clustered the table is with regards to the specified columns.

For more information about micro-partitions and clustering keys, see [Understanding Snowflake Table Structures](/user-guide/tables-micro-partitions).

See also:
:   [SYSTEM$CLUSTERING\_INFORMATION](/sql-reference/functions/system_clustering_information)

## Syntax

Copy code

```
SYSTEM$CLUSTERING_DEPTH( '<table_name>' , '( <col1> [ , <col2> ... ] )' [ , '<predicate>' ] )
```

## Arguments

`table_name`
:   Table for which you want to calculate the clustering depth.

`col1 [ , col2 ... ]`
:   Column(s) in the table used to calculate the clustering depth:

    - For a table with no clustering key, this argument is required. If this argument is omitted, an error is returned.
    - For a table with a clustering key, this argument is optional; if the argument is omitted, Snowflake uses the defined clustering key to calculate the depth.

    Note

    You can use this argument to calculate the depth for any columns in the table, regardless of the clustering key defined for the table.

`predicate`
:   Clause that filters the range of values in the columns on which to calculate the clustering depth. Note that `predicate` does not utilize a WHERE keyword at the beginning of the clause.

## Usage notes

- All arguments are strings (i.e. they must be enclosed in single quotes).
- If `predicate` contains a string, the string must be enclosed in single quotes, which then must be escaped using single quotes. For example:
  `SYSTEM$CLUSTERING_DEPTH( ... , 'col1 = 100 and col2 = ''A''' )`

## Examples

Calculate the clustering depth for a table using the clustering key defined for the table:

> Copy code
>
> ```
> SELECT SYSTEM$CLUSTERING_DEPTH('TPCH_ORDERS');
>
> +----------------------------------------+
> | SYSTEM$CLUSTERING_DEPTH('TPCH_ORDERS') |
> |----------------------------------------+
> | 2.4865                                 |
> +----------------------------------------+
> ```

Calculate the clustering depth for a table using two columns in the table:

> Copy code
>
> ```
> SELECT SYSTEM$CLUSTERING_DEPTH('TPCH_ORDERS', '(C2, C9)');
>
> +----------------------------------------------------+
> | SYSTEM$CLUSTERING_DEPTH('TPCH_ORDERS', '(C2, C9)') |
> +----------------------------------------------------+
> | 23.1351                                            |
> +----------------------------------------------------+
> ```

Same as the previous example, but with a predicate on one of the columns:

> Copy code
>
> ```
> SELECT SYSTEM$CLUSTERING_DEPTH('TPCH_ORDERS', '(C2, C9)', 'C2 = 25');
>
> +----------------------------------------------------+
> | SYSTEM$CLUSTERING_DEPTH('TPCH_ORDERS', '(C2, C9)') |
> +----------------------------------------------------+
> | 11.2452                                            |
> +----------------------------------------------------+
> ```
