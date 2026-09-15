Categories:
:   [Query syntax](/sql-reference/constructs)

# TOP *<n>*

Constrains the maximum number of rows returned by a statement or subquery.

See also:
:   [LIMIT / FETCH](/sql-reference/constructs/limit)

## Syntax

Copy code

```
SELECT
  [ TOP <n> ]
    ...
FROM ...
[ ORDER BY ... ]
[ ... ]
```

## Parameters

`n`
:   The maximum number of rows to return in the result set.

## Usage notes

- An [ORDER BY](/sql-reference/constructs/order-by) clause is not required; however, without an [ORDER BY](/sql-reference/constructs/order-by) clause, the results are non-deterministic because results within a result set are not necessarily in any particular order. To control the results returned, use an [ORDER BY](/sql-reference/constructs/order-by) clause.
- When TOP *<n>* and ORDER BY are at different nesting levels in a query, results can be unpredictable.
  For details and examples, see the [LIMIT / FETCH usage notes](/sql-reference/constructs/limit#label-limit-cmd-usage-notes).
- `n` must be a non-negative integer constant.
- TOP `n` and LIMIT `count` are equivalent.

## Examples

The following example shows the effect of TOP N. For simplicity, these
queries omit the ORDER BY clause and assume that the output order is
always the same as shown by the first query. **Real-world queries should
include an ORDER BY clause.**

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
SELECT TOP 4 c1 FROM testtable;
```

```
+----+
| C1 |
|----|
|  1 |
|  2 |
|  3 |
| 20 |
+----+
```
