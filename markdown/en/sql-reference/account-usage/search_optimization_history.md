Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SEARCH\_OPTIMIZATION\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view can be used to query the [search](/user-guide/search-optimization-service) history. The information returned by the view includes the search optimization service name and credits consumed by the service.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range. |
| CREDITS\_USED | NUMBER | Number of credits billed for the search optimization service during the START\_TIME and END\_TIME window. |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the search optimization service. |
| TABLE\_NAME | VARCHAR | This is a system-generated alias that contains the ID of the table for which search optimization was enabled; that ID is embedded inside a string of the form “SEARCH OPTIMIZATION ON TABLE\_ID: <optimized\_table\_id>”. For example, if you enable search optimization on a table named `accounts`, and if `accounts` has ID 1200, then the TABLE\_NAME (alias) shown in this column will be “SEARCH OPTIMIZATION ON TABLE\_ID: 1200”. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the search optimization service. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the search optimization service. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the search optimization service. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the search optimization service. |

Expand

Show lessSee more

## Usage notes

- Billing history is not necessarily updated immediately. Latency for the view may be up to 180 minutes (3 hours).

- Remember that the TABLE\_ID column and the TABLE\_NAME column do not refer to the same database object.

  - The TABLE\_ID identifies the search optimization service instance.
  - The TABLE\_NAME shows the table ID of the base table, which is the table

    on which the search optimization service is enabled

    .
- The output contains one row for each search optimization maintenance operation that is executed. Each optimization
  operation updates information about one table. The number of operations executed on each table depends on the number and
  size of updates to the data in that table.

  You can use combinations of aggregate functions and GROUP BY clauses to aggregate costs per table, or across all tables.
- The view shows only base table IDs, not base table names, so the view does not directly show costs associated with base
  tables by name.
- If you want to reconcile the data in this view with a corresponding view in the [ORGANIZATION USAGE schema](/sql-reference/organization-usage), you must first set the timezone of the session to UTC. Before querying the Account Usage view, execute:

  > Copy code
  >
  > ```
  > ALTER SESSION SET TIMEZONE = UTC;
  > ```
