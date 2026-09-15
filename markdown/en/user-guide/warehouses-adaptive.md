# Adaptive Compute

Feature — Generally Available

Available to accounts that are Enterprise Edition (or higher) in select Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP) regions. For details, see
[Region availability](/user-guide/warehouses-adaptive#label-adaptive-warehouse-region-availability).

Adaptive Compute is a compute service focused on delivering strong performance with effortless
operations. It replaces the fixed compute engine with a workload-aware one that adapts to your
queries automatically. The system decides how to allocate resources for the best performance,
eliminating the need for infrastructure tuning.

By automatically scaling resources and intelligently routing queries, Adaptive Compute removes the
operational complexity that comes with traditional warehouse management: manual cluster sizing,
disruptive upgrades, and hands-on performance tuning. It also incorporates the latest hardware and
performance enhancements, so Adaptive Warehouses can run significantly more queries at a similar
cost to Gen2.

You access Adaptive Compute through Adaptive Warehouses. With an Adaptive Warehouse, you no longer
need to manage:

- Warehouse size (XSMALL, SMALL, MEDIUM, and so on).
- Multi-cluster warehouse settings.
- Query Acceleration Service settings.
- Suspend and resume policies.

To control whether an Adaptive Warehouse accepts new jobs, see
[Enable or disable an Adaptive Warehouse](#label-adaptive-warehouse-enable-disable).

Snowflake handles sizing, scaling, and query routing automatically, so your team can focus on
working with data rather than managing the infrastructure behind it.

All jobs across all Adaptive Warehouses in an account are routed to a shared pool of compute
resources. This pool is dedicated to your account: it isn’t shared with other accounts in your
organization and isn’t used by other warehouse types, such as standard, interactive, or
Snowpark-optimized. You can still have multiple Adaptive Warehouses per account
for grouping workloads with similar performance and cost characteristics,
reporting, and governance.

Adaptive Warehouses use a query-based billing model, where the cost of each query
depends on factors like the amount of compute and software resources it uses. You
can still reason about costs at the warehouse level, because all queries running
in an Adaptive Warehouse add up to the total cost of that warehouse.

The same cost management tools are available:

- [Budgets](/user-guide/budgets) and
  [resource monitors](/user-guide/resource-monitors) for cost governance.
- [QUERY\_METERING\_HISTORY view](/sql-reference/account-usage/query_metering_history) for per-query credit usage.
- [WAREHOUSE\_METERING\_HISTORY view](/sql-reference/account-usage/warehouse_metering_history) for aggregated warehouse
  credit usage.

You can create new Adaptive Warehouses or convert existing standard warehouses to an Adaptive Warehouse
without downtime. Converting existing warehouses allows you to retain your existing
chargeback and showback structures and workload segregation (analytics versus ETL, team-based
warehouses, and so on). For example, the finance team might use one Adaptive Warehouse and the
engineering team might use another.

## When to use an Adaptive Warehouse

Adaptive Warehouses are a good fit when you want Snowflake to handle compute scaling and tuning,
and your workloads benefit from consistent performance without ongoing warehouse administration.

Consider Adaptive Warehouses for:

- **Analytical workloads**, where Adaptive Warehouses can deliver strong, consistent performance
  improvements compared with static warehouse sizing.
- **Data loading pipelines**, where per-query scheduling adapts well to changing ingestion
  parallelism.
- **Mixed BI and ETL workloads**, where bursty, varied query shapes are handled better than a
  fixed warehouse size.
- **Workloads with high size variance**, where queries range from XSMALL to XLARGE and benefit
  from per-query resource allocation.
- **Reduced operational overhead**, when you prefer not to manage warehouse size, multi-cluster
  settings, Query Acceleration Service configuration, or suspend and resume policies.
- **Warehouses with occasional HTAP queries**, where analytical queries account for most usage and
  hybrid transactional/analytical processing (HTAP) is a smaller share. You can convert to Adaptive Warehouse;
  both query types continue to run on the warehouse after conversion.

You might prefer a different warehouse type when:

- **Warehouses used primarily for HTAP**, where hybrid transactional/analytical processing
  accounts for most of the workload. Use a standard Gen2 warehouse instead of converting to Adaptive Warehouse.
- **You need direct control over warehouse size and scaling policy** for predictable, everyday
  analytics and reporting. Standard Gen2 warehouses give you full configuration control.
- **You need very low latency for dashboards, applications, or other user-facing queries**.
  Consider interactive warehouses.
- **You run high-memory Snowpark or machine learning workloads on a single node**. Consider
  Snowpark-optimized warehouses.

For supported and unsupported conversion paths, see [Limitations](#label-adaptive-warehouse-limitations).

## Limitations

Adaptive Warehouses require Enterprise Edition (or higher).
The following conversions are also **not** yet supported:

- Converting to or from an X5Large or X6Large warehouse.
- Converting to or from a Snowpark-optimized or interactive warehouse.

## Region availability

Adaptive Warehouses are generally available in select Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP) regions.
For more information about Snowflake regions, see [Supported cloud regions](/user-guide/intro-regions).

### Amazon Web Services (AWS)

#### Americas

- Canada (Central)
- South America (São Paulo)
- US East (N. Virginia)
- US East 2 (Ohio)
- US Gov East 1
- US Gov West 1
- US West 2 (Oregon)

#### Europe

- EU Central 1 (Frankfurt)
- EU North 1 (Stockholm)
- EU West 1 (Ireland)
- EU West 3 (Paris)
- Europe (London)

#### Asia Pacific

- AP Northeast 1 (Tokyo)
- AP Northeast 2 (Seoul)
- AP Northeast 3 (Osaka)
- AP South 1 (Mumbai)
- AP Southeast 2 (Sydney)
- AP Southeast 5 (Malaysia)
- AP Southeast 7 (Thailand)
- China (Ningxia)

#### Africa

- Africa (Cape Town)

### Microsoft Azure

#### Americas

- Canada Central
- Central US (Iowa)
- East US
- East US 2 (Virginia)
- Mexico Central
- South Central US (Texas)
- West US 2

#### Europe

- North Europe (Ireland)
- Sweden Central (Gävle)
- Switzerland North (Zurich)
- UK South (London)
- West Europe (Netherlands)

#### Middle East

- UAE North

#### Asia Pacific

- Australia East
- Central India
- Japan East
- Korea Central
- Southeast Asia (Singapore)

### Google Cloud Platform (GCP)

#### Americas

- us-central1 (Iowa)
- us-east4 (Northern Virginia)

#### Europe

- europe-west2 (London)
- europe-west3 (Frankfurt)
- europe-west4 (Netherlands)

#### Asia Pacific

- australia-southeast2 (Melbourne)

## Managing performance and throughput

Adaptive Warehouses expose two primary properties to control performance and throughput:

- MAX\_QUERY\_PERFORMANCE\_LEVEL
- QUERY\_THROUGHPUT\_MULTIPLIER

### MAX\_QUERY\_PERFORMANCE\_LEVEL

MAX\_QUERY\_PERFORMANCE\_LEVEL expresses the upper bound of performance for any individual query.
It’s set at the warehouse level and serves as the mechanism to allow the system to apply
performance optimizations on a query if it can do so with high confidence.

The property is expressed in units of t-shirt sizes (XSMALL through X4LARGE). Each t-shirt size
conveys a similar or better level of performance than its commensurate classic warehouse size.

Type:
:   `{ XSMALL | SMALL | MEDIUM | LARGE | XLARGE | XXLARGE | XXXLARGE | X4LARGE }`

Default:
:   `XLARGE`

**Semantics:**

- Larger values raise the upper bound, giving the system more room to apply performance
  optimizations when it has high confidence, at the cost of potentially higher instantaneous spend
  for a single query.
- Smaller values lower the upper bound, limiting how aggressively the system optimizes queries
  when it has high confidence.
- This value doesn’t map to a specific underlying compute configuration. It expresses only a
  performance level: Snowflake determines the actual resources used for each query.

**Behavior:**

For each query, Adaptive Compute evaluates whether it can improve performance with high
confidence. When confidence is high, the system may apply performance optimizations up to
MAX\_QUERY\_PERFORMANCE\_LEVEL. When confidence is lower, the system might use less compute, even
if that level is below MAX\_QUERY\_PERFORMANCE\_LEVEL.

If the system determines that the compute needed for an optimization exceeds
MAX\_QUERY\_PERFORMANCE\_LEVEL, Snowflake caps performance at MAX\_QUERY\_PERFORMANCE\_LEVEL.

**Guidance:**

Set MAX\_QUERY\_PERFORMANCE\_LEVEL to the highest performance level you’re comfortable allowing when
the system has high confidence to optimize a query. Use [budgets](/user-guide/budgets) and
[resource monitors](/user-guide/resource-monitors) to govern total spend over time.

### QUERY\_THROUGHPUT\_MULTIPLIER

QUERY\_THROUGHPUT\_MULTIPLIER is a scale factor that controls how many queries and how much total
work an Adaptive Warehouse can run at once, relative to a system-computed baseline for your chosen
MAX\_QUERY\_PERFORMANCE\_LEVEL.

Type:
:   Non-negative integer

Default:
:   `2`

Setting this value to `0` means unlimited throughput: the warehouse can use as much burst
capacity as available with no cap.

**Semantics:**

Snowflake calculates a throughput budget from QUERY\_THROUGHPUT\_MULTIPLIER and
MAX\_QUERY\_PERFORMANCE\_LEVEL.

Higher values increase how many queries and how much total work can run at once, which reduces
queuing at the cost of potentially higher instantaneous spend. Lower values constrain burst
throughput and reduce the risk of sudden spikes in spend, but might lead to queuing.

**Behavior:**

Each query has an estimated amount of work it needs to run based on the determined compute
configuration. Query work is fungible.

Admission control uses the throughput budget and estimated work to decide whether to start or queue
each new query.

A value of `N` doesn’t mean exactly `N` queries run concurrently at MAX\_QUERY\_PERFORMANCE\_LEVEL.
Instead, it raises or lowers the overall concurrency the system targets. The actual number of
concurrent queries depends on how much work each query needs relative to the budget.

**Guidance:**

Set QUERY\_THROUGHPUT\_MULTIPLIER to the aggregate amount of query processing your workload needs.
Consider testing the system defaults before tuning. If you see queuing, increase
QUERY\_THROUGHPUT\_MULTIPLIER.

Workloads with uneven load can have peaks that exceed the allotted capacity. If you’re more
concerned about capping instantaneous spend, reduce QUERY\_THROUGHPUT\_MULTIPLIER and rely on
budgets and resource monitors for absolute cost controls.

## Create an Adaptive Warehouse

You can create an Adaptive Warehouse using Snowsight, SQL, or
[Cortex Code](/user-guide/cortex-code/cortex-code).

SnowsightSQLCortex Code

To create an Adaptive Warehouse using Snowsight:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Compute** » **Warehouses**.
3. Select **+Warehouse**.
4. In the **Type** dropdown, select **Adaptive**.
5. Optionally, select **Advanced** and configure:
   - **Maximum query performance level** (default: XLarge)
   - **Query throughput multiplier** (default: 2)

The warehouse is created and can be used normally.

As an alternative to using Snowsight, you can create an Adaptive Warehouse using
the [CREATE ADAPTIVE WAREHOUSE](#label-create-adaptive-warehouse-syntax) command.

Copy code

```
CREATE ADAPTIVE WAREHOUSE my_adaptive_wh;
```

This creates an Adaptive Warehouse using defaults (MAX\_QUERY\_PERFORMANCE\_LEVEL = XLARGE,
QUERY\_THROUGHPUT\_MULTIPLIER = 2). Snowflake uses conservative, safe defaults so you can
start without tuning.

You can also specify properties at creation time:

Copy code

```
CREATE ADAPTIVE WAREHOUSE my_adaptive_wh
  WITH MAX_QUERY_PERFORMANCE_LEVEL = XLARGE
       QUERY_THROUGHPUT_MULTIPLIER = 4;
```

For the full syntax, additional examples, and the list of optional properties,
see the [SQL reference](#label-adaptive-warehouse-sql-reference) section.

You can ask [Cortex Code](/user-guide/cortex-code/cortex-code) to create an
Adaptive Warehouse using natural language. For example:

```
Create an Adaptive Warehouse called my_adaptive_wh with
MAX_QUERY_PERFORMANCE_LEVEL set to XLARGE and
QUERY_THROUGHPUT_MULTIPLIER set to 4.
```

Cortex Code generates and runs the appropriate SQL on your behalf.

## Convert a standard warehouse to an Adaptive Warehouse

You can convert a standard warehouse to an Adaptive Warehouse using Snowsight, SQL, or
[Cortex Code](/user-guide/cortex-code/cortex-code).

Note

Converting a warehouse to or from an Adaptive Warehouse is an *online operation*,
which means that it doesn’t involve any downtime. This conversion doesn’t make the
warehouse unavailable or interrupt any running queries.

When you convert a warehouse to an Adaptive Warehouse or back to a standard warehouse,
existing queries that were running on that warehouse continue to run to completion using
the existing compute resources. At the same time, the warehouse runs any new queries on
the compute resources of the new warehouse type. While the existing queries are running,
you’re charged for both sets of compute resources. If you’re converting the warehouse back
to a standard one, the warehouse doesn’t automatically suspend during this period, whether
or not any queries are using the new compute resources. When the existing queries complete,
the workload shifts entirely to the new compute resources.

SnowsightSQLCortex Code

To convert a standard warehouse to an Adaptive Warehouse using Snowsight:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Compute** » **Warehouses** » **<warehouse\_identifier>**.
3. Select the more menu **…** (three dots) » **Convert to Adaptive Warehouse**.
4. Confirm the operation.

To convert a standard warehouse to an Adaptive Warehouse, use the
ALTER WAREHOUSE command to set the WAREHOUSE\_TYPE property to
`ADAPTIVE`. For example:

Copy code

```
ALTER WAREHOUSE my_warehouse SET WAREHOUSE_TYPE = 'ADAPTIVE';
```

To convert the Adaptive Warehouse back to a standard warehouse,
change the property to `STANDARD`. For example:

Copy code

```
ALTER WAREHOUSE my_warehouse SET WAREHOUSE_TYPE = 'STANDARD';
```

You can ask [Cortex Code](/user-guide/cortex-code/cortex-code) to convert
a warehouse using natural language. For example:

```
Convert my_warehouse to an Adaptive Warehouse.
```

Cortex Code generates and runs the appropriate SQL on your behalf.

### Property behavior during conversion

When you convert a standard warehouse to an Adaptive Warehouse, the only property you must change
is WAREHOUSE\_TYPE. Snowflake automatically computes appropriate values for
MAX\_QUERY\_PERFORMANCE\_LEVEL and QUERY\_THROUGHPUT\_MULTIPLIER.

The system derives these from the existing configuration of the standard warehouse:

- Warehouse size.
- MAX\_CLUSTER\_COUNT (for multi-cluster warehouses).
- QAS scale factor.
- Warehouse generation (hardware/software generation).

The goal is to preserve or improve performance compared to the original standard warehouse,
provide enough burst capacity for typical load spikes, and avoid requiring manual tuning when
switching to Adaptive Warehouse.

After conversion, you can optionally override MAX\_QUERY\_PERFORMANCE\_LEVEL and
QUERY\_THROUGHPUT\_MULTIPLIER using ALTER WAREHOUSE. Standard warehouse properties
such as WAREHOUSE\_SIZE and MAX\_CLUSTER\_COUNT no longer apply after conversion to
Adaptive, and Adaptive Warehouse properties no longer apply after conversion back to standard.

## Enable or disable an Adaptive Warehouse

You can enable or disable an Adaptive Warehouse using [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse).
Use this to control whether the warehouse accepts new jobs without dropping the warehouse.

Disable an Adaptive Warehouse:

Copy code

```
ALTER WAREHOUSE my_warehouse DISABLE;
```

Enable an Adaptive Warehouse:

Copy code

```
ALTER WAREHOUSE my_warehouse ENABLE;
```

When an Adaptive Warehouse is **disabled**, new jobs submitted to that warehouse are **rejected**.
Queries that are already running on the warehouse can continue to completion.

When an Adaptive Warehouse is **enabled**, new jobs submitted to that warehouse are accepted for
execution.

To check whether a warehouse is enabled or disabled, use [SHOW WAREHOUSES](/sql-reference/sql/show-warehouses).
The `STATE` column shows `ENABLED` or `DISABLED`. If the warehouse is disabled, the
`DISABLED_REASONS` column lists why (for example, a manual `DISABLE` or a [resource monitor](/user-guide/resource-monitors)
action). For how resource monitors disable Adaptive Warehouses and enable them again when monitor conditions clear, see
[Resource monitors and Adaptive Warehouses](/user-guide/resource-monitors#label-resource-monitors-adaptive-warehouses).

## Billing and pricing

Adaptive Warehouses use a query-based billing model. The cost of each query
depends on factors like the amount of compute and software resources it uses,
including the cluster sizes and additional capacity used by features like
Query Acceleration Service (QAS). You aren’t charged for creating an Adaptive Warehouse: charges start when the first query runs.

All queries running in an Adaptive Warehouse add up to the total cost of that
warehouse, so you can continue to use existing chargeback and showback
structures. Adaptive Warehouse usage is reported as part of COMPUTE in usage
statements using virtual warehouse credits.

You control performance and spend primarily through:

- **MAX\_QUERY\_PERFORMANCE\_LEVEL**: upper bound for performance optimizations the system applies
  with high confidence.
- **QUERY\_THROUGHPUT\_MULTIPLIER**: caps how much total query work can run at once.
- **Budgets and resource monitors**: govern total spend over time at the account
  or warehouse level.

Typical configuration patterns:

| Workload type | Configuration |
| --- | --- |
| Latency-sensitive, critical workloads | Higher MAX\_QUERY\_PERFORMANCE\_LEVEL (XLARGE or above). Higher QUERY\_THROUGHPUT\_MULTIPLIER. Resource monitors or budgets to keep aggregate spend within plan. |
| Cost-sensitive, high-throughput workloads | Moderate MAX\_QUERY\_PERFORMANCE\_LEVEL (MEDIUM or LARGE). Medium QUERY\_THROUGHPUT\_MULTIPLIER to balance throughput against spend spikes. |
| Tightly budgeted workloads | Lower MAX\_QUERY\_PERFORMANCE\_LEVEL. Lower QUERY\_THROUGHPUT\_MULTIPLIER. Strict budgets and resource monitors. |

Expand

Show lessSee more

You can use [ACCOUNT\_USAGE](/sql-reference/account-usage) views to retrieve
granular data on credit consumption for a specific Adaptive Warehouse. Use
[QUERY\_METERING\_HISTORY view](/sql-reference/account-usage/query_metering_history) to view per-query credit
usage, or [WAREHOUSE\_METERING\_HISTORY view](/sql-reference/account-usage/warehouse_metering_history) for
aggregated warehouse credit usage. For a full list of relevant views, see
[Account and organization usage views](#label-adaptive-warehouse-usage-views).

For more information about compute cost, see
[Understanding compute cost](/user-guide/cost-understanding-compute).

## SQL reference

### CREATE ADAPTIVE WAREHOUSE

Creates a new Adaptive Warehouse.

Copy code

```
CREATE [ OR REPLACE ] ADAPTIVE WAREHOUSE [ IF NOT EXISTS ] <name>
  [ [ WITH ] adaptiveProperties ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
  [ objectParams ]

adaptiveProperties ::=
  COMMENT = '<string_literal>'
  MAX_QUERY_PERFORMANCE_LEVEL = { XSMALL | SMALL | MEDIUM | LARGE
                                | XLARGE | XXLARGE | XXXLARGE | X4LARGE }
  QUERY_THROUGHPUT_MULTIPLIER = <integer>

objectParams ::=
  STATEMENT_QUEUED_TIMEOUT_IN_SECONDS = <num>
  STATEMENT_TIMEOUT_IN_SECONDS = <num>
```

You can also create an Adaptive Warehouse using the standard
[CREATE WAREHOUSE](/sql-reference/sql/create-warehouse) syntax with
`WAREHOUSE_TYPE = 'ADAPTIVE'`:

Copy code

```
CREATE [ OR REPLACE ] WAREHOUSE [ IF NOT EXISTS ] <name>
  [ [ WITH ] WAREHOUSE_TYPE = 'ADAPTIVE'
    [ adaptiveProperties ]
  ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
  [ objectParams ]
```

Note

Standard warehouse properties such as WAREHOUSE\_SIZE, MIN\_CLUSTER\_COUNT,
MAX\_CLUSTER\_COUNT, and SCALING\_POLICY can’t be set on an Adaptive Warehouse.
Similarly, Adaptive Warehouse properties such as MAX\_QUERY\_PERFORMANCE\_LEVEL
and QUERY\_THROUGHPUT\_MULTIPLIER can’t be set on a standard warehouse.

#### Required parameters

`name`
:   Identifier for the Adaptive Warehouse. Must be unique for your account.
    Must start with an alphabetic character and can’t contain spaces or special
    characters unless enclosed in double quotes. See
    [Object identifiers](/sql-reference/identifiers) for details.

#### Optional properties

`MAX_QUERY_PERFORMANCE_LEVEL = { XSMALL | SMALL | MEDIUM | LARGE | XLARGE | XXLARGE | XXXLARGE | X4LARGE }`
:   Upper bound on the performance level for a single statement, expressed
    as a t-shirt size. Default: `XLARGE`.

    The system applies performance optimizations up to this bound only when it has high confidence
    that doing so will improve query performance. Choose a value appropriate for the performance level
    you want when the system is highly confident it can optimize a query.

    For more details, see [Managing performance and throughput](#label-adaptive-warehouse-perf).

`QUERY_THROUGHPUT_MULTIPLIER = <integer>`
:   Scale factor that controls how many queries and how much total work an Adaptive Warehouse can run
    at once, relative to a system-computed baseline for MAX\_QUERY\_PERFORMANCE\_LEVEL. Snowflake
    calculates a throughput budget from QUERY\_THROUGHPUT\_MULTIPLIER and MAX\_QUERY\_PERFORMANCE\_LEVEL;
    admission control uses that budget and per-query estimated work to decide whether to start or
    queue each new query. A value of `0` means unlimited throughput.

    Default: `2`.

    For more details, see [Managing performance and throughput](#label-adaptive-warehouse-perf).

`STATEMENT_QUEUED_TIMEOUT_IN_SECONDS = <num>`
:   Maximum time, in seconds, a SQL statement can remain queued on the warehouse
    before Snowflake cancels it. See
    [Parameters](/sql-reference/parameters) for details.

`STATEMENT_TIMEOUT_IN_SECONDS = <num>`
:   Maximum time, in seconds, a running SQL statement can run before Snowflake
    cancels it. See [Parameters](/sql-reference/parameters) for details.

#### Examples

Create an Adaptive Warehouse with defaults:

Copy code

```
CREATE ADAPTIVE WAREHOUSE my_adaptive_wh;
```

Create with a specific performance level:

Copy code

```
CREATE ADAPTIVE WAREHOUSE my_adaptive_wh
  WITH MAX_QUERY_PERFORMANCE_LEVEL = XXLARGE;
```

Create with both properties:

Copy code

```
CREATE ADAPTIVE WAREHOUSE my_adaptive_wh
  WITH MAX_QUERY_PERFORMANCE_LEVEL = MEDIUM
       QUERY_THROUGHPUT_MULTIPLIER = 6;
```

Create using the standard CREATE WAREHOUSE syntax:

Copy code

```
CREATE WAREHOUSE my_adaptive_wh
  WITH WAREHOUSE_TYPE = 'ADAPTIVE'
       MAX_QUERY_PERFORMANCE_LEVEL = LARGE
       QUERY_THROUGHPUT_MULTIPLIER = 3;
```

### ALTER WAREHOUSE (Adaptive Warehouse)

You can use [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) to enable or disable an
Adaptive Warehouse, convert a standard warehouse to an Adaptive Warehouse, modify Adaptive Warehouse
properties, or convert an Adaptive Warehouse back to standard.

Enable or disable an Adaptive Warehouse:

Copy code

```
ALTER WAREHOUSE my_warehouse ENABLE;
ALTER WAREHOUSE my_warehouse DISABLE;
```

For more information, see [Enable or disable an Adaptive Warehouse](#label-adaptive-warehouse-enable-disable).

Convert a standard warehouse to Adaptive Warehouse:

Copy code

```
ALTER WAREHOUSE my_warehouse SET WAREHOUSE_TYPE = 'ADAPTIVE';
```

Modify Adaptive Warehouse properties after creation or conversion:

Copy code

```
ALTER WAREHOUSE my_adaptive_wh SET
  MAX_QUERY_PERFORMANCE_LEVEL = XLARGE
  QUERY_THROUGHPUT_MULTIPLIER = 8;
```

Convert an Adaptive Warehouse back to standard:

Copy code

```
ALTER WAREHOUSE my_warehouse SET WAREHOUSE_TYPE = 'STANDARD';
```

## SHOW WAREHOUSES

The Adaptive Warehouse feature introduces new columns to the
[SHOW WAREHOUSES](/sql-reference/sql/show-warehouses) command. Properties
that don’t apply to Adaptive Warehouses are shown as `NULL`.

Columns specific to Adaptive Warehouses include:

| Column name | Description |
| --- | --- |
| STATE | One of:   - ENABLED: the warehouse accepts new jobs for execution. - DISABLED: the warehouse rejects new jobs. |
| MAX\_QUERY\_PERFORMANCE\_LEVEL | Expressed as a t-shirt size. Upper bound on per-statement performance when the system applies optimizations with high confidence. |
| QUERY\_THROUGHPUT\_MULTIPLIER | Integer scale factor controlling how much total query work the warehouse can run at once. |
| DISABLED\_REASONS | One or more reasons why the Adaptive Warehouse is disabled (for example, `ALTER WAREHOUSE ... DISABLE` or a resource monitor action). Populated when `STATE` is `DISABLED`. |

Expand

Show lessSee more

## Account and organization usage views

The following ACCOUNT\_USAGE views are available for Adaptive Warehouses:

- [QUERY\_METERING\_HISTORY view](/sql-reference/account-usage/query_metering_history)
- [WAREHOUSE\_METERING\_HISTORY view](/sql-reference/account-usage/warehouse_metering_history)
- [QUERY\_HISTORY view](/sql-reference/account-usage/query_history)
- [WAREHOUSE\_LOAD\_HISTORY view](/sql-reference/account-usage/warehouse_load_history)

Coming soon in ORGANIZATION\_USAGE:

- [QUERY\_METERING\_HISTORY view](/sql-reference/organization-usage/query_metering_history) (organization-wide per-query credit
  usage; view latency may be up to 24 hours)

Use [QUERY\_METERING\_HISTORY view](/sql-reference/account-usage/query_metering_history) to monitor per-query
cost for Adaptive Warehouse workloads. View latency may be up to 1 hour, and each row represents
credit usage for a query in a metering hour window. See
[- Latency for the view may be up to 1 hour. Charges accrued by a job may take…](/sql-reference/account-usage/query_metering_history#label-query-metering-history-data-freshness)
for how rows are refreshed while queries are running. For aggregated warehouse credit
usage, use [WAREHOUSE\_METERING\_HISTORY view](/sql-reference/account-usage/warehouse_metering_history).

Note

For Adaptive Warehouses, QAS usage is included in compute credits and doesn’t
appear as a separate credit column. Use
[WAREHOUSE\_LOAD\_HISTORY view](/sql-reference/account-usage/warehouse_load_history) to monitor queuing
behavior and understand whether to adjust MAX\_QUERY\_PERFORMANCE\_LEVEL or
QUERY\_THROUGHPUT\_MULTIPLIER.

The following sample query produces a time series of warehouse-level performance
data for any warehouse that ran at least one query in `ADAPTIVE` state within a
specified lookback period.

Copy code

```
WITH adaptive_whs AS (
  SELECT DISTINCT warehouse_name
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY q
  WHERE q.warehouse_size = 'ADAPTIVE'
    AND q.start_time >= DATEADD(day, -7, CURRENT_DATE())
)
SELECT
  q.end_time::DATE AS ds,
  q.warehouse_name,
  IFF(q.warehouse_size = 'ADAPTIVE', 'ADAPTIVE', 'STANDARD') AS warehouse_type,
  AVG(q.total_elapsed_time) AS avg_query_time,
  AVG(q.execution_time) AS avg_exec_time,
  AVG(q.queued_overload_time) AS avg_queued_overload_time,
  AVG(q.queued_provisioning_time) AS avg_queued_provisioning_time
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY q
WHERE q.start_time >= DATEADD(day, -7, CURRENT_DATE())
  AND q.warehouse_name IN (SELECT warehouse_name FROM adaptive_whs)
GROUP BY ALL;
```

## Bulk migration of standard warehouses to Adaptive Warehouse

If you want to migrate many standard warehouses to Adaptive Warehouse simultaneously,
you can use the SYSTEM$BULK\_UPDATE\_WH function.

**Parameters for SYSTEM$BULK\_UPDATE\_WH function**

| Parameter | Description | Allowed values |
| --- | --- | --- |
| property\_name | The warehouse property to update. | `'WAREHOUSE_TYPE'` |
| new\_value | New value for the property. | `'ADAPTIVE'` or `'STANDARD'` |
| property\_filter | JSON filter on warehouse properties (for example, name pattern, size). Warehouses matching all filters are considered for update. | `'{"name": "TEST.*"}'` |
| tag\_filter | JSON filter on tags. Warehouses must match all specified tags to be selected. | `'{"cost-center": "sales"}'` |
| execution\_mode | Operation mode: perform the update or dry run. | `'ACTIVE'`, `'DRY_RUN'` |

Expand

Show lessSee more

Suggested usage:

1. First, do a dry run and review the results:

   Copy code

   ```
   SELECT SYSTEM$BULK_UPDATE_WH(
     'WAREHOUSE_TYPE',
     'ADAPTIVE',
     '{"WAREHOUSE_TYPE": "STANDARD"}',
     'DRY_RUN'
   );
   ```
2. Review the output and adjust filters if necessary.
3. After verifying the dry run, call the function again using the active mode:

   Copy code

   ```
   SELECT SYSTEM$BULK_UPDATE_WH(
     'WAREHOUSE_TYPE',
     'ADAPTIVE',
     '{"WAREHOUSE_TYPE": "STANDARD"}',
     'ACTIVE'
   );
   ```
4. Carefully review the results and any errors before repeating or broadening
   the migration scope.
