# Serving online features

[Preview Feature — Open](/release-notes/preview-features)

Available to all accounts. Requires `snowflake-ml-python` version 1.41 or later.

Online feature serving stores the latest feature values keyed by entity so applications
can fetch features in milliseconds rather than running warehouse queries. The Online
Feature Store uses a managed Postgres serving layer for ultra-low-latency reads, stream
ingestion, time-windowed aggregations, and REST APIs. Enable online serving on a feature
view when you create it, or update an existing feature view later.

The Online Feature Store is well suited for real-time ML applications such as fraud
detection, recommendations, and personalization. It stays integrated with your batch
feature pipeline for training while serving the same feature values at inference time.

![Architecture of the Snowflake Online Feature Store showing offline feature views, the Postgres online serving layer, stream ingest, and online feature retrieval.](/static/images/screens/feature-store-architecture.png)

The following table summarizes ways you can use the Online Feature Store:

| Use | Description |
| --- | --- |
| Batch online feature views | Serve the latest row per entity key from batch feature views. |
| Stream feature views | Ingest events in real time and serve updated features with end-to-end freshness of less than two seconds. Includes stream sources, transformations, and backfill. |
| Real-time feature views | Compute features at query time from request inputs and upstream feature views. |
| REST ingest and query API | HTTP endpoints for streaming data ingestion and online feature retrieval. |
| Feature groups | Bundle multiple feature views into one versioned set for online reads and training. See [Feature groups](/developer-guide/snowflake-ml/feature-store/feature-groups). |

Expand

Show lessSee more

If you are interested in online serving using hybrid tables, see
[Online serving with hybrid tables](#label-online-serving-hybrid-tables).

Resources

For a hands-on walkthrough, see the
[Online Feature Store quickstart notebook](https://github.com/snowflake-labs/sf-samples/blob/main/samples/ml/feature_store/online_feature_store_postgres_quickstart.ipynb).

## How the Online Feature Store works

The online store stays in sync with your offline feature pipeline automatically, so you
don’t need separate sync jobs or extra infrastructure.

The Online Feature Store receives feature data in two ways:

- From the offline store: Feature values computed in the offline pipeline are
  synchronized to the online store on a schedule you configure with `target_lag`.
- From a stream or request source: For sub-minute freshness, features are computed
  as events arrive or at query time. See
  [Stream feature views](#label-online-fs-stream-feature-views) and
  [Real-time feature views](#label-online-fs-realtime-feature-views).

For real-time ML workloads, serving latency and data freshness matter most.

Serving latency is how long the store takes to return feature values at inference
time. The Online Feature Store achieves 10 ms p50 serving latency through the REST
query API.

Data freshness is the end-to-end lag from a source event to an updated served feature
value. For example, when a user generates clickstream events, freshness includes the time
to ingest events, compute features, update the online store, and make values available for
retrieval. With stream ingestion, end-to-end freshness is under 2 seconds.

Freshness depends on how you populate the online store:

- Offline to online sync: Set `target_lag` from 10 seconds to 8 days. Use
  this path when minute-scale freshness is acceptable.
- Stream ingest: Features update as events land in the ingest endpoint. Use stream
  feature views when you need sub-minute freshness.

Snowflake refreshes the online store in the background. If refresh fails five times in a
row, the online table is suspended. To troubleshoot, check your refresh history.

## Enabling online serving for feature views

Before you create an online feature store, complete the following:

- Install the Snowflake ML Python package:

  Copy code

  ```
  pip install --upgrade --force-reinstall "snowflake-ml-python>=1.41"
  ```
- Configure [Feature Store access control](/developer-guide/snowflake-ml/feature-store/rbac)
  for producer and consumer roles.
- Set up authentication using a [Programmatic Access Token (PAT)](/user-guide/programmatic-access-tokens)
  or [key pair authentication](/user-guide/key-pair-auth). For details, see
  [Base URL and authentication](#label-online-fs-rest-auth). If using a PAT:

  Copy code

  ```
  export SNOWFLAKE_PAT="<your_pat_token>"
  ```
- If your account has Tri-Secret Secure enabled, configure
  Postgres CMK before creating the online service. Without this, you’ll receive:
  `SnowparkSQLException: (1304): Postgres CMK setup required for Tri-Secret Secure accounts`.
  See [Snowflake Postgres Tri-Secret Secure](/user-guide/snowflake-postgres/postgres-tss).

You can create the feature store the same way you create an offline feature store. For details, see
[Creating or connecting to a feature store](/developer-guide/snowflake-ml/feature-store/create).
There is no special parameter you need to set at the feature store level to enable online serving.

Configure the online store details in the Feature View definition, pass an `OnlineConfig` with `store_type=OnlineStoreType.POSTGRES` when defining the feature view.
The following example creates a batch feature view that passes columns from the source
table to the online store. The online store serves the latest row per entity key.

Copy code

```
from snowflake.ml.feature_store import FeatureView, OnlineConfig, OnlineStoreType

source_df = session.table("CLICKSTREAM_DATA.ORDERS")

profile_fv = FeatureView(
    name="USER_BEHAVIOR_PROFILE",
    entities=[user_entity],
    feature_df=source_df,
    timestamp_col="LAST_ACTIVITY_TS",
    refresh_freq="1m",
    online_config=OnlineConfig(
        enable=True,
        target_lag="10s",
        store_type=OnlineStoreType.POSTGRES,
    ),
    desc="User behavior profile: purchases + engagement from orders and events",
)

registered_profile_fv = fs.register_feature_view(profile_fv, version="V1")
```

The following are the `OnlineConfig` parameters:

| Parameter | Type | Description | Default |
| --- | --- | --- | --- |
| `enable` | Boolean, optional | Specifies whether online feature serving should be enabled for the feature view. | `False` |
| `target_lag` | Str, optional | Target data freshness lag in a `"&lt;num&gt; (seconds|minutes|hours|days|s|m|h|d)"` format. Used for offline-to-online sync only; not used for stream feature views. | `10 seconds` |
| `store_type` | Enum, optional | Online store implementation. Set to `OnlineStoreType.POSTGRES` for the Online Feature Store. | `OnlineStoreType.HYBRID_TABLE` |

Expand

Show lessSee more

Note

`refresh_freq` controls how often the offline dynamic table refreshes when source data
changes. `OnlineConfig.target_lag` controls how often those offline values sync to the
online store. These settings act independently. In the example above, the effective lag from
source data to the online store is approximately `refresh_freq + online_config.target_lag`.

Warning

When `store_type=OnlineStoreType.POSTGRES`, keep the **combined length of the feature view
name and version at 46 characters or fewer**. The Postgres-backed online store maps feature
views to internal Postgres object names subject to Postgres identifier limits. Names that
are too long can be truncated and cause collisions or ingest errors. See
[Feature view name length with Postgres online serving](#label-online-fs-troubleshooting-postgres-name-length).

For existing feature views, update the online serving configuration with `update_feature_view`:

Copy code

```
from snowflake.ml.feature_store import OnlineConfig, OnlineStoreType

# Enable online feature serving
fs.update_feature_view(
    name="<name>",
    version="<version>",
    online_config=OnlineConfig(
        enable=True,
        target_lag="10s",
        store_type=OnlineStoreType.POSTGRES,
    ),
)

# Disable online feature serving
fs.update_feature_view(
    name="<name>",
    version="<version>",
    online_config=OnlineConfig(enable=False),
)
```

## Create the online service

The online service is a managed serving layer for low-latency online reads.
Create it once per feature store before registering feature views with online serving
enabled. The online service enables you to ingest data into the online store and read features from the online store using a REST API.

The `create_online_service` method takes the Snowflake database role names for the
producer (creates and operates on feature views) and consumer (reads feature views and
entities). These are the same roles you configure in
[Feature Store access control](/developer-guide/snowflake-ml/feature-store/rbac). Note that the role calling `create_online_service` must have the `CREATE SCHEMA` privilege on the
feature store database.

Copy code

```
create_result = fs.create_online_service("FS_PRODUCER_ROLE", "FS_CONSUMER_ROLE")
print(create_result)
```

Note

The online service runs continuously after you create it. Keep it running to serve online
traffic in production. For testing or development, call `drop_online_service()` when you’re
done to minimize cost of unused resources.

The online service can take several minutes to provision on first creation. Poll the status
until it reaches `RUNNING`:

Copy code

```
import time

status = fs.get_online_service_status()
while status.status != "RUNNING":
    time.sleep(30)
    status = fs.get_online_service_status()
    print(f"Status: {status.status}")

print(f"Size: {status.size}")
print(f"Query URL: {status.endpoints}")
```

### Choose an online service size

Note

Requires `snowflake-ml-python` version 1.54 or later.

The online service is provisioned at a size that determines its serving capacity. To pin a
size at creation, pass the `size` keyword argument. Larger sizes serve more concurrent reads
and ingestion throughput at higher cost.

Copy code

```
create_result = fs.create_online_service(
    "FS_PRODUCER_ROLE",
    "FS_CONSUMER_ROLE",
    size="M",
)
```

The `size` argument accepts one of the following values (case-insensitive):

| Size | Notes |
| --- | --- |
| `XS` | Prototyping and experiments. Available only at creation; an `XS` service can’t be resized later. |
| `S` | Light or early-stage production: a small working set and low QPS (roughly tens of QPS). |
| `M` | Steady production traffic with a moderate working set. Roughly double `S` (roughly 100 to 300 QPS). |
| `L` | Larger working sets or higher query and ingest QPS (roughly 300 to 500+ QPS). Roughly double `M`. |
| `XL` | High-throughput serving with a large in-memory working set (500+ QPS, with more latency headroom). |
| `2XL` | Very high throughput or very large working sets. Roughly double `XL`. |
| `3XL` | The largest workloads, with the most memory and serving headroom. |

Expand

Show lessSee more

The QPS ranges are rough, order-of-magnitude starting points for directional guidance, not
guarantees. Your actual size depends on your workload, so use these to pick a starting size and
then right-size against real traffic. See [Estimate the size you need](#label-online-fs-estimate-size)
for the factors that drive sizing.

When you omit `size`, the server applies its default size. Accounts that cap the available
size are provisioned at their cap instead. To read the size a service is provisioned at, check
the `size` attribute on the status returned by `get_online_service_status()`. This attribute is
`None` for services created before sizes were recorded.

To change the size of an existing online service, see
[Resize the online service](#label-online-fs-resize-online-service).

### Estimate the size you need

Note

These are rough guidelines, not performance guarantees. The right size depends on your data
and traffic, so benchmark your own workload and adjust. Because you can
[resize a running service](#label-online-fs-resize-online-service) up or down, you don’t have to
get this exactly right up front: start conservatively and scale based on what you observe.

The online store keeps feature values in memory for low-latency reads, so the size you need is
driven mainly by these factors:

- **Working set size.** The total online data that must fit in memory: roughly the number of
  entity keys multiplied by the number and size of the features across all online feature views.
  This is usually the dominant factor. Size for headroom above your current data rather than for
  an exact fit.
- **Read throughput and concurrency.** Your sustained and peak query QPS, and how many features
  (or feature groups) each request fetches.
- **Ingest throughput.** Your sustained and peak write and stream-ingest QPS.
- **Latency target.** The store targets about 10 ms p50 (see
  [Retrieval latency performance and benchmarking](#label-online-python-retrieve-features-from-online-storage)).
  Holding a tight latency target under high concurrency needs more headroom.

Each step up the tiers (`S` to `M` to `L`, and so on) roughly doubles the memory and serving
headroom available to the service. As a starting point:

- Use `XS` or `S` for prototyping and light workloads.
- Move up a tier or two for steady production traffic, based on your working set and peak QPS.
- Leave headroom for background work. Backfills, offline to online syncs, and feature view re-registration can
  run alongside peak serving traffic, so provision enough that they don’t compete with online reads.

If you’re unsure, start one tier above your minimum estimate, watch latency and utilization under
real traffic, and resize from there. Use the
[Online Feature Store Benchmark Kit](https://github.com/Snowflake-Labs/snowflake-feature-store-online-benchmark-kit)
to measure your workload before committing to a size.

**Signs a service is underprovisioned.** When a service is too small for its load, read latency
rises (especially p90 and p99), latency gets more variable, and a severely overloaded service
starts returning query or ingest errors. Watch request volume, latency percentiles, and error
rate on the
[Online Serving tab](/developer-guide/snowflake-ml/feature-store/monitoring#label-fs-monitoring-online-serving)
of the Feature Store monitoring view, including while background jobs run at peak traffic. If
latency trends toward your target or errors climb, [resize up](#label-online-fs-resize-online-service)
a tier.

### Resize the online service

Note

Requires `snowflake-ml-python` version 2.0.0 or later.

As your serving load changes, resize a running online service up or down with
`alter_online_service`. Pass the target `size` as a keyword argument:

Copy code

```
fs.alter_online_service(size="L")
```

Brief downtime during resize

A resize ends with a database failover that causes about 20 seconds of downtime, during which
online queries and ingestion return errors. Plan resizes for a low-traffic window and make sure
your clients retry. The service serves normally for the rest of the resize, which can otherwise
run for hours.

The `size` argument accepts one of `S`, `M`, `L`, `XL`, `2XL`, or `3XL` (case-insensitive).
Unlike [creation](#label-online-fs-create-online-service-size), `XS` isn’t a valid source or
target: it’s a prototyping tier, so reaching another size from an `XS` service means re-creating
the service.

Keep the following in mind when resizing:

- **Resize up or down.** You can move to any other tier in a single call, in either direction and
  any distance (for example, `S` directly to `L`, or `2XL` down to `M`). `alter_online_service` will raise an error if you request the size the service is already running at.
- **The service must be `RUNNING`.** Requesting a different size while a resize is already in
  flight is rejected. Re-requesting the size a resize is already converging to does nothing.
- **Resizing runs in the background.** `alter_online_service` returns as soon as the request is
  recorded. The change then runs in the background and can take hours on a large service. The
  service serves online reads and stream ingestion for most of the resize, except for about
  20 seconds of downtime at the final database failover, when queries and ingestion return
  errors. The service reports status `UPDATING_SIZE` while the change converges. An accepted
  resize can’t be cancelled: drop and re-create the service to stop one early.

Poll `get_online_service_status()` until the status is `RUNNING` and `size` is the size you
requested:

Copy code

```
import time

fs.alter_online_service(size="L")

status = fs.get_online_service_status()
while not (status.status == "RUNNING" and status.size == "L"):
    time.sleep(60)
    status = fs.get_online_service_status()
    print(f"Status: {status.status}, size: {status.size}")
```

## Read from the online store

Use the online store to retrieve feature values for specific entity keys at inference time.
You can read from a single feature view or from a [feature group](/developer-guide/snowflake-ml/feature-store/feature-groups)
that bundles multiple feature views into one versioned set. Feature groups let your model call
`read_feature_group` once instead of querying each feature view separately, and the same group
can be passed to `generate_training_set` for training. You can also query features through the
[REST query API](#label-online-fs-rest-query), including requests with `object_type=feature_group`.

### Read a single feature view

Use `read_feature_view` with `store_type="online"` to look up features from the Postgres online store.

First get a reference to the feature view object:

Copy code

```
fv = fs.get_feature_view("USER_BEHAVIOR_PROFILE", "V1")
```

Then read features from the online store:

Copy code

```
online_df = fs.read_feature_view(
    fv,
    keys=[["user_1"], ["user_2"], ["user_3"]],
    store_type="online",
)
online_df.show()
```

### Read a feature group

When a model consumes features from multiple feature views, register a [Feature group](/developer-guide/snowflake-ml/feature-store/feature-groups) and use
`read_feature_group` to fetch all member features in one round-trip.

Copy code

```
fg = fs.get_feature_group("USER_FG", "v1")

online_df = fs.read_feature_group(fg, keys=[["user_1"], ["user_2"], ["user_3"]])
online_df.show()
```

## Retrieval latency performance and benchmarking

The Postgres-backed online store is optimized for low-latency feature retrieval. In general, you can
expect 10ms p50, sub-15ms p95, and sub-20ms p99 latency through the REST query API.

Actual latency depends on factors such as the number of features per entity, the number
of entity keys per request, network distance between the caller and the online service,
and the payload size.

To measure latency in your own environment, we have released a
[Online Feature Store Benchmark Kit](https://github.com/Snowflake-Labs/snowflake-feature-store-online-benchmark-kit),
which provides scripts and instructions for running reproducible latency benchmarks against
your online service.

## Integrate with real-time model inference

In addition to fetching features with the Python SDK or the Query REST API, you can deploy a model from the
[Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview) as a managed real-time inference
service that automatically looks up feature values from the online store at inference time.

When your online feature store uses `OnlineStoreType.POSTGRES`, pass `feature_sources_per_function` to
`create_service()` to map a registered feature view to a model method (such as `predict`). At inference time, the
model service fetches any missing feature columns from the feature view before invoking the model. You can send only
entity IDs in the request payload and let the service retrieve the rest.

`mv` is a `ModelVersion` object from the [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview). Obtain it with `reg.get_model("my_model").version("v1")`, where `reg` is a `snowflake.ml.registry.Registry` object.

Copy code

```
mv = reg.get_model("my_model").version("v1")

mv.create_service(
    service_name="myservice",
    service_compute_pool="my_compute_pool",
    ingress_enabled=True,
    feature_sources_per_function={"predict": [registered_fv]},
)
```

For more details, see [Online Feature Store integration](/developer-guide/snowflake-ml/inference/real-time-inference-rest-api#label-real-time-inference-online-feature-store-integration)
in the real-time inference documentation.

## Stream feature views

Stream feature views allow you to ingest events in real time and serve updated
features with near-zero latency. They use a `StreamSource` to define the event schema
and a `StreamConfig` to specify the transformation logic and historical backfill data.

![Stream feature view architecture](/static/images/streamFV_diagram.png)

### Register a stream source

A `StreamSource` defines the schema for events that will be ingested in real time.
The column names and types must exactly match what is sent through the REST API.

Copy code

```
from snowflake.ml.feature_store import StreamSource
from snowflake.snowpark.types import (
    StructType, StructField, StringType, FloatType,
    TimestampType, TimestampTimeZone,
)

event_stream = StreamSource(
    name="CLICKSTREAM_EVENTS",
    schema=StructType([
        StructField("USER_ID", StringType()),
        StructField("EVENT_TS", TimestampType(TimestampTimeZone.NTZ)),
        StructField("EVENT_TYPE", StringType()),
        StructField("PRODUCT_ID", StringType()),
        StructField("AMOUNT", FloatType()),
    ]),
    desc="Real-time clickstream events for user activity tracking",
)

fs.register_stream_source(event_stream)
```

You can manage stream sources with:

- `fs.list_stream_sources()`: List all registered stream sources
- `fs.delete_stream_source(name)`: Delete a stream source
- `fs.ingest(name, records)`: Ingest a list of records (dicts) into a named stream source

### Create a stream feature view

A stream feature view uses a `StreamConfig` to link a registered stream source, a
transformation function, and a backfill DataFrame. The online store serves the latest
row per entity key.

#### Define the transformation function

The transformation function (`transformation_fn`) must be a named Python function
that takes a pandas DataFrame as input and returns a pandas DataFrame as output
(`pd.DataFrame` -> `pd.DataFrame`). Snowflake applies it to incoming stream events at
ingest time and to historical backfill data at registration time, so live and
backfilled features use the same logic. Lambdas and callable classes aren’t supported.
Inside the function, you can use `pandas`, `numpy`, `re`, `copy`, and Python built-ins.

Copy code

```
import pandas as pd

def transform_events(df: pd.DataFrame) -> pd.DataFrame:
    """Transform incoming events. Receives and returns a pandas DataFrame."""
    df["AMOUNT_CENTS"] = (df["AMOUNT"] * 100).astype(int)
    return df
```

#### Provide backfill data

`backfill_df` is a Snowpark DataFrame of historical events that match your
`StreamSource` schema. When you register the feature view, Snowflake runs
`transformation_fn` on this data server-side and loads the results into the online
store. That seeds serving with existing feature values before live events arrive
through the Ingest API.

Use a permanent table or view for `backfill_df`. Its SQL must be re-executable from
a fresh session, so avoid temporary tables, cached results, or DataFrames created from
local data. Column names and types must match the registered stream source. Do not pass
`feature_df` on a stream feature view; use `backfill_df` instead.

Copy code

```
backfill_df = session.table("CLICKSTREAM_DATA.BACKFILL_CLICKSTREAM_EVENTS")
```

#### Register the stream feature view

Pass the stream source, transformation function, and backfill DataFrame in
`StreamConfig`, then register the feature view with Postgres online serving enabled:

Copy code

```
from snowflake.ml.feature_store import FeatureView, OnlineConfig, OnlineStoreType, StreamConfig

stream_fv = FeatureView(
    name="USER_REALTIME_EVENTS",
    entities=[user_entity],
    timestamp_col="EVENT_TS",
    stream_config=StreamConfig(
        stream_source=event_stream,
        transformation_fn=transform_events,
        backfill_df=backfill_df,
    ),
    online_config=OnlineConfig(
        enable=True,
        target_lag="10s",
        store_type=OnlineStoreType.POSTGRES,
    ),
    desc="Real-time clickstream events: passthrough columns for online serving",
)

registered_stream_fv = fs.register_feature_view(stream_fv, version="V1")
```

### Stream feature view with time-windowed aggregation

You can combine stream ingestion with time-windowed aggregation to compute rolling metrics
(such as total spend over 48 hours) that update continuously as new events arrive. For
details on defining time-windowed aggregation features and which aggregations are
supported for Postgres online serving, see
[Time-windowed aggregation features](/developer-guide/snowflake-ml/feature-store/advanced-feature-engineering#label-fs-aggregation-support-by-store).

To get fresher online features, you can further enable continuous aggregation by setting the feature aggregation method as
`FeatureAggregationMethod.CONTINUOUS`. This instructs the online service to maintain running aggregates as events arrive
through the Ingest API, rather than periodically re-tiling from the offline store.

Copy code

```
from snowflake.ml.feature_store import Feature, FeatureView, OnlineConfig, OnlineStoreType
from snowflake.ml.feature_store.spec.enums import FeatureAggregationMethod

features = [
    Feature.sum("AMOUNT", "48h").alias("TOTAL_SPEND_48H"),
    Feature.count("AMOUNT", "48h").alias("TXN_COUNT_48H"),
]

stream_agg_fv = FeatureView(
    name="user_realtime_agg_features",
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
    desc="Real-time user transaction aggregations with continuous processing",
)

registered_fv = fs.register_feature_view(stream_agg_fv, version="V1")
```

## Real-time feature views

Many ML features can’t be precomputed because they depend on information that only
exists at the time of request. For example, a fraud model needs the current transaction amount
to compare against historical averages. A pricing model needs the live exchange rate
to convert a stored balance. A recommendation model needs the user’s current location
to weight nearby offers.

Real-time feature views solve this by running a Python function (`compute_fn`) at
query time rather than precomputing and storing results. When you call
`read_feature_view`, the online service evaluates the function against the latest
values from upstream feature views together with per-request inputs you provide,
and returns the computed result in the same call.

Common use cases include:

- Features from request-time data: Incorporate values that are only available at
  inference time, such as the current transaction amount, user GPS coordinates, or
  device context.
- Derived features from upstream feature views: Combine or transform values from
  one or more precomputed feature views into new features, such as a risk score that
  multiplies a transaction amount by a stored fraud probability.
- Post-processing on the fly: Apply null imputation, normalization, unit
  conversion, or other cleanup to stored feature values before they reach the model.

### Author the compute function

The compute function receives pandas DataFrames as input and returns a pandas
DataFrame. The first parameter receives the per-request data (from the
`RequestSource`), and each subsequent parameter receives the latest feature
values from one of the source feature views. The returned DataFrame must
contain the columns declared in `output_schema`.

The framework aligns input rows by position: row 0 of every input DataFrame
corresponds to the same entity key. You don’t need to handle join keys in
the function; they’re added to the output automatically.

Copy code

```
import pandas as pd

def compute_weighted_balance(request_df, balance_df):
    """WEIGHTED_BALANCE = BALANCE * WEIGHT, positional row alignment."""
    weight = request_df["WEIGHT"].astype(float).reset_index(drop=True)
    balance = balance_df["BALANCE"].fillna(0.0).reset_index(drop=True)
    return pd.DataFrame({"WEIGHTED_BALANCE": balance * weight})
```

The function must be a named function defined at module level or in a notebook
cell. Lambdas and callable classes aren’t supported. The number of parameters
must match the number of entries in `RealtimeConfig.sources`.

Inside the function, you can use `pandas`, `numpy`, `re`, `copy`, and Python
built-ins. Other imports aren’t supported and cause an error at registration
time.

### Define and register

Wrap the compute function in a `RealtimeConfig` together with its sources and
the output schema, then attach it to a `FeatureView`.

Copy code

```
from snowflake.ml.feature_store import (
    FeatureView, RealtimeConfig, RequestSource,
)
from snowflake.snowpark.types import DoubleType, StructField, StructType

request_source = RequestSource(
    schema=StructType([StructField("WEIGHT", DoubleType())]),
)

weighted_balance_rtfv = FeatureView(
    name="user_weighted_balance",
    entities=[user_entity],
    realtime_config=RealtimeConfig(
        compute_fn=compute_weighted_balance,
        sources=[request_source, reg_balance],
        output_schema=StructType([StructField("WEIGHTED_BALANCE", DoubleType())]),
    ),
    desc="Per-request weighted balance",
)

reg_rtfv = fs.register_feature_view(weighted_balance_rtfv, "V1")
```

The `sources` list begins with an optional `RequestSource` (for per-request
input), followed by one or more registered feature views or feature view
slices. Don’t include entity join keys in `RequestSource.schema`; the server
adds them automatically. Feature groups can’t be used as sources for a
real-time feature view.

### Read real-time features from the online store

When reading a real-time feature view, pass a `request_context` DataFrame
with one row per entity key. Each row provides the per-request inputs for
the corresponding key.

Copy code

```
import pandas as pd

pdf = fs.read_feature_view(
    reg_rtfv,
    keys=[["user_1"], ["user_2"], ["user_3"]],
    request_context=pd.DataFrame({"WEIGHT": [3.0, 2.0, 5.0]}),
)
```

Two row-alignment rules apply:

1. `request_context` must have exactly as many rows as there are entity keys.
2. Row *i* of `request_context` is paired with `keys[i]`, and the result
   preserves that order.

If a source feature view has no stored value for a requested entity key, the
corresponding DataFrame passed to `compute_fn` omits that row. Handle
missing values inside the function (for example, with `.fillna(0.0)`) to
ensure deterministic output.

Real-time feature views don’t have offline storage at the feature view level;
`read_feature_view` always reads through the online service. To generate a
training set that combines batch and real-time features, see
[Feature groups](/developer-guide/snowflake-ml/feature-store/feature-groups).

## REST API

In addition to the Python SDK, the online service exposes REST endpoints for
streaming data ingestion and online feature retrieval. These endpoints enable
integration with non-Python applications. Query requests accept either a feature view or a
[feature group](/developer-guide/snowflake-ml/feature-store/feature-groups) through the
`object_type` parameter.

For the complete API specifications, see:

- [Ingest API reference](/developer-guide/snowflake-ml/feature-store/online-feature-store-ingest-api-reference)
- [Query API reference](/developer-guide/snowflake-ml/feature-store/online-feature-store-query-api-reference)

### Base URL and authentication

Online reads through the Python SDK (`read_feature_view`, `read_feature_group`) and
REST query calls both require authentication and network connectivity to the online
service. Set a `SNOWFLAKE_PAT` environment variable or configure key-pair JWT
authentication as described in the setup prerequisites. The sections below cover
endpoint URLs, PrivateLink routing, and network rules.

Each online service has ingest and query endpoint URLs. Retrieve them from the
online service status:

Copy code

```
from snowflake.ml.feature_store import online_service

status = fs.get_online_service_status()
query_url = online_service.endpoint_url(status, "query")
ingest_url = online_service.endpoint_url(status, "ingest")
```

### PrivateLink URL configuration

By default, `endpoint_url` returns the PrivateLink URL when the account has
PrivateLink enabled. If the account doesn’t have a PrivateLink URL, it uses
SPCS-internal URLs when running inside SPCS, or falls back to the public URL
otherwise. For information about setting up private connectivity, see
[Snowpark Container Services private connectivity](/developer-guide/snowpark-container-services/private-connectivity).

To list all available endpoints (public, PrivateLink, and internal), run:

Copy code

```
SELECT SYSTEM$GET_FEATURE_STORE_ONLINE_SERVICE_STATUS('MY_DB.MY_FEATURE_STORE_SCHEMA')
```

To override the default URL routing, pass `online_service_access` when
initializing the Feature Store:

Copy code

```
from snowflake.ml.feature_store import FeatureStore, CreationMode
from snowflake.ml.feature_store.online_service import OnlineServiceAccess

fs = FeatureStore(
    session=session,
    database="CLICKSTREAM_FS_DEMO",
    name="FEATURE_STORE",
    default_warehouse="DEMO_WH",
    creation_mode=CreationMode.CREATE_IF_NOT_EXIST,
    online_service_access=OnlineServiceAccess.PRIVATELINK,  # or PUBLIC, INTERNAL
)
```

Valid values:

- `OnlineServiceAccess.PUBLIC`: Force the public REST API URL.
- `OnlineServiceAccess.PRIVATELINK`: Force the PrivateLink REST API URL.
- `OnlineServiceAccess.INTERNAL`: Force the SPCS-internal REST API URL.

All REST requests must include an `Authorization` header and set
`Content-Type: application/json`. You can authenticate with either a PAT or
a key pair JWT.

Using a PAT:

```
Authorization: Snowflake Token="<your_pat_token>"
Content-Type: application/json
```

## Online serving with hybrid tables

Snowflake also supports online serving through [online feature tables](/sql-reference/commands-feature-store)
backed by hybrid tables. This product is generally available and synchronizes the latest
feature values from the offline store on a schedule you configure with `target_lag`.

Use hybrid table online serving when you need low-latency point lookups for batch feature
views and don’t require Postgres-backed capabilities. Hybrid tables don’t support the
Online Feature Store online service, stream ingest, real-time feature views, REST APIs,
or the time-windowed aggregation API. That aggregation API isn’t currently supported
for hybrid table online serving. For those workloads, use `OnlineStoreType.POSTGRES` in
the sections above.

### Prerequisites

Important

You must have Snowflake version 9.26 or later and `snowflake-ml-python` version 1.18.0
or later to use hybrid table online serving.

Hybrid table online serving doesn’t use the Postgres online service. You don’t need to
call `create_online_service`, set `SNOWFLAKE_PAT`, or configure network access for the
REST endpoints described earlier on this page.

Create or connect to a feature store the same way you do for offline feature views. For
details, see [Creating or connecting to a feature store](/developer-guide/snowflake-ml/feature-store/create).

### Enable hybrid table online serving

Enable online serving in `OnlineConfig` on a batch feature view. When you omit
`store_type`, the feature view uses hybrid table online serving by default
(`OnlineStoreType.HYBRID_TABLE`). For parameter descriptions, see the
[`OnlineConfig` table](#batch-online-feature-views) above.

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

The `refresh_freq` and `target_lag` settings work the same way as described in [Enabling online serving for feature views](#batch-online-feature-views).

### Permissions

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

### Read features from hybrid table online store

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

### Time series data handling

To ensure data consistency, you can specify a `timestamp_col`. When multiple rows with the same primary key are found in the source, Snowflake only ingests the version with the most recent timestamp. If you don’t specify a timestamp column, the most recently processed row takes precedence.

### Understanding costs

Online feature tables incur costs across the following consumption modes:

- **Virtual warehouse compute**: Both key lookups and data ingestion operations consume virtual warehouse credits at standard rates. For more information, see [Virtual warehouse credit usage](/user-guide/cost-understanding-compute#label-virtual-warehouse-credit-usage).
- **Cloud Services compute**: Required to identify changes in underlying base objects and determine when refresh operations are needed. For more information, see [Cloud service credit usage](/user-guide/cost-understanding-compute#label-cloud-services-credit-usage).
- **Hybrid table storage**: Storage costs based on flat monthly rate per GB. It’s more expensive than the cost for traditional Snowflake storage, but identical to the cost to store hybrid tables. For more information, see Table 3(b) in the [Credit Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
- **Hybrid table requests**: As of March 1, 2026, hybrid table requests are no longer billed, and metering was disabled soon after this pricing change took effect.

Tip

Incremental refresh can help reduce costs. Incremental updates are generally more cost-efficient than full refresh, resulting in lower compute and data ingestion costs.

### Cost monitoring

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

For batch feature views with online serving enabled, Snowflake refreshes the offline
dynamic table on `refresh_freq` and syncs values to the online store on
`OnlineConfig.target_lag`. These settings apply to both Postgres and hybrid table online
serving.

You can also suspend refresh, trigger refreshes manually, and inspect refresh history
through the Python SDK.

### Refresh modes

Snowflake uses the following refresh modes when updating the offline dynamic table and,
for hybrid table online serving, the online feature table:

- Incremental refresh: Snowflake tracks changes in the sources and merges only the new or
  updated rows into the store. This is the preferred and most efficient mode.
- Full refresh: Snowflake drops all existing data in the table and reloads everything from
  the source. This mode is more resource-intensive and is used when an incremental refresh
  is not possible.

Set `refresh_mode` to `INCREMENTAL`, `FULL`, or `AUTO` on the feature view to choose a
mode explicitly, or use `AUTO` to let Snowflake pick the most efficient available mode.

For Postgres online serving, the Online Service syncs the online store automatically on
`target_lag`. Manual online refresh isn’t supported on that path.

### Suspend and resume refresh

Use `suspend_feature_view` and `resume_feature_view` to pause or restart refresh for a
feature view. These calls affect both the offline dynamic table and the online store so
offline and online data stay consistent.

Copy code

```
fs.suspend_feature_view(feature_view=fv)
fs.resume_feature_view(feature_view=fv)
```

### Trigger a refresh manually

Use `refresh_feature_view` to trigger a refresh outside the scheduled interval. Pass
`store_type=StoreType.OFFLINE` to refresh the offline dynamic table, or
`store_type=StoreType.ONLINE` to refresh a hybrid table online feature table.

Copy code

```
from snowflake.ml.feature_store import StoreType

# Refresh the offline dynamic table (default)
fs.refresh_feature_view(feature_view=fv, store_type=StoreType.OFFLINE)

# Refresh the hybrid table online feature table
fs.refresh_feature_view(feature_view=fv, store_type=StoreType.ONLINE)
```

Note

Manual online refresh isn’t supported when `store_type=OnlineStoreType.POSTGRES`. Postgres
online stores are refreshed automatically by the Online Service.

### View refresh history

Use `get_refresh_history` to inspect past refresh jobs for the offline store or online
store. To monitor refresh jobs in Snowsight, see
[Monitoring and Observability](/developer-guide/snowflake-ml/feature-store/monitoring).

Copy code

```
from snowflake.ml.feature_store import StoreType

# Offline dynamic table refresh history (default)
fs.get_refresh_history(feature_view=fv, store_type=StoreType.OFFLINE)

# Online store refresh history
fs.get_refresh_history(feature_view=fv, store_type=StoreType.ONLINE)
```

## Troubleshooting

This section lists common Online Feature Store issues and actionable workarounds
you can apply from your account or client environment. Platform-level limitations
that require admin action are listed under
[Known limitations](#label-online-fs-troubleshooting-known-limitations).

### Object already exists error on online service creation

If you receive the following error when calling `create_online_service()`:

```
RuntimeError: (2110) SQL compilation error: Object 'FS_RUNTIME_PG_NR_<id>' already exists.
```

A previous online service creation was interrupted or left in a partial state. Drop the
existing online service and recreate it:

Copy code

```
fs.drop_online_service()
fs.create_online_service("FS_PRODUCER_ROLE", "FS_CONSUMER_ROLE")
```

### Backfill fails and online table stays empty

When a stream feature view backfill job fails, it sets `backfill_status` to `FAILED`. The
SDK cleans up the `$BACKFILL` staging table by design and doesn’t retry. The online table
can then poll an empty staging table every 10 seconds and skip updates indefinitely. The
system can’t self-heal from this state.

Diagnose the root cause:

Copy code

```
-- Find the error from the backfill task
SELECT NAME, STATE, ERROR_CODE, ERROR_MESSAGE, SCHEDULED_TIME, COMPLETED_TIME, RETURN_VALUE
FROM TABLE(MY_DB.INFORMATION_SCHEMA.TASK_HISTORY(RESULT_LIMIT => 200))
WHERE NAME LIKE 'MY_FEATURE_VIEW$V1$BACKFILL%'
ORDER BY SCHEDULED_TIME DESC;

-- Check SDK metadata state
SELECT METADATA, UPDATED_AT
FROM MY_DB.MY_FEATURE_STORE._FEATURE_STORE_METADATA
WHERE OBJECT_TYPE = 'FEATURE_VIEW'
  AND OBJECT_NAME = 'MY_FEATURE_VIEW'
  AND VERSION = 'V1'
  AND METADATA_TYPE = 'STREAM_CONFIG';
```

Workaround: re-register the feature view with `overwrite=True` to reset state and
trigger a fresh backfill:

Copy code

```
fs.register_feature_view(my_feature_view, version="V1", overwrite=True)
```

Related caveats:

- If the feature view source is a SQL view rather than a base table, backfill is more
  likely to fail. Use a base table as the source where possible.
- For datasets larger than 10 million rows, use at least an XL warehouse. A backfill
  failure with no obvious SQL error can indicate out-of-memory on an undersized warehouse.

### Online table initial sync is stuck

After `create_online_service()` or `register_feature_view()`, the online table can show
initial sync running indefinitely without raising an error.

Diagnose task history:

Copy code

```
SELECT *
FROM TABLE(MY_DB.INFORMATION_SCHEMA.TASK_HISTORY(RESULT_LIMIT => 100))
WHERE NAME LIKE 'MY_FEATURE_VIEW$V1%'
ORDER BY SCHEDULED_TIME DESC;
```

Workaround: drop and recreate the online service to reset internal state:

Copy code

```
fs.drop_online_service()
fs.create_online_service("FS_PRODUCER_ROLE", "FS_CONSUMER_ROLE")
```

If sync hangs again, re-register the feature view:

Copy code

```
fs.register_feature_view(my_feature_view, version="V1", overwrite=True)
```

### Online service unreachable (DNS resolution with PrivateLink)

Error:

```
RuntimeError: (1500) Online Service is unreachable: [Errno 8] nodename nor servname provided, or not known
```

Accounts with both public and PrivateLink endpoints can resolve to a PrivateLink hostname
when `online_service_access` isn’t set or is set to `OnlineServiceAccess.PRIVATELINK`. That
hostname isn’t DNS-resolvable from machines outside the private network, such as a
developer laptop.

Set `online_service_access` when you construct the `FeatureStore` to match the network
your client runs on. For more context, see
[PrivateLink URL configuration](#label-online-fs-rest-auth).

Copy code

```
from snowflake.ml.feature_store import FeatureStore
from snowflake.ml.feature_store.online_service import OnlineServiceAccess

# From a developer laptop or public internet
fs = FeatureStore(
    session=session,
    database="MY_DB",
    name="MY_FEATURE_STORE",
    default_warehouse="MY_WH",
    online_service_access=OnlineServiceAccess.PUBLIC,
)

# From a server on the private network
fs = FeatureStore(
    session=session,
    database="MY_DB",
    name="MY_FEATURE_STORE",
    default_warehouse="MY_WH",
    online_service_access=OnlineServiceAccess.PRIVATELINK,
)
```

### HTTP 401: client IP not allowed

Error:

```
RuntimeError: (2201) Online Service error (HTTP 401): Authentication/authorization failed:
{"responseType":"ERROR_UNAUTHORIZED","detail":"Incoming request with IP/Token <your_ip> is not allowed to access Snowflake. ..."}
```

The SPCS endpoint that hosts the online service can enforce a network ingress rule that
doesn’t include your client IP. This is separate from account-level network policy: you
might reach Snowflake SQL endpoints but still be blocked at the SPCS endpoint.

Workaround: ask your Snowflake account admin to add the client IP to the network rule
attached to the SPCS endpoint:

Copy code

```
SHOW NETWORK RULES;

ALTER NETWORK RULE MY_NETWORK_RULE
  SET VALUE_LIST = ('203.0.113.10', '203.0.113.11', '198.51.100.5');
```

If online reads worked before and suddenly fail with HTTP 401, check whether network rules
were recently modified.

### Python UDF fails with dataclasses import blocked

Error (often surfaced through the Online Service REST API):

```
Online Service error: Blocked: importing 'dataclasses' is not allowed in UDFs
```

When a Python transform returns a list of dicts (for example,
`[{"COL": val}]`), pandas can lazy-load the `dataclasses` module during deserialization.
Snowflake UDFs block that import, so the transform fails. The error might appear as a
generic HTTP 500 from the online service.

Construct the output DataFrame directly instead of using a list of dicts:

Copy code

```
# Fails: pandas triggers dataclasses lazy-load from list of dicts
def my_transform(df: pd.DataFrame) -> pd.DataFrame:
    results = [{"MY_OUTPUT_COL": compute(row)} for _, row in df.iterrows()]
    return pd.DataFrame(results)

# Works: build columns directly
def my_transform(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "MY_OUTPUT_COL": df["MY_INPUT_COL"].apply(compute),
    })
```

### Feature group read fails when a member feature view is unhealthy

Error:

```
RuntimeError: (2201) Online Service error (HTTP 500): ...
```

Reading a feature group aggregates results from multiple feature views. If one member
feature view’s online table is stuck (hung sync, failed backfill), the entire group read
can fail even when other members are healthy. For more information about feature groups, see
[Feature groups](/developer-guide/snowflake-ml/feature-store/feature-groups).

Read each member feature view individually to find the failing one:

Copy code

```
fv_a = fs.get_feature_view("FV_A", "V1")
fv_b = fs.get_feature_view("FV_B", "V1")

result_a = fs.read_feature_view(fv_a, keys=[["entity_key"]], store_type="online")
result_b = fs.read_feature_view(fv_b, keys=[["entity_key"]], store_type="online")
```

Apply the workaround for the failing feature view (see
[Backfill fails and online table stays empty](#label-online-fs-troubleshooting-backfill-failed)
or [Online table initial sync is stuck](#label-online-fs-troubleshooting-sync-stuck)), then retry
the feature group read.

### Offline read returns incorrect feature values

Symptoms:

- `read_feature_view(..., store_type="online")` returns expected feature values for all users.
- `read_feature_view(..., store_type="offline")` returns entity keys but incorrect feature values
  for some users (for example, a count of `0` when the online read shows a value greater than zero).
- Offline refresh history, the transform UDF table, and the underlying dynamic table look healthy.

This divergence is often caused by the session `TIMEZONE` parameter. Offline reads through the
Python SDK can interpret timestamp columns using the session timezone rather than the timezone
stored in the feature table. Online reads through the Postgres-backed online store do not show
the same behavior because those timestamps are handled as NTZ/UTC. Offline-only or hybrid-table
feature views can also use `TIMESTAMP_LTZ`, so you can’t assume all offline data is stored in UTC.

Workaround: set the session timezone to UTC before calling `read_feature_view` with
`store_type="offline"`:

Copy code

```
ALTER SESSION SET TIMEZONE = 'UTC';
```

Copy code

```
fv = fs.get_feature_view("MY_FEATURE_VIEW", "V1")

offline_df = fs.read_feature_view(
    fv,
    keys=[["entity_key"]],
    store_type="offline",
)
offline_df.show()
```

Snowflake is working on timezone-aware offline reads for a future release. Until then, use UTC
for any notebook, job, or pipeline that reads offline feature views. For a general summary, see
[Known limitations](/developer-guide/snowflake-ml/feature-store/feature-views#label-feature-store-known-limitations)
on the feature views page.

### Feature view name length with Postgres online serving

PostgreSQL limits identifier length (`NAMEDATALEN` is a compile-time constant; the usable
length is 63 characters). This limit can’t be changed at runtime or through Snowflake
account configuration.

When you enable online serving with `OnlineStoreType.POSTGRES`, the online service creates
internal Postgres objects for each feature view. Snowflake adds fixed metadata padding to
the feature view name and version when building those internal names. As a result, the
**combined length of the feature view `name` and `version` must not exceed 46 characters**.

If the combined length exceeds this limit, registration might succeed, but the online
service can truncate internal Postgres identifiers. That can lead to:

- Collisions between feature views that differ only after truncation
- Undefined behavior when reading or ingesting features
- Stream ingest or online service errors (for example, HTTP 500)

Snowflake allows longer feature view names for offline-only feature views and for Snowflake
SQL identifiers generally (for example, version strings up to 128 characters). Those longer
limits do not apply to Postgres-backed online serving.

**Workaround:** Use abbreviated feature view names and short version strings before
registering with `OnlineStoreType.POSTGRES`. Plan naming conventions before migrating large
feature view catalogs to the online store.

**Example:** A feature view named `sender_document_sender_device_ip_address_count_endtoend_uuid_new_city`
(69 characters) with version `V1` exceeds the limit. Shorten the name (and version if needed)
so `len(name) + len(version) <= 46`.

Future SDK releases might reject registration when the combined length exceeds this limit.
Until then, validate name length in your own pipelines when enabling Postgres online serving.

### Known limitations

Accounts with Tri-Secret Secure enabled on PrivateLink must complete Postgres CMK setup
before creating the online service. Without CMK configuration, online service creation fails.
For more information, see [Snowflake Postgres Tri-Secret Secure](/user-guide/snowflake-postgres/postgres-tss).
