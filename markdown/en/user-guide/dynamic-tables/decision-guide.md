# Decision guide for dynamic tables

Use this guide to choose the right approach for your data pipeline: dynamic tables, streams and tasks,
or materialized views.

## Decision table

| Scenario | Dynamic tables | Streams and tasks | Materialized views |
| --- | --- | --- | --- |
| SQL-based pipeline with joins or aggregations | **Preferred** | Possible | No (single table only) |
| Multi-step declarative pipeline (bronze/silver/gold) | **Preferred** | Possible | No |
| Incremental processing of changed data | **Preferred** (declarative) | **Preferred** (procedural) | No |
| Single-table query acceleration | Possible | Possible | **Preferred** |
| Procedural logic (stored procedures, IF/ELSE, loops) | No | **Preferred** | No |
| MERGE or complex upsert patterns | No | **Preferred** | No |
| External function calls or API integrations | No | **Preferred** | No |
| Always-current data with no lag | No (minimum TARGET\_LAG setting is 1 minute) | Possible (tasks run on a schedule; not zero-lag) | **Preferred** |
| Transparent query acceleration (optimizer rewrites queries to use the precomputed result) | No | No | **Preferred** |
| Custom scheduling or strict orchestration control | Possible (manual trigger only; no CRON or cascade) | **Preferred** | No |
| Pipeline using UDFs, UDTFs, or Snowpark | Possible (scalar UDFs and UDTFs with explicit column lists; Snowpark not supported) | **Preferred** | No |

Expand

Show lessSee more

## If you need X, use Y

Use the following guidance to match your requirements to the right approach.

### If you need a declarative SQL pipeline, use dynamic tables

Dynamic tables let you define the result you want as a SELECT statement. Snowflake handles refresh timing,
dependency ordering, and incremental processing. You don’t need to write procedural code, manage streams, or
build a pipeline of tasks.

This is the recommended approach for new multi-table SQL pipelines in Snowflake, especially
pipelines with joins, aggregations, or window functions.

### If you need procedural logic or custom orchestration, use streams and tasks

Streams and tasks give you full control over the pipeline logic. Use them when your pipeline needs
stored procedures, MERGE operations, external function calls, custom retry logic, or explicit scheduling
with CRON expressions. For more information, see [Introduction to streams](/user-guide/streams-intro) and
[Introduction to tasks](/user-guide/tasks-intro).

### If you need single-table query acceleration, use materialized views

Materialized views accelerate repeated queries against a single base table. The query optimizer automatically
rewrites queries to use the materialized view, and the data is always current. Use materialized views when
your goal is read performance, not building a data pipeline. For more information, see
[Working with Materialized Views](/user-guide/views-materialized).

## Example: streams and tasks vs. dynamic tables

The following side-by-side comparison shows how the same definition (extracting names from raw JSON data)
looks with each approach. The dynamic table version replaces the stream, task, and MERGE logic with a single
SELECT statement.

### Streams and tasks approach

1. Create a landing table.
2. Create a stream on the landing table.
3. Create a target table.
4. Create a task with MERGE logic to process stream records.
5. Resume the task.

### Dynamic table approach

1. Create a landing table.
2. Create a dynamic table with the SELECT that defines the result.

| Streams and tasks | Dynamic tables |
| --- | --- |
| Copy code  ``` -- Create a landing table to store -- raw JSON data. CREATE OR REPLACE TABLE raw   (var VARIANT);  -- Create a stream to capture inserts -- to the landing table. CREATE OR REPLACE STREAM rawstream1   ON TABLE raw;  -- Create a table that stores the -- names of office visitors from the -- raw data. CREATE OR REPLACE TABLE names   (id INT,    first_name STRING,    last_name STRING);  -- Create a task that inserts new name -- records from the rawstream1 stream -- into the names table. -- Run the task every minute when -- the stream contains records. CREATE OR REPLACE TASK raw_to_names   WAREHOUSE = transform_wh   SCHEDULE = '1 minute'   WHEN     SYSTEM$STREAM_HAS_DATA('rawstream1')   AS     MERGE INTO names n       USING (         SELECT var:id id, var:fname fname,                var:lname lname,                metadata$action,                metadata$isupdate           FROM rawstream1       ) r1 ON n.id = TO_NUMBER(r1.id)       WHEN MATCHED         AND metadata$action = 'DELETE'         AND NOT metadata$isupdate THEN           DELETE       WHEN MATCHED         AND metadata$action = 'INSERT' THEN         UPDATE SET n.first_name = r1.fname,                    n.last_name = r1.lname       WHEN NOT MATCHED         AND metadata$action = 'INSERT' THEN         INSERT (id, first_name, last_name)           VALUES (r1.id, r1.fname, r1.lname);  -- Start the task. ALTER TASK raw_to_names RESUME; ``` | Copy code  ``` -- Create a landing table to store -- raw JSON data. CREATE OR REPLACE TABLE raw   (var VARIANT);  -- Create a dynamic table containing -- the names of office visitors from -- the raw data. -- Keep the data within 1 minute of -- the base table. CREATE OR REPLACE DYNAMIC TABLE dt_visitors   TARGET_LAG = '1 minute'   WAREHOUSE = transform_wh   REFRESH_MODE = INCREMENTAL   AS     SELECT       var:id::int id,       var:fname::string first_name,       var:lname::string last_name     FROM raw; ``` |

Expand

Show lessSee more

The dynamic table approach replaces four objects and MERGE logic with a single SELECT definition.

## When NOT to use dynamic tables

Don’t use dynamic tables when your pipeline has any of the following requirements. Use streams and tasks
or materialized views instead, as noted.

### You need DML on the output table

Dynamic tables are read-only. You can’t run INSERT, UPDATE, DELETE, or TRUNCATE against them. If your pipeline
requires direct modifications to the output (for example, GDPR right-to-erasure requests), use streams
and tasks with a standard table.

### You need stored procedures or external functions

The dynamic table definition can’t call stored procedures, external functions, or tasks. If your pipeline
requires procedural logic, conditional branching, or external API calls, use streams and tasks.

### You need sub-minute data freshness

The minimum target lag for a dynamic table is 1 minute. If you need always-current data with no lag,
use materialized views. If you need sub-minute freshness with custom logic, use streams and tasks.

### You need MERGE or complex upsert patterns

Dynamic tables use a declarative model and don’t support MERGE statements. If your pipeline relies
on upsert logic with compound keys, use streams and tasks.

### You need surrogate key generation

Dynamic tables don’t support sequence functions (SEQ1, SEQ2) or UUID\_STRING in incremental
refresh mode. RANDOM() is not supported in incremental refresh mode. If you use AUTO, it resolves to FULL when the definition includes RANDOM(). If your pipeline generates surrogate keys with these functions, use streams and tasks.

Timestamp functions like CURRENT\_TIMESTAMP are supported in WHERE/HAVING/QUALIFY clauses. See [supported queries](/user-guide/dynamic-tables/supported-queries#label-dynamic-tables-intro-supported-nondeterministic-functions) for the full matrix.

### You need schema evolution without reinitialization

Changing the definition of a dynamic table (for example, adding columns) triggers reinitialization (Snowflake reprocesses the entire table). If your pipeline requires frequent schema changes without reprocessing all data, use streams
and tasks with ALTER TABLE.

### You need SCD Type 2 history tracking

Dynamic tables represent the current state of the data, not a historical record. If your pipeline
needs to track changes over time (slowly changing dimensions Type 2), use streams and tasks.

### Your definition is a simple single-table query

If you only need to accelerate a query against a single base table without joins, a materialized view
is more efficient. The query optimizer automatically rewrites queries to use the materialized view, which
doesn’t happen with dynamic tables.

Key limitations

- A single account can hold a maximum of 50,000 dynamic tables.
- You can’t run DML (INSERT, UPDATE, DELETE, TRUNCATE) on a dynamic table.
- You can’t create a temporary dynamic table.
- Dynamic tables don’t support sources that include directory tables, external tables, streams, or materialized views.
- Frozen region predicates have restrictions on supported expressions. For details, see [Frozen regions and backfill](/user-guide/dynamic-tables/frozen-regions).

For the full list of limitations, see [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table).

## What’s next

After choosing your approach:

- To create your first dynamic table, see [Create a dynamic table](/user-guide/dynamic-tables/create).
- To understand how refresh modes work, see [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes).
- To set up a multi-table pipeline, see [Set the target lag for a dynamic table](/user-guide/dynamic-tables/target-lag).
- For queries supported in dynamic table definitions, see [Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries).
- If you chose streams and tasks, see [Introduction to streams](/user-guide/streams-intro) and [Introduction to tasks](/user-guide/tasks-intro).
- If you chose materialized views, see [Working with Materialized Views](/user-guide/views-materialized).
