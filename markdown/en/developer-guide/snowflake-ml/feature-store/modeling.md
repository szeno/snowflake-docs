# Model Training and Inference

## Generating tables for training

You can generate a training data set with the feature store’s `generate_training_set` method, which enriches a
Snowpark DataFrame that contains the source data with the derived feature values.

### Generate training data from feature views

To select features from individual feature views, pass a list to the `features` parameter. To select a subset of
features from a feature view, use `fv.slice`.

For time-series features, provide the timestamp column name to automate the point-in-time feature value lookup.

Copy code

```
training_set = fs.generate_training_set(
    spine_df=MySourceDataFrame,
    features=[registered_fv],
    save_as="data_20240101",                    # optional
    spine_timestamp_col="TS",                   # optional
    spine_label_cols=["LABEL1", "LABEL2"],      # optional
    include_feature_view_timestamp_col=False,   # optional
)
```

### Generate training data from a feature group

When your model consumes a bundled set of features in production, pass a
[feature group](/developer-guide/snowflake-ml/feature-store/feature-groups) to `generate_training_set` through the
`feature_group` parameter instead of the `features` list. This reproduces the same columns offline that
`read_feature_group` returns online, reducing training-serving skew. All source feature views in the group must
have online serving enabled with `store_type=OnlineStoreType.POSTGRES`.

Copy code

```
fg = fs.get_feature_group("USER_FG", "v1")

training_set = fs.generate_training_set(
    spine_df=MySourceDataFrame,
    feature_group=fg,
    spine_timestamp_col="TS",                   # optional
    spine_label_cols=["LABEL1", "LABEL2"],      # optional
)
```

For real-time feature views in the group, the spine DataFrame must also include columns declared in each member’s
`RequestSource`. For more information, see
[Generate training sets from feature groups](/developer-guide/snowflake-ml/feature-store/feature-groups#label-fs-feature-groups-training).

Note

Here, the `spine_df` (`MySourceDataFrame`) is a DataFrame containing the entity IDs in source data, the time
stamp, label columns, and additional columns containing training data. Requested features are retrieved for the list
of entity IDs, with point-in-time correctness with respect to the provided time stamp.

Training sets are ephemeral by default; they exist only as Snowpark DataFrames and are not materialized. To materialize
the training set to a Table, specify the argument `save_as` with a valid, non-existing table name. The training set
is written to the newly created table.

Materialized tables currently don’t guarantee immutability and have limited metadata support. If you require these
features, consider using [Snowflake Datasets](#label-feature-store-generate-datasets) instead.

Note

The `generate_training_set` API is available in `snowflake-ml-python` version `1.5.4` or later.

## Generating Snowflake Datasets for training

You can generate a [Snowflake Dataset](/developer-guide/snowflake-ml/dataset) using the feature store’s
`generate_dataset` method. The method signature is similar to `generate_training_set`; the key
differences are the required `name` argument, optional `version` argument, and additional metadata fields.
`generate_dataset` always materializes the result.

Snowflake Datasets provide an immutable, file-based snapshot of data, which helps to ensure model reproducibility
and efficient data ingestion for large datasets and/or distributed training. Datasets also have expanded metadata
support for easier discoverability and consumption.

The following code illustrates the generation of a dataset from a feature view:

Copy code

```
dataset: Dataset = fs.generate_dataset(
    name="MY_DATASET",
    spine_df=MySourceDataFrame,
    features=[registered_fv],
    version="v1",                               # optional
    spine_timestamp_col="TS",                   # optional
    spine_label_cols=["LABEL1", "LABEL2"],      # optional
    include_feature_view_timestamp_col=False,   # optional
    desc="my new dataset",                      # optional
)
```

## Model training

After creating a training data set, you can pass it to your model when training as follows.

If you generated a Snowpark DataFrame, pass it directly to your model:

Copy code

```
my_model = train_my_model(training_set)
```

If you generated a Snowflake Dataset, convert it to a Snowpark DataFrame and pass it to your model:

Copy code

```
my_model = train_my_model(dataset.read.to_snowpark_dataframe())
```

Once trained, the model can be logged in the [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview).

## Retrieving features and making predictions

If you created a model in your Python session, you can retrieve the feature view from the feature store and pass
it to your model for prediction, as shown here:

Copy code

```
prediction_df: snowpark.DataFrame = fs.retrieve_feature_values(
    spine_df=prediction_source_dataframe,
    features=[registered_fv],
    spine_timestamp_col="TS",
    exclude_columns=[],
)

# predict with your previously trained model
my_model.predict(prediction_df)
```

You can exclude specified columns using the `exclude_columns` argument, or include the timestamp column from the
feature view by setting `include_feature_view_timestamp_col`.
