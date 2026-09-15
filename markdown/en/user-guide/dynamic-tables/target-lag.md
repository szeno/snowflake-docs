# Set the target lag for a dynamic table

Target lag is a staleness target, not a refresh interval. `TARGET_LAG = '10 minutes'` means data should be no more than 10 minutes old, not
refresh every 10 minutes.

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_orders
    TARGET_LAG = '10 minutes'  -- data should be at most 10 minutes stale
    WAREHOUSE = transform_wh
    REFRESH_MODE = INCREMENTAL
AS
    SELECT ... FROM raw_orders ...;
```

For the full `dt_orders` definition, see [Create a dynamic table](/user-guide/dynamic-tables/create).

Target lag is best-effort, not a guarantee

Snowflake actively schedules refreshes to meet the target, but actual lag can exceed the target
when warehouse size, data volume, query complexity, or pipeline depth constrain throughput.
Applications should not assume that data is always within the target lag. Monitor actual lag and handle cases where it exceeds the target.
To detect when actual lag exceeds the target, see [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).

## How Snowflake uses target lag

Snowflake uses heuristics to decide when a refresh should start to meet the target lag.

If a refresh is still running when the next one would normally begin, Snowflake waits for it to
complete rather than starting a concurrent refresh of the same table. If refreshes consistently take
longer than the target lag, actual staleness exceeds the target.

The minimum target lag is **60 seconds**. Values below this fail validation. To change the target lag of an existing dynamic table, run `ALTER DYNAMIC TABLE <name> SET TARGET_LAG = '<duration>'`.

### Target lag in multi-table pipelines

When multiple dynamic tables form a pipeline, Snowflake coordinates their refreshes so that each
table processes data in dependency order (upstream tables first). If an upstream table’s data has
not changed since the last refresh, Snowflake can skip refreshing downstream tables that depend on
it. Within a single pipeline refresh cycle, Snowflake maintains snapshot consistency across all
tables, so every downstream table reads a single, coherent point-in-time view of its inputs. For
details on how snapshot isolation works and how to decouple pipelines when full coordination is not
needed, see [Data consistency and pipeline boundaries](/user-guide/dynamic-tables/data-consistency).

## Set TARGET\_LAG = DOWNSTREAM

TARGET\_LAG accepts two forms: a duration string (`'10 minutes'`) or the keyword `DOWNSTREAM`.

DOWNSTREAM (parameter) vs. downstream (direction)

`TARGET_LAG = DOWNSTREAM` is a scheduling parameter that means “don’t refresh on your own schedule;
refresh only when Snowflake determines a downstream consumer needs fresh data.” The word
“downstream” in prose means “a dynamic table that depends on this one.” The parameter is named for
the direction: it tells Snowflake to derive this table’s refresh schedule from its downstream
consumers.

When you set `TARGET_LAG = DOWNSTREAM`, the dynamic table has no independent refresh schedule. It
refreshes only when a downstream dynamic table (one that reads from it) triggers a refresh.
Snowflake uses the shortest target lag among all downstream consumers to determine timing. To set this mode, run `ALTER DYNAMIC TABLE <name> SET TARGET_LAG = DOWNSTREAM`.

For an example of using DOWNSTREAM to coordinate multiple pipelines, see [Synchronize multiple pipelines with a controller table](/user-guide/dynamic-tables/design-patterns#label-dynamic-tables-patterns-controller).

If a dynamic table with `TARGET_LAG = DOWNSTREAM` has no downstream consumers, it never refreshes
automatically, and Snowflake produces no warning about this.

Note

A downstream dynamic table that references this table through `DYNAMIC_TABLE_REFRESH_BOUNDARY()`
creates a soft dependency. Soft dependencies do not count as downstream consumers for scheduling
purposes. If the only downstream consumers use refresh boundaries, a table with
TARGET\_LAG = DOWNSTREAM does not refresh automatically.

## Target lag in a two-table pipeline

Consider two dynamic tables where `dt_orders_daily` reads from `dt_orders`:

| `dt_orders` | `dt_orders_daily` | Behavior |
| --- | --- | --- |
| `TARGET_LAG = DOWNSTREAM` | `TARGET_LAG = '10 minutes'` | Recommended. `dt_orders_daily` refreshes to stay within 10 minutes of freshness. `dt_orders` refreshes on demand whenever `dt_orders_daily` needs it. |
| `TARGET_LAG = '5 minutes'` | `TARGET_LAG = '10 minutes'` | `dt_orders_daily` refreshes within 10 minutes, using data from `dt_orders` that is at most 5 minutes stale. |
| `TARGET_LAG = '10 minutes'` | `TARGET_LAG = DOWNSTREAM` | Avoid. `dt_orders` refreshes every 10 minutes, but `dt_orders_daily` never refreshes because it has no downstream consumers. Queries against `dt_orders_daily` return stale or empty data. |
| `TARGET_LAG = DOWNSTREAM` | `TARGET_LAG = DOWNSTREAM` | Neither table refreshes automatically. Both wait for a downstream consumer that doesn’t exist. Use manual refresh to trigger the pipeline. |
| `TARGET_LAG = '1 hour'` | `TARGET_LAG = '10 minutes'` | Invalid. The downstream table can’t be fresher than its upstream source. Snowflake raises an error. |

Expand

Show lessSee more

Target lag is measured relative to the base tables at the root of the pipeline, not the direct upstream
dynamic table. To see the graph of tables connected to your dynamic table, see [View the pipeline graph in Snowsight](/user-guide/dynamic-tables/monitoring#label-dynamic-tables-monitor-view-graph-snowsight).

## Manually refresh a dynamic table

You can trigger an immediate refresh without waiting for the next scheduled check. This is useful
during development, for one-time refreshes, or when a dynamic table has a long target lag and you need
the data now. To trigger a manual refresh, run `ALTER DYNAMIC TABLE <name> REFRESH`.

Avoid frequent manual refreshes on dynamic tables with downstream consumers that rely on scheduled
refreshes. Manual refreshes can cause Snowflake to skip scheduled checks, which delays downstream
tables.

## SCHEDULER = DISABLE vs. SUSPEND

There are two distinct ways to stop scheduled refreshes: `SUSPEND` (temporary suspension that preserves
configuration) and SCHEDULER = DISABLE (permanent removal from scheduling). For detailed syntax,
examples, and guidance on choosing between them, see
[SCHEDULER = DISABLE vs. SUSPEND](/user-guide/dynamic-tables/manage).

## What’s next

- To optimize target lag for your workload, see [Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization).
- To monitor whether your dynamic tables are meeting their target lag, see [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).
- To understand how refresh modes affect target lag behavior, see [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes).
- To manage dynamic table costs related to target lag, see [Understanding costs for dynamic tables](/user-guide/dynamic-tables/cost).
