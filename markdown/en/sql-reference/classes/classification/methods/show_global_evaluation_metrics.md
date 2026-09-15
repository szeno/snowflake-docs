# <model\_name>!SHOW\_GLOBAL\_EVALUATION\_METRICS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Returns overall evaluation metrics for models where evaluation was enabled at instantiation. This method
takes no arguments. See [Metrics in `show\_global\_evaluation\_metrics`](/user-guide/ml-functions/classification#label-cortex-classification-show-global-evaluation-metrics).

## Output

| Column | Type | Description |
| --- | --- | --- |
| `dataset_type` | [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | The name of the dataset used for metrics calculation, currently EVAL. |
| `average_type` | [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | The method of aggregation used to calculate overall metrics from the individual class metrics, currently MACRO. |
| `error_metric` | [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | The error metric name. Can include Precision, Recall, F1, etc. |
| `metric_value` | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | The error metric value |
| `logs` | [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | Contains error or warning messages. |

Expand

Show lessSee more
