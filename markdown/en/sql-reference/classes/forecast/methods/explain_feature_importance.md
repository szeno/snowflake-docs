# <model\_name>!EXPLAIN\_FEATURE\_IMPORTANCE

Returns the relative feature importance for each feature used by the model.

If you need to select specific columns from the data returned by this method, you can call the method in the FROM clause of a
SELECT statement. See [Selecting columns from SQL class instance methods that return tabular data](/sql-reference/snowflake-db-classes#label-class-select-from-methods).

## Syntax

Copy code

```
<model_name>!EXPLAIN_FEATURE_IMPORTANCE();
```

## Output

| Column | Type | Description |
| --- | --- | --- |
| SERIES | [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | Series value (NULL if model was trained with single time series). |
| RANK | [INTEGER](/sql-reference/data-types-numeric#label-data-type-integer) | The importance rank of a feature for a particular series. |
| FEATURE\_NAME | [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | The name of the feature used to train the model. `aggregated_endogenous_features` represents all features derived as transformations of the target variable. |
| IMPORTANCE\_SCORE | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | The feature’s importance score: a value in [0, 1], with 0 being the lowest possible importance, and 1 the highest. |
| FEATURE\_TYPE | [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | The source of the feature. One of:   - `user_provided`: Feature data provided by the user. - `derived_from_timestamp`: Periodic feature (e.g. day, week, or month) derived from timestamp data. - `derived_from_endogenous`: Features derived from a transformation of the target variable. |

Expand

Show lessSee more

## Examples

See [Examples](/user-guide/ml-functions/forecasting#label-analysis-forecasting-examples).
