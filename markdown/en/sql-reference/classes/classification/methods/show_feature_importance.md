# <model\_name>!SHOW\_FEATURE\_IMPORTANCE

Returns the relative feature importance for each feature used by the model. This method takes no arguments.

## Syntax

Copy code

```
<model_name>!SHOW_FEATURE_IMPORTANCE();
```

## Output

| Column | Type | Description |
| --- | --- | --- |
| `rank` | [INTEGER](/sql-reference/data-types-numeric#label-data-type-integer) | The importance rank of a feature. |
| `feature` | [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | The name of the feature used to train the model. |
| `score` | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | The feature’s importance score: a value in [0, 1], with 0 being the lowest possible importance, and 1 the highest. |
| `feature_type` | [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | The source of the feature. Currently this is always `user_provided`, which denotes feature data provided by the user. |

Expand

Show lessSee more
