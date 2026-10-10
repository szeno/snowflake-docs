[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SNOWPIPE\_STREAMING\_CLIENT\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view can be used to query the amount of time spent loading data into Snowflake tables using [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview) within the last 365 days (1 year). The view displays the amount of data loaded and timestamp of the Snowpipe Streaming client calls for accounts in your organization.

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
| CLIENT\_NAME | VARCHAR | Name of the Snowpipe Streaming ingest client. |
| SNOWFLAKE\_PROVIDED\_ID | VARCHAR | Internal/system-generated identifier for the Snowpipe Streaming ingest client used for the data load. |
| EVENT\_TIMESTAMP | TIMESTAMP\_LTZ | Start of the time (in the local time zone) range in which data loading took place. |
| EVENT\_TYPE | VARCHAR | Type of the event. |
| BLOB\_SIZE\_BYTES | NUMBER | The blob size in bytes. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 240 minutes (4 hours).
