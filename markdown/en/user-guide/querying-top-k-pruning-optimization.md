# Top-K pruning for improved query performance

If a SELECT statement contains [LIMIT](/sql-reference/constructs/limit) and [ORDER BY](/sql-reference/constructs/order-by)
clauses, Snowflake ordinarily scans all eligible rows because any row might be part of the top-K results, where K
is the value from the LIMIT clause. With top-K pruning, Snowflake stops scanning when it determines that none of
the remaining rows can be in a result set that consists of K records.

Top-K pruning can improve the performance of SELECT statements that contain LIMIT and ORDER BY clauses. Queries on large
tables benefit the most from top-K pruning.

## Queries that use top-K pruning

Snowflake applies top-K pruning only when all of the following are true:

- The query contains both an ORDER BY clause and a LIMIT clause.
- The first column specified in the ORDER BY clause has one of the following data types:

  - An integer-representable data type (that is, an [INTEGER type](/sql-reference/data-types-numeric#label-data-type-integer), a [DATE type](/sql-reference/data-types-datetime#label-datatypes-date),
    or a [TIMESTAMP type](/sql-reference/data-types-datetime#label-datatypes-timestamp)). Expressions that return integers, such as casts, are not supported.
  - A [string or binary data type](/sql-reference/data-types-text), including [collated strings](/sql-reference/collation).
  - A field in a [VARIANT](/sql-reference/data-types-semistructured) column with a supported underlying type (that is, a type listed
    in the previous two bulleted list items) and cast to that underlying type.

  If multiple columns are specified, Snowflake considers only the first column.
- When the query contains a join, the ORDER BY column is a column from the larger table. In data warehousing, the
  larger table is often referred to as the [fact table](https://en.wikipedia.org/wiki/Fact_table) or probe side. The smaller table is referred to as the [dimension table](https://en.wikipedia.org/wiki/Dimension_%28data_warehouse%29#Dimension_table).

Queries with LIMIT clauses that are already fast (such as queries in which a full table scan is fast) might not benefit
from top-K pruning. Queries that return fewer than K rows also don’t benefit.

Queries that contain [ORDER BY](/sql-reference/constructs/order-by) … DESCENDING on a nullable field are pruned only if
they also specify NULLS LAST.

## Queries on VARIANT columns

This section provides examples of queries on a field in a VARIANT column to show the types of queries that can use top-K
pruning.

Create a table with a VARIANT column and insert data:

Copy code

```
CREATE OR REPLACE TABLE variant_topk_test (var_col VARIANT);

INSERT INTO variant_topk_test
  SELECT PARSE_JSON(column1)
    FROM VALUES
      ('{"s": "aa", "i": 1}'),
      ('{"s": "bb", "i": 2}'),
      ('{"s": "cc", "i": 3}'),
      ('{"s": "dd", "i": 4}'),
      ('{"s": "ee", "i": 5}'),
      ('{"s": "ff", "i": 6}'),
      ('{"s": "gg", "i": 7}'),
      ('{"s": "hh", "i": 8}'),
      ('{"s": "ii", "i": 9}'),
      ('{"s": "jj", "i": 10}');
```

This table is relatively small to provide an example, but remember that top-K pruning benefits larger tables.

The following queries on this table can use top-K pruning:

Copy code

```
SELECT * FROM variant_topk_test ORDER BY TO_VARCHAR(var_col:s) LIMIT 5;
```

Copy code

```
SELECT * FROM variant_topk_test ORDER BY var_col:s::VARCHAR LIMIT 5;
```

Copy code

```
SELECT * FROM variant_topk_test ORDER BY TO_NUMBER(var_col:i) LIMIT 5;
```

Copy code

```
SELECT * FROM variant_topk_test ORDER BY var_col:i::NUMBER LIMIT 5;
```

The following query can’t use top-K pruning because the value isn’t cast to the underlying data type:

Copy code

```
SELECT * FROM variant_topk_test ORDER BY var_col:s LIMIT 5;
```

The following query can’t use top-K pruning because the value is cast to a data type that is different from
the underlying data type:

Copy code

```
SELECT * FROM variant_topk_test ORDER BY var_col:i::VARCHAR LIMIT 5;
```

## Queries that contain an aggregate function

Queries that contain an [aggregate function](/sql-reference/functions-aggregation) are pruned only if they
meet all of the following conditions:

- They include a [GROUP BY](/sql-reference/constructs/group-by) clause.
- The first ORDER BY column is also a GROUP BY column.

For example, the following query can use top-K pruning because the first ORDER BY column `c2` is also a GROUP BY
column and isn’t an aggregated column:

Copy code

```
SELECT c1, c2, c3, COUNT(*) AS agg_col
  FROM mytable
  GROUP BY c1, c2, c3
  ORDER BY c2, c1, agg_col, c3
  LIMIT 5;
```

The following query can’t use top-K pruning because the first ORDER BY column `agg_col` is an aggregated column:

Copy code

```
SELECT c1, c2, c3, COUNT(*) AS agg_col
  FROM mytable
  GROUP BY c1, c2, c3
  ORDER BY agg_col, c2, c1
  LIMIT 5;
```
