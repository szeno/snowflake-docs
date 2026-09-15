# Connector stats reference

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

## Database objects and procedures

The following database objects are created through the file `observability/connector_stats.sql`.

### PUBLIC.GENERIC\_CONNECTOR\_STATS

View not available for any role, access via view `CONNECTOR_STATS`. View providing the data about ongoing and finished
ingestion runs. A view that retrieves and maps the data from the union of [`STATE.INGESTION_RUN` /
`STATE.RESOURCE_INGESTION_DEFINITION` / `STATE.INGESTION_PROCESS`] internal tables.

View structure with mapping is as follows:

1. ID (col) → RUN\_ID (col);
2. RESOURCE\_INGESTION\_DEFINITION\_ID (col)
3. INGESTION\_CONFIGURATION\_ID (col)
4. INGESTION\_PROCESS\_ID (col)
5. NAME (col)
6. STARTED\_AT (col)
7. UPDATED\_AT (col)
8. COMPLETED\_AT (col)
9. STATUS (col)
10. INGESTED\_ROWS (col)
11. DATEDIFF(second from STARTED\_AT and COMPLETED\_AT) (col) → DURATION\_S (col);
12. INGESTED\_ROWS (col) / DURATION\_S (col) → THROUGHPUT\_RPS (col);
13. METADATA (col)

### PUBLIC.AGGREGATED\_CONNECTOR\_STATS

This view is exposed to the `ADMIN` and `VIEWER` roles. It returns aggregated data from the above view and allows
access for the defined user. The rows will be grouped by truncated hours and displayed with summed updated rows.
View providing the aggregated data about daily ingestion runs.

A view that retrieves and maps the data from the `GENERIC_CONNECTOR_STATS` internal table
The mapping is as follows:

1. GROUPED BY(hours from STARTED\_AT (col)) → RUN\_DATE (col);
2. SUM(INGESTED\_ROWS (col)) → UPDATED\_ROWS (col);

Example `AGGREGATED_CONNECTOR_STATS` view created on example GENERIC\_CONNECTOR\_STATS:

| RUN\_DATE | UPDATED\_ROWS |
| --- | --- |
| <timestamp\_ntz> | 20 |
| <timestamp\_ntz> | 40 |
| … | … |

Expand

Show lessSee more

Overwriting this view is not recommended.

### PUBLIC.CONNECTOR\_STATS

This view is exposed to the `ADMIN` role. It returns data from the connector stats view and allows access for the defined user.
In the default implementation this view exists only as an additional layer above `GENERIC_CONNECTOR_STATS`.
This implementation should be overwritten if some additional custom data needs to be added.

## Related tables and views

Connector stats are related to and dependent on the objects from the following files:

- `ingestion/ingestion_run.sql` (See: [STATE.INGESTION\_RUN](/developer-guide/native-apps/connector-sdk/reference/resource_definition_and_ingestion_processes_reference#label-connectors-native-sdk-ingestion-run))
- `ingestion/resource_ingestion_definition.sql` (See: [STATE.RESOURCE\_INGESTION\_DEFINITION](/developer-guide/native-apps/connector-sdk/reference/resource_definition_and_ingestion_processes_reference#label-connectors-native-sdk-ingestion-definition))
- `ingestion/ingestion_process.sql` (See: [STATE.INGESTION\_PROCESS](/developer-guide/native-apps/connector-sdk/reference/resource_definition_and_ingestion_processes_reference#label-connectors-native-sdk-ingestion-process))
