# Data governance policy inheritance for Cortex Search

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

By default, a Cortex Search service runs with the service owner’s rights. This is standard Snowflake behavior: the service’s index is built and served under the permissions of whoever created it. The consequence is that [row access policies](/user-guide/security-row-intro) and [masking policies](/user-guide/security-column-intro) already applied to the base table don’t take effect at query time. Every caller sees results as the service owner would, regardless of their own access level.

Data governance policy inheritance solves this. When enabled, a Cortex Search service honors the row access policies and masking policies on its base table, so query results reflect the querying user’s own access. Row access policies filter out rows the querying user isn’t permitted to see, and masking policies apply to the returned columns. If a column that the service searches or filters on is masked, results that matched on it are dropped or the query is rejected. For details, see [Masking policy considerations](#masking-policy-considerations).

## Requirements

- `INHERIT_DATA_GOVERNANCE_POLICIES = TRUE` must be set on the service.
- A primary key column must be declared on the service (for example, `PRIMARY KEY id`). The primary key serves as the join key: after the index returns candidate matches, the service re-fetches those rows from the base table using the primary key under the caller’s session context, which is how row access policies and masking policies get enforced per caller.
- The service owner role must have access to every base table row that you want to include in the index. The service builds and refreshes its index with the owner’s rights, so the base table’s row access policies also apply when the index is built. Rows that the owner role can’t see are left out of the index, and no caller can retrieve them, even a caller whose own roles grant access to those rows. Make sure your row access policies allow the owner role to see these rows (for example, with an `IS_ROLE_IN_SESSION` exception for the owner role), and use a dedicated, tightly controlled role as the service owner.
- Queries must use the [CORTEX\_SEARCH\_BATCH](/user-guide/snowflake-cortex/cortex-search/batch-cortex-search) or [CORTEX\_SEARCH\_RETRIEVE](/user-guide/snowflake-cortex/cortex-search/cortex-search-retrieve) SQL functions. Only these SQL functions enforce inherited policies. The REST API, the Python API, and the `SEARCH_PREVIEW` function are blocked for a governance-enabled service.

Note

Both SQL functions enforce inherited policies. Choose between them based on your workload:

- Use [CORTEX\_SEARCH\_RETRIEVE](/user-guide/snowflake-cortex/cortex-search/cortex-search-retrieve) for low-latency, real-time queries that run one or a few queries at a time, such as retrieval-augmented generation, chatbots, and in-app search.
- Use [CORTEX\_SEARCH\_BATCH](/user-guide/snowflake-cortex/cortex-search/batch-cortex-search) for high-throughput, offline workloads that submit many queries at once, such as entity resolution, deduplication, or clustering.

## Usage

1. **Add a row access policy to the base table.** In this example, `search_owner_role` is the role that creates and owns the Cortex Search service. The policy grants that role access to all rows so that the service can index them:

   Copy code

   ```
   CREATE ROW ACCESS POLICY rap_policy
     AS (category VARCHAR) RETURNS BOOLEAN ->
       CASE
         WHEN IS_ROLE_IN_SESSION('SEARCH_OWNER_ROLE') THEN TRUE
         WHEN IS_ROLE_IN_SESSION('ADMIN') THEN TRUE
         WHEN category = 'PUBLIC' THEN TRUE
         ELSE FALSE
       END;

   ALTER TABLE my_table ADD ROW ACCESS POLICY rap_policy ON (category);
   ```
2. **Add a masking policy to a base column.** The masked column shouldn’t be a search column or a column that queries filter on. For details, see [Masking policy considerations](#masking-policy-considerations). This policy returns the `author` value to sessions that include the `ADMIN` role and masks it for everyone else:

   Copy code

   ```
   CREATE MASKING POLICY author_mask AS (val VARCHAR) RETURNS VARCHAR ->
     CASE
       WHEN IS_ROLE_IN_SESSION('ADMIN') THEN val
       ELSE '***MASKED***'
     END;

   ALTER TABLE my_table MODIFY COLUMN author SET MASKING POLICY author_mask;
   ```
3. **Create the Cortex Search service with governance inheritance enabled, using the owner role:**

   Copy code

   ```
   USE ROLE search_owner_role;

   CREATE CORTEX SEARCH SERVICE my_service
     ON content
     PRIMARY KEY id
     ATTRIBUTES category, author
     WAREHOUSE = my_wh
     TARGET_LAG = '1 hour'
     INHERIT_DATA_GOVERNANCE_POLICIES = TRUE
     AS (SELECT id, content, category, author FROM my_table);
   ```
4. **Query the service.** Row access policies filter the results to the rows that the querying user’s session roles are allowed to see, and masking policies apply to the returned columns. A session without the `ADMIN` role sees only `PUBLIC` rows, with the `author` column masked:

   Copy code

   ```
   SELECT cs.id, cs.content, cs.category, cs.author
   FROM TABLE(CORTEX_SEARCH_RETRIEVE(
       service_name => 'my_service',
       query => 'hello',
       limit => 10
   )) cs;
   ```

   Copy code

   ```
   +----+--------------------------+----------+--------------+
   | ID | CONTENT                  | CATEGORY | AUTHOR       |
   |----+--------------------------+----------+--------------|
   |  1 | hello from the docs team | PUBLIC   | ***MASKED*** |
   +----+--------------------------+----------+--------------+
   ```

   A session that includes the `ADMIN` role sees all matching rows with the `author` column unmasked.

## Performance

For a governed service, each query joins the search results back to the service’s source query to apply policies, so the source query runs again on every query. A complex source query can make queries much slower than on an equivalent ungoverned service.

To keep queries fast:

- **Keep the source query simple.** Select from a single table where you can. Each join, filter, and computed column in the source query, including inside any view it reads, adds work to every query.
- **Size the warehouse.** Both `CORTEX_SEARCH_BATCH` and `CORTEX_SEARCH_RETRIEVE` require an active warehouse. Because the row access policies and masking policies are enforced through the warehouse, a larger warehouse can reduce query latency. Choose a warehouse size that meets your latency requirements.

As a starting point, size the warehouse to the base table’s row count:

| Base table size | Recommended warehouse |
| --- | --- |
| Fewer than 10M rows | `XSMALL` |
| 10M to 100M rows | `SMALL` or `MEDIUM` |
| 100M to 500M rows | `LARGE` |
| More than 500M rows | `XLARGE` or larger |

Expand

Show lessSee more

## Limitations

- **Masking policies on primary key columns aren’t supported.** Don’t apply a masking policy to a column that’s used as the service’s primary key. This isn’t currently blocked by the system, so applying one can produce incorrect results.
- **The `limit` table-function argument must be a literal integer.** This applies to the `limit` argument passed to `CORTEX_SEARCH_RETRIEVE` or `CORTEX_SEARCH_BATCH`, not to a SQL `LIMIT` clause on the surrounding query. For example, `limit => 10` works, but a parameterized or computed value such as `limit => :my_var` does not. This is because the service needs to know the candidate count upfront in order to fetch the right number of results before the row access policy filters are applied.
- **Recall may be imperfect.** Because row access policies filter results after retrieval, and hits that match on a column with a masking policy are dropped, a governed service may return fewer results than an equivalent ungoverned service. For details, see [Masking policy considerations](#masking-policy-considerations).
- **Rows changed since the last refresh can be dropped.** For a search column that has a masking policy, a row that changed since the last index refresh isn’t returned, even to roles that see the unmasked value.
- **The operator and column names in the `filter` argument must be written in the query.** Only filter values can come from per-row data. For details, see [Filters must name their columns](#filters-must-name-their-columns).
- **Source queries that use a masked column to choose rows are rejected.** For details, see [Source queries that use masked columns to choose rows](#source-queries-that-use-masked-columns-to-choose-rows).

### Filters must name their columns

Snowflake must know which columns a filter references when it compiles the query, before it reads any rows, so that it can reject filters on masked columns. A filter has three parts:

Copy code

```
{'@eq': {'category': 'PUBLIC'}}
   │         │          │
operator  column name  value
```

The operator and column name must be written in the query. The value can come from per-row data, for example from the input table of a `CORTEX_SEARCH_BATCH` query:

| Filter | Columns known at compile time? | Result |
| --- | --- | --- |
| `{'@eq': {'category': 'PUBLIC'}}` | Yes | Allowed |
| `{'@eq': {'category': q.category}}` | Yes. Only the value varies per row. | Allowed |
| `NULL` | No filter | Allowed |
| `q.filter` | No. Each row can reference different columns. | Rejected |
| `{'@eq': q.obj}` | No. The column name is inside `q.obj`. | Rejected |

Expand

Show lessSee more

### Source queries that use masked columns to choose rows

If `INHERIT_DATA_GOVERNANCE_POLICIES` is enabled and the service’s source query uses a masked column to choose rows, **every query to the service is rejected, for every role**, including roles that see the real value.

A source query that uses a masked column to decide which rows it returns can leak the masked value through the set of rows that the service indexes. Masking policies are evaluated for each caller at query time, so the service can’t serve some roles and not others, and rejects every query.

For example, the following source query leaks information:

Copy code

```
Source query:   SELECT ... FROM employees WHERE salary > 100000
Masking policy: salary is masked for the HR_VIEWER role

HR_VIEWER searches the service and sees Alice in the results, with salary = ***MASKED***.
But only employees with salary > 100000 were indexed, so HR_VIEWER learns Alice's salary is above 100000.
```

A source query uses a masked column to choose rows when the column appears in `WHERE`, `JOIN ... ON`, `GROUP BY`, `HAVING`, `QUALIFY`, or `DISTINCT`, including inside any view, CTE, or derived table that the source query reads. To avoid the rejection, choose rows only by unmasked columns.

### Masking policy considerations

Masking policies need extra care because the service matches your query against an index that holds unmasked values, and the policies are applied only when the service returns each hit. If the service returned a hit that matched on a masked value, the caller could learn the hidden value even though the value in the result is masked. For example, a caller who sees `body` as `***MASKED***` and searches for `refund` would learn that ticket 42 mentions refunds.

The following rules apply to `CORTEX_SEARCH_BATCH` and `CORTEX_SEARCH_RETRIEVE` queries, whether you set the masking policy directly or through a tag.

To prevent this, the service handles each column that a query can match on as follows:

| If this column is masked for the caller | What happens |
| --- | --- |
| A search column (`ON` or a `TEXT INDEXES` column), or the text column that an auto-embedded vector index is built from | Hits that matched on it are dropped silently, unless the value that the masking policy returns for the caller equals the indexed value (for example, the policy returns the original value for the caller’s role). The caller can get fewer results, or none. |
| A user-provided `VECTOR` column, or a column the service matches on but doesn’t return in the results (for example, a `TEXT INDEXES` column that isn’t returned) | The query is rejected. |
| An attribute column that the `filter` argument references | The query is rejected. Otherwise, a filter such as `{'@eq': {'author': 'Bob'}}` would reveal which rows Bob wrote. |
| An attribute column that the `filter` argument doesn’t reference | No change. The value is masked in results as usual. |

Expand

Show lessSee more

For a search column that has a masking policy, a row that changed since the last index refresh is also dropped, even for roles that see the unmasked value. This applies to every role.
