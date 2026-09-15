# Feature groups

[Preview Feature — Open](/release-notes/preview-features)

Available to all accounts. Requires online serving with `store_type=OnlineStoreType.POSTGRES` on all source feature views.

A **feature group** bundles one or more feature views into a single, versioned set of features that a model can
consume for training and inference. This pattern is also known as a *feature service* in other feature store
platforms.

Models rarely consume features from a single feature view. A fraud model might need user profile features from a
batch view, recent transaction aggregations from a stream view, and a derived score from a real-time view. A feature
group collects those sources into one deployable unit so your application or training pipeline does not need to know
which feature views implement each column. Instead, the model calls one API: `read_feature_group` for online inference,
or `generate_training_set` with the `feature_group` parameter for offline training.

That abstraction gives you two practical benefits:

- **One contract per model**: Version the bundle (`name$version`) and point production and training at the same object.
- **Training-serving consistency**: Reproduce the exact feature set used in production when you build training data,
  reducing training-serving skew.

For operational visibility, the Online Serving tab in Snowsight lets you filter metrics by feature group. For REST
access, the Query API accepts `object_type=feature_group`. For more information, see
[Monitoring and Observability](/developer-guide/snowflake-ml/feature-store/monitoring) and
[Query API reference](/developer-guide/snowflake-ml/feature-store/online-feature-store-query-api-reference).

## Primary keys and join behavior

The output primary key is the union of join keys from all source feature views. When source feature views have
different join key granularities (for example, per-user features combined with per-user-per-session features), the
coarser source’s values are repeated across the finer-grained keys.

## Define and register a feature group

Source feature views must already be registered with online serving enabled and store type set as
`OnlineStoreType.POSTGRES`. If two source feature views share a join key column name, both must use the same
Snowpark data type for that column. These constraints are validated at registration time.

Copy code

```
from snowflake.ml.feature_store import FeatureGroup

user_fg = FeatureGroup(
    name="USER_FG",
    features=[
        reg_purchases,
        reg_profile.slice(["TIER"]).with_name("loyalty"),
    ],
    auto_prefix=False,
    desc="Combined per-user purchase and tier features",
)

registered_fg = fs.register_feature_group(user_fg, "v1")
```

The `features` list accepts full feature views, sliced feature views (`.slice([cols])`), or aliased slices
(`.slice([cols]).with_name(prefix)`). With `auto_prefix=True` (default), each source feature view’s columns are
prefixed with `<fv_name>_<fv_version>_` to avoid name collisions. Set `auto_prefix=False` and use `.with_name(prefix)`
per source for shorter, more readable column names. Each source feature view can appear only once (by name and
version) in a feature group. To include different subsets of columns from the same feature view, combine them into a
single `.slice()` call.

## Include real-time feature views in a feature group

A feature group can include real-time feature views alongside batch and stream feature views. When at least one
source has a `RequestSource`, you must pass a `request_context` DataFrame at read time.

Copy code

```
fg = FeatureGroup(
    name="USER_FG_RT",
    features=[bfv_live, rtfv_live],
    auto_prefix=False,
)

registered = fs.register_feature_group(fg, "v1")
```

If two or more real-time feature views in the same group use a request column with the same name (matched
case-insensitively), the columns must have the same Snowpark data type. The feature group’s `request_context` schema
is the union of all `RequestSource` schemas from its real-time sources.

## Read a feature group online

Once registered, retrieve features from the entire group in a single call using `read_feature_group`. The result is a
pandas DataFrame with primary-key columns first, followed by the features from each source view.

Copy code

```
pdf = fs.read_feature_group(
    fg_live,
    keys=[["user_1"], ["user_2"], ["user_3"]],
)
```

For a feature group that contains a real-time feature view with a `RequestSource`, supply `request_context`:

Copy code

```
import pandas as pd

pdf = fs.read_feature_group(
    fg_live,
    keys=[[user_id]],
    request_context=pd.DataFrame({"WEIGHT": [2.5]}),
)
```

`request_context` is required if and only if at least one source feature view is a real-time feature view that
declares a `RequestSource`. The same row-alignment rules apply as for
[Real-time feature views](/developer-guide/snowflake-ml/feature-store/online-feature-store#label-online-fs-realtime-feature-views).
Feature names that collide with primary-key columns are removed from the output.

## Generate training sets from feature groups

Pass a feature group to `generate_training_set` through the `feature_group` parameter to reproduce the exact same set
of features offline that your model consumes in production. For more information about training workflows, see
[Model training and inference](/developer-guide/snowflake-ml/feature-store/modeling).

If the feature group includes real-time feature views, the spine DataFrame must contain both the entity join key
columns and the columns declared in each real-time feature view’s `RequestSource`. The framework evaluates each
`compute_fn` against the offline source tables and joins the results onto the spine.

Copy code

```
training_df = fs.generate_training_set(
    spine_df=spine_df,
    feature_group=fg_live,
    spine_timestamp_col="QUERY_TS",
    spine_label_cols=["LABEL"],
)
```

## Manage feature groups

Use the `FeatureStore` methods to manage feature groups:

- `fs.list_feature_groups()`: List all registered feature groups.
- `fs.get_feature_group(name, version)`: Retrieve a registered feature group.
- `fs.delete_feature_group(name, version)`: Delete a feature group. You must delete the feature group before deleting
  any of its source feature views.
