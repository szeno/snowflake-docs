# Advanced feature engineering

This page covers advanced feature patterns you’ll use when moving from basic feature
sets to production-grade ML systems.

## Overview of feature patterns

The following patterns describe the different ways you can define, compute, and serve
features in Snowflake Feature Store. These aren’t mutually exclusive categories. A single
feature view can combine multiple patterns. For example, a managed feature view can also be
served online with time-windowed aggregations. Think of each pattern as a capability you
can layer onto your feature views as your requirements evolve:

| Pattern | Description | Online retrieval | How you build it | Examples |
| --- | --- | --- | --- | --- |
| External | Defined and refreshed outside Feature Store (often static or slow-changing). | Yes | Feature View with externally maintained table or view, no `refresh_freq`. | Account tier, signup channel |
| Managed | Feature Store computes and refreshes on a schedule. | Yes | Feature View with `refresh_freq` specified. | Daily engagement score, hourly KPIs |
| Online | Low-latency “latest values” lookup for inference. | Yes | Online feature store or table synced from Feature Views. | Real-time churn scoring, fraud scoring |
| Time-windowed | Trailing-window aggregates over recent history. | Yes | Feature View using the Aggregations API with tiling (`feature_granularity`, `refresh_freq`). | Spend 7d, orders 30d, last N items |
| Rollup | Aggregates features from a lower-level entity to a higher-level entity through a mapping. | No | Rollup Feature View from a source Feature View and a mapping DataFrame. | Visitor to subscriber, card to account |
| Iceberg | Open-format features stored as Dynamic Iceberg Tables for cross-engine interoperability. | No | Feature View with `StorageConfig` pointing to an external volume with `StorageFormat.ICEBERG`. | Features consumed by Spark/Trino, data lake integration |
| Stream (Public Preview) | Real-time event ingestion with near-zero latency feature updates. | Yes | Feature View with `StreamSource` and `StreamConfig` for continuous ingestion. | Live clickstream signals, real-time transaction features |
| Real-time (Public Preview) | On-demand features computed at read time from upstream feature views and per-request inputs. | Yes | Feature View with `RealtimeConfig`, `compute_fn`, and `RequestSource`. | Weighted balance, currency conversion, derived scores |

Expand

Show lessSee more

## Online features

Online feature serving provides low-latency feature retrieval for real-time inference.
It isn’t a separate pattern but a serving configuration you can layer on top of most
other patterns. Enabling online serving synchronizes the latest feature values keyed
by entity so applications can fetch features in milliseconds rather than running
warehouse queries.

Enabling online retrieval doesn’t change how features are computed for offline
datasets. It changes where and how feature values are stored for serving, and synchronization
frequency between online and offline store.

For end-to-end instructions, see
[Serving online features](/developer-guide/snowflake-ml/feature-store/online-feature-store).

### Stream feature views

Public Preview

This feature is in public preview.

Stream feature views provide continuous, near-real-time feature updates from live event
streams. Use this pattern when your model needs features that reflect the very latest
events, with end-to-end freshness of less than 2 seconds, such as live clickstream signals
or real-time transaction features. Stream feature views use a `StreamSource` and
`StreamConfig` to define transformation logic and historical backfill data, and can be
combined with time-windowed aggregation to compute rolling metrics that update
continuously as new events arrive.

For more details, including how to register a stream source, create a stream feature view,
and combine streaming with time-windowed aggregation, see
[Stream feature views](/developer-guide/snowflake-ml/feature-store/online-feature-store#label-online-fs-stream-feature-views).

### Real-time feature views

Public Preview

This feature is in public preview.

Real-time feature views evaluate a Python function during each query to produce
features that can’t be precomputed, whether that means incorporating per-request
inputs like a transaction amount or device fingerprint, deriving new values by
combining upstream feature views (for example, computing a z-score from a stored
mean and standard deviation), or applying last-mile transformations such as filling
nulls or converting units before the data reaches your model.

For more details on how to use real-time feature views, see
[Real-time feature views](/developer-guide/snowflake-ml/feature-store/online-feature-store#label-online-fs-realtime-feature-views).

## Time-windowed aggregation features

Note

Time-windowed aggregation requires `snowflake-ml-python` version 1.24.0 or later.

Time-windowed aggregation computes rolling metrics over recent history, such as “spend
in the last 7 days” or “number of sessions in the last 30 days.” Use this pattern when
your model needs features that summarize recent behavior within a trailing time horizon
and must stay fresh as new events arrive.

With time-windowed aggregations you can:

- Define multiple windows (for example, 1h, 24h, 7d, 30d) over the same event stream once
  and reuse them across many models.
- Generate training datasets that are point-in-time correct, so each training row only uses
  data that would have been available as of the label or event timestamp.
- Reduce compute cost by incrementally maintaining partial aggregates (tiles) instead of
  repeatedly scanning raw events.

### Define time-windowed features

Use the `Feature` class to define aggregate features in the `FeatureView` definition:

| Parameter | Description |
| --- | --- |
| `features` | List of `Feature` objects defining the aggregation logic. |
| `feature_granularity` | The tile size: how frequently aggregation tiles are computed (for example, `"1h"`). |
| `timestamp_col` | The column used for time-indexing. |

Expand

Show lessSee more

Supported aggregation functions:

- `Feature.sum(column, window)`: Sum over a time window
- `Feature.min(column, window)`: Minimum over a time window
- `Feature.max(column, window)`: Maximum over a time window
- `Feature.count(column, window)`: Count over a time window
- `Feature.avg(column, window)`: Average over a time window
- `Feature.last_distinct_n(column, window, n)`: Last N distinct values in a time window (offline only; see [`last_distinct_n` aggregation](#label-fs-last-distinct-n-aggregation))
- `Feature.approx_count_distinct(column, window)`: Approximate distinct count over a time window (see [`approx_count_distinct` aggregation](#label-online-fs-approx-count-distinct))

### Aggregation function support by store type

The following table lists which functions are supported for the offline Feature Store and
the Postgres-backed Online Feature Store. Note that
[Online feature tables (hybrid table)](/developer-guide/snowflake-ml/feature-store/online-feature-store#label-online-serving-hybrid-tables)
do not support time-windowed aggregation functions.

| Aggregation function | Offline Feature Store | Online Feature Store |
| --- | --- | --- |
| `sum`, `min`, `max`, `count`, `avg` | Supported | Supported |
| `approx_count_distinct` | Supported | Supported |
| `last_distinct_n` | Supported | Not supported |

Expand

Show lessSee more

Note

The Postgres-backed online store can maintain running aggregates as events arrive
(for example with `FeatureAggregationMethod.CONTINUOUS`). If you register a feature
view with an unsupported aggregation for Postgres online serving, the Snowflake ML
Python SDK returns an error at registration time.

The following example defines entities, aggregation features, and creates a tiled
feature view:

Copy code

```
from snowflake.ml.feature_store import Entity, Feature, FeatureView

user = Entity(name="user", keys=["USER_ID"])

features = [
    Feature.sum("AMOUNT", "7d").alias("TOTAL_SPEND_7D"),
    Feature.count("EVENT_ID", "30d").alias("EVENT_COUNT_30D"),
    Feature.avg("AMOUNT", "24h").alias("AVG_AMOUNT_24H"),
    Feature.last_distinct_n("PRODUCT_ID", "7d", n=10).alias("RECENT_PRODUCTS_7D"),
]

fv = FeatureView(
    name="USER_BEHAVIOR_WINDOWED",
    entities=[user],
    feature_df=session.table("RAW_EVENTS"),
    timestamp_col="EVENT_TS",
    feature_granularity="1h",
    refresh_freq="1h",
    features=features,
)
```

To make computation scalable, the Feature Store maintains intermediate results at
a fixed `feature_granularity` interval (often hourly or daily). These intermediate
results are refreshed on the `refresh_freq` schedule, then stitched together at
query time to produce “last 7d”, “last 30d”, and similar windows.

### Generate a training set with tiled features

When generating a training set that includes tiled feature views, you must pass
`join_method="cte"` to `generate_training_set`:

Copy code

```
training_df = fs.generate_training_set(
    spine_df=spine_df,
    features=[registered_purchase_fv, registered_agg_fv],
    spine_timestamp_col="SESSION_START_TS",
    spine_label_cols=["LABEL"],
    join_method="cte",
)
```

### Using window offset

The `offset` parameter shifts the lookback window into the past, which is the
standard way to build comparative features such as week-over-week or month-over-month
trends. For example, a 7-day spend feature with `offset="7d"` returns the previous
7-day period relative to the current tile boundary. You can pair this with the current
window to capture momentum or change over time.

The `offset` must be a multiple of `feature_granularity` so the shifted window
aligns cleanly to tile boundaries.

Copy code

```
features = [
    Feature.sum("AMOUNT", "7d").alias("CURRENT_WEEK_SUM"),
    Feature.sum("AMOUNT", "7d", offset="7d").alias("PREV_WEEK_SUM"),
]
```

### Transformations alongside aggregation

In many pipelines, raw events need preparation before they can be aggregated. If you
provide both `feature_df` and `features` in a `FeatureView`, the Feature Store
applies them in a clear order: the `feature_df` transformation runs first to define
and prepare the base dataset, including any joins, filters, or derived columns. The
declarative `Feature` aggregations specified in `features` are then computed on top
of that resulting dataset.

For example, suppose you have raw event data where an `EVENT_JSON` column contains
nested attributes that must be parsed before aggregation. You can use SQL in
`feature_df` to extract structured fields, then apply time-windowed aggregations
using `features`:

Copy code

```
from snowflake.ml.feature_store import Entity, Feature, FeatureView

user = Entity(name="user", keys=["USER_ID"])

preprocess_df = session.sql("""
    SELECT
        USER_ID,
        EVENT_TS,
        TRY_TO_DOUBLE(EVENT_JSON:amount)         AS AMOUNT,
        TRY_TO_VARCHAR(EVENT_JSON:merchant_id)    AS MERCHANT_ID
    FROM RAW_EVENTS
    WHERE EVENT_TYPE = 'PURCHASE'
""")

features = [
    Feature.sum("AMOUNT", "7d").alias("TOTAL_SPEND_7D"),
    Feature.count("MERCHANT_ID", "30d").alias("DISTINCT_MERCHANT_EVENTS_30D"),
]

fv = FeatureView(
    name="USER_PURCHASE_WINDOWED",
    entities=[user],
    feature_df=preprocess_df,
    timestamp_col="EVENT_TS",
    feature_granularity="1h",
    refresh_freq="1h",
    features=features,
)
```

### Best practices for granularity and refresh

Choosing `feature_granularity` and `refresh_freq` is a trade-off between time
precision, freshness, and operational cost:

- **Match granularity to signal velocity.** Hourly granularity is a good default for
  clickstream or transactional activity where recency matters. Daily granularity is
  often sufficient for slower-moving signals such as account-level properties.
- **Align windows and offsets to the tile size.** Window lengths should be an even
  multiple of `feature_granularity` (for example, `"24h"` with `"1h"` tiles, or
  `"28d"` with `"1d"` tiles) so the approximation error margin stays consistent
  over time.
- **Set refresh\_freq to the slowest cadence that meets your freshness needs.** Refreshing
  more frequently than new data arrives rarely improves feature quality but does increase
  compute. In production, it’s common to standardize on a small set of granularity and
  refresh combinations (for example, hourly and daily) to keep cost predictable.

### `approx_count_distinct` aggregation

The `approx_count_distinct` aggregation computes the approximate number of
distinct values within a time window. It uses
[HyperLogLog](https://en.wikipedia.org/wiki/HyperLogLog), a probabilistic
algorithm that estimates cardinality with minimal memory overhead. This makes
it well suited for high-cardinality columns (such as user IDs or product IDs)
where maintaining exact distinct counts in real time would be too expensive.

Copy code

```
from snowflake.ml.feature_store import Feature

features = [
    Feature.approx_count_distinct("PRODUCT_ID", "24h").alias("UNIQUE_PRODUCTS_24H"),
    Feature.approx_count_distinct("SESSION_ID", "1h", precision=12).alias("UNIQUE_SESSIONS_1H"),
]
```

Use the `precision` parameter to control the trade-off between accuracy and
performance. Higher precision uses more memory but produces more accurate
estimates; lower precision uses less memory and runs faster. Valid values
range from `4` to `21`. The default is `8`.

The following table shows the
[Relative Standard Error](https://simple.wikipedia.org/wiki/Standard_error#Relative_standard_error)
(RSE) for each precision setting. RSE is the typical percentage by which the
estimate deviates from the true distinct count. For example, with the default
precision of `8`, the estimate is typically within about 6.5% of the true
value.

| Precision | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **RSE** | 25.7% | 18.2% | 23.0% | 9.16% | 6.49% | 4.59% | 3.24% | 2.30% | 1.62% | 1.15% | 0.81% | 0.57% | 0.41% | 0.29% | 0.20% | 0.14% | 0.10% | 0.07% |

Expand

Show lessSee more

### `last_distinct_n` aggregation

The `last_distinct_n` aggregation returns the last *N* distinct values of a column
observed within a time window, ordered by recency. Use this pattern when your model
needs a short list of recent categorical signals, such as the last 10 products a user
viewed or the last 5 merchants they purchased from.

Copy code

```
from snowflake.ml.feature_store import Feature

features = [
    Feature.last_distinct_n("PRODUCT_ID", "7d", n=10).alias("RECENT_PRODUCTS_7D"),
    Feature.last_distinct_n("MERCHANT_ID", "30d", n=5).alias("RECENT_MERCHANTS_30D"),
]
```

The `n` parameter sets how many distinct values to retain per entity within the window.
Use `last_distinct_n` in batch or offline feature views when you need recency-ordered
distinct lists for training or batch inference.

Note

`last_distinct_n` is supported for the offline Feature Store only. It is not supported
for Postgres-backed online serving. If you register a feature view with `last_distinct_n`
and enable Postgres online serving, the Snowflake ML Python SDK returns an error at
registration time. For online cardinality estimates, use [`approx_count_distinct`](#label-online-fs-approx-count-distinct)
instead.

### Secondary key aggregation

Secondary key aggregation uses an additional column to break down your time-windowed
aggregations into finer-grained groups without changing the entity key you query by.
You can use `aggregation_secondary_keys` with any feature view that uses time-windowed
aggregation, whether it’s a batch feature view or a stream feature view.

By default, time-windowed aggregations produce a single value per entity key. For
example, a feature view keyed by `USER_ID` might compute `CLICK_COUNT_24H`, giving
one click count per user across all activity.

But what if you need those aggregations broken down by a second dimension that you
don’t know ahead of time? Consider a retailer who tracks user clicks on product
offers. They want to know how many times each user clicked on each offer in the past
24 hours. The entity key is `USER_ID`, and the breakdown column is `OFFER_ID`.

Without secondary keys, the retailer would need to look up every `OFFER_ID`
associated with a user and make a separate feature request for each
`(USER_ID, OFFER_ID)` pair, which is impractical when the set of offer IDs
is large or unknown at request time. The `aggregation_secondary_keys`
parameter solves this by letting you query with
just the entity key (`USER_ID`) and get back aggregations grouped by the secondary key
(`OFFER_ID`) in a single response.

When you set `aggregation_secondary_keys`, the Feature Store computes each aggregation
independently for every distinct value of the secondary key within the time window.
At query time, you request features using only the entity key, and the response
contains the aggregated values broken down by the secondary key.

For example, querying `USER_ID=1234` returns:

| USER\_ID | OFFER\_ID | CLICK\_COUNT\_24H |
| --- | --- | --- |
| 1234 | offer\_A | 5 |
| 1234 | offer\_B | 12 |
| 1234 | offer\_C | 1 |

Expand

Show lessSee more

#### Define a feature view with a secondary key

The entity for the feature view is the primary key you’ll query by (`USER_ID`). The
`aggregation_secondary_keys` column (`OFFER_ID`) must be present in the source
schema but isn’t part of the entity definition. The following example uses a stream
feature view, but the same parameter works with batch feature views that use
time-windowed aggregation.

Copy code

```
from snowflake.ml.feature_store.spec.enums import FeatureAggregationMethod

features = [
    Feature.count("OFFER_ID", "24h").alias("CLICK_COUNT_24H"),
    Feature.max("EVENT_TS", "48h").alias("LATEST_CLICK_48H"),
]

offer_clicks_fv = FeatureView(
    name="user_offer_clicks",
    entities=[user_entity],
    stream_config=stream_cfg,
    timestamp_col="EVENT_TS",
    refresh_freq="1 minute",
    feature_granularity="1 minute",
    features=features,
    online_config=OnlineConfig(
        enable=True,
        store_type=OnlineStoreType.POSTGRES,
    ),
    feature_aggregation_method=FeatureAggregationMethod.CONTINUOUS,
    aggregation_secondary_keys=["OFFER_ID"],
    desc="Per-offer click aggregations grouped by offer, queryable by user",
)

registered_fv = fs.register_feature_view(offer_clicks_fv, version="V1")
```

At query time, a single request for `USER_ID=1234` returns one row per `OFFER_ID`
with the aggregated click counts, without needing to know the offer IDs in advance.
To ingest events for stream feature views, see
[Stream feature views](/developer-guide/snowflake-ml/feature-store/online-feature-store#label-online-fs-stream-feature-views)
and the [Ingest API reference](/developer-guide/snowflake-ml/feature-store/online-feature-store-ingest-api-reference).

## Rollup aggregation features

Note

Rollup aggregation requires `snowflake-ml-python` version 1.26.0 or later.

Rollup aggregation lets you derive higher-level features from existing lower-level
feature views without reprocessing raw events. Use this pattern whenever your model
operates at a coarser granularity than your source features, such as rolling product-level
metrics up to categories, user-level signals up to cohorts, or transaction-level features
up to merchants.

In Snowflake Feature Store, a rollup Feature View is defined from two inputs:

1. A registered source Feature View at the lower-level entity.
2. A mapping dataset that maps lower-level keys to higher-level keys.

The Feature Store applies the mapping and aggregates the source feature values to
produce features keyed by the higher-level entity.

### Example: Product to category rollup

Assume you already compute product-level features (one row per `PRODUCT_ID`), and
you want category-level features (one row per `CATEGORY_ID`) by rolling up all
products in the category.

**Source Feature View output (PRODUCT\_ID level):**

The following shows example output from a registered source Feature View
`PRODUCT_SALES_FV`:

| PRODUCT\_ID | UNITS\_SOLD\_30D | REVENUE\_30D |
| --- | --- | --- |
| P101 | 120 | 2400.00 |
| P102 | 35 | 700.00 |
| P201 | 80 | 1600.00 |

Expand

Show lessSee more

**Mapping table (PRODUCT\_ID to CATEGORY\_ID):**

| PRODUCT\_ID | CATEGORY\_ID |
| --- | --- |
| P101 | CAT10 |
| P102 | CAT10 |
| P201 | CAT20 |

Expand

Show lessSee more

To create the category-level rollup, provide the source Feature View and a mapping
DataFrame, then register a new Feature View keyed by `CATEGORY_ID`:

Copy code

```
from snowflake.ml.feature_store import Entity, FeatureView, RollupConfig

product = Entity("product", keys=["PRODUCT_ID"])
category = Entity("category", keys=["CATEGORY_ID"])

mapping_df = session.table("PRODUCT_CATEGORY_MAPPING")

rollup_config = RollupConfig(
    source=product_sales_fv,
    mapping_df=mapping_df,
)

category_rollup_fv = FeatureView(
    name="CATEGORY_SALES_ROLLUP",
    entities=[category],
    rollup_config=rollup_config,
)

category_rollup_fv = fs.register_feature_view(category_rollup_fv, version="v1")
```

This gives you category-level features that are consistent with the product-level
definitions and reusable for models that operate at the category level (for example,
category demand forecasting).

**Rolled-up result (CATEGORY\_ID level):**

| CATEGORY\_ID | UNITS\_SOLD\_30D\_SUM | REVENUE\_30D\_SUM | PRODUCT\_COUNT |
| --- | --- | --- | --- |
| CAT10 | 155 | 3100.00 | 2 |
| CAT20 | 80 | 1600.00 | 1 |

Expand

Show lessSee more

Once registered, a rollup Feature View is consumed like any other Feature View.
You join it to a spine using the target entity key (`CATEGORY_ID` in this example).
Downstream users don’t need to know whether features came from raw events or from a
rollup. They simply request features from the Feature View they need.

### Feature column prefixing for disambiguation

When generating datasets from multiple feature views, column name collisions can
occur if different feature views contain features with identical names (for example,
`COUNT_7D`). Snowflake provides two ways to disambiguate column names.

**Option 1: Auto-prefix**

Use `auto_prefix=True` to automatically prefix all feature columns with
`{FV_NAME}_{VERSION}_`, which guarantees uniqueness when multiple Feature Views
contain the same feature names.

Copy code

```
product_sales_fv = fs.get_feature_view("PRODUCT_SALES_FV", "v1")
category_rollup_fv = fs.get_feature_view("CATEGORY_SALES_ROLLUP", "v1")

dataset = fs.generate_dataset(
    spine_df=category_spine,
    features=[product_sales_fv, category_rollup_fv],
    spine_timestamp_col="EVENT_TS",
    auto_prefix=True,
)

# Output columns include:
# PRODUCT_SALES_FV_V1_REVENUE_30D
# CATEGORY_SALES_ROLLUP_V1_REVENUE_30D
```

**Option 2: Custom names**

Use `.with_name()` to assign readable custom prefixes to specific feature views.

Copy code

```
dataset = fs.generate_dataset(
    spine_df=category_spine,
    features=[
        product_sales_fv.with_name("product"),
        category_rollup_fv.with_name("category"),
    ],
    spine_timestamp_col="EVENT_TS",
)

# Output columns include:
# PRODUCT_REVENUE_30D
# CATEGORY_REVENUE_30D
```

## Append-only batch feature view

Note

Requires `snowflake-ml-python` version 1.41 or later.

Append-only batch feature views preserve a complete history of feature snapshots for
point-in-time correct training. Use this pattern when your model training requires
knowing exactly what feature values looked like in a past moment.
Both standard and append-only batch feature views produce point-in-time correct
training data. The difference is how much history they retain. Standard batch feature
views keep only the latest values: each refresh overwrites the previous snapshot, so
training joins are always against the most recent version. Append-only batch feature
views retain every version by appending the current feature values alongside a
timestamp on each refresh, building up a full history of how features changed over
time. This deeper history lets the Feature Store join the feature values that were
current as of each row’s timestamp in your training spine, which is important when
feature drift matters and you need to reconstruct what the model would have seen at
any point in the past.

### How it works

When you set `append_only=True` on a `FeatureView`, each scheduled refresh
appends the current feature values to a persistent snapshot table managed by
the Feature Store. Over time, this table accumulates a time series of feature
snapshots. This parameter requires `timestamp_col` and a cron expression for
`refresh_freq`.

### Backfill from existing history

If you already have historical feature snapshots, pass `backup_source` with
the fully qualified table name to seed the snapshot table at registration time.
The Feature Store clones the backup table (a zero-copy operation) and validates
that it contains the required entity join keys and timestamp column.

### Schema evolution

Append-only feature views support extend-only schema changes: you can add new
columns to the source, but dropping, reordering, or changing the data type of
existing columns isn’t supported. Re-registering with `overwrite=True` isn’t
allowed for append-only feature views. If you re-register an existing
append-only feature view as a standard (non-append-only) feature view with
`overwrite=True`, the accumulated snapshot table is dropped.

### Generate point-in-time correct training sets

As with regular batch feature views, use `generate_dataset` with `spine_timestamp_col`
to build training sets from the accumulated snapshots. For each row in the
spine, the Feature Store performs an ASOF join and selects the most recent
snapshot row for each entity key at or before the spine timestamp. This ensures
that the training set reflects the features as they existed at the time of
each training example, preventing future data from leaking into the model.

The `spine_timestamp_col` column must also exist in the feature view’s output.
When an append-only feature view is used as a feature source,
`spine_timestamp_col` is required.

Register an append-only feature view:

Copy code

```
from snowflake.ml.feature_store import Entity, FeatureStore, FeatureView

fs = FeatureStore(session, db, schema, default_warehouse=warehouse)
e = Entity("CUSTOMER", ["id"])
fs.register_entity(e)

fv = FeatureView(
    name="customer_features",
    entities=[e],
    feature_df=session.sql("SELECT id, score, ts FROM customer_source"),
    timestamp_col="ts",
    refresh_mode="FULL",
    refresh_freq="0 0 * * * UTC",  # daily; cron is required for append_only
    append_only=True,
    backup_source="MY_DB.MY_SCHEMA.HISTORICAL_SNAPSHOTS",
)
registered_fv = fs.register_feature_view(feature_view=fv, version="v1")
```

Build a point-in-time correct training set from the accumulated snapshots. For each
row in the spine, the Feature Store performs an as-of join to select the most recent
snapshot at or before the spine timestamp:

Copy code

```
spine_df = session.create_dataframe(
    [(1, "2024-01-15 00:00:00", 0), (2, "2024-01-15 00:00:00", 1)],
    schema=["id", "event_ts", "label"],
)
training_set = fs.generate_training_set(
    spine_df=spine_df,
    features=[registered_fv],
    spine_timestamp_col="event_ts",
    spine_label_cols=["label"],
)
```

## Iceberg-backed feature views

Iceberg-backed feature views store features as Dynamic Iceberg Tables for cross-engine
interoperability. Use this pattern when downstream consumers need to read feature data
using external engines such as Spark, Trino, or Flink through the Iceberg open table
format, or when you want to integrate feature pipelines with a broader data lake
architecture.

Note

Requires `snowflake-ml-python` version 1.26.0 or later. An
[external volume](/sql-reference/sql/create-external-volume) configured for
Iceberg storage is also required.

Iceberg-backed feature views don’t support online feature retrieval today. Use them for
batch training, offline feature serving, and cross-engine interoperability scenarios.

### Configure storage for Iceberg

Use `StorageConfig` to point the feature view at your external volume. The `base_location`
specifies the subdirectory within the external volume where Iceberg metadata and data files
are written.

Copy code

```
from snowflake.ml.feature_store.feature_view import StorageConfig, StorageFormat

storage_config = StorageConfig(
    external_volume="MY_ICEBERG_EXTERNAL_VOLUME",
    format=StorageFormat.ICEBERG,
    base_location="my_feature_view_data",
)
```

### Create an Iceberg-backed feature view

Pass `storage_config` when creating the `FeatureView`. A `refresh_freq` is required
because the underlying Dynamic Iceberg Table needs a refresh schedule.

Copy code

```
fv = FeatureView(
    name="MY_ICEBERG_FEATURES",
    entities=[my_entity],
    feature_df=source_df,
    timestamp_col="TS",
    refresh_freq="1d",
    storage_config=storage_config,
    desc="Features stored as a Dynamic Iceberg Table",
)

registered_fv = fs.register_feature_view(fv, version="1")
```

Note

Iceberg supports microsecond precision for timestamp types. If your source data uses
nanosecond precision, cast it to microsecond precision (for example, `TIMESTAMP(6)`) in
your feature DataFrame.
