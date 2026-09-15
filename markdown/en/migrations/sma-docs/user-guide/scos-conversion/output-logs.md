description:
:   Everything that happened. Everything.

# Snowpark Migration Accelerator: Output Logs

The Snowpark Migration Accelerator (SMA) creates detailed log files during its execution. These logs track the tool’s operations and are valuable resources for troubleshooting when issues occur.

The SMA generates three log files during execution. Each log file has a .log extension and includes the date in its filename. These files are continuously updated while SMA is running.

- **Controller-Log**: Displays basic information about the SMA execution, including the session ID and summary metrics. This log is completed when the tool finishes running.
- **Generic-Scanner-Log**: Shows basic scanning information from the initial tool execution, including session ID, execution ID, and scanner completion status.
- **SparkSnowConvert-Log**: The main log file produced by the SMA (previously known as SnowConvert for Spark). It records detailed information about:
  - Tool execution steps
  - Error messages (both execution and conversion errors)
  - Troubleshooting information for failed executions

The log is completed when the tool finishes running.

If you are experiencing issues with the Snowpark Migration Accelerator (SMA) and need to analyze the logs, visit [the Support section](/migrations/sma-docs/support/general-troubleshooting/README) of our documentation or contact our support team directly at [sma-support@snowflake.com](mailto:sma-support@snowflake.com).
