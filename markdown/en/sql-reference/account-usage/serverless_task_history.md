Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SERVERLESS\_TASK\_HISTORY view

This Account Usage view can be used to query the [serverless task](/user-guide/tasks-intro#label-tasks-compute-resources) usage history. The information
returned by the view includes the serverless task name and credits consumed by serverless task usage.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range. |
| CREDITS\_USED | VARCHAR | Number of credits billed for serverless task usage during the START\_TIME and END\_TIME window. |
| TASK\_ID | NUMBER | Internal/system-generated identifier for the serverless task. |
| TASK\_NAME | VARCHAR | Name of the serverless task. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the serverless task. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the serverless task. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the serverless task. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the serverless task. |
| INSTANCE\_ID | NUMBER | Internal/system-generated identifier for the instance which the object belongs to. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
