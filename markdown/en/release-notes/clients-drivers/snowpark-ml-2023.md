# Snowflake ML release notes

This article contains the release notes for the Snowflake ML, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Note

These notes do not include changes in features that have not been publicly released.

See [Snowflake ML: End-to-End Agentic Machine Learning](/developer-guide/snowflake-ml/overview) for documentation.

## Version 1.1.2 (2023-12-18)

### New features and updates

Model development updates:

- Implemented `precision_score` metric in SQL.

### Bug fixes

- Fixed an issue where stack trace was being hidden by telemetry.

Model development fixes:

- Inferring model signatures no longer materializes the full dataframe in memory.

## Version 1.1.1 (2023-12-6)

### New features and updates

- Designated Snowpark ML Modeling API as Generally Available.
- New `passthrough_col` parameter in the Modeling API allows you to exclude specific columns, like index columns, during
  training or inference when not explicitly specifying `input_cols`.

### Bug fixes

- Model development fixes:
  - `confusion_matrix` provided incorrect results when the row number could not be divided by the batch size.

## Version 1.1.0 (2023-12-1)

### New features and updates

- `GridSearchCV` and `RandomizedSearchCV` execution is now distributed on multi-node warehouses.

### Bug fixes

- Model development fixes:
  - Columns were being excluded if their normalized names did not match the names specified in `output_columns`
    in `OrdinalEncoder` and `LabelEncoder`. Output columns no longer need to be valid Snowflake identifiers.

## Version 1.0.12 (2023-11-15)

### New features and updates

- None

### Bug fixes

- Model development fixes:
  - Increased the column capacity of `OrdinalEncoder`.

## Version 1.0.11 (2023-10-28)

### New features and updates

- Add support for `kneighbors`.
- Support `DecimalType` as a data type.

### Bug fixes

- Model development fixes:
  - Fix support for XGBoost and LightGBM models using SKLearn Grid Search and Randomized Search model selectors.
  - Fix metrics compatibility with Snowpark DataFrames that use Snowflake identifiers

## Version 1.0.10 (2023-10-15)

### New features and updates

- `precision_score`, `recall_score`, `f1_score`, `fbeta_score`, `precision_recall_fscore_support`,
  `mean_absolute_error`, `mean_squared_error`, and `mean_absolute_percentage_error` metric calculations are now
  distributed.

### Bug fixes

- Model development fixes:
  - Fix UTF-8 decoding errors when using modeling modules on Windows.
  - Fix alias definitions causing `SnowparkSQLUnexpectedAliasException` in inference.

## Version 1.0.9 (2023-09-28)

### New features and updates

- Calculation of `log_loss` metric is now distributed.

### Bug fixes

- Model development fixes:
  - Building images no longer fails with some Docker setups.
  - Embedding local ML library no longer fails when the library is imported by zipimport.
  - Update incorrect documentation about platform argument in the `deploy` function.

## Version 1.0.8 (2023-09-15)

### New features and updates

- None

### Bug fixes

- Model development fixes:
  - Ordinal encoder can be used with mixed input column types.
  - Fix an issue when the sklearn default value is `np.nan`.

## Version 1.0.7 (2023-09-05)

### New features and updates

> - Allow disabling telemetry.

### Bug fixes

- Model development fixes:
  - Fix an error related to `pandas.io.json.json_normalizer`.

## Version 1.0.6 (2023-09-01)

### New features and updates

- Model development: Size of metrics result can exceed previous 8MB limit.

### Bug fixes

- Model development fixes:
  - Fixed a bug when using simple imputer with NumPy >= 1.25.
  - Fixed a bug when inferring the type of label columns.

## Version 1.0.5 (2023-08-17)

This release contains internal changes only.

## Version 1.0.4 (2023-07-28)

### New features and updates

- Model development: Input dataframes can now be joined against data loaded from staged files.
- Model development: Added support for non-English languages.

### Bug fixes

- None

## Version 1.0.3 (2023-07-14)

This release contains internal changes only.

## Version 1.0.2 (2023-06-22)

### New features and updates

- Model development: Added metrics:
  - d2\_absolute\_error\_score
  - d2\_pinball\_score
  - explained\_variance\_score
  - mean\_absolute\_error
  - mean\_absolute\_percentage\_error
  - mean\_squared\_error

### Bug fixes

Model development: `accuracy_score` now works when given label column names that are lists of single values.

## Version 1.0.1 (2023-06-16)

### Behavior changes

- Model development: Changed Metrics APIs to follow scikit-learn metrics modules:
  - `accuracy_score`, `confusion_matrix`, `precision_recall_fscore_support`, and `precision_score` methods move to `metrics.classification`.

### New features and updates

- Model development: Added metrics:
  - `f1_score`
  - `fbeta_score`
  - `recall_score`
  - `roc_auc_score`
  - `roc_curve`
  - `log_loss`
  - `precision_recall_curve`

## Version 1.0.0 (2023-06-09)

Initial public preview release.
