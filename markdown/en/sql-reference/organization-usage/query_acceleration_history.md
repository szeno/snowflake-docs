Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# QUERY\_ACCELERATION\_HISTORY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

The QUERY\_ACCELERATION\_HISTORY view in the ORGANIZATION\_USAGE schema is used for querying the history of queries accelerated
by the [query acceleration service](/user-guide/query-acceleration-service). The information returned by the view
includes the warehouse name and the credits consumed by the query acceleration service.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_NAME | VARCHAR | Name of the account (user-defined). |
| ACCOUNT\_LOCATOR | VARCHAR | Account locator of the account (system-defined). |
| REGION | VARCHAR | Name of the region where the account is located. |
| USAGE\_DATE | DATE | Date (in the UTC time zone) when queries were accelerated. |
| CREDITS\_USED | NUMBER | Number of credits billed for the query acceleration service during the USAGE\_DATE. |
| WAREHOUSE\_ID | NUMBER | Internal/system-generated identifier for the warehouse that the queries were executed on. |
| WAREHOUSE\_NAME | VARCHAR | Name of the warehouse that the queries were executed on. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours (1 day).
