Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# OPENFLOW\_USAGE\_HISTORY view

This Account Usage view returns the hourly runtime credit usage for an account within the last 365 days (1 year).

Note

This view returns records only for Openflow BYOC deployments. It doesn’t return records for Openflow Snowflake
Deployments, which are billed under the *OPENFLOW\_COMPUTE\_SNOWFLAKE* service type. To track the cost of an Openflow
Snowflake Deployment, see [Openflow Snowflake Deployment cost and scaling considerations](/user-guide/data-integration/openflow/cost-spcs).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the usage took place. |
| DATA\_PLANE\_ID | VARCHAR | ID of the data plane which incurred the credit usage. |
| DATA\_PLANE\_TYPE | VARCHAR | Type of the data plane. The only value currently returned is *BYOC*. |
| DATA\_PLANE\_CREDITS\_USED | NUMBER | Number of compute credits the data plane used in the hour. This value is always 0, because *BYOC* data planes run on infrastructure you manage and incur no Snowflake compute credits. For *BYOC*, you’re charged credits only for runtime usage. |
| RUNTIME\_KEY | VARCHAR | Key identifying the runtime which incurred the credit usage. |
| RUNTIME\_NAME | VARCHAR | Name of the runtime which incurred the credit usage. |
| RUNTIME\_CREDITS\_USED | NUMBER | Number of compute credits the runtime used in the hour. This does not include the credits used by the data plane or the credits used to ingest the data in Snowflake. |

Expand

Show lessSee more
