# September 04, 2024 — Easier Training of Anomaly Detection Models from Real-World Data

We are pleased to announce that the Anomaly Detection ML Function now includes preprocessing features that allow
you to successfully train an anomaly detection model even when your training data has missing, duplicate, or misaligned time
steps. In the past, such issues, which are common in real-world data, typically prevented the model from being trained.
The new preprocessing features let you:

- Manually specify an event cadence in case the model fails to infer it or infers it incorrectly.
- Automatically interpolate missing target values from nearby time steps.
- Aggregate dimensional values from events occurring outside the canonical event cadence. You can specify aggregation
  behaviors for the type of value or per column, or use defaults.

A relatively small number of such corrections does not noticeably affect detection accuracy.

For more information, see [Dealing with real-world data in Time-Series Forecasting](/user-guide/ml-functions/preprocessing).
