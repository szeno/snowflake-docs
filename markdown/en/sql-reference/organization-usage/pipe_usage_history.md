Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# PIPE\_USAGE\_HISTORY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

The PIPE\_USAGE\_HISTORY view in the ORGANIZATION\_USAGE schema can be used
to query the history of data loaded into Snowflake tables and Apache Iceberg™ tables using
[Snowpipe](/user-guide/data-load-snowpipe-intro) within a specified date range.
It includes the history of data loaded and credits billed for your
entire Snowflake organization.

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| REGION | VARCHAR | Name of the region where the account is located. |
| PIPE\_ID | NUMBER | Internal/system-generated identifier for the pipe used for the data load. Displays NULL if no pipe name was specified in the query. Each row includes the totals for all pipes in use within the time range. |
| PIPE\_NAME | VARCHAR | Name of the pipe. Displays NULL for the internal (hidden) pipe object used to refresh the metadata for an external table. |
| USAGE\_DATE | DATE | Date (in the UTC time zone) of this usage history record. |
| CREDITS\_USED | NUMBER | Number of credits billed for Snowpipe data loads during the USAGE\_DATE. |
| BYTES\_INSERTED | VARIANT | Number of bytes loaded during the USAGE\_DATE. |
| FILES\_INSERTED | VARIANT | Number of files loaded during the USAGE\_DATE. |
| BYTES\_BILLED | NUMBER | Represents the number of bytes Snowpipe uses for billing purposes, providing visibility into Snowpipe’s cost implications directly within these history views. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours (1 day).
- The data is retained for 365 days (1 year).
