# <model\_name>!SHOW\_TRAINING\_LOGS

Returns logs from model training. Output is non-NULL only when `'ON_ERROR' = 'SKIP'` is set in the training
`CONFIG_OBJECT`.

If you need to select specific columns from the data returned by this method, you can call the method in the FROM clause of a
SELECT statement. See [Selecting columns from SQL class instance methods that return tabular data](/sql-reference/snowflake-db-classes#label-class-select-from-methods).

## Syntax

Copy code

```
<model_name>!SHOW_TRAINING_LOGS();
```

## Returns

| Column | Type | Description |
| --- | --- | --- |
| SERIES | [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | Series value (NULL if model was trained with single time series). Note Your single-series results may not have a SERIES column. [See recent change](/release-notes/bcr-bundles/un-bundled/bcr-cortex-forecast-anomaly-detection-series-column). |
| LOGS | [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) | A log of errors encountered during training. The value for the key `Errors` is an array of training errors. If no errors were encountered, the LOGS column is NULL. |

Expand

Show lessSee more

## Examples

See [Detecting Anomalies](/user-guide/ml-functions/anomaly-detection#label-analysis-anomaly-detection-examples).
