# <model\_name>!EXPLAIN\_FEATURE\_IMPORTANCE

Returns the relative feature importance for each feature used by the model.

If you need to select specific columns from the data returned by this method, you can call the method in the FROM clause of a
SELECT statement. See [Selecting columns from SQL class instance methods that return tabular data](/sql-reference/snowflake-db-classes#label-class-select-from-methods).

## Syntax

Copy code

```
<model_name>!EXPLAIN_FEATURE_IMPORTANCE();
```

## Returns

| Column | Type | Description |
| --- | --- | --- |
| SERIES | [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | Series value (NULL if model was trained with single time series). |
| RANK | [INTEGER](/sql-reference/data-types-numeric#label-data-type-integer) | The importance rank of a feature for a specific series |
| FEATURE\_NAME | [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | The name of the feature used to train the model `aggregated_endogenous_features` represents all features derived as transformations of your target variable. |
| IMPORTANCE\_SCORE | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | The feature’s importance score: a value in [0, 1], with 0 being the lowest possible importance, and 1 the highest. |
| FEATURE\_TYPE | [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | The source of the feature, one of:   - `user_provided` - `derived_from_timestamp` - `derived_from_endogenous` |

Expand

Show lessSee more
