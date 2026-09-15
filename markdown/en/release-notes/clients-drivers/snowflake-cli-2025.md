# Snowflake CLI release notes for 2025

This article contains the release notes for the Snowflake CLI, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

See [Snowflake CLI](/developer-guide/snowflake-cli/index) for documentation.

## Version 3.14.0 (Dec 09, 2025)

### New features and updates

- Updated the `snow streamlit deploy` command to use the updated CREATE STREAMLIT syntax (FROM *source\_location*) instead of the deprecated syntax (ROOT\_LOCATION = ‘<stage\_path\_and\_root\_directory>’).

  Note

  The deprecated syntax is still supported, but Snowflake recommends using the new syntax for better clarity and consistency. You can use the `snow streamlit deploy --legacy` option to continue using the deprecated syntax.

### Bug fixes

- None.

## Version 3.13.1 (Dec 02, 2025)

### New features and updates

- None.

### Bug fixes

- Fixed an issue with parsing the `--vars` values provided to `snow dbt execute` subcommands. This fix allows you to pass variables the same way as you would to the dbt CLI, such as `--vars '{"key": "value"}`’.

## Version 3.13.0 (Nov 03, 2025)

### New features and updates

- Added the `--decimal-precision` global option to allow setting arbitrary precision for Python’s `Decimal` type.
- Added support for the `auto_suspend_secs` parameter in SPCS service commands (`deploy`, `set`, `unset`) to configure automatic service suspension after a period of inactivity.
- Added the `snow dbt describe` and `snow dbt drop` commands.
- Added the `snow dbt execute ... retry` subcommand.
- Added the following `snow dbt deploy` command options:

  - `--default-target` to set a default target.
  - `--unset-default-target` to clear the default target.
  - `--external-access-integration` to set external access integrations (needed to pull external dependencies for altering a dbt project object).
  - `--install-local-deps` to install dependencies located in the project.
- Added support for running Streamlit apps on SPCS runtime.
- Added grant privileges definitions to the Streamlit `snowflake.yml` file.
- Updated snowflake-connector-python to version 3.18.0.
- Relaxed dbt `profiles.yml` validation rules; added extra validation for role specified in `profiles.yml`.

### Bug fixes

- None.

## Version 3.12.0 (Sep 24, 2025)

### New features and updates

- Added the `!edit` command to the `snow sql` command to support external editors.
- Added the `--partial` option to the `snow logs` command to support partial, case-insensitive matching of log messages.
- Improved parsing `!source` with trailing comments.
- Upgraded to `typer=0.17.3` to improve the display of help messages.
- Improved output handling with streaming queries in the `snow sql` command.

### Bug fixes

- Fixed crashes with older x86\_64 Intel CPUs.
- Fixed the `!` commands in `snow sql` commands so they no longer require a trailing `;` for evaluation.
- Fixed using `ctx.var` in `snow sql` with Jinja templating.
- Fixed issues when pasting content with trailing new lines.
- Fixed an issue with `snow snowpark deploy` failing on duplicated packages.
- Fixed an issue causing a `snow spcs logs` `IndexOutOfRange` error.

## Version 3.11.0 (Aug 25, 2025)

### New features and updates

- Added the `snow connection remove` command.
- Added support for the `runtime_environment_version` field in notebook entity configurations to let you specify runtime environment version for containerized notebooks.
- Added the `snow auth oidc` commands for managing workload identity federation authentication:

  - `snow auth oidc read-token` to read and display OIDC tokens from CI/CD environments.

  Also included GitHub Actions provider support in these commands for password-less authentication in CI/CD pipelines.

### Bug fixes

- None.

## Version 3.10.1 (Aug 15, 2025)

### New features and updates

- None

### Bug fixes

- Fixed `snow dbt deploy` command to properly handle fully qualified names.
- Fixed `snow dbt deploy` command to properly handle local directories with dots in names.

## Version 3.10.0 (July 17, 2025)

### Deprecations

- This version deprecates the Snowpark processor in the Snowflake Native App Framework.

### New features and updates

- Added support for passing an OAuth token with the `--token` option.
- Added the ability to suppress new Snowflake CLI version messages.
- Added the following new `--format` options for outputting data:

  - `CSV`, which formats query output as CSV.
  - `JSON_EXT`, which outputs JSON as JSON objects instead of strings.
- Added the `--enabled_templating` option for the `snow sql` command that lets you specify which of the following templates to use when resolving variables:

  - Standard (`<% ... %>`), enabled by default.
  - Legacy (`&{ ... }`), enabled by default.
  - Jinja (`{{ ... }}`), disabled by default.
- Added a `packages` alias for `artifact_repository_packages` in the `snowflake.yml` schema.
- Added the `snow stage copy @src_stage @dst_stage` command for copying files directly between two named stages.
- Added support for the DBT `deploy`, `execute`, and `list` commands.

### Bug fixes

- Fixed an issue where the `snow sql` command would fail when `snowflake.yml` is invalid and the query has no templating.
- Fixed an issue with JSON serialization for the `Decimal`, `time`, and `binary` data types.

## Version 3.9.1 (June 09, 2025)

### New features and updates

- Added the `--private-link` option to `snow spcs image-registry login` command to log in using private link URLs.

### Bug fixes

- None.

## Version 3.9.0 (May 29, 2025)

### New features and updates

- Added the `--encryption` option to the `snow stage create` command to define the type of encryption to use for all files on the stage.

### Bug fixes

- Fixed errors that occurred for `use` commands if the current database is not set.

## Version 3.8.3 (May 22, 2025)

### New features and updates

- None

### Bug fixes

- Added the `--private-link` option to the `snow spcs image-registry url` command for retrieving private link URLs.

## Version 3.8.2 (May 21, 2025)

### New features and updates

- None

### Bug fixes

- Changed the `enable_release_channels` property default from `False` to None.

## Version 3.8.1 (May 20, 2025)

### New features and updates

- None

### Bug fixes

- The upgrade message is now sent to `stderr`.
- Fixed a `snowflake.core` import issue on newer Python versions.

## Version 3.8.0 (May 16, 2025)

### New features and updates

- Added support for OAuth tokens.
- Added the following enhancements to the `snow sql` command:
  - Added an interactive mode.
  - Added support for asynchronous SQL queries.
  - Added support for the `!queries`, `!result`, and `!abort` SQL query commands.
  - Added the `--single-transaction` command-line option to execute multiple SQL queries as an all-or-nothing batch, ensuring that all commands complete successfully before any of the changes are committed.
  - Added the `artifact_repository` field to the Snowpark Entity Model to support using non-anaconda packages.

### Bug fixes

- Fixed an issue with deploying Snowpark project using the `!=` operator in `requirements.txt`.
- Fixed an issue with escaping identifiers for `use` commands.
- Moved the `enable_release_channels` parameter from the global level to the project level.
- Fixed the `snow spcs service metrics` command to accept fully qualified service names.

## Version 3.7.2 (May 12, 2025)

### New features and updates

- None.

### Bug fixes

- Fixed an issue with errors appearing in help messages.

## Version 3.7.1 (April 28, 2025)

### New features and updates

- None.

### Bug fixes

- Fixed certificate connection issues.
- Fixed a `snow spcs image-registry` login slow query problem.

## Version 3.7.0 (April 16, 2025)

### New features and updates

- Added the `--prune` option to the `snow notebook deploy`, `snow snowpark deploy`, and `snow streamlit deploy` commands that removes files that exist in the stage, but not in the local filesystem.
- Added the `snow logs` command for retrieving and streaming logs from the server.
- Added the `snow helper check-snowsql-env-vars` that reports environment variables from SnowSQL with their Snowflake CLI replacements.

### Bug fixes

- Updated the MacOS post-install script to update the `PATH` environment variable, if needed, to ensure the `snow` command is available.

## Version 3.6.0 (April 2, 2025)

### New features and updates

- Added support for the `!source` command in SQL queries to allow executing SQL from local files.

### Bug fixes

- Fixed an issue with incompatible options in `snow spcs compute-pool` commands that didn’t raise error.
- Changed binary builds to embed the whole Python environment.
- Fixed recursive copying to a stage for unbalanced directory trees.
- Fixed checking for a new Snowflake CLI version.
- Added file execution logs in `snow stage` and `snow git` commands.

## Version 3.5.0 (March 10, 2025)

### New features and updates

- Extended project definition (`snowflake.yml`) support for the following SPCS (Snowpark Container Services) entities:

  - Compute pool
  - Image repository
  - Service
- Added the `snow spcs compute pool deploy` command that reads a `snowflake.yml` project definition file.
- Added the `snow spcs image repository deploy` command that reads a `snowflake.yml` project definition file.
- Added the `snow spcs service deploy` command that reads a `snowflake.yml` project definition file.

### Bug fixes

- Fixed an issue with data type handling in the `snow sql` command when using JSON for the output format.

## Version 3.4.0 (February 13, 2025)

### New features and updates

- Added the optional `stage_subdirectory` field to the application package entity.
  When this value is specified, application artifacts are uploaded to this subdirectory instead of to the root of the application package’s stage.
- Added the following `snow spcs service` commands:

  - `snow spcs service events` retrieves service-specific events.
  - `snow spcs service metrics` fetches service metrics.
- Added the following `snow app release-directive` commands:

  - `snow app release-directive add-accounts` adds accounts to a release directive.
  - `snow app release-directive remove-accounts` removes accounts from a release directive.
- Added the `snow app release-channel set-accounts` command to set accounts for release channels.
- Added the `--force-replace` option to the `snow snowpark deploy` command to replace entities even if no changes are detected.
- Added the following notebook functionality:

  - Added the `snow notebook deploy` command that allows the creation of a notebook using a local file.
  - Added support for containerized notebooks.
  - Added `notebook` to the supported object types for the `snow object` commands.
- Added support for glob patterns (except `**)` in artifacts paths in Streamlit and Snowpark `snowflake.yml` files.

  Note

  Using glob patterns in Snowpark `snowflake.yml` files requires enabling the ENABLE\_SNOWPARK\_GLOB\_SUPPORT feature flag.
- Added support for the Mac OS x86\_64 architecture.

### Bug fixes

- Fixed an MFA caching issue in the Snowflake CLI binary installation files.
- Fixed an auto-completion issue in the Snowflake CLI binary installation files.

## Version 3.3.0 (January 21, 2025)

Note

On January 28, 2025, Snowflake updated the documentation for the `snow add release channel` commands to indicate that the feature is in Public Preview instead of General Availability.

### New features and updates

- Added the following Snowflake Native Apps features and updates:

  - Added the following commands to support release directives:

    - `snow app release-directive list`
    - `snow app release-directive set`
    - `snow app release-directive unset`
  - Added support for release channels, including the following:

    - Added support release channels in the `snow app version create` and `snow app version drop` commands.
    - Added the ability to specify a release channel when creating an application instance from a release directive (`snow app run --from-release-directive --channel=<channel>`).
    - Added the `snow app release-channel list` to list available release channels.
    - Added the `now app release-channel add-accounts` and `snow app release-channel remove-accounts` commands to support adding and removing accounts from release channels.
    - Added the `snow app release-channel add-version` and `snow app release-channel remove-version` commands to add versions to and remove versions from release channels.
  - Added the `snow app publish` command to simplify publishing versions to release channels and to update release directives.
  - Made the following changes to the `snow app version create` command:

    - The command now returns the version, patch, and label in JSON format.
    - Added the `--from-stage` option to allow version creation from the content of a stage without needing to re-synchronize to the stage.
- Added the `snow helpers import-snowsql-connections` command to import connections from existing SnowSQL configurations.
- Added support for restricting user access to Snowflake CLI only. For more information, see [Add an authentication policy that limits access to Snowflake CLI only](/developer-guide/snowflake-cli/connecting/configure-cli#label-snowcli-limit-access).

### Bug fixes

- Fixed the inability to add patches to lowercase quoted versions.
- Fixed an issue with setting label to blank instead of `None` when not provided.
- Fixed the `snow connection generate-jwt` command to preserve command-line connection options.
- Fixed stage path handling for notebook commands.
