# Evaluate cost for hybrid tables

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

When you use hybrid tables, your account is charged based on two modes of consumption:

- **Hybrid table storage**: Cost for storage of hybrid tables depends on the
  amount of data that you are storing. Storage cost is based on a flat monthly rate per gigabyte (GB).
  See Table 3(b) in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf), which covers unit pricing for hybrid
  table storage.

  Note that hybrid table storage *for the row-store copy of the data* is more expensive than traditional
  Snowflake storage. The copy of the current data in the column store (object storage) is not billed.

  Historical time travel data is billed at standard storage prices.
- **Virtual warehouse compute**: Queries against hybrid tables are executed
  through virtual warehouses. The consumption rate of a warehouse is the same
  for querying hybrid tables as it is for standard tables.
  See [Virtual warehouse credit usage](/user-guide/cost-understanding-compute#label-virtual-warehouse-credit-usage).

## Monitoring storage consumption for hybrid tables

You can view storage usage for hybrid tables and monitor consumption of hybrid table storage credits by querying the following views and functions:

- [STORAGE\_USAGE view](/sql-reference/account-usage/storage_usage) (STORAGE\_BYTES and HYBRID\_TABLE\_STORAGE\_BYTES columns).
- DATABASE\_STORAGE\_USAGE\_HISTORY (AVERAGE\_HYBRID\_TABLE\_STORAGE\_BYTES and AVERAGE\_DATABASE\_BYTES columns):

  - Account Usage [DATABASE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/account-usage/database_storage_usage_history)
  - Organization Usage [DATABASE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/organization-usage/database_storage_usage_history)
  - Information Schema [DATABASE\_STORAGE\_USAGE\_HISTORY](/sql-reference/functions/database_storage_usage_history) function
- [HYBRID\_TABLES view](/sql-reference/account-usage/hybrid_tables) (data per specific hybrid table in the BYTES column).
- [AGGREGATE\_QUERY\_HISTORY view](/sql-reference/account-usage/aggregate_query_history): Monitor virtual warehouse compute resources used during specific queries that are
  executed against hybrid tables. See [Monitor workloads](/user-guide/tables-hybrid-monitor-workload#label-hybrid-tables-monitor-workloads).

## Hybrid table storage for Time Travel data

Consumption for hybrid table storage takes into account the data that is retained by [Time Travel](/user-guide/data-time-travel).
Data retained by Time Travel is included in the following storage metrics:

- STORAGE\_BYTES column in the [STORAGE\_USAGE view](/sql-reference/account-usage/storage_usage)
- AVERAGE\_DATABASE\_BYTES column in DATABASE\_STORAGE\_USAGE\_HISTORY:
  - Account Usage [DATABASE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/account-usage/database_storage_usage_history)
  - Organization Usage [DATABASE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/organization-usage/database_storage_usage_history)
  - Information Schema [DATABASE\_STORAGE\_USAGE\_HISTORY](/sql-reference/functions/database_storage_usage_history) function

Data retained by Time Travel is stored in object storage, not the row store, and is charged at the standard table rate,
not the higher hybrid table rate.
