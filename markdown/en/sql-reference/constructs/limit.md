Categories:
:   [Query syntax](/sql-reference/constructs)

# LIMIT / FETCH

Constrains the maximum number of rows returned by a statement or subquery. Both LIMIT (PostgreSQL syntax) and FETCH (ANSI syntax) are supported, and produce the same result.

See also:
:   [TOP <n>](/sql-reference/constructs/top_n)

## Syntax

### PostgreSQL syntax

Copy code

```
SELECT ...
FROM ...
[ ORDER BY ... ]
LIMIT <count> [ OFFSET <start> ]
[ ... ]
```

### ANSI syntax

Copy code

```
SELECT ...
FROM ...
[ ORDER BY ... ]
[ OFFSET <start> ] [ { ROW | ROWS } ] FETCH [ { FIRST | NEXT } ] <count> [ { ROW | ROWS } ] [ ONLY ]
[ ... ]
```

## Parameters

`count`
:   The number of rows returned. Must be a non-negative integer constant.

    The values NULL, empty string (`''`), and `$$$$` are also accepted and are treated as
    “unlimited”; this is useful primarily for connectors and drivers (such as the JDBC driver) if they
    receive an incomplete parameter list when dynamically binding parameters to a statement.

`OFFSET` `start`
:   The row number after which the limited/fetched rows are returned. Must be a non-negative integer constant.

    If `OFFSET` is omitted, the output starts from the first row in the result set.

    The values NULL, empty string (`''`) and `$$$$` are also accepted and are treated as 0
    (i.e. do not skip any rows); this is useful primarily for connectors and drivers (such as the JDBC
    driver) if they receive an incomplete parameter list when dynamically binding parameters to a statement.

`ONLY`
:   Optional keyword that does not affect the output. It is used for emphasis to the
    human reader.

## Usage notes

- An [ORDER BY](/sql-reference/constructs/order-by) clause is not required; however, without an ORDER BY clause, the results are non-deterministic
  because query results are not necessarily in any particular order. To control the results returned, use an ORDER BY clause.
- An ORDER BY clause in a subquery only guarantees ordering within that subquery. The ordering is
  not preserved in outer query levels. When a LIMIT clause depends on an ORDER BY clause from a
  different nesting level, the optimizer might not apply the LIMIT clause as expected, and the
  number of rows returned can differ from the LIMIT value. A COUNT(\*) query on the same subquery
  might also report a different number of rows from the actual number of rows returned.

  For example, in the following query the innermost subquery orders the results, the middle
  subquery limits the output to six rows, and the outer query limits the output to 100 rows. You might expect six rows
  because the inner LIMIT clause is smaller, but because the ORDER BY clause is in a different
  subquery from the LIMIT clause, results are unpredictable and the query might return more or
  fewer than six rows:

  Copy code

  ```
  SELECT *
    FROM (
       SELECT *
         FROM (
                SELECT *
                  FROM my_table
                  ORDER BY col1  -- Ordering: innermost level
              )
         LIMIT 6                 -- LIMIT: middle level
      )
    LIMIT 100;                      -- LIMIT: outermost level
  ```

  To avoid unpredictable results, keep the ORDER BY clause and the LIMIT (or FETCH) clause at the
  same query level:

  Copy code

  ```
  SELECT *
    FROM my_table
    ORDER BY col1
    LIMIT 6;
  ```
- Top-K pruning can improve the performance of queries that include both LIMIT and ORDER BY clauses. For more
  information, see [Top-K pruning for improved query performance](/user-guide/querying-top-k-pruning-optimization).
- TOP `n` and LIMIT `count` are equivalent.
- Both the LIMIT clause and the [SAMPLE](/sql-reference/constructs/sample) clause return a subset of rows from a table. When you use the
  LIMIT clause, Snowflake returns the specified number of rows in the fastest way possible. When you use the SAMPLE
  clause, Snowflake returns rows based on the sampling method specified in the clause.

## Examples

The following examples show the effect of LIMIT. For simplicity, these
queries omit the ORDER BY clause and assume that the output order is
always the same as shown by the first query. **Real-world queries should
include ORDER BY.**

Copy code

```
SELECT c1 FROM testtable;
```

```
+------+
|   C1 |
|------|
|    1 |
|    2 |
|    3 |
|   20 |
|   19 |
|   18 |
|    1 |
|    2 |
|    3 |
|    4 |
| NULL |
|   30 |
| NULL |
+------+
```

Copy code

```
SELECT c1 FROM testtable LIMIT 3 OFFSET 3;
```

```
+----+
| C1 |
|----|
| 20 |
| 19 |
| 18 |
+----+
```

Copy code

```
SELECT c1 FROM testtable ORDER BY c1;
```

```
+------+
|   C1 |
|------|
|    1 |
|    1 |
|    2 |
|    2 |
|    3 |
|    3 |
|    4 |
|   18 |
|   19 |
|   20 |
|   30 |
| NULL |
| NULL |
+------+
```

Copy code

```
SELECT c1 FROM testtable ORDER BY c1 LIMIT 3 OFFSET 3;
```

```
+----+
| ID |
|----|
|  2 |
|  3 |
|  3 |
+----+
```

The following examples demonstrate the use of NULLs to indicate:

- No limit to the number of rows.
- Start at row one (do not skip any rows).

  Copy code

  ```
  CREATE TABLE demo1 (i INTEGER);
  INSERT INTO demo1 (i) VALUES (1), (2);
  ```

  Copy code

  ```
  SELECT * FROM demo1 ORDER BY i LIMIT NULL OFFSET NULL;
  ```

  ```
  +---+
  | I |
  |---|
  | 1 |
  | 2 |
  +---+
  ```

  Copy code

  ```
  SELECT * FROM demo1 ORDER BY i LIMIT '' OFFSET '';
  ```

  ```
  +---+
  | I |
  |---|
  | 1 |
  | 2 |
  +---+
  ```

  Copy code

  ```
  SELECT * FROM demo1 ORDER BY i LIMIT $$$$ OFFSET $$$$;
  ```

  ```
  +---+
  | I |
  |---|
  | 1 |
  | 2 |
  +---+
  ```
