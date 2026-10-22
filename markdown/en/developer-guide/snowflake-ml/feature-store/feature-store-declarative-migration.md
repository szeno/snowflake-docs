# Migrating to declarative

You might have registered feature store objects through the imperative
`snowflake.ml.feature_store` API: from a notebook, an ad-hoc script, or an existing
pipeline. You don’t have to re-author them by hand to adopt the declarative `snow feature`
workflow. `snow feature sync` reads the deployed runtime and writes spec files back into
your project, so the migration is mostly a pull-and-verify loop.

## Why declarative

The imperative API registers objects immediately against a live Snowflake session. There’s
no preview, no diff, and no artifact you can review or check into source control. The
declarative workflow adds:

- **`plan` and `apply`**: a preview of every create, update, recreate, and drop before it
  runs, with destructive operations gated behind `--destructive`.
- **Reviewable diffs**: a feature store that’s a directory of YAML or Python spec files you
  can diff, review, and roll back like any other code.
- **CI-friendly deployment**: a single `sources/` tree that deploys to dev and prod through
  manifest targets, with no notebook required.

## The migration path: Initialize once, then sync

This path assumes your objects already live in Snowflake, registered earlier through
`FeatureStore.register_entity`, `register_feature_view`, or `register_feature_group`.

1. **Run `snow feature init` once** if you don’t have a project yet. This writes
   `manifest.yml`, scaffolds `sources/`, ensures the schema and metadata exist, and exports
   every deployed object. Objects are written as Python spec files by default. Pass `--yaml`
   to author in YAML instead.
2. **Run `snow feature sync`** to refresh `sources/` from the runtime whenever the deployed
   state changes, for example after a colleague applies, or after you register more objects
   imperatively. `sync` runs the same export pass as `init` without re-bootstrapping the
   schema. Use `sync --name <OBJECT>` to pull just the objects with that name, or
   `sync --yaml` to emit YAML.
3. **Run `snow feature plan`** to confirm the round-trip. A faithfully captured object
   re-plans with no actionable operations (`NO_CHANGE`). From here on, you edit the spec
   files declaratively and drive changes through `plan` and `apply`.

## Field mapping

The declarative spec fields line up closely with the imperative constructors, with a few
deliberate name differences. The following tables map each imperative construct to its
declarative equivalent, grouped by object. For each object’s full authoring details, see
[Declarative authoring](/developer-guide/snowflake-ml/feature-store/feature-store-declarative-authoring).

Across all objects, column types are Snowpark classes in the imperative API
(`StructField("USER_ID", StringType())`) but strings in the declarative forms
(`type: StringType`).

### Entities and sources

| Imperative (`snowflake-ml-python`) | Declarative (YAML or Python) | Notes |
| --- | --- | --- |
| `Entity(join_keys=["USER_ID"], desc=...)` | `kind: Entity`, `join_keys: [{name, type}]`, `description` | Uses `description`, not the imperative `desc`. |
| `StreamSource(schema=StructType([...]))` | `kind: StreamingSource`, `columns: [{name, type}]` | The imperative class is `StreamSource`; the declarative kind is `StreamingSource`. |
| Snowpark DataFrame passed as `feature_df=` | `kind: BatchSource`, `columns`, plus one of `table`, `query`, or `query_file` | Set exactly one of `table`, `query`, or `query_file`. |

Expand

Show lessSee more

### Feature views

| Imperative (`snowflake-ml-python`) | Declarative (YAML or Python) | Notes |
| --- | --- | --- |
| `FeatureView(refresh_freq=...)` | `refresh_freq` | Same name in both APIs. The former declarative name `batch_schedule` was removed and has no alias: the loader errors if it appears. |
| `OnlineConfig(enable=True, target_lag=...)` | `online: true`, `target_lag` | `target_lag` is rejected when `online: false`. |
| `feature_df=<DataFrame>` | `sources: [{name, source_type: Batch}]` |  |
| `stream_config=StreamConfig(stream_source=..., transformation_fn=...)` | `sources: [{name, source_type: Stream}]`, `udf` |  |
| `features=[Feature.sum("col", "1h").alias("OUT")]` | `features: [{source_column, output_column, function, window}]` | Batch feature views use `window`; streaming feature views use `window_sec`. |
| `FeatureView(append_only=True)` | `append_only: true` |  |

Expand

Show lessSee more

### Feature groups

| Imperative (`snowflake-ml-python`) | Declarative (YAML or Python) | Notes |
| --- | --- | --- |
| `FeatureGroup(features=[fv1, fv2])` | `feature_views: [{name, version}]` | Uses `desc`, not `description`, to match the imperative API. |
| `register_feature_group(fg, version="V1")` | `version` on the feature group spec |  |

Expand

Show lessSee more

## Not yet supported

Some imperative capabilities don’t yet have a declarative equivalent:

- **`backup_source`**, which seeds an append-only snapshot table from a historical table at
  registration, is available on the imperative `FeatureView` but isn’t yet supported in the
  declarative form.
- **Real-time feature views** can’t be authored declaratively yet. Continue to register
  them through the imperative API, or use the supported real-time push path with
  [streaming feature views](/developer-guide/snowflake-ml/feature-store/feature-store-declarative-authoring#label-feature-authoring-streaming-fv).
