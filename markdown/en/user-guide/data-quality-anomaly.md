# Detecting anomalies in data quality

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts that are Enterprise Edition (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returning a value from a data metric function (DMF) provides useful information, but it might be hard to know whether it indicates a data
quality issue. You can define an [expectation](/user-guide/data-quality-expectations) if you know what is an acceptable value, but it might be
difficult to define enough manual rules to identify all possible data quality issues.

As a solution, Snowflake provides an algorithm that can detect anomalies in the values returned by a DMF. Snowflake trains this algorithm
with historical data, then automatically identifies return values that are above or below a predicted range.

You can enable anomaly detection for the following system DMFs:

- [ROW\_COUNT](/sql-reference/functions/dmf_row_count): Use to identify anomalies in the volume of data in a table.
- [FRESHNESS](/sql-reference/functions/dmf_freshness): Use to identify anomalies in the frequency with which a table is being
  updated.

The following example shows how to enable anomaly detection for the association between the ROW\_COUNT DMF and table `t1`:

Copy code

```
ALTER TABLE t1
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.ROW_COUNT ON ()
    ANOMALY_DETECTION = TRUE;
```

Snowflake trains the algorithm and then automatically starts identifying anomalies in the volume of table `t1`.

## About the training period

When you enable anomaly detection, Snowflake trains the anomaly-detecting algorithm on historical data. The length of the training period
depends on how frequently the DMF runs.

- **For DMFs that run frequently**, Snowflake requires at least two weeks of DMF data to start detecting anomalies. This two-week period is
  essential for establishing weekly seasonality. If the DMF has been running for longer, Snowflake trains the algorithm on up to 60 days of
  data. This longer training period establishes monthly seasonality and increases accuracy. Snowflake recommends that you let the algorithm
  be trained on 60 days of data to detect anomalies with a high degree of confidence.
- **For DMFs that run infrequently or on a trigger-based schedule**, Snowflake must have at least two data points to train the algorithm.
  For example, if a DMF runs every month, then Snowflake looks back two months to train the algorithm.

You can identify whether Snowflake is still in the training period by running the
[DATA\_METRIC\_FUNCTION\_REFERENCES](/sql-reference/functions/data_metric_function_references) function. If anomaly detection was enabled but the algorithm is still
being trained, the `anomaly_detection_status` column of the output contains the value `TRAINING_IN_PROGRESS`.

## Enable anomaly detection

You can enable anomaly detection for a DMF association when you first associate the DMF with an object, or you can enable it later.

Example: Enable anomaly detection when associating DMF
:   To enable anomaly detection when associating the FRESHNESS DMF with view `v1`, run the following command:

    Copy code

    ```
    ALTER VIEW v1
      ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.FRESHNESS ON (c_timestamp)
        ANOMALY_DETECTION = TRUE;
    ```

Example: Enable anomaly detection for an existing association
:   To enable anomaly detection for an existing association between the ROW\_COUNT DMF and table `t1`, run the following command:

    Copy code

    ```
    ALTER TABLE t1
      MODIFY DATA METRIC FUNCTION SNOWFLAKE.CORE.ROW_COUNT ON ()
        SET ANOMALY_DETECTION = TRUE;
    ```

## Adjust the sensitivity level of anomaly detection

After you enable anomaly detection, you can [track how many anomalies](#label-data-quality-anomalies-identify) are occurring in your
account. If the number of anomalies seems too low or too high, you can adjust the sensitivity level of the anomaly detection
algorithm.

- If there are too many false positives (that is, values mistakenly identified as anomalies), you can change the sensitivity to LOW to find
  fewer anomalies.
- If there are too many false negatives (that is, values that weren’t identified as anomalies, but really are), you can change the
  sensitivity to HIGH to find more anomalies.

The default sensitivity level is MEDIUM.

For example, to increase the sensitivity for a DMF association that finds anomalies in the volume of table `t1`, run the following
command:

Copy code

```
ALTER TABLE t1
  MODIFY DATA METRIC FUNCTION SNOWFLAKE.CORE.ROW_COUNT ON ()
    SET SENSITIVITY = 'HIGH';
```

## Disable anomaly detection

You can disable anomaly detection for a DMF association at any time by using an ALTER statement to modify the object.

For example, to disable anomaly detection for the association between the ROW\_COUNT DMF and table `t1`, run the following command:

Copy code

```
ALTER TABLE t1
  MODIFY DATA METRIC FUNCTION SNOWFLAKE.CORE.ROW_COUNT ON ()
    SET ANOMALY_DETECTION = FALSE;
```

## Identify anomalies

You can identify anomalies using the following:

- [SNOWFLAKE.LOCAL.DATA\_QUALITY\_MONITORING\_RESULTS\_RAW](#label-dmf-anomaly-monitor-event-table): A dedicated event table that records raw data quality results.
- [DATA\_QUALITY\_MONITORING\_ANOMALY\_DETECTION\_STATUS view](#label-dmf-anomaly-monitor-local-view): View in the SNOWFLAKE.LOCAL schema that contains flattened results.

### SNOWFLAKE.LOCAL.DATA\_QUALITY\_MONITORING\_RESULTS\_RAW

Data quality results are recorded in the dedicated event table SNOWFLAKE.LOCAL.DATA\_QUALITY\_MONITORING\_RESULTS\_RAW.

If anomaly detection is enabled for a DMF association, two rows are added to the table every time Snowflake computes the result
of the DMF. The first row records information about the object the DMF is associated with, the DMF itself, and the result of the data
quality check. The second row records information related to anomaly detection.

The `snow.data_metric.record_type` field in the `record_attribute` column indicates whether a row corresponds to anomaly
detection. This field has two possible values:

- `ANOMALY_DETECTION_STATUS` — Indicates that the row corresponds to anomaly detection.
- `EVALUATION_RESULT` — Indicates that the row corresponds to the evaluation of the DMF.

#### Identifying whether there was an anomaly

After you have determined that a row in the event table corresponds to anomaly detection, you can check the
`snow.data_metric.evaluation_result` field in the `resource_attribute` column to determine if there was an anomaly.

This field contains a VARIANT that contains the value returned by the DMF and a BOOLEAN value indicating whether that value was an anomaly.
For example, if the value of the `snow.data_metric.evaluation_result` field is `5, TRUE`, then the returned value was `5` and
Snowflake identified it as an anomaly.

#### Additional fields

If the row in the event table corresponds to anomaly detection, the `resource_attribute` column also contains the following fields:

- `snow.data_metric.upper_bound`: Highest value that should be returned by the DMF based on the anomaly-detecting algorithm. If the
  value returned by the DMF is above this upper bound, it is an anomaly.
- `snow.data_metric.lower_bound`: Lowest value that should be returned by the DMF based on the anomaly-detecting algorithm. If the
  value returned by the DMF is below this lower bound, it is an anomaly.
- `snow.data_metric.forecast`: Value that the anomaly-detecting algorithm predicted would be returned by the DMF.

### DATA\_QUALITY\_MONITORING\_ANOMALY\_DETECTION\_STATUS view

The [DATA\_QUALITY\_MONITORING\_ANOMALY\_DETECTION\_STATUS view](/sql-reference/local/data_quality_monitoring_anomaly_detection_status), which exists in the SNOWFLAKE.LOCAL schema, flattens the
information in the event table to make it easier to access DMF results.
