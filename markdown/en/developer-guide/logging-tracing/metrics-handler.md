# Emitting metrics data from handler code

To have your procedure or UDF emit metrics data, you don’t need to add any code to your handler. Snowflake generates the data collected in an
event table.

## How metrics are measured

Due to the way the Java and Python execution environments differ, the metrics data collected also differs. For reference information
about the data collected, see [RECORD column reference](/developer-guide/logging-tracing/event-table-columns#label-event-table-record-column-metric).

The following describes how the captured data corresponds to the execution environment.

Java:
:   JVM (Java Virtual Machine) CPU and memory metrics are reported for each query ID.

    Each stored procedure is allocated its own JVM. The following describes the metric data collected:

    - `process.memory.usage`: Amount of memory, in bytes, consumed by the JVM executing the stored procedure handler.
    - `process.cpu.utilization`: Total CPU time divided by the wall-clock time per logical CPU, measured as a percentage where
      1.0 indicates 100 percent utilization. Total CPU time is the total time spent on non-idle tasks.

    Each Java and Scala UDF called in a query shares a single JVM. Metric values are aggregated across each Java or Scala function in the query. The
    following describes the metric data collected:

    - `process.memory.usage`: Memory use, shown as the sum of all the associated Java functions called in the query.
    - `process.cpu.utilization`: CPU use, shown as the average of all the Java and Scala functions called in the query.

Python:
:   CPU and memory metrics are reported for each Python function or procedure.

    Each stored procedure executes on only one Python process. The following describes the metric data collected:

    - `process.memory.usage`: Amount of memory, in bytes, consumed by the Python process executing the stored procedure handler.
    - `process.cpu.utilization`: Total CPU time divided by the wall-clock time per logical CPU, measured as a percentage where 1.0
      indicates 100 percent use. Total CPU time is the total time spent on non-idle tasks.

    Each UDF can be executed on multiple Python execution processes. Values are aggregated across multiple processes. The following describes
    the metric data collected:

    - `process.memory.usage`: Memory use, shown as the sum of all the associated Python processes of that UDF.
    - `process.cpu.utilization`: Reported CPU, shown as the average of all the associated Python processes of that UDF.

## Python example

Use the following steps to generate metrics example data.

1. Set the metrics level of your session. The `METRIC_LEVEL` parameter controls whether to emit auto-instrumented resource
   metrics data points to the event table. You can set the parameter to `NONE` or `ALL`, and set it on the object and
   session level. For more information, see [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

   Copy code

   ```
   ALTER SESSION SET METRIC_LEVEL = ALL;
   ```
2. Create a stored procedure.

   Copy code

   ```
   CREATE OR REPLACE PROCEDURE DEMO_SP(n_queries number)
   RETURNS VARCHAR
   LANGUAGE PYTHON
   RUNTIME_VERSION = '3.10'
   PACKAGES = ('snowflake-snowpark-python')
   HANDLER = 'my_handler'
   AS $$
   import time
   def my_handler(session, n_queries):
     import snowflake.snowpark
     from snowflake.snowpark.functions import col, udf
     from snowflake import telemetry

     session.sql('create or replace stage udf_stage;').collect()

     @udf(name='example_udf', is_permanent=True, stage_location='@udf_stage', replace=True)
     def example_udf(x: int) -> int:
    # This UDF will consume 1GB of memory to illustrate the memory consumption metric
    one_gb_list = [0] * (1024**3 // 8)
    return x

     pandas_grouped_df = session.table('snowflake.account_usage.query_history').select(
    col('total_elapsed_time'),
    col('rows_written_to_result'),
    col('database_name'),
    example_udf(col('bytes_scanned'))
     ).limit(n_queries)\
     .to_pandas()\
     .groupby('DATABASE_NAME')

     mean_time = pandas_grouped_df['TOTAL_ELAPSED_TIME'].mean()
     mean_rows_written = pandas_grouped_df['ROWS_WRITTEN_TO_RESULT'].mean()

     return f"""
     {mean_time}
     {mean_rows_written}
     """
   $$;
   ```
3. Run the stored procedure

   Copy code

   ```
   CALL DEMO_SP(100);
   ```
4. When the query is completed, view metrics data as described in [Viewing metrics data](/developer-guide/logging-tracing/metrics-viewing-data).
