# JDBC Driver diagnostic service

To aid Snowflake Support in diagnosing customer incidents, the Snowflake JDBC driver utilizes a diagnostic service that runs in the background. When the driver encounters an issue that
prevents it from performing normally, the diagnostic service records information about the issue in a pair of compressed dump files located in the `/tmp/snowflake_dumps` folder:

- `sf_incident_<incident_number>.dmp.gz`
- `sf_log_<incident_number>.dmp.gz`

Important

The dump files may contain sensitive information (such as IP addresses) to further assist in solving the issue. Note that these files are only stored locally; they are not sent
to Snowflake. You must choose to share the files, such as when diagnosing issues with Snowflake Support.

If you wish to prevent the creation of these dump files by the drivers, set the `snowflake.disable_debug_dumps=true` system property.

When the driver encounters an issue, the service may also send diagnostic information to Snowflake to help fix the problem. This information includes:

- Driver version information.
- A generic description of the issue.
- Stack traces for the driver that pertain to the issue. Other than the account identifier, these stack traces include no customer information.
