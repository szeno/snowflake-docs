# <model\_name>!SHOW\_TRAINING\_LOGS

Returns logs from model training. Output is non-NULL only when `'ON_ERROR' = 'SKIP'` is set in the training
`CONFIG_OBJECT`; otherwise the entire model fails to train.

If you need to select specific columns from the data returned by this method, you can call the method in the FROM clause of a
SELECT statement. See [Selecting columns from SQL class instance methods that return tabular data](/sql-reference/snowflake-db-classes#label-class-select-from-methods).

## Syntax

Copy code

```
<model_name>!SHOW_TRAINING_LOGS();
```

## Output

| Column | Type | Description |
| --- | --- | --- |
| SERIES | [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | Series value (NULL if model was trained with single time series). |
| LOGS | [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) | Object containing errors encountered during training. Currently the only key is `Errors`, an array of errors. If no errors were encountered, the logs object is NULL. |

Expand

Show lessSee more

## Examples

See [Examples](/user-guide/ml-functions/forecasting#label-analysis-forecasting-examples).
