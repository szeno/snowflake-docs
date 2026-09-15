# About the Snowflake Connector for ServiceNow®

Feature — Generally Available

The Snowflake Connector for ServiceNow® is generally available on supported cloud platforms.

The Snowflake Connector for ServiceNow® enables you to ingest ServiceNow® data into your Snowflake account.

ServiceNow® is a cloud-based platform that delivers workflows for service management including incident management, change management, asset management, configuration management, service catalog, request fulfillment, etc.

The Snowflake Connector for ServiceNow® allows you to ingest data from ServiceNow® into Snowflake automatically. The connector supports both the initial load of historical data as well as incremental updates. The latest data is regularly pulled from ServiceNow®. You control how frequently it is refreshed.

Note

Data ingestion relies on `v2` of the ServiceNow® [table API](https://developer.servicenow.com/dev.do#!/reference/api/latest/rest/c_TableAPI).

The connector lets you replicate key dimensions and metrics from ServiceNow®, including:

- Incidents
- Changes
- Users
- Service catalog items
- Configuration items
- Company assets

## Known Limitations

The Snowflake Connector for ServiceNow® has the following limitations:

- The connector can only ingest ServiceNow® tables with the `sys_id` column present.
- Changes to ServiceNow® table schema are not reflected in already ingested rows, unless they are updated.
- ServiceNow® views are not supported.
- Archived records in ServiceNow® are not ingested into Snowflake. See [the documentation](/connectors/servicenow/ingestion#label-servicenow-connector-archived-records) for more details.
- The connector does not work with ServiceNow® instances where IP address access control has been configured to deny access from an outside network.
- The connector does not work with a ServiceNow® instance that is hidden behind a VPN.
- Replication of the connector to failover region is not automatic and requires additional manual steps.
- The connector does not support [MANAGED ACCESS](/sql-reference/sql/create-versioned-schema#label-create-versioned-schema-optional-parameters) destination schemas.
- The connector requires the [AUTOCOMMIT parameter](/sql-reference/parameters#label-autocommit) to be enabled.
- The connector requires a virtual warehouse with AUTO\_RESUME enabled. Serverless is not supported. Connector procedures are not guaranteed to work when called using serverless compute.
- Executing certain procedures via external tasks is not supported, that is:
  - `CHECK_IF_AUDIT_ENABLED`
  - `CHECK_RECORD_HISTORY`
  - `TEST_CONNECTION`
  - `TEST_TABLE_ACCESS`
  - `GET_AVAILABLE_TABLES`
  - `ENABLE_TABLE` (with custom configuration parameters)
  - `SET_CONNECTION_CONFIGURATION`
  - `FINALIZE_CONNECTOR_CONFIGURATION`
  - `CONFIGURE_QUERY_CATEGORY`
  - `CONFIGURE_CUSTOM_API_PATH`
