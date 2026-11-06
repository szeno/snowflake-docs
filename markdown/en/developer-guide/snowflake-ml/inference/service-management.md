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

In any distributed system, failures happen. For mission-critical workloads, you can configure your inference service to be resilient against node, zonal, and regional failures. The following table summarizes how to configure for each failure scenario.

| Failure scenario | How to configure |
| --- | --- |
| **Node failure** | Run multiple service instances and over-provision capacity by setting `min_instances` above the minimum required baseline. |
| **Placement group (zone) failure** | Distribute instances across multiple placement groups by running the service on a compute pool with `PLACEMENT_GROUP = 'DISTRIBUTED'`. |
| **Regional failure** | Deploy a second copy in another Snowflake account and region, then route or fail over traffic between the regions. |

Expand

Show lessSee more

### Node failure resilience

To tolerate standard node failures, Snowflake recommends over-provisioning by 50% or maintaining a minimum of 3 instances (whichever is higher).

**Example:** If you need 4 instances to support peak traffic, you should provision 6 instances

### Zonal failure resilience

For workloads that must survive the loss of a full placement group, run the service on a distributed [compute pool](/sql-reference/sql/create-compute-pool). When you set `PLACEMENT_GROUP` to `DISTRIBUTED`, Snowflake attempts to distribute the pool’s nodes across all available placement groups. If one placement group goes down, you don’t lose all the nodes. If a placement group has insufficient capacity, Snowflake provisions nodes in other placement groups, which can result in an uneven distribution. For more information, see [Compute pool placement](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-placement-group).

Combine this with node failure resilience: set `min_instances` so that the instances left after losing one placement group can still carry peak traffic.

#### Convert an existing pool

Warning

You cannot change this setting on an active pool. You must suspend it first.

Copy code

```
ALTER COMPUTE POOL my_pool SUSPEND;

ALTER COMPUTE POOL my_pool
  SET PLACEMENT_GROUP = 'DISTRIBUTED';

ALTER COMPUTE POOL my_pool RESUME;
```

#### Revert an existing pool

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

### Route requests through a gateway

Within a region, send client requests to a [Snowflake Gateway](/developer-guide/snowflake-ml/inference/stable-endpoints-api-reference) rather than directly to a service. The gateway gives clients one stable URL and automatically fails over to healthy endpoints when a target becomes unavailable. You can also use it to split traffic between model versions during a rollout.

### Regional failure resilience

A Snowflake account and its compute pools, services, and gateways all live in one cloud region. To keep serving through a regional outage, deploy the model in a second account in another region and route traffic between the two regions:

1. Create a second account in another region, in the same Snowflake organization.
2. Replicate the database that contains your model registry schema to the second account. Use a replication group for one-way replication, or a failover group if the second account is also your disaster recovery target. Failover groups require Business Critical Edition (or higher). For more information, see [Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro).
3. The replicated database is read-only. Copy the approved version into a local database in the second account so that account owns and serves its own model:

   Copy code

   ```
   CREATE MODEL serving_db.registry.my_model
     WITH VERSION v1
     FROM MODEL replica_db.registry.my_model
     VERSION v1;
   ```

   For more information, see [Using multiple schemas](/developer-guide/snowflake-ml/model-registry/model-management#label-model-management-lifecycle-multiple-schemas).
4. Create the compute pools, services, and gateways in each account, and apply the same node and zonal resilience settings in both regions.
5. Expose a single client-facing endpoint through a global DNS or traffic-management service, such as Amazon Route 53, Azure Traffic Manager, or Google Cloud DNS, and route requests to the healthy regional deployment. Because each account has its own gateway URL and credentials, configure client authentication for both regions in advance.

Tip

Start with active/passive routing and a warm standby: keep the secondary region’s services running at a small `min_instances` and scale up on failover. A cold standby with no running services costs less, but starting services during an outage can take minutes and depends on available capacity. Use active/active routing if you need near-zero failover time or lower latency for clients in both regions.

#### Roll out new model versions in both regions

Clients reach each region through that region’s gateway, so you can roll out a new model version without changing client URLs. In the primary account, promote and deploy the new version as usual. In the secondary account, after the replication refresh brings in the new version:

1. Add the new version to the local model from the replica:

   Copy code

   ```
   ALTER MODEL serving_db.registry.my_model
     ADD VERSION v2
     FROM MODEL replica_db.registry.my_model
     VERSION v2;
   ```
2. Create a service for the new version, using the same compute pool and resilience settings as the primary region.
3. Use `ALTER GATEWAY` to shift traffic from the old version’s service to the new one, the same way you do in the primary region. For more information, see [Stable Endpoints & API Reference](/developer-guide/snowflake-ml/inference/stable-endpoints-api-reference).

To keep both regions serving the same version, run these steps from one CI/CD pipeline, triggered from your Git repository, that deploys to both accounts. For example, each release can promote the version in the primary account, wait for the replication refresh, copy the version into the secondary account, and apply the same service settings and gateway specification in both regions. Store the gateway specifications in Git so that both regions use the same configuration, and fail the release if either region fails. For more information, see [Integrating CI/CD with Snowflake CLI](/developer-guide/snowflake-cli/cicd/integrate-ci-cd).
