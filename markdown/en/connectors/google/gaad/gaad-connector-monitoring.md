# Monitoring the

This section describes how to monitor the state of the and troubleshoot problems.

## About monitoring the connector

To monitor the state of the and troubleshoot problems, you can use the following database objects to access
the connector’s configuration, error messages, and statistics:

| Name | Description |
| --- | --- |
| `PUBLIC.REPORT_LIST_VIEW` | The list of currently configured reports, including information about the most recent ingestion:   - Report unique ID and name - Google Analytics property ID - Refresh interval - Information about the most recent ingestion |
| `PUBLIC.CONNECTOR_STATS` | Data about finished ingestion runs:   - Resource ingestion definition id: unique report ID - Ingestion configuration id: always `STANDARD` - Ingestion process id: always `NULL` - Resource name: report name - Started at: start of a single ingestion run - Updated at: last update time - Completed at: end of a single ingestion run - Status: status of ingestion run; can be `COMPLETED`, `FAILED` or `CANCELED` - Ingested rows: how many rows were fetched during the ingestion - Duration in seconds: duration of ingestion (difference between *started at* and *completed at*, in seconds) - Throughput in rows per seconds: number of ingested rows divided by duration |
| `PUBLIC.CONNECTOR_ERRORS` | Stored application error logs:   - Code: error code - Message: readable message as a string - Created\_at: timestamp when log was created - context: payload that defines the error context |

Expand

Show lessSee more

These objects can be accessed by the `ADMIN` and `VIEWER` application roles defined by the connector.
