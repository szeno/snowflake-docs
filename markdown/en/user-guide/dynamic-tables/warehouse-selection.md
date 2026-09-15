# Choose and size warehouses for dynamic tables

Every dynamic table needs a warehouse that runs its refreshes. The warehouse you assign controls
how much memory and parallelism each refresh gets, and directly affects both refresh speed and
credit consumption.

## WAREHOUSE vs INITIALIZATION\_WAREHOUSE

Dynamic tables support two warehouse parameters. WAREHOUSE runs regular incremental refreshes.
INITIALIZATION\_WAREHOUSE, when set, runs the initial refresh and any subsequent reinitializations,
which perform a full scan of the source data and are typically more resource-intensive.
Common reinitialization triggers include base table recreation, upstream view changes, and
masking policy changes. For the full list, see
[Reinitialization triggers](/user-guide/dynamic-tables/modify#label-dynamic-tables-evolving-reinitialization-triggers).

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_orders
    TARGET_LAG = '10 minutes'
    WAREHOUSE = transform_wh                    -- steady-state incremental refreshes
    INITIALIZATION_WAREHOUSE = transform_wh_xl  -- initial build and reinitializations
    REFRESH_MODE = INCREMENTAL
AS
    SELECT ... FROM raw_orders ...;
```

The following table shows which warehouse runs each type of refresh operation.

| Operation | Warehouse used |
| --- | --- |
| Incremental refresh | WAREHOUSE |
| Scheduled full refresh (REFRESH\_MODE = FULL) | WAREHOUSE |
| Initial refresh (scheduled) | INITIALIZATION\_WAREHOUSE if set, otherwise WAREHOUSE |
| Reinitialization | INITIALIZATION\_WAREHOUSE if set, otherwise WAREHOUSE |
| Manual refresh (ALTER DYNAMIC TABLE … REFRESH) | Same as scheduled refresh (WAREHOUSE or INITIALIZATION\_WAREHOUSE based on operation type) |
| Manual refresh (ALTER DYNAMIC TABLE … REFRESH COPY SESSION) | Current session warehouse (overrides both WAREHOUSE and INITIALIZATION\_WAREHOUSE) |

Expand

Show lessSee more

When you don’t set INITIALIZATION\_WAREHOUSE, all refresh operations run on the warehouse
specified by WAREHOUSE.

## Use separate warehouses for initialization and steady-state refreshes

Initialization scans the entire source dataset; incremental refreshes process only changed rows. A single warehouse for both workloads means over-provisioning for daily refreshes or under-provisioning for initialization.

Use a larger INITIALIZATION\_WAREHOUSE so that initial builds and reinitializations finish
quickly, while keeping a smaller WAREHOUSE for cost-effective incremental refreshes. This
pattern is especially useful when you need fast recovery after promoting a secondary dynamic
table to primary, or when you must meet strict recovery time objective (RTO) / recovery point
objective (RPO) requirements without increasing steady-state costs.

You can add or change the initialization warehouse at any time without recreating the dynamic
table by running `ALTER DYNAMIC TABLE <name> SET INITIALIZATION_WAREHOUSE = <warehouse>`. To remove it and run all operations on the primary warehouse, run `ALTER DYNAMIC TABLE <name> UNSET INITIALIZATION_WAREHOUSE`.

If you reference a warehouse that does not exist, the statement fails:

Copy code

```
ALTER DYNAMIC TABLE dt_orders
    SET INITIALIZATION_WAREHOUSE = nonexistent_wh;
```

```
Object 'NONEXISTENT_WH' does not exist or not authorized.
```

Both WAREHOUSE and INITIALIZATION\_WAREHOUSE require the owner role to have USAGE on the assigned warehouse; without it, the CREATE or ALTER statement fails with the ‘does not exist or not authorized’ error.

## Detect an undersized warehouse

When a warehouse doesn’t have enough memory for a refresh, Snowflake spills intermediate data
to local disk or remote storage. Spilling slows down the refresh and can cause it to exceed its
target lag.

To check for spilling, open the query profile for a recent refresh
([Exploring execution times](/user-guide/performance-query-exploring)) and look at the **Statistics** section. The two
signals to watch are:

- **Bytes spilled to local storage**: The warehouse ran low on memory but handled the overflow
  on local disk. Consider upsizing the warehouse, especially if the refresh duration is close
  to the target lag.
- **Bytes spilled to remote storage**: The warehouse exhausted both memory and local disk.
  If this occurs repeatedly on steady-state incremental refreshes and the refresh duration
  exceeds the target lag, upsize the warehouse. Remote spill during a one-time
  initialization is expected and does not necessarily require a change.

You can also check spill metrics for a specific warehouse in the query history. For a
step-by-step monitoring workflow, see [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).

## Size warehouses for dynamic table workloads

Choose the smallest warehouse that prevents spilling and still meets your target lag. Start
small and scale up based on evidence from refresh history and query profiles. To find how much
data a refresh scans, check the BYTES\_SCANNED column in
DYNAMIC\_TABLE\_REFRESH\_HISTORY or the query profile for a completed refresh.

The following table shows example starting points based on typical workloads.

| Workload | Starting recommendation |
| --- | --- |
| Low-volume incremental refreshes (less than 1 GB scanned per refresh) | X-Small |
| Medium-volume incremental refreshes (1 to 5 GB scanned) | Small |
| High-volume incremental refreshes (more than 5 GB scanned or complex joins) | Medium or larger |
| Initialization of a large table (hundreds of millions of rows) | Large or X-Large |

Expand

Show lessSee more

Note

These are starting points, not guarantees. Optimal warehouse size depends on your query
complexity, data locality, change volume, and concurrency. Monitor refresh history and adjust
based on actual performance.

## Compilation time vs warehouse time

Not all refresh time is warehouse compute. Each refresh has two phases:

1. **Compilation**: Snowflake plans the refresh, identifies changed partitions, and
   generates the execution plan. Compilation runs on Cloud Services, not the warehouse. A
   larger warehouse doesn’t reduce compilation time.
2. **Warehouse execution**: The warehouse runs the refresh computation. A larger
   warehouse can reduce this phase through more memory and parallelism.

When most of the refresh time is spent in compilation, upsizing the warehouse won’t help.
Check the query profile to see how time is split between the two phases. If compilation
dominates, consider simplifying the definition or reducing the number of base tables.

## Isolate dynamic table workloads on dedicated warehouses

Use dedicated warehouses for dynamic table refreshes to achieve the following outcomes:

- **Cost isolation**: You can attribute all credits on a warehouse to a specific pipeline or
  team. This simplifies cost monitoring because spill and duration metrics reflect only the
  dynamic table workload.
- **No resource contention**: Ad-hoc queries and other workloads don’t compete with refreshes
  for warehouse resources.
- **Predictable sizing**: You can right-size the warehouse for the dynamic table workload
  without affecting other users.

Set AUTO\_SUSPEND to a short interval (for example, 60 seconds) on dedicated refresh
warehouses to avoid paying for idle time between refreshes. Snowflake
automatically resumes the warehouse when a refresh is dispatched.

When multiple dynamic tables share a warehouse and refreshes queue, consider a
[multi-cluster warehouse](/user-guide/warehouses-multicluster) to handle concurrency. Multi-cluster warehouses add clusters when queries queue and remove them when demand drops. They require Enterprise Edition or higher.

## What’s next

- To monitor refresh performance and diagnose bottlenecks, see [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).
- To understand how refresh modes affect performance, see [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes).
- To optimize your dynamic table queries for incremental refresh, see
  [Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization).
- For general warehouse sizing guidance, see [Increasing warehouse size](/user-guide/performance-query-warehouse-size).
