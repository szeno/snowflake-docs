# Monitor the Snowflake Connector for SharePoint

[Preview Feature](/release-notes/preview-features) — Open

Support for this feature is available to accounts in most Snowflake regions. See [Regional availability](/connectors/unstructured-data-connectors/sharepoint/about#label-sharepoint-regional-availability) for a full list of regions.

Note

The Snowflake Connector for SharePoint is subject to the [Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

Important

Thank you for your interest in the Snowflake Connector for SharePoint.
We’re now focused on a next-generation solution that will offer a significantly
improved experience; therefore, moving this connector to the general availability
status is currently not on our product roadmap.
You may continue to use this connector as a preview feature, but please note that support for future bug
fixes and improvements is not guaranteed. The new solution is available as [Openflow Connector for SharePoint](/user-guide/data-integration/openflow/connectors/sharepoint/about) and
includes better performance, customizability, and enhanced deployment options.

This topic describes how to monitor the state of the Snowflake Connector for SharePoint.

## Views

To monitor the state of the Snowflake Connector for SharePoint and troubleshoot problems, view
the connector configuration, error messages and statistics detailed the following views, which are defined in
the PUBLIC schema of the connector application.

| View | Description |
| --- | --- |
| `APP_PROPERTIES` | Provides information to the user interface about properties supported by the Snowflake Connector for SharePoint |
| `CONNECTOR_CONFIGURATION` | Provides a list of the values for configuration settings used by the connector. |
| `CONNECTOR_ERRORS` | Provides access to errors that have occurred during data ingestion. |
| `SYNC_STATUS` | Provides the general status of the connector and the ingestion process, and includes states:   - `PAUSED`: The connector is currently paused or resuming and no ingestion of any data is currently ongoing. - `SYNCING_DATA`: The connector is actively ingesting data. - `LAST_SYNCED`: Ingestion for at least one table has completed.   The timestamp of the most recently completed ingestion is provided in the `LAST_SYNCED_AT` column. |

Expand

Show lessSee more

### Examples

> Copy code
>
> ```
> SELECT * FROM <APPLICATION_INSTANCE_DATABASE>.PUBLIC.CONNECTOR_CONFIGURATION;
> SELECT * FROM <APPLICATION_INSTANCE_DATABASE>.PUBLIC.CONNECTOR_ERRORS;
> SELECT * FROM <APPLICATION_INSTANCE_DATABASE>.PUBLIC.SYNC_STATUS;
> ```

Note that all the timestamps displayed in these views are provided in the UTC timezone with no offset.

### Required roles

The following roles have access to the described views:

- The owner of the connector application (typically the ACCOUNTADMIN system role).
- Any role with ADMIN or VIEWER application role granted.
