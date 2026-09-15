Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SEARCH\_OPTIMIZATION\_HISTORY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

The SEARCH\_OPTIMIZATION\_HISTORY view in the ORGANIZATION\_USAGE schema
is used for querying
the [search optimization service](/user-guide/search-optimization-service)
maintenance history for a specified table within a specified date range. The
information returned by the function includes the table name and credits
consumed each time a search optimization maintenance operation occurred.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization where the usage took place. |
| ACCOUNT\_NAME | VARCHAR | Name of the account where the usage took place. |
| ACCOUNT\_LOCATOR | VARCHAR | Name of the account locator. |
| REGION | VARCHAR | Name of the region where the account is located. |
| USAGE\_DATE | DATE | Date (in the UTC time zone) of this usage record. |
| CREDITS\_USED | NUMBER | Number of credits billed for the search optimization service during the USAGE\_DATE. |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the search optimization service. |
| TABLE\_NAME | VARCHAR | This is a system-generated alias that contains the ID of the table for which search optimization was enabled; that ID is embedded inside a string of the form “SEARCH OPTIMIZATION ON TABLE\_ID: <optimized\_table\_id>”. For example, if you enable search optimization on a table named `accounts`, and if `accounts` has ID 1200, then the TABLE\_NAME (alias) shown in this column will be “SEARCH OPTIMIZATION ON TABLE\_ID: 1200”. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the search optimization service. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the search optimization service. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the search optimization service. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the search optimization service. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours (1 day).
