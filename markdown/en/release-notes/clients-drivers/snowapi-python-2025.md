# Snowflake Python APIs release notes for 2025

This article contains the release notes for the Snowflake Python APIs, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

See [Snowflake Python APIs: Managing Snowflake objects with Python](/developer-guide/snowflake-python-api/snowflake-python-overview) for documentation.

## Version 1.10.0 (Dec 8, 2025)

### New features and updates

- Added support for the Streamlit resource.
- Added support for the DECFLOAT data type.

### Bug fixes

None.

## Version 1.9.0 (Nov 13, 2025)

### New features and updates

- Added support for the following resources:
  - Artifact repository
  - Network rule
  - Password policy
  - Secret
  - Sequence
  - Tag

### Bug fixes

None.

## Version 1.8.0 (Sep 22, 2025)

### New features and updates

- Added support for proxy configuration. You can provide proxy settings by using the `HTTPS_PROXY` environment variable.

### Bug fixes

None.

## Version 1.7.0 (Jul 31, 2025)

### New features and updates

- Added support to the following methods for specifying the point-of-time reference when you use Time Travel to create streams:
  - `PointOfTimeStatement`
  - `PointOfTimeStream`
  - `PointOfTimeTimestamp`

### Bug fixes

- Fixed a warning: `'allow_population_by_field_name' has been renamed to 'validate_by_name'`.
- Restored the behavior of the `drop` method of `DAGOperation` such that `drop_finalizer` must be set to `True` before
  the finalizer task is dropped.

  As a result of changes in the 9.20 Snowflake release, `fetch_task_dependents` started returning the finalizer task alongside other
  tasks that belong to the Directed Acyclic Graph (DAG). This behavior caused the `drop` method to always drop the finalizer.

## Version 1.6.0 (Jun 26, 2025)

### New features and updates

- Optionalized the `query` and `column` parameters in `QueryRequest` for the Cortex Search service API.

### Bug fixes

None.

## Version 1.5.1 (May 28, 2025)

### New features and updates

None.

### Bug fixes

- Fixed a bug in `ProcedureResource` that caused the `call` method to return wrong results when using the `extract`
  option with the `ReturnTable` type.
- `CortexInferenceService.complete` can now be called from Python worksheets and notebooks.

## Version 1.5.0 (May 14, 2025)

### New features and updates

- Deprecated the `ServiceResource.get_service_status` method in favor of the `ServiceResource.get_containers` method.
- Added the `extract` option to the `procedure.call` method. Enabling this option causes the method to extract results from the
  returned payload.

  For example, setting `extract=False` (current default behavior) returns a result such as `[{'procedure_name': 42}]`. In this
  example, you can set `extract=True` to return the value `42`.

  Note

  `extract=False` remains the current default setting but now returns a deprecation warning. The recommendation is to switch to using
  `extract=True`, which will become the new default in the next major release.
- Added support for mapping the VARIANT type in a stored procedure call.

### Bug fixes

- Fixed the type mapping for the GEOMETRY, GEOGRAPHY, OBJECT return types in stored procedures.
- The `__repr__` implementation for stored procedures and functions now shows a list of arguments in addition to the name.

## Version 1.4.0 (Apr 23, 2025)

### New features and updates

- Implemented the `__repr__` method for all collection, resource, and model classes.

### Bug fixes

- Changed the `_SNOWFLAKE_PRINT_VERBOSE_STACK_TRACE` environment variable to be enabled by default, which causes printed error messages
  to display the full stack trace.

  This change was made to avoid disabling stack traces for all exceptions, which happens when `SNOWFLAKE_PRINT_VERBOSE_STACK_TRACE` is
  not set.

## Version 1.3.0 (Apr 9, 2025)

### New features and updates

- Added the `snowflake.core.FQN` class, which represents an object identifier.
- The `DAGOperation.drop` method drops the finalizer task associated with the DAG if the `drop_finalizer` argument is set to `True`.

  Important

  The `drop_finalizer` argument will be removed in the next major API release, and the `DAGOperation.drop` method will always
  drop the associated finalizer task along with the DAG.

### Bug fixes

None.

## Version 1.2.0 (Mar 26, 2025)

### New features and updates

- Added support for asynchronous requests across all of the existing endpoints.

  Asynchronous methods are denoted by the `_async` suffix in their names and use polling to determine whether an operation was completed.

  The number of calls that can execute in parallel depends on the number of CPUs. To change the size of the thread pool, use the `_SNOWFLAKE_MAX_THREADS` environment variable.

  For example usage, see the [snowflake.core.PollingOperation](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.PollingOperation) class documentation.
- Added support for creating serverless tasks using the `StoredProcedureCall` definition.
- Added support for the SERVERLESS\_TASK\_MIN\_STATEMENT\_SIZE and SERVERLESS\_TASK\_MAX\_STATEMENT\_SIZE serverless attributes to the
  `Database` and `Schema` resources (dependent on Snowflake version 9.8).
- Added support for setting the SUSPEND\_TASK\_AFTER\_NUM\_FAILURES, USER\_TASK\_MANAGED\_INITIAL\_WAREHOUSE\_SIZE, and USER\_TASK\_TIMEOUT\_MS
  attributes on cloned databases and schemas (dependent on Snowflake version 9.8).
- Deprecated `CortexAgentService.Run` in favor of `CortexAgentService.run`.
- Added new optional attributes to various models within the Cortex Search service API:

  - `text_boosts` and `vector_boosts` to the `Function` model
  - `weights` to the `ScoringConfig` model

### Bug fixes

- You can now call `create_or_alter` with a task object returned from the `iter` method.

## Version 1.1.0 (Mar 12, 2025)

### New features and updates

- Added support for the TARGET\_COMPLETION\_INTERVAL, SERVERLESS\_TASK\_MIN\_STATEMENT\_SIZE, and SERVERLESS\_TASK\_MAX\_STATEMENT\_SIZE serverless
  attributes to the Task resource.
- Added support for the following new resources:
  - API integrations
  - Iceberg tables (dependent on Snowflake version 9.6)

### Bug fixes

None.

## Version 1.0.5 (Feb 19, 2025)

### New features and updates

- Removed the `protobuf` dependency from `snowflake.core`.

### Bug fixes

None.

## Version 1.0.4 (Feb 13, 2025)

### New features and updates

- Added support for the Cortex Lite Agent resource.

### Bug fixes

None.

## Version 1.0.3 (Feb 4, 2025)

### New features and updates

- Added support for the Cortex Embed resource.

### Bug fixes

None.
