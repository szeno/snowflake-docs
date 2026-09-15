# Dealing with real-world data in Time-Series Forecasting

Time-series data from the real world is often imperfect, with missing, duplicate, or unaligned time steps. The Forecast
and Anomaly Detection ML Functions include these preprocessing features to help you use your real-world data to train a
model that makes useful predictions:

- You can specify an event frequency to override the frequency that the model automatically infers.
- The model can infer data at missing time steps and aggregate multiple values within a time step. You can specify how
  aggregation should be done for each feature or type of feature, or let the ML function do it for you automatically.

These capabilities let you train a useful model even when your training data has common consistency issues. Generally,
the more consistent your data is, the more accurate your forecasting model will be, but a relatively small number of
such adjustments does not noticeably affect the accuracy of the model.

## Specifying event frequency

Model training infers the frequency of the time steps in your training data using heuristics that, on rare occasions,
choose the wrong frequency. To avoid this risk, or to correct an incorrect inference, you can optionally specify the
desired frequency when initiating training using the CONFIG\_OBJECT parameter `frequency`. This parameter
specifies a time period in a form similar to `'1 day'` or `'2 weeks'`.

- The interval specification is a string and therefore must be surrounded with single quotes.
- Supported intervals are seconds, minutes, hours, days, weeks, months, quarters, and years.
- Use the full interval names, not abbreviations. Plurals are acceptable. (“Second” or “seconds,” not “sec”).

The following example shows how to train a forecast model using a frequency of one day.

Copy code

```
CREATE SNOWFLAKE.ML.FORECAST model1(
  INPUT_DATA => TABLE(v1),
  TIMESTAMP_COLNAME => 'date',
  TARGET_COLNAME => 'sales',
  CONFIG_OBJECT => {'frequency': '1 day'}
);
```

If you do not specify an event frequency, the training process infers the closest matching event frequency.

## Filling in values for missing time steps

A time stamp that does not have a target value uses:

- Zero if the target value aggregation behavior is SUM (see [Handling multiple values in a time step](#label-time-series-preprocessing-aggregation))
- Linear interpolation from nearby values in all other cases

Missing feature values are not filled in, but rather replaced with NULL values. Model training ignores these.

## Handling multiple values in a time step

When there are multiple events in a time step, preprocessing can aggregate their values in various ways. For example,
if the frequency of events is hourly, then values that occur outside of the hourly cadence can be averaged to produce a
value for the nearest canonical hourly timestamp.

The following table summarizes the available aggregation behaviors.

| Kind of value | Available behaviors | Default behavior |
| --- | --- | --- |
| Numeric | - MEAN: average of values - MEDIAN: middle value - MODE: most frequent value - MIN: lowest value - MAX: highest value - SUM: total of values - FIRST: earliest value - LAST: latest value | MEAN |
| Categorical (string or Boolean) | - MODE: most frequent value - FIRST: earliest value - LAST: latest value | MODE |

Expand

Show lessSee more

Tip

Use the SUM method for count data, such as the number of items sold. MEAN is appropriate for most other numeric values.

All behaviors ignore NULL values and apply over the time period being interpolated or aggregated. For example, the SUM
of values on an hourly cadence is the sum of the values within the hour centered on the canonical time stamp.

You can override the default behavior for a column in two ways:

- By kind of value (target, numeric, or categorical)
- By the exact column name

If you override behaviors in both ways, the column name override takes precedence.

### Overriding by kind of value

Set the following options in the function’s CONFIG\_OBJECT parameter to override specific types of values: categorical,
numeric, and target. The behaviors are as [previously defined](#label-time-series-preprocessing-aggregation).

| Option | Possible values |
| --- | --- |
| `aggregation_categorical` | MODE, FIRST, LAST |
| `aggregation_numeric` | MEAN, MEDIAN, MODE, MIN, MAX, SUM, FIRST, LAST |
| `aggregation_target` | MEAN, MEDIAN, MODE, MIN, MAX, SUM, FIRST, LAST |

Expand

Show lessSee more

Note

If `aggregation_target` is not specified, target aggregation uses the behavior, if any, specified by `aggregate_numeric`.
Otherwise, the default, MEAN, is used.

The following example shows how to set aggregation behaviors for categorical and numeric features.

Copy code

```
CREATE SNOWFLAKE.ML.FORECAST model1(
  INPUT_DATA => TABLE(v1),
  TIMESTAMP_COLNAME => 'date',
  TARGET_COLNAME => 'sales',
  CONFIG_OBJECT => {
    'frequency': '1 day',
    'aggregation_categorical': 'MODE',
    'aggregation_numeric': 'MEDIAN'}
);
```

Tip

Consider specifying all of these values even if you’re using the defaults. That way, you don’t need to know what the
default behavior is to understand what the statement is doing, and if you want to change the behavior later, you
won’t need to look up the parameter name.

### Overriding by column name

The `aggregation_column` option in CONFIG\_OBJECT is an object that maps behaviors to column names. These behaviors
override any behaviors specified using the parameters described above.

Note

The aggregation behavior for the target value cannot be specified by column name. Use the `aggregation_target`
option instead.

For example, the following SQL statement specifies aggregation behaviors for two different columns using the
`aggregation_column` option.

Copy code

```
CREATE SNOWFLAKE.ML.FORECAST model1(
  INPUT_DATA => TABLE(v1),
  TIMESTAMP_COLNAME => 'date',
  TARGET_COLNAME => 'sales',
  CONFIG_OBJECT => {
    'frequency': '1 day',
    'aggregation_target': 'MEDIAN',
    'aggregation_column': {
        'temperature': 'MEDIAN',
        'employee_id': 'FIRST'
    }
  }
);
```
