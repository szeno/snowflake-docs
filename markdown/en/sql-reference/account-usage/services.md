Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SERVICES view

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

This SERVICES view in the Account Usage schema is similar to the SERVICES view in the information schema, except this view includes services that have been deleted. For more information about the differences in these schemas, see
[Differences between Account Usage and Information Schema](/sql-reference/account-usage#label-differences-between-account-usage-and-information-schema).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| SERVICE\_ID | NUMBER | Internal/system-generated identifier for the service. |
| SERVICE\_NAME | VARCHAR | Name of the service. |
| SERVICE\_CATALOG\_ID | NUMBER | Internal, Snowflake-generated identifier of the database for the service. |
| SERVICE\_CATALOG | VARCHAR | Database that the service belongs to. |
| SERVICE\_SCHEMA\_ID | NUMBER | Internal, Snowflake-generated identifier of the schema for the service. |
| SERVICE\_SCHEMA | VARCHAR | Schema that the service belongs to. |
| SERVICE\_OWNER | VARCHAR | Name of the role that owns the service. App instance name if in an app. |
| SERVICE\_OWNER\_ROLE\_TYPE | VARCHAR | Type of the owner role. |
| COMPUTE\_POOL\_ID | NUMBER | Identifier of the compute pool that runs the service. |
| COMPUTE\_POOL\_NAME | VARCHAR | Name of the compute pool that runs the service. |
| DNS\_NAME | VARCHAR | DNS name associated with the service. |
| MIN\_READY\_INSTANCES | NUMBER | Minimum service instances that must be ready for Snowflake to consider the service ready to process requests. |
| MIN\_INSTANCES | NUMBER | Minimum instances for the service. |
| MAX\_INSTANCES | NUMBER | Maximum instances for the service. |
| AUTO\_RESUME | BOOLEAN | Flag that determines if the service can be auto resumed. |
| QUERY\_WAREHOUSE | VARCHAR | Name of the default query warehouse of the service. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the service. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Last altered time of the service. |
| LAST\_RESUMED | TIMESTAMP\_LTZ | Last resumed time of the service. |
| LAST\_SUSPENDED | TIMESTAMP\_LTZ | Last suspended time of the service. |
| AUTO\_SUSPEND\_SECS | NUMBER | Number of seconds of inactivity after which the service is automatically suspended. |
| DELETED | TIMESTAMP\_LTZ | Deletion time of the service. |
| COMMENT | VARCHAR | Comment for this service. |
| IS\_JOB | BOOLEAN | `true` if the service is a job service; `false` otherwise. |
| IS\_ASYNC\_JOB | BOOLEAN | `true` if the service is an asynchronous job service; `false` otherwise. |

Expand

Show lessSee more

## Example

Copy code

```
SELECT *
FROM snowflake.account_usage.services
WHERE service_name LIKE '%myservice%';
```
