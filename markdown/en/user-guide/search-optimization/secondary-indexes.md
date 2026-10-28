# Secondary indexes

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Secondary indexes speed up highly selective point lookups and range queries on columns or expressions.
A secondary index maps those values to the micro-partitions that contain them, so Snowflake can skip
data that the query doesn’t need.

These indexes are part of the [search optimization service](/user-guide/search-optimization-service).
They aren’t [secondary indexes on hybrid tables](/user-guide/tables-hybrid-index). Hybrid table index
maintenance doesn’t appear in search optimization history.

## Overview

A clustering key organizes a table for one access pattern. You can create more than one secondary index
on the same table, so you can support additional access patterns that you don’t want to use as the
clustering key.

Each index has two parts:

- **Key expressions.** An ordered list of columns or deterministic scalar expressions. Snowflake uses
  this order when it prunes micro-partitions for multi-column predicates. The order is significant:
  earlier expressions are generally more effective at pruning than later expressions.
- **Included expressions.** An optional set of expressions stored with the index. These expressions don’t
  prune the index. They let some queries read the result from the index without reading the base table.
  An index that can satisfy a query this way is a covering index.

You can create a secondary index on a standard table. Views and materialized views
aren’t supported. Snowflake maintains the index automatically. Dropping the base table drops its
secondary indexes.

Note

Secondary indexes aren’t supported on [Iceberg tables](/user-guide/tables-iceberg).

## Comparison with search optimization and clustering

Secondary indexes, the search optimization service, and Automatic Clustering solve different parts of
the same performance problem. The following table compares them:

| Dimension | Secondary index | Search optimization index | Automatic Clustering |
| --- | --- | --- | --- |
| Predicate support | Equality, inequality, range, and IN lists. | High-cardinality lookups that use equality, IN lists, and functions such as LIKE, ILIKE, RLIKE, SUBSTRING, UPPER, LOWER, geospatial functions, and SEARCH. | Range and equality pruning on the clustered table. |
| Expression support | Columns and deterministic scalar expressions, including casts. | Columns only. | Columns and expressions in the clustering key. |
| Serves results directly | Yes, when the query can be satisfied from the index key and INCLUDE expressions. That index is a covering index. | No. The query still reads the base table. | Yes. Clustering organizes the base table. There is no separate index. |
| Billing | Search optimization service. | Search optimization service. | Automatic Clustering. |
| Maintenance | Automatic. | Automatic. | Automatic. |

Expand

Show lessSee more

## Query performance

You don’t name a secondary index in the query. The optimizer can rewrite a query against the base table
to use a secondary index.

A secondary index can improve a query in either of these ways:

- **Covering index.** If the index contains every column or expression the query needs from that table,
  the optimizer can return those results from the index and skip the base table. This applies to a query
  on one table, and it can apply to one table in a multi-table join.
- **Pruning.** If the query needs columns that aren’t in the index, the optimizer can still use the index
  to skip micro-partitions in the base table.

The optimizer uses at most one secondary index for a table in a scan. If more than one index could
apply, it chooses the index with the highest expected pruning benefit. It doesn’t combine multiple
secondary indexes on the same table.

The optimizer might not use a secondary index, even when the index could cover the query or improve
pruning. Secondary indexes aren’t used for queries that read a previous version of the table with
Time Travel.

## Access control

To create a secondary index, use a role that has the same privileges required to enable search
optimization on the table:

- OWNERSHIP privilege on the table.
- ADD SEARCH OPTIMIZATION privilege on the schema that contains the table.

For more information, see
[To enable search optimization, use a role that has the necessary privileges,…](/user-guide/search-optimization/enabling#label-access-control-privileges-for-search-optimization).

Only the role that owns the base table, or a role that inherits that owner role, can drop a secondary
index.

## Index creation and removal

Create, replace, and drop a secondary index with CREATE INDEX and DROP INDEX.

### CREATE INDEX

Copy code

```
CREATE [ OR REPLACE ] INDEX [ IF NOT EXISTS ] <index_name>
  ON <table_name> ( <expression> [ , <expression> ... ] )
  [ INCLUDE ( <expression> [ , <expression> ... ] ) ]
```

- `index_name` is unique for the base table. A table can have more than one secondary index if each
  index has a different name.
- `table_name` is the base table. Views, materialized views, and Iceberg tables aren’t supported.
- Each key `expression` is a column or a deterministic scalar expression. The order of the key expressions is significant, with earlier expressions being more effective at pruning than later expressions.
- `INCLUDE` stores extra expressions in the index so a query can use the index as a covering index. Included expressions
  can also be used for pruning, although generally less effective than the key expressions.

The following statement indexes `col1` and `col2`, and stores `col3` and `col4` so a query that needs
only those columns can be served from the index:

Copy code

```
CREATE INDEX my_index
  ON table_a (col1, col2)
  INCLUDE (col3, col4);
```

### DROP INDEX

Copy code

```
DROP INDEX [ IF EXISTS ] <table_name>.<index_name>
```

Copy code

```
DROP INDEX table_a.my_index;
```

## Key selection

- Create a multi-column key, such as `(col1, col2)`, when each column alone isn’t very selective, but
  the combination is. A multi-column primary key is one example.
- Put the column or expression that you filter most selectively in the leftmost position. If queries
  filter `col1` more often than `col2`, define the key as `(col1, col2)`.
- Put a very high-cardinality column last in a composite key.
- Put a column in the key when queries filter on it. Put a column in `INCLUDE` when queries return it.
  In some cases, adding a filter column in `INCLUDE` also improves performance. Adding many included
  columns can increase cost.
- If a filter uses an expression whose minimum and maximum values cannot be derived from the source
  column, index the expression. For example, index `UPPER(string_col)` when queries filter on
  `UPPER(string_col)`.

## Limitations

- Secondary indexes aren’t replicated. This is a temporary limitation.
- A secondary index is dropped if you drop or rename a base table column that the index references, or
  if you change that column’s data type.
- Secondary indexes aren’t allowed on tables or columns that have a
  [row access policy](/user-guide/security-row-intro),
  [masking policy](/user-guide/security-column-ddm-intro),
  [aggregation policy](/user-guide/aggregation-policies), or
  [privacy policy](/sql-reference/sql/create-privacy-policy).
- Secondary indexes aren’t supported on Iceberg tables, views, or materialized views.
- Secondary indexes aren’t used for queries that use Time Travel.
- The optimizer doesn’t combine multiple secondary indexes on the same table in one query. It chooses
  the index with the highest expected pruning benefit.

## Index metadata

Use [SHOW INDEXES](/sql-reference/sql/show-indexes-standard-tables) to list secondary indexes:

Copy code

```
SHOW INDEXES IN TABLE table_a;
```

For the output columns and status values, see
[Output](/sql-reference/sql/show-indexes-standard-tables#label-show-indexes-standard-output).

## Cost

Secondary index maintenance is billed as part of the search optimization service. For credit usage by
index, see the `INDEX_TYPE` column in
[SEARCH\_OPTIMIZATION\_HISTORY view](/sql-reference/account-usage/search_optimization_history). The value
`Secondary Index` identifies one of these indexes. It isn’t a hybrid table secondary index.
