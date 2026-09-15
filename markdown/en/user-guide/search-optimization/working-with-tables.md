# Working with search-optimized tables

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Search optimization is generally transparent to users. Queries work the same; some are just faster. However, it is
important to be aware of possible effects of other table operations on the search optimization service, or the reverse.

## Modifying the table

A search access path becomes invalid if the default value of a column is changed.

To use search optimization again after a search access path has become invalid, you must
[drop the SEARCH OPTIMIZATION property](#label-remove-search-optimization-property) and
[add the SEARCH OPTIMIZATION property](/user-guide/search-optimization/enabling#label-search-optimization-service-configuration-entire-table) back to the table.

A search access path remains valid if you add, drop, or rename a column:

- If you enabled search optimization for an entire table without specifying specific columns, then when you add a column to a table, the
  new column is added to the search access path automatically. However, if you used the ON clause when enabling search optimization for a
  column, new columns are not added automatically.
- When you drop a column from a table, the dropped column is removed from the search access path automatically.
- Renaming a column doesn’t require any changes to the search access path.

If you drop a table, the SEARCH OPTIMIZATION property and search access paths are also dropped. Note that:

- Undropping the table immediately reestablishes search optimization as a property of the table.
- When you drop a table, the search access path has the same data retention period as the table.

If you [drop the SEARCH OPTIMIZATION property](#label-remove-search-optimization-property) from the table, the search access
path is removed. When you
[add the SEARCH OPTIMIZATION property](/user-guide/search-optimization/enabling#label-search-optimization-service-configuration-entire-table) back to the table,
the maintenance service needs to recreate the search access path. (There is no way to undrop the property.)

## Cloning the table, schema, or database

If you clone a table, schema, or database, the SEARCH OPTIMIZATION property and search access paths of each table are
also cloned. Cloning a table, schema, or database creates a [zero-copy clone](/user-guide/tables-storage-considerations#label-cloning-tables) of each table
and its corresponding search access paths. However, if the search access path for a table is out-of-date at the time the clone
is created, both the original table and the cloned table incur the maintenance costs for the search optimization service to
update the search access path.

The search access path might be out-of-date if a DML operation significantly modifies a table just before the clone operation. For example,
if an INSERT statement results in a large increase in the size of the original table, the search access path requires maintenance to
reflect this change.

A zero-copy clone isn’t created for search access paths of replicated cloned tables. For more information, see
[Working with tables in a secondary database (database replication support)](#label-search-optimization-replication-support).

To avoid or minimize the costs of search optimization maintenance tasks on the cloned table, follow one or both of these steps:

1. If you need to leave search optimization enabled on the cloned table, verify that the search access path is up-to-date *before*
   executing the CREATE TABLE … CLONE statement. Otherwise, skip to the next step.

   In most cases, you can execute a SHOW TABLES statement and check the value in the SEARCH\_OPTIMIZATION\_PROGRESS column. If the
   column’s value is `100`, the search access path is up-to-date. However, maintenance might be incurred if the search access
   path is being compacted to remove information pertaining to deleted source table data.
2. Disable the search optimization service on the cloned table immediately after the clone is created. For example, to disable
   the search optimization service on table `t1`, execute the following statement:

   Copy code

   ```
   ALTER TABLE t1 DROP SEARCH OPTIMIZATION;
   ```

   For more information, see [Search optimization actions (`searchOptimizationAction`)](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction) in the ALTER TABLE topic.

If you use CREATE TABLE … LIKE to create a new empty table with the same columns as the original table,
the SEARCH OPTIMIZATION property is not copied to the new table.

## Working with tables in a secondary database (database replication support)

If a table in the primary database has the SEARCH OPTIMIZATION property enabled, the property is replicated to the corresponding
table in the secondary database.

Search access paths in the secondary database aren’t replicated but are instead rebuilt automatically. This also applies to
replicated cloned tables. Replication doesn’t create [zero-copy clone](/user-guide/tables-storage-considerations#label-cloning-tables) for cloned search access
paths but fully rebuilds them in the secondary database automatically. Subsequent maintenance on the cloned search access
paths isn’t replicated from the primary database but is performed in the secondary database. This process incurs the same
kinds of costs described in [Search optimization cost estimation and management](/user-guide/search-optimization/cost-estimation#label-search-optimization-maintenance-billing).

## Sharing tables

Data providers can use [Secure Data Sharing](/user-guide/data-sharing-intro) to share tables that have search optimization
enabled.

When querying shared tables, data consumers can benefit from any performance improvements made by the search optimization service.

## Masking policies and row access policies

The search optimization service is fully compatible with tables that use masking policies and row access policies.

However, when search optimization is enabled, a user who is prevented from seeing a value due to a masking policy or row
access policy might be able to deduce with greater certainty whether that value exists. With or without search
optimization, differences in query latency can provide hints about the presence or absence of data restricted by a
policy, which may constitute a security issue depending on the sensitivity of the data. This effect can be magnified by
search optimization since it can make a query that does not return results even faster.

For example, suppose that a row access policy prevents a user from accessing rows with `country = 'US'`, but the data
does not include rows with `country = 'US'`. Now suppose that search optimization is enabled for the `country` column
and that the user runs a query with `WHERE country = 'US'`. The query returns empty results as expected, but the query
might run faster with search optimization than without. In this case, the user can more easily infer that the data does not
contain any rows where `country = 'US'` based on the time taken to run the query.
