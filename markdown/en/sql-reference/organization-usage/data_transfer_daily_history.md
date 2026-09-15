Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# DATA\_TRANSFER\_DAILY\_HISTORY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

The DATA\_TRANSFER\_DAILY\_HISTORY view in the ORGANIZATION\_USAGE schema can be used to query the history of data transferred from Snowflake tables into a different cloud storage provider’s network (i.e. from Snowflake on Amazon Web Services (AWS), Google Cloud Platform, or Microsoft Azure into the other cloud provider’s network) and/or geographical region within the last 365 days (1 year).

The view includes the history of data transfer for all accounts in your Snowflake organization.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| SERVICE\_TYPE | VARCHAR | Either `DATA_TRANSFER` or [INTERNAL\_DATA\_TRANSFER](/developer-guide/snowpark-container-services/accounts-orgs-usage-views#label-spcs-data-transfer-cost). |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization . |
| ACCOUNT\_NAME | VARCHAR | Name of the account. |
| USAGE\_DATE | DATE | Date (in the UTC time zone) in which the usage took place. |
| TB\_TRANSFERED | FLOAT | Number of terabytes transferred during the USAGE\_DATE. |
| REGION | VARCHAR | ID of the Snowflake Region where the account is located. |
| ACCOUNT\_LOCATOR | VARCHAR | Account locator for the account. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
