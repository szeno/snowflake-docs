[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# TABLE\_DML\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view can be used to determine the magnitude and effects of the DML operations performed on a table. Note that
these DML operations include ones initiated by [Snowpipe](/user-guide/data-load-snowpipe-intro) but exclude operations initiated
by background maintenance services
(for example, [Automatic Clustering](/user-guide/tables-auto-reclustering), maintenance for materialized views and
[search optimization](/user-guide/search-optimization-service)).

You can query this view with the [QUERY\_HISTORY view](/sql-reference/organization-usage/query_history) and the
[LOAD\_HISTORY view](/sql-reference/organization-usage/load_history) to identify the DML operations that have a significant impact. This can
help you to identify opportunities for optimization.

In addition, you can query this view with the [AUTOMATIC\_CLUSTERING\_HISTORY view](/sql-reference/organization-usage/automatic_clustering_history) and the
[SEARCH\_OPTIMIZATION\_HISTORY view](/sql-reference/organization-usage/search_optimization_history) to visualize the relationship between these DML operations and the
credits charged for Automatic Clustering and the search optimization service. (These services can be triggered by DML operations.)

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
| START\_TIME | TIMESTAMP\_LTZ | Start of the time range (on the hour mark) during which the DML operations were performed. |
| END\_TIME | TIMESTAMP\_LTZ | End of the time range (on the hour mark) during which the DML operations were performed. |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the table modified by the DML operations. |
| TABLE\_NAME | VARCHAR | Name of the table modified by the DML operations. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the table modified by the DML operations. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the table modified by the DML operations. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the table modified by the DML operations. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the table modified by the DML operations. |
| ROWS\_ADDED | NUMBER | Number of rows added by DML operations performed by users on the table during the START\_TIME and END\_TIME window. |
| ROWS\_REMOVED | NUMBER | Number of rows removed by DML operations performed by users on the table during the START\_TIME and END\_TIME window. |
| ROWS\_UPDATED | NUMBER | Number of rows updated by DML operations performed by users on the table during the START\_TIME and END\_TIME window. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 8 hours.
- This view does not include DML operations on [hybrid tables](/user-guide/tables-hybrid).
