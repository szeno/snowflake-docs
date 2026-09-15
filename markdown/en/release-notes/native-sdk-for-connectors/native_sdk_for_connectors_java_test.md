# Native SDK for Connectors Java Test - release notes

Release notes for Native SDK for Connectors Java test library.

## Version 2.2.0 (December 10th, 2024)

### General changes

- Replaced the SnowSQL tool with new Snowflake CLI tool
- Updated Java dependencies

### Behavior changes

- `com.snowflake.connectors.application.scheduler.CreateSchedulerHandlerTestBuilder`:

  - Renamed `withSchedulerCreator(SchedulerCreator)` method to `withSchedulerManager(SchedulerManager)`.
- `com.snowflake.connectors.application.scheduler.InMemoryDefaultSchedulerCreator`:

  - Renamed class to `InMemoryDefaultSchedulerManager`.
- `com.snowflake.connectors.taskreactor.commands.queue.InMemoryCommandsQueueRepository`:

  - Renamed class to `InMemoryCommandsQueue`.

### New features

- New test builders for various handlers that let you fully customize objects used by handler classes:

  - Added `com.snowflake.connectors.application.configuration.reset.ResetConfigurationHandlerTestBuilder`.
- `com.snowflake.connectors.application.lifecycle.pause.PauseConnectorHandlerTestBuilder`:

  - Added `withSchedulerManager(SchedulerManager)` method.
- `com.snowflake.connectors.application.lifecycle.resume.ResumeConnectorHandlerTestBuilder`:

  - Added `withSchedulerManager(SchedulerManager)` method.
- Added new assertion classes:

  - `com.snowflake.connectors.common.assertions.ingestion.IngestionConfigurationAssert` for asserting objects of `com.snowflake.connectors.application.ingestion.definition.IngestionConfiguration` class.
  - `com.snowflake.connectors.common.assertions.UUIDAssertions` for asserting String representations of UUIDs.
- `com.snowflake.connectors.common.assertions.task.TaskPropertiesAssert`:

  - Added `hasPredecessors(List<TaskRef>)` assertion.
- `com.snowflake.connectors.common.assertions.ingestion.IngestionRunAssert`:

  - Added `hasIdAsUUID()` assertion.
  - Added `hasIngestionConfigurationIdAsUUID()` assertion.
  - Added `hasIngestionProcessIdAsUUID()` assertion.
  - Added `hasStartedAt()` assertion.
  - Added `hasCompletedAt()` assertion.
  - Added `hasCompletedAtAfterStartedAt()` assertion.
  - Added `hasIngestedRowsGreaterThan(int)` assertion.
  - Added `hasUpdatedAt()` assertion.
  - Added `hasMetadata()` assertion.
  - Added `hasCompletedState()` assertion.
- Added new classes for use in integration testing:

  - `com.snowflake.connectors.common.SharedObjects`.
  - `com.snowflake.connectors.common.PathResolver`.
  - `com.snowflake.connectors.common.procedure.ProcedureDescriptor`.
  - `com.snowflake.connectors.common.procedure.ProcedureProperties`.

### Bug fixes

- `com.snowflake.connectors.application.ingestion.process.InMemoryIngestionProcessRepository`:
  - Provided an implementation of `endProcess(String, String, String)` method, instead of throwing `UnsupportedOperationException`.

## Version 2.1.0 (July 8th, 2024)

### Behavior changes

- Removed `com.snowflake.connectors.taskreactor.InMemoryConfiguredTaskReactorExistenceVerifier` class.
- Removed `com.snowflake.connectors.taskreactor.InMemoryNotConfiguredTaskReactorExistenceVerifier` class.
- Removed `com.snowflake.connectors.application.common.task.InMemoryTaskRepository` class.

### New features

- New test builders for various handlers that let you fully customize objects used by handler classes:

  - Added `com.snowflake.connectors.application.ingestion.create.CreateResourceHandlerTestBuilder`.
  - Added `com.snowflake.connectors.application.ingestion.enable.EnableResourceHandlerTestBuilder`.
  - Added `com.snowflake.connectors.application.ingestion.disable.DisableResourceHandlerTestBuilder`.
  - Added `com.snowflake.connectors.application.ingestion.update.UpdateResourceHandlerTestBuilder`.
  - Added `com.snowflake.connectors.application.scheduler.CreateSchedulerHandlerTestBuilder`.
- New in-memory implementations:

  - Added `com.snowflake.connectors.application.scheduler.InMemoryDefaultSchedulerCreator`.
  - Added `com.snowflake.connectors.application.configuration.connector.InMemoryConnectorConfigurationService`.
  - Added `com.snowflake.connectors.application.status.InMemoryConnectorStatusRepository`.
  - Added `com.snowflake.connectors.application.status.InMemoryConnectorStatusRepository`.
  - Added `com.snowflake.connectors.taskreactor.InMemoryTaskManagement`.
  - Added `com.snowflake.connectors.util.snowflake.InMemoryAccessTools`.
  - Added `com.snowflake.connectors.util.snowflake.InMemoryTransactionManager`.
- Added new assertions in `com.snowflake.connectors.common.assertions.NativeSdkAssertions`:

  - Added `com.snowflake.connectors.common.assertions.task.CommandAssert` for asserting objects of `com.snowflake.connectors.taskreactor.commands.queue.Command` class.
  - Added `com.snowflake.connectors.common.assertions.common.object.ObjectNameAssert` for asserting objects of `com.snowflake.connectors.common.object.ObjectName` class.
  - Added `com.snowflake.connectors.common.assertions.common.object.SchemaNameAssert` for asserting objects of `com.snowflake.connectors.common.object.SchemaName` class.
  - Added `com.snowflake.connectors.common.assertions.common.object.ReferenceAssert` for asserting objects of `com.snowflake.connectors.common.object.Reference` class.
- `com.snowflake.connectors.common.assertions.ingestion.definition.ResourceIngestionDefinitionAssert`:

  - Added `isEnabled()` method.
  - Added `isDisabled()` method.
- `com.snowflake.connectors.common.assertions.common.response`:
  :   - Added `hasAdditionalPayload()` method.

## Version 2.0.0 (May 24th, 2024)

Initial release.
