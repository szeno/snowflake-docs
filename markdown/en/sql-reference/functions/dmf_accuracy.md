Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# ACCURACY (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of rows in which a predicted value is equal to the actual value. Use this function to measure the output of
a classification model, such as a model that predicts a category, a label, or a yes-or-no outcome.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.ACCURACY(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects two columns. The first column contains the predicted values, and the second column contains
    the actual values.

## Allowed data types

The two columns projected by the `query` must have the same data type, which must be one of
the following:

- `BOOLEAN`
- `NUMBER`
- `VARCHAR`

## Returns

The function returns a `FLOAT` value from 0 to 100. A value of 100 means that every prediction is equal to the actual value.
The function returns `NULL` if no row has both a predicted and an actual value.

## Usage notes

- The function compares the two values with the `=` operator. Rows in which either value is `NULL` are ignored.
- When you associate the function with a table or view, specify the predicted column first:
  `ON (predicted_column, actual_column)`.
- You can’t mix data types. For example, you can’t use the function on a `VARCHAR` column of predictions and a `NUMBER` column
  of actual values.
- The function doesn’t support `FLOAT` columns. To measure predictions of continuous values, use a regression metric such as
  [MAE](/sql-reference/functions/dmf_mae) or [RMSE](/sql-reference/functions/dmf_rmse).

## Examples

The examples use the following table of predicted and actual labels. The prediction in the last row is missing, so the function
ignores that row:

Copy code

```
CREATE TABLE ml.predictions.animal_labels (
  predicted_label VARCHAR,
  actual_label VARCHAR);

INSERT INTO ml.predictions.animal_labels VALUES
  ('cat', 'cat'),
  ('dog', 'cat'),
  ('cat', 'cat'),
  ('bird', 'bird'),
  (NULL, 'dog');
```

Measure the percentage of correct predictions. Three of the four predictions match:

Copy code

```
SELECT SNOWFLAKE.CORE.ACCURACY(
  SELECT
    predicted_label,
    actual_label
  FROM ml.predictions.animal_labels
) AS accuracy;
```

```
+----------+
| ACCURACY |
+----------+
| 75       |
+----------+
```

Associate the function with the table, and define an expectation that is violated when fewer than 90 percent of the predictions
are correct:

Copy code

```
ALTER TABLE ml.predictions.animal_labels
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.ACCURACY
    ON (predicted_label, actual_label)
    EXPECTATION accuracy_at_least_90 (VALUE >= 90);
```
