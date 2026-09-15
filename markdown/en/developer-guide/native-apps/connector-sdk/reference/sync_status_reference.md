# Sync status reference

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

## Database objects and procedures

The following database objects are created through the file `observability/sync_status.sql`.

### PUBLIC.SYNC\_STATUS

View exposed to the `ADMIN` and `VIEWER` roles and providing information about the synchronization status of the connector.
The main functionalities are based on the tables `APP_STATE`, `GENERIC_CONNECTOR_STATS`, `INGESTION_DEFINITIONS`,
be careful when overwriting so that the view is still usable.

The view contains the following columns:

1. `status` `STRING`
2. `last_synced_at` `TIMESTAMP_NTZ`

With the following statuses available:

- `PAUSED` when the connector is paused.
- `LAST_SYNCED` when at least one run ended with COMPLETED status.
- `SYNCING_DATA` when there is an enabled resource but no runs ended with COMPLETED status.
- `NOT_SYNCING` when no runs were started and all resources are disabled.
- `DISCONNECTED` this state is not supported yet.

## Related tables and views

Sync Status is related to and dependent on the objects from the following files:

- `core.sql` (See [Core SQL reference](/developer-guide/native-apps/connector-sdk/reference/core_reference))
- `observability/connector_stats.sql` (See [Connector stats reference](/developer-guide/native-apps/connector-sdk/reference/connector_stats_reference))
- `ingestion/ingestion_definitions_view.sql` (See [Resource definition and ingestion SQL reference](/developer-guide/native-apps/connector-sdk/reference/resource_definition_and_ingestion_processes_reference))
