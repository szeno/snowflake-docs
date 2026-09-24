# Supported queries for dynamic tables

This page lists which SQL constructs, functions, and data types are supported in each refresh mode.
Use it before creating dynamic tables to predict whether a
definition qualifies for incremental refresh.

Recently added query support

- **Non-deterministic aggregate functions** (APPROX\_COUNT\_DISTINCT, APPROX\_PERCENTILE, APPROX\_TOP\_K) in the SELECT clause (Sep 2026)
- **VOLATILE scalar UDFs** (Jul 2026)
- **MIN\_BY / MAX\_BY** aggregate and window functions (Mar 2026)
- **Expanded outer join patterns** including self-joins (Apr 2026)
- **Primary key-based incremental refresh** downstream of full-refresh dynamic tables (Apr 2026)
- **UNION** set operator for incremental refresh (Aug 2025)
- **Cortex AI functions** in SELECT clause for incremental refresh (Sep 2025)
- **CURRENT\_TIMESTAMP/DATE/TIME** filtering in WHERE/HAVING/QUALIFY (May 2025)

ADAPTIVE refresh and query support

ADAPTIVE has the same query construct requirements as incremental refresh. For details on ADAPTIVE behavior, see [ADAPTIVE refresh](/user-guide/dynamic-tables/refresh-modes#label-dynamic-tables-refresh-adaptive).

If your definition contains a construct that is not supported for incremental refresh, Snowflake selects a full
refresh instead, which reprocesses all data on every refresh. For cost implications, see
[Understanding costs for dynamic tables](/user-guide/dynamic-tables/cost).

For guidance on how query patterns affect incremental refresh performance, see
[Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization).

## Supported data types

Dynamic tables support all [Snowflake SQL data types](/sql-reference/intro-summary-data-types)
for both incremental and full refresh, except:

- [Structured data types](/sql-reference/data-types-structured) (structured OBJECT, structured ARRAY, and MAP).
  This limitation applies to both incremental and full refresh. Semi-structured types (VARIANT, OBJECT, ARRAY
  without a defined schema) are fully supported.
- Geospatial data types (full refresh only).

## Incremental and full refresh support matrix

The following table shows which SQL constructs are supported in each refresh mode. Where a construct is supported
for incremental refresh with restrictions, the table describes the specific conditions.

| Construct | Incremental refresh | Full refresh |
| --- | --- | --- |
| [WITH](/sql-reference/constructs/with) | Supported when the CTE subquery uses only incrementally supported features.  WITH RECURSIVE is not supported. | Supported |
| [CONNECT BY](/sql-reference/constructs/connect-by) | Not supported | Supported |
| [SELECT](/sql-reference/sql/select) | Supported. Expressions must use deterministic built-in functions and [immutable](/sql-reference/sql/create-function#label-create-function-syntax) [user-defined functions](/developer-guide/udf/udf-overview), except for functions this page lists as supported in the SELECT clause. That includes [non-deterministic aggregate functions](#label-dynamic-tables-supported-nondeterministic-aggregates) such as APPROX\_COUNT\_DISTINCT, APPROX\_PERCENTILE, and APPROX\_TOP\_K, and scalar [VOLATILE](/sql-reference/sql/create-function#label-create-function-syntax) [user-defined functions](/developer-guide/udf/udf-overview). | Supported |
| [DISTINCT](/sql-reference/sql/select) | Supported | Supported |
| [FROM](/sql-reference/constructs/from) | Base tables, views, Snowflake-managed Apache Iceberg™ tables, externally managed Iceberg tables, Delta Direct tables, and other dynamic tables.  Subqueries outside of FROM clauses (for example, WHERE EXISTS) are not supported. | Supported |
| [WHERE](/sql-reference/constructs/where) / [HAVING](/sql-reference/constructs/having) / [QUALIFY](/sql-reference/constructs/qualify) | Filters with the same expressions that are valid in SELECT are supported, except for functions this page lists as supported in the SELECT clause only (for example, APPROX\_COUNT\_DISTINCT, APPROX\_PERCENTILE, APPROX\_TOP\_K, and VOLATILE scalar UDFs).  Filters with the CURRENT\_TIMESTAMP, CURRENT\_TIME, and CURRENT\_DATE functions and their aliases are supported. | Supported.  Filters with the CURRENT\_TIMESTAMP, CURRENT\_TIME, and CURRENT\_DATE functions and their aliases are supported. |
| [GROUP BY](/sql-reference/constructs/group-by) | Supported. GROUP BY ROLLUP, GROUP BY CUBE, and GROUP BY GROUPING SETS are not supported for incremental refresh. | Supported |
| Scalar aggregates | Supported | Supported |
| [INNER JOIN](/sql-reference/constructs/join) | Supported. You can specify any number of tables, and Snowflake tracks changes to all tables in the join. | Supported |
| [CROSS JOIN](/sql-reference/constructs/join) | Supported. You can specify any number of tables, and Snowflake tracks changes to all tables in the join. | Supported |
| [LEFT | RIGHT | FULL] [OUTER JOIN](/sql-reference/constructs/join) | Supported with equality predicates only. Outer joins with non-equality predicates (for example, `ON a.id > b.id`) are not supported for incremental refresh.  Self-joins (where both sides of the outer join reference the same table) are supported.  You can specify any number of tables, and Snowflake tracks changes to all tables in the join. See [LEFT JOIN example](#label-dynamic-tables-supported-left-join-example). | Supported |
| [LATERAL](/sql-reference/constructs/join-lateral) JOIN | Not supported. However, you can use [LATERAL with FLATTEN()](#label-dynamic-tables-supported-lateral-flatten-example).  When using AUTO, Snowflake usually resolves to incremental refresh for definitions with lateral flatten joins, unless the definition contains other unsupported constructs.  Selecting the flatten SEQ column from a lateral flatten join is not supported for incremental refresh. | Supported |
| [UNION ALL](/sql-reference/operators-query) | Supported. See [UNION ALL example](#label-dynamic-tables-supported-union-all-example). | Supported |
| [UNION](/sql-reference/operators-query) (without ALL) | Supported. Behaves like UNION ALL combined with SELECT DISTINCT. | Supported |
| [MINUS, EXCEPT, INTERSECT](/sql-reference/operators-query) | Not supported | Supported |
| [ORDER BY](/sql-reference/constructs/order-by) | Accepted but has no effect. Dynamic tables have no guaranteed row order. | Accepted but has no effect. Dynamic tables have no guaranteed row order. |
| [LIMIT / FETCH](/sql-reference/constructs/limit) / [TOP <n>](/sql-reference/constructs/top_n) | Not supported | Supported |
| [Window functions](/sql-reference/functions-window) | Supported, except for the following:   - PERCENT\_RANK, DENSE\_RANK, or RANK with sliding window frames (for example, `ROWS BETWEEN 2 PRECEDING AND UNBOUNDED FOLLOWING`). - ANY\_VALUE is not supported because it is a non-deterministic function.   Non-deterministic aggregate functions such as APPROX\_COUNT\_DISTINCT, APPROX\_PERCENTILE, and APPROX\_TOP\_K are supported in the SELECT clause. See [Non-deterministic aggregate functions](#label-dynamic-tables-supported-nondeterministic-aggregates). | Supported |
| [User-defined functions](/developer-guide/udf/udf-overview) (UDFs and UDTFs) | Supported with restrictions. See [User-defined functions](#user-defined-functions) below. | Supported |
| [ML or LLM functions](/user-guide/snowflake-cortex/aisql) | Supported in the SELECT clause. | Supported |
| All [subquery operators](/sql-reference/operators-subquery) | Not supported | Supported |
| [External functions](/sql-reference/external-functions-introduction) | Not supported | Not supported |
| [PIVOT](/sql-reference/constructs/pivot) | Supported when using a fixed value list in the IN clause. Not supported when using a subquery in the IN clause. | Supported |
| [UNPIVOT](/sql-reference/constructs/unpivot) | Not supported | Supported |
| [SAMPLE / TABLESAMPLE](/sql-reference/constructs/sample) | Not supported | Not supported |
| [Sequences](/user-guide/querying-sequences) | Not supported | Supported |

Expand

Show lessSee more

## Examples for common constructs

The following examples demonstrate common SQL patterns that qualify for incremental refresh.

### Example: LEFT JOIN with incremental refresh

The following example creates a dynamic table that LEFT JOINs order data with customer data. Because the LEFT JOIN
uses an equality predicate, this definition qualifies for incremental refresh.

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_orders_with_customers
    TARGET_LAG = '10 minutes'
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT
        o.order_id,
        o.order_date,
        o.product_name,
        o.quantity * o.unit_price AS line_total,
        c.customer_name,
        c.region
    FROM raw_orders o
    LEFT JOIN dim_customers c
        ON o.customer_id = c.customer_id;
```

Orders without a matching customer appear in the results with NULL values for `customer_name` and `region`.
Snowflake tracks changes to both `raw_orders` and `dim_customers`.

### Example: UNION ALL with incremental refresh

The following example combines rows from two base tables using UNION ALL. Both branches must produce compatible
column lists.

Copy code

```
-- Base tables (simplified setup)
CREATE OR REPLACE TABLE raw_orders_us (
    order_id INT, customer_id INT, order_date TIMESTAMP_NTZ,
    product_name VARCHAR, quantity INT, unit_price DECIMAL(10,2),
    region VARCHAR DEFAULT 'US'
);

CREATE OR REPLACE TABLE raw_orders_eu (
    order_id INT, customer_id INT, order_date TIMESTAMP_NTZ,
    product_name VARCHAR, quantity INT, unit_price DECIMAL(10,2),
    region VARCHAR DEFAULT 'EU'
);

CREATE OR REPLACE DYNAMIC TABLE dt_combined_orders
    TARGET_LAG = '10 minutes'
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT order_id, customer_id, order_date, product_name, quantity, unit_price, region
    FROM raw_orders_us
    UNION ALL
    SELECT order_id, customer_id, order_date, product_name, quantity, unit_price, region
    FROM raw_orders_eu;
```

Snowflake tracks changes to both `raw_orders_us` and `raw_orders_eu` independently. New rows inserted into
either table are processed incrementally.

### Example: LATERAL FLATTEN with incremental refresh

The following example flattens a semi-structured VARIANT column using LATERAL FLATTEN, which is supported for
incremental refresh.

First, create a base table with nested JSON data:

Copy code

```
CREATE OR REPLACE TABLE persons
 AS
  SELECT column1 AS id, parse_json(column2) AS entity
  FROM values
   (12712555,
   '{ name:  { first: "John", last: "Smith"},
     contact: [
     { business:[
       { type: "phone", content:"555-1234" },
       { type: "email", content:"j.smith@example.com" } ] } ] }'),
   (98127771,
    '{ name:  { first: "Jane", last: "Doe"},
     contact: [
     { business:[
       { type: "phone", content:"555-1236" },
       { type: "email", content:"j.doe@example.com" } ] } ] }');
```

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_flattened_contacts
 TARGET_LAG = '10 minutes'
 WAREHOUSE = transform_wh
 AS
  SELECT p.id, f.value, f.path
  FROM persons p,
  LATERAL FLATTEN(input => p.entity) f;
```

## Supported non-deterministic functions

Many non-deterministic functions are supported for incremental refresh. Timestamp functions
(CURRENT\_TIMESTAMP, CURRENT\_DATE, CURRENT\_TIME) work in WHERE, HAVING, and QUALIFY clauses.
Non-deterministic aggregate functions such as APPROX\_COUNT\_DISTINCT, APPROX\_PERCENTILE, and APPROX\_TOP\_K are supported in the SELECT clause.
Session-context functions (CURRENT\_USER, CURRENT\_ROLE, CURRENT\_WAREHOUSE) and sequence
functions are restricted. The following table shows the full matrix.

Tip

`METADATA$ROW_LAST_COMMIT_TIME` provides the commit time of each row and is compatible with incremental refresh. Use it instead of `CURRENT_TIMESTAMP()` in the SELECT list when you need a refresh timestamp without forcing full refresh mode. See [Use row timestamps to measure latency in your pipelines](/user-guide/data-engineering/row-timestamps).

| Non-deterministic function | Incremental refresh | Full refresh |
| --- | --- | --- |
| [ANY\_VALUE](/sql-reference/functions/any_value) | Not supported | Not supported |
| [APPROX\_COUNT\_DISTINCT](/sql-reference/functions/approx_count_distinct) | Supported in the SELECT clause | Supported |
| [APPROX\_PERCENTILE](/sql-reference/functions/approx_percentile) | Supported in the SELECT clause | Supported |
| [APPROX\_TOP\_K](/sql-reference/functions/approx_top_k) | Supported in the SELECT clause | Supported |
| [AI\_CLASSIFY](/sql-reference/functions/ai_classify) | Supported in the SELECT clause | Supported |
| [AI\_COMPLETE](/sql-reference/functions/ai_complete) | Supported in the SELECT clause | Supported |
| [CURRENT\_ACCOUNT](/sql-reference/functions/current_account) | Not supported | Supported |
| [CURRENT\_DATE](/sql-reference/functions/current_date) (and aliases) | Supported only as a part of a WHERE/HAVING/QUALIFY clause. | Supported only as a part of a WHERE/HAVING/QUALIFY clause. |
| [CURRENT\_REGION](/sql-reference/functions/current_region) | Not supported | Supported |
| [CURRENT\_ROLE](/sql-reference/functions/current_role) | Not supported | Supported |
| [CURRENT\_TIME](/sql-reference/functions/current_time) (and aliases) | Supported only as a part of a WHERE/HAVING/QUALIFY clause. | Supported only as a part of a WHERE/HAVING/QUALIFY clause. |
| [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp) (and aliases) | Supported only as a part of a WHERE/HAVING/QUALIFY clause. | Supported only as a part of a WHERE/HAVING/QUALIFY clause. |
| Functions that rely on [CURRENT\_USER](/sql-reference/functions/current_user). | Not supported. Dynamic table refreshes act as their owner role with a special SYSTEM user. | Not supported. Dynamic table refreshes act as their owner role with a special SYSTEM user. |
| [CURRENT\_WAREHOUSE](/sql-reference/functions/current_warehouse) | Not supported | Supported |
| [DENSE\_RANK](/sql-reference/functions/dense_rank) | Supported | Supported |
| [AI\_EMBED](/sql-reference/functions/ai_embed) | Supported in the SELECT clause | Supported |
| [AI\_EXTRACT](/sql-reference/functions/ai_extract) | Supported in the SELECT clause | Supported |
| [FINETUNE (SNOWFLAKE.CORTEX)](/sql-reference/functions/finetune-snowflake-cortex) | Supported in the SELECT clause | Supported |
| [FIRST\_VALUE](/sql-reference/functions/first_value) | Supported | Supported |
| [LAST\_VALUE](/sql-reference/functions/last_value) | Supported | Supported |
| [MAX\_BY](/sql-reference/functions/max_by) | Supported | Supported |
| [MIN\_BY](/sql-reference/functions/min_by) | Supported | Supported |
| [NTH\_VALUE](/sql-reference/functions/nth_value) | Supported | Supported |
| [RANK](/sql-reference/functions/rank) | Supported | Supported |
| [ROW\_NUMBER](/sql-reference/functions/row_number) | Supported | Supported |
| [SENTIMENT (SNOWFLAKE.CORTEX)](/sql-reference/functions/sentiment-snowflake-cortex) | Supported in the SELECT clause | Supported |
| [Sequence functions](/sql-reference/functions/seq1) (such as `SEQ1`, `SEQ2`) | Not supported | Supported |
| [AI\_TRANSLATE](/sql-reference/functions/ai_translate) | Supported in the SELECT clause | Supported |
| [VOLATILE](/sql-reference/sql/create-function#label-create-function-syntax) user-defined functions | Supported in the SELECT clause | Supported |

Expand

Show lessSee more

### Non-deterministic aggregate functions

Non-deterministic aggregate functions are supported
for incremental refresh in INCREMENTAL, AUTO, and ADAPTIVE refresh modes when they appear in the
SELECT clause. You can use them as aggregates with GROUP BY or as window functions.

The following functions are supported:

- [APPROX\_COUNT\_DISTINCT](/sql-reference/functions/approx_count_distinct) (and its alias [HLL](/sql-reference/functions/hll))
- [APPROX\_PERCENTILE](/sql-reference/functions/approx_percentile)
- [APPROX\_TOP\_K](/sql-reference/functions/approx_top_k)

These functions return approximations, not exact results. For example, APPROX\_COUNT\_DISTINCT
returns an approximation of `COUNT(DISTINCT ...)`, not an exact distinct count.

Place non-deterministic aggregates in the SELECT clause only

Non-deterministic aggregate functions are supported for incremental refresh only in the SELECT
clause. Placing them in WHERE, GROUP BY, HAVING, or QUALIFY clauses is not supported.

The following example groups orders by customer and uses APPROX\_COUNT\_DISTINCT to estimate how many
distinct products each customer ordered:

Copy code

```
CREATE OR ALTER DYNAMIC TABLE dt_orders_by_customer
    TARGET_LAG = '30 minutes'
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT
        customer_id,
        APPROX_COUNT_DISTINCT(product_name) AS approx_distinct_products,
        SUM(quantity * unit_price) AS order_total
    FROM raw_orders
    GROUP BY customer_id;
```

### User-defined functions

UDFs are supported in dynamic table definitions. Whether a UDF supports incremental refresh depends on the function type and [volatility](/sql-reference/sql/create-function#label-create-function-volatile-immutable):

**Scalar UDFs:**

- IMMUTABLE: compatible with incremental refresh
- VOLATILE: compatible with incremental refresh when used only in SELECT clause

Place VOLATILE UDFs in the SELECT clause only

VOLATILE scalar UDFs are supported for incremental refresh only in the SELECT clause. Placing them in WHERE, GROUP BY, HAVING, or QUALIFY clauses is not supported.

**Table functions (UDTFs):**

- Supported in lateral joins only
- UDTFs always force full refresh regardless of volatility

If you replace an IMMUTABLE UDF that an existing dynamic table uses, subsequent incremental refreshes fail. Recreate the dynamic table after replacing the UDF.

For details, see [User-defined functions overview](/developer-guide/udf/udf-overview).

## Supported Snowflake Cortex AI functions

You can use [Snowflake Cortex AI Functions (including LLM functions)](/user-guide/snowflake-cortex/aisql) in the SELECT clause for dynamic tables in incremental refresh
mode. The same availability restrictions as described in [Cortex AI functions](/user-guide/snowflake-cortex/aisql#label-cortex-llm-ai-function) apply.

Cortex AI functions let you add AI-powered insights directly to your dynamic tables, automatically analyzing data as
it refreshes. For example, you can classify customer reviews, support tickets, or survey responses.

Place Cortex AI functions in the SELECT clause only

Cortex AI functions are supported for incremental refresh only in the SELECT clause. Placing them in WHERE, GROUP BY, HAVING, or QUALIFY clauses is not supported.

In the following example, `dt_review_sentiment` uses AI\_FILTER to evaluate each review with an LLM. The output column
`enjoyed` indicates whether the reviewer enjoyed the restaurant, based on the prompt.

Copy code

```
CREATE OR REPLACE TABLE reviews AS
  SELECT 'Wow... Loved this place.' AS review
  UNION ALL
  SELECT 'The pizza is not good.' AS review;

CREATE OR REPLACE DYNAMIC TABLE dt_review_sentiment
  TARGET_LAG = '10 minutes'
  WAREHOUSE = transform_wh
  REFRESH_MODE = INCREMENTAL
  AS
    SELECT review, AI_FILTER(CONCAT('The reviewer enjoyed the restaurant', review), {'model': 'llama3.1-70b'}) AS enjoyed FROM reviews;
```

## What causes fallback to full refresh

The following conditions cause Snowflake to use full refresh instead of incremental refresh. When `REFRESH_MODE = INCREMENTAL`, creation fails if any condition applies. When `REFRESH_MODE = AUTO`, creation succeeds but resolves to FULL at creation time. For details on how AUTO chooses between incremental and full refresh, see [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes).

| Condition | Category |
| --- | --- |
| Definition contains EXCEPT, INTERSECT, or MINUS | Definition shape |
| Definition contains LIMIT / TOP | Definition shape |
| GROUP BY ROLLUP, GROUP BY CUBE, or GROUP BY GROUPING SETS | Definition shape |
| Outer joins with non-equality predicates (such as `ON a.id > b.id`) | Definition shape |
| WITH RECURSIVE | Definition shape |
| Subqueries outside FROM clauses (such as WHERE EXISTS, WHERE IN (SELECT …)) | Definition shape |
| Non-deterministic scalar functions in SELECT (such as RANDOM(), UUID\_STRING(), CURRENT\_TIMESTAMP()) | Function type |
| SQL UDFs that contain subqueries | Function type |
| External functions | Function type |
| An upstream dynamic table uses FULL refresh (unless it has a [system-derived unique key](/user-guide/dynamic-tables/input-data-optimization)) | Pipeline shape |
| Change tracking is not enabled on a base table | Configuration |

Expand

Show lessSee more

To identify why a dynamic table resolved to full refresh, query the `refresh_mode_reason` column:

Copy code

```
SHOW DYNAMIC TABLES LIKE 'dt_orders';
```

```
+-------------------+-------------------------------------------+
| refresh_mode      | refresh_mode_reason                       |
|-------------------+-------------------------------------------|
| FULL              | QUERY_NOT_SUPPORTED_FOR_INCREMENTAL       |
+-------------------+-------------------------------------------+
```

Common `refresh_mode_reason` values include:

| Value | Meaning |
| --- | --- |
| QUERY\_NOT\_SUPPORTED\_FOR\_INCREMENTAL | The definition contains constructs that are not supported for incremental refresh. |
| USER\_SPECIFIED\_FULL\_REFRESH | The dynamic table was created with `REFRESH_MODE = FULL`. |
| UPSTREAM\_USES\_FULL\_REFRESH | An upstream dynamic table uses full refresh and does not have a system-derived unique key. |
| NULL | Incremental refresh is supported. No fallback reason. |

Expand

Show lessSee more

Additional values may appear in future releases.

Tip

If your query uses a construct that forces full refresh and you need incremental processing, consider
[custom incrementalization](/user-guide/dynamic-tables/custom-incrementalization). Custom incremental dynamic
tables bypass standard query analysis and let you define refresh logic directly as MERGE or INSERT DML.

### What happens when you use an unsupported construct with INCREMENTAL

If you explicitly set `REFRESH_MODE = INCREMENTAL` and the definition contains a construct that is not supported
for incremental refresh, the CREATE DYNAMIC TABLE statement fails with an error:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_unsupported_example
    TARGET_LAG = '10 minutes'
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT order_id, order_date
    FROM raw_orders
    EXCEPT
    SELECT order_id, order_date
    FROM excluded_orders;
```

```
002711 (0A000): SQL compilation error:
  Dynamic Table 'DT_UNSUPPORTED_EXAMPLE' is defined with REFRESH_MODE = INCREMENTAL,
  but the query is not supported for incremental refresh.
```

When you use `REFRESH_MODE = AUTO` instead, the same definition succeeds but resolves to FULL.

## Incremental refresh constraints

The following constraints apply specifically to dynamic tables that use incremental refresh.

### Incremental refresh on upstream full-refresh dynamic tables

Dynamic tables in incremental refresh mode can’t consume an upstream dynamic table that uses full refresh unless
the upstream full-refresh dynamic table has a system-derived unique key or a
[frozen region](/user-guide/dynamic-tables/frozen-regions) (a snapshot of rows that won’t change). When either condition is met, Snowflake
computes row-level changes across full refreshes, enabling downstream incremental processing.

To use this capability, set `REFRESH_MODE = INCREMENTAL` explicitly on the downstream dynamic table. AUTO doesn’t
resolve to incremental in this scenario.

For more information, see [Optimize input data for dynamic tables](/user-guide/dynamic-tables/input-data-optimization).

### Masking and row access policies

Masking or row access policies on a dynamic table don’t affect its refresh mode. Policies applied on base objects
affect incremental refresh as follows:

> - Incremental dynamic tables support most access and row masking policies on the base tables.
>   Non-deterministic policies (for example, with subqueries) and policies that look up data from tables are only supported
>   when the dynamic table refresh role is explicitly allowed access. Previously, only
>   [CURRENT\_ROLE](/sql-reference/functions/current_role) and [IS\_ROLE\_IN\_SESSION](/sql-reference/functions/is_role_in_session) were supported
>   incrementally.
> - Policy changes on base objects can trigger reinitialization. For details, see
>   [Modify dynamic tables](/user-guide/dynamic-tables/modify).
> - `CURRENT_AVAILABLE_ROLES()` returns an empty string set during refresh by default, because the refresh
>   runs without a named user’s role context. If a masking or row access policy references this
>   function, set `EXECUTE AS USER` on the dynamic table so the function evaluates the correct roles
>   during refresh. For setup steps, see
>   [Refresh with specific user privileges (EXECUTE AS USER)](/user-guide/dynamic-tables/privileges#label-dynamic-tables-privileges-execute-as-user).

### Replication

Replicated dynamic tables with incremental refresh reinitialize after failover before they can resume incremental
refresh.

For more information, see [Replication and dynamic tables](/user-guide/account-replication-considerations#label-replication-and-dynamic-tables).

### Cloning

[Cloned incremental dynamic tables](/sql-reference/sql/create-dynamic-table#label-create-dt-clone-syntax) might need to reinitialize during their
initial refresh after being created.

If a dynamic table is cloned from another dynamic table with dropped base tables, the clone is suspended and
can’t be resumed or refreshed.

## What’s next

- To optimize query patterns for incremental refresh performance, see
  [Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization).
- To define refresh logic directly with MERGE or INSERT statements, see
  [Custom incrementalization](/user-guide/dynamic-tables/custom-incrementalization).
- To understand the cost differences between incremental and full refresh, see
  [Understanding costs for dynamic tables](/user-guide/dynamic-tables/cost).
- To troubleshoot refresh issues, see
  [Troubleshoot dynamic table refresh issues](/user-guide/dynamic-tables/troubleshoot-refreshes).
- For the full CREATE DYNAMIC TABLE syntax, see
  [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table).
