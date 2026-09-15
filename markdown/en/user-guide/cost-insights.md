# Using Optimization insights to save

Snowflake provides Optimization insights that identify opportunities to optimize Snowflake for cost within a particular account. These insights are
calculated and refreshed weekly.

Each insight indicates how many credits or terabytes could be saved by optimizing Snowflake.

To access the **Optimization insights** tile:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with [access to Optimization insights](/user-guide/cost-account-overview#label-account-overview-cost-insights-privileges).
3. In the navigation menu, select **Admin** » **Cost management**.
4. Select the **Account Overview** tab.
5. Find the **Optimization insights** tile.

Each of the following insights includes suggestions on how to optimize your spend.

- [Insight: Rarely used tables with automatic clustering](/user-guide/cost-insights#label-cost-optimize-insight-clustering)
- [Insight: Rarely used materialized views](/user-guide/cost-insights#label-cost-optimize-insight-mv)
- [Insight: Rarely used search optimization paths](/user-guide/cost-insights#label-cost-optimize-insight-so)
- [Insight: Large tables that are never queried](/user-guide/cost-insights#label-cost-optimize-insight-large-tables)
- [Insight: Tables over 100 GB from which data is written but not read](/user-guide/cost-insights#label-cost-optimize-insight-never-read)
- [Insight: Short-lived permanent tables](/user-guide/cost-insights#label-cost-optimize-insight-temp-tables)
- [Insight: Active warehouses with large gaps between successive queries](/user-guide/cost-insights#label-cost-optimize-insight-gaps-in-queries)
- [Insight: Inefficient usage of multi-cluster warehouses](/user-guide/cost-insights#label-cost-optimize-insight-multi-cluster-wh)
- [Insight: Tables with significant cold file storage](/user-guide/cost-insights#label-cost-optimize-insight-cold-storage)

Insight: Rarely used tables with automatic clustering
:   This insight identifies tables with [automatic clustering](/user-guide/tables-auto-reclustering) that are queried fewer than 100
    times per week by this account.

    Enabling automatic clustering for a table can significantly improve the performance of queries against that table. However, as the table
    changes, Snowflake must use serverless compute resources to keep it in a well-clustered state. If the number of queries executed against
    the table is minimal, the cost incurred might not justify the performance improvements.

    **Recommendation:**
    Consider disabling automatic clustering on these tables. Before you turn off automatic clustering, determine whether the table exists
    solely for disaster recovery purposes or for use by other Snowflake accounts through data sharing, which might explain why it isn’t
    accessed frequently.

    For example, to disable automatic clustering for a table named `t1`, execute the following command:

    Copy code

    ```
    ALTER TABLE t1 SUSPEND RECLUSTER;
    ```

Insight: Rarely used materialized views
:   This insight identifies [materialized views](/user-guide/views-materialized) that are queried fewer than 10 times per week by this
    account.

    Creating a materialized view can significantly improve performance for certain query patterns. However, materialized views incur
    additional storage costs as well as serverless compute costs associated with keeping the materialized view up to date with new data. If
    the number of queries executed against the materialized view is minimal, the cost incurred might not justify the performance improvements.

    **Recommendation:**
    Consider removing or suspending updates to the materialized views. Before you drop a materialized view, determine whether the materialized view exists
    solely for disaster recovery purposes or for use by other Snowflake accounts through data sharing, which might explain why it isn’t
    accessed frequently.

    For example, to delete a materialized view named `mv1`, execute the following command:

    Copy code

    ```
    DROP MATERIALIZED VIEW mv1;
    ```

Insight: Rarely used search optimization paths
:   This insight identifies [search optimization](/user-guide/search-optimization-service) access paths that are used fewer than
    10 times per week by this account.

    Search optimization uses search access paths to improve the performance of certain types of point lookup and analytical queries. Adding
    search optimization to a table can significantly improve performance for these queries. However, search optimization incurs additional
    storage costs as well as serverless compute costs associated with keeping that storage up to date. If the number of queries that use the
    search access path created by search optimization is minimal, the cost incurred might not justify the performance improvements.

    **Recommendation:**
    Consider removing search optimization from the table. Before you remove search optimization, determine whether the table exists solely
    for disaster recovery purposes or for use by other Snowflake accounts through data sharing, which might explain why it isn’t accessed
    frequently.

    For example, to completely remove search optimization from a table named `t1`, execute the following command:

    Copy code

    ```
    ALTER TABLE t1 DROP SEARCH OPTIMIZATION;
    ```

Insight: Large tables that are never queried
:   This insight identifies large tables that have not been queried in the last week by this account.

    **Recommendation:**
    Consider deleting unused tables, which can reduce storage costs without impacting any workloads. Before you drop the tables, determine
    whether the table exists solely for disaster recovery purposes or for use by other Snowflake accounts through data sharing, which might
    explain why it isn’t accessed frequently.

    For example, to delete a table named `t1`, execute the following command:

    Copy code

    ```
    DROP TABLE t1;
    ```

Insight: Tables over 100 GB from which data is written but not read
:   This insight identifies tables over 100 GB where data is written but never read by this account.

    **Recommendation:**
    It might be wasteful to store data and ingest new data into Snowflake if the data is never read. Consider dropping these tables to save on
    storage costs or stop writing new data to save on credits consumed by ingestion. Before you drop the tables, determine whether the table
    exists solely for disaster recovery purposes or for use by other Snowflake accounts through data sharing, which might explain why it
    isn’t being read.

    For example, to drop a table named `t1`, execute the following command:

    Copy code

    ```
    DROP TABLE t1;
    ```

Insight: Short-lived permanent tables
:   This insight identifies tables over 100 GB that were deleted within 24 hours of their creation.

    **Recommendation:** If data needs to be persisted for only a short time, consider using a
    [temporary table or transient table](/user-guide/tables-temp-transient) for future tables. Using a temporary table or transient
    table might help you save on [Fail-safe and Time Travel costs](/user-guide/data-cdp-storage-costs).

    For example, to create a new transient table `t1`, execute the following command:

    Copy code

    ```
    CREATE TRANSIENT TABLE t1;
    ```

Insight: Active warehouses with large gaps between successive queries
:   An active warehouse consumes credits even if it isn’t executing any queries. This insight identifies warehouses that are idle
    (not executing queries) more than 50% of the time that they are active.

    **Recommendation:**
    Consider lowering the auto-suspend setting, which determines how long a warehouse remains idle before suspending. Suspended warehouses
    don’t incur costs. To optimize costs, you might set auto-suspend to 5 minutes or lower.

    Keep in mind that lowering the auto-suspend time limit can occasionally make query performance worse by reducing cache usage. For more
    information, see [About the cache and auto-suspension](/user-guide/performance-query-warehouse-cache#label-performance-query-cache-auto-suspend).

    For example, to set the auto-suspend time limit to 1 minute for a warehouse named `wh1`, execute the following command:

    Copy code

    ```
    ALTER WAREHOUSE wh1 AUTO_SUSPEND = 60;
    ```

Insight: Inefficient usage of multi-cluster warehouses
:   This insight identifies when you have the minimum and maximum cluster count set to the same value for a multi-cluster warehouse, which
    prevents the warehouse from scaling up or down to respond to demand. If your multi-cluster warehouse can scale down during periods of
    lighter usage, it can save credits.

    **Recommendation:** Consider lowering the minimum cluster count to allow the multi-cluster warehouse to scale down during periods of
    lighter usage.

    For example, to set the minimum cluster count to 1 for a warehouse named `wh1`, execute the following command:

    Copy code

    ```
    ALTER WAREHOUSE wh1 SET MIN_CLUSTER_COUNT = 1;
    ```

Insight: Tables with significant cold file storage
:   This insight identifies tables with 100 GB or more of cold (unaccessed) file storage. Cold files are files within a table that have
    not been accessed by any query in one year. Storing large amounts of cold data at standard storage rates can lead to unnecessary costs.

    **Recommendation:**
    Consider creating a [storage lifecycle policy](/user-guide/storage-management/storage-lifecycle-policies) to automatically move
    infrequently accessed data to a lower-cost archive storage tier.

    For example, to create a storage lifecycle policy that archives rows older than 365 days, and then attach it to a table named `t1`:

    Copy code

    ```
    CREATE STORAGE LIFECYCLE POLICY archive_cold_data
      AS (event_ts TIMESTAMP)
      RETURNS BOOLEAN ->
        event_ts < DATEADD(DAY, -365, CURRENT_TIMESTAMP())
      ARCHIVE_TIER = COLD
      ARCHIVE_FOR_DAYS = 730;

    ALTER TABLE t1 ADD STORAGE LIFECYCLE POLICY archive_cold_data
      ON (created_at);
    ```

    For more information, see [Storage lifecycle policy commands](/sql-reference/commands-storage-lifecycle-policies).
