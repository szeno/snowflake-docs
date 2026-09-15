Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# COMPUTE\_POOLS view

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Use this view to get a historical view of compute pools (creation, deletion) in your account for the last 365 days.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| NAME | VARCHAR | Compute pool name. |
| ID | NUMBER | Internal, Snowflake-generated identifier for the compute pool. |
| IS\_SUSPENDED | BOOLEAN | Whether the pool is currently suspended. |
| MIN\_NODES | NUMBER | Minimum number of nodes in the compute pool. |
| MAX\_NODES | NUMBER | Maximum number of nodes in the compute pool. |
| INSTANCE\_FAMILY | VARCHAR | Machine type of nodes in the compute pool. |
| AUTO\_SUSPEND\_SECS | NUMBER | Number of seconds of inactivity after which the compute pool is automatically suspended. |
| AUTO\_RESUME | BOOLEAN | Whether the compute pool is automatically resumed when Snowflake attempts to start a service or job. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the compute pool was created. |
| LAST\_RESUMED | TIMESTAMP\_LTZ | Date and time when the suspended compute pool was last resumed. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the compute pool was last updated. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the compute pool was deleted. |
| OWNER | VARCHAR | Role name that owns the compute pool. |
| OWNER\_ROLE\_TYPE | VARCHAR | Type of the role that owns the compute pool. |
| IS\_EXCLUSIVE | BOOLEAN | Whether the compute pool was created for an application. |
| APPLICATION\_NAME | VARCHAR | Application name for which the compute pool was created. Null if the compute pool was not created for an application or if the application no longer exists. |
| APPLICATION\_ID | NUMBER | Application ID for which the compute pool was created. Null if the compute pool was not created for an application. |
| COMMENT | VARCHAR | A comment. |

Expand

Show lessSee more

## Usage notes

- Latency for the view can be up to 180 minutes (3 hours).
