# ANOMALY\_DETECTION (SNOWFLAKE.ML)

Anomaly detection allows you to detect outliers in your time series data by using a machine learning algorithm. You use [CREATE SNOWFLAKE.ML.ANOMALY\_DETECTION](/sql-reference/classes/anomaly-detection/commands/create-anomaly-detection#label-class-anomaly-detection-create) to create
and train a detection model, and then use the [<model\_name>!DETECT\_ANOMALIES](/sql-reference/classes/anomaly-detection/methods/detect_anomalies#label-class-anomaly-detection-detect-anomalies) method to detect anomalies.

Important

**Legal notice.** This Snowflake ML function is powered by machine learning technology, which you, not Snowflake, determine when and how to use. Machine
learning technology and results provided may be inaccurate, inappropriate, or biased.
Snowflake provides you with the machine learning models that you can use within your own workflows. Decisions based on machine
learning outputs, including those built into automatic pipelines, should have human oversight and review processes
to ensure model-generated content is accurate.
Snowflake provides algorithms (without any pretraining) and you’re responsible for the data that you provide the algorithm (for example, for training and inference) and the decisions you make using the resulting model’s output.
Queries for this feature or function are treated as any
other SQL query and may be considered [metadata](/sql-reference/metadata).

**Metadata.** When you use Snowflake ML functions, Snowflake logs generic error messages returned by an ML
function. These error logs help us troubleshoot issues that arise and improve these functions to serve you better.

For further information, see [Snowflake AI Trust and Safety FAQ](https://www.snowflake.com/en/legal/snowflake-ai-trust-and-safety/).

## ANOMALY\_DETECTION commands

- [CREATE SNOWFLAKE.ML.ANOMALY\_DETECTION](/sql-reference/classes/anomaly-detection/commands/create-anomaly-detection)
- [DROP SNOWFLAKE.ML.ANOMALY\_DETECTION](/sql-reference/classes/anomaly-detection/commands/drop-anomaly-detection)
- [SHOW SNOWFLAKE.ML.ANOMALY\_DETECTION](/sql-reference/classes/anomaly-detection/commands/show-anomaly-detection)

## ANOMALY\_DETECTION methods

- [<model\_name>!DETECT\_ANOMALIES](/sql-reference/classes/anomaly-detection/methods/detect_anomalies)
- [<model\_name>!EXPLAIN\_FEATURE\_IMPORTANCE](/sql-reference/classes/anomaly-detection/methods/explain_feature_importance)
- [<model\_name>!SHOW\_EVALUATION\_METRICS](/sql-reference/classes/anomaly-detection/methods/show_evaluation_metrics)
- [<model\_name>!SHOW\_TRAINING\_LOGS](/sql-reference/classes/anomaly-detection/methods/show_training_logs)
