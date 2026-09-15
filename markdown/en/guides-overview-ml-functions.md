# ML Functions

These powerful analysis functions give you automated predictions and insights into your data using machine learning.
Snowflake provides an appropriate type of model for each feature, so you don’t have to be a machine learning expert
to take advantage of them. All you need is your data.

## Time-Series Functions

Use time-series functions to train a machine learning model on your time-series data to determine how a specified metric (for example,
sales) varies over time and relative to other features of your data. The model then provides insights or predictions
based on the trends detected in the data.

- [Forecasting](/user-guide/ml-functions/forecasting) predicts future metric values from past trends in time-series data.
- [Anomaly Detection](/user-guide/ml-functions/anomaly-detection) flags metric values that differ from typical expectations.

## Other Analysis Functions

These features don’t require time series data.

- [Classification](/user-guide/ml-functions/classification) sort rows into two or more classes based on
  their most predictive features.
- [Top Insights](/user-guide/ml-functions/top-insights) helps you find dimensions and values that affect the metric in
  surprising ways.

## Cost Considerations

When you use ML functions, you incur storage and compute costs. These costs vary depending on the feature used and the
quantity of data used in training and prediction.

The storage costs you incur reflect storage of the ML model instances created during the training step. To view the
objects associated with your model instance, navigate to your [Account Usage views](/sql-reference/account-usage#label-account-usage-views)
(ACCOUNT\_USAGE.TABLES and ACCOUNT\_USAGE.STAGES). These objects appear with null database and schema columns. The
`instance_id` column, however, will be populated, indicating that these objects are contained in a model instance.
These objects are fully managed by the model instance, and you cannot access or delete them separately. To reduce
storage costs associated with your models, delete unused or obsolete models.

See [Understanding compute cost](/user-guide/cost-understanding-compute) for general information on Snowflake compute costs.

## Limitations

Before you use ML functions, you must ensure [AUTOCOMMIT](/sql-reference/transactions#label-txn-autocommit) is enabled in your session. AUTOCOMMIT is
enabled by default when you start a new Snowflake session.

## Using ML functions in Snowpark

`session.call` is not yet compatible with models created by ML functions. To call such a model in Snowpark, use
`session.sql` instead, as shown here.

Copy code

```
session.sql('call my_model!FORECAST(...)').collect()
```
