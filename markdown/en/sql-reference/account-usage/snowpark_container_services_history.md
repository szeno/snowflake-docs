Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SNOWPARK\_CONTAINER\_SERVICES\_HISTORY view

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

The SNOWPARK\_CONTAINER\_SERVICES\_HISTORY view in the ACCOUNT\_USAGE schema can be used to return the hourly
[compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool) credit usage for an account within the last 365 days (1 year).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the usage took place. |
| COMPUTE\_POOL\_NAME | VARCHAR | Name of the compute pool which incurred the credit usage. |
| COMPUTE\_POOL\_ID | NUMBER | Internal, Snowflake-generated identifier of the compute pool which incurred the credit usage. |
| IS\_EXCLUSIVE | BOOLEAN | TRUE, if the compute pool was created for an [application](/developer-guide/native-apps/native-apps-about). |
| APPLICATION\_NAME | VARCHAR | The name of the application for which the compute pool was created. NULL if the compute pool was not created for an application or if the application no longer exists. |
| APPLICATION\_ID | NUMBER | The ID of the application for which the compute pool was created; otherwise NULL. |
| CREDITS\_USED | NUMBER | Number of credits the compute pool used in the hour. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- The view provides hourly [compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool) credit usage for an account within the last 365 days (1 year).
- The credit rate usage is determined based on the machine type (instance family) of the compute pool, as outlined in the consumption table.
