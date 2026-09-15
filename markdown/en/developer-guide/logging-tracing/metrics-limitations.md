# Metrics limitations

- Metrics are collected from the Python and Java environments at regular 10-second intervals.
  If a UDF or stored procedure is completed before the first interval, no metrics are collected for the execution.
- Snowpark CPU and memory metrics are not supported for JavaScript stored procedures or UDFs.
