# Manual Reclustering — *Deprecated*

Deprecated Feature

As of May, 2020, manual reclustering has been deprecated for all accounts.

If manual reclustering is still available in your account, you can use the [ALTER TABLE](/sql-reference/sql/alter-table) command with a `RECLUSTER` clause to manually recluster
a clustered table at any time.

## What is Manual Reclustering?

The `RECLUSTER` clause instructs Snowflake to perform immediate reclustering of the specified table. Unlike Automatic Clustering, this DML operation requires a virtual
warehouse in your account and locks the table for the duration of the operation.

Also, after a period of significant/sustained DML activity on a clustered table that does not have Automatic Clustering enabled, manual reclustering may need to be performed
multiple times on the table to achieve the desired results.

For these reasons, as well as other benefits, we recommend using [Automatic Clustering](/user-guide/tables-auto-reclustering) instead of manual reclustering.

Tip

As a general rule of thumb and best practice, we recommend manual reclustering after performing significant DML on a clustered table. You can use the
[clustering information](/sql-reference/functions/system_clustering_information) for the table to measure whether clustering on the table has degraded due to DML.

## Performance Impact of Manual Reclustering

The grouping/sorting that Snowflake performs during manual reclustering can impact the performance of the virtual warehouse used to perform the reclustering.

Due to this impact, if you choose to perform manual reclustering, we recommend using a separate, dedicated warehouse, and ensuring that the warehouse is of sufficient size.

## Switching from Manual Reclustering to Automatic Clustering

If manual reclustering is still available in your account, [Automatic Clustering](/user-guide/tables-auto-reclustering) may not be enabled yet for your account.

You can request Automatic Clustering to be enabled for your account; however, it will only affect clustered tables that are defined from the time after the feature is
enabled.

For clustered tables that were defined before the feature is enabled, you must explicitly “resume” Automatic Clustering for each table. You can use SQL to determine whether
Automatic Clustering is enabled for a given table.

For more details, see:

- [Viewing the Automatic Clustering status for a table](/user-guide/tables-auto-reclustering#label-viewing-auto-clustering).
- [Resuming Automatic Clustering for a table](/user-guide/tables-auto-reclustering#label-resuming-auto-clustering).

## Manually Reclustering a Table

Use [ALTER TABLE](/sql-reference/sql/alter-table) with a `RECLUSTER` clause to manually recluster a table for which a clustering key has been defined. You can use a `WHERE`
clause to specify a condition or range on which to recluster data in the table.

For example:

- To recluster table `t1`:

  Copy code

  ```
  ALTER TABLE t1 RECLUSTER;
  ```
- To recluster data that was inserted into table `t1` in the first week of 2016:

  Copy code

  ```
  ALTER TABLE t1 RECLUSTER WHERE CREATE_DATE BETWEEN ('2016-01-01') AND ('2016-01-07');
  ```

These examples use the current warehouse (for the session) to recluster the table. The amount of resources allocated to manual reclustering is based on the size of the warehouse.
The larger the warehouse, the more resources are allocated to the recluster command, which results in more effective reclustering.

Note

Manual reclustering can only be performed on clustered tables (i.e. tables that have a clustering key defined).
