# ODBC Driver 4.x overview

**Version: 4.x.** [Switch to ODBC 3.x](/developer-guide/odbc/odbc-download-3x) · [Choose another task](/developer-guide/odbc/odbc).

Snowflake ODBC Driver 4.x is generally available. Starting with version 4.0.0, the driver is built on the
[Universal Core](/developer-guide/universal-core/universal-core), a shared Rust library for networking, authentication,
result-set fetching, and stage transfers. Your application continues to use the ODBC interface;
you do not need to write Rust code.

Version 4.x introduces installation, configuration, and behavior changes from 3.x. Before replacing an existing
driver, follow the [migration guide](/developer-guide/odbc/odbc-migration) and validate your application on a separate host.

## What’s changed

The Universal Core shares networking, authentication, and data-transfer implementations across drivers built on it.
For the architecture, see [Universal Core](/developer-guide/universal-core/universal-core). For ODBC-specific improvements and
changes, see the [4.0.0 release notes](/release-notes/clients-drivers/odbc-2026) and
[migration guide](/developer-guide/odbc/odbc-migration).

## Install and connect

Choose an installer that matches your operating system and application architecture:

- [Download ODBC 4.x](/developer-guide/odbc/odbc-download).
- [Install and configure (Linux)](/developer-guide/odbc/odbc-linux).
- [Install and configure (macOS)](/developer-guide/odbc/odbc-mac).
- [Install and configure (Windows)](/developer-guide/odbc/odbc-windows).

## Configure the driver

Use the [configuration and connection parameter reference](/developer-guide/odbc/odbc-parameters) for supported settings.
The [configuration differences](/developer-guide/odbc/odbc-migration#label-odbc-migration-config) explain 4.x logging,
certificate revocation checking, connection profiles, and parameter replacements.

## Migrate from 3.x

Follow the [migration steps](/developer-guide/odbc/odbc-migration#label-odbc-migration-steps) before a production cutover.
Review the [behavior differences](/developer-guide/odbc/odbc-migration#label-odbc-migration-behavior-differences) and
[ODBC API reference](/developer-guide/odbc/odbc-api) for changes relevant to your application.

## Check application compatibility

If a tool or vendor manages the driver, follow its supported upgrade process rather than replacing the driver independently.
Check with your tool vendor or Snowflake account team about compatibility with your application and version.

## Troubleshoot and track changes

For logging and connectivity diagnostics, see [ODBC Driver diagnostic service](/developer-guide/odbc/odbc-diagnostic-service).
Use the [release notes](/release-notes/clients-drivers/odbc) to track fixes and the
[migration guide](/developer-guide/odbc/odbc-migration) to distinguish behavior changes from issues resolved during preview.
