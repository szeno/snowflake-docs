Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SEARCH\_OPTIMIZATION\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view can be used to query maintenance history for indexes maintained by the
[search optimization service](/user-guide/search-optimization-service). The information returned by the view includes the index, the
base table, and the credits consumed by each maintenance operation.

Note

The `INDEX_ID`, `INDEX_NAME`, `INDEX_TYPE`, `BASE_TABLE_ID`, and `BASE_TABLE_NAME` columns replace `TABLE_ID` and `TABLE_NAME` when
[SEARCH\_OPTIMIZATION\_HISTORY views: New columns and column changes (Pending)](/release-notes/bcr-bundles/2026_06/bcr-2384) is enabled. If you have scripts that query `TABLE_ID` or `TABLE_NAME`, update them to use
the new column names.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range. |
| CREDITS\_USED | NUMBER | Number of credits billed for search optimization service index maintenance during the START\_TIME and END\_TIME window. |
| INDEX\_ID | NUMBER | Internal/system-generated identifier for the index. Replaces `TABLE_ID`. |
| INDEX\_NAME | VARCHAR | Name of the index. Replaces `TABLE_NAME`. For a search optimization index, this is a system-generated alias of the form `SEARCH OPTIMIZATION ON: <base_table_id>`. For a search optimization secondary index, this is the customer-defined index name. |
| INDEX\_TYPE | VARCHAR | Type of index maintained by the search optimization service. Possible values are `Search Optimization Index` and `Secondary Index`. `Secondary Index` is not a [hybrid table secondary index](/user-guide/tables-hybrid-index). |
| BASE\_TABLE\_ID | NUMBER | Internal/system-generated identifier for the base table. |
| BASE\_TABLE\_NAME | VARCHAR | Name of the base table. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the base table. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the base table. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the base table. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the base table. |

Expand

Show lessSee more

## Usage notes

- Billing history is not necessarily updated immediately. Latency for the view may be up to 180 minutes (3 hours).

- Use `INDEX_TYPE` to distinguish search optimization index maintenance (`Search Optimization Index`) from search
  optimization secondary index maintenance (`Secondary Index`). These values are not
  [hybrid table secondary indexes](/user-guide/tables-hybrid-index).
- `INDEX_ID` identifies the specific index. `INDEX_NAME` is a system-generated alias for a search optimization index
  (`SEARCH OPTIMIZATION ON: <base_table_id>`), or the customer-defined name for a search optimization secondary index.
- `BASE_TABLE_ID` and `BASE_TABLE_NAME` identify the table that the index is defined on.
- The output contains one row for each maintenance operation that is executed. Each operation updates information about
  one index. The number of operations executed on each index depends on the number and size of updates to the data in
  the base table.

  You can use combinations of aggregate functions and GROUP BY clauses to aggregate costs per index, per base table, or
  across all tables.
- If you want to reconcile the data in this view with a corresponding view in the [ORGANIZATION USAGE schema](/sql-reference/organization-usage), you must first set the timezone of the session to UTC. Before querying the Account Usage view, execute:

  > Copy code
  >
  > ```
  > ALTER SESSION SET TIMEZONE = UTC;
  > ```
