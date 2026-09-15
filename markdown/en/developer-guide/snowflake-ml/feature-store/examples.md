# Example feature patterns

This page lists common **transformation shapes** you can express in the SQL (or view) behind a
[Snowflake-managed feature view](/developer-guide/snowflake-ml/feature-store/feature-views#label-feature-store-feature-view-managed).
Use it as a reference when you already know the pattern you need and want a starting query.

Note

For **time-windowed aggregations** (for example, spend in the last 7 days), **online serving**,
**stream ingestion**, and other production-grade patterns, use the Feature Store aggregation API
and guidance in
[Advanced feature engineering](/developer-guide/snowflake-ml/feature-store/advanced-feature-engineering)
instead of hand-rolling window logic in SQL or Snowpark.

The open source [snowflake-ml-python](https://github.com/snowflakedb/snowflake-ml-python/tree/main/snowflake/ml/feature_store/examples)
repository also contains end-to-end feature view and entity examples on public datasets.

## Per-row features

Per-row features apply a function to each input row. The result has one output row per input row.

Copy code

```
SELECT
    entity_id,
    event_ts,
    COALESCE(foo, 0) AS foo,
    compute_zipcode(lat, long) AS zipcode
FROM source_events;
```

## Per-group features

Per-group features aggregate within a group key. The result has one row per group. For example,
sum daily rainfall by city:

Copy code

```
SELECT
    location,
    TO_DATE(timestamp) AS date,
    SUM(rain) AS sum_rain,
    AVG(humidity) AS avg_humidity
FROM source_events
GROUP BY location, date;
```

## Row-based window features

Row-based window features aggregate over a fixed number of preceding or following rows within a
partition. For example, sum the last three transaction amounts per account:

Copy code

```
SELECT
    entity_id,
    event_ts,
    SUM(amount) OVER (
        PARTITION BY entity_id
        ORDER BY event_ts
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS sum_past_3_transactions
FROM transactions;
```

Prefer the [time-windowed aggregation API](/developer-guide/snowflake-ml/feature-store/advanced-feature-engineering#label-online-fs-time-windowed-aggregation)
when your window is defined by **time** (for example, the last 7 days) rather than a row count,
especially if you need point-in-time correct training data or online serving.

## Time-based window features

Time-based window features aggregate over a trailing or sliding **time** range. Examples include
trip count over the past week or sales over the last three days.

For new feature views, define these with the aggregation API in
[Advanced feature engineering](/developer-guide/snowflake-ml/feature-store/advanced-feature-engineering#label-online-fs-time-windowed-aggregation).
The API handles tiling, incremental maintenance, and online sync more reliably than custom SQL
or client-side window helpers.

The following SQL illustrates the shape of a time-range window if you implement the logic directly
in a managed feature view query (for example, before migrating to the aggregation API):

Copy code

```
SELECT
    entity_id,
    event_ts,
    SUM(amount) OVER (
        PARTITION BY entity_id
        ORDER BY event_ts
        RANGE BETWEEN INTERVAL '7 days' PRECEDING AND CURRENT ROW
    ) AS sum_amount_7d
FROM transactions;
```

For general window function syntax, see [Window functions](/sql-reference/functions-window).

Legacy Snowpark analytics helpers

Older Feature Store workflows sometimes used Snowpark `DataFrame.analytics` helpers (such as
`moving_agg`, `cumulative_agg`, `compute_lag`, or `time_series_agg`) to build windowed features in
Python. Snowflake recommends SQL or the aggregation API for new development. Existing pipelines can
continue to use those helpers, but plan to migrate time-windowed features to
[Advanced feature engineering](/developer-guide/snowflake-ml/feature-store/advanced-feature-engineering).

## Lag and lead features

Lag and lead features compare each row to earlier or later rows in the same partition. They are
useful for trend and change-detection features:

Copy code

```
SELECT
    entity_id,
    event_ts,
    amount,
    LAG(amount, 1) OVER (PARTITION BY entity_id ORDER BY event_ts) AS amount_lag_1,
    LEAD(amount, 1) OVER (PARTITION BY entity_id ORDER BY event_ts) AS amount_lead_1
FROM transactions;
```

## User-defined functions in feature pipelines

Feature views can call user-defined functions (UDFs) in transformation SQL. Only **deterministic**
functions (functions that always return the same result for the same input) can be incrementally
maintained in a Snowflake-managed feature view.

Mark SQL UDFs as immutable when you create them. See [CREATE FUNCTION](/sql-reference/sql/create-function).

Copy code

```
CREATE OR REPLACE FUNCTION my_normalize (input NUMBER)
  RETURNS NUMBER
  IMMUTABLE
  AS
  $$
    -- normalization logic
  $$;
```

If you register a Python UDF through Snowpark, set `immutable=True` when you define it so dynamic
table incremental refresh can use it.
