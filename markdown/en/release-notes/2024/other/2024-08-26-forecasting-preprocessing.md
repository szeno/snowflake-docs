# August 26, 2024 — Easier Training of Forecasting Models from Real-World Data

We are pleased to announce that the Time-Series Forecasting ML Function now includes preprocessing features that allow
you to successfully train a forecasting model even when your training data has missing, duplicate, or misaligned time
steps. In the past, such issues, which are common in real-world data, typically prevented the model from being trained.
These features are:

- You can manually specify an event cadence in case the model fails to infer it or infers it incorrectly
- The model can interpolate missing target values from nearby time steps.
- The model can aggregate dimensional values from events occurring outside the canonical event cadence in a number of
  ways, and you can specify aggregation behaviors for the type of value or per column.

A relatively small number of such corrections does not noticeably affect prediction accuracy.

For more information, see [Dealing with real-world data in Time-Series Forecasting](/user-guide/ml-functions/preprocessing).
