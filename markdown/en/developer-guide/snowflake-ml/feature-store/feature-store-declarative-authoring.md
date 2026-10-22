# Declarative authoring

Each object in a declarative project is a single file under `sources/`, authored as YAML or
Python. This page covers how to author each object kind. For the project directory
structure, the `manifest.yml` schema, deployment targets, and templating, see
[Declarative project configuration](/developer-guide/snowflake-ml/feature-store/feature-store-declarative-projects).
For the end-to-end workflow, see
[Declarative feature store overview](/developer-guide/snowflake-ml/feature-store/feature-development-lifecycle).

## Author entities

An entity declares the join key that a feature view is grouped by. The same entity can be
shared by many feature views.

YAML (`sources/entities/USER_ID.yaml`):

Copy code

```
kind: Entity
name: USER_ID
join_keys:
  - name: USER_ID
    type: StringType
description: Shared user identifier.
```

Python (`sources/entities/user_id.py`):

Copy code

```
from snowflake.ml.feature_store.decl import Entity, FSColumn

user_id = Entity(
    name="USER_ID",
    join_keys=[FSColumn(name="USER_ID", type="StringType")],
    description="Shared user identifier.",
)
```

The order of `join_keys` matters: it sets the order in which the keys appear in the online
feature table’s primary key.

## Author data sources

A source declares where feature data comes from. There are two kinds:

- A **batch source** reads from a Snowflake table or SQL query.
- A **streaming source** declares the schema of records pushed to the online service’s
  ingest endpoint.

### Batch sources

A `BatchSource` must set exactly one of `table`, `query`, or `query_file`.

YAML (`sources/datasources/EVENTS_BATCH_DECL.yaml`):

Copy code

```
kind: BatchSource
name: EVENTS_BATCH_DECL
table: RAW_EVENTS_BATCH_DECL
columns:
  - name: USER_ID
    type: StringType
  - name: EVENT_TS
    type: TimestampType
  - name: METRIC_VAL
    type: FloatType
```

Python (`sources/datasources/events_batch_decl.py`):

Copy code

```
from snowflake.ml.feature_store.decl import BatchSource, FSColumn

events_batch_decl = BatchSource(
    name="EVENTS_BATCH_DECL",
    table="RAW_EVENTS_BATCH_DECL",
    columns=[
        FSColumn(name="USER_ID", type="StringType"),
        FSColumn(name="EVENT_TS", type="TimestampType"),
        FSColumn(name="METRIC_VAL", type="FloatType"),
    ],
)
```

Use `query` for an inline SQL `SELECT`, or `query_file` to keep a long query in a sibling
`.sql` file (which also supports templating). In the Python form, pass `query="SELECT ..."`
in place of `table=`. Batch SQL supports `--` single-line and `/* ... */` block comments.
C-style `//` comments aren’t supported.

### Streaming sources

A `StreamingSource` registers the schema of incoming records as metadata. It doesn’t create
a Snowflake table. The column set is also a runtime contract: the client-side preflight in
`snow feature ingest` rejects payloads that don’t match the registered columns before any
HTTP call.

YAML (`sources/datasources/CLICKSTREAM_EVENTS.yaml`):

Copy code

```
kind: StreamingSource
name: CLICKSTREAM_EVENTS
type: REST
columns:
  - name: USER_ID
    type: StringType
  - name: EVENT_TYPE
    type: StringType
  - name: TIMESTAMP
    type: TimestampType
  - name: TIME_ON_PAGE_SECONDS
    type: DoubleType
```

Python (`sources/datasources/clickstream_events.py`):

Copy code

```
from snowflake.ml.feature_store.decl import FSColumn, StreamingSource

clickstream_events = StreamingSource(
    name="CLICKSTREAM_EVENTS",
    type="REST",
    columns=[
        FSColumn(name="USER_ID", type="StringType"),
        FSColumn(name="EVENT_TYPE", type="StringType"),
        FSColumn(name="TIMESTAMP", type="TimestampType"),
        FSColumn(name="TIME_ON_PAGE_SECONDS", type="DoubleType"),
    ],
)
```

`REST` is the only supported wire protocol today.

## Author batch feature views

A batch feature view materializes features from a batch source into a
[dynamic table](/user-guide/dynamic-tables/overview) that refreshes on a schedule. It can
be **online** (`online: true`, which also materializes an online feature table for
low-latency lookups) or **offline-only** (`online: false`, suitable for training-set
generation).

### Passthrough feature view

The simplest batch feature view projects its source with no aggregation:

YAML (`sources/feature_views/MY_BATCH_FV_BATCH_DECL.yaml`):

Copy code

```
kind: BatchFeatureView
name: MY_BATCH_FV_BATCH_DECL
version: V1
online: true
target_lag: 1 minute
entities:
  - USER_ID
sources:
  - name: EVENTS_BATCH_DECL
    source_type: Batch
refresh_freq: 1 minute
```

Python (`sources/feature_views/my_batch_fv_batch_decl.py`) references the source object
directly:

Copy code

```
from snowflake.ml.feature_store.decl import BatchFeatureView
from events_batch_decl import events_batch_decl

my_batch_fv_batch_decl = BatchFeatureView(
    name="MY_BATCH_FV_BATCH_DECL",
    version="V1",
    online=True,
    target_lag="1 minute",
    entities=["USER_ID"],
    sources=[events_batch_decl],
    refresh_freq="1 minute",
)
```

`refresh_freq` sets the dynamic table refresh cadence (a duration such as `"5 minutes"` or a
CRON expression). `target_lag` sets the online feature table staleness target and is valid
only when `online: true`.

### Tiled aggregation

To serve time-windowed aggregations, add a `timestamp_col`, declare the tile size with
`feature_granularity`, set `feature_aggregation_method: tiles`, and list the aggregation
`features`:

YAML (`sources/feature_views/MY_ADV_BFV_DECL.yaml`):

Copy code

```
kind: BatchFeatureView
name: MY_ADV_BFV_DECL
version: V1
online: false
entities:
  - USER_ID
sources:
  - name: EVENTS_ADV_DECL
    source_type: Batch
timestamp_col: EVENT_TS
feature_granularity: 1h
feature_aggregation_method: tiles
refresh_freq: 5 minutes
features:
  - source_column:
      name: AMOUNT
      type: FloatType
    output_column:
      name: AMOUNT_SUM_1H
      type: FloatType
    function: sum
    window: 1h
```

Python (`sources/feature_views/my_adv_bfv_decl.py`):

Copy code

```
from snowflake.ml.feature_store.decl import BatchFeatureView, Feature, FSColumn
from events_adv_decl import events_adv_decl

my_adv_bfv_decl = BatchFeatureView(
    name="MY_ADV_BFV_DECL",
    version="V1",
    online=False,
    entities=["USER_ID"],
    sources=[events_adv_decl],
    timestamp_col="EVENT_TS",
    feature_granularity="1h",
    feature_aggregation_method="tiles",
    refresh_freq="5 minutes",
    features=[
        Feature(
            source_column=FSColumn(name="AMOUNT", type="FloatType"),
            output_column=FSColumn(name="AMOUNT_SUM_1H", type="FloatType"),
            function="sum",
            window="1h",
        ),
    ],
)
```

Aggregation features are validated at plan time, before any Snowflake call. Every feature
needs a `function`, a `source_column`, an `output_column`, and a window.

### Append-only feature views

An append-only batch feature view retains history for point-in-time correct training-set
generation. Instead of overwriting the dynamic table on each refresh, it appends the current
contents to a companion snapshot table. Set `append_only: true`. This mode requires
`refresh_mode: FULL`, a CRON `refresh_freq`, and a `timestamp_col`, and it doesn’t support
tiled aggregation:

YAML (`sources/feature_views/MY_APPEND_BFV_DECL.yaml`):

Copy code

```
kind: BatchFeatureView
name: MY_APPEND_BFV_DECL
version: V1
online: true
target_lag: 1 minute
entities:
  - USER_ID
sources:
  - name: EVENTS_APPEND_DECL
    source_type: Batch
timestamp_col: EVENT_TS
refresh_mode: FULL
refresh_freq: 0 0 * * * UTC
append_only: true
```

Python (`sources/feature_views/my_append_bfv_decl.py`):

Copy code

```
from snowflake.ml.feature_store.decl import BatchFeatureView
from events_append_decl import events_append_decl

my_append_bfv_decl = BatchFeatureView(
    name="MY_APPEND_BFV_DECL",
    version="V1",
    online=True,
    target_lag="1 minute",
    entities=["USER_ID"],
    sources=[events_append_decl],
    timestamp_col="EVENT_TS",
    refresh_mode="FULL",
    refresh_freq="0 0 * * * UTC",
    append_only=True,
)
```

For training-only use with no online lookup, set `online: false` and drop `target_lag`
(it’s rejected on offline feature views). Everything else is unchanged.

### Online compared to offline

The following table compares the two serving modes for a batch feature view:

| Aspect | `online: true` | `online: false` |
| --- | --- | --- |
| Online feature table created? | Yes, queryable with `snow feature query` | No, only the offline dynamic table |
| Requires the online service? | Yes | No |
| `target_lag` field | Allowed (online staleness) | Rejected at load time |
| Suitable for | Low-latency point lookups | Training-set generation |
| Usable in a feature group? | Yes | No |

Expand

Show lessSee more

### Destructive compared to non-destructive edits

Operational edits apply in place through `UPDATE_FV`. Structural edits require a drop and
recreate through `RECREATE_FV`, which `apply` refuses without `--destructive`. The following
table lists how each kind of edit is planned:

| Edit | Plan operation | Destructive? |
| --- | --- | --- |
| `refresh_freq`, `target_lag`, `warehouse`, `description` | `UPDATE_FV` | No |
| Schema-preserving edit on a deployed append-only feature view | `EVOLVE_FV` | No, keeps snapshot history |
| `cluster_by`, `refresh_mode`, aggregation features, source schema, `append_only` | `RECREATE_FV` | Yes |
| Removing the feature view file | `DROP_FV` | Yes |

Expand

Show lessSee more

## Author streaming feature views

A streaming feature view computes features from a real-time push stream and serves them
through a Postgres-backed online feature table. Records arrive on the online service’s
ingest endpoint, flow through a pandas user-defined function, and materialize into tiled or
continuous aggregations.

Streaming feature views are always online. Authoring `online: false` is rejected. A
streaming feature view binds an entity and a streaming source, declares a `udf` that
transforms incoming rows, and declares aggregation `features`:

YAML (`sources/feature_views/USER_CLICK_STATS_DECL.yaml`):

Copy code

```
kind: StreamingFeatureView
name: USER_CLICK_STATS_DECL
version: V1
entities:
  - USER_ID
timestamp_col: TIMESTAMP
feature_granularity_sec: 300
feature_aggregation_method: tiles
refresh_freq: 5 minutes
sources:
  - name: CLICKSTREAM_EVENTS
    source_type: Stream
features:
  - output_column:
      name: TOTAL_ENGAGEMENT_1H
      type: DoubleType
    window_sec: 3600
    function: sum
    source_column:
      name: ENGAGEMENT_SCORE
      type: DoubleType
udf:
  name: compute_engagement_metrics
  engine: pandas
  file: USER_CLICK_STATS_DECL.py
  output_columns:
    - name: USER_ID
      type: StringType
    - name: TIMESTAMP
      type: TimestampType
    - name: ENGAGEMENT_SCORE
      type: DoubleType
```

The `udf.file` value points at a sibling Python file containing the named transformation
function (`sources/feature_views/USER_CLICK_STATS_DECL.py`). The loader reads the file’s
source and inlines it as the UDF body:

Copy code

```
import pandas as pd

def compute_engagement_metrics(clickstream: pd.DataFrame) -> pd.DataFrame:
    """Compute engagement metrics from click-stream events."""
    df = clickstream.copy()
    weights = {"page_view": 1.0, "click": 2.0, "purchase": 10.0}
    df["ENGAGEMENT_SCORE"] = df["EVENT_TYPE"].map(weights).fillna(1.0)
    return df[["USER_ID", "TIMESTAMP", "ENGAGEMENT_SCORE"]]
```

The Python declarative form collapses the YAML and its sidecar UDF file into a single file,
passing the transformation function as a callable:

Copy code

```
from __future__ import annotations

import pandas as pd

from snowflake.ml.feature_store.decl import (
    Feature, FSColumn, StreamingFeatureView, UDF,
)
from clickstream_events import clickstream_events

def compute_engagement_metrics(clickstream: pd.DataFrame) -> pd.DataFrame:
    df = clickstream.copy()
    weights = {"page_view": 1.0, "click": 2.0, "purchase": 10.0}
    df["ENGAGEMENT_SCORE"] = df["EVENT_TYPE"].map(weights).fillna(1.0)
    return df[["USER_ID", "TIMESTAMP", "ENGAGEMENT_SCORE"]]

user_click_stats_decl = StreamingFeatureView(
    name="USER_CLICK_STATS_DECL",
    version="V1",
    entities=["USER_ID"],
    sources=[clickstream_events],
    timestamp_col="TIMESTAMP",
    feature_granularity_sec=300,
    feature_aggregation_method="tiles",
    refresh_freq="5 minutes",
    udf=UDF(
        name="compute_engagement_metrics",
        engine="pandas",
        function_definition=compute_engagement_metrics,
        output_columns=[
            FSColumn(name="USER_ID", type="StringType"),
            FSColumn(name="TIMESTAMP", type="TimestampType"),
            FSColumn(name="ENGAGEMENT_SCORE", type="DoubleType"),
        ],
    ),
    features=[
        Feature(
            output_column=FSColumn(name="TOTAL_ENGAGEMENT_1H", type="DoubleType"),
            source_column=FSColumn(name="ENGAGEMENT_SCORE", type="DoubleType"),
            window_sec=3600,
            function="sum",
        ),
    ],
)
```

The UDF’s signature is `(df: pd.DataFrame) -> pd.DataFrame`. It must be a named top-level
function (no lambdas, nested definitions, or class methods) and may import only from
`numpy`, `pandas`, `re`, and `copy`.

`refresh_freq` sets the cadence of the offline tile dynamic table and is required whenever a
feature declares a window. The online feature table itself always serves at 0-second lag,
so `target_lag` is rejected on streaming feature views. For continuous aggregation, set
`feature_aggregation_method: continuous`.

Changes to a streaming feature view’s transformation or aggregation schema can’t be patched
in place: they route through `RECREATE_FV`. Use versions (`V1`, `V2`) to roll out a breaking
change without disrupting active consumers.

## Real-time feature views

Note

Real-time feature views can’t currently be authored, planned, or applied through the
declarative `snow feature` workflow. For a real-time push path today, use a streaming
feature view, which is the supported low-latency option. If you already rely on real-time
feature views, continue to register them through the imperative
`snowflake.ml.feature_store` API.

## Feature groups

A feature group combines multiple online, Postgres-backed feature views into a single
online feature table. In the declarative workflow, a feature group is authored as a file
under `sources/feature_groups/` that references each member by `(name, version)`. Members
must be `online: true` and Postgres-backed, and the schema must have a running online
service.

The following example combines two online batch feature views into one feature group.

YAML (`sources/feature_groups/USER_FRAUD_FG_DECL.yaml`):

Copy code

```
kind: FeatureGroup
name: USER_FRAUD_FG_DECL
version: V1
desc: User-level fraud-signal feature group.
auto_prefix: true
feature_views:
  - name: USER_CLICKS_FG_DECL
    version: V1
  - name: USER_AMOUNTS_FG_DECL
    version: V1
```

Python (`sources/feature_groups/user_fraud_fg_decl.py`):

Copy code

```
from snowflake.ml.feature_store.decl import FeatureGroup
from user_clicks_fg_decl import user_clicks_fg_decl
from user_amounts_fg_decl import user_amounts_fg_decl

user_fraud_fg_decl = FeatureGroup(
    name="USER_FRAUD_FG_DECL",
    version="V1",
    desc="User-level fraud-signal feature group.",
    auto_prefix=True,
    feature_views=[user_clicks_fg_decl, user_amounts_fg_decl],
)
```

The Python form accepts either the source feature view objects directly (as shown) or
`FeatureViewRef(name=..., version=...)` pairs that mirror the YAML shape. With
`auto_prefix: true`, each member’s output columns are prefixed with
`<fv_name>_<fv_version>_` to avoid name collisions. Use the `desc` field (not
`description`) on a feature group, to match the imperative API.

Important

Feature groups have no in-place update. Any change to a feature group’s authored surface,
such as its description, `auto_prefix`, or member list, is a destructive recreate that
`apply` refuses without `--destructive`. A member feature view also can’t be dropped or
recreated while a feature group still references it.

For the concept, primary-key and join behavior, reading online, and training-set
generation, see [Feature groups](/developer-guide/snowflake-ml/feature-store/feature-groups).
