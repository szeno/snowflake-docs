# Snowflake Python APIs release notes for 2024

This article contains the release notes for the Snowflake Python APIs, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

See [Snowflake Python APIs: Managing Snowflake objects with Python](/developer-guide/snowflake-python-api/snowflake-python-overview) for documentation.

## Version 1.0.2 (2024-11-13)

### New features and updates

- Removed the `async_req` parameter (asynchronous mode) from the `execute_job` API in the `Service` resource.

### Bug fixes

- None.

## Version 1.0.1 (2024-11-11)

### New features and updates

- Added support for the following new resources:

  - Cortex Chat
  - Cortex inference
- Added support for customized user agents.

### Bug fixes

- Fixed the `ValueError` message for `Enum` types.
- Fixed the API documentation for `Enum` types to show possible values.
- Added the missing `DeleteMode` type to the API documentation.

## Version 1.0.0 (2024-10-22)

Initial general availability release.

### New features and updates

- Improved error messages by shortening stack traces. To control this behavior, use the `_SNOWFLAKE_PRINT_VERBOSE_STACK_TRACE`
  environment variable option.
- Now includes read-only properties by default in dictionaries returned by `to_dict()` from models. To toggle this option, use
  `to_dict (hide_readonly_properties=True)`.
- Added the `if_exists` property, which toggles whether you can perform an action without erroring if the given resource does not
  exist, to the following methods and resources:

  - `drop()` for `Database`, `NetworkPolicy`, `View`, `User`, `ComputePool`, `ImageRepository`,
    `Pipe`, `Role`, `Service`, `Stage`, `Table`, `Task`, `DynamicTable`, `Role`,
    `Alert`, `Procedure`, `Warehouse`, `Schema`, and `Function`.
  - `refresh()` for `Database` and `DynamicTable`.
  - `suspend()` and `resume()` for `Service`, `DynamicTable`, and `Warehouse`.
  - `suspendRecluster()` and `resumeRecluster()` for `DynamicTable` and `Table`.
- `Database` now supports the `undrop()` method.
- `Service` now supports the `from_name` parameter in `iter()`.
- `Table` now supports the `target_database` and `target_schema` parameters in `swap_with()`.
- `Procedure` now supports the `copy_grants` parameter in `create()`.

### Bug fixes

- Creating dynamic tables now properly allows cloning source objects from different databases and schemas.
- Fixed an SSL connection issue for accounts and organizations with underscores when used in hostnames.

## Version 0.13.1 (2024-10-11)

### New features and updates

- Added support for the database role resource.
- Added new methods to the role, database role, and user resources to manage access privileges.
- Improved logs with secrets scrubbed.

### Bug fixes

- None.

## Version 0.13.0 (2024-10-04)

### New features and updates

- Improved the API documentation significantly.
- Removed `snowflake-snowpark-python` as a dependency of `snowflake.core`. However, this package is still required for some
  features, such as task graph (DAG) concepts; the check and requirement for these features is performed at runtime.
- Added support for all Python versions 3.8 or newer.
- Added support for `targetDatabase` and `targetSchema` for cloning tables.
- Added support for `targetDatabase` for cloning Schemas.
- Exposed type definitions.
- Added support for `execute_job` in `ServiceCollection`.
- Added support for `get_containers`, `get_instances`, and `get_roles` in `ServiceResource`.
- Added support for `create_or_update` in `Service` and `ComputePool`.
- Added support for the following new resources:
  - Account
  - Alert
  - Catalog integration
  - Event table
  - External volume
  - Managed account
  - Network policy
  - Notebook
  - Notification integration
  - Pipe
  - Procedure
  - Stream
  - User defined functions
  - View

### Bug fixes

- Fixed a bug relating to the logging of URLs, where not all the URL pieces were injected into logging.

## Version 0.12.1 (2024-08-29)

### New features and updates

- None.

### Bug fixes

- Fixed multiple issues related to handling large results.

## Version 0.12.0 (2024-08-20)

### New features and updates

- The client now retries requests on retryable error codes.
- The following `StageResource` methods are now deprecated and have been renamed. The old method names are now aliases.
  - From `upload_file` to `put`.
  - From `download_file` to `get`.

## Version 0.11.0 (2024-07-25)

### New features and updates

Note

The following new features require the Snowflake version 8.27 release.

- Added client logging to the library to enhance debug ability.
- Added `undrop` support to the `DynamicTable`, `Schema`, and `Table` object types.
- Enhanced support for the `Grant` object type with the following limitations:

  - The SQL command SHOW GRANTS ON is not supported.
  - Only `Grantees.role` is supported as the grantee value for the `Grants.to` method (SHOW GRANTS TO).
- To be more consistent with their equivalent SQL commands, the following methods are now deprecated and have been renamed as follows. The
  old method names are now aliases that call the new method names, so the old method names will still work as expected.

  - From `create_or_update` to `create_or_alter`.
  - From `delete` to `drop`.
  - From `undelete` to `undrop`.

### Bug fixes

- Fixed a bug in stored procedure generated code.

## Version 0.10.0 (2024-06-24)

### New features and updates

Note

The following new features are dependent on the release of Snowflake version 8.23.

- Added API support for the following resources:

  - `DynamicTable`
  - `Function` (Currently supports service functions only)
  - `Grant`
- Added support for finalizers in tasks and task graphs (DAGs).

## Version 0.9.0 (2024-06-10)

### New features and updates

- Added API support in *experimental* mode for the following resources:

  - `User`
  - `Role`
  - Management `Stage`
- Re-added `create_or_update` support for the `Warehouse`, `Schema`, and `Database` resources.

  Note

  The `create_or_update` feature for these resources requires the upcoming release of Snowflake version 8.23, which is currently
  unreleased as of June 10, 2024.
- Added the `get_endpoints` method for `Service` resources that returns a list of endpoints for a given `Service` object.

### Bug fixes

- `with_managed_access` is now properly returned as a property of `SchemaResource`.

## Version 0.8.1 (2024-05-31)

### New features and updates

- Added the `with_managed_access` Boolean option in `create_or_update` for `SchemaResource`. This option is equivalent to
  the WITH MANAGED ACCESS optional parameter in [CREATE SCHEMA](/sql-reference/sql/create-schema).

  - Usage example:

    Copy code

    ```
    schema.create_or_update(schema_def, with_managed_access = True)
    ```
- Added the `get_endpoints` method for `Service` resources that returns a list of endpoints for a given `Service` object.

## Version 0.8.0 (2024-04-30)

### Behavior changes

- Removed the `deep` parameter from `fetch()` on `TableResource` objects. `fetch()` always returns detailed
  columns and constraints information of a `TableResource`.
- `create_or_update()` currently no longer works for `Schema`, `Warehouse`, `Database`, and `ComputePool`
  resources. `create()` does work for these resources.
- Creating tables using `as_select` no longer carries over information from any source tables used in the `as_select` query.
- The `data_retention_time_in_days` and `max_data_extension_time_in_days` properties of a table are inherited from schema or
  database settings when not explicitly set in a `create_or_update` statement that alters an existing table.

### New features and updates

- Added support for the Cortex Search API endpoint.
- Added support for large results.
- Added support for long-running queries.
- Added the `ServiceSpec` helper function to infer the specification type from a provided string in `Service` resources.
- Updated to use the Snowflake API REST platform for all resources.
- `pip install snowflake[ml]` installs `snowflake-ml-python` v1.4.0.

### Bug fixes

- Various bug fixes.

## Version 0.7.0 (2024-03-20)

Version 0.7.0 introduces updates across the `snowflake` and `snowflake.core` packages.

### New features and updates

`snowflake` package updates:

- You can now run `pip install snowflake[ml]` to install the [Snowpark ML](https://pypi.org/project/snowflake-ml-python/) library
  as an extra package dependency.

`snowflake.core` package updates:

- Task predecessors now return their fully qualified name.
- Added the `__str__()` and `__repr_html__()` methods to `DAGRun` to make it notebook compatible.
- Replaced “DAGs” with “task graphs” in the API reference documentation to better align with Snowflake documentation.

### Bug fixes

`snowflake.core` package fixes:

- Fixed code generator and updated OpenAPI-spec driven models.
- Fixed Pydantic compatibility issues.
- Fixed a bug in the `Task.error_integration` property.
- Fixed a bug in the `Task.config` property when the REST property was missing.

## Version 0.6.0 (2024-02-06)

### New features and updates

- The `>>` and `<<` operators of `DAGTask` now accept a function directly.
- `DAGTask` now uses the DAG’s warehouse by default.
- `DAGTask` accepts a new parameter `session_parameters`.
- Updated `TaskContext`:

  - The method `get_predecessor_return_value` now works for both long and short names of a `DAGTask`.
  - Added the methods `get_current_task_short_name` and `get_task_graph_config_property`.
- Added support for pydantic 2.x.
- Added support for Python 3.11.

### Bug fixes

- Fixed a bug where `DAGOperation.run()` raised an exception if the DAG doesn’t have a schedule.
- Fixed a bug where deleting a DAG didn’t delete all of its sub-tasks.
- Fixed a bug that raised an error when a DAG’s `config` is set.
