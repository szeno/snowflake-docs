# Snowflake CLI release notes for 2026

This article contains the release notes for the Snowflake CLI, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

See [Snowflake CLI](/developer-guide/snowflake-cli/index) for documentation.

## Version 3.26.0 (Aug 31, 2026)

### New additions

- `snow connection test --enable-diag` now appends [SnowCD](https://docs.snowflake.com/en/user-guide/snowcd)-style per-endpoint connectivity checks (health, latency, certificate info, and an effective network policy summary) to the existing `SnowflakeConnectionTestReport.txt`. Stdout is unchanged. Pass `--print-diag` with `--enable-diag` to print that same report to stdout. Replaces the end-of-life SnowCD tool.
- `app.yml` (version 2) for Snowflake App Runtime projects is now generally available, and no longer needs a feature flag. `snow app setup` creates an `app.yml` for new projects. Existing `snowflake.yml` projects keep working as before.
- Git metadata support for `snow dbt deploy` is now available. `--git-commit` and `--git-branch` record the source commit and branch in the project’s `last_deployed_from` metadata. These values will also be auto-detected from GitHub Actions environments if no explicit flags are specified.

### Fixes and improvements

- `snow app deploy` for Snowflake App Runtime projects now explains a failure while preparing code storage in terms of the statement that actually failed. A missing database or schema is reported as such instead of as a missing privilege, a privilege error names only the grant that statement needs, and a rejected stage encryption type is named explicitly.
- `snow app deploy` for Snowflake App Runtime projects no longer surfaces a raw connector traceback when uploading code fails. The error now names the stage or workspace being written to, how many files had already uploaded, and what to do next. Failed file transfers, which were previously not caught at all, are reported the same way.
- `snow helpers detect-encoding` now detects when the Windows console isn’t configured for UTF-8 output (independent of the CLI’s own encoding settings) and points the user at the fix — `chcp.com 65001` for cmd.exe/Git Bash, or the docs for PowerShell 5.x. The CLI’s startup encoding warning surfaces the same note, but only when it isn’t already warning about a Python encoding mismatch — run `snow helpers detect-encoding` for the full picture.
- `snow app deploy` for Snowflake App Runtime projects no longer needs OWNERSHIP on the code stage and CREATE STAGE on the schema to redeploy. The upload used to start by dropping the stage and creating it again, so a role holding only WRITE could deploy once and then never again — and a role allowed to drop the stage but not create one lost the stage entirely. The stage is now only dropped when the deploying role can also recreate it; otherwise its contents are cleared, with a warning that files deleted from the project since the last deploy may survive on the stage.
- Snowflake App Runtime projects now use temporary code storage by default. `snow app setup` leaves `code_stage`/`code_workspace` out of `app.yml`, and `snow app deploy` provisions a temporary `<app>_CODE` stage (or a `<app>_CODE` workspace for personal databases, which don’t support stages) just for the build and drops it once the build finishes. Because the name is derived from the app, `--build-only` can still find and drop what `--upload-only` created. Set `code_stage` or `code_workspace` in `app.yml` to keep a persisted stage/workspace instead.
- Fixed `snow helpers check-version` failing with “Could not determine the latest Snowflake CLI version” when the local version cache file was corrupted. A corrupted or unreadable cache now falls back to a live network fetch instead of silently returning nothing.
- The passive new-version banner no longer blocks CLI startup. The version cache is refreshed in a background thread while the command runs, and the banner is shown after the command completes (including on `--help`, `--version`, and `--info`).

## Version 3.25.0 (Aug 24, 2026)

### New additions

- `snow connection add` now supports `--client-store-temporary-credential`, which writes `client_store_temporary_credential = true` to the new connection in `config.toml`.
- `snow sql --local-only` default can now be set via the `SNOWFLAKE_CLI_SQL_LOCAL_ONLY` environment variable. When unset, the default remains `false`.
- `snow app events` now accepts `--instance <N>` (Snowflake App Runtime only) to retrieve live container logs from a specific service instance. Useful when horizontal scaling is active and more than one instance is running. Defaults to instance 0 when the flag is omitted.
- The `snow app` commands now support an `app.yml` (version 2) for Snowflake App Runtime projects; when present it drives the flow instead of `snowflake.yml` (the Native App flow is unchanged). Its `targets` block declares named per-environment deployments, and a new `--target` flag on `deploy`, `open`, `events`, `teardown`, and `validate` selects which one to use. `snow app deploy` runs an upload, build, and deploy pipeline, in that order, that can be limited to a single phase with `--upload-only`, `--build-only`, or `--promote-only`.
- `dbt_projects_profiles.yml` support in `snow dbt deploy` is now generally available. When the profiles directory contains a `dbt_projects_profiles.yml`, it takes precedence over `profiles.yml` and is staged into the deployed project under its own name. The profiles directory is the one given by `--profiles-dir`, or the project root when that option is omitted, so projects that already contain a `dbt_projects_profiles.yml` alongside `profiles.yml` will now deploy with the former and emit a warning.

### Fixes and improvements

- A `snow app` command no longer fails because it could not clean up after itself. If a leftover file cannot be deleted (common on Windows, where an editor or antivirus can be holding it), the command still succeeds and warns which directory was left behind. When the bundle directory cannot be cleared before bundling, the command now stops with an explanation of what to do instead of a permissions error.
- `snow app` commands no longer delete anything in a Snowflake App Runtime project’s `output` directory apart from the bundle they created there. A project that keeps its own build results, exports or notebook output under `output` lost them to a command that only meant to bundle.
- `snow app events` for Snowflake App Runtime projects can now return more events by requesting a higher `--last` value.
- `snow app deploy` with workspace-backed storage now builds from `versions/live/` (the current working state) instead of the last committed version. In the Workspaces editor, files auto-save to the live version continuously; reading `versions/last` during the build phase caused stale content to be deployed when running from a live workspace session.
- DCM projects: the `snow dcm preview`, `snow dcm refresh`, and `snow dcm test` commands are not yet generally available. They are now hidden from `--help` unless the `enable_dcm_preview_features` CLI feature flag is enabled, so they no longer appear in `snow dcm --help` without an explicit opt-in.
- `snow dcm plan` now tracks the server’s own progress, like `snow dcm deploy` already does: its `RENDER`, `COMPILE` and `PLAN` steps advance as the backend reports each phase. Previously `RENDER` and `COMPILE` completed instantly and the rest of the run showed as a single `PLAN` spinner.
- `snow dcm deploy`, `snow dcm plan` and `snow dcm purge` no longer require an active warehouse. Progress tracking read the result with `RESULT_SCAN`, which requires a warehouse.
- `snow dcm deploy`, `snow dcm plan` and `snow dcm purge` now wrap a change line too wide for the terminal, with its continuation aligned under the change instead of breaking back to the left margin. The file list shown while uploading uses the same tree guides as the changeset.
- `snow streamlit deploy --replace`: fixed a crash when replacing a legacy `ROOT_LOCATION` Streamlit app with a versioned deployment.
- Upgraded `GitPython` from 3.1.57 to 3.1.58.
- Upgraded the Python interpreter embedded in Linux binaries from 3.10.16 to 3.10.21.
- Upgraded pip from 26.1.2 to 26.2.1.

## Version 3.24.1 (Aug 06, 2026)

### Bug fixes

- The `--env-file` (`-e`) option for `snow dcm deploy`, `snow dcm plan`, and `snow dcm preview` is not yet generally available. It is now hidden from `--help` output unless the `enable_dcm_project_env_vars` feature flag is enabled. This corrects a bug introduced in version 3.24.0 where the option was visible without requiring any opt-in.

## Version 3.24.0 (Aug 04, 2026)

### Breaking changes

- `snow app` commands for Snowflake App Runtime projects now always operate on `APPLICATION SERVICE` objects and no longer fall back to SPCS `SERVICE` objects. Apps still deployed as legacy SPCS services are no longer supported by these commands.

### New features and updates

- `snow dcm` commands are now generally available. The `snow dcm preview` and `snow dcm test` commands remain in public preview.
- Added `--delta` to `snow dcm plan` to process only statements changed since the last deployment, plus statements potentially impacted by those changes.
- `snow dcm deploy`, `snow dcm plan`, and `snow dcm preview` now support environment variables and secrets declared in a project manifest’s `templating.env_vars` and `templating.env_secrets` sections. Declared values are collected from the shell environment, or from a `.env` file passed with `--env-file` (`-e`). When a name is declared in both, the shell value wins. Values are forwarded to the server. This capability isn’t generally available yet; enable the `enable_dcm_project_env_vars` feature flag to use it. For more information, see version 3.24.1.
- `snow dcm deploy`, `snow dcm purge`, `snow dcm plan`, `snow dcm preview`, and `snow dcm test` now show live, per-step progress as an interactive checklist instead of a single generic spinner.
- `snow dcm` commands now summarize uploaded files as a tree beneath the upload step, instead of listing every file on its own line.
- `snow dcm plan`, `snow dcm deploy`, and `snow dcm purge` now render each altered object’s changes as an indented tree, showing added, modified, and removed columns, constraints, grants, and other properties with previous and new values, instead of only the object name. Long or multi-line values are collapsed to a single line.
- `snow dcm` commands run with `--save-output` now write artifacts directly into the `out/` directory, with each command’s response in `out/<command>_result.json`, instead of nesting them under a per-command subdirectory. The `out/` directory is recreated empty at the start of every such run.
- Recursive stage uploads now upload directories concurrently instead of one at a time. This applies to every command that uploads a directory tree to a stage (for example, `snow stage copy --recursive`, `snow dcm deploy`, `snow dcm plan`, `snow dbt deploy`, and `snow spcs service build-image`). Total upload concurrency is bounded by the `SNOWFLAKE_CLI_STAGE_UPLOAD_WORKERS` setting (config key `cli.stage_upload_workers`, default 16; set to 1 to restore the previous serial behavior). For `snow stage copy`, this budget is shared with `--parallel` rather than multiplied by it, so existing invocations don’t spawn more threads than before.
- Added the `snow spcs service remote-build`, `remote-build-status`, and `remote-build-history` commands to submit and track SPCS image and app builds through the remote build REST API. These commands are hidden by default and gated by the `enable_spcs_remote_build` CLI feature flag.
- Added optional `--validation-profile` to `snow spcs service remote-build` (for example, `ML_JOB`, `NOTEBOOK`). The value is forwarded as `validation_profile` on `POST /api/v2/remote-build/execute` so the image builder can select a pre-baked validation ruleset. When omitted, no image validation is requested. Ignored for `--build-type app`.
- Added the `snow helpers check-version` command to report the installed Snowflake CLI version alongside the latest published version and whether an upgrade is available. Use `--refresh` to bypass the local cache and query PyPI/Homebrew directly.
- Added the `snow dbt copy` command to copy files between a local directory and a stage, or between stages, for a dbt project. It’s an alias of `snow stage copy` and supports the same options (`--recursive`, `--overwrite`, `--parallel`, `--auto-compress`, `--refresh`).
- `snow app events` now surfaces app health telemetry for Snowflake App Runtime projects. Use `--type log|metric|lifecycle` to select the telemetry stream (default `log`). The `--since` and `--until` options for Snowflake App Runtime projects now accept relative shorthand (for example, `30m`, `6h`, `2d`) or absolute UTC timestamps, and switch logs to the historical event table. Use `--metric cpu|memory|network` to narrow metric output and `--raw` to emit unconverted values.
- Upgraded `GitPython` from 3.1.50 to 3.1.57.
- `snow app` commands (`validate`, `open`, `events`, `deploy`, `teardown`) now resolve their database and schema from the active connection like other CLI commands, so a bare `USER$` database configured in `snowflake.yml` is expanded to the caller’s personal database.

### Bug fixes

- A `USER$` database resolved from the active connection is now expanded to the caller’s personal database (`USER$<username>`) when the connection specifies a username.
- `snow app setup` and `snow app deploy` now default to a workspace for code storage on all databases, falling back to a stage if a workspace can’t be used.

## Version 3.23.0 (Jul 16, 2026)

### New features and updates

- `snow spcs service events` is now generally available. The command now returns service-level and service-instance-level platform events in addition to container-level events. The `--container-name` and `--instance-id` filters are now optional; omit them to retrieve all events for the service.
- Added a `--watch` flag to `snow app open` for Snowflake App Runtime projects. With `--watch`, the command no longer fails when the app service doesn’t exist yet; it polls until the service is created and its endpoint is ready before opening (or printing) the URL.
- `snow app --help` is now context-aware: when the current project’s `snowflake.yml` unambiguously targets one app family (Native Apps or Snowflake App Runtime), the help listing hides the other family’s commands. Hidden commands remain fully runnable, and shell completion reflects the same filtering.
- Upgraded `snowflake-connector-python` from 4.6.0 to 4.7.1.
- Upgraded `snowflake-snowpark-python` from 1.41.0 to 1.53.0.

### Bug fixes

- `snow app deploy` now drops the code stage before recreating it only when the stage already exists. A first deploy no longer issues `DROP STAGE` unnecessarily, which allows a role with only `CREATE STAGE` (and not `OWNERSHIP`) to deploy successfully.

## Version 3.22.1 (Jul 14, 2026)

### Bug fixes

- Fixed `snow streamlit deploy` incorrectly attempting to UNSET schema-inherited governance tags that the deploying role has no APPLY privilege on when re-deploying an app. Omitting the `tags` property from `snowflake.yml` now leaves directly-set tags untouched; use `tags: []` to explicitly clear all directly-set tags.

## Version 3.22.0 (Jul 07, 2026)

### New features and updates

- Added a `tags` field to the Streamlit entity so that you can set object tags with `snow streamlit deploy`.
- `config.toml` and `connections.toml` files with `0644` permissions (readable by group or others) now emit a warning instead of a hard error when `SF_SKIP_TOKEN_FILE_PERMISSIONS_VERIFICATION=true` or `SKIP_TOKEN_FILE_PERMISSIONS_VERIFICATION=true` is set, aligning with the behavior of `snowflake-connector-python`. Files that are writable by group or others remain a hard error regardless of the environment variable.

### Bug fixes

- `snow app setup` now correctly preserves case-sensitive (double-quoted) identifiers in the generated `snowflake.yml`. Previously, values such as `"lower_db"` were silently stripped of their surrounding quotes, which caused Snowflake to uppercase the identifier and fail to locate the object.
- `snow app setup` no longer writes `build_compute_pool` or `service_compute_pool` to the generated `snowflake.yml`, and no longer reads the `DEFAULT_SNOWFLAKE_APPS_BUILD_COMPUTE_POOL` or `DEFAULT_SNOWFLAKE_APPS_SERVICE_COMPUTE_POOL` account parameters. Snowflake App Runtime services now always run on server-managed compute pools. Existing projects that set these fields in `snowflake.yml` continue to be honored by `snow app deploy`.
- `snow app setup --dry-run` now exits with code 0 while still printing the same setup validation errors that a non-dry-run invocation surfaces.
- `snow app deploy` now supports a separate `service_eai` field on `snowflake-app` entities for newly created application services. When `service_eai` isn’t set, deploy continues to fall back to `build_eai` for backward compatibility.
- `snow dbt deploy` now preserves the original key order in `profiles.yml` instead of reordering keys alphabetically.
- `snow app setup` and `snow app deploy` now resolve their Snowflake App Runtime defaults through the `SYSTEM$GET_APPLICATION_SERVICE_DEFAULTS()` system function, and automatically fall back to the previous `SHOW PARAMETERS`-based resolution on accounts where that function isn’t yet available.
- Fixed `snow app events` and `snow app setup --dry-run` crashing on Windows with an uncaught `UnicodeEncodeError` when their output contained non-ASCII characters (for example, emoji, box-drawing characters, or accented text). The `snow app` commands now render output as UTF-8 instead of the platform default code page.

## Version 3.21.0 (Jun 24, 2026)

### New features and updates

- Added a `cli.encoding` configuration section (and matching `SNOWFLAKE_CLI_ENCODING_*` environment variables) to control text encoding in three areas: `file_io` for reading and writing project files (such as SQL files and `snowflake.yml`), `subprocess` for decoding the output of external processes (such as Docker and pip), and `stdout` for encoding CLI output written to standard output. Setting all three to `utf-8` ensures correct Unicode handling on Windows systems where the platform default encoding isn’t UTF-8. For more information, see [Configuring Snowflake CLI](/developer-guide/snowflake-cli/connecting/configure-cli).
- Added the `snow helpers detect-encoding` command, which shows the encoding configuration for the current environment and flags any discrepancies that could corrupt files when sharing projects across platforms. Run it after an encoding warning to see the full details and recommended remediation steps.
- Added the `--no-prompt-exit-repl` option (and matching configuration setting) to skip the exit confirmation prompt in the SQL REPL.
- Added the `--server-session-keep-alive` global connection option (with the matching `SNOWFLAKE_SERVER_SESSION_KEEP_ALIVE` environment variable and `server_session_keep_alive` configuration key) that prevents Snowflake from closing idle sessions. This is useful for long-running operations or connections held open between multiple operations.

### Bug fixes

- Fixed REST API object operations (for example, `snow object create`) crashing with `ModuleNotFoundError: No module named 'snowflake.connector.vendored'` when running against the Snowflake Universal Driver (connector-python v5). HTTP error handling now works on both connector v4.x and the Universal Driver v5.
- Renamed the `--deploy-only` option of `snow app deploy` to `--promote-only`. The previous `--deploy-only` name continues to work as a hidden alias for now, but this backward compatibility is temporary and will be removed soon.
- The `snow app setup --compute-pool` option and the `build_compute_pool` and `service_compute_pool` fields of a `snowflake-app` entity are now hidden and undocumented (omitted from `--help` and from the generated project-definition JSON Schema). They remain fully functional: `snow app setup` and `snow app deploy` still honor the `DEFAULT_SNOWFLAKE_APPS_BUILD_COMPUTE_POOL` and `DEFAULT_SNOWFLAKE_APPS_SERVICE_COMPUTE_POOL` account parameters and any compute pools configured in `snowflake.yml`.
- `snow streamlit deploy --replace` now uses `ALTER STREAMLIT ... SET` instead of `CREATE OR REPLACE STREAMLIT` when the app already exists, preserving existing grants and permissions on the object.
- `snow app setup` and `snow app deploy` now default to a workspace (instead of a stage) for app code whenever the resolved destination is a personal database (`USER$<user>`), which doesn’t support stages. An explicitly configured `code_stage` is still honored, with a warning when the destination is a personal database.
- `snow app setup` now honors the `--warehouse`, `--database`, and `--schema` connection options as explicit overrides for the generated `snowflake.yml`, taking precedence over account parameters and connection defaults. When you specify `--database`, you must also specify `--schema`.
- The `build_eai` field of a `snowflake-app` entity can now be specified as a bare string (for example, `build_eai: MY_EAI`) in addition to the existing object form.
- Fixed `snow app` commands (for example, `snow app deploy` and `snow app validate`) failing on Windows with a `UnicodeDecodeError` when `snowflake.yml` contained non-ASCII characters. The `snow app` command group now defaults to reading and writing `snowflake.yml` as UTF-8. An explicit `cli.encoding.file_io` setting still takes precedence.
- Fixed `snow app deploy` failing on Windows, and failing when directory names contain glob metacharacters (for example, Next.js dynamic-route directories such as `[id]` or `[...slug]`), by escaping local file paths before they’re passed to `PUT`.
- `snow app deploy` now drops and recreates the code stage before uploading (instead of clearing it with `REMOVE`), uploads app code one file at a time while preserving the directory structure, and uploads files in parallel (up to five at a time).
- `snow dcm` commands now use the system temporary folder to bundle project files before uploading, rather than creating and then dropping an `output` project directory.
- `snow dbt` no longer rejects valid `--dbt-version` values (for example, `2.0.0-preview.175`) that don’t match a hard-coded client-side pattern. Versions are now validated against the server’s supported list.
- Fixed `snow app setup` incorrectly treating system-default parameter values as admin-configured values after running `ALTER ACCOUNT UNSET` on the compute-pool account parameters.
- Upgraded `pip` from 26.1.1 to 26.1.2.

## Version 3.20.0 (Jun 08, 2026)

### New features and updates

- Added the `--protocol` option (with the matching `SNOWFLAKE_PROTOCOL` environment variable and `protocol` configuration key) to `snow connection add` and the global connection overrides. This option selects `http` or `https` as the connection protocol without editing `config.toml`, which is primarily useful for local development against `http` deployments.
- Added the `snow helpers generate-project-schema` command to emit a JSON Schema for the `snowflake.yml` project definition file. The output follows [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema) and can be used by editors (for example, VS Code with the YAML extension) or CI pipelines to get completion and to catch structural mistakes such as unknown keys, wrong types, and missing required fields before a deploy. Use the `--definition-version` option to select the project definition version (`1`, `1.1`, or `2`; the default is `2`) and the `--output-file` (`-o`) option to write the schema to a file.

### Bug fixes

- Fixed `TooManyFilesError` during `snow streamlit deploy` when `main_file` is a descendant of a directory listed in `artifacts`.
- Fixed `snow sql` table output rendering as a series of `|` characters when selecting many columns into a non-terminal destination, for example piped or redirected output.
- Fixed `get_account_identifier()` and `snow spcs service build-image` to raise a clear, user-visible error when `CURRENT_ORGANIZATION_NAME()` or `CURRENT_ACCOUNT_NAME()` returns no row or a NULL value, instead of a cryptic `TypeError` or `AttributeError`.
- `snow dcm list-deployments` and `snow dcm drop-deployment` now wrap the project name in `IDENTIFIER(...)`, matching the other DCM subcommands. Fully qualified and quoted project names are now handled consistently.
- `snow app setup` and `snow app deploy` now verify that the current role can deploy to the account-configured destination (the `DEFAULT_SNOWFLAKE_APPS_DESTINATION_DATABASE` and `DEFAULT_SNOWFLAKE_APPS_DESTINATION_SCHEMA` account defaults) before using it. When the role is missing the required privileges, the commands fall back to your personal database and print a warning that lists the missing grants.
- Updated `snowflake-connector-python` to version 4.6.0.

## Version 3.19.0 (May 26, 2026)

### New features and updates

- Added a `--local-only` option to `snow sql` (and the interactive REPL it launches) that restricts the `!source` and `!load` directives to local SQL files. When set, `!source`/`!load` directives that reference `http://` or `https://` URLs are rejected instead of being fetched. Local file paths are unaffected, and the restriction also applies transitively to nested `!source` directives reached from sourced files. Use this option in environments where SQL inputs should not trigger outbound network requests, or when running SQL files whose content should be reviewed locally before execution.

## Version 3.18.0 (May 20, 2026)

### New features and updates

- Added the `snow streamlit logs` command to stream live logs from a Streamlit-in-Snowflake app running on the SPCSv2 container runtime. Supports `--tail` for historical lines, `--name` to target apps without a project definition, and honors the global `--format` option (plain, JSON, or CSV) for downstream piping.
- Updated `snowflake-connector-python` to version 4.5.0.
- Updated `gitpython` to version 3.1.50.
- Upgraded `pip` to version 26.1.1.

### Bug fixes

- Fixed the macOS arm64 installer incorrectly requiring Rosetta 2. The `Distribution.xml` package metadata now declares `hostArchitectures="arm64,x86_64"`, so the installer is recognized as native on Apple Silicon.
- Fixed `snow spcs service build-image` on Azure accounts to work with stages that use the `SNOWFLAKE_FULL` encryption type.
- Fixed Snowsight URL generation (used by `snow streamlit deploy`, `snow streamlit get-url`, `snow app run`, `snow notebook`, and similar commands) for accounts whose host is 4-part (for example, `<account>.us-east-1.snowflakecomputing.com`) or 5-part with a cloud suffix (for example, `<account>.<region>.aws.snowflakecomputing.com`). These hosts now resolve to the correct regioned Snowsight URL instead of raising a “host was missing or not in the expected format” error.
- Fixed `snow connection list` crashing with `AttributeError` when `config.toml` contains a scalar value directly under `[connections]`. Such entries are now skipped with a warning so valid connections are still listed.
- Fixed boolean connection parameters (`client_store_temporary_credential`, `oauth_disable_pkce`, `oauth_enable_refresh_tokens`, `oauth_enable_single_use_refresh_tokens`) being passed to the connector as raw strings when supplied via `SNOWFLAKE_*` or `SNOWFLAKE_CONNECTIONS_<name>_*` environment variables. Values like `false` and `0` are now correctly interpreted as `False` rather than truthy strings.
- Closed several SQL injection paths and improved input handling across the CLI:
  - Fixed SQL injection in `snow spcs service create`, `execute-job`, and `upgrade` where a `$$` sequence in a YAML spec file could break out of the dollar-quoted SQL literal.
  - Fixed SQL string literal escaping in `SHOW ... LIKE` patterns to use Snowflake’s standard single-quote doubling (`''`) instead of backslash escaping, which is not interpreted under the default `STANDARD_ESCAPE_SEQUENCES=FALSE` session setting.
  - Fixed SQL injection through `FQN.sql_identifier` (single quotes are now escaped).
  - Improved input handling in `snow cortex complete` and `snow cortex translate`.
  - Improved input handling in `snow git setup`, `snow connection` secret creation, and API integration creation.
  - Improved argument handling in SPCS service status and log commands.
  - Improved string handling in `CREATE STREAMLIT` SQL emitted by `snow streamlit deploy` and related commands.
  - Improved pattern handling for `--like` arguments to `snow object show`, `snow git show`, and `snow spcs image-repository list-images`.
- Improved file and path handling across the CLI:
  - Improved file handling in the `read_file_content` and `procedure_from_js_file` Jinja filters used during SQL template rendering.
  - Improved path handling in the Snowpark annotation processor (`nativeapp codegen snowpark`).
  - Improved path handling for post-deploy `sql_script` hooks.
  - Improved file handling in artifact bundling for `snow app` and `snow snowpark`.
- Improved the output of `repr(ConnectionContext)` and related debug logs to redact credentials.

## Version 3.17.1 (May 12, 2026)

### Bug fixes

- Encrypted private key files no longer require `PRIVATE_KEY_PASSPHRASE` to be set in the environment. The passphrase can now be read from `private_key_file_pwd` (the name used by `snowflake-connector-python`) or `private_key_passphrase` in `connections.toml` or `config.toml`. The `PRIVATE_KEY_PASSPHRASE` environment variable continues to take precedence when set. This also fixes a regression in 3.17.0 where commands using key-pair authentication with `private_key_passphrase` in `connections.toml` failed with `argument 'password': Cannot convert "<class 'str'>" instance to a buffer`.

## Version 3.17.0 (May 11, 2026)

### New features and updates

- The `snow app` command group now supports both Snowflake Native Apps (`application` and `application package` entities) and Snowflake Apps Deploy (`snowflake-app` entities). The entity type in `snowflake.yml` determines which flow is used, so shared subcommands such as `bundle`, `deploy`, `validate`, `open`, `events`, and `teardown` automatically select the correct behavior. The experimental hidden `snow __app` command group and the `ENABLE_SNOWFLAKE_APPS` feature flag have been removed.
- Added the `snow app setup` command for initializing a `snowflake.yml` file for a Snowflake Apps Deploy project.
- Added the `snow connection generate-workload-identity-token` command to generate a workload identity token for the current environment. Supports AWS, GCP, Azure, and OIDC providers via the `--workload-identity-provider` option or connection configuration.
- Added the `snow custom-image validate` command to validate custom Docker images against configured rules (entrypoint, environment variables, Python packages, and dependency health). Supports an optional `--scan-vulnerabilities` flag to run Grype vulnerability scanning.
- Added the `snow dcm purge` command to drop all the objects managed by the specified DCM Project. The project object itself is not dropped.
- DCM manifest targets now validate the `account_identifier` and `project_owner` fields. The CLI checks these against the current session and prints a warning on mismatch: `account_identifier` is checked for all manifest-based commands, and `project_owner` is checked for `snow dcm create`.
- Added the `--secondary-roles` option (and matching `SNOWFLAKE_SECONDARY_ROLES` environment variable and `secondary_roles` configuration key) to `snow connection add` and the global connection overrides. The value is forwarded to `snowflake-connector-python` and accepts `ALL` or `NONE`, so sessions can be pinned to the primary role without running `USE SECONDARY ROLES`.
- Added the `--force` option to `snow spcs service drop` to allow dropping services that contain block storage volumes.
- Significantly improved DCM file upload performance.
- Updated `snowflake-connector-python` to version 4.4.0. The 4.x series introduced stricter permission checks. In future versions of Snowflake CLI, strict configuration file permissions will become mandatory. To test whether your files have the correct permissions, set `SNOWFLAKE_CLI_FEATURES_ENFORCE_STRICT_CONFIG_PERMISSIONS=1` before running CLI commands.

### Bug fixes

- Fixed `snow streamlit deploy` failing with a collision error when a `pages/*.py` glob in `additional_source_files` overlaps with the automatically-included `pages/` directory. Overlapping glob patterns are now deduplicated during v1-to-v2 definition conversion.
- Fixed the error message when the `PRIVATE_KEY_PASSPHRASE` environment variable is set to an empty string.
- Fixed `SELECT *` output being corrupted when joined tables share column names. Duplicate column names are now disambiguated by appending a numeric suffix (for example, `NAME`, `NAME_2`).
- Fixed `snow connection generate-jwt` and `snow connection generate-workload-identity-token` failing with `Connection None is not configured` when used with `--temporary-connection`.
- Fixed duplicate `LOGIN_HISTORY` events (and `OVERFLOW_FAILURE_EVENTS_ELIDED` entries) previously emitted when a `snow` invocation was rejected by an authentication policy. The internal connection cache now remembers failed connect attempts and re-raises the original exception on subsequent accesses within the same process, instead of re-dialing Snowflake every time a command accesses the shared connection.
- Fixed session/master token connections created from environment variables or named connection configuration not enabling token keep-alive settings. This could cause follow-up commands to fail with `251007: Session and master tokens invalid`.

## Version 3.16.0 (Mar 19, 2026)

### New features and updates

- Added support for DCM commands in preview.
- Added the `--in-account` option to list commands (for example, `snow object list`, `snow stage list`). This option lists all objects of a given type in the account. Cannot be used together with the `--in` option.
- Added the **experimental** command `snow spcs service build-image` to build container images using an SPCS service. The command uploads the local build context to a stage, executes a build job, and streams logs in real time until completion. This command is experimental and subject to change.
- Added the `--async` option to the `snow spcs service execute-job` command to execute job services asynchronously without waiting for completion.
- Added the `--replicas` option to the `snow spcs service execute-job` command to specify the number of job replicas to run.
- Added the `--dbt-version` option to the `snow dbt deploy` and `snow dbt execute` commands. This option sets the dbt Core version on a dbt project object (`snow dbt deploy` command) or executes a dbt command on a specific dbt Core version without altering the dbt object (`snow dbt execute` commands).
- All authenticators (including `snowflake-jwt`, `username_password_mfa`, and `workload_identity`) are now case-insensitive.
- Changed how the fully qualified names for temporary stages are established for `snow dbt deploy`. The database and schema from the dbt project object’s fully qualified name now take precedence over those from the session.

### Bug fixes

- Fixed `snow stage copy --recursive` dropping database and schema qualifiers from fully qualified stage names, which caused the command to resolve stages against the connection’s default database instead of the one specified in the FQN.
- Fixed `snow streamlit deploy --prune` failing with an incorrect stage path format for Streamlit entities using versioned deployment. The `snow://` prefix is now correctly preserved through all stage path operations.
- Fixed a bug with `snow dbt deploy` where the dbt project uploaded files first and updated project properties afterward. This could cause deploys to fail if, for example, the project lacked external access integrations and dependencies were specified.
- Fixed the `snow stage copy` and `snow stage put` commands failing when a local directory path contains glob special characters (such as, square brackets in [id] or [slug]). The path is now escaped before glob expansion, so literal directory names are matched correctly.

## Version 3.15.0 (Feb 03, 2026)

### New features and updates

- Added the `--if-exists` option to the `snow object drop` command and object-specific drop commands (for example, `snow stage drop`) to drop objects only if they exist, preventing errors when dropping non-existent objects.
- Updated the project definition with supported Python versions aligned with `snowflake-connector-python`.

### Bug fixes

- Fixed git repository path parsing to allow quotes around both repository and branch names (such as `@"example-repo"/branches/"feature/branch"/*`).
- Fixed external browser authentication (`EXTERNALBROWSER`) for headless systems.
