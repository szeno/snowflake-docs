# <model\_name>!SHOW\_CONFUSION\_MATRIX

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Returns a table containing the number of instances of each combination of actual class and predicted class in models
where evaluation was enabled at instantiation. You can use this dataset to plot a confusion matrix. This method takes no
arguments. See [Confusion Matrix in `show\_confusion\_matrix`](/user-guide/ml-functions/classification#label-cortex-classification-show-confusion-matrix).

## Output

| Column | Type | Description |
| --- | --- | --- |
| `dataset_type` | [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | The name of the dataset used for metrics calculation, currently EVAL. |
| `actual_class` | [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | The actual class. |
| `predicted_class` | [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | The predicted class. |
| `count` | [INTEGER](/sql-reference/data-types-numeric#label-data-type-integer) | The number of instances of the given combination of actual and predicted class. |
| `logs` | [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | Contains error or warning messages. |

Expand

Show lessSee more
