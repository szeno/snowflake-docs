# Snowpark Container Services: Working with compute pools

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

A compute pool is a collection of one or more virtual machine (VM) nodes
on which Snowflake runs your Snowpark Container Services services (including job services).
You create a compute pool using the [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool) command.
You then specify it when
[creating a service](/sql-reference/sql/create-service) or [executing a job service](/sql-reference/sql/execute-job-service).

## Creating a compute pool

A compute pool is an account-level construct, analogous to a Snowflake virtual
warehouse. The naming scope of the compute pool is your account.
That is, you cannot have multiple compute pools with the same name in your
account.

The minimum information required to create a compute pool includes the following:

- The machine type (referred to as the [instance family](/developer-guide/snowpark-container-services/instance-families)) to provision for the compute pool nodes
- The minimum nodes to launch the compute pool with
- The maximum number of nodes the compute pool can scale to (Snowflake manages the scaling.)

If you expect a substantial load or sudden bursts of activity on the services you intend to run within your compute pool, you can set a minimum node count greater than 1. This approach ensures that additional nodes are readily available when needed, instead of waiting for autoscaling to start.

Setting a maximum node limit prevents an unexpectedly large number of nodes from being added to your compute pool by Snowflake autoscaling. This can be crucial in scenarios such as unexpected load spikes or issues in your code that might cause Snowflake to allocate a larger number of compute pool nodes than originally planned.

To create a compute pool using [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) or SQL:

Snowsight:
:   1. In the navigation menu, select **Compute** » **Compute Pools**.
    2. Select your username at the bottom of the navigation bar and switch to the ACCOUNTADMIN role, or any role that is allowed to create a compute pool.
    3. Select **+ Compute Pool**.
    4. In the **New compute pool** UI, specify the required information (the compute pool name, the instance family, and the node limit).
    5. Select **Create Compute Pool**.

SQL:
:   Execute the [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool) command.

    For example, the following command creates a one-node compute pool:

    Copy code

    ```
    CREATE COMPUTE POOL tutorial_compute_pool
      MIN_NODES = 1
      MAX_NODES = 1
      INSTANCE_FAMILY = CPU_X64_XS;
    ```

The instance family identifies the type of machine you want to provision
for compute pool nodes. Specifying instance family in
creating a compute pool is similar to specifying warehouse size
(XSMALL, SMALL, MEDIUM, LARGE and so on) when creating a warehouse. The following table lists the available machine types. You can also use the [SHOW COMPUTE POOL INSTANCE FAMILIES](/sql-reference/sql/show-compute-pool-instance-families) command to get this list of available instance families.

### Compute pool placement

A *placement group* is a fault-isolation domain within a Snowflake region, similar to an availability zone (AZ) in AWS or Azure. You can optionally specify which placement group to provision compute pool nodes in by using the `placement_group` parameter in the [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool) statement.

If `placement_group` is not specified, Snowflake places compute pool nodes based on availability, which might span multiple placement groups.

If you choose to specify a `placement_group`, you have two options:

- **Specify a specific placement group:** When you specify `placement_group`, Snowflake provisions all nodes for that pool from the specified placement group. You should set `placement_group` to a specific placement group in the following situations:

  - You need reduced cross-node latency and lower communication costs for highly
    interactive, tightly coupled services.
  - You are building a highly available service and you choose to deploy the same code
    across multiple services, each one running on a separate compute pool that is assigned to a distinct placement group.

  The following guidelines apply when you set a specific placement group for a compute pool:

  - Instance family availability varies by placement group and region. Smaller regions might offer fewer placement group options,
    especially for GPU families. Call the
    [SYSTEM$GET\_INSTANCE\_FAMILY\_PLACEMENT\_GROUPS](/sql-reference/functions/system_get_instance_family_placement_groups) system function to list the placement groups available for
    a specific instance family in your region.
  - Placement group names are consistent within an account across different instance families.
    Different Snowflake accounts might observe different names for the same underlying placement groups.
  - When you configure a placement group for a compute pool, it restricts Snowpark Container Services’ flexibility to
    optimize node placement. This restriction can increase the likelihood of insufficient-capacity errors and lengthen startup times
    during peak demand.
  - You can alter a placement group only if the compute pool is fully suspended and your services
    don’t use block storage.
- **Specify DISTRIBUTED:** When you set `placement_group` to DISTRIBUTED, Snowflake attempts to distribute nodes for that compute pool
  across all available placement groups. You should set `placement_group` to `DISTRIBUTED` if you want to maintain healthy fault tolerance across multiple placement groups. When compute pool nodes are distributed across multiple placement groups, if one placement group goes down, you don’t lose all the nodes.

  The following behaviors apply when you set `placement_group` to DISTRIBUTED for a compute pool:

  - Node distribution: Snowflake uses an equal-partition strategy to spread nodes across all available placement groups in a region. If a
    specific placement group encounters insufficient capacity errors, nodes are provisioned in other placement groups with available capacity, which can result in an uneven distribution.
  - Service instances distribution: When there is more than one service instance, Snowflake attempts to evenly distribute the instances across placement groups.
    Sometimes even distribution can’t be achieved because of constraints, such as capacity limitations.
  - Outage behavior: In the current implementation, if a placement group fails, Snowflake doesn’t automatically fail over nodes to
    healthy placement groups. You should overprovision your service instances (N+1) so that nodes in the remaining placement groups can handle the traffic load during an outage. In the event of placement group outage, Snowflake takes the following actions:
    - Stops placing new service instances in the impacted placement group.
    - Routes ingress traffic to service instances in the healthy placement groups.
    - Recreates service instances in the impacted placement group on the healthy placement groups.

Note

- In smaller Snowflake regions, some instance types might not be available across multiple placement groups, which can reduce the compute pool’s resilience to placement group failures.
- After a placement group recovers, Snowflake doesn’t automatically move service instances back to it; the system gradually rebalances during node upgrades or routine service maintenance.

### Instance families for compute pool nodes

For a complete list of available instance families organized by cloud provider, see
[Instance Families](/developer-guide/snowpark-container-services/instance-families).
You can also use [SHOW COMPUTE POOL INSTANCE FAMILIES](/sql-reference/sql/show-compute-pool-instance-families)
to retrieve current availability and specifications programmatically.

### Autoscaling of compute pool nodes

After you create a compute pool, Snowflake launches the minimum number of nodes
and automatically creates additional nodes up to the maximum allowed. This is
called *autoscaling*. New nodes are allocated when the running nodes
cannot take any additional workload. For example,
suppose that two service instances are running on two nodes
within your compute pool. If you execute another service within
the same compute pool, the additional resource requirements might cause Snowflake to start an additional node.

However, if no services run on a node for a specific duration, Snowflake automatically removes the node, ensuring that the compute pool maintains the minimum required nodes even after the removal.

### Backup instance types

If the primary instance family for a compute pool is capacity-constrained, Snowflake can automatically fall back to a backup instance family that you specify, instead of returning an insufficient capacity error (ICE). To configure this, set the `BACKUP_INSTANCE_FAMILIES` parameter when you [create](/sql-reference/sql/create-compute-pool) or [alter](/sql-reference/sql/alter-compute-pool) a compute pool.

If you have experienced ICEs on a compute pool, or run production workloads in regions where capacity for your instance type is frequently constrained, backup instance types provide automatic failover without manual intervention. Backup families may have different hardware specifications and pricing than the primary; verify compatibility and pricing before configuring.

Each time the pool scales up, Snowflake checks the primary instance type first: if the primary family has capacity, new nodes use it; otherwise, they use a backup family. Snowflake works through the backup list in order, selecting the first family with no recent insufficient capacity error.

Nodes already running on a backup family aren’t swapped immediately when primary capacity returns. They’re replaced with primary-family nodes only as those nodes are cycled, for example during a maintenance window.

Snowflake does not validate workload compatibility between families. For the full list of compatibility requirements, see [BACKUP\_INSTANCE\_FAMILIES in CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool#label-create-compute-pool-backup-instance-families). When choosing backup families, a reliable starting point is to use the next-larger size within the same family. For example, `GEN_X64_G2_8` is a sound backup for a `GEN_X64_G2_4` primary because it shares the same architecture, network capabilities, and local storage ratios while providing more vCPU and memory headroom.

Use [SHOW NODES IN COMPUTE POOL](/sql-reference/sql/show-nodes-compute-pool) to verify backup families are in use: if a node’s `instance_family` value differs from the pool’s configured `INSTANCE_FAMILY`, that node is running on a backup family. Use the `backup_instance_families` column of [SHOW COMPUTE POOLS](/sql-reference/sql/show-compute-pools) to view the configured fallback list.

The pool’s configured `INSTANCE_FAMILY` has no effect on billing; billing is based on the instance type actually provisioned on each node. For example, if your primary is `GEN_X64_G2_4` but a node is provisioned on `GEN_X64_G2_8`, that node is billed at `GEN_X64_G2_8` rates. Because backup families may have different pricing than the primary, use [SHOW NODES IN COMPUTE POOL](/sql-reference/sql/show-nodes-compute-pool) to see the current instance mix, and the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) for rates.

## Managing a compute pool

You can manage a compute pool using [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) or SQL.

In [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in), you choose the more options menu (**…**) next to the compute pool name, and choose the desired operation from the menu. This section explains SQL commands you can use to manage a compute pool.

Snowpark Container Services provides the following commands to manage compute pools:

- **Monitoring:** Use the [SHOW COMPUTE POOLS](/sql-reference/sql/show-compute-pools) command to get information about compute pools.
- **Operating:** Use the [ALTER COMPUTE POOL](/sql-reference/sql/alter-compute-pool) command to change the state of a compute pool.

  Copy code

  ```
  ALTER COMPUTE POOL <name> { SUSPEND | RESUME | STOP ALL }
  ```

  When you suspend a compute pool, Snowflake suspends all services except the job services. The job services continue to run until they reach a terminal state
  (DONE or FAILED), after which the compute pool nodes are released.

  A suspended compute pool must be resumed before you can start a new service. If the compute pool is configured to auto-resume
  (with the AUTO\_RESUME property set to TRUE), Snowflake automatically resumes the pool when a service is submitted to it. Otherwise, you
  need to run the ALTER COMPUTE POOL command to manually resume the compute pool.
- **Modifying:** Use the [ALTER COMPUTE POOL](/sql-reference/sql/alter-compute-pool) command to change compute pool properties.

  Copy code

  ```
  ALTER COMPUTE POOL <name> SET propertiesToAlter = <value>
  propertiesToAlter := { MIN_NODES | MAX_NODES | AUTO_RESUME | AUTO_SUSPEND_SECS | PLACEMENT_GROUP | INSTANCE_FAMILY | BACKUP_INSTANCE_FAMILIES | TAG | COMMENT }
  ```

  When you decrease MAX\_NODES, note the following potential effects:

  - Snowflake might need to terminate one or more service instances and restart them on other available nodes in the compute pool. If
    MAX\_NODES is set too low, Snowflake might be unable to schedule certain service instances.
  - If the node terminated had a job service execution in progress, the job execution will fail. Snowflake will not restart the job service.

    **Example:**

    Copy code

    ```
    ALTER COMPUTE POOL my_pool SET MIN_NODES = 2 MAX_NODES = 2;
    ```
- **Removing:** Use the [DROP COMPUTE POOL](/sql-reference/sql/drop-compute-pool) command to remove a compute pool.
  **Example:**

  Copy code

  ```
  DROP COMPUTE POOL <name>
  ```

  You must stop all running services before you can drop a compute pool.
- **Listing compute pools and viewing properties:** Use SHOW COMPUTE POOLS and DESCRIBE COMPUTE POOL commands. For examples, see [Show Compute Pools](/sql-reference/sql/show-compute-pools).

### About the target\_nodes compute pool property

This section explains the `target_nodes` property with examples. The `target_nodes` property indicates the number of nodes that Snowflake is targeting for your compute pool. If `active_nodes` isn’t equal to the `target_nodes`, Snowflake autoscales the cluster
to add or remove the nodes.

There are several properties related to the number of nodes in a compute pool. These include: `min_nodes`, `max_nodes`, `active_nodes`, `idle_nodes`, and `target_nodes`. For more information about these properties, see [DESC COMPUTE POOL](/sql-reference/sql/desc-compute-pool) and [SHOW COMPUTE POOLS](/sql-reference/sql/show-compute-pools).

The following examples demonstrate how to interpret the values in the `target_nodes` column.

#### Example 1

Suppose in a [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool) command, you specify MIN\_NODES=1 and MAX\_NODES=3.

While Snowflake is provisioning a node, initially the value in the `active_nodes` and `idle_nodes` columns is 0, and the value in the `target_nodes` column is 1. (The value in the `target_nodes` column is the same as the value that you specified for the MIN\_NODES parameter.) This indicates that there should be one node in the compute pool that Snowflake is provisioning.

After Snowflake provisions one node, the value in the `idle_nodes` column is 1 (assuming that there are no services running). The value in the `target_nodes` column is still 1, indicating there should be one node in the compute pool.

#### Example 2

Snowflake might try to add a node to an existing compute pool due to autoscaling or changes to the minimum number of nodes (through [ALTER COMPUTE POOL … SET MIN\_NODES](/sql-reference/sql/alter-compute-pool)).

While Snowflake is provisioning a node, the value in the `state` column is `resizing`. To determine how many nodes Snowflake is adding, check the value in the `target_nodes` column.

For example, suppose that the value in the `active_nodes` column is 1, the value in the `idle_nodes` column is 0, and you resize the compute pool by updating the MIN\_NODES property from 1 to 2. In this case, the value in the `target_nodes` column is 2 (the number of nodes that should be in the compute pool). From this, you can infer that Snowflake is provisioning one additional node.

## Compute pool lifecycle

A compute pool can be in any of the following states:

- **IDLE:** The compute pool has the desired number of virtual machine (VM) nodes, but no
  services are scheduled. In this state, autoscaling can shrink the
  compute pool to the minimum size due to lack of activity.
- **ACTIVE:** The compute pool has at least one service running or
  scheduled to run on it. The pool can grow (up to the maximum nodes) or
  shrink (down to the minimum nodes) in response to load or user actions.
- **SUSPENDED:** The pool currently contains no running virtual machine nodes, but if the AUTO\_RESUME compute pool property is set to TRUE, the pool will automatically resume when a service is scheduled.

The following states are transient:

- **STARTING:** When you create or resume a compute pool, the compute pool enters the STARTING state until at least one node is provisioned.
- **STOPPING:** When you suspend a compute pool (using ALTER COMPUTE POOL), the compute pool enters the STOPPING state until Snowflake has released all nodes in the compute pool. When you suspend a compute pool, Snowflake suspends all services except the job services. The job services continue to run until they reach a terminal state (DONE or FAILED), after which the compute pool nodes are released.
- **RESIZING:** When you create a compute pool, initially it enters the STARTING state. After it has one node provisioned, it enters the RESIZING state until the minimum number of nodes (as specified in CREATE COMPUTE POOL) are provisioned. When you change a compute pool (ALTER COMPUTE POOL) and update the minimum and maximum node values, the pool enters the RESIZING state until the minimum nodes are provisioned. Note that autoscaling of a compute pool also puts the compute pool in the RESIZING state.

For information about the costs incurred during the different states of the compute pool lifecycle, see [Compute pool cost](/developer-guide/snowpark-container-services/accounts-orgs-usage-views#label-compute-pool-cost).

## Compute pool privileges

When you work with compute pools, the following privilege model applies:

- To create a compute pool in an account, the current role needs the
  CREATE COMPUTE POOL privilege on the account. If you create a pool, as an owner you have OWNERSHIP permission, which grants full control over that compute pool. Having OWNERSHIP of one compute pool doesn’t imply any permissions on other compute pools.
- For compute pool management, the following privileges (capabilities)
  are supported:

  | Privilege | Usage |
  | --- | --- |
  | MODIFY | Enables altering any compute pool properties, including changing the size. |
  | MONITOR | Enables viewing compute pool usage, including describing compute pool properties. Enables access to the monitoring endpoint exposed by the compute pool. |
  | OPERATE | Enables changing the state of the compute pool (suspend, resume). In addition, enables stopping any scheduled services (including job services). |
  | USAGE | Enables creating services in the compute pool. Note that when a compute pool is in a suspended state and has its AUTO\_RESUME property set to true, a role with USAGE permission on the compute pool can implicitly trigger the compute pool’s resumption when they start or resume a service, even if the role lacks the OPERATE permission. |
  | OWNERSHIP | Grants full control over the compute pool. Only a single role can hold this privilege on a specific object at a time. Enables access to the monitoring endpoint exposed by the compute pool. |
  | ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the compute pool. |

  Expand

  Show lessSee more

## Compute pool maintenance

As part of routine internal-infrastructure maintenance, Snowflake regularly updates
compute pool nodes to ensure optimal performance and security. This includes
operating system upgrades, driver enhancements, and security fixes. Maintenance
involves replacing outdated nodes with updated ones every few weeks, with each
node active for up to a month.

### Maintenance window

In general, scheduled maintenance occurs every Saturday from 8 PM to Sunday at 8 AM, and every Sunday from 8 PM to Monday at 8 AM, in the timezone of the region where your account is hosted. For [early access accounts](/user-guide/intro-releases#label-releases-early-access-to-full-releases), maintenance takes place daily starting at 11 PM and can last up to 6 hours.

### Service disruption

During maintenance, Snowflake automatically recreates service instances running on older compute pool nodes on the new nodes. Snowflake uses a rolling method to recreate service instances.

- If a service only has one instance, service disruption occurs while Snowflake is recreating the instance.
- For services with multiple instances, Snowflake recreates the service instances incrementally on the upgraded nodes. No more than 50
  percent of the service instances are replaced at a time. Note that this might lead to fewer available instances than the MIN\_INSTANCES
  requested for the service. If the available instances drop to fewer than MIN\_READY\_INSTANCES, it causes the service to transition from
  the READY state to the PENDING state, causing service disruption. Therefore, to avoid service disruption, consider setting
  MIN\_READY\_INSTANCES to less than 50 percent of MIN\_INSTANCES.

Ongoing job services will be disrupted and must be restarted by customers after maintenance is complete.

Attention

Service disruptions during a maintenance window or critical updates are not covered by the Service Level set forth in [Snowflake’s Support Policy and Service Level Agreement](https://www.snowflake.com/legal/support-policy-and-service-level-agreement/).

### Best practices to minimize downtime

- **Run multiple service instances:** Having multiple instances minimizes service disruption during maintenance, ensuring high availability.
- **Store application state in persistent storage:** Store data and stateful objects on persistent storage including block storage, Snowflake stages, or Snowflake tables.
- **Catch the SIGTERM signal:** When terminating a service instance, Snowflake first sends a SIGTERM signal to each service container (see [Terminate service](/developer-guide/snowpark-container-services/working-with-services#label-spcs-working-with-services-service-termination)). As part of processing the signal, the container code can save the service state before the service instance is shut down or restarted.
- **Design high availability services to run in degraded state during maintenance:** To remain available during maintenance, your service must be tolerant to running with only 50% of the instances.
- **Provide a readiness probe:** If you don’t provide a readiness probe, Snowflake assumes your service instance is ready as soon as the code starts executing. Typically it takes some time for a container to complete initialization and be ready to handle requests. You should provide a readiness probe in the service configuration to explicitly tell Snowflake when your service instance is ready to handle requests.
- **Monitor maintenance schedules:** Use [SYSTEM$GET\_COMPUTE\_POOL\_PENDING\_MAINTENANCE](/sql-reference/functions/system_get_compute_pool_pending_maintenance) to check whether maintenance is pending and when the next window begins. Avoid scheduling critical tasks during a maintenance window.
- **Avoid scheduling job service to run during maintenance windows:** Snowflake might cancel a running job during a maintenance window.
- **Perform regular backups or checkpoints:** Periodically back up or checkpoint your application state on persistent storage (including block storage, Snowflake stages, or Snowflake tables).

## How services are scheduled on a compute pool

At the time of [creating a service](/sql-reference/sql/create-service), you might choose to run multiple instances to manage incoming load.
Snowflake uses the following general guidelines when scheduling your service
instances on compute pool nodes:

- All containers in a service instance always run on a single compute pool node.
  That is, a service instance never spans across multiple nodes.
- When you run multiple service instances,
  Snowflake may run these service instances on the same node or different
  nodes within the compute pool. When making this decision, Snowflake considers any specified hard
  resource requirements (such as memory and GPU) as outlined in the
  service specification file (see [`containers.resources` field](/developer-guide/snowpark-container-services/specification-reference#label-spcs-spec-reference-containers-resources-field)).

  For example, suppose each node in your compute pool provides 8 GB of memory.
  If your service specification includes a 6-GB memory requirement, and
  you choose to run two instances when creating a service,
  Snowflake cannot run both instances on the same node. In this case,
  Snowflake schedules each instance on a separate node within the compute pool to fulfill
  the memory requirements.

Note

Snowflake supports stage mounts for use by application containers. Snowflake internal stage is one of the supported storage volume types.

For optimal performance, Snowflake now limits the total number of [stage volume](/developer-guide/snowpark-container-services/snowflake-stage-volume) mounts to eight per compute pool node, regardless of whether these volumes belong to the same service instance, the same service, or different services.

When the limit on a node is reached, Snowflake doesn’t use that node to start new service instances that use a stage volume. If the limit is reached on all nodes in the compute pool, Snowflake will be unable to start your service instance. In this scenario, when you execute the SHOW SERVICE CONTAINERS IN SERVICE command, Snowflake returns PENDING status with the “Unschedulable due to insufficient resources” message.

To accommodate this stage mount allotment limit on a node, in some cases, you can increase the maximum number of nodes that you request for a compute pool. This ensures that additional nodes are available for Snowflake to start your service instances.

## System compute pools

Every Snowflake account includes two system compute pools: one CPU-based and one GPU-based exclusively for the following workloads:

- Notebooks
- Streamlit apps (CPU only)
- Model serving
- ML jobs

With system compute pools, you can run these workloads immediately, no compute pool setup required.

The system compute pools have the following default configuration:

- **Compute pool name:** SYSTEM\_COMPUTE\_POOL\_GPU

  - **Instance family:** Depending on whether your Snowflake account is in AWS or Microsoft Azure regions, Snowflake uses the following GPU [instance family](/developer-guide/snowpark-container-services/instance-families) for this compute pool.

    - In Azure, GPU\_NV\_SM.
    - In AWS, GPU\_NV\_S.

    Note that the following regions do not support SYSTEM\_COMPUTE\_POOL\_GPU:

    - In AWS: Singapore, Switzerland North, Paris, and Osaka.
    - In Azure: Central US.
    - Google Cloud: GPU compute pool isn’t available.
  - **Default configuration:**

    - MIN\_NODES=1
    - MAX\_NODES=50
    - INITIALLY\_SUSPENDED=true
    - AUTO\_SUSPEND\_SECS=600
- **Compute pool name:** SYSTEM\_COMPUTE\_POOL\_CPU

  - **Instance family:** CPU\_X64\_S
  - **Default configuration:**
    - MIN\_NODES=1
    - MAX\_NODES=150
    - INITIALLY\_SUSPENDED=true
    - AUTO\_SUSPEND\_SECS=259200

Note that

- Compute pools are initially in a suspended state and only begin incurring costs when a supported Snowflake workload starts using them.
- For the CPU system compute pool, Snowflake keeps one idle node in the pool at no cost to you whenever the pool is active, so that new workloads can start quickly. The following details apply:

  - The idle node is visible in the `idle_nodes` column of SHOW COMPUTE POOLS and DESCRIBE COMPUTE POOL output.
  - The idle node counts against the compute pool’s MAX\_NODES limit and the per-account node limit.
  - Snowflake covers the cost of one idle node. It doesn’t appear in your billing.
  - When a workload starts on the idle node, that node is billed to you normally and Snowflake provisions a new idle node to replace it.
  - This behavior isn’t configurable. Contact [Snowflake Support](https://community.snowflake.com/s/article/How-To-Submit-a-Support-Case-in-Snowflake-Lodge) if you have questions about this behavior.
- If no workloads are running, the GPU compute pool is automatically suspended after 10 minutes and the CPU compute pool is automatically suspended after 3 days. To modify the auto-suspension policy for system compute pools, use the [ALTER COMPUTE POOL SET AUTO\_SUSPEND\_SECS](/sql-reference/sql/alter-compute-pool) command.

### Managing the system compute pools

In a Snowflake account, the ACCOUNTADMIN role owns these system compute pools. Administrators have full control over the compute pools, including modifying their properties, suspending operations, and monitoring consumption. The ACCOUNTADMIN role can delete the compute pool. For example:

Copy code

```
USE ROLE ACCOUNTADMIN;
ALTER COMPUTE POOL SYSTEM_COMPUTE_POOL_CPU STOP ALL;
DROP COMPUTE POOL SYSTEM_COMPUTE_POOL_CPU;
```

By default, the USAGE permission on system compute pools is granted to the PUBLIC role, allowing all roles in the account to use them. However, the ACCOUNTADMIN can modify these privileges to restrict access if necessary.

To restrict access to system compute pools to specific roles in your account, use the ACCOUNTADMIN role to revoke the USAGE permission from the PUBLIC role and grant it to the desired role(s). For example:

> Copy code
>
> ```
> USE ROLE ACCOUNTADMIN;
> REVOKE USAGE ON COMPUTE POOL SYSTEM_COMPUTE_POOL_CPU FROM ROLE PUBLIC;
> GRANT USAGE ON COMPUTE POOL SYSTEM_COMPUTE_POOL_CPU TO ROLE <role-name>;
> ```

System compute pools can be associated with [budgets](/user-guide/budgets) for cost management.

### Configuring your own preferred compute pools for Streamlit apps

When you create a container-runtime Streamlit app and don’t specify a COMPUTE\_POOL, Snowflake uses
the compute pool specified by the [DEFAULT\_STREAMLIT\_COMPUTE\_POOL](/sql-reference/parameters#label-default-streamlit-compute-pool) parameter. Snowflake
sets this parameter to SYSTEM\_COMPUTE\_POOL\_CPU for new accounts, so Streamlit apps run on the system
compute pool by default. To use a different compute pool, set this account-level parameter.

When DEFAULT\_STREAMLIT\_COMPUTE\_POOL is set, the compute pool selector is not shown in the Snowsight
creation dialog. The app is created on the default compute pool automatically. To use a different
pool, change it after creation using App Settings or ALTER STREAMLIT. See
[Change the compute pool](/developer-guide/streamlit/app-development/managing-your-app#label-streamlit-change-compute-pool).

The following example configures `my_pool` as the default compute pool for Streamlit apps:

Copy code

```
ALTER ACCOUNT SET DEFAULT_STREAMLIT_COMPUTE_POOL='my_pool';
```

To show the compute pool selector in the Snowsight creation dialog, set the parameter to an
empty string:

Copy code

```
ALTER ACCOUNT SET DEFAULT_STREAMLIT_COMPUTE_POOL='';
```

Setting the parameter to an empty string effectively clears it. This is not the same as executing
`ALTER ACCOUNT UNSET DEFAULT_STREAMLIT_COMPUTE_POOL`, which restores the parameter to its
built-in default of `SYSTEM_COMPUTE_POOL_CPU`.

Use the following command to check the current compute pool preference configured in your account for Streamlit apps:

Copy code

```
SHOW PARAMETERS LIKE 'DEFAULT_STREAMLIT_COMPUTE_POOL' IN ACCOUNT;
```

For more information, see [SHOW PARAMETERS](/sql-reference/sql/show-parameters).

### Configuring your own preferred compute pools for Notebooks

By default, Notebook services run in system compute pools. If you don’t want to use the Snowflake-provisioned compute pools, you have the option to choose other compute pools in your account for Notebooks. To override the Snowflake-provisioned compute pools, you can set these parameters ([DEFAULT\_NOTEBOOK\_COMPUTE\_POOL\_CPU](/sql-reference/parameters#label-default-notebook-compute-pool-cpu) and [DEFAULT\_NOTEBOOK\_COMPUTE\_POOL\_GPU](/sql-reference/parameters#label-default-notebook-compute-pool-gpu)). Note that this will change your Snowsight experience. When creating a Notebook in Snowsight, the compute pool you configure using these parameters appears as the first preference in the UI. The following example commands set these parameters:

- Configure `my_pool` as the account-level compute pool preferred for Notebooks using GPU runtime.

  Copy code

  ```
  ALTER ACCOUNT SET DEFAULT_NOTEBOOK_COMPUTE_POOL_GPU='my_pool';
  ```
- Configure `my_pool` as the compute pool preferred for Notebooks created in the database `my_db`.

  Copy code

  ```
  ALTER DATABASE my_db SET DEFAULT_NOTEBOOK_COMPUTE_POOL_GPU='my_pool';
  ```
- Configure `my_pool` as the compute pool preferred for Notebooks created in the schema `my_db.my_schema`.

  Copy code

  ```
  ALTER SCHEMA my_db.my_schema SET DEFAULT_NOTEBOOK_COMPUTE_POOL_GPU='my_pool';
  ```

Use the following commands to check the current GPU compute pool preference configured in your account to run Notebooks:

Copy code

```
SHOW PARAMETERS LIKE 'DEFAULT_NOTEBOOK_COMPUTE_POOL_GPU' IN ACCOUNT;

SHOW PARAMETERS LIKE 'DEFAULT_NOTEBOOK_COMPUTE_POOL_GPU' IN DATABASE my_db;

SHOW PARAMETERS LIKE 'DEFAULT_NOTEBOOK_COMPUTE_POOL_GPU' IN SCHEMA my_db.my_schema;
```

For more information, see [SHOW PARAMETERS](/sql-reference/sql/show-parameters).

## Guidelines and limitations

- **CREATE COMPUTE POOL permission:** If you cannot create a compute pool under the current role,
  consult your account administrator to grant permission. For example:

  Copy code

  ```
  GRANT CREATE COMPUTE POOL ON ACCOUNT TO ROLE <role_name> [WITH GRANT OPTION];
  ```

  For more information, see [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege).
- **Per account limit on compute pool nodes**.

  - The maximum number of nodes you can create in your account (regardless of the number of compute pools) is 750.

  In addition, there is a limit on the number of nodes allowed for each instance family (see the **Node limit** column in the [instance family tables](/developer-guide/snowpark-container-services/instance-families)). If you see an error message like `Requested number of nodes <#> exceeds the node limit for the account`, you have encountered these limits. For more information, contact your account representative.
