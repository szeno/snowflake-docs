# Troubleshooting the Snowflake Connector for PostgreSQL

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts except government regions.

Important

Thank you for your interest in the Snowflake Connector for PostgreSQL.
Note that we’re now focused on a next-generation solution that will offer a significantly improved experience.
Hence, moving this connector to the general availability status is currently not on our product roadmap.
You may continue to use this connector as a preview feature, but please note that support for future bug
fixes and improvements are not guaranteed. The new solution is available as [Openflow Connector for PostgreSQL](/user-guide/data-integration/openflow/connectors/postgres/about) and
includes better performance, customizability, and enhanced deployment options.

## Contact Snowflake Support

If you encounter an issue while using the connector, [submit a support case](/user-guide/ui-support).

Snowflake usually analyzes the logs from your connector to offer a resolution. Logs from the connector, both the native app and the database agent logs, are stored in the event table of your account. However, there are different mechanisms for sharing these logs with Snowflake.

### Sharing the Native App logs

By default, the native app logs are accessible to Snowflake. To find out more about the sharing mechanism, see [Set up event tracing for an app](http://docs.snowflake.com/native-apps/consumer-enable-logging).

Note

If you disable log sharing, then you need to attach the logs to any support case you submit. Re-enabling log sharing does not include historical records, but only entries from the time you re-enable it.

### Sharing the database agent logs

The agent replicates its Native App counterpart. To send the agent logs back to Snowflake:

1. Access the agent logs table as described in [Viewing the agent logs](/connectors/postgres6/monitor#label-postgres-connector-viewing-agent-logs-6).

1. Select **Download or View Results**.
2. Click **Export**.
3. Attach the exported file to your support case.
