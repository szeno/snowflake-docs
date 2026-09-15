Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# STAGE\_STORAGE\_USAGE\_HISTORY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

The STAGE\_STORAGE\_USAGE\_HISTORY view in the ORGANIZATION\_USAGE schema can be
used to query the average daily data storage usage, in bytes, for all
the Snowflake stages in your organization within the last 12 months.

The output includes storage for:

- Named internal stages.
- Default staging areas (for tables and users).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization where the usage took place. |
| ACCOUNT\_NAME | VARCHAR | Name of the account where the usage took place. |
| ACCOUNT\_LOCATOR | VARCHAR | Name of the account locator. |
| REGION | VARCHAR | Name of the region where the account is located. |
| USAGE\_DATE | DATE | Date of this storage usage record. |
| AVERAGE\_STAGE\_BYTES | NUMBER | Number of bytes of stage storage used. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours (1 day).
- The data is retained for 365 days (1 year).
