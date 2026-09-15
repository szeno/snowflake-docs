Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# DATA\_TRANSFER\_HISTORY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

The DATA\_TRANSFER\_HISTORY view in the ORGANIZATION\_USAGE schema can be
used to query the history of data transferred from Snowflake tables into a
different cloud storage provider’s network (i.e. from Snowflake on AWS, Google
Cloud Platform, or Microsoft Azure into another cloud provider’s network)
and/or geographical region within a specified date range. The function returns
the history for your entire Snowflake organization.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization where the usage took place. |
| ACCOUNT\_NAME | VARCHAR | Name of the account where the usage took place. |
| ACCOUNT\_LOCATOR | VARCHAR | Name of the account locator. |
| REGION | VARCHAR | Name of the region where the account is located. |
| USAGE\_DATE | DATE | Date (in the UTC time zone) of this transfer history record. |
| SOURCE\_CLOUD | VARCHAR | Name of the cloud provider for the platform where the data transfer originated: Amazon Web Services (AWS), Google Cloud Platform, or Microsoft Azure. |
| SOURCE\_REGION | VARCHAR | Region where the data transfer originated. |
| TARGET\_CLOUD | VARCHAR | Name of the cloud provider for the platform where the data was sent: AWS, Google Cloud Platform, or Microsoft Azure. |
| TARGET\_REGION | VARCHAR | Region where the data was sent. |
| BYTES\_TRANSFERRED | VARIANT | Number of bytes transferred during the usage date. |
| TRANSFER\_TYPE | VARCHAR | Type of operation that caused the transfer. [COPY](/sql-reference/sql/copy-into-location), [COPY\_FILES](/sql-reference/sql/copy-files), [DATA\_LAKE](/user-guide/tables-iceberg), [REPLICATION](/user-guide/account-replication-intro), [EXTERNAL\_FUNCTION](/sql-reference/external-functions), [INTERNAL](/developer-guide/snowpark-container-services/accounts-orgs-usage-views#label-spcs-data-transfer-cost). |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours (1 day).
- The data is retained for 365 days (1 year).
