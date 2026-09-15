# Native SDK for Connectors Java - release notes

Release notes for Native SDK for Connectors Java library.

## Version 2.2.0 (July 10th, 2024)

### General changes

- Replaced the SnowSQL tool with new Snowflake CLI tool
- Updated Java dependencies

### Behavior changes

- `com.snowflake.connectors.common.object`:

  - Changed value returned by `toString` to be the same as in `getValue` in classes:
    - `Identifier`
    - `ObjectName`
    - `Reference`
    - `SchemaName`
- `com.snowflake.connectors.application.scheduler.SchedulerCreator`:

  - Renamed class to `SchedulerManager`.
- `com.snowflake.connectors.taskreactor.commands.queue.CommandsQueueRepository`:

  - Renamed class to `CommandsQueue`.
- `com.snowflake.connectors.application.integration.SchedulerTaskReactorOnIngestionScheduled`:

  - Renamed class to `TaskReactorOnIngestionScheduledCallback`.
  - The class now uses `ResourceIngestionDefinition` and its generic parameters.
- `com.snowflake.connectors.taskreactor.config.ConfigRepository`:

  - Config values are now always treated as Strings, not Variants.

### New features

- New `PUBLIC.RESET_CONFIGURATION()` procedure that resets the configuration wizard state.
  Additional callbacks let you perform custom operations during the procedure flow.
  See also [Reset configuration](../../developer-guide/native-apps/connector-sdk/flow/reset_configuration).
- New `PUBLIC.RECOVER_CONNECTOR_STATE(STRING)` procedure that resets the connector state.
  See also [Recover connector state](/developer-guide/native-apps/connector-sdk/reference/core_reference#label-connectors-native-sdk-recover-connector-state).
- New `TASK_REACTOR.REMOVE_INSTANCE(STRING)` procedure that removes a Task Reactor instance.
  See also [Remove instance](/developer-guide/native-apps/connector-sdk/reference/task_reactor_reference#label-connectors-native-sdk-task-reactor-remove-instance).
- `com.snowflake.connectors.application.configuration.connector.ConnectorConfigurationKey`:

  - Added new `CORTEX_WAREHOUSE` key.
  - Added new `CORTEX_USER_ROLE` key.
- `com.snowflake.connectors.util.time`:

  - Added new classes for JSON serialization of `LocalDate` and `ZoneId`.
- `com.snowflake.connectors.common.task.TaskRepository`:

  - Added support for the `AFTER` parameter during task creation, if task predecessors have been specified.
  - Added support for the `USER_TASK_TIMEOUT_MS` parameter.
- `com.snowflake.connectors.common.task.TaskProperties`:

  - Added support for task predecessors.
  - Added support for the `USER_TASK_TIMEOUT_MS` property.
- `com.snowflake.connectors.util.sql.SqlTools`:

> - Added `callProcedureRaw(Session, String, String...)` method.
> - Added `callProcedureRaw(Session, String, String, String...)` method.

- Added new `com.snowflake.connectors.taskreactor.worker.ingestion.SimpleIngestionWorker` class - a
  simple worker implementation for use with ingestion workloads.
- Added new `com.snowflake.connectors.taskreactor.worker.ingestion.SimpleIngestion` class - a simple
  ingestion representation, for use by an `IngestionWorker`.
- Added new `com.snowflake.connectors.taskreactor.worker.ingestion.SimpleIngestionWorkItem` class - a
  simple work item implementation for ingestion work.

### Bug fixes

- `com.snowflake.connectors.common.task.TaskRepository`:

  - Fixed the successful task creation condition check in `create(TaskDefinition, boolean, boolean)`.
- `com.snowflake.connectors.util.variant.VarianMapper`:

  - Fixed handling of timestamps in Variants.
- Corrected default input validators in handlers for the connector configuration processes.
- Removed `DataFrame#first` from most `SELECT` queries, which fixed issues with using some procedures
  in tasks.
- Removed granting `USAGE` on `STATE` schema to app role `ADMIN`.
- Added missing `UPDATED_AT` column to the Task Reactor config table.

## Version 2.1.0 (July 8th, 2024)

### Behavior changes

- New identifier approach.

  Important

  This new approach may change how identifiers are used in your connector, please test the new changes thoroughly!

  - The SDK now expects all identifiers to be sent as provided by the user; the SDK will assess by itself whether it’s a quoted identifier or not in order to process it correctly further.
  - Auto quoting of identifiers will be done only when using values returned by Snowflake queries.
  - To use the new approach with the UI - the connector must return a new property in the `PUBLIC.APP_PROPERTIES` view, with the key of `UI_ADD_QUOTES_TO_EXISTING_QUOTED_IDENTIFIERS` and a value of `TRUE`.
  - Changed `com.snowflake.connectors.common.object.Identifier` class:
    - Removed `fromWithAutoQuoting()` and `getName()` methods.
    - Removed the concept of an empty identifier; removed `empty()`, `isNullOrEmpty()`, `validateNullOrEmpty()`, and `isEmpty()` methods.
    - Added new `from()` method, which allows for enabling of auto quoting during identifier instance creation; the provided String will not be auto quoted if it is an unquoted, fully uppercase identifier.
    - Changed `validate()` method to `isValid()`.
    - Changed `toSqlString()` method to `getValue()`.
    - Added `getUnquotedValue()`, `getQuotedValue()`, `getVariantValue()`, and `isUnquoted()` methods.

> - Changed `com.snowflake.connectors.common.object.ObjectName` class:
>
>   - Made database and schema properties `Optional`.
>   - Changed return type of `getDatabase()` and `getSchema()` to `Optional`.
>   - Changed `validate()` method to `isValid()`.
>   - Changed `validateDoubleDot()` method to `isDoubleDot()`.
>   - Changed `getEscapedName()` method to `getValue()`.
>   - Added `getVariantValue()` and `getSchemaName()` methods.
> - Changed `com.snowflake.connectors.common.object.Reference` class:
>
>   - Removed the concept of an empty reference; removed `empty()` and `isEmpty()` methods.
>   - Changed `validate()` method to `isValid()`.
>   - Changed `referenceName()` method to `getName()`.
>   - Changed `value()` method to `getValue()`.
>   - Added new `com.snowflake.connectors.common.object.SchemaName` class for representing the schema; similar behavior to `com.snowflake.connectors.common.object.ObjectName` class.
>   - Added new `com.snowflake.connectors.common.object.InvalidSchemaNameException` class.

#### Other additions and changes

> - Changed `applyToAllInitializedTaskReactorInstances()` method in the `com.snowflake.connectors.taskreactor.TaskReactorInstanceActionExecutor` to execute an action only on initialized task reactor instances. Previous behavior: actions were executed on all registered task reactor instances.

### New features

- Resource management procedures:

  - Introduced new callbacks to the `PUBLIC.CREATE_RESOURCE()` procedure that let you perform custom operations during the procedure flow.
    See also [Create resource](../../developer-guide/native-apps/connector-sdk/flow/ingestion-management/create_resource).
  - New `PUBLIC.ENABLE_RESOURCE()` procedure that enables a disabled resource.
    Additional callbacks let you perform custom operations during the procedure flow.
    See also [Enable resource](../../developer-guide/native-apps/connector-sdk/flow/ingestion-management/enable_resource).
  - New `PUBLIC.DISABLE_RESOURCE()` procedure that disables an enabled resource.
    Additional callbacks let you perform custom operations during the procedure flow.
    See also [Disable resource](../../developer-guide/native-apps/connector-sdk/flow/ingestion-management/disable_resource).
  - New `PUBLIC.UPDATE_RESOURCE()` procedure that updates ingestion configurations of a particular resource.
    Additional callbacks let you perform custom operations during the procedure flow.
    See also [Update resource](../../developer-guide/native-apps/connector-sdk/flow/ingestion-management/update_resource).
- `com.snowflake.connectors.util.sql.SqlTools`:

  - Added `asVarchar()` method that is expected to replace `varcharArgument()` method.
  - Added `asVariant()` method that is expected to replace `variantArgument()` method.
  - Marked `varcharArgument()` and `variantArgument()` methods as deprecated and set them to be removed in the future.
- Other additions:

  - Defined Ingestion Process status as constants in the `com.snowflake.connectors.application.ingestion.process.IngestionProcessStatuses` class.
  - Added `isNotOk()` method to `com.snowflake.connectors.common.response.ConnectorResponse` class.
  - Added `com.snowflake.connectors.util.snowflake.DefaultTransactionManager` class that lets you execute SQL statements within a transaction by using the `withTransaction()` method.
  - Improved logging in the task reactor.

### Bug fixes

- Fixed bug that resulted in removing task reactor instance schema, once unexpected error was raised during `CREATE_INSTANCE_OBJECTS()` procedure.

## Version 2.0.0 (May 24th, 2024)

Initial release.
