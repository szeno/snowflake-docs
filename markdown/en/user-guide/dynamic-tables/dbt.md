# Use dynamic tables in dbt

The [dbt-snowflake adapter](https://docs.getdbt.com/docs/core/connect-data-platform/snowflake-setup) lets you define dynamic tables as dbt models. When you set `materialized='dynamic_table'`,
dbt issues CREATE DYNAMIC TABLE instead of CREATE TABLE. This gives you dbt’s software engineering discipline
(version control, testing, lineage) alongside dynamic tables’ built-in incremental refresh. Two choices remain
independent: who controls scheduling, and how data is processed.

## Prerequisites

Before you begin, make sure you have:

- The dbt-snowflake adapter v1.11.5 or later installed.
- A configured Snowflake connection in your dbt profile (`~/.dbt/profiles.yml`).
- A Snowflake role with CREATE DYNAMIC TABLE privilege on the target schema. For required privileges, see
  [Dynamic table access control](/user-guide/dynamic-tables/privileges).
- `CHANGE_TRACKING = TRUE` set on base tables that feed your dynamic tables. Without this, CREATE OR REPLACE
  on upstream models breaks change tracking for downstream dynamic tables.

For dbt installation instructions, see the
[dbt-snowflake setup guide](https://docs.getdbt.com/docs/core/connect-data-platform/snowflake-setup).

## Choose a scheduling model

You have two options for who triggers refreshes, independent of the processing model.

### dbt-managed refresh (default)

When you omit `target_lag` from your config (or explicitly set `scheduler: DISABLE`), dbt controls when
refreshes happen. Each `dbt run` creates or alters the dynamic table, then issues
`ALTER DYNAMIC TABLE ... REFRESH` to trigger a synchronous refresh.

Copy code

```
models:
  - name: dt_orders
    config:
      materialized: dynamic_table
      snowflake_warehouse: transform_wh
      scheduler: DISABLE
```

With dbt-managed refresh:

- Each model refreshes synchronously and independently during `dbt run`.
- No cascading. Downstream dynamic tables do not refresh automatically.
- You retain full control over orchestration timing through your existing dbt scheduler (Airflow, dbt Cloud, cron).

Best for teams that already use an external orchestrator (Airflow, dbt Cloud, cron) and want to keep refresh timing under that orchestrator’s control.

### Snowflake-managed refresh

When you set `target_lag`, Snowflake refreshes the dynamic table autonomously to meet the specified target lag.

Copy code

```
models:
  - name: dt_orders
    config:
      materialized: dynamic_table
      snowflake_warehouse: transform_wh
      target_lag: '10 minutes'
```

With Snowflake-managed refresh:

- Snowflake decides when and how often to refresh based on `target_lag`.
- Cascading pipelines coordinate automatically. When an upstream dynamic table refreshes, downstream tables
  refresh in dependency order at the same snapshot, providing consistency across the pipeline.
- `dbt run` creates or alters the definition but does not trigger a refresh. Snowflake handles that independently.

Best for pipelines that need continuous freshness (such as dashboards with SLA-driven staleness targets) regardless of when `dbt run` executes.

## Choose a processing model

Independent of who controls scheduling, you choose how data is processed on each refresh.

### Replace CTAS models (migration step one)

A straightforward migration path: swap `materialized: table` to `materialized: dynamic_table` with zero SQL changes.
Your existing SELECT statement becomes the dynamic table definition, and Snowflake detects when source data
has not changed and skips the refresh with no additional configuration.

Copy code

```
# Before
models:
  - name: dt_orders
    config:
      materialized: table

# After (zero SQL changes needed)
models:
  - name: dt_orders
    config:
      materialized: dynamic_table
      snowflake_warehouse: transform_wh
      refresh_mode: FULL
```

Setting `refresh_mode: FULL` makes this a safe drop-in replacement for CTAS because the processing behavior
is identical. If you omit `refresh_mode`, it defaults to AUTO, and Snowflake chooses the optimal strategy
at creation time.

### Incremental processing (migration step two)

After the initial migration, optimize models that benefit from processing only changed rows. Unlike dbt’s
built-in incremental materialization, you do not need `{% if is_incremental() %}` blocks. Snowflake tracks
changes internally and processes only deltas.

Copy code

```
models:
  - name: dt_orders
    config:
      materialized: dynamic_table
      snowflake_warehouse: transform_wh
      refresh_mode: INCREMENTAL
```

Incremental processing works for aggregations, joins, and filters over append-only sources. For the full list
of SQL constructs that support incremental refresh, see [Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries).

`REFRESH_MODE = FULL` can outperform incremental processing when a large proportion of source data changes
between refreshes. In those cases, tracking individual row deltas costs more than recomputing the entire result.

## Configuration reference

Set these properties in your model’s YAML config or in a `config()` block at the top of the SQL file.

| dbt config | Snowflake DDL equivalent | Default | Description |
| --- | --- | --- | --- |
| `target_lag` | [TARGET\_LAG](/user-guide/dynamic-tables/target-lag) | None (dbt-managed refresh) | Maximum acceptable data staleness (for example, `'10 minutes'`, `'1 hour'`, or `DOWNSTREAM`). Omit to use dbt-managed refresh. |
| `snowflake_warehouse` | WAREHOUSE | Profile default | Warehouse used for refreshes. |
| `refresh_mode` | REFRESH\_MODE | AUTO | How Snowflake refreshes data: `INCREMENTAL`, `FULL`, or `AUTO`. |
| `initialize` | INITIALIZE | ON\_CREATE | When the initial refresh runs: `ON_CREATE` (immediately) or `ON_SCHEDULE` (deferred). |
| `scheduler` | SCHEDULER | ENABLE | Whether Snowflake schedules refreshes autonomously: `ENABLE` or `DISABLE`. Set to `DISABLE` for dbt-managed refresh. |
| `on_configuration_change` | N/A (dbt-only) | apply | What dbt does when config changes on an existing dynamic table: `apply` (issue ALTER), `continue` (skip with warning), or `fail` (fail the run). |
| `snowflake_initialization_warehouse` | INITIALIZATION\_WAREHOUSE | None | A separate warehouse for the initial full refresh. Useful when initialization is more expensive than subsequent refreshes. |
| `cluster_by` | CLUSTER BY | None | Clustering keys for the dynamic table. Accepts a column name or list of columns. |
| `immutable_where` | FROZEN WHERE | None | A filter condition applied at creation time. Rows matching this condition are never reprocessed. |
| `transient` | TRANSIENT | false | Creates a transient dynamic table (no Fail-safe, lower storage cost). |

Expand

Show lessSee more

For a complete list of dbt-snowflake dynamic table configs, see the
[dbt-snowflake documentation](https://docs.getdbt.com/reference/resource-configs/snowflake-configs#dynamic-tables).

## Example model

This example shows a minimal dynamic table model with dbt-managed refresh:

Copy code

```
# models/staging/dt_orders.yml
models:
  - name: dt_orders
    config:
      materialized: dynamic_table
      snowflake_warehouse: transform_wh
      scheduler: DISABLE
      refresh_mode: INCREMENTAL
```

Copy code

```
-- models/staging/dt_orders.sql
SELECT
    order_id,
    customer_id,
    order_date,
    TRIM(UPPER(product_name)) AS product_name,
    quantity,
    unit_price
FROM {{ source('raw', 'raw_orders') }}
WHERE order_status != 'returned'
```

Running `dbt run` compiles this into a CREATE DYNAMIC TABLE statement, then triggers a refresh. Subsequent
runs detect if the SQL is unchanged and skip the model entirely.

## Handle schema changes

Dynamic tables handle configuration and definition changes differently.

### Configuration changes

When you change only config properties (target lag, warehouse, refresh mode) and `on_configuration_change`
is set to `apply`, dbt issues ALTER DYNAMIC TABLE to apply the new settings without replacing the table.
Set `on_configuration_change` to `continue` to skip changes with a warning, or `fail` to abort the run.

### SQL changes

Any change to the model’s SELECT statement triggers CREATE OR REPLACE, which causes
[reinitialization](/user-guide/dynamic-tables/modify#label-dynamic-tables-evolving-reinitialization-triggers).
The dynamic table rebuilds from scratch.

### CHANGE\_TRACKING on base tables

When dbt issues CREATE OR REPLACE on a staging model that feeds downstream dynamic tables, change tracking
metadata is lost. To prevent pipeline failures:

1. Set `CHANGE_TRACKING = TRUE` explicitly on base tables:

Copy code

```
ALTER TABLE raw_orders SET CHANGE_TRACKING = TRUE;
```

2. Use INSERT OVERWRITE instead of CREATE OR REPLACE for upstream staging tables where possible. This
   preserves the table object identity and change tracking metadata.
3. For deployments that must use CREATE OR REPLACE, suspend downstream dynamic tables before the run and
   resume them afterward. See [Suspend and resume around deployments](#label-dynamic-tables-dbt-suspend-resume).

## Suspend and resume around deployments

Running `dbt run --full-refresh` issues CREATE OR REPLACE for every model, even unchanged ones. Each
CREATE OR REPLACE destroys and recreates the dynamic table, triggering reinitialization. If upstream base tables are
also replaced, downstream dynamic tables can lose their change tracking reference and fail.

To prevent failures during deployment, suspend downstream dynamic tables before the dbt run and resume them
afterward:

Copy code

```
# models/marts/dt_orders_daily.yml
models:
  - name: dt_orders_daily
    config:
      materialized: dynamic_table
      snowflake_warehouse: transform_wh
      target_lag: '30 minutes'
      +pre-hook:
        - "ALTER DYNAMIC TABLE IF EXISTS {{ this }} SUSPEND"
      +post-hook:
        - "ALTER DYNAMIC TABLE IF EXISTS {{ this }} RESUME"
```

The IF EXISTS clause prevents errors when a model is created for the first time and the table does not yet exist.

## Set QUOTED\_IDENTIFIERS\_IGNORE\_CASE to FALSE

The dbt-snowflake adapter expects lowercase column names in the results of SHOW DYNAMIC TABLES. If your Snowflake
account has `QUOTED_IDENTIFIERS_IGNORE_CASE = TRUE`, SHOW DYNAMIC TABLES returns uppercase column names, which causes
the adapter’s config parser to fail with:

```
SnowflakeDynamicTableConfig.__init__() missing 6 required positional arguments
```

This issue was fixed in dbt-snowflake v1.10.0. On older versions, set the parameter to FALSE at the account or
session level:

Copy code

```
# ~/.dbt/profiles.yml
my_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: my_account
      # ... other connection settings ...
      session_parameters:
        QUOTED_IDENTIFIERS_IGNORE_CASE: FALSE
```

## Limitations

| Limitation | Details |
| --- | --- |
| No model contracts | dbt model contracts (column type enforcement) are not supported with the `dynamic_table` materialization. Validate column types with dbt tests instead. |
| No copy grants | The `copy_grants` config is not supported. Grants are reset on each CREATE OR REPLACE. Re-grant privileges after deployments. |
| SQL changes require full replacement | Any change to the model’s SQL triggers CREATE OR REPLACE, which causes reinitialization. Config-only changes (target lag, warehouse) are applied with ALTER when `on_configuration_change` is set to `apply`. |
| Unsupported upstream source types | Dynamic tables can’t reference materialized views, external tables, directory tables, or streams as upstream sources. This is a Snowflake platform constraint. For the complete list, see [Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries). |
| `--full-refresh` rebuilds all models | Running `dbt run --full-refresh` issues CREATE OR REPLACE for every model, including unchanged ones, causing unnecessary reinitialization. Use the SUSPEND/RESUME pattern described above, or tag models to exclude unchanged ones from full-refresh runs. |
| dbt tests run against current state | dbt tests query the current table state, not a specific refresh result. If a dynamic table is mid-refresh when `dbt test` runs, tests read whatever state is available. Schedule tests after confirming refresh completion. |

Expand

Show lessSee more

## What’s next

- To learn about refresh scheduling, see [Set the target lag for a dynamic table](/user-guide/dynamic-tables/target-lag).
- To understand which SQL constructs support incremental refresh, see [Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries).
- To monitor refresh health after dbt deployments, see [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).
- To manage dynamic table lifecycle operations, see [Manage dynamic tables](/user-guide/dynamic-tables/manage).
