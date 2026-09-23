Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SEARCH\_OPTIMIZATION\_HISTORY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

The SEARCH\_OPTIMIZATION\_HISTORY view in the ORGANIZATION\_USAGE schema
is used for querying maintenance history for indexes maintained by the
[search optimization service](/user-guide/search-optimization-service). The information returned
by the view includes the index, the base table, and the credits consumed each
time a maintenance operation occurred.

Note

The `INDEX_ID`, `INDEX_NAME`, `INDEX_TYPE`, `BASE_TABLE_ID`, and `BASE_TABLE_NAME` columns replace `TABLE_ID` and `TABLE_NAME` when
[SEARCH\_OPTIMIZATION\_HISTORY views: New columns and column changes (Pending)](/release-notes/bcr-bundles/2026_06/bcr-2384) is enabled. If you have scripts that query `TABLE_ID` or `TABLE_NAME`, update them to use
the new column names.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization where the usage took place. |
| ACCOUNT\_NAME | VARCHAR | Name of the account where the usage took place. |
| ACCOUNT\_LOCATOR | VARCHAR | Name of the account locator. |
| REGION | VARCHAR | Name of the region where the account is located. |
| USAGE\_DATE | DATE | Date (in the UTC time zone) of this usage record. |
| CREDITS\_USED | NUMBER | Number of credits billed for search optimization service index maintenance during the USAGE\_DATE. |
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

- Latency for the view may be up to 24 hours (1 day).
- Use `INDEX_TYPE` to distinguish search optimization index maintenance (`Search Optimization Index`) from search
  optimization secondary index maintenance (`Secondary Index`). These values are not
  [hybrid table secondary indexes](/user-guide/tables-hybrid-index).
- `INDEX_ID` identifies the specific index. `INDEX_NAME` is a system-generated alias for a search optimization index
  (`SEARCH OPTIMIZATION ON: <base_table_id>`), or the customer-defined name for a search optimization secondary index.
- `BASE_TABLE_ID` and `BASE_TABLE_NAME` identify the table that the index is defined on.
