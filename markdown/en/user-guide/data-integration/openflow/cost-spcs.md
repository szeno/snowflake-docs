# Openflow Snowflake Deployment cost and scaling considerations

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/user-guide/data-integration/openflow/about-spcs#label-openflow-spcs-available-regions).

When running Openflow - Snowflake Deployment, you must be aware of the cost considerations associated with multiple Snowflake components, including, but not limited to, the following cost categories:

- Compute pool costs
- Snowpark Container Services infrastructure
- Data ingestion
- Telemetry data ingestion
- Other costs not explicitly mentioned in this topic

Using and scaling Openflow involves understanding these costs. The following sections describe Openflow costs in general, and provide a number of examples of scaling Openflow runtimes and associated costs.

## Openflow - Snowflake Deployment costs

When using Openflow - Snowflake Deployment, you can incur costs from multiple Snowflake components that
Openflow uses. These cost categories are described in the following sections.

However, your actual costs may vary based on your specific environment. See [Examples for calculating Openflow - Snowflake Deployment consumption](#label-openflow-spcs-consumption-examples) for examples of different
cost consumption scenarios.

### Openflow compute pool costs

Note

This cost category is shown as **Openflow Compute Snowflake** on your Snowflake bill.

The total costs for running Openflow are based on the number and types of instances used by [Snowpark Container Services compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool) in your Snowflake account.

Openflow uses compute pools for two different purposes:

- Openflow Management Services (a compute pool whose name ends in `_CONTROL_POOL`)

  Openflow Management Services run as part of an Openflow deployment. They
  use a dedicated compute pool to manage the Openflow deployment. This compute pool begins running
  as soon as you create a deployment. It continues to run as long as the deployment is
  active. See [Compute pool naming and per-deployment attribution](#label-openflow-spcs-compute-pool-naming) for how to identify this compute pool.

  Caution

  The compute pool associated with the Openflow Management Services continues to run and incurs costs, even if there are no runtimes running.
- Openflow runtimes

  Openflow uses compute pools to run the Openflow runtimes. The number of compute
  pools required and the number of nodes within each compute pool are scaled based on the
  number of runtimes that are currently running. Snowflake schedules multiple runtime pods per
  compute pool node, so the number of compute pool instances required is typically fewer than the
  total number of runtime nodes.

  When all runtimes associated with a compute pool are stopped, the compute pool associated
  with the runtimes is scaled down to 0 nodes. No costs are incurred for a runtime compute pool when it is not in use.

Credits are billed per-second with a 5-minute minimum. For information on the rate per Snowpark Container Services
Compute Instance Family per hour, refer to Table 1(d) in the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

The following views in the [Account Usage](/sql-reference/account-usage) schema provide additional details on Openflow
compute costs:

- [METERING\_DAILY\_HISTORY](/sql-reference/account-usage/metering_daily_history)
- [METERING\_HISTORY](/sql-reference/account-usage/metering_history)

Compute pool costs related to Openflow appear under *SERVICE\_TYPE* as *OPENFLOW\_COMPUTE\_SNOWFLAKE*. In these rows,
*NAME* returns the name of the compute pool that incurred the cost and *ENTITY\_ID* returns the compute pool’s ID,
which lets you separate Openflow Management Services costs from runtime costs. See
[Compute pool naming and per-deployment attribution](#label-openflow-spcs-compute-pool-naming) for what the compute pool name tells you about attributing costs to a
specific deployment.

Note

The [OPENFLOW\_USAGE\_HISTORY](/sql-reference/account-usage/openflow_usage_history) view currently does not
contain records for the *OPENFLOW\_COMPUTE\_SNOWFLAKE* service type. That view covers Openflow BYOC deployments only.

Per-runtime cost attribution isn’t available for Openflow Snowflake Deployments: runtimes of the same size within a
deployment share the same compute pool. Per-deployment attribution is possible in some cases; see
[Compute pool naming and per-deployment attribution](#label-openflow-spcs-compute-pool-naming).

#### Compute pool naming and per-deployment attribution

Compute pool names follow the pattern `<cluster_name>_CONTROL_POOL`, `<cluster_name>_SMALL`,
`<cluster_name>_MEDIUM`, or `<cluster_name>_LARGE`. The `<cluster_name>` portion depends on when the deployment
was created:

- Most existing deployments use the shared default cluster name `INTERNAL_OPENFLOW_0`, so their compute pools are
  named `INTERNAL_OPENFLOW_0_CONTROL_POOL`, `INTERNAL_OPENFLOW_0_SMALL`, `INTERNAL_OPENFLOW_0_MEDIUM`, and
  `INTERNAL_OPENFLOW_0_LARGE`. **Every Openflow Snowflake Deployment in the account that uses the default cluster
  name shares these same compute pools.**
- Some deployments have a unique, generated cluster name that embeds an internal deployment identifier, for
  example `OPENFLOW_1234567890_SMALL` or `OPENFLOW_A1B2C3D4_E5F6_7890_ABCD_EF1234567890_SMALL`. Each such
  deployment has its own dedicated set of compute pools.

To find out which naming pattern applies to a deployment, check the *NAME* values that
[METERING\_HISTORY](/sql-reference/account-usage/metering_history) returns for *SERVICE\_TYPE* =
*OPENFLOW\_COMPUTE\_SNOWFLAKE*, or run `SHOW COMPUTE POOLS LIKE 'INTERNAL_OPENFLOW%'` and
`SHOW COMPUTE POOLS LIKE 'OPENFLOW%'`.

When every Openflow Snowflake Deployment in an account uses the default cluster name, you can split *management*
(`CONTROL_POOL`) costs from *runtime* (`SMALL`/`MEDIUM`/`LARGE`) costs, but you can’t attribute credits to a
specific deployment, because the pools are shared. When a deployment has a unique generated cluster name, you can
additionally group `METERING_HISTORY` rows by that cluster-name prefix to attribute credits to that deployment; see
[Query: Openflow compute credit consumption per deployment](#label-openflow-spcs-cost-openflow-per-deployment-query).

Snowflake doesn’t currently provide a documented `SHOW` command or Account Usage view that maps a generated
cluster name back to the deployment name that created it. Contact Snowflake Support if you need that mapping.

For more information on compute costs in Snowflake, see [Exploring compute cost](/user-guide/cost-exploring-compute).

#### Viewing Openflow compute costs in Snowsight

To view Openflow compute costs in [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in):

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with [access to cost and usage data](/user-guide/cost-access-control).
3. In the navigation menu, select **Admin** » **Cost management**.
4. Select a warehouse to use to view the usage data.
5. Select **Consumption**.
6. Select **Compute** from the Usage Type drop-down.
7. Select **By Service** and look for **Openflow Compute Snowflake**.

#### Query: Daily Openflow compute credit consumption

The following query returns daily credit consumption for Openflow compute over the last 30 days. Because
[METERING\_DAILY\_HISTORY](/sql-reference/account-usage/metering_daily_history) aggregates by *SERVICE\_TYPE*, this
returns one total per day for all Openflow Snowflake Deployment compute in the account; it doesn’t break out
individual compute pools or deployments. Use the hourly queries that follow for that level of detail.

Copy code

```
SELECT TO_DATE(usage_date) AS date,
  service_type,
  SUM(credits_used) AS credits_used
FROM snowflake.account_usage.metering_daily_history
WHERE service_type = 'OPENFLOW_COMPUTE_SNOWFLAKE'
  AND usage_date >= DATEADD(month, -1, CURRENT_TIMESTAMP())
GROUP BY 1, 2
ORDER BY 1 DESC;
```

#### Query: Hourly Openflow compute credit consumption by compute pool

The following query returns hourly credit consumption for Openflow compute, including the compute pool name and
ID. Use *NAME* to separate management (`_CONTROL_POOL`) costs from runtime pool costs, and to identify peak-usage
periods:

Copy code

```
SELECT start_time,
  name,
  entity_id,
  service_type,
  credits_used_compute
FROM snowflake.account_usage.metering_history
WHERE service_type = 'OPENFLOW_COMPUTE_SNOWFLAKE'
  AND start_time >= DATEADD(month, -1, CURRENT_TIMESTAMP())
ORDER BY start_time DESC;
```

#### Query: Openflow compute credit consumption per deployment

The following query groups Openflow compute credit consumption by `cluster_name`, the shared prefix of each
compute pool’s *NAME* (everything before the trailing `_CONTROL_POOL`, `_SMALL`, `_MEDIUM`, or `_LARGE`):

Copy code

```
SELECT
  REGEXP_REPLACE(name, '_(CONTROL_POOL|SMALL|MEDIUM|LARGE)$', '') AS cluster_name,
  SUM(credits_used_compute) AS credits_used
FROM snowflake.account_usage.metering_history
WHERE service_type = 'OPENFLOW_COMPUTE_SNOWFLAKE'
  AND start_time >= DATEADD(month, -1, CURRENT_TIMESTAMP())
GROUP BY 1
ORDER BY 2 DESC;
```

If every row for the account returns the same `cluster_name` (for example, `INTERNAL_OPENFLOW_0`), every Openflow
Snowflake Deployment in the account shares the same compute pools and this query can’t separate their costs.
Distinct `cluster_name` values identify separate deployments; see
[Compute pool naming and per-deployment attribution](#label-openflow-spcs-compute-pool-naming).

### Snowpark Container Services infrastructure costs

In addition to compute pool costs, there are costs associated with additional Snowpark Container Services infrastructure, including storage and data transfer.

For additional information, see [Snowpark Container Services costs](/developer-guide/snowpark-container-services/accounts-orgs-usage-views).

### Data ingestion costs

Costs are incurred when loading data into Snowflake using services such as Snowpipe or Snowpipe Streaming. These costs are based on the volume of data ingested.

Note

These costs appear on your Snowflake bill under their respective ingestion service line items (for example, **Pipe** for Snowpipe or **Snowpipe Streaming** for Snowpipe Streaming).

Additionally, some connectors may require a warehouse and will incur warehouse costs. For example, database CDC connectors require a warehouse for both the
initial snapshots and ongoing incremental Change Data Capture (CDC).

### Telemetry data ingestion costs

Note

This cost category is shown as **Telemetry Data Ingest** on your Snowflake bill.

When using an event table to store telemetry data for Openflow, Snowflake charges
for sending logs and metrics to Openflow deployments. There are also charges for
sending runtime telemetry data to your event table within Snowflake.

The rate for credits per GB of telemetry data is specified in Table 5 in the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
This item is referred to as Telemetry Data Ingest.

## Reducing Openflow credit consumption

The following strategies can help you lower your Openflow credit consumption.

### Suspend idle runtimes

If you have runtimes that are not actively in use, suspend them. Suspending a runtime
stops credit consumption for the associated runtime compute pool. When a runtime is suspended, its compute pool
scales down to 0 nodes and no longer incurs charges.

### Choose the smallest runtime type that meets your workload

Each runtime type maps to a different compute pool instance family with different per-hour credit rates.
A Small runtime uses a CPU\_X64\_S instance, a Medium runtime uses CPU\_X64\_SL, and a Large runtime uses CPU\_X64\_L.
Selecting the smallest runtime type that satisfies your workload’s CPU and memory requirements avoids paying for
unused capacity. See [the runtime-to-compute-pool mapping](#label-openflow-spcs-scaling-overview) for details.

### Set appropriate maximum node limits

Openflow scales compute pool nodes based on CPU consumption, up to the maximum node setting you specify
during runtime creation. Setting a lower maximum node limit caps how much a runtime can scale out, which directly
limits your peak compute cost. Evaluate your workload’s actual scaling needs and avoid setting the maximum higher
than necessary.

### Minimize the number of active deployments

The Openflow Management Services compute pool runs continuously as long as the deployment is active, even
if no runtimes are running. Each deployment incurs this fixed cost (1 CPU\_X64\_S instance). If you have
multiple deployments that could be consolidated, reducing the number of active deployments eliminates
redundant management pool charges.

### Manage telemetry data volume

Snowflake charges per GB of telemetry data ingested into your event table. If your runtimes generate
high volumes of logs and metrics, consider adjusting your telemetry configuration to reduce the volume
of data sent to the event table. The per-GB rate is specified in Table 5 of the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

### Right-size warehouses for CDC connectors

Database CDC connectors require a warehouse for both initial snapshots and ongoing incremental Change Data
Capture. Choose an appropriately sized warehouse to avoid over-provisioning compute for these operations.

## Openflow - Snowflake Deployment costs associated with runtimes and scaling behavior

How you choose to configure and scale runtimes is important for managing costs effectively. Openflow supports different runtime types, each with its own scaling characteristics and associated costs.

### Mapping runtimes to Snowflake compute pools

The runtime type you choose determines the runtime pods that are scheduled on the associated compute pool. Using a larger runtime type will result in a larger compute pool being used, which will incur higher costs.

The runtime sizes and their scaling behavior are described in the following table:

| Runtime type | vCPUs | Available memory (GB) | Snowflake Compute Pool instance family | Snowflake Compute Pool | Instance Family - vCPUs | Instance Family - memory (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| Small | 1 | 2 | CPU\_X64\_S | INTERNAL\_OPENFLOW\_0\_SMALL | 4 | 16 |
| Medium | 4 | 10 | CPU\_X64\_SL | INTERNAL\_OPENFLOW\_0\_MEDIUM | 16 | 64 |
| Large | 8 | 20 | CPU\_X64\_L | INTERNAL\_OPENFLOW\_0\_LARGE | 32 | 128 |

Expand

Show lessSee more

The `INTERNAL_OPENFLOW_0_*` names shown here are the default; some deployments have a different, unique compute
pool name instead. See [Compute pool naming and per-deployment attribution](#label-openflow-spcs-compute-pool-naming) for the full naming pattern.

Openflow scales the underlying Snowflake Compute Pools when additional compute pool
nodes need to be scheduled, based on CPU consumption, up to the maximum node count specified during runtime creation.

Compute pools are configured with a minimum size of 0 nodes and a maximum of 50 nodes. The required size is dynamically adjusted depending on the CPU and memory
requirements of the runtimes.

If there are no resource demands, for example, if the runtime is not running, a compute pool scales down to 0 nodes after 600 seconds (10 minutes).

| Runtime | Activity | Snowflake costs | Cloud costs |
| --- | --- | --- | --- |
| No runtimes | None | Openflow Control Pool x 1 node = 1 CPU\_X64\_S instance-hour | None |
| 1 small runtime (1 vCPU) (min=1 max=2) | Active for 1 hour.  Runtime does not scale to 2. | Openflow Control Pool x 1 node + Small Openflow Compute Pool (CPU\_X64\_S) x 1 node = 2 CPU\_X64\_S instance-hours | None |
| 2 small runtimes (1 vCPU) (min/max=2). 1 large runtime (8 vCPU) (min/max=10). | Small: 4 nodes active for 1 hour. Large: 10 nodes active for 1 hour. | Openflow Control Pool x 1 node + Small Openflow Compute Pool (CPU\_X64\_S) x 2 nodes + Large Openflow Compute Pool (CPU\_X64\_L) x 4 nodes = 3 CPU\_X64\_S instance-hours + 4 CPU\_X64\_L instance-hours | None |
| 1 medium (4 vCPU) (min=1 max=2) | First 20 minutes: 1 node is running. After 20 minutes: scales to 2 nodes. After 40 minutes: scales back to 1 node. Total: 1 hour. | Openflow Control Pool x 1 node + Medium Openflow Compute Pool (CPU\_X64\_SL) x 1 node = 1 CPU\_X64\_S instance-hour + 1 CPU\_X64\_SL instance-hour | None |
| 1 medium (4 vCPU) (min/max=2) | First 30 minutes: 2 nodes running. Suspends after the first 30 minutes. | Openflow Control Pool x 1 node + Medium Openflow Compute Pool (CPU\_X64\_SL) x 1 node x 1/2 hour = 1 CPU\_X64\_S instance-hour + 1/2 CPU\_X64\_SL instance-hour | None |

Expand

Show lessSee more

### Examples for calculating Openflow - Snowflake Deployment consumption

The following examples use the default compute pool names (`INTERNAL_OPENFLOW_0_*`). If your deployment has a
generated cluster name instead, the same math applies to your `<cluster_name>_*` pools; see
[Compute pool naming and per-deployment attribution](#label-openflow-spcs-compute-pool-naming).

You created an Openflow Snowflake Deployment and have not created any runtimes.
:   - The INTERNAL\_OPENFLOW\_0\_CONTROL\_POOL Compute Pool is running with one CPU\_X64\_S instance
    - Total Openflow consumption = 1 CPU\_X64\_S instance-hour

You created one small runtime with Min Nodes = 1 and Max Nodes = 2. Runtime stays at 1 node for 1 hour.
:   - The INTERNAL\_OPENFLOW\_0\_CONTROL\_POOL Compute Pool is running with 1 CPU\_X64\_S instance
    - The INTERNAL\_OPENFLOW\_0\_SMALL Compute Pool is running with 1 CPU\_X64\_S instance
    - Total Openflow consumption = 2 CPU\_X64\_S instance-hours

You created two small runtimes with min/max of two nodes each, and one large runtime with min/max of 10 nodes. These Runtimes are active for one hour.
:   - The INTERNAL\_OPENFLOW\_0\_CONTROL\_POOL Compute Pool is running with 1 CPU\_X64\_S instance

      - Two small runtimes at two nodes = INTERNAL\_OPENFLOW\_0\_SMALL Compute Pool is running with 2 CPU\_X64\_S instances = 2 CPU\_X64\_S instance-hours
      - One large runtime at 10 nodes = INTERNAL\_OPENFLOW\_0\_LARGE Compute Pool is running with 4 CPU\_X64\_L instances = 4 CPU\_X64\_L instance-hours
    - Total Openflow consumption = 3 CPU\_X64\_S instance-hours + 4 CPU\_X64\_L instance-hours

You created one medium runtime with one node. After 20 minutes, it scales to two nodes. After 20 minutes, it scales back down to one node and runs for another 20 minutes.
:   - The INTERNAL\_OPENFLOW\_0\_CONTROL\_POOL Compute Pool is running with 1 CPU\_X64\_S instance
    - One medium runtime scaling up to two nodes = INTERNAL\_OPENFLOW\_0\_MEDIUM Compute Pool is running with 1 CPU\_X64\_SL instance = 1 CPU\_X64\_SL instance-hour
    - Total Openflow consumption = 1 CPU\_X64\_S instance-hour + 1 CPU\_X64\_SL instance-hour

You created one medium runtime with two nodes, then suspended it after 30 minutes.
:   - The INTERNAL\_OPENFLOW\_0\_CONTROL\_POOL Compute Pool is running with 1 CPU\_X64\_S instance
    - One medium runtime at one node = INTERNAL\_OPENFLOW\_0\_MEDIUM Compute Pool is running with 1 CPU\_X64\_SL instance
    - 30 minutes = 1/2 hour
    - Total Openflow consumption = 1 CPU\_X64\_S instance-hour + 1/2 CPU\_X64\_SL instance-hour
