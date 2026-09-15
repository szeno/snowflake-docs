Categories:
:   [Query syntax](/sql-reference/constructs)

# QUALIFY

In a SELECT statement, the QUALIFY clause filters the results of window functions.

QUALIFY does with window functions what HAVING does with aggregate functions and GROUP BY clauses.

In the execution order of a query, QUALIFY is therefore evaluated after window functions are computed. Typically,
a SELECT statement’s clauses are evaluated in the order shown below:

> 1. FROM
> 2. WHERE
> 3. GROUP BY
> 4. HAVING
> 5. WINDOW
> 6. QUALIFY
> 7. DISTINCT
> 8. ORDER BY
> 9. LIMIT

## Syntax

Copy code

```
QUALIFY <predicate>
```

The general form of a statement with QUALIFY is similar to the following
(some variations in order are allowed, but are not shown):

Copy code

```
SELECT <column_list>
  FROM <data_source>
  [GROUP BY ...]
  [HAVING ...]
  QUALIFY <predicate>
  [ ... ]
```

## Parameters

`column_list`
:   This generally follows the rules for the projection clause of a [SELECT](/sql-reference/sql/select) statement.

`data_source`
:   The data source is usually a table, but can be another table-like data source, such as a view, UDTF (user-defined table function),
    etc.

`predicate`
:   The predicate is an expression that filters the result after aggregates and window functions are computed.
    The predicate should look similar to a [HAVING](/sql-reference/constructs/having) clause, but without the
    keyword HAVING. In addition, the predicate can also contain window functions.

    See the [Examples](#examples) section (in this topic) for predicate examples.

## Usage notes

- The QUALIFY clause requires at least one window function to be specified in at least one of the following clauses
  of the SELECT statement:

  - The SELECT column list.
  - The filter predicate of the QUALIFY clause.

  Examples of each of these are shown in the Examples section below.
- Expressions in the SELECT list, including window functions, can be referred to by the column alias defined in the
  SELECT list.
- QUALIFY supports aggregates and subqueries in the predicate. For aggregates, the same rules as for the HAVING clause
  apply.
- The word QUALIFY is a reserved word.
- The Snowflake syntax for QUALIFY is not part of the ANSI standard.

## Examples

The QUALIFY clause simplifies queries that require filtering on the result of window functions. Without QUALIFY,
filtering requires nesting. The example below uses the ROW\_NUMBER() function to return only the first row in each
partition.

Create and load a table:

Copy code

```
CREATE TABLE qt (i INTEGER, p CHAR(1), o INTEGER);
INSERT INTO qt (i, p, o) VALUES
  (1, 'A', 1),
  (2, 'A', 2),
  (3, 'B', 1),
  (4, 'B', 2);
```

```
+-------------------------+
| number of rows inserted |
|-------------------------|
|                       4 |
+-------------------------+
```

This query uses nesting rather than QUALIFY:

Copy code

```
SELECT *
  FROM (
    SELECT i, p, o, ROW_NUMBER() OVER (PARTITION BY p ORDER BY o) AS row_num
      FROM qt)
  WHERE row_num = 1;
```

```
+---+---+---+---------+
| I | P | O | ROW_NUM |
|---+---+---+---------|
| 1 | A | 1 |       1 |
| 3 | B | 1 |       1 |
+---+---+---+---------+
```

This query uses QUALIFY:

Copy code

```
SELECT i, p, o
  FROM qt
  QUALIFY ROW_NUMBER() OVER (PARTITION BY p ORDER BY o) = 1;
```

```
+---+---+---+
| I | P | O |
|---+---+---|
| 1 | A | 1 |
| 3 | B | 1 |
+---+---+---+
```

You can also use QUALIFY to reference window functions that are in the SELECT column list:

Copy code

```
SELECT i, p, o, ROW_NUMBER() OVER (PARTITION BY p ORDER BY o) AS row_num
  FROM qt
  QUALIFY row_num = 1;
```

```
+---+---+---+---------+
| I | P | O | ROW_NUM |
|---+---+---+---------|
| 1 | A | 1 |       1 |
| 3 | B | 1 |       1 |
+---+---+---+---------+
```

You can see how QUALIFY acts as a filter by removing it from the previous query and comparing the output:

Copy code

```
SELECT i, p, o, ROW_NUMBER() OVER (PARTITION BY p ORDER BY o) AS row_num
  FROM qt;
```

```
+---+---+---+---------+
| I | P | O | ROW_NUM |
|---+---+---+---------|
| 1 | A | 1 |       1 |
| 2 | A | 2 |       2 |
| 3 | B | 1 |       1 |
| 4 | B | 2 |       2 |
+---+---+---+---------+
```

The QUALIFY clause can also be combined with aggregate functions and subqueries in the predicate. In such a query,
HAVING filters rows after GROUP BY aggregation, while QUALIFY filters rows after window functions are computed.
Both clauses can appear together when a query requires both kinds of filtering. For example:

Copy code

```
SELECT p, SUM(o) OVER (PARTITION BY p) AS r
  FROM qt
  WHERE o < 4
  GROUP BY p, o
  HAVING SUM(i) > 3
  QUALIFY r IN (
    SELECT MIN(i)
      FROM qt
      GROUP BY p
      HAVING MIN(i) > 3);
```
