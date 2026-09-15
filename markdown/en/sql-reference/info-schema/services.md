# SERVICES view

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

This view shows existing Snowpark Container Services services in the database.

## Columns

| Column | Data type | Description |
| --- | --- | --- |
| SERVICE\_CATALOG | TEXT | Database that the service belongs to. |
| SERVICE\_SCHEMA | TEXT | Schema that the service belongs to. |
| SERVICE\_NAME | TEXT | Name of the service. |
| SERVICE\_OWNER | TEXT | Name of the role that owns the service. App instance name if in an app. |
| SERVICE\_OWNER\_ROLE\_TYPE | TEXT | Type of the owner role. |
| COMPUTE\_POOL\_NAME | TEXT | Compute pool where the job was executed. |
| DNS\_NAME | TEXT | DNS name associated with the service. |
| CURRENT\_INSTANCES | NUMBER | The current number of instances for the service. |
| TARGET\_INSTANCES | NUMBER | The target number of service instances that should be running as determined by Snowflake.  When the CURRENT\_INSTANCES value is not equal to the TARGET\_INSTANCES value, Snowflake is either in the process of shutting down or launching service instances.  For example, consider the following:   - Suppose you create a service with MIN\_INSTANCES = 1 and MAX\_INSTANCES = 3. While the service is running, Snowflake might   determine that one instance is not enough. In this case, the value of TARGET\_INSTANCES will increase, indicating Snowflake is in the process of launching additional instances.   It’s also possible that the TARGET\_INSTANCES value is less than the CURRENT\_INSTANCES value, which indicates that Snowflake is in the process of reducing the number of running instances.   - If you create services but the compute pool doesn’t have capacity for the minimum number of instances that you requested, the   value of TARGET\_INSTANCES will be equal to the value of MIN\_INSTANCES. The value of CURRENT\_INSTANCES will be less than the value of TARGET\_INSTANCES. |
| MIN\_READY\_INSTANCES | INT | Minimum service instances that must be ready for Snowflake to consider the service is ready to process requests. |
| MIN\_INSTANCES | INT | Minimum instances for the service. |
| MAX\_INSTANCES | INT | Maximum instances for the service. |
| AUTO\_RESUME | BOOLEAN | Flag that determines if the service can be auto resumed. |
| QUERY\_WAREHOUSE | TEXT | Name of the default query warehouse of the service. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the service. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Last altered time of the service. |
| LAST\_RESUMED | TIMESTAMP\_LTZ | Last resumed time of the service. |
| COMMENT | TEXT | Comment for this service. |
| IS\_JOB | BOOLEAN | `true` if the service is a job service; `false` otherwise. |
| SPEC\_DIGEST | VARCHAR | The unique and immutable identifier representing the service spec content.  To observe the changes to the value of the SPEC\_DIGEST column over time, a service user might execute the SHOW SERVICES command periodically. If the service user notices a change in value, they can infer that the service was upgraded. |
| IS\_UPGRADING | BOOLEAN | TRUE, if Snowflake is in the process of upgrading the service. |
| MANAGING\_OBJECT\_DOMAIN | VARCHAR | The domain of the managing object (for example, the domain of the notebook that manages the service). NULL if the service is not managed by a Snowflake entity. |
| MANAGING\_OBJECT\_NAME | VARCHAR | The name of the managing object (for example, the name of the notebook that manages the service). NULL if the service is not managed by a Snowflake entity. |

Expand

Show lessSee more

## Example

Copy code

```
SELECT *
FROM my_database.information_schema.services
WHERE service_name LIKE '%myservice_%';
```
