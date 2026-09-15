# Resource definition and ingestion SQL reference

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

## STATE.RESOURCE\_INGESTION\_DEFINITION

This table is used to persist the data about configured resources. The data consists mostly of semi-structured variants.
The definition can be found in the file `ingestion/resource_ingestion_definition.sql`.

The table contains the following columns:

| Column name | Description |
| --- | --- |
| `id` | Id of Resource Ingestion Definition. |
| `name` | Name of the Resource Ingestion Definition that can be shown on UI. |
| `enabled` | Information whether the ingestion is enabled. |
| `parent_id` | Id of parent’s Resource Ingestion Definition, it lets you create a resource hierarchy that can be ingested |
| `resource_id` | Set of properties that are needed to define a resource in a specific connector. They identify a resource in a source system. They are set by a user. |
| `resource_metadata` | Set of additional properties that describe a resource. They can be fetched automatically or calculated by a connector. Optional. |
| `ingestion_configurations` | Set of configuration properties that describe how the resource should be ingested from the source system. Structure of this field is described in the next table. |
| `updated_at` | UTC timestamp representing recent update. |

Expand

Show lessSee more

The `ingestion_configuration` property should follow the below schema:

| Field name | Description |
| --- | --- |
| `id` | Id of Ingestion Configuration. Unique for given Resource Ingestion Definition |
| `ingestion_strategy` | Strategy of given ingestion. Values: snapshot, incremental |
| `custom_configuration` | Set of connector-specific ingestion properties |
| `schedule_type` | Type of schedule. Values: interval, cron |
| `schedule_definition` | String defining a schedule. e.g. 30m, 4h, 1d for interval. Cron expression in case of cron. |
| `destination` | Set of properties that describe where ingested data for a given resource should be stored. |

Expand

Show lessSee more

### Related Java objects

To interact with the `RESOURCE_INGESTION_DEFINITION` table the following Java objects are useful:

- [ResourceIngestionDefinitionRepository](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/ingestion/definition/ResourceIngestionDefinitionRepository.html)
- [ResourceIngestionDefinition](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/ingestion/definition/ResourceIngestionDefinition.html)
- [IngestionConfiguration](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/ingestion/definition/IngestionConfiguration.html)
- [IngestionStrategy](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/ingestion/definition/IngestionStrategy.html)
- [ScheduleType](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/ingestion/definition/ScheduleType.html)

## PUBLIC.INGESTION\_DEFINITIONS

File: `ingestion/ingestion_definitions_view.sql`

This view available to `ADMIN` and `VIEWER` users returns the data from the `STATE.RESOURCE_INGESTION_DEFINITION` table. The returned data is simplified and contains only some of the columns:

- id
- resource\_id
- name
- enabled

## STATE.INGESTION\_PROCESS

File: `ingestion/ingestion_run.sql`

This table is used to persist the data about process. It is not available to any role apart from the connector itself.
It contains the following columns:

> | Column | Type |
> | --- | --- |
> | `id` | `STRING` |
> | `resource_ingestion_definition_id` | `STRING` |
> | `ingestion_configuration_id` | `STRING` |
> | `type` | `STRING` |
> | `status` | `STRING` |
> | `created_at` | `TIMESTAMP_NTZ` |
> | `finished_at` | `TIMESTAMP_NTZ` |
> | `updated_at` | `TIMESTAMP_NTZ` |
>
> Expand
>
> Show lessSee more

### Related Java objects

The following Java classes are related to this table:

- [IngestionProcessRepository](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/ingestion/process/IngestionProcessRepository.html)
- [CrudIngestionProcessRepository](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/ingestion/process/CrudIngestionProcessRepository.html)
- [IngestionProcess](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/ingestion/process/IngestionProcess.html)

## STATE.INGESTION\_RUN

File: `ingestion/ingestion_run.sql`

A table used to store log data about past and current ingestion triggered by the scheduler. It is not available to any role apart from the connector itself.

It contains the following columns:

> | Column | Type |
> | --- | --- |
> | `id` | `STRING` |
> | `resource_ingestion_definition_id` | `STRING` |
> | `ingestion_configuration_id` | `STRING` |
> | `process_id` | `STRING` |
> | `started_at` | `TIMESTAMP_NTZ` |
> | `completed_at` | `TIMESTAMP_NTZ` |
> | `status` | `STRING` |
> | `ingested_rows` | `NUMBER` |
> | `metadata` | `VARIANT` |
>
> Expand
>
> Show lessSee more

### Related Java objects

The following Java classes are related to this table:

- [IngestionRunRepository](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/observability/IngestionRunRepository.html)
- [CrudIngestionRunRepository](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/observability/CrudIngestionRunRepository.html)
- [IngestionRun](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/observability/IngestionRun.html)
- [IngestionRun.IngestionStatus](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/observability/IngestionRun.IngestionStatus.html)
