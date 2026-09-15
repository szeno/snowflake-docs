# Openflow Snowflake Deployment cost and scaling considerations

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

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

- Openflow Management Services (the `Openflow_Control_Pool_0` compute pool)

  Openflow Management Services run as part of an Openflow deployment. They
  use a dedicated compute pool to manage the Openflow deployment. This compute pool begins running
  as soon as you create a deployment. It continues to run as long as the deployment is
  active.

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
*NAME* returns the name of the compute pool that incurred the cost, which lets you separate Openflow Management
Services costs from runtime costs.

Note

The [OPENFLOW\_USAGE\_HISTORY](/sql-reference/account-usage/openflow_usage_history) view currently does not
contain records for the *OPENFLOW\_COMPUTE\_SNOWFLAKE* service type. That view covers Openflow BYOC deployments only.

As a result, per-runtime cost attribution isn’t available for Openflow Snowflake Deployments.

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

The following query returns daily credit consumption for Openflow compute over the last 30 days:

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

#### Query: Hourly Openflow compute credit consumption

The following query returns hourly credit consumption for Openflow compute, useful for identifying peak-usage periods:

Copy code

```
SELECT start_time,
  service_type,
  credits_used
FROM snowflake.account_usage.metering_history
WHERE service_type = 'OPENFLOW_COMPUTE_SNOWFLAKE'
  AND start_time >= DATEADD(day, -7, CURRENT_TIMESTAMP())
ORDER BY 1 DESC;
```

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

You created an Openflow Snowflake Deployment and have not created any runtimes.
:   - The Openflow\_Control\_Pool\_0 Compute Pool is running with one CPU\_X64\_S instance
    - Total Openflow consumption = 1 CPU\_X64\_S instance-hour

You created one small runtime with Min Nodes = 1 and Max Nodes = 2. Runtime stays at 1 node for 1 hour.
:   - The Openflow\_Control\_Pool\_0 Compute Pool is running with 1 CPU\_X64\_S instance
    - The INTERNAL\_OPENFLOW\_0\_SMALL Compute Pool is running with 1 CPU\_X64\_S instance
    - Total Openflow consumption = 2 CPU\_X64\_S instance-hours

You created two small runtimes with min/max of two nodes each, and one large runtime with min/max of 10 nodes. These Runtimes are active for one hour.
:   - The Openflow\_Control\_Pool\_0 Compute Pool is running with 1 CPU\_X64\_S instance

      - Two small runtimes at two nodes = INTERNAL\_OPENFLOW\_0\_SMALL Compute Pool is running with 2 CPU\_X64\_S instances = 2 CPU\_X64\_S instance-hours
      - One large runtime at 10 nodes = INTERNAL\_OPENFLOW\_0\_LARGE Compute Pool is running with 4 CPU\_X64\_L instances = 4 CPU\_X64\_L instance-hours
    - Total Openflow consumption = 3 CPU\_X64\_S instance-hours + 4 CPU\_X64\_L instance-hours

You created one medium runtime with one node. After 20 minutes, it scales to two nodes. After 20 minutes, it scales back down to one node and runs for another 20 minutes.
:   - The Openflow\_Control\_Pool\_0 Compute Pool is running with 1 CPU\_X64\_S instance
    - One medium runtime scaling up to two nodes = INTERNAL\_OPENFLOW\_0\_MEDIUM Compute Pool is running with 1 CPU\_X64\_SL instance = 1 CPU\_X64\_SL instance-hour
    - Total Openflow consumption = 1 CPU\_X64\_S instance-hour + 1 CPU\_X64\_SL instance-hour

You created one medium runtime with two nodes, then suspended it after 30 minutes.
:   - The Openflow\_Control\_Pool\_0 Compute Pool is running with 1 CPU\_X64\_S instance
    - One medium runtime at one node = INTERNAL\_OPENFLOW\_0\_MEDIUM Compute Pool is running with 1 CPU\_X64\_SL instance
    - 30 minutes = 1/2 hour
    - Total Openflow consumption = 1 CPU\_X64\_S instance-hour + 1/2 CPU\_X64\_SL instance-hour
