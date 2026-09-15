# <instance\_name>!GET\_DRIVERS

Finds the most important dimensions in a dataset, builds segments from those dimensions, and then determines which of
those segments most influenced the metric.

GET\_DRIVERS is well-suited to extracting root causes from datasets that have a large number of dimensions. Continuous
dimensions are also supported without pre-processing them into categorical dimensions, and the results can indicate
dimensions with negative conditions (for example, “region is not North America”).

If you need to select specific columns from the data returned by this method, use
[RESULT\_SCAN](/sql-reference/functions/result_scan).

## Syntax

Copy code

```
<model_name>!GET_DRIVERS(
  INPUT_DATA => <input_data>,
  LABEL_COLNAME => '<label_colname>',
  METRIC_COLNAME => '<metric_colname>'
);
```

INPUT\_DATA
:   A [reference](/sql-reference/references) to a table, view, or query. All columns other than the ones specified
    by LABEL\_COLNAME and METRIC\_COLNAME are taken as dimensions to be considered by Top Insights. Numeric columns are
    taken to be continuous dimensions, while string and Boolean columns are considered categorical dimensions. To treat a
    numeric column as a categorical dimension, cast it to a string.

LABEL\_COLNAME
:   The name of a Boolean column in INPUT\_DATA designated as the label that indicates control data (FALSE) vs test data
    (TRUE).

METRIC\_COLNAME
:   The name of a [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) column in INPUT\_DATA representing the value of interest that has
    been influenced by the included dimensions.

## Output

| Column | Type | Description |
| --- | --- | --- |
| CONTRIBUTOR | [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) | ARRAY of strings describing a segment or insight from the algorithm. |
| METRIC\_CONTROL | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | The total value of the metric in the control period in a specific segment. |
| METRIC\_TEST | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | The total value of the metric in the test period in a specific segment. |
| CONTRIBUTION | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | The absolute impact of the segment on the change in the metric. |
| RELATIVE\_CONTRIBUTION | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | The impact of the segment as a proportion of the overall change in the metric between test and control. |
| GROWTH\_RATE | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | The change in the metric in the segment as a proportion of the metric in the control group in the segment. |

Expand

Show lessSee more

## Usage Notes

- Execution time scales with the number of dimensions and the cardinality of those dimensions.
- The input metric must be an individual observation or an aggregate.
- For categorical dimensions having more than 25 values, Top Insights uses only the top 25 most influential values to create segments.

## Examples

See [Examples](/user-guide/ml-functions/top-insights#label-top-insights-examples).
