Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# MATERIALIZED\_VIEW\_REFRESH\_HISTORY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

[Enterprise Edition Feature](/user-guide/intro-editions)

Materialized views require Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

The MATERIALIZED\_VIEW\_REFRESH\_HISTORY view in the ORGANIZATION\_USAGE
schema is used for querying the
[materialized views](/user-guide/views-materialized) refresh history for
a specified materialized view within a specified date range. The information
returned by the function includes the view name and credits consumed each time
a materialized view is refreshed.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_NAME | VARCHAR | Name of the account (user-defined). |
| ACCOUNT\_LOCATOR | VARCHAR | Locator of the account (system-defined). |
| REGION | VARCHAR | Name of the region where the account is located. |
| USAGE\_DATE | DATE | Date (in the UTC time zone) of this refresh history record. |
| CREDITS\_USED | NUMBER | Number of credits billed for materialized view maintenance during the USAGE\_DATE. |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the materialized view. |
| TABLE\_NAME | VARCHAR | Name of the materialized view. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the materialized view. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the materialized view. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the materialized view. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the materialized view. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours (1 day).
- The data is retained for 365 days (1 year).
