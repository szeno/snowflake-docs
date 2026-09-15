# Clone dynamic tables

Cloning creates a new dynamic table with the same column definitions and data as the source, without physically copying the data. This page
explains how to clone a single dynamic table, clone a dynamic table to a regular table, and clone an entire pipeline.

For the full syntax reference, see [CREATE DYNAMIC TABLE … CLONE](/sql-reference/sql/create-dynamic-table#label-create-dt-clone-syntax).

Clones are suspended after creation. Resume a cloned dynamic table before it refreshes on schedule (see [Resume cloned dynamic tables](#label-dynamic-tables-clone-resume)).

## Clone a dynamic table

The simplest clone creates an identical dynamic table that shares the source’s data through Snowflake’s [zero-copy cloning](/user-guide/tables-storage-considerations#label-cloning-tables):

Copy code

```
CREATE DYNAMIC TABLE dt_orders_clone CLONE dt_orders;
```

The clone inherits the source’s properties, including its column definitions, definition, target lag, warehouse, refresh mode, INITIALIZE
setting, frozen region, clustering keys, and attached storage lifecycle policy. It does not inherit the source’s refresh history or scheduling state.

### Clone with time travel

You can clone a dynamic table as it existed at a specific point in the past:

Copy code

```
CREATE DYNAMIC TABLE dt_orders_clone
  CLONE dt_orders
    AT (TIMESTAMP => '2025-01-16 12:00:00'::TIMESTAMP_TZ);
```

For more information about the AT and BEFORE clauses, see [Understanding & using Time Travel](/user-guide/data-time-travel).

### Override properties at clone time

You can change the target lag and warehouse when you clone a dynamic table:

Copy code

```
CREATE DYNAMIC TABLE dt_orders_dev
  CLONE dt_orders
  COPY GRANTS
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh;
```

Use [COPY GRANTS](/sql-reference/sql/create-table#label-create-table-copy-grants) to preserve existing privilege grants on the cloned dynamic table.

## Clone a dynamic Iceberg table

You can clone a [dynamic Iceberg table](/user-guide/dynamic-tables/create-iceberg) to a new dynamic Iceberg table, the same way you clone
a regular dynamic table:

Copy code

```
CREATE DYNAMIC ICEBERG TABLE dt_orders_iceberg_clone
  CLONE dt_orders_iceberg;
```

The clone is always a Snowflake-managed Iceberg table. You can’t set EXTERNAL\_VOLUME, CATALOG, or BASE\_LOCATION on the clone statement;
specifying any of these options returns an error. Snowflake assigns the clone its own base location. The clone also keeps the source’s
Iceberg format version.

Time travel, COPY GRANTS, and target lag and warehouse overrides work the same as they do for regular dynamic tables. For example, you can
clone a dynamic Iceberg table at an earlier point in time and override its target lag and warehouse:

Copy code

```
CREATE DYNAMIC ICEBERG TABLE dt_orders_iceberg_dev
  CLONE dt_orders_iceberg
    AT (TIMESTAMP => '2025-01-16 12:00:00'::TIMESTAMP_TZ)
  COPY GRANTS
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh;
```

When you clone a schema or database that contains a dynamic Iceberg table, the clone includes the dynamic Iceberg table along with the
other objects in the schema or database.

### Clone a dynamic Iceberg table to a Snowflake-managed Iceberg table

To create a static snapshot of a dynamic Iceberg table’s data, clone it to a [Snowflake-managed Iceberg table](/user-guide/tables-iceberg).
The resulting Iceberg table has the same columns and data but no refresh schedule, target lag, or warehouse assignment:

Copy code

```
CREATE ICEBERG TABLE orders_iceberg_snapshot
  CLONE dt_orders_iceberg;
```

The source dynamic Iceberg table must be [initialized](/user-guide/dynamic-tables/overview#label-dynamic-tables-initialization) before you
can clone it to a Snowflake-managed Iceberg table.

See [Limitations](#label-dynamic-tables-clone-limitations).

## Clone a dynamic table to a regular table

To create a static snapshot of a dynamic table’s data, clone it to a regular table. The resulting table has the same columns and data but
no refresh schedule, target lag, or warehouse assignment:

Copy code

```
CREATE TABLE orders_snapshot
  CLONE dt_orders;
```

The cloned table retains row access policies, masking policies, tags, clustering keys, and comments from the source dynamic table.

Cloning a dynamic table to a regular table has these requirements:

- The source dynamic table must be [initialized](/user-guide/dynamic-tables/overview#label-dynamic-tables-initialization). An uninitialized
  dynamic table has not completed its initial refresh, so there is no materialized snapshot to clone.
- You can’t clone a dynamic Iceberg table to a regular table. To clone a dynamic Iceberg table, clone it to a new dynamic Iceberg table or
  to a Snowflake-managed Iceberg table instead. See [Clone a dynamic Iceberg table](#label-dynamic-tables-clone-iceberg).

### Error: cloning an uninitialized dynamic table

If you try to clone an uninitialized dynamic table to a regular table, you get the following error:

Copy code

```
CREATE TABLE dt_uninitialized_snapshot CLONE dt_uninitialized;
```

```
Cannot clone an uninitialized dynamic table. Please run a manual refresh or wait for a scheduled refresh before cloning.
```

To resolve this, run a manual refresh on the source dynamic table first, or clone it to another dynamic table instead (which doesn’t
require initialization).

## Clone an entire pipeline

When a dynamic table depends on other dynamic tables or base tables, clone the entire schema or database rather than individual objects.
This preserves the relationships between objects in the pipeline, avoiding reinitializations that would otherwise occur.

Copy code

```
CREATE SCHEMA analytics_dev
  CLONE analytics_prod;
```

The schema-level CLONE copies all objects together (base tables, views, and dynamic tables), preserving their relationships. In the cloned schema,
unqualified object references in definitions resolve to the cloned copies, so the pipeline is fully independent. However, fully qualified
references (such as `other_schema.table_name`) still point to the original objects, creating cross-schema dependencies.

If you clone a single dynamic table without its upstream objects, the clone still references the original upstream tables. This creates
a dependency across environments that may cause unexpected behavior (reinitialization or, if a base object was missing at clone time, refresh failures).

| Clone scope | Pipeline preserved? | Reinitialization risk | When to use |
| --- | --- | --- | --- |
| Single dynamic table (same schema) | No (references original upstream objects) | Low | Isolated dynamic tables with no upstream dependencies |
| Single dynamic table (cross-schema) | No (references original upstream objects) | Higher | Testing with shared upstream sources |
| Schema clone | Yes (all objects cloned together) | Lower | Pipelines contained in one schema |
| Database clone | Yes (all objects cloned together) | Lowest | Full environment copies for development or testing |

Expand

Show lessSee more

## Resume cloned dynamic tables

All cloned dynamic tables are suspended after cloning. In [DYNAMIC\_TABLE\_GRAPH\_HISTORY](/sql-reference/functions/dynamic_table_graph_history),
this appears as SUSPENDED in the scheduling\_state column with a suspend reason of CLONED\_AUTO\_SUSPENDED. Any downstream dynamic tables of the cloned object are also suspended,
shown as UPSTREAM\_CLONED\_AUTO\_SUSPENDED.

To resume scheduled refreshes, run `ALTER DYNAMIC TABLE <name> RESUME` for each cloned dynamic table.

When you resume an upstream dynamic table, its downstream dynamic tables with the UPSTREAM\_CLONED\_AUTO\_SUSPENDED state automatically resume
as well, provided that:

- The downstream dynamic table was not manually suspended before the clone. If it was manually suspended, you must resume it explicitly.
- All upstream dynamic tables that the downstream depends on are resumed. If it depends on multiple upstream dynamic
  tables, it stays suspended until every one is resumed.
- Dynamic tables that were already suspended before the clone retain their original suspend reason and are not affected by the clone operation.

### Initial refresh may reinitialize

The initial refresh after cloning may be a full [reinitialization](/user-guide/dynamic-tables/modify#label-dynamic-tables-evolving-reinitialization-triggers) rather than an incremental refresh. Snowflake triggers a full reinitialization if the clone’s change-tracking state has diverged from its base objects.

Reinitialization is more likely when you clone a single dynamic table without its base objects, or when you delay resuming the clone
after cloning. Cloning the entire schema or database together reduces this risk.

Plan for the compute cost of a full reinitialization on the initial refresh. For more information, see [Reinitialization triggers](/user-guide/dynamic-tables/modify#label-dynamic-tables-evolving-reinitialization-triggers).

Subsequent refreshes return to the normal refresh mode (INCREMENTAL, FULL, ADAPTIVE, or CUSTOM\_INCREMENTAL) based on the dynamic table’s REFRESH\_MODE setting.

## Limitations

- **A dynamic Iceberg table can be cloned only to a dynamic Iceberg table or a Snowflake-managed Iceberg table.** You can’t clone a
  dynamic Iceberg table to a regular (non-Iceberg) table. Cloning a regular dynamic table always produces a regular dynamic table; there’s
  no syntax to clone a regular dynamic table into Iceberg format. For details, see [Clone a dynamic Iceberg table](#label-dynamic-tables-clone-iceberg).
- **You can’t set storage options on a dynamic Iceberg table clone.** A dynamic Iceberg table clone uses the same external volume and
  catalog as the source, and Snowflake assigns it a new base location. Specifying EXTERNAL\_VOLUME, CATALOG, or BASE\_LOCATION on the clone
  statement returns an error. The clone also keeps the source’s Iceberg format version.
- **Lag constraint violations can surface at clone time.** If an upstream dynamic table’s target lag was changed after a downstream dynamic
  table was created, the lag constraint (downstream lag must be greater than or equal to the largest upstream lag) is only validated during the
  clone. The clone command fails if the constraint is not met. To avoid this, verify target lag constraints before cloning. For more
  information, see [Set the target lag for a dynamic table](/user-guide/dynamic-tables/target-lag).
- **Storage diverges after cloning.** At clone time, the source and clone share existing micro-partitions through zero-copy cloning. As
  each side is modified through refreshes, the shared storage diverges and both copies accrue independent storage costs.

## What’s next

- To suspend or resume dynamic tables manually, see [Manage dynamic tables](/user-guide/dynamic-tables/manage).
- To check the refresh status of cloned dynamic tables, see [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).
- To share cloned dynamic tables across accounts, see [Share dynamic tables with other accounts](/user-guide/dynamic-tables/sharing).
- [Modify dynamic tables](/user-guide/dynamic-tables/modify)
