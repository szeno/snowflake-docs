# Sep 15, 2026: Predict dynamic table refresh behavior with EXPLAIN CHANGES (*General availability*)

You can now use `EXPLAIN CHANGES` to predict a dynamic table’s refresh behavior before it happens,
either for a manual refresh or as part of a DDL change, without applying the change.

The prediction reports the effective action the refresh will take, including whether it will
reinitialize, along with the reasoning if available.

For more information, see [Predict refresh behavior](/user-guide/dynamic-tables/predict-refresh).
