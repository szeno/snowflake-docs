# ODBC Driver diagnostic service

## ODBC 4.x

For ODBC 4.x, set `SNOWFLAKE_TROUBLESHOOTING_ENABLED=true` before starting the application.
Set `SNOWFLAKE_TROUBLESHOOTING_REPORT_PATH` to the output directory; the troubleshooting log is
`sf_driver_troubleshooting.log`. See [Configuration differences](/developer-guide/odbc/odbc-migration#label-odbc-migration-config)
for connectivity diagnostics and logging configuration.

The background incident-dump service described below applies to ODBC 3.x.

## ODBC 3.x

To aid Snowflake Support in diagnosing customer incidents, the Snowflake ODBC 3.x driver utilizes a diagnostic service that runs in the background. When the driver encounters an issue that prevents
it from performing normally, the diagnostic service records information about the issue:

- The service writes a single compressed `sf_incident_log.dmp.gz` file to the `/tmp` folder by default.
- A different ODBC dump file location can be specified using the `LogPath` property in `simba.snowflake.ini`.

Important

The dump file may contain sensitive information (such as IP addresses) to further assist in solving the issue. Note that this file is only stored locally; it is not sent to Snowflake.
You must choose to share the files, such as when diagnosing issues with Snowflake Support.

If you wish to prevent the creation of dump files by the 3.x driver, set the `DisableSfDumps=true` parameter in `simba.snowflake.ini`.

When a driver encounters an issue, the service may also send diagnostic information to Snowflake to help fix the problem. This information includes:

- Driver version information.
- A generic description of the issue.
- Stack traces for the driver that pertain to the issue. Other than the account identifier, these stack traces include no customer information.
