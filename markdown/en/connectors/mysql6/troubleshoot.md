# Troubleshooting the Snowflake Connector for MySQL

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts except government regions.

Important

Thank you for your interest in the Snowflake Connector for MySQL.
We’re now focused on a next-generation solution that will offer a significantly
improved experience; therefore, moving this connector to the general availability
status is currently not on our product roadmap.
You may continue to use this connector as preview feature, but please note that support for future bug
fixes and improvements are not guaranteed. The new solution is available as [Openflow Connector for MySQL](/user-guide/data-integration/openflow/connectors/mysql/about) and
includes better performance, customizability, and enhanced deployment options.

## Contact Snowflake Support

If you encounter an issue while using the connector, [submit a support case](/user-guide/ui-support).

Snowflake usually analyzes the logs from your connector to offer a resolution. Logs from the connector, both the native app and the database agent logs, are stored in the event table of your account. However, there are different mechanisms for sharing these logs with Snowflake.

### Sharing the native app logs with Snowflake

By default, the native app logs are accessible to Snowflake. To find out more about the sharing mechanism, see [Set up event tracing for an app](http://docs.snowflake.com/native-apps/consumer-enable-logging).

Note

If you disable log sharing, then you need to attach the logs to any support case you submit. Re-enabling log sharing does not include historical records, but only entries from the time you re-enable it.

### Sharing the database agent logs with Snowflake

> To share the database agent logs with Snowflake, you must extract them and attach them to the support case manually, as described in the following steps:

1. Query the logs as described in [Viewing the agent logs](/connectors/mysql6/monitor#label-mysql-connector-viewing-agent-logs-6).

1. Select **Download or View Results**.
2. Click **Export**.
3. Attach the exported file to your support case.
