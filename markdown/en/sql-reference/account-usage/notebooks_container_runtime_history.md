Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# NOTEBOOKS\_CONTAINER\_RUNTIME\_HISTORY view

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

You can use the NOTEBOOKS\_CONTAINER\_RUNTIME\_HISTORY view in the ACCOUNT\_USAGE schema to return the hourly credit usage for notebooks running on Snowpark Container Services within the last 365 days (1 year).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the usage took place. |
| NOTEBOOK\_NAME | VARCHAR | The name of the notebook (running on Snowpark Container Services) that incurred the credit usage. |
| NOTEBOOK\_ID | NUMBER | The ID of the notebook that incurred the credit usage. |
| USER\_NAME | VARCHAR | The name of the user associated with the notebook. NULL if the notebook was not run interactively. |
| USER\_ID | NUMBER | The ID of the user associated with the notebook. NULL if the notebook was not run interactively. |
| COMPUTE\_POOL\_NAME | VARCHAR | The name of the compute pool associated with the notebook. |
| COMPUTE\_POOL\_ID | NUMBER | The ID of the compute pool associated with the notebook. |
| SERVICE\_NAME | VARCHAR | The name of the service associated with the notebook. |
| SERVICE\_ID | NUMBER | The ID of the service associated with the notebook. |
| NOTEBOOK\_EXECUTION\_TIME\_SECS | NUMBER | The run time of the notebook in the given hour. |
| CREDITS | NUMBER(38, 9) | The number of credits that the notebook used in the hour. |

Expand

Show lessSee more

## Usage notes

- Latency for the view might be up to 180 minutes (3 hours).

- The view provides hourly container notebook credit usage for an account within the last 365 days (1 year).
- The credit rate usage is determined based on the machine type (instance family) of the compute pool, as outlined in the consumption table.
