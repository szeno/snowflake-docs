Categories:
:   [Query syntax](/sql-reference/constructs)

# ORDER BY

Specifies an ordering of the rows of the result table from a [SELECT](/sql-reference/sql/select) list.

## Syntax

**Sorting by specific columns**

Copy code

```
SELECT ...
  FROM ...
  ORDER BY orderItem [ , orderItem , ... ]
  [ ... ]
```

Where:

Copy code

```
orderItem ::= { <column_alias> | <position> | <expr> } [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ]
```

**Sorting by all columns**

Copy code

```
SELECT ...
  FROM ...
  ORDER BY ALL [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ]
  [ ... ]
```

## Parameters

`column_alias`
:   Column alias appearing in the query block’s [SELECT](/sql-reference/sql/select) list.

`position`
:   Position of an expression in the [SELECT](/sql-reference/sql/select) list.

`expr`
:   Any expression on tables in the current scope.

`{ ASC | DESC }`
:   Optionally returns the values of the sort key in ascending (lowest to highest) or descending (highest to lowest) order.

    Default: ASC

`NULLS { FIRST | LAST }`
:   Optionally specifies whether NULL values are returned before/after non-NULL values, based on the sort order (ASC or DESC).

    Default: Depends on the sort order (ASC or DESC); see the usage notes below for details

`ALL`
:   Sorts the results by all of the columns specified in the SELECT list. The results are sorted by the columns in the order in
    which they appear.

    For example, suppose that the SELECT list contains:

    Copy code

    ```
    SELECT col_1, col_2, col_3
      FROM my_table
      ORDER BY ALL;
    ```

    The results are sorted first by `col_1`, then by `col_2`, and then by `col_3`.

    Note

    You cannot specify ORDER BY ALL if a column in the SELECT list uses an aggregate function.

## Usage notes

- All data is sorted according to the numeric byte value of each character in the ASCII table. UTF-8 encoding is supported.
- For numeric values, leading zeros before the decimal point and trailing zeros (`0`) after the decimal point have no effect on sort order.

- When NULLS FIRST or NULLS LAST isn’t specified, the ordering of NULL values depends on the setting of the
  [DEFAULT\_NULL\_ORDERING](/sql-reference/parameters#label-default-null-ordering) parameter and the sort order:

  - When the sort order is ASC (the default) and the DEFAULT\_NULL\_ORDERING parameter is set to `LAST`
    (the default), NULL values are returned last. Therefore, unless specified otherwise, NULL values are considered to be higher than
    any non-NULL values.
  - When the sort order is ASC and the DEFAULT\_NULL\_ORDERING parameter is set to `FIRST`, NULL values are returned first.
  - When the sort order is DESC and the DEFAULT\_NULL\_ORDERING parameter is set to `FIRST`, NULL values are returned last.
  - When the sort order is DESC and the DEFAULT\_NULL\_ORDERING parameter is set to `LAST`, NULL values are returned first.
- The sort order isn’t guaranteed to be consistent for values of different data types in
  [semi-structured](/sql-reference/data-types-semistructured) data, such as an array that contains elements of
  different data types.
- Top-K pruning can improve the performance of queries that include both [LIMIT](/sql-reference/constructs/limit) and ORDER BY clauses. For more
  information, see [Top-K pruning for improved query performance](/user-guide/querying-top-k-pruning-optimization).
- An ORDER BY clause can be used at different levels in a query, such as in a subquery or inside an OVER() clause for a window function.
  An ORDER BY clause inside a subquery or an OVER() clause applies only in that context. For example, the ORDER BY clause
  in the following query orders results only within the subquery, not the outermost level of the query:

  Copy code

  ```
  SELECT *
    FROM (
   SELECT branch_name
     FROM branch_offices
     ORDER BY monthly_sales DESC
     LIMIT 3
    );
  ```

  In this example, the ORDER BY clause is specified in the subquery, so the subquery returns the names in order of monthly
  sales. The ORDER BY clause in the subquery does not apply to the outer query. This query returns the names of the three
  branches that had the highest monthly sales, but not necessarily in order by monthly sales.

  Sorting can be expensive. If you want the results of the outer query sorted, use an ORDER BY clause only at the
  top level of the query, and avoid using ORDER BY clauses in subqueries unless necessary.

  Similarly, when ORDER BY and [LIMIT](/sql-reference/constructs/limit) (or FETCH) clauses are at different nesting levels, results
  can be unpredictable. For details and examples, see the [LIMIT / FETCH usage notes](/sql-reference/constructs/limit#label-limit-cmd-usage-notes).

## Examples

The following examples demonstrate how to use ORDER BY to sort the results:

- [Sorting by string values](#label-order-by-examples-strings)
- [Sorting by numeric values](#label-order-by-examples-numbers)
- [Sorting NULLS first or last](#label-order-by-examples-nulls)

### Sorting by string values

The following example sorts the results by string values:

Copy code

```
SELECT column1
  FROM VALUES
    ('a'), ('1'), ('B'), (null), ('2'), ('01'), ('05'),
    (' this'), ('this'), ('this and that'), ('&'), ('%')
  ORDER BY column1;
```

```
+---------------+
| COLUMN1       |
|---------------|
|  this         |
| %             |
| &             |
| 01            |
| 05            |
| 1             |
| 2             |
| B             |
| a             |
| this          |
| this and that |
| NULL          |
+---------------+
```

### Sorting by numeric values

The following example sorts the results by numeric values:

Copy code

```
SELECT column1
  FROM VALUES
    (3), (4), (null), (1), (2), (6),
    (5), (0005), (.05), (.5), (.5000)
  ORDER BY column1;
```

```
+---------+
| COLUMN1 |
|---------|
|    0.05 |
|    0.50 |
|    0.50 |
|    1.00 |
|    2.00 |
|    3.00 |
|    4.00 |
|    5.00 |
|    5.00 |
|    6.00 |
|    NULL |
+---------+
```

### Sorting NULLS first or last

The following example configures all queries in the session to sort NULLS last by setting the [DEFAULT\_NULL\_ORDERING](/sql-reference/parameters#label-default-null-ordering)
parameter to `LAST`.

Copy code

```
ALTER SESSION SET DEFAULT_NULL_ORDERING = 'LAST';
```

Copy code

```
SELECT column1
  FROM VALUES (1), (null), (2), (null), (3)
  ORDER BY column1;
```

```
+---------+
| COLUMN1 |
|---------|
|       1 |
|       2 |
|       3 |
|    NULL |
|    NULL |
+---------+
```

Copy code

```
SELECT column1
  FROM VALUES (1), (null), (2), (null), (3)
  ORDER BY column1 DESC;
```

```
+---------+
| COLUMN1 |
|---------|
|    NULL |
|    NULL |
|       3 |
|       2 |
|       1 |
+---------+
```

The following example overrides the DEFAULT\_NULL\_ORDERING parameter by specifying NULLS FIRST in a query:

Copy code

```
SELECT column1
  FROM VALUES (1), (null), (2), (null), (3)
  ORDER BY column1 NULLS FIRST;
```

```
+---------+
| COLUMN1 |
|---------|
|    NULL |
|    NULL |
|       1 |
|       2 |
|       3 |
+---------+
```

The following example sets the DEFAULT\_NULL\_ORDERING parameter to `FIRST` to sort NULLS first:

Copy code

```
ALTER SESSION SET DEFAULT_NULL_ORDERING = 'FIRST';

SELECT column1
  FROM VALUES (1), (null), (2), (null), (3)
  ORDER BY column1;
```

```
+---------+
| COLUMN1 |
|---------|
|    NULL |
|    NULL |
|       1 |
|       2 |
|       3 |
+---------+
```

Copy code

```
SELECT column1
  FROM VALUES (1), (null), (2), (null), (3)
  ORDER BY column1 DESC;
```

```
+---------+
| COLUMN1 |
|---------|
|       3 |
|       2 |
|       1 |
|    NULL |
|    NULL |
+---------+
```

The following example overrides the DEFAULT\_NULL\_ORDERING parameter by specifying NULLS LAST in a query:

Copy code

```
SELECT column1
  FROM VALUES (1), (null), (2), (null), (3)
  ORDER BY column1 NULLS LAST;
```

```
+---------+
| COLUMN1 |
|---------|
|       1 |
|       2 |
|       3 |
|    NULL |
|    NULL |
+---------+
```

### Sorting by all columns in the SELECT list

To run the examples in this section, create the following table:

Copy code

```
CREATE OR REPLACE TABLE my_sort_example(a NUMBER, s VARCHAR, b BOOLEAN);

INSERT INTO my_sort_example VALUES
  (0, 'abc', TRUE),
  (0, 'abc', FALSE),
  (0, 'abc', NULL),
  (0, 'xyz', FALSE),
  (0, NULL, FALSE),
  (1, 'xyz', TRUE),
  (NULL, 'xyz', FALSE);
```

The following example sorts the results by all columns in the table:

Copy code

```
SELECT * FROM my_sort_example
  ORDER BY ALL;
```

As shown below, the results are sorted first by the `a` column, then by the `s` column, and then by the `b` column (the
order in which the columns were defined in the table).

```
+------+------+-------+
| A    | S    | B     |
|------+------+-------|
| 0    | abc  | False |
| 0    | abc  | True  |
| 0    | abc  | NULL  |
| 0    | xyz  | False |
| 0    | NULL | False |
| 1    | xyz  | True  |
| NULL | xyz  | False |
+------+------+-------+
```

The following example sorts the results in ascending order:

Copy code

```
SELECT * FROM my_sort_example
  ORDER BY ALL ASC;
```

```
+------+------+-------+
| A    | S    | B     |
|------+------+-------|
| 0    | abc  | False |
| 0    | abc  | True  |
| 0    | abc  | NULL  |
| 0    | xyz  | False |
| 0    | NULL | False |
| 1    | xyz  | True  |
| NULL | xyz  | False |
+------+------+-------+
```

The following example sets the DEFAULT\_NULL\_ORDERING parameter to sort NULL values last for all queries executed during the
session:

Copy code

```
ALTER SESSION SET DEFAULT_NULL_ORDERING = 'LAST';

SELECT * FROM my_sort_example
  ORDER BY ALL;
```

```
+------+------+-------+
| A    | S    | B     |
|------+------+-------|
| NULL | xyz  | False |
| 0    | NULL | False |
| 0    | abc  | NULL  |
| 0    | abc  | False |
| 0    | abc  | True  |
| 0    | xyz  | False |
| 1    | xyz  | True  |
+------+------+-------+
```

The following example specifies NULLS FIRST in a query to override that setting:

Copy code

```
SELECT * FROM my_sort_example
  ORDER BY ALL NULLS FIRST;
```

```
+------+------+-------+
| A    | S    | B     |
|------+------+-------|
| NULL | xyz  | False |
| 0    | NULL | False |
| 0    | abc  | NULL  |
| 0    | abc  | False |
| 0    | abc  | True  |
| 0    | xyz  | False |
| 1    | xyz  | True  |
+------+------+-------+
```

The following example returns the columns in the order `b`, `s`, and `a`. The results are sorted first by `b`, then by
`s`, and then by `a`:

Copy code

```
SELECT b, s, a FROM my_sort_example
  ORDER BY ALL NULLS LAST;
```

```
+-------+------+------+
| B     | S    | A    |
|-------+------+------|
| False | abc  | 0    |
| False | xyz  | 0    |
| False | xyz  | NULL |
| False | NULL | 0    |
| True  | abc  | 0    |
| True  | xyz  | 1    |
| NULL  | abc  | 0    |
+-------+------+------+
```
