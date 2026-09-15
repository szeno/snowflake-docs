# <model\_name>!SHOW\_THRESHOLD\_METRICS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Returns raw counts and metrics for a specific threshold for each class in models where evaluation was enabled at instantiation.
This method takes no arguments. See [Metrics in `show\_threshold\_metrics`](/user-guide/ml-functions/classification#label-cortex-classification-show-threshold-metrics).

## Output

| Column | Type | Description |
| --- | --- | --- |
| `dataset_type` | [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | The name of the dataset used for metrics calculation, currently EVAL. |
| `class` | [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | The predicted class. Each class has its own set of metrics, which are provided in multiple rows. |
| `threshold` | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | Threshold used to generate predictions. |
| `precision` | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | Precision for the given class. The ratio of true positives to the total predicted positives. |
| `recall` | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | Recall for the given class. Also called “sensitivity.” The ratio of true positives to the total actual positives. |
| `f1` | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | F1 score for the given class. |
| `tpr` | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | True positive rate for the given class. |
| `fpr` | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | False positive rate for the given class. |
| `tp` | [INTEGER](/sql-reference/data-types-numeric#label-data-type-integer) | Total count of true positives in the given class. |
| `fp` | [INTEGER](/sql-reference/data-types-numeric#label-data-type-integer) | Total count of false positives in the given class. |
| `tn` | [INTEGER](/sql-reference/data-types-numeric#label-data-type-integer) | Total count of true negatives in the given class. |
| `fn` | [INTEGER](/sql-reference/data-types-numeric#label-data-type-integer) | Total count of false negatives in the given class. |
| `accuracy` | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | The accuracy (ratio of correct predictions, both positive and negative, to the total number of predictions) for the given class. |
| `support` | [INTEGER](/sql-reference/data-types-numeric#label-data-type-integer) | The support (true positives plus false negatives) for the given class. |
| `logs` | [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | Contains error or warning messages. |

Expand

Show lessSee more
