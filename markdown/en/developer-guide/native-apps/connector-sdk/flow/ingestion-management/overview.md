# Ingestion management

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

After the connector is configured it can start ingesting the data.
However, usually some more information is needed before it can ingest the data from the source system.
Most of the systems persist the data with at least some granularity, be it tables, repositories, files, or reports.
The Snowflake Native SDK for Connectors uses a term `resource` regardless of the name in the original system.
To identify resources and customize settings for their ingestion, `resource_ingestion_definitions` are being used. Additionally,
the actual process of ingestion is organized into `ingestion_processes`, which consist of multiple `ingestion_runs`.
This abstraction makes it easier to track, schedule and differentiate processes.

## Requirements

This section requires at least the following SQL files to be executed during native app installation:

- `ingestion/ingestion_management.sql`
- `ingestion/ingestion_definitions_view.sql`
- `ingestion/ingestion_process.sql`
- `ingestion/ingestion_run.sql`
- `ingestion/resource_ingestion_definition.sql`

## Resource ingestion definition

Resource ingestion definition is a generic entity that contains the definition of the source data in the source system.
To keep it as generic as possible the system specific options are persisted as `variants`
in the underlying `STATE.RESOURCE_INGESTION_DEFINITION` table. However, the Java definition of the repository `ResourceIngestionDefinitionRepository`
is a generic interface to have better control over typing.

Since most of the resource ingestion definition can be customized by during the implementation,
then it is up to the developer to decide how to use the generic fields and then make use of them during ingestion.

The most important customizable properties of the resource ingestion definition are:

- `parent_id`

This optional parameter allows linking resource definitions with each other, for example, to inherit a part of the configuration.

- `resource_id`

This `variant` should allow the identification of a resource in the source system, it should be unique.

- `ingestion_configurations`

This property actual configuration of the ingestion, each definition can have multiple configurations,
for example if for some reason the same resource should be ingested at two different schedules or saved into multiple sink tables.
This property has some required fields inside of it, but still allows some flexibility when it comes to defining custom configuration
and destination of the data.

- `resource_metadata`

This property should contain any additional information that is needed, but does not fit into above mentioned fields.

## Ingestion process

Ingestion process is an entity representing enabled process of ingesting a defined resource. It is created once a resource is added or enabled and should be completed
once it’s deleted or disabled. In a way it is kind of like a background process in the operating system, it can be alive but not necessarily doing any work at the particular moment.
Whenever the ingestion is actually running it can be transitioned to `IN_PROGRESS` state, otherwise it can remain in `SCHEDULED` state.
When dispatching work `scheduler` retrieves all the `SCHEDULED` processes and runs ingestion for them.

The ingestion process can be also used to define different types of ingestion, for example, say that on a daily basis connector loads some data,
but for some reason some old data is corrupted and needs to be reloaded. If that’s the case then a new process `type` can be introduced, for example `RELOAD`.
Then `scheduler` can have custom logic to perform different operations for different types of processes.

## Ingestion run

Ingestion run is another entity to store information about the past and ongoing ingestion. However, this data is more granular than the `ingestion_process` itself.
First of all, ingestion run should be considered as a log data. Secondly, `ingestion_run` is an entry describing just a single invocation during a long running process.
So if a resource is ingested once a day, then every day there should be a new ingestion run entry. All of those entries will be linked with the single process.

## Ingestion management operations

### Creating new resource

Resource creation process is used to define and schedule an ingestion of data from a source system.
It creates a resource ingestion definition record and corresponding ingestion processes if a given resource should be initially enabled.

For more information, see [Create Resource](/developer-guide/native-apps/connector-sdk/flow/ingestion-management/create_resource).

### Viewing resources

Configured resources definitions can be examined in the `PUBLIC.INGESTION_DEFINITIONS` view. However, this view only returns basic information about each resource.
All the custom configurations are not visible to the end user, especially because some of them can be generated internally by the connector’s logic.

### Disabling a resource

The disabling a resource step is used to stop ingesting data for a given resource.
It finishes active ingestion processes and marks a resource ingestion definition as disabled.

For more information, see [Disable Resource](/developer-guide/native-apps/connector-sdk/flow/ingestion-management/disable_resource).

### Enabling a resource

Enabling a resource is used to start ingesting data for a given resource.
It creates new ingestion processes and marks a resource ingestion definition as enabled.

For more information, see [Enable Resource](/developer-guide/native-apps/connector-sdk/flow/ingestion-management/enable_resource).

### Updating a resource

Updating a resource is used to change a configuration of ingestion for a given resource.
It modifies a resource ingestion definition and finishes or creates new ingestion processes.

For more information, see [Update Resource](/developer-guide/native-apps/connector-sdk/flow/ingestion-management/update_resource).
