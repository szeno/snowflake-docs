# Monitoring the Snowflake Connector for Google Analytics Raw Data

This topic describes how to monitor the state of the Snowflake Connector for Google Analytics Raw Data and troubleshoot problems.

## About monitoring the connector

To monitor the state of the Snowflake Connector for Google Analytics Raw Data and troubleshoot problems, you can access
the connector configuration, error messages and statistics through the following views, which are defined
in the `PUBLIC` schema in the database that serves an instance of the connector:

| View Name | Description |
| --- | --- |
| `CONNECTOR_CONFIGURATION` | The parameters used to configure the connector such as:   - Destination database and schema for ingested data. - Data owner role. - Warehouse used by the connector. - Secret used for authentication. - Dispatcher schedule. - Number of worker tasks. - Object names of the external access integration, security integration and secret used by the Connector. |
| `CONNECTOR_ERRORS` | Log of errors that occurred during the connector’s work. |
| `CONNECTOR_STATS` | Log of all the connector’s attempt to retrieve data, detailing:   - Source BigQuery table and Snowflake destination table. - Start and end time of the attempt. - Status of the attempt. Possible values include:    - `IN_PROGRESS` - data ingestion is currently running.   - `COMPLETED` - data ingestion has successfully finished.   - `FAILED` - data ingestion failed and is being retried.   - `CANCELLED` - data ingestion was terminated and is being retried.   - `DATA_NOT_FOUND` - at the time of the ingestion attempt, the related Google Analytics daily table was not visible in BigQuery. - For successful attempts, the total number of records retrieved, the time it took to retrieve them, and the average throughput. - Errors encountered during the attempt, if any. |
| `ENABLED_PROPERTIES` | List of currently enabled Google Analytics properties. |

Expand

Show lessSee more

To see the full list of columns in each view, use the [DESCRIBE VIEW](/sql-reference/sql/desc-view) command.

After the connector installation, only the ACCOUNTADMIN system role has access to these views. To change it, grant the appropriate permission to the other roles.
