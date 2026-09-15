# Snowflake Python APIs release notes for 2026

This article contains the release notes for the Snowflake Python APIs, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

See [Snowflake Python APIs: Managing Snowflake objects with Python](/developer-guide/snowflake-python-api/snowflake-python-overview) for documentation.

## Version 1.13.1 (Aug 12, 2026)

### New features and updates

- **Code Bundle API:**
  - Added typed `BundleSpec` and `CodeBundleSpecification` models for code bundles and code bundle executions.
  - Added `iter()` support for code bundle executions.
- **Dynamic Table API:**
  - Added `initialization_warehouse`, `frozen_where`, `backfill_from`, `default_ddl_collation`, `log_level`, `row_timestamp`, `cluster_by_raw`, and `start_at` fields to `DynamicTable`.
  - Added `DataMetricSchedule`, `DataMetricCronSchedule`, `DataMetricMinutesSchedule`, and `DataMetricTriggerOnChangesSchedule` models for data metric scheduling.
  - Extended `refresh_mode` with `ADAPTIVE` and `CUSTOM_INCREMENTAL` values.

### Bug fixes

- None.

## Version 1.13.0 (Aug 10, 2026)

### New features and updates

- **Task and DAG APIs:**
  - Added `condition` parameter to `DAG` to support setting a WHEN condition on the root task.
  - Added the `recursive` argument to `TaskResource.fetch_task_dependents`.
  - Added support for defining task schedules and target completion intervals at a granularity of seconds, including intervals under a minute.
  - Added `overlap_policy` on `Task` and on the `DAG` root task.
  - Added `success_integration` and `execute_as_user` on `Task` and `DAGTask`.
- **Code Bundle API:**
  - Added support for managing code bundles through `root.databases[<db>].schemas[<schema>].code_bundles` (create, iterate, fetch, add a version, execute, and drop).
  - Added support for code bundle executions through `root.code_bundle_execution` (execute a code bundle from a stage location, and fetch the status of or cancel an execution).
  - Added the `_SNOWFLAKE_SKIP_ASYNC_EXEC_POLLING` environment variable. When set to `true`, a request submitted with `asyncExec=true` that receives a `202 Accepted` response returns that accepted response (carrying the job id) immediately, instead of polling the execution to completion. Transient-error retries, for example, 429/503/504, are unaffected.

### Bug fixes

- `copy.copy`, `copy.deepcopy`, and pickling of `IntervalSchedule` and `TargetCompletionInterval` now work; previously they would raise an exception.
- **Security improvements** - for more information, see [CVE-2026-19594](https://www.cve.org/CVERecord?id=CVE-2026-19594):
  - Improved validation of path parameters; values consisting solely of dot-segments (`.` or `..`) now raise a clear `ValueError`.
  - Improved encoding of URL query parameters; resource names containing special characters, such as `&`, `=`, or `#`, are now percent-encoded correctly, preventing failures on rename, swap, and clone operations for resources whose names include such characters.
  - Fixed `DagRun._repr_html_()` to correctly escape special characters in property values.
  - Improved validation of single-quoted string literals used in stage paths; strings with unescaped embedded quotes are no longer incorrectly treated as valid.
  - Improved sanitization of stage path values; backslash sequences immediately preceding a single quote are now doubled.

## Version 1.12.1 (Jun 10, 2026)

### New features and updates

- None.

### Bug fixes

- Proxy configuration through environment variables now honors both the uppercase `HTTPS_PROXY` and the lowercase `https_proxy` variable.
- The CA bundle used for TLS verification now honors the `SSL_CERT_FILE` environment variable (both uppercase `SSL_CERT_FILE` and lowercase `ssl_cert_file`), allowing connections through corporate proxies with a custom trust store.

## Version 1.12.0 (Feb 12, 2026)

### New features and updates

- Added support for setting (`set_tags`), unsetting (`unset_tags`), and fetching tag assignments (`get_tags`).
  Tagging support for specific resources is introduced in the following Snowflake server releases:
  - **10.3**: Alert, database, database role, dynamic table, event table, image repository, network policy, notebook, password policy, pipe,
    procedure, role, schema, stream, table, task, user, user-defined function, view, warehouse.
  - **10.4**: API integration, catalog integration, compute pool, function, iceberg table, notification integration, Streamlit.

### Bug fixes

- None.

## Version 1.11.0 (Jan 21, 2026)

### New features and updates

- The `DAGTask` object type now accepts custom objects with a `to_sql()` method as task definitions.
- The `UserDefinedFunction` object type now supports executing scalar UDFs using the `execute` method.

### Bug fixes

- Creating, fetching, and listing stored procedures that use a staged handler (where the `body` property is empty) no longer raises a `ValidationError`.
- Pydantic deprecation warnings related to `class-based config` and the `update_forward_refs`, `parse_obj`, and `_iter` methods no longer occur.
