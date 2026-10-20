# Online serving with hybrid tables

Snowflake also supports online serving through [online feature tables](/sql-reference/commands-feature-store)
backed by hybrid tables. Hybrid table online serving synchronizes the latest
feature values from the offline store on a schedule you configure with `target_lag`.

Use hybrid table online serving when you need low-latency point lookups for batch feature
views and don’t require Postgres-backed capabilities. Hybrid tables don’t support the
Online Feature Store online service, stream ingest, real-time feature views, REST APIs,
or the time-windowed aggregation API. That aggregation API isn’t currently supported
for hybrid table online serving. For those workloads, use the
[Postgres-backed Online Feature Store](/developer-guide/snowflake-ml/feature-store/online-feature-store). Hybrid table online serving typically achieves retrieval latency under 50 ms at P50. The
Postgres-backed Online Feature Store offers lower latency, typically under 10 ms at P50. For a detailed comparison, see the
[Online Feature Store Benchmark Kit](https://github.com/Snowflake-Labs/snowflake-feature-store-online-benchmark-kit).

## Regional availability

Hybrid table online serving is available in the commercial Amazon Web Services (AWS) and
Microsoft Azure regions where hybrid tables are available. Google Cloud Platform (GCP) isn’t
currently supported. For the full list of restrictions, including trial accounts and
government regions, see
[Hybrid tables clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

## Prerequisites

Important

You must have Snowflake version 9.26 or later and `snowflake-ml-python` version 1.18.0
or later to use hybrid table online serving.

Hybrid table online serving doesn’t use the Postgres online service. You don’t need to
call `create_online_service`, set `SNOWFLAKE_PAT`, or configure network access for the
REST endpoints described in [Serving online features](/developer-guide/snowflake-ml/feature-store/online-feature-store).

Create or connect to a feature store the same way you do for offline feature views. For
details, see [Creating or connecting to a feature store](/developer-guide/snowflake-ml/feature-store/create).

## Enable hybrid table online serving

Enable online serving in `OnlineConfig` on a batch feature view. When you omit
`store_type`, the feature view uses hybrid table online serving by default
(`OnlineStoreType.HYBRID_TABLE`). For parameter descriptions, see the
[`OnlineConfig` table](/developer-guide/snowflake-ml/feature-store/online-feature-store#batch-online-feature-views).

Copy code

```
from snowflake.ml.feature_store import FeatureView, OnlineConfig

source_df = session.table("MY_DB.MY_SCHEMA.SOURCE_TABLE")

fv = FeatureView(
    name="MY_ONLINE_FV",
    entities=[my_entity],
    feature_df=source_df,
    timestamp_col="EVENT_TS",
    refresh_freq="5 minutes",
    online_config=OnlineConfig(enable=True, target_lag="30 seconds"),
    desc="Batch features served from a hybrid table online feature table",
)

fs.register_feature_view(fv, version="v1")
```

For how `refresh_freq` and `target_lag` interact, see
[Managing offline to online sync](#label-online-fs-hybrid-sync).

## Permissions

Before you enable hybrid table online serving, grant the producer and consumer roles
access to online feature tables. Use the access control script in
[Feature Store access control](/developer-guide/snowflake-ml/feature-store/rbac#label-snowflake-feature-store-setup-sql),
then grant the following privileges:

Copy code

```
GRANT CREATE ONLINE FEATURE TABLE ON SCHEMA IDENTIFIER($SCHEMA_FQN) TO ROLE IDENTIFIER($FS_ROLE_PRODUCER);

GRANT SELECT, MONITOR ON FUTURE ONLINE FEATURE TABLES IN SCHEMA IDENTIFIER($SCHEMA_FQN) TO ROLE IDENTIFIER($FS_ROLE_CONSUMER);

GRANT SELECT, MONITOR ON ALL ONLINE FEATURE TABLES IN SCHEMA IDENTIFIER($SCHEMA_FQN) TO ROLE IDENTIFIER($FS_ROLE_CONSUMER);
```

## Read features from the online feature table

To retrieve feature values from hybrid table online storage, use `read_feature_view`
with `store_type=StoreType.ONLINE`. Reads use the hybrid table online feature table,
not the Postgres online service.

Copy code

```
from snowflake.ml.feature_store import StoreType

fv = fs.get_feature_view("MY_ONLINE_FV", "v1")

fs.read_feature_view(
    feature_view=fv,
    keys=[["entity_key_1"], ["entity_key_2"]],
    feature_names=["FEATURE_A", "FEATURE_B"],
    store_type=StoreType.ONLINE,
)
```

Alternatively, you can read features from the hybrid table directly through SQL. This approach isn’t recommended for production use because it can increase latency.

## Time series data handling

To ensure data consistency, you can specify a `timestamp_col`. When multiple rows with the same primary key are found in the source, Snowflake only ingests the version with the most recent timestamp. If you don’t specify a timestamp column, the most recently processed row takes precedence.

## Cost and billing considerations

Online feature tables incur costs across the following consumption modes:

- **Virtual warehouse compute**: Both key lookups and data ingestion operations consume virtual warehouse credits at standard rates. For more information, see [Virtual warehouse credit usage](/user-guide/cost-understanding-compute#label-virtual-warehouse-credit-usage).
- **Cloud Services compute**: Required to identify changes in underlying base objects and determine when refresh operations are needed. For more information, see [Cloud service credit usage](/user-guide/cost-understanding-compute#label-cloud-services-credit-usage).
- **Hybrid table storage**: Storage costs based on flat monthly rate per GB. It’s more expensive than the cost for traditional Snowflake storage, but identical to the cost to store hybrid tables. For more information, see Table 3(b) in the [Credit Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
- **Hybrid table requests**: As of March 1, 2026, hybrid table requests are no longer billed, and metering was disabled soon after this pricing change took effect.

Tip

Incremental refresh can help reduce costs. Incremental updates are generally more cost-efficient than full refresh, resulting in lower compute and data ingestion costs.

### Monitor costs

To monitor costs, use these views:

Copy code

```
-- Hybrid table request credits (historical data only; no new events are recorded)
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.HYBRID_TABLE_USAGE_HISTORY;

-- Storage consumption
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.STORAGE_USAGE;
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.DATABASE_STORAGE_USAGE_HISTORY;

-- Overall costs
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_HISTORY;
```

## Managing offline to online sync

Snowflake refreshes the offline dynamic table on `refresh_freq` and syncs values to the
online feature table on `OnlineConfig.target_lag`. These settings act independently: the
effective lag from source data to the online feature table is approximately
`refresh_freq + target_lag`.

You can also suspend refresh, trigger refreshes manually, and inspect refresh history
through the Python SDK.

### Refresh modes

Snowflake uses the following refresh modes when updating the offline dynamic table and
the online feature table:

- Incremental refresh: Snowflake tracks changes in the sources and merges only the new or
  updated rows into the store. This is the preferred and most efficient mode.
- Full refresh: Snowflake drops all existing data in the table and reloads everything from
  the source. This mode is more resource-intensive and is used when an incremental refresh
  isn’t possible.

Set `refresh_mode` to `INCREMENTAL` or `FULL` on the feature view to choose a mode
explicitly, or use `AUTO` to let Snowflake pick the most efficient available mode.

### Suspend and resume refresh

Use `suspend_feature_view` and `resume_feature_view` to pause or restart refresh for a
feature view. These calls affect both the offline dynamic table and the online feature
table, so offline and online data stay consistent.

Copy code

```
fs.suspend_feature_view(feature_view=fv)
fs.resume_feature_view(feature_view=fv)
```

### Trigger a refresh manually

Use `refresh_feature_view` to trigger a refresh outside the scheduled interval. Pass
`store_type=StoreType.OFFLINE` to refresh the offline dynamic table, or
`store_type=StoreType.ONLINE` to refresh the online feature table.

Copy code

```
from snowflake.ml.feature_store import StoreType

# Refresh the offline dynamic table (default)
fs.refresh_feature_view(feature_view=fv, store_type=StoreType.OFFLINE)

# Refresh the online feature table
fs.refresh_feature_view(feature_view=fv, store_type=StoreType.ONLINE)
```

### View refresh history

Use `get_refresh_history` to inspect past refresh jobs for the offline store or the online
feature table. To monitor refresh jobs in Snowsight, see
[Monitoring and Observability](/developer-guide/snowflake-ml/feature-store/monitoring).

Copy code

```
from snowflake.ml.feature_store import StoreType

# Offline dynamic table refresh history (default)
fs.get_refresh_history(feature_view=fv, store_type=StoreType.OFFLINE)

# Online feature table refresh history
fs.get_refresh_history(feature_view=fv, store_type=StoreType.ONLINE)
```
