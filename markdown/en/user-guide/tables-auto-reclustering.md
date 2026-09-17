# Automatic Clustering

Automatic Clustering is the Snowflake service that seamlessly and continually manages all reclustering, as needed, of clustered tables.
Automatic Clustering includes two versions:

- **Optima Clustering**: Snowflake’s next-generation autonomous table optimization engine. Optima Clustering optimizes tables for query
  performance with zero manual maintenance and predictable, ingestion-based billing.
- **Clustering Classic**: The previous Automatic Clustering behavior. Clustering Classic continues to run for tables that are already
  clustered.

Starting September 1, 2026, newly clustered tables use Optima Clustering. Tables that are already clustered remain on Clustering Classic. You don’t need to take any action for the rollout. This change isn’t a breaking change: tables continue to see equivalent or
better clustering performance.

Note that, after a clustered table is defined, reclustering does not necessarily start immediately. Snowflake only reclusters a clustered table if it will benefit from the
operation.

Note

If manual reclustering is still available in your account, Automatic Clustering might not be enabled yet for your account. For more details, see [Manual Reclustering — Deprecated](/user-guide/tables-clustering-manual).

## Optima Clustering

Compared with Clustering Classic, Optima Clustering offers the following advantages:

- Faster time to cluster new data, which can improve query performance on clustered tables.
- A smart clustering algorithm that prioritizes clustering the data that matters most for query performance.
- Highly predictable billing based on data volume ingested, not compute hours. For details, see [Optima Clustering costs](#label-optima-clustering-cost).
- Expanded clustering key length: Optima Clustering can use up to 1 KB total across all clustering key columns. Clustering Classic uses
  only the first 5 bytes of each clustering key column. For more information, see [Clustering Keys & Clustered Tables](/user-guide/tables-clustering-keys).

### Identifying Optima Clustering or Clustering Classic

To determine whether a table uses Optima Clustering or Clustering Classic, call
[SYSTEM$CLUSTERING\_INFORMATION](/sql-reference/functions/system_clustering_information).

To compare costs for each version over time, query the `VERSION` column in
[AUTOMATIC\_CLUSTERING\_HISTORY view](/sql-reference/account-usage/automatic_clustering_history). The column value is `OPTIMA` or `CLASSIC`.

### Moving a table from Clustering Classic to Optima Clustering

Tables that are already clustered remain on Clustering Classic indefinitely. Changing the clustering key with an ALTER TABLE statement
doesn’t move a table to Optima Clustering, and there is no migrate command.

## Benefits of Automatic Clustering

### Ease-of-maintenance

Automatic Clustering eliminates the need for performing any of the following tasks:

- Monitoring the state of clustered tables.

  Instead, as DML is performed on these tables, Snowflake monitors and evaluates the tables to determine whether they would benefit from reclustering, and automatically
  reclusters them, as needed.
- Designating warehouses in your account to use for reclustering.

  Snowflake performs automatic reclustering in the background, and you do not need to specify a warehouse to use.

All you need to do is define a clustering key for each table (if appropriate) and Snowflake manages all future maintenance.

### Full control

You can suspend and resume Automatic Clustering for a clustered table at any time using ALTER TABLE … SUSPEND / RESUME RECLUSTER. While Automatic Clustering is suspended
for a table, the table is never automatically reclustered, regardless of its clustering state and, therefore, does not incur any related credit charges.

For Optima Clustering, suspending immediately stops billing for newly ingested data. When you resume clustering, Snowflake applies a catch-up cost for data ingested while
clustering was suspended. Using suspend and resume primarily to control costs is generally not cost-effective under Optima Clustering. If you want to stop paying for
clustering permanently, drop the clustering key instead.

You can also drop the clustering key on a clustered table at any time, which prevents all future reclustering on the table.

### Non-blocking DML

Automatic Clustering is transparent and does not block DML statements issued against tables while they are being reclustered.

### Optimal efficiency

With Automatic Clustering, Snowflake internally manages the state of clustered tables, as well as the resources (servers, memory, and so on) used for all automated clustering
operations. This allows Snowflake to dynamically allocate resources as needed, resulting in the most efficient and effective reclustering.

Also, Automatic Clustering does not perform any unnecessary reclustering. Reclustering is triggered only when the table would benefit from the operation.

## Enabling Automatic Clustering for a table

In most cases, no tasks are required to enable Automatic Clustering for a table. You simply define a
[clustering key](/user-guide/tables-clustering-keys) for the table.

However, the rule does not apply to tables created by cloning ([CREATE TABLE … CLONE …](/sql-reference/sql/create-clone))
from a source table that has clustering keys. The new table starts with Automatic Clustering suspended, even if Automatic
Clustering for the source table is not suspended. (This is true whether the `CLONE` command cloned the table, the schema
containing the table, or the database containing the table.)

Tip

Before you define a clustering key for a table, consider the following conditions, which may cause reclustering activity (and corresponding credit charges):

- The table is not optimally clustered. For more details, see [Micro-partitions & Data Clustering](/user-guide/tables-clustering-micropartitions).
- The clustering key on the table has changed.

As such, we recommend starting with one or two selected tables and assessing the impact of Automatic Clustering on these tables. Once you are comfortable or familiar with how
Automatic Clustering performs reclustering, you can then define clustering keys for your other tables.

For information about choosing optimal clustering keys, see [Strategies for Selecting Clustering Keys](/user-guide/tables-clustering-keys#label-clustering-keys-strategies).

To add clustering to a table, you must also have USAGE or OWNERSHIP privileges on the schema and database that
contain the table.

## Viewing the Automatic Clustering status for a table

You can use SQL to view whether Automatic Clustering is enabled for a table:

- [SHOW TABLES](/sql-reference/sql/show-tables) command.
- [TABLES](/sql-reference/info-schema/tables) view (in the [Snowflake Information Schema](/sql-reference/info-schema)).
- [TABLES](/sql-reference/account-usage/tables) view (in the [Account Usage](/sql-reference/account-usage) shared database).

The `AUTO_CLUSTERING_ON` column in the output displays the Automatic Clustering status for each table, which can be used to determine whether to suspend or resume Automatic
Clustering for a given table.

In addition, the `CLUSTER_BY` column (SHOW TABLES) or `CLUSTERING_KEY` column (TABLES view) displays the column(s) defined as the clustering key(s) for each table.

## Suspending Automatic Clustering for a table

To suspend Automatic Clustering for a table, use the [ALTER TABLE](/sql-reference/sql/alter-table) command with a `SUSPEND RECLUSTER` clause. For example:

> Copy code
>
> ```
> ALTER TABLE t1 SUSPEND RECLUSTER;
>
> SHOW TABLES LIKE 't1';
>
> +---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+----------+----------------+----------------------+
> |           created_on            | name | database_name | schema_name | kind  | comment | cluster_by | rows | bytes |  owner   | retention_time | automatic_clustering |
> +---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+----------+----------------+----------------------+
> | Thu, 12 Apr 2018 13:29:01 -0700 | T1   | TESTDB        | MY_SCHEMA   | TABLE |         | LINEAR(C1) | 0    | 0     | SYSADMIN | 1              | OFF                  |
> +---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+----------+----------------+----------------------+
> ```

Note

Changing the clustering key of a table resumes automatic clustering, which can result in credit consumption by serverless resources.
Including the word LINEAR in the ALTER TABLE … CLUSTER BY statement is considered a change to the clustering key even if the column
doesn’t change.

## Resuming Automatic Clustering for a table

To resume Automatic Clustering for a clustered table, use the [ALTER TABLE](/sql-reference/sql/alter-table) command with a `RESUME RECLUSTER` clause. For example:

> Copy code
>
> ```
> ALTER TABLE t1 RESUME RECLUSTER;
>
> SHOW TABLES LIKE 't1';
>
> +---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+----------+----------------+----------------------+
> |           created_on            | name | database_name | schema_name | kind  | comment | cluster_by | rows | bytes |  owner   | retention_time | automatic_clustering |
> +---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+----------+----------------+----------------------+
> | Thu, 12 Apr 2018 13:29:01 -0700 | T1   | TESTDB        | MY_SCHEMA   | TABLE |         | LINEAR(C1) | 0    | 0     | SYSADMIN | 1              | ON                   |
> +---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+----------+----------------+----------------------+
> ```

Tip

Before you resume Automatic Clustering on a clustered table, consider the following conditions, which may cause reclustering activity (and corresponding credit charges):

- The table is not optimally clustered (for example, significant DML has been performed on the table since it was last reclustered).
- The clustering key on the table has changed.

For more details, see [Micro-partitions & Data Clustering](/user-guide/tables-clustering-micropartitions) and [Clustering Keys & Clustered Tables](/user-guide/tables-clustering-keys).

## Automatic Clustering costs

Automatic Clustering costs depend on whether a table uses Optima Clustering or Clustering Classic. Both versions bill under the same Auto
Clustering service type.

### Optima Clustering costs

Optima Clustering bills based on the volume of uncompressed data you ingest, not on serverless compute hours. Snowflake calculates the
cost as:

```
Clustering cost = uncompressed GB ingested × per uncompressed GB billing rate × overlap factor
```

For the current per uncompressed GB billing rate, see the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

The overlap factor is a value between `0` and `1` that represents the proportion of ingested data that requires active clustering:

- If all ingested data requires active clustering, the overlap factor is `1`, and the cost is billed at the full per uncompressed GB rate.
- If the data is naturally well clustered on arrival, the overlap factor approaches `0`, and the cost approaches zero.

The overlap factor isn’t shown as a separate rebate on your bill. Your bill shows Optima Clustering credits only.

Examples:

- Append-only workloads clustered by an ingestion timestamp (for example, hourly loads clustered by
  `TO_DATE(ingestion_time)`) typically have an overlap factor near `0` and little or no clustering charge.
- Updates that change clustering key values usually have an overlap factor of `1` and are billed at the full rate.
- Data that partially overlaps existing micro-partitions has an overlap factor between `0` and `1`.

As with Clustering Classic, changing a clustering key triggers a one-time clustering cost. For Optima Clustering, that one-time cost is
based on the existing table size at the time of the key change. Snowflake applies the overlap factor as if the whole table were newly
written data, so a small key change that doesn’t require rewriting much data results in minimal charges.

### Clustering Classic costs

For Clustering Classic, the cost of enabling Automatic Clustering can be broken down into compute costs and storage costs.

Compute costs
:   Snowflake uses [serverless compute resources](/user-guide/cost-understanding-compute#label-serverless-credit-usage) to cluster a table for the first time. It also uses compute resources to maintain that table in a well-clustered state as new data is added to the table. The more changes to a table, the higher the
    maintenance costs.

Storage costs
:   Because Automatic Clustering reorganizes existing data rather than creating additional storage, in many cases there are no additional
    storage costs. However, reclustering can incur additional storage costs if it increases the size of
    [Fail-safe](/user-guide/data-failsafe) storage. For more information, see [Credit and Storage Impact of Reclustering](/user-guide/tables-clustering-keys#label-clustering-keys-reclustering-credit-storage).

### Credit usage and warehouses for Automatic Clustering

Automatic Clustering consumes Snowflake credits, but does not require you to provide a virtual warehouse. Instead, Snowflake internally
manages and achieves efficient resource utilization for reclustering the tables.

Your account is billed only for the actual credits consumed by automatic clustering operations on your clustered tables.

For Clustering Classic credit rates per compute-hour, refer to the “Serverless Feature Credit Table” in the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

Important

After enabling or resuming Automatic Clustering on a clustered table, if it has been a while since the table was reclustered, you may
experience reclustering activity (and corresponding credit charges) as Snowflake brings the table to an optimally clustered state. Once
the table is optimally clustered, the reclustering activity will drop off.

Likewise, defining a clustering key on an existing table or changing the clustering key on a clustered table may trigger reclustering and
credit charges.

To prevent any unexpected credit charges, we recommend starting with one or two selected tables and observing the credit charges
associated with keeping the tables well-clustered as DML is performed. This will help you establish a baseline for the number of credits
consumed by reclustering activity.

### Estimating Automatic Clustering cost

You can call the [SYSTEM$ESTIMATE\_AUTOMATIC\_CLUSTERING\_COSTS](/sql-reference/functions/system_estimate_automatic_clustering_costs) function to help estimate the compute cost of
enabling Automatic Clustering for a table and maintaining the table in a well-clustered state. You can also call the function to help predict
the compute cost of changing the cluster key of a table.

For Optima Clustering, the function supports estimates for one-time costs (for example, enabling clustering or changing a clustering key).
It doesn’t yet return a maintenance cost estimate for Optima Clustering. Optima Clustering maintenance costs are bounded at the per
uncompressed GB billing rate. For the current rate, see the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

Important

The cost estimates returned by the SYSTEM$ESTIMATE\_AUTOMATIC\_CLUSTERING\_COSTS function are best efforts. The actual realized costs can vary by up to 100% (or, in rare cases, several times) from the estimated costs.

### Viewing Automatic Clustering cost

Users with the proper privileges can view the cost of automatic clustering using [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) or SQL:

> Snowsight:
> :   In the navigation menu, select **Admin** » **Cost management**.
>
> SQL:
> :   Query either of the following:
>
>     - [AUTOMATIC\_CLUSTERING\_HISTORY](/sql-reference/functions/automatic_clustering_history) table function (in the [Snowflake Information Schema](/sql-reference/info-schema)).
>     - [AUTOMATIC\_CLUSTERING\_HISTORY view](/sql-reference/account-usage/automatic_clustering_history) (in [Account Usage](/sql-reference/account-usage)).
>
>       Both Optima Clustering and Clustering Classic appear under the Auto Clustering service type. Use the `VERSION` column in
>       AUTOMATIC\_CLUSTERING\_HISTORY to distinguish them (`OPTIMA` or `CLASSIC`).
>
>       The following queries can be executed against the AUTOMATIC\_CLUSTERING\_HISTORY view:
>
>       **Query: Automatic Clustering cost history (by day, by object)**
>
>       This query provides a list of tables with Automatic Clustering and the volume of credits consumed via the service over the last 30 days,
>       broken out by day. Any irregularities in the credit consumption or consistently high consumption are flags for additional investigation.
>
>       Copy code
>
>       ```
>       SELECT TO_DATE(start_time) AS date,
>         database_name,
>         schema_name,
>         table_name,
>         SUM(credits_used) AS credits_used
>       FROM snowflake.account_usage.automatic_clustering_history
>       WHERE start_time >= DATEADD(month,-1,CURRENT_TIMESTAMP())
>       GROUP BY 1,2,3,4
>       ORDER BY 5 DESC;
>       ```
>
>       **Query: Automatic Clustering History & m-day average**
>
>       This query shows the average daily credits consumed by Automatic Clustering grouped by week over the last year. It can help identify
>       anomalies in daily averages over the year so you can investigate spikes or unexpected changes in consumption.
>
>       Copy code
>
>       ```
>       WITH credits_by_day AS (
>         SELECT TO_DATE(start_time) AS date,
>           SUM(credits_used) AS credits_used
>         FROM snowflake.account_usage.automatic_clustering_history
>         WHERE start_time >= DATEADD(year,-1,CURRENT_TIMESTAMP())
>         GROUP BY 1
>         ORDER BY 2 DESC
>       )
>
>       SELECT DATE_TRUNC('week',date),
>             AVG(credits_used) AS avg_daily_credits
>       FROM credits_by_day
>       GROUP BY 1
>       ORDER BY 1;
>       ```
>
>       **Query: Optima Clustering vs Clustering Classic costs (by day)**
>
>       Copy code
>
>       ```
>       SELECT
>           DATE_TRUNC('DAY', START_TIME) AS USAGE_DATE,
>           VERSION,
>           SUM(CREDITS_USED) AS TOTAL_CREDITS
>       FROM SNOWFLAKE.ACCOUNT_USAGE.AUTOMATIC_CLUSTERING_HISTORY
>       WHERE START_TIME >= DATEADD('day', -30, CURRENT_DATE())
>       GROUP BY 1, 2
>       ORDER BY 1 DESC, 2;
>       ```

Note

[Resource monitors](/user-guide/resource-monitors) provide control over virtual warehouse credit usage; however, you cannot use
them to control credit usage for the Snowflake-provided warehouses, including the [![Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png)](/static/images/logo-snowflake-sans-text.png) **AUTOMATIC\_CLUSTERING**
warehouse.
