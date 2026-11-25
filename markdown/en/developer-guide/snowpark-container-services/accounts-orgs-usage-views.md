# Snowpark Container Services costs

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

The costs associated with using Snowpark Container Services can be categorized into storage cost, compute pool cost, and data
transfer cost.

## What you pay for

The following table summarizes the resources that Snowpark Container Services bills for. For the rate of each resource, see the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

| Resource | Billing basis | Where it appears |
| --- | --- | --- |
| Compute pool nodes | Credits per node, based on the instance family. Charged while the pool is in the IDLE, ACTIVE, STOPPING, or RESIZING state, but not STARTING or SUSPENDED. | SNOWPARK\_CONTAINER\_SERVICES\_HISTORY, METERING\_HISTORY, and METERING\_DAILY\_HISTORY (`SERVICE_TYPE = 'SNOWPARK_CONTAINER_SERVICES'`) |
| Storage (image repository, stages, event tables) | Standard Snowflake storage rates. | Storage usage views (see [Exploring storage cost](/user-guide/cost-exploring-data-storage)) |
| Block storage and snapshots | Storage rates in the Service Consumption Table. | Storage usage views |
| Outbound data transfer | Data transfer rates by cloud and region. | DATA\_TRANSFER\_HISTORY (`TRANSFER_TYPE = 'SNOWPARK_CONTAINER_SERVICES'`) |
| Internal data transfer | SPCS same-cloud, same-region rate. | DATA\_TRANSFER\_HISTORY (`TRANSFER_TYPE = 'INTERNAL'`) and INTERNAL\_DATA\_TRANSFER\_HISTORY |

Expand

Show lessSee more

Local storage on a compute pool node is covered by the compute pool node cost and isn’t billed separately.

## Storage cost

When you use Snowpark Container Services, storage costs associated with Snowflake, including the cost of Snowflake stage usage
or database table storage, apply. For more information, see [Exploring storage cost](/user-guide/cost-exploring-data-storage). In addition, the
following cost considerations apply:

- **Image repository storage cost:** The implementation of the [image repository](/developer-guide/snowpark-container-services/working-with-registry-repository) uses
  a Snowflake stage. Therefore, the associated cost for using the Snowflake stage applies.
- **Log storage cost:** When you store
  [local container logs in event tables](/developer-guide/snowpark-container-services/monitoring-services#label-snowpark-containers-working-with-services-local-logs), event table storage
  costs apply.
- **Mounting volumes cost:**

  - When you mount a Snowflake stage as a volume, the cost of using the Snowflake stage applies.
  - When you mount storage from the compute pool node as a volume, it appears as local storage in the container. But there is no
    additional cost because the local storage cost is covered by the cost of the compute pool node.
- **Block storage cost:** When you create a service that uses [block storage](/developer-guide/snowpark-container-services/block-storage-volume), you are billed for block storage and snapshot storage. For more information about storage pricing, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf). The SPCS Block Storage Pricing table in this document provides the information.

## Compute pool cost

A [compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool) is a collection of one or more virtual machine (VM) nodes on which Snowflake
runs your Snowpark Container Services jobs and services. The number and type (instance family) of the nodes in the compute pool
(see [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool)) determine the credits it consumes and thus the cost you pay. For more information, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

You incur charges for a compute pool in the IDLE, ACTIVE, STOPPING, or RESIZING state, but not when it is in a STARTING or
SUSPENDED state. To optimize compute pool expenses, you should leverage the AUTO\_SUSPEND feature (see CREATE COMPUTE POOL).

The following views provide usage information:

- **ACCOUNT\_USAGE views**

  The following ACCOUNT\_USAGE views contain Snowpark Container Services credit usage information:

  - The [SNOWPARK\_CONTAINER\_SERVICES\_HISTORY view](/sql-reference/account-usage/snowpark_container_services_history) offers
    credit usage information (hourly consumption) exclusively for Snowpark Container Services.
  - In the [METERING\_DAILY\_HISTORY view](/sql-reference/account-usage/metering_daily_history), query for rows in which the
    `service_type` column contains the value `SNOWPARK_CONTAINER_SERVICES`.
  - In the [METERING\_HISTORY view](/sql-reference/account-usage/metering_history), query for rows in which the
    `service_type` column contains the value `SNOWPARK_CONTAINER_SERVICES`.
- **ORGANIZATION\_USAGE views**

  - In the [METERING\_DAILY\_HISTORY view](/sql-reference/organization-usage/metering_daily_history), use the
    `SERVICE_TYPE = SNOWPARK_CONTAINER_SERVICES` query filter.

### Example queries

The following query returns the credits that each compute pool used per day over the last 30 days:

Copy code

```
SELECT
    DATE_TRUNC('day', start_time) AS usage_date,
    compute_pool_name,
    SUM(credits_used) AS credits_used
  FROM SNOWFLAKE.ACCOUNT_USAGE.SNOWPARK_CONTAINER_SERVICES_HISTORY
  WHERE start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP())
  GROUP BY 1, 2
  ORDER BY 1, 2;
```

To see hourly consumption, group by `start_time` instead of `DATE_TRUNC('day', start_time)`.

The following query returns the daily credits that your account used for Snowpark Container Services:

Copy code

```
SELECT usage_date, SUM(credits_used) AS credits_used
  FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_DAILY_HISTORY
  WHERE service_type = 'SNOWPARK_CONTAINER_SERVICES'
    AND usage_date >= DATEADD('day', -30, CURRENT_DATE())
  GROUP BY usage_date
  ORDER BY usage_date;
```

The following query returns the same information for each account in your organization:

Copy code

```
SELECT account_name, usage_date, SUM(credits_used) AS credits_used
  FROM SNOWFLAKE.ORGANIZATION_USAGE.METERING_DAILY_HISTORY
  WHERE service_type = 'SNOWPARK_CONTAINER_SERVICES'
    AND usage_date >= DATEADD('day', -30, CURRENT_DATE())
  GROUP BY account_name, usage_date
  ORDER BY account_name, usage_date;
```

## Data transfer cost

Data transfer is the process of moving data into (ingress) and out of (egress) Snowflake. For more information, see
[Understanding data transfer cost](/user-guide/cost-understanding-data-transfer). When you use Snowpark Container Services, the following additional cost
considerations apply:

- **Outbound data transfer:** Snowflake applies the same data transfer rate for outbound data transfers from services and jobs
  to other cloud regions and to the internet, consistent with the rate for all Snowflake outbound data transfers. For more
  information, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) (table 4a).

  You can query the [DATA\_TRANSFER\_HISTORY ACCOUNT\_USAGE view](/sql-reference/account-usage/data_transfer_history) for
  usage information. The `transfer_type` column identifies this cost as the `SNOWPARK_CONTAINER_SERVICES` type.
- **Internal data transfer:** This class of data transfer refers to data movements across compute entities within Snowflake, such as
  between two compute pools or a compute pool and a warehouse, that resulted from executing a
  [service function](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating).
  For more information, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)
  (tables 4(a) for AWS, 4(b) for Azure, and the column titled “SPCS Data Transfer to Same Cloud Provider, Same Region”).

  To view the costs associated with internal data transfer, you can do the following:

  - Query the [INTERNAL\_DATA\_TRANSFER\_HISTORY view](/sql-reference/account-usage/internal_data_transfer_history) in the ACCOUNT\_USAGE schema.
  - Query the [DATA\_TRANSFER\_HISTORY view](/sql-reference/account-usage/data_transfer_history) in the ACCOUNT\_USAGE schema. The
    `transfer_type` column identifies this cost as the `INTERNAL` type.
  - Query the [DATA\_TRANSFER\_HISTORY view](/sql-reference/organization-usage/data_transfer_history) in the ORGANIZATION\_USAGE schema.
    The `transfer_type` column identifies this cost as the `INTERNAL` type.
  - Query the [DATA\_TRANSFER\_DAILY\_HISTORY view](/sql-reference/organization-usage/data_transfer_daily_history) in the ORGANIZATION\_USAGE schema. The `service_type` column identifies this cost as the `INTERNAL_DATA_TRANSFER` type.
  - Query the [RATE\_SHEET\_DAILY view](/sql-reference/organization-usage/rate_sheet_daily) in the ORGANIZATION USAGE
    schema. The `service_type` column identifies this cost as the `INTERNAL_DATA_TRANSFER` type.
  - Query the [USAGE\_IN\_CURRENCY\_DAILY view](/sql-reference/organization-usage/usage_in_currency_daily) in the ORGANIZATION USAGE
    schema. The `service_type` column identifies this cost as the `INTERNAL_DATA_TRANSFER` type.

The following query returns the bytes transferred over the last 30 days by Snowpark Container Services and internal transfers:

Copy code

```
SELECT transfer_type, SUM(bytes_transferred) AS bytes_transferred
  FROM SNOWFLAKE.ACCOUNT_USAGE.DATA_TRANSFER_HISTORY
  WHERE transfer_type IN ('SNOWPARK_CONTAINER_SERVICES', 'INTERNAL')
    AND start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP())
  GROUP BY transfer_type;
```

Note

Data transfer costs are currently not billed for Snowflake accounts on Google Cloud.
