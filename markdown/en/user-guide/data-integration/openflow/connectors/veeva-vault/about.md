# About the Openflow Connector for Veeva Vault

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

The Openflow Connector for Veeva Vault replicates data from a Veeva Vault instance into Snowflake using
[Direct Data API](https://general.veevavault.dev/direct-data-api).
The connector downloads Direct Data files, extracts the CSV data they contain, and
loads that data into Snowflake tables using Snowpipe Streaming. It supports full snapshots,
incremental updates, and optional audit log ingestion.

## Use cases

The connector supports the following use cases:

- **Full data replication:** Perform a one-time full snapshot of all Veeva Vault data
  into Snowflake for reporting, analytics, and compliance.
- **Incremental synchronization:** After the initial snapshot, the connector polls for
  incremental Direct Data files on a configurable schedule (default: every 15 minutes) to
  keep Snowflake tables up to date with changes in Veeva Vault.
- **Audit log ingestion:** Optionally ingest Veeva Vault audit log archives alongside data
  archives, providing a complete audit trail in Snowflake.
- **Migration and analytics:** Centralize Veeva Vault data in Snowflake for cross-system
  analytics, data science, and regulatory reporting.

## The replication lifecycle

A table’s replication cycle begins with a full data snapshot and then transitions to
incremental synchronization.

1. **Snapshot phase:** The connector downloads the latest full Direct Data file from
   Veeva Vault. This archive is a tar.gz file containing one CSV per Vault data object.
   The connector unpacks the archive, creates a destination table in Snowflake for each
   object (if it doesn’t already exist), loads the data through Snowpipe Streaming into
   a staging table, and merges the staging data into the final destination table.
2. **Incremental phase:** After the snapshot completes, the connector polls Veeva Vault for
   incremental Direct Data files. Each incremental file contains only the records
   that changed since the previous incremental file. The connector applies updates through the same
   staging-and-merge pipeline and processes deletes separately based on the configured
   delete strategy. Data freshness in Snowflake depends on how frequently Veeva Vault
   publishes Direct Data files and the configured sync frequency of the connector.
3. **Audit log phase (optional):** When audit log ingestion is enabled, the connector also
   downloads `log_directdata` files and loads them into Snowflake following the same
   pipeline.

The connector groups Direct Data files by their reported time window and processes one
window at a time to ensure each batch is handled atomically before moving to the next.

The connector tracks its progress using a persisted state that records the last processed
timestamp. If the connector is stopped and restarted, it resumes from where it left off.

## Ingestion modes

The connector supports three ingestion modes that control how Direct Data files are consumed:

SNAPSHOT\_AND\_INCREMENTAL (default):
:   The connector first processes the latest full Direct Data file (snapshot). Once the
    snapshot is complete, it transitions to polling for incremental archives. This is the
    recommended mode for most deployments.

SNAPSHOT:
:   The connector continuously polls for the latest full Direct Data file. Each time a
    new full file becomes available, it is processed. Use this mode when you want to
    periodically replace all data in Snowflake with a fresh full export.

INCREMENTAL:
:   The connector polls only for incremental Direct Data files. No full snapshot is
    performed. Use this mode when a snapshot has already been loaded by other means or when
    only recent changes are needed. You can optionally specify a start time to control how
    far back incremental polling begins.

## Authentication

The connector authenticates with Veeva Vault using session-based authentication. You provide
a service account username and password, and the connector obtains a session identifier from
the Vault API auth endpoint. This session is reused across requests and is automatically
refreshed when it expires.

For Snowflake authentication, the connector supports two strategies:

SNOWFLAKE\_MANAGED (default):
:   Uses the Snowflake-managed token associated with the Openflow runtime’s execute-as role. This is the
    recommended strategy for both Openflow - Snowflake Deployments and Openflow - BYOC Deployments.

KEY\_PAIR:
:   Uses a user-provided RSA key pair for authentication. This strategy is available only
    on Openflow - BYOC Deployments and is intended for cross-account scenarios where the connector needs
    to write to a Snowflake account different from the one hosting the Openflow runtime.

## How deletes are handled

When the connector receives a delete extract from Veeva Vault, it applies the deletes in
Snowflake according to the configured delete strategy:

Hard Delete (default):
:   Rows are permanently removed from the destination table using a `DELETE` statement.

Soft Delete:
:   Rows are not removed. Instead, the connector sets a `__SNOWFLAKE_DELETED` column to
    `TRUE` and a `__SNOWFLAKE_DELETED_AT` column to the current timestamp. If these columns
    don’t exist in the destination table, the connector adds them automatically.

## Schema evolution

The connector supports schema evolution when the structure of Veeva Vault data changes
between files. When the connector detects new columns in an incoming file, it
automatically adds those columns to the destination and staging tables in Snowflake.

When a column is no longer present in the incoming file, the connector applies the
configured column removal strategy:

Drop Column (default):
:   Drops the column from the Snowflake table.

Rename Column:
:   Renames the column by appending a configurable suffix (default: `__deleted`). This
    preserves historical data in the table.

Ignore Column:
:   Leaves the column as-is in the Snowflake table and stops populating it.

## Automatic retry handling

The connector automatically retries failed API calls using an exponential backoff strategy.
Retryable conditions include HTTP status codes 500, 502, 503, and 504,
as well as transient network errors.

If a session expires or becomes invalid, the connector automatically re-authenticates and
retries the request.

## Limitations

Consider the following limitations when using the connector:

- Direct Data must be enabled on your Vault instance before using the connector.
  Contact your Veeva Vault administrator to enable this feature.
- The connector authenticates using session-based username and password credentials. Other
  authentication methods (such as OAuth) aren’t yet supported.
- The connector replicates structured data from Direct Data files only. Document and
  attachment content (such as files stored in Veeva Vault) isn’t replicated.
- The connector currently only performs an initial load of objects of type
  [legacy\_workflow](https://platform.veevavault.help/en/gr/5205/)
  and doesn’t replicate ongoing changes.

## Next steps

For information on how to set up the connector, see [Setting up the Openflow Connector for Veeva Vault](/user-guide/data-integration/openflow/connectors/veeva-vault/setup).
