Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# DATA\_TRANSFER\_HISTORY view

This Account Usage view can be used to query the history of data transferred from Snowflake tables into a different cloud storage provider’s network (i.e. from Snowflake on AWS, Google Cloud Platform, or Microsoft Azure into
the other cloud provider’s network) or geographical region within the last 365 days (1 year). The view includes the history for your entire Snowflake account.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range in which the data transfer took place. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range in which the data transfer took place. |
| SOURCE\_CLOUD | VARCHAR | Name of the cloud provider where the data transfer originated: Amazon Web Services (AWS), Google Cloud Platform, or Microsoft Azure. |
| SOURCE\_REGION | VARCHAR | Region where the data transfer originated. |
| TARGET\_CLOUD | VARCHAR | Name of the cloud provider where the data was sent: AWS, Google Cloud Platform, or Microsoft Azure. |
| TARGET\_REGION | VARCHAR | Region where the data was sent. |
| BYTES\_TRANSFERRED | VARIANT | Number of bytes transferred during the START\_TIME and END\_TIME window. |
| TRANSFER\_TYPE | VARCHAR | Type of operation that caused the transfer. [COPY](/sql-reference/sql/copy-into-location), [COPY\_FILES](/sql-reference/sql/copy-files), [DATA\_LAKE](/user-guide/tables-iceberg), [EXTERNAL\_ACCESS](/developer-guide/external-network-access/external-network-access-overview), [EXTERNAL\_FUNCTION](/sql-reference/external-functions), [INTERNAL](/developer-guide/snowpark-container-services/accounts-orgs-usage-views#label-spcs-data-transfer-cost), [POSTGRES](/user-guide/snowflake-postgres/postgres-data-movement), [REPLICATION](/user-guide/account-replication-intro), [SNOWPARK\_CONTAINER\_SERVICES](/developer-guide/snowpark-container-services/accounts-orgs-usage-views#label-spcs-data-transfer-cost). |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).
- If you want to reconcile the data in this view with a corresponding view in the [ORGANIZATION USAGE schema](/sql-reference/organization-usage), you must first set the timezone of the session to UTC. Before querying the Account Usage view, execute:

  > Copy code
  >
  > ```
  > ALTER SESSION SET TIMEZONE = UTC;
  > ```
