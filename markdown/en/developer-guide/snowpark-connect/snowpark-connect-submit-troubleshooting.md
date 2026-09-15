# Troubleshooting Snowpark Submit

To diagnose and resolve issues that you encounter when you use Snowpark Submit, try the following the suggestion:

For more detailed options and command-line help, run `snowpark-submit --help` or see the
[Snowpark Submit reference](/developer-guide/snowpark-connect/snowpark-connect-submit-reference).

- Check the workload status and logs.

  Copy code

  ```
  snowpark-submit --snowflake-workload-name MY_JOB --workload-status --display-logs --snowflake-connection-name MY_CONNECTION
  ```

  When an event table is not used to store log data, logs are retained for a short period of time, such as five minutes or less.
- Verify your compute pool’s configuration.

  Ensure that your compute pool exists and has the appropriate privileges to run the workload.
- Ensure access to stages that are needed.

  Confirm that your application has proper access to any referenced stages and files within them.
- Ensure that dependencies are included.

  Verify that all application dependencies are correctly packaged and accessible to your Spark application.
