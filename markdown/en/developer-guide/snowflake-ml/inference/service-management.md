# Service Management & Scaling

Once a model is deployed to Snowpark Container Services (SPCS), you must manage its lifecycle, resource consumption, and reliability. This page covers standard operations, observability, and configuring high availability for production workloads.

## Managing services

Snowpark Container Services offers a SQL interface for managing services. You can use the DESCRIBE SERVICE and ALTER SERVICE commands with SPCS services created by Snowflake Model Serving just as you would for managing any other SPCS service. For example, you can:

- Change MIN\_INSTANCES and other properties of a service
- Drop (delete) a service
- Share a service to another account
- Change ownership of a service (the new owner must have READ access to the model)

Note

If the owner of a service loses access to the underlying model for any reason, the service stops working after a restart. It will continue running until it is restarted.

To ensure reproducibility and debugability, you cannot change the specification of an existing inference service. You can, however, copy the specification, customize it, and use the customized specification to create your own service to host the model. However, this method does not protect the underlying model from being deleted. Furthermore, it does not track lineage. It is best to allow Snowflake Model Serving to create services.

## Scaling services

Note

Starting with snowflake-ml-python 1.25.0, you can define the scaling boundaries for your inference service by setting min\_instances and max\_instances within the create\_service method.

### How Autoscaling Works

The service initializes with the number of nodes specified in min\_instances and dynamically scales within your defined range based on real-time traffic volume and hardware utilization.

**Scale-to-Zero (Auto-Suspend):** If min\_instances is set to 0 (the default), the service will automatically suspend if no traffic is detected for 30 minutes.

**Scaling Latency:** Scaling triggers typically activate after one minute of meeting the required condition. Note that total spin-up time includes this trigger period plus the time required to provision and initialize new service instances.

### Configuration Best Practices

| Parameter | Recommended Strategy |
| --- | --- |
| min\_instances | Set to 1 or more for production workloads to ensure immediate availability and avoid cold-start delays. |
| max\_instances | Set to accommodate peak demand while maintaining a ceiling on resource consumption and cost. |

Expand

Show lessSee more

## Suspending services

The default min\_instances=0 setting allows the service to auto-suspend after 30 minutes of inactivity. Incoming requests will trigger a resume, with the total delay determined by compute pool availability and the model’s loading time (startup delay).

To manually suspend or resume a service, use the ALTER SERVICE command.

Copy code

```
ALTER SERVICE my_service [ SUSPEND | RESUME ];
```

## Deleting models

You can manage models and model versions as usual with either the SQL interface or the Python API, with the restriction that a model or model version that is being used by a service (whether running or suspended) cannot be dropped (deleted). To drop a model or model version, drop the service first.

## Monitoring services

When running models in Snowpark Container Services, you can monitor service health and troubleshoot issues by accessing container logs and metrics. Model serving services generate logs that can help you understand service behavior, diagnose errors, and optimize performance.

For comprehensive information about monitoring SPCS services, including accessing metrics and logs, see [Monitoring services](/developer-guide/snowpark-container-services/monitoring-services).

### In Snowsight

You can monitor model serving services in Snowsight:

1. In the navigation menu, select **Monitoring » Services & jobs**.
2. On the **Services** tab, select your service to view the service details page.
3. The **Overview** tab displays service information including the compute pool, endpoints, and instance count.
4. The **Logs**, **Metrics**, and **Events** tabs provide logs, performance metrics, and service events (such as instance provisioning and shutdowns). Filter results by instance and container name as needed.

### Accessing service logs

You can access logs for your model serving services using any of the following methods:

#### Using the service helper function

Model serving include a built-in helper function that retrieves logs from the event table for running or suspended services (the caller must have at least the MONITOR privilege on the service):

Copy code

```
-- Retrieve logs using the service helper function
SELECT * FROM TABLE(mydb.myschema.my_model_service!SPCS_GET_LOGS())
WHERE
timestamp > dateadd(hour, -1, current_timestamp())
AND instance_id = 0  -- choose all instances or one particular
AND container_name = 'model-inference';
```

#### Querying the event table directly

If you have an event table configured for your account, you can query it directly to retrieve service logs:

Copy code

```
-- Find the event table for your account
SHOW PARAMETERS LIKE 'event_table' IN ACCOUNT;

-- Query the event table for model service logs
SELECT TIMESTAMP, RESOURCE_ATTRIBUTES, RECORD_ATTRIBUTES, VALUE
FROM <current_event_table_for_your_account>
WHERE timestamp > dateadd(hour, -1, current_timestamp())
    AND RESOURCE_ATTRIBUTES:"snow.service.name" = '<model_service_name>'
    AND RECORD_TYPE = 'LOG'
    AND RESOURCE_ATTRIBUTES:"snow.service.container.instance" = '0'  -- choose all instances or one particular
    AND RESOURCE_ATTRIBUTES:"snow.service.container.name" = 'model-inference'
ORDER BY timestamp DESC
LIMIT 10;
```

#### Using the system function (Running instances only)

For real-time debugging of active containers you can use the SYSTEM$GET\_SERVICE\_LOGS function:

Copy code

```
-- Retrieve logs from a specific service instance
SELECT SYSTEM$GET_SERVICE_LOGS('model_service_name', '0', 'model-inference', 10);
```

Note

The container name for model inference services is model-inference. For troubleshooting image build issues, use model-build as the container name.

### Accessing service metrics

Model serving services emit performance and health metrics that can help you monitor resource utilization, request rates, latency, and other operational characteristics. These metrics are captured in the event table and can be queried to analyze service performance over time.

For more information about SPCS service metrics, see [Accessing event table service metrics](/developer-guide/snowpark-container-services/monitoring-services).

#### Using the service helper function

Model serving services include a built-in helper function that retrieves metrics from the event table for running or suspended services:

Copy code

```
-- Retrieve metrics using the service helper function
SELECT *
FROM TABLE(mydb.myschema.my_model_service!SPCS_GET_METRICS())
WHERE
timestamp > dateadd(hour, -1, current_timestamp())
AND instance_id = 0  -- choose all instances or one particular
AND container_name = 'model-inference';
```

#### Querying the event table directly

You can query the event table directly to retrieve and filter specific metrics:

Copy code

```
-- Find the event table for your account
SHOW PARAMETERS LIKE 'event_table' IN ACCOUNT;

-- Query the event table for model service metrics
SELECT
    timestamp,
    RESOURCE_ATTRIBUTES:"snow.service.container.instance" as instance,
    RESOURCE_ATTRIBUTES:"snow.service.container.name" as container,
    RECORD:metric:"name" as metric,
    value
FROM my_event_table_db.my_event_table_schema.my_event_table
WHERE timestamp > DATEADD(hour, -1, CURRENT_TIMESTAMP())
    AND RESOURCE_ATTRIBUTES:"snow.service.name" = '<model_service_name>'
    AND RECORD_TYPE = 'METRIC'
    AND RESOURCE_ATTRIBUTES:"snow.service.container.instance" = '0'  -- choose all instances or one particular
    AND RESOURCE_ATTRIBUTES:"snow.service.container.name" = 'model-inference'
ORDER BY timestamp DESC
LIMIT 100;
```

## Fault tolerance

In any distributed system, failures happen. For mission-critical workloads it is on users to configure the service to be resilient against node and zonal failures.

### Node Failure Resilience

To tolerate standard node failures, Snowflake recommends over-provisioning by 50% or maintaining a minimum of 3 instances (whichever is higher).

**Example:** If you need 4 instances to support peak traffic, you should provision 6 instances

### Zonal Failure Resilience

For mission-critical workloads that require resilience against a full zonal failure, you can use a distributed [compute pool](/sql-reference/sql/create-compute-pool) when creating a [service](/sql-reference/sql/create-service). Distributed compute pools are created with the PLACEMENT\_GROUP parameter set to DISTRIBUTED. For more information about distributed compute pools, see [Compute pool placement](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-placement-group).

### Configuration Guide

#### Convert an Existing Pool

Warning

You cannot change this setting on an active pool. You must suspend it first.

Copy code

```
ALTER COMPUTE POOL my_pool SUSPEND;

ALTER COMPUTE POOL my_pool
  SET PLACEMENT_GROUP = 'DISTRIBUTED';

ALTER COMPUTE POOL my_pool RESUME;
```

#### Revert an Existing Pool

Warning

You cannot change this setting on an active pool. You must suspend it first.

Copy code

```
ALTER COMPUTE POOL my_pool SUSPEND;

ALTER COMPUTE POOL my_pool
  UNSET PLACEMENT_GROUP;

ALTER COMPUTE POOL my_pool RESUME;
```

#### Verification

To confirm your pool is correctly configured for HA, check the placement\_group column:

Copy code

```
DESCRIBE COMPUTE POOL my_service_pool;
```
