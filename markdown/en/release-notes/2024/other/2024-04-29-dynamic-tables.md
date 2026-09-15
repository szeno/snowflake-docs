# April 29, 2024 — Dynamic Tables — *General Availability*

With this release, we are pleased to announce the general availability of dynamic
tables, which are a new table type for continuous processing pipelines. Whether
you’re processing batch data daily or real time data in minutes, dynamic tables
allow you to create data pipelines that are easy to build, operate, and evolve.

With general availability, the following new enhancements are added:

- **Sharing and collaboration**: Dynamic tables can now be
  [shared](/user-guide/dynamic-tables/sharing) across regions and clouds using
  Snowflake’s sharing and collaboration features. This makes it easy to share
  clean, enriched, and transformed data products with consumers in your
  organization, partner organizations, or the broader data cloud community,
  ensuring they stay updated according to your specified cadence.
- **Disaster recovery and replication**: Dynamic tables now support high
  availability through Snowflake’s
  [replication infrastructure](/user-guide/account-replication-considerations#label-replication-and-dynamic-tables). You can
  build your production pipelines with peace of mind knowing that you’re supported
  with Snowflake’s disaster recovery solutions.
- **Observability**: New functionality added for better observability via Snowsight
  and programmatic interfaces. In Snowsight, there are new account-level views,
  visibility into [warehouse consumption](/user-guide/dynamic-tables/cost),
  improved [graph](/sql-reference/functions/dynamic_table_graph_history) and
  [refresh history](/sql-reference/functions/dynamic_table_refresh_history),
  and the ability to [suspend and resume refreshes](/sql-reference/sql/alter-dynamic-table).
  Observability functions now include new account usage views, extended retention of
  information schema functions and added support for consistent metadata across
  Snowflake observability interfaces.
- **Data Cloud integrations**: Added support for [clustering](/sql-reference/sql/alter-dynamic-table#label-alter-dynamic-table-clusteringaction),
  [transient](/sql-reference/sql/create-dynamic-table#label-transient-dts) dynamic tables, and governance policies (on
  sources of dynamic tables and dynamic tables themselves), allowing you to benefit
  from the best features of the Snowflake Data Cloud.
- **Scalability**: You can now create four times more dynamic tables in your account,
  and ten times more dynamic table sources feeding into another dynamic table. There
  are no longer any limits on the depth of a directed acyclic graph (DAG) that you can
  create.
- **Query evolution support**: Dynamic tables now automatically filter out new columns
  added to base tables without needing to rebuild the dynamic table, as long as the
  definition of the dynamic table does not use `SELECT *`.
- **New documentation**: We’ve added new articles to our documentation covering
  development best practices,
  [performance optimization guides](/user-guide/dynamic-tables/refresh-optimization),
  [troubleshooting](/user-guide/dynamic-tables/troubleshoot-refreshes) pipeline issues,
  and other improvements.

Additionally, Snowflake has made numerous under-the-hood refinements to enhance refresh
performance, system stability and scalability.

For more information, see [Dynamic tables](/user-guide/dynamic-tables/overview).
