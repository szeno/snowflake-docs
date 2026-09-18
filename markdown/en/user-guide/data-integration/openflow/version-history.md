# Snowflake Openflow version history

This topic provides version history for [Snowflake Openflow](/user-guide/data-integration/openflow/about).

To apply the latest updates to your deployment, runtimes, or connectors, see [Manage Openflow](/user-guide/data-integration/openflow/manage).

Show entries for:DeploymentRuntime / ConnectorControl Plane

## September 16, 2026

### Control Plane Core `0.133.0`

- Deployment upgrade is now triggerable from Control Plane for BYOC Deployments
- Connector configuration parameters now refresh automatically when a connector’s version changes, eliminating the need to reload the page to see updated parameter options after an upgrade
- Runtime and connector display names containing special characters (e.g. parentheses, quotes) are now handled correctly
- Fixed a case where creation of multiple Snowflake Deployment at exactly the same time could lead to a failure
- Security patches and dependency upgrades

### Control Plane UI `0.92.0`

- Connector install dialogs now explain why certain runtime versions are filtered out (e.g. incompatible version constraints), giving users actionable context rather than an unexplained empty list
- Schema lookup in connector configuration now uses the query-parameter API, improving reliability and reducing failures on accounts with large schema counts
- Gen 2 connector, runtime, and deployment names are now validated as valid Snowflake identifiers in real time as you type, surfacing naming errors before submission
- Fixed a UI state issue where the “saving” spinner on deployment listings would remain stuck after a mutation completed successfully
- Security patches and dependency upgrades

### Data Plane Service `0.133.0`

- Diagnostic bundles now recover and include a Runtime’s flow file even when a Runtime’s pods are unhealthy
- Security patches and dependency upgrades

### Data Plane UI `0.23.0`

- Security patches and dependency upgrades

### Runtime Operator `0.77.0`

- Security patches and dependency upgrades

### Ingress Controller `2026.9.9-18`

- Security patches and dependency upgrades

### Openflow Token Refresher `1.20.0`

- Security patches and dependency upgrades

### AWS Data Plane Agent `1.66.0`

- Security patches and dependency upgrades

### SPCS Data Plane Agent `1.49.0`

- Security patches and dependency upgrades

## September 11, 2026

### SPCS Data Plane Agent 1.47.2

- Fixed issue with Openflow using DCP for a subset of customers who experienced errors with workload identify and egress for newly created runtimes.
- Security patches and dependency upgrades.

## September 10, 2026

### Runtime Server 2026.9.10.2

- Security patches and dependency upgrades.
- Gen 2 connectors: Included property defaults during connector configuration verification.
- Fixed automatic reloading of symlinked security stores, specifically in Kubernetes-based deployments when certificates are rotated.
- Upgraded the Runtime UI to version 0.89.0.

### Runtime Extensions 2026.9.10.9

- Iceberg: Improved PutIcebergRecord processor support for complex types and timestamps.
- SharePoint: Introduced the SharePoint gen 2 connector in Private Preview.
- Oracle CDC: Prevented spurious errors when a recoverable Oracle connection reset occurs while adjusting the billing counter, processing new tables, or validating a license. The connector now reconnects on the next trigger.
- MongoDB: Limited snapshot output FlowFiles to a configurable target size, reducing repeated Snowpipe Streaming failures when collections contain large documents.
- Snowflake Parameter Provider: Continued loading accessible AWS Secrets Manager and Azure Key Vault secrets when the runtime role cannot access other secrets in the same integration. Verification now reports listed and fetched secret counts and fails when no parameters are retrievable.
- CDC SQL Server: Added support for `DBCPConnectionPoolLookup` with one connection pool per database for Azure SQL Database singleton replication and validated change tracking retention for databases that begin replicating later.

### Connectors 2026.9.10.1

- Oracle Embedded License 0.49.0:
  - Added a clone, truncate, and archive re-snapshot workflow that creates a unique snapshot table before replacing the destination table.
- Oracle Embedded License Public Sector 0.48.0:
  - Added a clone, truncate, and archive re-snapshot workflow that creates a unique snapshot table before replacing the destination table.
- Oracle Independent License 0.48.0:
  - Added a clone, truncate, and archive re-snapshot workflow that creates a unique snapshot table before replacing the destination table.
- Table Consolidation 0.8.0:
  - Added support for configurable row lineage columns and clustering, and created destination streams next to their destination tables.

## September 8, 2026

### AWS Data Plane Agent 1.64.1

- Added support for AWS Tags with colon-space (“: “) values
- Fixed intermittent timeouts of the cluster telemetry Helm release by raising its timeout from the 5-minute default to 7 minutes.
- Added Helm release cleanup logic to the cluster bootstrap step to prevent failures from attempting to reuse a release name that was still in use.

### Runtime Server 2026.9.8.2

- Security patches and dependency upgrades.

### Runtime Extensions 2026.9.8.2

- Databases: Added a Database Password Provider for Google Cloud SQL IAM database authentication. This allows the use of GCP IAM authentication in the CDC PostgreSQL connector when connecting to Google Cloud SQL for PostgreSQL instances.
- Jira Core: Prevented a custom field named `Updated` from interfering with incremental issue updates.
- Table Consolidation: Used the destination stream identity supplied by the flow, allowing destination change streams to reside next to their destination tables.
- CDC Databases, MongoDB, and Snowflake: Logged automatically retried connectivity and infrastructure issues as warnings instead of errors.
- CDC MySQL: Removed the false-positive warning `Ignoring a commit position with no server UUID` during connector startup.
- Table Consolidation: After a restart, looked up each destination table’s primary key once from Snowflake instead of persisting primary keys in processor state.
- Table Consolidation: Added optional custom row lineage columns sourced from a Snowflake configuration table. When the property is empty or no rows match, the existing `ROW_LINEAGE` behavior remains unchanged.

### Connectors 2026.9.8.1

- CDC SQL Server CT 0.54.0:
  - Restored the configured destination database after provisioning connector-events objects for Table Consolidation so subsequent snapshot objects are created in the correct database and replication does not stall.
- BigQuery 0.10.0:
  - Preserved microsecond precision for BigQuery `TIMESTAMP` values instead of truncating them to milliseconds.

## September 7, 2026

### Runtime Server 2026.9.5.13

- Security patches and dependency upgrades.
- Allowed existing flows containing legacy and/or invalid parameter names to load.

### Runtime Extensions 2026.9.5.13

- CDC MySQL: Fixed GTID restart tracking so stopping `CaptureChangeMySQL` cannot permanently skip transactions that were queued but not yet processed.
- Snowpipe Streaming: Logged DNS resolution failures from `PublishSnowpipeStreaming` at the error level.
- CDC Oracle: Added a warning and incremented the `Unsupported LOB Events Ignored` counter for unsupported partial LOB operations, including the source table and replication keys so operators can identify affected rows. Partial LOB operations continued to be unsupported.

### Connectors 2026.9.5.12

- Oracle Embedded License 0.48.0:
  - Configured the Oracle connection pool to present the client certificate from the configured wallet, enabling mutual TLS for snapshot and schema operations.
- Oracle Embedded License Public Sector 0.47.0:
  - Configured the Oracle connection pool to present the client certificate from the configured wallet, enabling mutual TLS for snapshot and schema operations.
- Oracle Independent License 0.47.0:
  - Configured the Oracle connection pool to present the client certificate from the configured wallet, enabling mutual TLS for snapshot and schema operations.
- CDC PostgreSQL 0.66.0:
  - Separated changes committed while a snapshot is running into a snapshot change log and compacted them by primary key before merging, preventing duplicate destination rows and preserving values needed for TOAST updates.
- Table Consolidation 0.7.0:
  - Gated merge events until provisioning DDL commits so a merge cannot run before its destination stream exists.
  - Ran Consolidate Table Data with four concurrent tasks so independent consolidated tables can merge in parallel.

## September 4, 2026

### Control Plane Core 0.131.0

- Removed the Public Preview label from the Jira Cloud (Core) connector in the connector catalog, following its move to general availability.
- Gen2 CDC MySQL and PostgreSQL: These connectors now require Runtime Extensions 2026.8.25.11 or later.
- Fixed a rare issue affecting Openflow when a Snowflake account was dropped and then recreated with the same name.
- Improved control plane responsiveness when listing runtimes, particularly on accounts with many runtimes.
- Security patches and dependency upgrades.

### Data Plane Service 0.131.0

- Increased timeouts for long-running runtime operations, improving success rates on larger runtimes.
- Security patches and dependency upgrades.

### Control Plane UI 0.90.0

- Added a Connector library tab to the connector catalog.
- SharePoint: Added file type filters to the connector setup wizard.
- Security patches and dependency upgrades.

### Data Plane UI 0.22.0

- SharePoint: Added file type filters to the connector setup wizard.
- Updated Connector library tab naming.
- Security patches and dependency upgrades.

### Runtime Operator 0.76.0

- Improved runtime startup times by copying connector extensions in parallel.
- Security patches and dependency upgrades.

### Ingress Controller 2026.9.3-0

- Security patches and dependency upgrades.

### SPCS Data Plane Agent 1.47.0

- Security patches and dependency upgrades.

### AWS Data Plane Agent 1.63.1

- Fixed deployment agent out-of-memory failures during large infrastructure operations. These failures could interrupt deployment creation or deletion and leave deployment state inconsistent.
- Deployment deletion is now cleaner, faster, and more reliable, addressing several conditions that could block or complicate teardown.
- Security patches and dependency upgrades.

## September 3, 2026

### Runtime Server 2026.9.3.2

- Security patches and dependency upgrades.

### Runtime Extensions 2026.9.3.12

- CDC SQL Server: The connector no longer stops discovering tables across the source instance when one CDC-enabled database cannot be read. The unreadable database is reported as unavailable and skipped while discovery continues for the others.
- CDC Oracle: Adds mutual TLS support for thin JDBC connections by presenting the client certificate from the configured Oracle wallet.
- CDC Oracle: The CaptureChangeOracle processor can keep table schemas in memory when `OPENFLOW_ORACLE_CDC_CONNECTOR_STATE_STORAGE` is set to `IN_MEMORY`. Existing deployments retain the default NiFi-state behavior.
- Gen 2 CDC MySQL and PostgreSQL: Changes the default merge schedule to once every minute, matching the existing gen 1 connector behavior.

### Connectors 2026.9.3.1

- Jira Core 0.9.0:
  - Orders duplicate Jira issue updates by the `UPDATED` timestamp so the replicated issue table retains the newest values instead of an arbitrary stale version.
- Oracle Embedded License 0.47.0:
  - Wires the `Concurrent Snapshot Queries` parameter to row-ID snapshot fetching so customers can control snapshot concurrency without editing the flow.
- Oracle Embedded License Public Sector 0.46.0:
  - Wires the `Concurrent Snapshot Queries` parameter to row-ID snapshot fetching so customers can control snapshot concurrency without editing the flow.
- Oracle Independent License 0.46.0:
  - Wires the `Concurrent Snapshot Queries` parameter to row-ID snapshot fetching so customers can control snapshot concurrency without editing the flow.
- SQL Server CDC 0.50.0:
  - Adds clone, truncate, and archive re-snapshot handling when the destination table already exists.
- SQL Server CT 0.53.0:
  - Adds clone, truncate, and archive re-snapshot handling when the destination table already exists.

## September 1, 2026

### Runtime Server 2026.9.1.2

- Security patches and dependency upgrades.
- Upgraded the Runtime UI to version 0.88.0.
  - Gen2 Database CDC: Preserves column-filter configurations that the wizard cannot model by providing a validated raw JSON editor instead of silently dropping or reformatting them.
  - Gen2 Database CDC migration: Re-evaluates destination authentication visibility after migration and waits for the result before allowing the wizard to advance.
- Gen2 connector configuration: Distinguishes missing connector configuration and asset files from transient Snowflake stage failures, and retries transient stage operations instead of silently returning an empty configuration.
- GCP deployments: Enables internal connector stage uploads and downloads through bucket-scoped GCS endpoints, avoiding connector `START_FAILED` errors caused by inaccessible public GCS endpoints.
- Fixed clustered Parameter Context updates when adding provider-backed inheritance.

### Runtime Extensions 2026.9.1.15

- CDC MySQL: Fixed automatic migration from binlog-file position tracking to GTID tracking when the source has purged older binary logs. If purged history cannot be verified safely, migration is deferred and replication continues using binlog positions.
- Gen2 CDC MySQL and PostgreSQL: Connectors now add Snowflake primary key metadata when creating destination tables for source tables with primary keys, except when user-defined logical keys are used.
- Gen2 CDC MySQL and PostgreSQL: Connectors now start correctly on runtimes with a custom NAR installed. Previously, a newly created connector could have an empty flow that could not start.
- CDC Databases: Merge scheduling no longer starts an additional small merge for data queued after the scheduled merge boundary, reducing unexpected warehouse activity and credit consumption.
- Gen2 CDC MySQL and PostgreSQL: After migrating a connector that uses `KEY_PAIR` authentication to a managed-token runtime, `KEY_PAIR` remains selectable so the private key can be re-entered. Switching to `SNOWFLAKE_MANAGED` hides the `KEY_PAIR`-only fields on the next configuration fetch.
- CDC SQL Server: Publishes each table’s committed capture position independently and only after the corresponding NiFi session commits. State publication retries without advancing capture, preventing stale durable positions and missed changes when local-state persistence is delayed or temporarily unavailable.

### Connectors 2026.9.1.1

- Jira Core 0.8.0:
  - Consolidates duplicated per-endpoint ingestion paths into shared run-scoped processing, reducing flow complexity while isolating concurrent ingestion runs.
  - Advances the audit-deletes checkpoint from the latest deletion timestamp fetched instead of the current time, preventing deletion events from being skipped.
- Table Consolidation 0.4.0:
  - Groups consolidated SQL Server tables by resolved source schema and table so equivalent tables from multiple source databases land in one consolidated table with source lineage.
  - Reconciles consolidated table schemas additively when source tables differ, adding missing columns without dropping existing columns so rows from every source can be merged safely.
- Google Drive No Cortex/DWD 0.22.0, No Cortex/No DWD 0.4.0, Cortex/DWD 0.28.0, Cortex/No DWD 0.5.0:
  - Preserves connector ID sequences across runtime restarts, preventing sequence resets and resulting ID conflicts.

## August 28, 2026

### Runtime Operator 0.75.0

- Security patches and dependency upgrades.

### Ingress Controller 2026.8.25-18

- Security patches and dependency upgrades.

### Control Plane Core 0.130.0

- Diagnostic bundle generation is now more reliable — transient failures are automatically retried rather than requiring manual intervention.
- Security patches and dependency upgrades.

### Data Plane Service 0.130.0

- Fixed an issue where connectors were incorrectly shown as idle when activity data was temporarily unavailable.
- Security patches and dependency upgrades.

### Control Plane UI 0.89.0

- Security patches and dependency upgrades.

### Data Plane UI 0.21.0

- Security patches and dependency upgrades.

### Openflow Token Refresher 1.19.0

- Security patches and dependency upgrades.

### AWS Data Plane Agent 1.62.0

- Improved deployment reliability across several common failure scenarios, including slow IAM propagation, certificate drift after upgrades, and Terraform state inconsistencies with custom ingress rules.
- Deployments now automatically recover from membership ring issues that could previously cause stuck or degraded runtime states.
- Security patches and dependency upgrades.

### SPCS Data Plane Agent 1.46.0

- Security patches and dependency upgrades.

## August 25, 2026

### Runtime Server 2026.8.24.20

- Security patches and dependency upgrades.
- Upgraded the Runtime UI to version 0.87.0.
  - Database CDC: Shows the backend-provided failure reason for failed tables in the Reload tables dialog.
  - Connector migration: Gates the Gen1-to-Gen2 Migrate wizard step with the migration runtime setting.
  - Connector migration: Keeps migration discoverable and shows unmet prerequisites when migration is blocked.
  - Connector wizard: Displays stored false values correctly in Boolean toggles and immediately refreshes dependent steps and properties.
  - Connector installation: Adds an in-context prompt that users can copy into CoCo when installing a Gen2 connector.
  - Connector migration: Clarifies why a flow cannot be migrated and simplifies post-migration success feedback.
  - Preserves unsaved Parameter Context changes when navigating to an inherited Parameter Context.
- Connector migration: Records the source Gen1 process group when migration completes, enabling connector-scoped alerts to be migrated to the Gen2 connector.
- Runtime storage and recovery: Caps local-state write-ahead journals at 1 GB to limit disk growth and improve recovery under sustained updates.
- Applies auto-termination changes when a versioned-flow update disconnects a previously connected relationship.
- Validates versioned Parameter names and allows invalid Parameters to be removed.
- Corrects partition-rebalancing lifecycle handling.
- Reloads parameter-driven Connector method classpaths when parameters change.

### Runtime Extensions 2026.8.25.11

- Kafka: Adds FlowFile grouping strategy support to Kafka consumption.
- Table Consolidation: Backfills a table’s existing rows as soon as consolidation is enabled when that table has already reached incremental replication, instead of requiring a subsequent merge.
- CDC PostgreSQL: Fixes CTID snapshots for rows updated during the snapshot. Earlier versions could produce rows with duplicate primary keys under specific PostgreSQL storage conditions.
- CDC Databases: Preserves the earliest commit timestamp during journal compaction so end-to-end replication latency remains accurate.
- CDC PostgreSQL Gen2: Adds a Logical key configuration wizard step for declaring key columns on tables without a primary key or overriding the default key. Configured logical keys cause CDC updates to use MERGE instead of INSERT, preventing duplicate rows.
- MongoDB: Adds opt-in replication of change events larger than 16 MiB on MongoDB 6.0.9 and later. Amazon DocumentDB does not support this mode.
- CDC MySQL Gen2: Adds a Table key configuration wizard step for declaring key columns on tables without a primary key or overriding the default key. Configured logical keys cause CDC updates to use MERGE instead of INSERT, preventing duplicate rows.
- CDC PostgreSQL: Replicates incremental changes for tables and columns with non-ASCII names. Previously, the snapshot succeeded but subsequent inserts, updates, and deletes were silently omitted.
- Snowpipe Streaming: Removes the deprecated `PutSnowpipeStreaming2` processor in favor of `PublishSnowpipeStreaming`.
- CDC PostgreSQL: Prevents connector validation from hanging on the table schema step by removing publication-table validation from that flow-building path.
- CDC MySQL and CDC PostgreSQL: Resolves Execute As Role in every flow-building path, allowing connectors to start correctly after exiting troubleshooting mode.
- Table Consolidation: Groups consolidated rows by source schema and table, allowing the same logical table across tenant databases to be consolidated together while keeping different source schemas separate. This applies to the preview Table Consolidation feature.
- CDC MySQL: Adds an Error Handling Strategy for rows rejected by Snowflake. The default records rejected rows and continues valid-row replication; `Fail Table` stops that table on the first rejected row.
- CDC SQL Server: Retries table listing when SQL Server reports a transient deadlock instead of routing immediately to failure, preventing replication from stalling when connectors enumerate the same source databases concurrently.
- BigQuery: Preserves microsecond precision for TIMESTAMP values ingested by `FetchBigQueryStream` with a Record Writer instead of truncating them to milliseconds.
- CDC PostgreSQL: `SplitPostgreSQLTable` no longer reports an error when it starts against an older PostgreSQL database. If a table is actually split against an unsupported source, that FlowFile is routed to `invalid`. The processor requires PostgreSQL 13 or higher.
- Salesforce Bulk API: Uses a soft target of 500,000 records and subdivides dense query windows before job submission. Subdivision stops at a minimum 24-hour window, so the target is not a hard limit.
- Snowpipe Streaming: Processes a large change-data FlowFile separately when adding it to an existing batch would exceed the configured batch target.

### Connectors 2026.8.25.1

- CDC MySQL 0.58.0: Removes a duplicated failure processor, adjusts queue backpressure, and adds destination primary-key metadata for source tables with real primary keys.
- Oracle Embedded License 0.46.0: Uses `CountTableRows` during snapshot planning and adds destination primary-key metadata for source tables with real primary keys.
- Oracle Embedded License Public Sector 0.45.0: Uses `CountTableRows` during snapshot planning and adds destination primary-key metadata for source tables with real primary keys.
- Oracle Independent License 0.45.0: Uses `CountTableRows` during snapshot planning and adds destination primary-key metadata for source tables with real primary keys.
- CDC PostgreSQL 0.64.0: Uses `CountTableRows` for CTID snapshot planning and adds destination primary-key metadata for source tables with real primary keys.
- CDC SQL Server CDC 0.49.0: Adds destination primary-key metadata for source tables with real primary keys.
- CDC SQL Server CT 0.51.0: Backfills tables that were already in incremental replication when Table Consolidation is enabled.
- Table Consolidation 0.2.0: Backfills tables that were already in incremental replication when consolidation is enabled.

## August 20, 2026

### Control Plane Core 0.129.0

- Security patches and dependency upgrades.
- Tightened permissions on runtime diagnostic bundle download: OWNERSHIP privilege is now required.
- DB CDC connectors can now be deployed on small runtimes with Snowpipe Streaming v2 enabled.
- Fixed a rare issue where a Runtime restart could show success before all pods were healthy.

### Data Plane Service 0.129.0

- Security patches and dependency upgrades.
- Fixed a rare issue where a Runtime restart could show success before all pods were healthy.

### Control Plane UI 0.88.0

- Security patches and dependency upgrades.
- Fixed keyboard usability for searchable select controls with grouped options.

### Runtime Operator 0.74.0

- Security patches and dependency upgrades.

### Ingress Controller 2026.8.18-17

- Security patches and dependency upgrades.

### SPCS Data Plane Agent 1.45.0

- Security patches and dependency upgrades.

### AWS Data Plane Agent 1.61.0

- Security patches and dependency upgrades.
- Fixed an intermittent deployment creation failure caused by IAM role availability
  delays due to eventual consistency.
- Fixed a rare deployment deletion failure that occurred when Custom Resource
  Definitions (CRDs) were absent at destroy time.

## August 18, 2026

### Runtime Server 2026.8.18.9

- Security patches and dependency upgrades.
- Upgraded the Runtime UI to version 0.86.0.
  - Prompted users to save or discard unsaved edits before navigating to an inherited Parameter Context, preventing silent loss of configuration changes.

### Runtime Extensions 2026.8.18.9

- Databases: Added a `CountTableRows` processor that counts rows in a SQL table and stores the result in a configured FlowFile attribute.
- Salesforce: Selected the latest staged snapshot for each Salesforce record during deduplication, preventing stale values from being merged when staging contains multiple snapshots.
- CDC SQL Server: Fixed a rare data-loss window where a captured batch could be silently skipped if the destination commit failed after the batch was read.
- Snowflake: Added an opt-in stream-existence cache to `UpdateSnowflakeStream`, avoiding a redundant DDL statement per FlowFile when using `Create Stream If Not Exists`.

### Connectors 2026.8.18.1

- MongoDB 0.27.0: Used a 60-second Snowpipe Streaming offset-tracking timeout to reduce transient polling failures while data continues flowing.
- CDC MySQL 0.57.0: Used a 60-second Snowpipe Streaming offset-tracking timeout to reduce transient polling failures while data continues flowing.
- Oracle Embedded License 0.45.0: Increased the default snapshot fetch size from 100 to 5,000 rows and used a 60-second offset-tracking timeout.
- Oracle Embedded License Public Sector 0.44.0: Increased the default snapshot fetch size from 100 to 5,000 rows and used a 60-second offset-tracking timeout.
- Oracle Independent License 0.44.0: Increased the default snapshot fetch size from 100 to 5,000 rows and used a 60-second offset-tracking timeout.
- CDC PostgreSQL 0.62.0: Used a 60-second Snowpipe Streaming offset-tracking timeout to reduce transient polling failures while data continues flowing.
- CDC SQL Server 0.48.0: Used a 60-second Snowpipe Streaming offset-tracking timeout to reduce transient polling failures while data continues flowing.
- SQL Server CT 0.49.0: Added optional connector-event publishing for table consolidation and used a 60-second offset-tracking timeout.
- Table Consolidation 0.1.0: Added a flow that consumes connector events and merges snapshot and CDC rows into consolidated destination tables.

## August 13, 2026

### Runtime Extensions 2026.8.17.9

- Oracle CDC: Restored merge performance for tables with user-defined logical keys by reverting to plain equality for key comparison, fixing a full-target-table-scan regression.
- Salesforce: Failed Bulk jobs now included Salesforce’s failure reason in the processor bulletin, making job failures diagnosable without inspecting Salesforce separately.
- CDC PostgreSQL: Added an Error Handling Strategy for rows Snowflake rejects during ingestion. The default `Log Errors and Continue` strategy records rejected rows in the table’s error table while valid rows continue replicating; `Fail Table` stops replication for that table on the first rejected row.
- CDC MySQL and PostgreSQL: Used a 60-second Snowpipe Streaming offset-tracking timeout to reduce transient, self-healing `Polling Failed after 30000 ms` errors while data continues flowing.

### Runtime Server 2026.8.13.16

- Security patches and dependency upgrades.

### Runtime Extensions 2026.8.13.17

- Openflow connectors: Fixed Gen 2 connector configuration for quoted connector names so `DESCRIBE CONNECTOR` no longer adds a second pair of quotes and reports the connector as missing or unauthorized.
- CDC Iceberg: Created integer columns as `LONG` so source integer widening does not require an unsupported Iceberg type change and 64-bit values are represented safely.
- CDC Gen 2 connectors: Connector configuration verification now reports the actual Snowflake error when an External Access Integration cannot be evaluated, instead of incorrectly reporting that no egress Network Rule allows access to the source endpoint.
- CDC MySQL: `CaptureChangeMySQL` can now be switched from Binlog Position to GTID position tracking without losing or replaying events. The connector completes the switch automatically at the next binlog rotation; no manual state cleanup or re-snapshot is required.
- CDC SQL Server: Fixed a rare data-loss window where a Change Tracking batch could be silently skipped if the destination commit failed after the batch was read.
- CDC SQL Server: Snapshot loads of tables with very large rows no longer risk filling runtime disk. Batches stop at a bounded data volume and subsequent batches resume from the exact remaining rows without configuration changes.
- CDC SQL Server: Drains large single-version Change Tracking batches with `Max Batch Size = -1` using one bounded query without an unnecessary sort, reducing `tempdb` pressure during bulk updates.
- CDC PostgreSQL: Fixed replication of large hour-based `INTERVAL` values so Snowflake receives correct ISO-8601 duration strings instead of corrupted negative values.
- Jira: Jira connector record fingerprints now use SHA-256 instead of MD5. Existing records may receive a one-time update after upgrading.

### Connectors 2026.8.13.7

- Veeva Vault 0.7.0: Clarified Direct Data audit-log and ingestion-mode parameter descriptions.
- Salesforce 1.14.0: Removed downstream back pressure after batched Snowpipe Streaming publishing to prevent the Salesforce connector from deadlocking when Snowpipe Streaming errors occur.

## August 11, 2026

### Runtime Server 2026.8.11.2

- Security patches and dependency upgrades.
- Moved from Java 21 to Java 25.
- Upgraded the Runtime UI to version 0.85.0.

### Runtime Extensions 2026.8.11.10

- CDC SQL Server: Added `Max Batch Size = -1` to disable Change Tracking pagination, reducing repeated `CHANGETABLE` evaluation for large backlogs. Enabling `Use Snapshot Isolation` is recommended when using this mode.
- CDC SQL Server: Prevented brief source outages during Azure SQL Managed Instance maintenance or similar failover windows from removing all tables from replication; empty database discovery now retries.
- CDC Oracle: Added multi-PDB replication for users granted `SET CONTAINER`, while preserving existing single-PDB behavior otherwise.
- Salesforce: Formula views now return typed NULL values for formulas referencing unreplicated relationship lookup fields instead of failing view creation.
- CDC SQL Server: Fixed a concurrency race that could cause Change Tracking to silently skip changes for idle tables.

### Connectors 2026.8.11.1

- Dataverse 0.32.0: Added an `Include Formatted Values` parameter so ingestion can include display-friendly formatted values while preserving the original raw values.
- Dataverse 0.32.0: Fixed incorrect `_SNOWFLAKE_ID` values by copying the resolved primary-key value instead of the primary-key field name.
- Salesforce 1.13.0: Special objects now use `queryAll` to ingest archived Task and Event records and soft-deleted records. Existing objects require a connector state reset and full reload to retrieve historical records.
- Salesforce 1.13.0: Retained failed Bulk API query jobs so they remain available for troubleshooting.

## August 6, 2026

### Runtime Server 2026.8.6.2

- Security patches and dependency upgrades.
- Upgraded the Runtime UI to version 0.84.0.
  - Flow Designer: Fixed the load-balance icon rendering outside the connection label box when a connection is actively load-balancing.
  - Flow Designer: Fixed validation-error and comment tooltips closing before the cursor reaches them on the Controller Services, Reporting Tasks, Parameter Providers, and Connectors listings, so users can move onto the tooltip and scroll the full text.

### Runtime Extensions 2026.8.6.2

- Added external assertion (`client_assertion_type` and `client_assertion`) support to `JWTBearerOAuth2AccessTokenProvider` for OAuth2 JWT bearer flows. This unblocks scenarios where Snowflake Workload Identity Federation is used in Openflow to authenticate against services running in AWS while identities are managed in Microsoft Entra.
- Snowflake Connection Service: No longer returns `COPY INTO` result metadata by default. Configure the dynamic property `enableCopyResultSet=true` to opt in to `COPY INTO` result metadata.
- Salesforce: `QuerySFDCObject` can now use Salesforce `queryAll` to retrieve archived Task and Event records and soft-deleted records. Direct processor usage is supported in this release; standard connector-flow wiring ships separately.
- CDC PostgreSQL: Emits a WARN bulletin after creating a replication slot on PostgreSQL 17+ if `synchronized_standby_slots` is not configured on the primary while standbys are connected, or if the created slot unexpectedly lacks `failover=true`. Standalone deployments do not trigger the warning.
- CDC Oracle: Added support for Oracle multi-PDB table listing on AWS RDS Multi-Tenant by routing `MultiDatabaseListTableNames` across multiple Oracle Pluggable Databases when `MultiPdbOracleConnectionPool` from the separately installed Oracle via DMS NAR is configured.
- Oracle via DMS: Introduced a standalone installable `runtime-oracle-dms-processors-nar` with `ProcessChangeFromOracleDMS` and `MultiPdbOracleConnectionPool` for Oracle-to-DMS-to-MSK-to-Openflow pipelines. This NAR requires separate installation and is not shipped in the standard runtime image.
- CDC MySQL: Reads source `TIMESTAMP` values as `LocalDateTime` instead of through the server-timezone-dependent JDBC timestamp path, preventing shifted values in Snowflake snapshots from non-UTC MySQL servers.
- CDC SQL Server: Preserves the original per-row time zone offset of `datetimeoffset` columns when writing to Snowflake `TIMESTAMP_TZ`, instead of converting them to UTC. Values replicated before this change remain in UTC; re-snapshot the table to correct historical rows.
- Dataverse: Microsoft Dataverse table ingestion can now optionally include display-friendly formatted values for choice, status, lookup, currency, and date fields in the `_DATAVERSE_FORMATTED_VALUES` object while preserving the original raw values.
- CDC SQL Server: Logs a repeated WARN with manual remediation SQL when capture-instance rotation is blocked by a missing or non-executable `sf_openflow_cdc_enable_table` or `sf_openflow_cdc_disable_table` wrapper procedure, instead of failing the incremental run.

### Connectors 2026.8.6.1

- CDC MySQL 0.56.0: Set `connectionTimeZone=UTC` and `forceConnectionTimeZoneToSession=true` as JDBC dynamic properties in the connector flow so snapshot timestamps are normalized to UTC regardless of the MySQL server configuration.
- Workday 0.15.0: Fixed intermittent column and data misalignment in Workday RaaS ingestion caused by the API returning fields in non-deterministic order. The `INSERT` now uses column-name matching (`UNION ALL BY NAME`) instead of positional `SELECT *`, preventing data from landing in the wrong columns.

## August 4, 2026

### Runtime Server 2026.8.4.2

- Security patches and dependency upgrades.

### Runtime Extensions 2026.8.4.8

- CDC SQL Server: Fixed a rare data-loss condition where, under concurrent writes and multi-threaded processing, some committed change rows could be skipped. Change reads are now bounded by the committed log watermark so every committed change is captured.
- CDC SQL Server: Fixed an issue where data committed shortly before a schema change could be silently dropped when the connector rotated to a new capture instance.
- CDC SQL Server: Fixed O(n^2) change-table drain performance by making keyset pagination seekable. Users with large or busy tables may have seen steadily increasing end-to-end CDC lag as the change table grew.
- CDC SQL Server: Fixed an issue where lifting a column exclusion filter did not restore the column in downstream replication without restarting the processor.
- CDC SQL Server: Fixed an issue where re-adding a table after schema changes while it was excluded from replication could fail with a data continuity gap.
- CDC SQL Server: The connector now emits an actionable WARN bulletin with manual CDC guidance when automatic capture-instance rotation fails.
- CDC Oracle: Tables replicated with a user-defined logical key whose key columns contain NULLs now merge correctly — updates and deletes match NULL-valued keys instead of missing them.
- CDC Oracle: Tables replicated with a user-defined logical key whose key columns contain NULLs no longer force those columns to NOT NULL in the destination, allowing such rows to load.
- Snowflake: Connectors using the placeholders\_snowflake\_managed merge strategy now use a single-pass journal read for tables with 10 or fewer changed columns, reducing merge compilation time and eliminating a class of internal query errors.
- CDC PostgreSQL: The connector now emits a WARN bulletin when a replication slot is created against a PostgreSQL 17+ standby, indicating that the slot was created without the failover flag and will need to be recreated if the primary fails over.
- CDC Databases: Removed a noisy WARN bulletin that CDC Merge processors could emit when a parameter has not yet been rolled out to a deployment.
- Amazon Ads: The connector now honors Amazon’s rate-limit (HTTP 429) responses. Report status checks that are rate-limited are retried instead of failing, preventing in-progress reports from being abandoned during transient rate limiting.
- MongoDB: Added StandardDocumentDB Service with initial support for connecting to Amazon DocumentDB using an Access Key.

### Connectors 2026.8.4.1

- Salesforce: Removed backpressure before WaitForBulkJobs processor. Backpressure may have caused issues in the gate releasing mechanism that is in place for cost optimization of the warehouse usage when running the merge queries.
- Jira: Standard merge path now takes the \_SNOWFLAKE\_HASH column into account, preventing unnecessary updates when only hash differs.
- Salesforce: Added parameter to enable detailed per-object record operation metrics (created, updated, deleted) for the merge query.

## August 11, 2026

### Control Plane Core 0.128.0

- Security patches and dependency upgrades.

### Data Plane Service 0.128.0

- Security patches and dependency upgrades.

### Control Plane UI 0.87.0

- Security patches and dependency upgrades.

### Data Plane UI 0.20.0

- Security patches and dependency upgrades.

### Runtime Operator 0.73.0

- Security patches and dependency upgrades.

### Ingress Controller 2026.8.10-2

- Security patches and dependency upgrades.

### SPCS Data Plane Agent 1.44.0

- Security patches and dependency upgrades.

### AWS Data Plane Agent 1.60.0

- A requested Deployment upgrade now triggers as soon as possible instead of
  waiting up to 10 minutes.
- Fixed issues that occasionally cause Deployment upgrades and teardowns to fail.
- Security patches and dependency upgrades.

## August 3, 2026

### Control Plane Core 0.127.0

- Security patches and dependency upgrades.

### Data Plane Service 0.127.0

- Fixed an issue causing false Upgrade Failed results when resizing a multi-node Runtime.
- Security patches and dependency upgrades.

### Control Plane UI 0.86.0

- Fixed textareas sometimes displaying as a single line.
- Security patches and dependency upgrades.

### Runtime Operator 0.72.0

- Security patches and dependency upgrades.

### Openflow Runtime Gateway 2026.7.29.14

- Security patches and dependency upgrades.

### Ingress Controller 2026.7.29-14

- Security patches and dependency upgrades.

### Openflow Token Refresher 1.18.0

- Security patches and dependency upgrades.

### SPCS Data Plane Agent 1.43.0

- Improved diagnostic bundle to include runtime certificate and truststore metadata.
- Security patches and dependency upgrades.

### AWS Data Plane Agent 1.59.0

- Fixed a permission issue that caused upgrade failures for deployments using a custom Ingress.
- Improved security group configuration for BYOC Custom Ingress.
- Improved diagnostic bundle to include runtime certificate and truststore metadata.
- Added support for optional recursive DNS nameservers in cert-manager configurations.
- Security patches and dependency upgrades.

## July 30, 2026

### Runtime Server 2026.7.30.2

- Security patches and dependency upgrades.
- Applied `autoResumeState` when scheduling Controller Services so recovery mode can enable controller services.

### Runtime Extensions 2026.7.30.2

- Snowflake: Exposed COPY INTO result metadata through an opt-in connection property and allowed ExecuteSQLStatement to write query result sets as FlowFile content.
- Jira: Added ingestion-completion marker FlowFiles on the `last.page` relationship so Jira connector flows can reliably detect successful completion, including empty result sets.

### Connectors 2026.7.30.1

- Amazon Ads: Fixed incremental ingestion so overlapping report windows delete prior rows before inserting refreshed data, preventing duplicate rows from accumulating.

## July 29, 2026

### Runtime Extensions 2026.7.29.18

- CDC Databases: Added a Max-by aggregate merge strategy for tables without primary-key changes, reducing Snowflake merge compilation time on wide tables by using MAX\_BY aggregation instead of per-column window functions.
- CDC Databases: Fixed runtime restart delays where Table State Services could delay controller-service enablement, causing connector flow synchronization failures after upgrades or restarts.
- CDC PostgreSQL: Accounted for PostgreSQL TOAST data when splitting snapshot reads into CTID chunks, preventing oversized chunks from running for minutes on wide tables with large text or binary columns.

## July 28, 2026

### Runtime Server 2026.7.28.2

- Security patches and dependency upgrades.
- Upgraded the Runtime UI to version 0.83.0.
- Handled migration-created Controller Services as environmental changes in Versioned Flows.

### Runtime Extensions 2026.7.28.12

- CDC SQL Server (CDC): Uses the committed database watermark for idle checkpoints to prevent potential data loss when no changes are flowing.
- CDC Oracle: Allows schema-fetch connection errors to recover gracefully instead of stalling the connector indefinitely.
- Jira Cloud: Skips boards that Jira’s API cannot serve (HTTP 422) instead of failing the entire sync.
- Salesforce: Translates the string + operator as SQL concatenation and resolves cross-object formula operand types from the destination schema.
- CDC Databases: Adaptive insert-only fast path that bypasses MERGE and uses direct INSERT when a batch contains only inserts, improving throughput.
- CDC SQL Server: Exposes replication.key.source property so Change Tracking connectors can derive destination PK metadata from the source.
- CDC SQL Server: Supports tables without primary keys using logical key configuration and unique-key fallback strategy.
- CDC MySQL: GTID position encoding enabling fine-grained deduplication to prevent duplicate rows after restarts.
- CDC MySQL: Server UUID failover detection that automatically detects replica promotion and adjusts replication position.
- CDC MySQL: GTID availability detection that selects binlog or GTID-based replication automatically from the first connection.
- Corrected paging for Branches in BitBucket Flow Registry Client.

### Connectors 2026.7.28.1

- CDC SQL Server (CDC): Wires the Table Key Configuration Service into the connector so customers can declare a logical replication key.
- CDC Oracle, MySQL, & SQL Server: Adds configurable Error Handling Strategy parameter allowing invalid rows to be logged and skipped instead of failing the table.

## July 24, 2026

### Data Plane Service 0.125.1

- Fixed an issue where changing the minimum or maximum number of nodes for a Runtime would incorrectly mark it as “Update Failed” when it actually succeeded.

### AWS Data Plane Agent 1.55.1

- Security patches and dependency upgrades.

### SPCS Data Plane Agent 1.40.1

- Security patches and dependency upgrades.

## July 23, 2026

### Runtime Server 2026.7.23.7

- Upgraded the Runtime UI to version 0.82.0:
  - Fixed create endpoint target form field alignment issues.
  - Sanitized route and query-derived segments in NiFi API URLs to prevent path injection.
  - Included eventId in provenance lineage requests.
  - Addressed security findings: log injection via unvalidated URL params, StoreDevtools exposed in production builds, and sensitive data in error telemetry.
  - Fixed textareas clamped to one line under Angular Material 21.

### Runtime Extensions 2026.7.23.16

- CDC SQL Server: Downgraded transient source-connection failure logs from ERROR to a descriptive WARN with the attached root cause, reducing alert noise during brief network interruptions.
- CDC MySQL: Added support for MariaDB legacy column types that were previously unrecognized during replication.
- CDC Databases (multi-database): Fixed an issue where the Table State Store could run incorrectly on multi-node environments.
- CDC Oracle: Switched ResultSet column access from name-based to index-based lookup to avoid ambiguous column errors.
- Security patches and dependency upgrades.

### Connectors 2026.7.23.1

- Salesforce Bulk API: Added an “Iceberg Version” parameter to the connector flow, allowing users to select Iceberg version 2 or 3 when using Iceberg as the table storage format.

## July 22, 2026

### Control Plane Core 0.125.0

- Enabled Oracle PubSec Connector for eligible accounts.
- Promoted SQL Server CDC to GA.
- Security patches and dependency upgrades.

### Control Plane UI 0.85.0

- Security patches and dependency upgrades.

### Data Plane UI 0.19.0

- Fix alignment in Create Endpoint Target form.
- Enhancements and usability improvements for Gen 2 Connectors and Runtimes (Private Preview).

### AWS Data Plane Agent 1.55.0

- Hardened the Terraform state S3 bucket (`byoc-tf-state-{key}-{Region}`) on every reconcile: enforces AES256 default encryption, blocks public access, and applies a restrictive bucket policy that denies non-TLS access. The agent’s Terraform-managed IAM policy is updated automatically on upgrade to grant the required S3 actions (`s3:PutEncryptionConfiguration`, `s3:PutBucketPublicAccessBlock`, `s3:PutBucketPolicy`, and their Get/Delete counterparts).

  **Note:** If your AWS account is governed by an AWS Organizations Service Control Policy (SCP) that explicitly denies `s3:PutEncryptionConfiguration`, `s3:PutBucketPublicAccessBlock`, or `s3:PutBucketPolicy` on the state bucket, the upgrade will fail with a 403 AccessDenied error. An SCP explicit deny overrides IAM allows, so you must add a scoped SCP exception for the Openflow agent role `openflow-agent-role-{key}` on the state bucket resource (or an equivalent SCP exception) before upgrading to 1.55.0.
- Fixed intermittent installation failures in regions with slower IAM propagation, preventing AccessDenied errors on secretsmanager:GetRandomPassword during fresh installs.
- Security patches and dependency upgrades.

### SPCS Data Plane Agent 1.40.0

- Security patches and dependency upgrades.

### Runtime Operator 0.69.0

- Fixed an issue that prevented updates for multi-node Runtimes using custom NARs.

### Data Plane Service 0.125.0

- Security patches and dependency upgrades.

### Ingress Controller 2026.7.22-0

- Security patches and dependency upgrades.

### Openflow Runtime Gateway 2026.7.22-0

- Security patches and dependency upgrades.

### Openflow Token Refresher 1.17.0

- Security patches and dependency upgrades.

## July 20, 2026

### Control Plane Core 0.124.0

- Fixed case where a Snowflake Deployment can get stuck in UPGRADING state.
- Fixed issue where a Snowflake Deployment won’t heal from Upgrade Failed to Active if its version already matches the latest available version.
- Fixed case where a Runtime in Upgrade Failed state doesn’t refresh its upgrade available flag if a new version is released.
- Renamed SQL Server connector to SQL Server CT.
- Security patches and dependency upgrades.

### Data Plane Service 0.124.0

- Improved Runtime Upgrade reliability by waiting for NiFi cluster connected nodes before creating Snowflake Connection Service during the upgrade.
- Security patches and dependency upgrades.

### Control Plane UI 0.84.0

- Conditional recovery mode option for Upgrade and Resume dialogs.
- Security patches and dependency upgrades.

### Data Plane UI 0.18.0

- Security patches and dependency upgrades.

### Runtime Operator 0.68.0

- Security patches and dependency upgrades.

### Openflow Runtime Gateway 2026.7.14.19

- Security patches and dependency upgrades.

### Ingress Controller 2026.7.17-19

- Security patches and dependency upgrades.

### Openflow Token Refresher 1.16.0

- Security patches and dependency upgrades.

### SPCS Data Plane Agent 1.39.0

- Fixed race condition during upgrade readiness checks to improve reliability of Deployment upgrade.
- Reduced agent heartbeat frequency from 30 seconds to 1 minute to reduce load and align with AWS agent frequency.
- Security patches and dependency upgrades.

### AWS Data Plane Agent 1.54.0

- Refreshed diagnostic bundle script to capture the latest components including Openflow Ingress Controller.
- Supported Agent Host OS refresh during upgrade flow.
- Security patches and dependency upgrades.

## July 21, 2026

### Runtime Server 2026.7.21.8

- Security patches and dependency upgrades.
- Increased the CDC metrics cardinality limit from 50,000 to 75,000 time-series entries, preventing metric ingestion failures for customers with high numbers of replicated tables.
- Upgraded the Runtime UI to version 0.81.0:
  - Adds support for creating a new branch directly from the UI when saving a flow version via Flow Registry Clients.
  - Adds a Flow Version Diff View in the change-version dialog, letting users compare what changed between two flow versions before upgrading.

### Runtime Extensions 2026.7.21.11

- Snowflake: The Snowflake Parameter Provider can now resolve external secrets stored in Azure Key Vault via a Snowflake security integration, in addition to the existing AWS Secrets Manager support.
- CDC SQL Server CT: Fixes a bug where the primary-key cursor value for one table could leak into a different table’s Change Tracking position query. When the leaking table had a bigint primary key and the target table had an int key, the connector would bind an out-of-range value into an integer predicate and fail with SQL Server error 8115 (“Arithmetic overflow error converting expression to data type int”), causing affected tables to be permanently marked FAILED.
- CDC SQL Server CDC: Fixes an infinite retry loop triggered when a SQL Server CDC column undergoes an incompatible type change applied via a CDC disable → ALTER COLUMN → re-enable cycle. The connector now detects the schema change, emits a DDL event with the new column definition, and resumes replication.
- CDC Databases: Tables that fail replication permanently (for example, tables missing a primary key) now remain in the FAILED state and are no longer inadvertently re-queued for snapshot replication by concurrent processors.
- CDC SQL Server & Oracle: Batches multiple table-state removal operations into a single write during cleanup, reducing state I/O overhead when many tables are removed at once.
- Salesforce: Adds a new FetchSFDCBlobContent processor that resolves Salesforce URL sentinels in blob fields (such as Attachment.Body and ContentVersion.VersionData) by calling the Salesforce content endpoint and replacing each sentinel with base64-encoded binary content.
- Salesforce: Extends the formula view to support chained formula fields — formula fields that reference other formula fields, including cross-object chains.
- Salesforce: Formula view columns that could not be translated now include the original Salesforce formula expression in their failure comment, making it easier to understand which construct was unsupported.

### Connectors 2026.7.21.1

- CDC MySQL, CDC PostgreSQL, CDC SQL Server, and Oracle: Adds an “Iceberg Version” parameter to database connector flows. When using Iceberg as the table storage format, users can now select Iceberg version 2 or 3.
- Salesforce Bulk API: Adds support for capturing and ingesting binary blob fields (such as Attachment.Body and ContentVersion.VersionData) from Salesforce objects.
- Atlassian Jira Core: Adds four lookup tables (STATUS, PRIORITY, RESOLUTION, and ISSUE\_TYPE) alongside the existing ISSUE fact table, containing human-readable names for the numeric IDs previously stored on ISSUE. This unblocks customers who need to join Jira reference data to issue records.

## July 16, 2026

### Runtime Server 2026.7.16.2

- Security patches and dependency upgrades.

### Runtime Extensions 2026.7.16.14

- CDC SQL Server: Verifies at startup that the required CDC wrapper stored procedures exist and the configured role has `EXECUTE` permission, providing actionable errors instead of runtime failures.
- CDC SQL Server: Hardened SQL Server CDC enable and disable wrapper scripts to work correctly in Azure singleton configurations.
- Jira: Fixed the default field value in `FetchJiraResolutions` so the correct field is selected on first run without manual configuration.
- CDC PostgreSQL: Stopped setting the `failover` flag on replication slots on standby servers where that flag is not permitted, preventing slot creation failures.
- CDC MySQL, CDC PostgreSQL: Verifies at startup that the execute-as role has write permission on the destination database, surfacing access issues before replication begins.
- Snowflake Processors: Added an Iceberg Version property to `UpdateSnowflakeTable` to control which Iceberg format version is written.
- CDC SQL Server: Detects when the SQL Server CDC retention purge removes unconsumed records and triggers an inventory refresh to recover automatically.
- Snowpipe Streaming: Changed HTTP 429 and 503 throttling responses from error to info level, reducing alert noise during normal Snowflake backpressure.
- CDC PostgreSQL: Disconnects the replication stream on SQL exception, preventing the connector from hanging on a broken connection.

### Connectors 2026.7.16.1

- CDC MySQL, CDC PostgreSQL, CDC SQL Server, CDC Oracle: Changed the default merge schedule from once per hour to once per minute for all database connectors, reducing data latency with default settings.
- CDC MySQL, CDC PostgreSQL: Removed the “Schedule Warehouse” processor step from MySQL and PostgreSQL connector flows, simplifying the pipeline.
- CDC PostgreSQL: Added a Dead Letter Queue (DLQ) to the PostgreSQL CDC connector, routing failed records to a separate queue instead of blocking replication.
- Salesforce: Fixed view creation for Salesforce formula fields with cross-object references that previously caused incorrect or failed view generation.

## July 14, 2026

### Runtime Server 2026.7.14.2

- Security patches and dependency upgrades.
- Fixed a load-balanced connection desynchronizing socket after an in-flight transaction was unregistered.
- Added Flow Registry Client Synchronization Interval property.

### Runtime Extensions 2026.7.14.2

- Salesforce — Fixed formula view compilation failures that occurred when a formula field references a non-replicated column or related object.
- Salesforce — Fixed incorrect SQL generated by the ISBLANK and BLANKVALUE operators for DATE, TIMESTAMP, and numeric formula fields.
- CDC Oracle — Fixed an issue where CaptureChangeOracle stalled after encountering invalid log positions following a node restart.
- CDC Oracle — Isolated per-table schema conversion failures in CaptureChangeOracle so that an error on one table no longer halts incremental ingestion for all other tables.

### Connectors 2026.7.14.1

- Salesforce — Fixed jobs not being marked as FAILED when the Salesforce Bulk API is unreachable during result retrieval.
- Salesforce — Split large outbound FlowFiles into bounded chunks to prevent oversized Snowpipe Streaming v2 fragments during replication.

## July 9, 2026

### Runtime Server 2026.7.9.19

- Security patches and dependency upgrades.
- Fixed a flow synchronization failure that occurred when a Parameter Provider-backed Parameter Context contained a parameter not flagged as provided.

### Runtime Extensions 2026.7.9.19

- CDC Databases — Reconciled single-database and multi-database TableStateChangeReason handling. As a result, some error codes between 4025 and 4035 might indicate different failure reasons than they did before.
- CDC PostgreSQL — Added support for PostgreSQL 17+ major-version upgrades and failovers.
- CDC Databases (multi-database) — Added a configurable merge schedule to the multi-database journal merge processor.
- CDC Databases — Added merge schedule configuration to the MergeSnowflakeJournalTable processor.
- CDC Oracle — Oracle’s unbounded NUMBER type is now mapped to DECFLOAT.

### Connectors 2026.7.9.18

- Salesforce — Added Snowflake Managed Iceberg table format support to the Salesforce Bulk API connector (preview).
- BigQuery — Improved column selection for the BigQuery journal.

## July 7, 2026

### Control Plane Core 0.122.0

- Fixed automatic upgrades of Snowflake Deployments prematurely transitioning to Active
  while an upgrade is still progressing.
- Fixed automatic upgrades of Snowflake Deployments incorrectly moving to Not Reporting state
  instead of Upgrade Failed when the Deployment is unhealthy.
- Security patches and dependency upgrades.

## July 6, 2026

### Runtime Server 2026.7.6.18

- Security patches and dependency upgrades.
- Newly added Controller Services are now enabled automatically when you upgrade a version-controlled flow.

### Runtime Extensions 2026.7.6.18

- Kinesis — Fixed a lingering rename lock that could remain after an error in ConsumeKinesis.
- CDC SQL Server — Large partitioned tables can now be snapshotted partition by partition, so initial loads run faster and a failure affects only one partition.
- CDC SQL Server — Snapshot fetch automatically uses a partition-aware strategy when partition information is available.
- CDC SQL Server — Snapshot completion tracking is now configurable (count- or marker-based) to support partition-aware loading.
- CDC SQL Server — Transient Change Tracking errors are now retried before a table is marked failed, avoiding manual re-snapshots.
- CDC PostgreSQL — Re-snapshotting a table that already exists in Snowflake now refreshes it in place instead of failing.
- CDC PostgreSQL and Oracle — Dates with years outside Snowflake’s supported range are now adjusted to the nearest valid value instead of failing the load.
- CDC Oracle — Fixed a slow schema-discovery query on databases with very large numbers of tables.
- CDC Databases — Added a Snowflake-managed option that automatically selects the best merge strategy per table based on its column count.
- Dataverse — Restored the last-page indicator on the Fetch Microsoft Dataverse Table processor.

### Connectors 2026.7.6.17

- CDC SQL Server — Connector flows now use partition-aware snapshot loading for faster initial loads of large partitioned tables.
- Oracle — Added an Oracle connector variant for public-sector deployments (embedded license).
- Salesforce — Migrated the Salesforce Bulk API connector to the newer, more reliable ingestion path (Snowpipe Streaming v2).
- CDC MySQL, Oracle, and PostgreSQL — Tuned connection pool sizing to prevent connection exhaustion during snapshots.

## June 30, 2026

### Control Plane Core 0.121.1

- Fixed an issue causing Runtime deletion failures in some old AWS deployments.

### Runtime Operator 0.65.0

- Fixed an issue that blocked Runtime upgrades when a scaling-down cluster node reconnected to the
  cluster before being fully stopped.
- Security patches and dependency upgrades.

### AWS Data Plane Agent 1.51.0

- Fixed an issue that blocked upgrades of older BYOC deployments due to conflicts with the
  metrics server deployment.
- Security patches and dependency upgrades.

### SPCS Data Plane Agent 1.36.0

- Improved resource utilization for high telemetry use cases.

### Runtime Server 2026.6.30.15

- Security patches and dependency upgrades.
- Gen 2 Connectors: You can now use secrets stored in AWS Secrets Manager (through Snowflake) for connector credentials.

### Runtime Extensions 2026.6.30.15

- CDC MySQL — You can now tell the MySQL connector which column(s) uniquely identify each row, so change capture works on tables that don’t have a primary key.
- Shopify — Added a new sign-in option (client-credentials / custom app) for connecting to Shopify.
- CDC SQL Server — When the connector hits a SQL Server error it can’t retry, it now records clearer details so you can understand why ingestion stopped.
- CDC Databases — Large rows are now compressed as they are read, lowering memory use and improving performance when capturing wide tables.
- CDC Oracle — Fixed a problem where checking an Oracle connection could fail because the database driver wasn’t loaded; validation now works reliably.
- CDC PostgreSQL — You can now tell the PostgreSQL connector which column(s) uniquely identify each row, so change capture works on tables without a primary key.
- Snowpipe Streaming — Added support for Elastic Channels, which scale automatically to handle higher streaming volumes.
- Snowpipe Streaming — Compressed (zstd) input is now detected and handled automatically, so no extra setup is needed.
- CDC Databases — When capturing from multiple databases, you can now choose how changes are merged into Snowflake (Snowflake-managed or adaptive).

### Connectors 2026.6.30.15

- CDC MySQL and PostgreSQL — Connector flows now support user-declared keys end to end, so you can capture changes from tables without a primary key.
- Shopify — Connector flow now supports the new client-credentials sign-in option.
- CDC Oracle — Fixed setup so the tracking-table creation step runs in the right order, avoiding occasional setup failures.
- CDC Oracle — Made the connector faster by increasing parallelism and tuning how data is fetched.

## June 29, 2026

### Runtime Server 2026.6.29.22

- Fixed an issue that prevented Runtimes on versions 2026.6.22 - 2026.6.25 from scaling down properly.

## June 26, 2026

### Control Plane Core 0.121.0

- Oracle CDC connector with an upfront payment option is now available in the connector catalog (Private Preview).
- MongoDB connector is now available in the connector catalog (Public Preview).
- Force-delete support for Gen 2 connectors: operators can now terminate connectors stuck in a failed state
  via a force flag on the delete API, triggering a full NiFi queue drain and purge before resource removal.
- Security patches and dependency upgrades.

### Control Plane UI 0.83.0

- New connector troubleshooting states and task types are now recognized and surfaced in the UI.
- “Go to Observability” shortcut from the connector listing navigates directly to Snowsight monitoring.
- Fixed an issue where the Snowsight deep-link URL was malformed on accounts whose account URL carries
  the SPA hash prefix.
- “Add” button renamed to “Install” in the Select Runtime connector dialog for clarity.
- Security patches and dependency upgrades.

### Data Plane Service 0.121.0

- Enabled Gen 2 connector troubleshooting workflow using NiFi troubleshooting mode.
- Connector deletion now purges NiFi queues and drains active processing before removing resources.
- Improved support for installing Gen 1 connectors for users with many roles.
- Security patches and dependency upgrades.

### Data Plane UI 0.17.0

- Security patches and dependency upgrades.

### Runtime Operator 0.64.0

- Security patches and dependency upgrades.

### Openflow Runtime Gateway 2026.6.25.18

- Security patches and dependency upgrades.

### AWS Data Plane Agent 1.50.0

- Fixed an issue where a deployment upgrade that eventually succeeds would prematurely report an
  upgrade failure due to transient AWS API errors during the EKS upgrade process.
- Security patches and dependency upgrades.

### SPCS Data Plane Agent 1.35.0

- Security patches and dependency upgrades.

## June 25, 2026

### Runtime Server 2026.6.25.16

- Security patches and dependency upgrades.

### Runtime Extensions 2026.6.25.16

- CDC MySQL, CDC PostgreSQL: Fixed a silent data-loss issue where re-running an initial snapshot could reuse a stale streaming channel and skip rows; snapshot channels are now uniquely identified per run.
- CDC MySQL: Fixed a crash where an empty binary JSON value in the MySQL binlog permanently failed the entire table; the connector now maps empty binary JSON values to NULL and continues replication.
- CDC Databases: Removed spurious schema-checksum error log entries that appeared after a source table was dropped.

### Connectors 2026.6.25.16

- SharePoint: Made page-splitting during OCR of multi-page documents a configurable parameter on the SharePoint connectors.
- SharePoint: Added chunk size and chunk overlap parameters to the SharePoint Cortex AI connectors for controlling how document text is segmented before embedding, enabling tuning for RAG and vector-search retrieval quality.
- CDC PostgreSQL: Added a CTID-based snapshot strategy for PostgreSQL 14+ that enables faster initial snapshots on large tables and tables without a primary key.
- CDC MySQL: Snapshots against an existing Snowflake table now archive the table as a zero-copy clone, then truncate and reload in place instead of failing, preserving attached Snowflake streams so CDC resumes automatically after the snapshot.

## June 23, 2026

### Runtime Server 2026.6.23.15

- Security patches and dependency upgrades.

### Runtime Extensions 2026.6.23.15

- Added Hex header encoding option to `ConsumeKafka`.
- Jira: Adds `FetchJiraIssueTypes`, `FetchJiraPriorities`, `FetchJiraResolutions`, and `FetchJiraStatuses`
  processors for looking up Jira metadata dictionaries in flows.
- CDC SQL Server: Fixes tables being permanently evicted to `FAILED` during SQL Server Multi-AZ/AG failover
  by marking inaccessible databases as `UNAVAILABLE` instead of dropping them.
- CDC Oracle: Fixes list-tables and license-validation queries to be compatible with Oracle 11.2.0.4.
- CDC PostgreSQL: Adjusts partition size limits, timeout settings, and query generation in
  `SplitPostgreSQLTable` and `FetchRowsByCtid`.
- CDC SQL Server: Fixes a permanent arithmetic overflow (8115) when computing the last-row commit time
  by executing the timestamp lookup in a separate standalone query.
- CDC Databases (multi-database): Fixes an out-of-memory error in snapshot by deferring catalog restore
  until after the ResultSet is fully consumed.
- Snowpipe Streaming: Fixes `ALTER TABLE` statements in `UpdateSnowflakeTable` being routed to
  “table exists”; they are now correctly routed to “failure”.
- CDC Oracle: Fixes license validation to look up historical database IDs so connectors remain valid
  after a database migration.
- CDC PostgreSQL: Adds `SplitPostgreSQLTable` and `FetchRowsByCtid` processors enabling CTID-based
  parallel table snapshot.
- CDC PostgreSQL and CDC MySQL 2nd Gen: Connector verification only attaches error messages to a field
  when the error is directly caused by that field.

### Connectors 2026.6.23.15

- CDC PostgreSQL: Adds a group-snapshot-by-primary-key step to the connector flow.
- CDC PostgreSQL: Adds clone-and-truncate snapshot promotion strategy to the connector flow.

## June 18, 2026

### Runtime Extensions 2026.6.18.9

- Snowpipe Streaming: Added per-batch error and invalid row counts as FlowFile attributes in
  Snowpipe Streaming v2 processors, allowing downstream flows to react to partial delivery
  failures.
- CDC Oracle (multi-database): Added support for Oracle 11.2.0.4 by handling the absence of
  the `USER_GENERATED` column in `ALL_TAB_COLS` when listing columns for replication.
- CDC Databases: Added rows-inserted and rows-updated counters to MergeSnowflakeJournal
  processors so throughput metrics are visible per processor.
- CDC SQL Server (multi-database): Fixed slow keyset pagination scans on busy change tables
  by aligning the CDC query ordering with the SQL Server clustered index key order.
- CDC Databases: Fixed missing failure reasons for clone-and-truncate snapshot promotion
  failures. `SCHEMA_RECONCILE_FAILED`, `CLONE_TO_ARCHIVE_FAILED`, and
  `TRUNCATE_DESTINATION_FAILED` are now correctly persisted in the table state.
- Jira: Fixed column names for Jira custom fields whose display names start with a digit;
  the leading digit was previously dropped from the resulting column name.
- CDC Oracle (multi-database): Reduced the XStream batch acknowledgment interval to improve
  progress tracking speed and allow faster detach during pauses.
- CDC SQL Server: Reduced memory overhead when replicating binary column types (`binary`,
  `varbinary`, `image`, `hierarchyid`) by avoiding large intermediate allocations during
  JSON serialization.

### Connectors 2026.6.18.9

- CDC SQL Server (multi-database): Added Iceberg table storage format support to the SQL
  Server multi-database CDC connector, enabling Iceberg-format destination tables.

## June 17, 2026

### Control Plane Core 0.120.0

- Added support for upgrading runtimes in Recovery Mode, which skips automatically starting
  the flow when it is preventing the runtime from fully upgrading.
- Security patches and dependency upgrades.

### Control Plane UI 0.82.0

- Introduced Gen 2 indicators and filters throughout the UI to differentiate between Gen 1
  and Gen 2 resources.
- Added Recovery Mode option during the Upgrade Runtime action.
- Fixed manage access dialog privilege label wrapping and row misalignment.
- Updated text for disabled Deployment options to “Not available”.
- Filtered out non-Gen 2 Runtimes when installing Gen 2 Connectors.
- Security patches and dependency upgrades.

### Data Plane Service 0.120.0

- Added support for upgrading runtimes in Recovery Mode, which skips automatically starting
  the flow when it is preventing the runtime from fully upgrading.
- Security patches and dependency upgrades.

### Runtime Operator 0.63.0

- Security patches and dependency upgrades.

### Openflow Runtime Gateway 2026.6.12.19

- Security patches and dependency upgrades.

### Ingress Controller 2026.6.11-13

- Security patches and dependency upgrades.

### Openflow Token Refresher 1.15.0

- Security patches and dependency upgrades.

### AWS Data Plane Agent 1.49.0

- Improved diagnostics bundle to include directory walk and system service status.
- Increased metrics support for CDC Connectors with large numbers of tables in replication.
- Upgraded Openflow BYOC to use the latest AWS EKS 1.36.
- Security patches and dependency upgrades.

### SPCS Data Plane Agent 1.34.0

- Security patches and dependency upgrades.

## June 16, 2026

### Runtime Server 2026.6.16.13

- Upgraded the Openflow UI frontend from 0.76.0 to 0.78.0. Notable improvements include:
  - Added the ability to run, stop, and change the run status of individual components via the
    context menu in connector troubleshooting mode.
  - Added support for upgrading connectors in recovery mode from the runtime canvas.
  - Added a “View Documentation” action for processors directly from the connector canvas.
  - Enabled editing component configuration from the canvas configure dialogs.
  - Added support for dragging a connection endpoint to a new destination processor.
  - Added “Go to Source” and “Go to Destination” navigation actions for connections on the canvas.
  - Added access to Processor Advanced custom UI in connector troubleshooting mode.
  - Fixed canvas SVG transform producing `scale(Infinity)` when two components are placed at the
    same position, causing them to overlap.
  - Fixed an issue preventing deselection of a currently selected component.

### Runtime Extensions 2026.6.16.10

- SharePoint: Added optional extended metadata fetching, allowing additional SharePoint item
  properties to be included in the data extracted by the connector.
- CDC MySQL, CDC PostgreSQL: Capped the number of concurrent queries at 8 to prevent resource
  exhaustion under heavy load.
- CDC Oracle: Fixed a CaptureChangeOracle processor failure during connection verification when
  SSL is enabled.
- CDC MongoDB: Fixed a snapshot and CDC ID mismatch for MongoDB Date and Binary BSON types that
  could cause data inconsistencies.
- CDC Databases: Fixed a stray SQL comma in the JOURNAL\_CHANGES CTE generated when all payload
  columns are primary key columns, preventing merge query failures.
- CDC PostgreSQL: Added validation in the Summary setup step to ensure all configured tables
  exist in the PostgreSQL publication.
- CDC PostgreSQL: Added WAL level validation during connector setup with clearer error messages
  when the replication level is insufficient.
- CDC MySQL: Added a TableStorageFormat configuration option to the Gen 2 MySQL Connector for
  controlling the destination table storage format.

### Connectors 2026.6.16.9

- CDC PostgreSQL, CDC MySQL, CDC Oracle, CDC SQL Server: Updated snapshot channel groups to use
  the `table.state.created` event, improving snapshot lifecycle reliability.
- CDC Oracle — Adds a TableStorageFormat configuration option to the Oracle Connector for
  controlling destination table storage format. This adds support for snowflake managed catalog
  iceberg destination.

## June 12, 2026

### Runtime Server 2026.6.12.19

- Security patches and dependency upgrades.

### Runtime Extensions 2026.6.12.19

- CDC MySQL: Added a configurable Destination Schema Strategy, allowing users to control how
  source schemas map to Snowflake destination schemas (for example, use only the source schema
  name, add a prefix or suffix, or apply a custom pattern), matching the capability already
  available in the CDC PostgreSQL connector.
- Snowpipe Streaming: Fixed spurious “Invalid Rows” warnings and incorrect routing of FlowFiles
  to the INVALID relationship caused by the error count not being initialized from the streaming
  channel when creating a status placeholder.
- CDC PostgreSQL: Improved cron schedule validation error messages to be accurate and
  user-friendly, and added support for cron macros such as @hourly and @daily.

### Connectors 2026.6.12.17

- MongoDB: Removed the separate AddSnowflakeSpecificColumns processor from the Snapshot flow,
  integrating that behavior directly into FetchMongoDBConnectionSnapshot for improved performance.

## June 11, 2026

### Runtime Server 2026.6.11.18

- Security patches and dependency upgrades.

### Runtime Extensions 2026.6.11.18

- Jira: Reduced memory consumption in all Jira processors by streaming API responses rather
  than loading entire paginated results into memory at once.
- Shopify: Applied code-review fixes and cleanup to the Shopify connector, including
  improvements to schema derivation, rate-limit handling, and sync state management.
- MongoDB CDC: Added record metadata fields to the FetchMongoDBCollectionSnapshot processor
  output, including source information such as namespace, timestamp, and operation type.
- Snowpipe Streaming: Fixed an incorrect date conversion caused by Julian calendar arithmetic
  in the Snowflake type converter, ensuring dates are consistently handled using the proleptic
  Gregorian calendar.

### Connectors 2026.6.11.16

- Excel: Added a staging table step to Excel (S3 and SharePoint) connector flows, enabling
  more reliable data loading before the final merge into the target table.
- MongoDB: Migrated the MongoDB connector to Snowpipe Streaming v2 and removed the deprecated
  “Merge into Bigger” feature flag.
- MongoDB CDC: Enabled the WaitForSnapshotCompletion processor in both snapshot and incremental
  flow phases, improving coordination when a snapshot must complete before incremental
  processing begins.
- CDC SQL Server (multi-database): Set the ListDatabaseTables processor output data format to
  Grouped, fixing an inconsistency with the expected connector behavior.
- Google Drive: Added automatic retry logic for transient Google Drive API failures, reducing
  connector errors caused by intermittent API unavailability.

## June 9, 2026

### Runtime Server 2026.6.9.14

- Security patches and dependency upgrades.

### Runtime Extensions 2026.6.9.17

- CDC PostgreSQL: Added a Destination Schema Strategy option, giving users control over
  how source database schemas map to Snowflake destination schemas (for example, use only
  the schema name, prefix with the database name, or apply a fixed custom name), matching
  the capability available in the MySQL CDC connector.
- CDC Databases: Added a `table.state.created` timestamp attribute to FlowFiles produced
  when a new table is added to CDC replication state, enabling downstream processors to
  distinguish newly-tracked tables and supporting stable Snowpipe Streaming channel naming
  across table removal and re-add operations.
- Security patches and dependency upgrades.

### Connectors 2026.6.9.9

- CDC Oracle and SQL Server: Flattened Oracle (embedded and independent license) and SQL
  Server multi-database connector flows to simplify the flow structure and remove obsolete
  parameters.

## June 4, 2026

### Runtime Server 2026.6.4.18

- Security patches and dependency upgrades.
- Fixed date conversion for consistent use of the Proleptic Gregorian Calendar.
- Added a size limit to the Standard Content Viewer.
- Upgraded the UI frontend to version 0.76.0:
  - Added support for import/export of flow definitions including component state.

### Runtime Extensions 2026.6.4.18

- Added Parsing Strategy to `JsonTreeReader` and `JsonPathReader` with a Lenient
  option.
- CDC MySQL: Introduced the initial MySQL CDC Connector based on the same
  architecture as the PostgreSQL CDC connector.
- Shopify: Introduced a new Shopify source connector.
- CDC Databases: Added a `SNOWFLAKE_MANAGED` merge strategy for the FULL journal
  type (`ReducedJournalRead` mode), reducing compile time and bytes scanned.
- CDC Oracle and SQL Server: Flattened DML record structure to skip the Enrich
  processor, simplifying the pipeline.
- CDC Databases: Added aggregate table status metrics reporting so operators can
  monitor the health of multiple CDC tables in one view.
- CDC MongoDB: Migrated to `DirectJsonRecordWriter`, improving record writing
  performance and consistency.
- Snowpipe Streaming: Deprecated the legacy `PutSnowpipeStreaming2` processor in
  favor of `PublishSnowpipeStreaming`.
- CDC Databases: Increased fetch size in `MultiDatabaseListTableNames` to improve
  performance when listing a large number of tables.
- CDC Databases: Ported sub-chunk part counting to `WaitForSnapshotCompletion`,
  improving snapshot progress tracking.
- Dataverse: Refactored pagination loop for more efficient flow file handling.
- SharePoint: Fixed a `NullPointerException` in `FetchSharepointFile` when the
  `Retry-After` response header is absent.
- CDC Databases: Fixed error handling in `getConnection()` within
  `MergeSnowflakeJournalTable` to prevent silent failures.
- CDC SQL Server: Added graceful handling of Change Tracking expiration for
  inactive databases, preventing pipeline failures.
- CDC SQL Server: Added proper non-retryable exception handling to prevent CDC
  tables from being stuck in an error loop.
- CDC Oracle: Excluded index-organized table segments from Oracle table listing to
  prevent spurious tables from appearing in the connector.
- CDC Databases: Added missing query status handling in explicit response
  processing to prevent unhandled state transitions.

### Connectors 2026.6.4.15

- Shopify: Added versioned flows for the new Shopify source connector.
- Dataverse: Tables are now moved to a FAILED status when an error does not
  recover, preventing silent data loss and alerting operators to problems.
- Dataverse: Improved merge scheduling by adding a `GateFlowFile` processor to
  handle scheduling, reducing unnecessary flow file releases.

## May 22, 2026

### Runtime Extensions 2026.5.22.12

- CDC SQL Server: Added configurable properties to control which metrics are
  logged during change tracking capture.
- Snowpipe Streaming: Fixed a `NoClassDefFoundError` when using HTTP/HTTPS
  proxies or Azure internal stages by restoring Netty proxy classes to the
  Snowflake JDBC NAR.
- CDC MySQL: Added Iceberg type override support with unsigned integer handling
  and proper bit-width mapping for MySQL source columns.
- Snowflake: Added a Snowflake Provenance Reporting Task that streams Openflow
  provenance events to Snowflake via Snowpipe Streaming v2.
- Snowpipe Streaming: Reduced log message size for PutSnowpipeStreaming failures
  by logging FlowFile IDs instead of full object references.
- CDC PostgreSQL: Added proper Iceberg type mapping for PostgreSQL integer types
  using bit-width and temporal precision fields.
- CDC Databases: Added bitWidth and temporalPrecision fields to Column for
  improved schema fingerprinting (v2) without affecting existing v1 connectors.

## May 21, 2026

### Runtime Server 2026.5.21.15

- Security patches and dependency upgrades.

### Runtime Extensions 2026.5.21.16

- CDC Oracle: Adds support for multiple databases in Oracle CDC connector.
- CDC Databases: Adds an adaptive placeholder merge strategy that optimizes
  merge query performance by reducing journal reads.
- CDC SQL Server: Throws a permanent failure when the change tracking version
  expires due to retention, providing a clear error and marking the table as
  failed.
- Salesforce: Allows currency fields to be treated as float type in the
  Salesforce describe object operation.
- Snowpipe Streaming: Adds wait time information to retry log messages for
  better troubleshooting.
- All connectors: Fixes managed authentication for BYOC deployments in the
  Snowflake Connection Service.

### Connectors 2026.5.21.15

- Dataverse: Increases max retry attempts on the Dataverse API to improve
  resilience.
- Jira: Fixes the handling of deleted issues in the Jira Core connector.
- CDC SQL Server: Adds parameters for Metrics Enabled, Max Batch Size, and Read
  Timeout.
- MongoDB: Changes Schema Access Strategy to infer schema in the MongoDB
  connector.
- CDC Oracle: Strips table selection criteria attributes for Oracle connectors to
  fix upgrade issues.

## May 20, 2026

### Control Plane Core 0.116.1

- Improved reliability of Deployment and Runtime actions.
- Security patches and dependency upgrades.

### Data Plane Service 0.116.0

- Fixed rare case of Runtime Upgrade Failure determination happening too soon
  while the upgrade is still processing.
- Security patches and dependency upgrades.

### Control Plane UI 0.81.0

- Changed “Snowflake Role” label to “Execute as role” terminology.
- Fixed hint for runtimes in the connector install dialog.
- Fixed error not shown when querying for the listing of Connectors.
- Preserve original route when user is redirected to authenticate.
- Fixed issue preventing the link in the hint from opening in connector install
  dialog.
- Security patches and dependency upgrades.

### Data Plane UI 0.16.0

- Security patches and dependency upgrades.

### AWS Data Plane Agent 1.44.0

- Fixed internal certificate renewal process for Openflow Ingress Controller.
  All customers running BYOC Deployments 1.31.2 - 1.42.0 should upgrade before
  June 15, 2026.
- Improved upgrade reliability by fixing an IAM issue with
  “DescribeAddonVersions” that temporarily marked deployments as “Upgrade
  Failed” before automatically recovering.
- Fixed redaction of sensitive values in telemetry to allow Key values from the
  LogAttributes processor to pass through as-is.
- Security patches and dependency upgrades.

### SPCS Data Plane Agent 1.30.0

- Improved upgrade reliability by identifying unhealthy PostgreSQL deployment
  blocking the upgrade process.
- Security patches and dependency upgrades.

### Runtime Operator 0.61.0

- Security patches and dependency upgrades.

### Openflow Runtime Gateway 2026.5.13.18

- Security patches and dependency upgrades.

### Openflow Ingress Controller 2026.5.13-18

- Security patches and dependency upgrades.

### Openflow Token Refresher 1.12.0

- Security patches and dependency upgrades.

## May 19, 2026

### Runtime Server 2026.5.19.16

- Increased the web request timeout from the default to 5 minutes, preventing
  timeout errors when the runtime is under heavy load or processing large
  configuration changes.
- Fixed connector flow URI pattern matching in cluster response merging that
  could cause incorrect flow resolution when multiple connectors share similar
  URI patterns.
- Fixed an issue where adding parameters to a Parameter Context with multiple
  suffixed variants incorrectly applied changes to the wrong context during flow
  upgrades.
- Enabled parameter value expressions to reference parameters defined in
  inherited parameter contexts.

### Runtime Extensions 2026.5.19.17

- CDC SQL Server (CT): When a Change Tracking query fails for a specific table,
  the connector now applies a backoff delay to that individual table instead of
  failing the entire connector run, and includes the table name in the error
  message for easier troubleshooting.
- CDC SQL Server: Fixed a race condition where removing a table from replication
  and re-adding it before the next scheduler cycle caused the table to silently
  stop being processed until a full connector restart.
- CDC SQL Server (CDC): Proactively detects source-table schema changes (DDL) by
  polling cdc.ddl\_history, and detects when CDC is disabled mid-replication;
  affected tables are now moved to FAILED state instead of looping indefinitely
  on transient errors or producing rows against a stale schema.
- CDC SQL Server (CT): Adds the table name to the error message when change
  tracking is found to be disabled on a table, making it clear which table needs
  attention.
- CDC MySQL: Adds defensive type validation during binary log parsing to prevent
  corrupted records when a MySQL column returns an unexpected data type (for example,
  after an undetected schema change).
- Snowpipe Streaming: Fixed URI path segment encoding so that database, schema,
  or table names containing special characters (spaces, hyphens, mixed case) no
  longer cause channel-open failures; uses RFC 3986 compliant encoding instead
  of URL form encoding.
- Snowpipe Streaming: Added detailed error logging (including FlowFile
  attributes and exception details) immediately before routing records to the
  FAILURE relationship, improving diagnostics when ingestion errors occur.
- CDC Oracle: Treats database connection reset exceptions as warnings instead of
  errors; the connection is rarely used (once daily for license checks and
  schema fetches), is often stale, and the connector recovers automatically on
  the next cycle — this prevents false “Unhealthy” status on the connector
  dashboard.
- CDC Databases: Added a dedicated SCHEMA\_NOT\_FOUND failure reason when a source
  table disappears or its schema cannot be fetched after retries are exhausted,
  providing operators with a clear indication of why a table stopped replicating
  instead of a generic error.
- SharePoint: Fixed handling of HTTP 410 (Gone) errors when the SharePoint delta
  link expires, and added additional logging around delta link resolution to
  help troubleshoot synchronization issues with large document libraries.
- CDC SQL Server: Improved snapshot performance for partitioned tables by placing
  the partition column first in the ORDER BY and keyset WHERE clauses, enabling
  SQL Server partition elimination during keyset pagination and significantly
  reducing query execution time for large partitioned tables.

### Connectors 2026.5.19.16

- CDC Oracle & SQL Server (CDC): Added a stale-streams filter parameter that
  automatically excludes journal streams nearing their staleness threshold from
  CDC processing, preventing failures when streams expire during long-running
  replication cycles.
- SharePoint: Added an auto re-sync parameter to all SharePoint CDC connector
  variants that automatically re-synchronizes the full document library when the
  delta link expires or becomes invalid, instead of requiring manual
  intervention.
- CDC Databases: Fixed a connection leak where some connections were not routed
  through Private Link; ensures all database connections from the connector
  (including internal health-check and metadata queries) go through the
  configured private link endpoint.
- CDC Oracle & SQL Server: Adopted the enhanced
  MultiDatabaseWaitForSnapshotCompletion processor in incremental-only mode,
  which provides better coordination between snapshot and incremental phases and
  reduces the window where tables can miss changes during the transition.
- CDC Oracle: Added an Oversized Value Strategy parameter to Oracle connectors,
  allowing operators to choose how to handle column values that exceed
  Snowflake’s maximum column size (truncate, route to failure, or skip the
  column).
- MongoDB: Strips internal collection selection criteria attributes from
  FlowFile metadata before sending to Snowflake, preventing unnecessary
  attribute pollution in the destination.
- MongoDB: Improved failure reason reporting to distinguish between different
  types of ingestion errors (schema mismatch, connection timeout, authentication
  failure) for better operator visibility.

## May 14, 2026

### Runtime Server 2026.5.14.16

- Added support for loading asset configurations when connectors are created via
  SQL.

### Runtime Extensions 2026.5.14.16

- CDC SQL Server (CT version): Added source commit time, row count, and per-cycle
  phase instrumentation for SQL Server Change Tracking.
- Dataverse: Added FAILED table status tracking and a processor for managing table
  ingestion state.
- Added GateFlowFile processor for flow control.
- CDC Databases: Made the CDC schema registry resilient to TableSchema class
  changes, preventing failures on connector upgrades.
- CDC Databases: Fixed NullPointerException on dynamic-property initialization in
  RouteOnSnowflakeParameter processors.
- CDC SQL Server: Fixed keyset pagination failures by properly casting
  int/smallint/tinyint primary key placeholders.
- Kafka: Refactored Kafka3ConnectionService to use SSLContextProvider for cleaner
  SSL handling and possibility to use PEM-based authentication.
- AWS: Added Token Request Endpoint property to AwsRdsIamDatabasePasswordProvider
  for custom STS endpoints.

### Connectors 2026.5.14.16

- CDC Oracle: Added Concurrent Snapshot Queries parameter to allow parallel
  snapshot fetching.
- CDC Oracle: Adjusted Oracle connector flows to comply with FlowFile size limits.
- CDC MySQL, PostgreSQL, SQL Server: Removed tables listing FlowFile attributes to
  reduce pressure on Provenance Repository when syncing thousands of tables.
- CDC MongoDB: Improved stream staleness prevention to reduce unnecessary restarts.

## May 12, 2026

### Runtime Server 2026.5.12.16

- Fixed potential corruption with modify-after-write on Local State Provider.
- Flow import/export with stateful components state.

### Runtime Extensions 2026.5.12.16

- Snowpipe Streaming: Added PrivateLink support to Snowpipe Streaming v2
  processors.
- CDC Databases: Added STALE\_AFTER flow-file attribute to
  GetSnowflakeJournalStreams and MultiDatabaseGetSnowflakeJournalStreams for
  stream staleness monitoring.
- CDC Databases (multi-database): Added Incremental strategy to
  MultiDatabaseWaitForSnapshotCompletion processor.
- CDC SQL Server: Widened CdcStreamPosition to BigInteger to support 10-byte
  SQL Server Log Sequence Numbers.
- CDC Oracle: Reduced the number of row ID ranges generated by
  SplitOracleTable to improve snapshot performance.
- CDC Oracle: Added oversized value support to FetchRowsByRowId processor.
- Dataverse: Fixed backpressure on success queue deadlocking
  FetchMicrosoftDataverseTable by only listing idle tables during long
  snapshots.
- CDC PostgreSQL: Changed publication verification fall-through outcome from
  FAILED to SKIPPED to prevent false failures.

### Connectors 2026.5.12.16

- CDC MySQL, PostgreSQL, SQL Server: Added filter for streams nearing
  staleness within 7 days.
- CDC MySQL: Replaced WaitForTableState processor with enhanced version in
  Incremental flow.
- MongoDB: Added object identifier resolution.

## May 8, 2026

### Runtime Server 2026.5.8.5

- CDC SQL Server: INFO-level logging for MultiDatabaseCaptureChangeSqlServer are
  now captured in the event table.
- Fixed Repository Record creation for S2S and Load-Balanced Connections.

### Runtime Extensions 2026.5.8.8

- CDC PostgreSQL: Added Table Storage Format (Standard/Iceberg) option to the
  Postgres CDC connector wizard.
- CDC SQL Server: Added logging for CT query performance tracking if Metrics
  Enabled property is set to true.
- Dataverse: Enabled reingestion of all tables by allowing empty Tables Filter
  Value.
- Dataverse: Added ability to drop individual table state records for selective
  reingestion.
- CDC SQL Server: Reports capture metrics on empty fetches for better
  observability.
- CDC PostgreSQL: Separated replication and non-replication connections to
  prevent connection pool exhaustion.
- Snowpipe Streaming: Fixed GCS object transfer on SPCS for Snowpipe Streaming
  v2.
- CDC SQL Server: Added FlowFile size limit to MultiDatabaseFetchRowsByRowId to
  prevent memory issues.
- BigQuery: Automatically retries on transient gRPC exceptions instead of
  failing the flow.
- BigQuery: Fixed case-insensitive database merge query failures.

### Connectors 2026.5.7.18

- Jira: Fixed duplicate issues when project has changed.
- CDC SQL Server: Bumped concurrent tasks to 2 on MultiDatabaseEnrichCdcStream
  for improved throughput.
- CDC SQL Server: Added Concurrent Select Queries parameter for incremental
  loads in multi-database mode.

## May 5, 2026

### Control Plane Core 0.114.0

- Updated SQL Server connector CDC preview documentation link.
- Replaced legacy Jira connector with Core and Agile versions.
- Fixed intermittent issue with the available Deployment list missing some
  Deployment options when creating a new Runtime.
- Security patches and dependency upgrades.

### Data Plane Service 0.113.0

- Improved reliability of Runtime Upgrade by handling a case where the Runtime
  StatefulSet is stuck waiting on unhealthy pods prior to upgrade.
- Security patches and dependency upgrades.

### Control Plane UI 0.80.0

- Upgraded to Stellar 0.31.3 for consistency across Snowflake products.

### AWS Data Plane Agent 1.42.0

- Security patches and dependency upgrades.

### SPCS Data Plane Agent 1.28.0

- Security patches and dependency upgrades.

### Runtime Operator 0.59.0

- Improved reliability of Runtime scale down by disallowing a node to reconnect
  to the cluster while waiting on decommissioning.
- Security patches and dependency upgrades.

### Openflow Runtime Gateway 2026.5.1.10

- Security patches and dependency upgrades.

### Openflow Ingress Controller 2026.5.1-10

- Security patches and dependency upgrades.

### Openflow Token Refresher 1.11.0

- Security patches and dependency upgrades.

### Runtime Server 2026.5.5.17

- Fixed handling of PROPERTY\_PARAMETERIZATION\_REMOVED as a local change during
  versioned Process Group upgrades.
- Fixed lineage start index tracking in Session.create().

### Runtime Extensions 2026.5.5.19

- CDC Oracle: Added support for user-declared logical keys, allowing custom
  replication key columns instead of relying on auto-detected primary keys.
- CDC Databases (multi-DB): Prioritized newly added tables in the table
  scheduler so they begin replicating sooner.
- Veeva Vault: Switched to STREAM-based change tracking in
  MergeVeevaVaultStagingTable for more efficient incremental processing.
- CDC SQL Server: Fixed an off-by-one error at the LATEST starting position
  that could cause the first change event to be missed.

### Connectors 2026.5.5.16

- CDC Oracle: Added logical-key (user-declared) Oracle connector flows.
- CDC PostgreSQL: Added Iceberg table support for PostgreSQL CDC connector.
- Veeva Vault: Set Offset Tracking Resolution to DISABLED for
  PublishSnowpipeStreaming in Veeva Vault connector.
- CDC MySQL: Switched to Snowflake journal record structure for MySQL Capture
  processor.
- Salesforce Bulk API: Added Object Identifier Resolution parameter to Describe
  SFDC Object processors.
- Confluence: Switched to documentId as the stage file name to prevent duplicate
  pages on connector restart.
- BigQuery: Improved BigQuery incremental failure handling.

## May 1, 2026

### Runtime Server 2026.5.1.1

- Fixed node offload handling for Processors like PublishSnowpipeStreaming and
  MergeContent that create and manage multiple process sessions.
- Added metrics collection for Jira Processors.

### Runtime Extensions 2026.5.1.1

- Added support for Iceberg Tables to UpdateSnowflakeTable Processor.
- Improved merge handling in MergeVeevaVaultStagingTable Processor.
- Added DML Record Structure property to CaptureChangeMySQL Processor.

## April 28, 2026

### AWS Data Plane Agent 1.41.0

- Enabled logs from the Openflow Agent in your Snowflake Event Table,
  improving support and reducing triage time for support cases.
- Fixed an upgrade issue for older deployments that use Custom Ingress with
  multiple Custom Ingress Security Groups.
- Improved support for adding observability agents in the EKS cluster
  alongside Openflow services.
- Security patches and dependency upgrades.

### Runtime Server 2026.4.28.17

- Security patches and dependency upgrades.

### Runtime Extensions 2026.4.28.15

- CDC PostgreSQL: Added configuration verification to CaptureChangePostgreSQL.
- CDC Databases: Added SNOWFLAKE\_OPENFLOW application tag to CDC Merge queries.
- CDC Google BigQuery: Added support for up to 7 days of history for CDC with
  Google BigQuery.
- CDC Oracle: Improved Oracle table splitting performance.

## April 24, 2026

### Runtime Server 2026.4.24.16

- Excluded Parameter Description from Flow Version change determination.
- Added configurable Content Claim Truncation to FileSystemRepository.
- Added Registered Flow ID Version Path to MDC Attributes.
- Preserved prioritizer order in Git flow Registry serialization.

### Runtime Extensions 2026.4.24.16

- CDC SQL Server: Added CDC-based change capture processor as an alternative to Change Tracking.
- CDC SQL Server: Added Snapshot Isolation support for consistent reads during change capture and table snapshots.
- Jira v2: Added Agile components including boards, board configuration, board projects, board sprints, and filters.
- CDC Oracle: Added Oversized Values handling, allowing truncation or rejection of values exceeding a configurable size limit.
- CDC Databases: Added Incremental strategy to WaitForSnapshotCompletion so high-traffic tables no longer block other tables.
- Veeva: Added connector and components to sync data from Veeva Vault.
- CDC SQL Server: Fixed empty-string primary key handling where CAST caused infinite retry loops during keyset pagination.
- CDC Databases (multi-DB): Fixed journal stream prefix collision bug where tables sharing the same bare name were incorrectly matched.
- Dataverse: Fixed deadlock in FetchMicrosoftDataverseTable where a table stuck in FETCHING state after a non-retryable error would never recover.
- Snowpipe Streaming: Fixed MergeSnowflakeJournalTable incorrectly handling failed merge queries, causing silent data loss.

### Connectors 2026.4.24.16

- Jira: Added Jira v2 core connector with improved entity coverage, custom fields, user groups, worklogs, issue relations, and project filtering.
- Jira: Added Jira Agile connector for boards, sprints, sprint-to-board, and sprint-to-issue ingestion.
- CDC MySQL & PostgreSQL: Added destination schema mapping support for routing source schemas to custom Snowflake destination schemas.
- CDC SQL Server: Added multi-database CDC connector flow definition using Change Data Capture mode.
- CDC PostgreSQL: Switched to flattened DML record output, approximately doubling ingestion throughput.
- CDC PostgreSQL: Replaced WaitForTableState with WaitForSnapshotCompletion in incremental mode to reduce unnecessary queuing during snapshot phases.
- CDC Databases: Fixed scheduling stuck issue for connectors with more than 10,000 tables by increasing backpressure queue limit.
- Dataverse: Replaced PutSQL with ExecuteSQL for merge step, simplified flow, and added automatic cleanup of deprecated columns.
- Veeva: Added connector and components to sync data from Veeva Vault.
- CDC PostgreSQL: Reverted UpdateTableState property changes that could cause data loss during snapshot with concurrent channels.

## April 17, 2026

### AWS Data Plane Agent 1.38.0

- Security patches and dependency upgrades.

### SPCS Data Plane Agent 1.27.0

- Security patches and dependency upgrades.

### Control Plane Core 0.111.0

- Security patches and dependency upgrades.
- Improved performance when listing and interacting with Deployments and Runtimes.
- HubSpot connector is now available in public preview.

### Data Plane Service 0.110.0

- Security patches and dependency upgrades.

### Ingress Controller 2026.4.14-17

- Security patches and dependency upgrades.

### Openflow Runtime Gateway 2026.4.14.17

- Security patches and dependency upgrades.

### Openflow Token Refresher 1.10.0

- Security patches and dependency upgrades.

### Control Plane UI 0.78.0

- Security patches and dependency upgrades.

### Data Plane UI 0.15.0

- Security patches and dependency upgrades.

## April 16, 2026

### Runtime Extensions 2026.4.16.18

- CDC Oracle: Auto-detects UNIQUE key constraints as replication keys when no
  primary key is defined.
- CDC SQL Server: Fixed `sysname` columns causing infinite schema-mismatch
  loop.
- CDC SQL Server: Fixed duplicate DDL emission for unchanged tables by
  disambiguating `EARLIEST` position.
- CDC Databases: Made `CdcSchemaRegistry` resilient to internal
  `TableSchema` class changes during upgrades.
- Removed preview labels from UpdateSnowflake\* processors.

### Connectors 2026.4.16.16

- CDC MySQL: Added Oversized Value Strategy parameter.
- Dataverse: Fixed inability to change type of \_SNOWFLAKE\_DELETED column.
- CDC SQL Server: Increased incremental load batch size to 100K rows.

## April 14, 2026

### Runtime Server 2026.4.14.16

- Fixed local change detection for versioned flows when updating a property that
  was not set previously.
- Runtime UI: Allows users to resume a suspended runtime in recovery mode.

### Runtime Extensions 2026.4.14.16

- Jira (Atlassian): Added Jira v2 core components including new processors for
  ingesting comments, changelogs, deleted issues, projects, permissions, users,
  worklogs, and other Jira entities.
- CDC Databases: Introduced a configurable Oversized Value Limit property
  (default 16 MB) on CDC and snapshot processors.
- CDC Oracle: Removed unnecessary Oracle database privileges from configuration
  scripts.
- Snowpipe Streaming: Removed Preview tags from PublishSnowpipeStreaming
  processors, marking them as generally available.

### Connectors 2026.4.14.15

- Kafka: Disabled flow-file-based offset tracking to prevent data loss during
  downscaling.
- Kafka: Added a new high-performance Kafka connector flow with
  PublishSnowpipeStreaming.
- CDC Oracle and SQL Server: Exposed table exclusion parameter for multi-database
  connectors.
- CDC Oracle: Added Snowpipe Streaming v2 routing with automatic v1 fallback.
- Salesforce: Explicitly set warehouse in MERGE pre-query to prevent failures
  when no default warehouse is configured.

## April 13, 2026

### AWS Data Plane Agent 1.37.0

- Improved custom ingress to simultaneously support load balancer security
  groups managed by both Openflow and deployment-specific configurations.
- Removed duplicate ingress rules for default custom ingress security group.

## April 10, 2026

### AWS Data Plane Agent 1.36.0

- Security patches and dependency upgrades.
- Improved resiliency of new Deployments and upgrades related to how AWS IAM
  permissions are created and refreshed.
- Improved cost efficiency of telemetry by removing unused or low-value metrics from being
  exported to Event Tables.

### SPCS Data Plane Agent 1.26.0

- Security patches and dependency upgrades.
- Improved cost efficiency of telemetry by removing unused or low-value metrics from being
  exported to Event Tables.

### Control Plane Core 0.109.1

- Security patches and dependency upgrades.
- Oracle Embedded License Connector added to Featured Connectors.

### Data Plane Service 0.109.0

- Security patches and dependency upgrades.

### Ingress Controller 2026.4.7

- Security patches and dependency upgrades.

### Runtime Operator 0.58.0

- Security patches and dependency upgrades.

### Control Plane UI 0.77.0

- Added third-party icons for Atlassian, Salesforce, and Microsoft SQL Server
  connector cards.
- Added support for resuming suspended Runtimes in recovery mode.
- Hide gateway version in Runtime upgrade dialog when appropriate.
- Improved warnings and guidance when users lack permissions to create a
  Deployment.
- Improved Connector installation process to no longer wait for available
  Runtimes to load before opening the dialog.

### Data Plane UI 0.14.0

- Security patches and dependency upgrades.

## April 9, 2026

### Runtime Server 2026.4.9.16

- Fixed Parameter and Parameter Context descriptions being lost during versioned
  flow upgrades.
- Fixed record path functions (`toBytes`, `toDate`, `toString`, and
  `format`) to return the correct types.
- Snowpipe Streaming: Exports metrics from `PublishChangeDataSnowpipeStreaming`
  to the event table for better observability.

### Runtime Extensions 2026.4.9.16

- CDC SQL Server: Improved error visibility during connection setup by fixing
  exception masking in `CatalogHelper` and unifying `setCatalog` usage.
- CDC SQL Server and Oracle: Switched to `DirectJsonRecordWriter` for storing
  change data as JSON in VARIANT columns, improving Snowflake ingestion
  efficiency.
- CDC MySQL: Fixed composite primary key column ordering by reading from
  `KEY_COLUMN_USAGE`, ensuring correct row identification during snapshot.

### Connectors 2026.4.9.15

- Dataverse: Updated merge journal process to include `SNOWFLAKE_ID` in the
  Dataverse schema.
- Box, Confluence, Google Drive, SharePoint, and Slack: Fixed Cortex-enabled
  connectors to preserve existing CORTEX SEARCH SERVICE configuration instead of
  overwriting it.
- CDC MySQL, PostgreSQL, Oracle, and SQL Server: Increased run duration on
  CPU-bound processors in incremental flows to reduce backpressure.
- CDC Oracle: Added staleness prevention to keep pipelines active during periods
  of low data volume.

## April 7, 2026

### Runtime Extensions 2026.4.7.16

- Kafka: Fixed duplicate message delivery in ConsumeKafka when consumers rejoin a
  consumer group during rebalance.
- CDC MySQL: Fixed data corruption when a MySQL server restart reassigns table IDs to
  different tables, preventing stale schema mappings from causing type mismatch errors
  during data ingestion.
- CDC Oracle: Fixed Oracle XStream CDC failing to read the LCR version when the XStream
  outbound server is configured on a different database instance (PDB vs CDB).
- CDC Databases: Reduced unnecessary Snowpipe Streaming query retries by penalizing the
  MergeSnowflakeJournalTable processor when no new data is available or the connection is
  disconnected, improving throughput.
- CDC SQL Server: Added table draining to ensure tables with large change backlogs are
  fully consumed before the connector moves to the next table.

### Connectors 2026.4.7.16

- CDC MySQL and PostgreSQL: Added a `Re-snapshot Table Exclusions` parameter to allow
  specific tables to be excluded from replication, enabling re-snapshotting use cases.

## April 6, 2026

### AWS Data Plane Agent 1.34.0

- Improved deployment upgrade time for customers with many Runtimes.
- Improved speed and reliability of upgrades from Openflow Deployments running EKS 1.32 to EKS 1.35.

## April 2, 2026

### Runtime Server 2026.4.2.16

- Increased the CDC connector metrics table row limit for observability dashboards from 30,000 to 40,000.
- Fixed inherited Parameter Context synchronization on versioned Process Group upgrades when new parameters are added.
- Fixed the provenance repository to honor the configured maximum attribute character size when reading entries.
- Fixed component bundle resolution and rollback behavior on versioned flow changes.
- Updated to Runtime UI 0.70.0.

### Runtime Extensions 2026.4.2.16

- Added Google Cloud Storage Provider for Iceberg.
- Fixed empty Private Key check for PGP Secret Key.
- CDC Databases: Added a new `MultiDatabaseGetSnowflakeJournalStreams` processor that supports multi-source CDC replication by mapping 3-part source table names (database + schema + table) to Snowflake destination schemas using a configurable naming pattern.
- CDC PostgreSQL: Added a “Flatten DML Records” option to `CaptureChangePostgreSQL` that writes change events in the final flat format at capture time, eliminating the intermediate file read-and-rewrite step in `EnrichCdcStream` and reducing disk I/O.
- Snowpipe Streaming 2: Added a “Destination Type” property to `PublishSnowpipeStreaming` that allows users to target either a named Pipe or a Table directly, with automatic migration to preserve existing Pipe-based configurations.
- CDC Databases: Added an “Excluded Comma Separated Source Table Names” property to `ListTableNames` (and its multi-database equivalent) that lets users exclude specific tables from replication.
- BigQuery: Fixed a property migration bug in `CreateReadSession` that caused incorrect processor configuration when upgrading from older flow versions.
- CDC PostgreSQL: Fixed `FetchTableSnapshot` failures on tables containing `bytea` columns by using a more compatible JDBC method to read binary data.
- CDC Databases: Updated the `DESTINATION_SCHEMA_NAME_PATTERN` placeholders from `{database}`, `{schema}` to `${source.database.name}`, `${source.schema.name}`, and `${source.table.name}`. A fixed schema name is now valid (the validator constraint requiring at least one placeholder has been removed).
- All connectors: Added a `Validation Mode` property to the `SetAttributesValidatingReferences` processor, allowing configuration of how attribute reference validation is enforced.

### Connectors 2026.4.2.16

- BigQuery: Reduced the concurrency of parallel streaming jobs (PSS) to prevent resource contention issues.
- SharePoint: Fixed a file removal pattern bug for customers with the `ENABLE_FIX_209969` account parameter set to false, where the pattern would fail to match and remove processed files.
- BigQuery: Prevented CDC and view ingestion from starting when the required temporary dataset parameter is not configured, avoiding accidental table failures.
- CDC MySQL, PostgreSQL, and SQL Server: Configured the source database connection pool with validation-on-borrow and periodic eviction of idle connections, preventing misleading “connection reset” errors caused by stale connections being reused after a server-side timeout.
- Dataverse: Added a `_SNOWFLAKE_ID` column to replicated records by mapping the source primary key, allowing downstream consumers to uniquely identify each record in Snowflake.
- CDC SQL Server, MySQL, and PostgreSQL: Added the new stream staleness prevention mechanism to the connector.
- Jira: Fixed an incorrect merge query in the Jira connector.

## April 1, 2026

### AWS Data Plane Agent 1.33.0

- Upgraded to AWS EKS 1.35.
- Added the EKS kube-proxy add-on for automated, managed upgrades of networking components.
- Improved auto-healing when EKS node groups are down or offline for extended periods.
- Improved cost efficiency of telemetry collection by ignoring low-value metrics.

## March 31, 2026

### AWS Data Plane Agent 1.31.3

- Security patches and dependency upgrades.

### SPCS Data Plane Agent 1.24.1

- Security patches and dependency upgrades.

### Control Plane Core 0.108.2

- Security patches and dependency upgrades.
- Fixed Oracle Connector License syncing for accounts with renamed organizations.

### Data Plane Service 0.108.2

- Security patches and dependency upgrades.

## March 30, 2026

### Runtime Server 2026.3.27.21

- Added `isValidDate` and `isValidInstant` Expression Language functions.
- Fixed inherited parameter context preservation during `KEEP_EXISTING` versioned flow deployment.
- **Behavior change:** When upgrading a running versioned flow to a new version, new components added in the new version are automatically started.

### Runtime Extensions 2026.3.27.21

- AWS: Fixed AWS connection pool shutdown on EKS with STS credential refresh.
- Google Drive: Reverted to correct default scopes in Google Drive components, with a new property to use the Google Cloud Platform scope when using Workload Identity Federation with impersonation.
- Kinesis: Handled `ResourceNotFoundException` in `ConsumeKinesis` when shards are not found or removed.
- Oracle: Added support for LCR positions V1 and separate connection and XStream attach, adding support for 12.1 and 12.0.
- Dataverse: Unknown Dataverse attribute types fall back to STRING.
- Salesforce: Fixed Salesforce formula field translation producing invalid SQL for date arithmetic.
- Snowflake: Fixed `PublishSnowpipeStreaming` skipping FlowFiles after pipe recreation due to a stale offset.
- Dataverse: Added a parameter to configure maximum fetched column size in `FetchMicrosoftDataverseTable`.
- Dataverse: Added table-level removal to the Dataverse connector.
- Snowflake: Fixed Workload Identity Federation token header format for Snowpipe Streaming 2.

### Connectors 2026.3.26.19

- CDC database connectors: Added metrics collection for observability dashboards.
- CDC SQL Server: Switched from Snowpipe Streaming v1 to v2.

## March 27, 2026

### AWS Data Plane Agent 1.31.2

- Replaced Ingress-Nginx with Openflow Ingress Controller.
- Switched TLS certificate validation for Snowflake managed ingress from HTTP-01 to DNS-01. This introduces new network requirements for BYOC deployments using Snowflake managed ingress. For more information, see [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc#prerequisites-for-byo-vpc-existing-vpc).
- Fixed an issue with load balancer security group rules when multiple deployments share the same private security group.
- Security patches and dependency upgrades.
- Improved support for adding many Runtimes to a Deployment at once.
- Removed the need for ingress on port 80. All Deployment and Runtime ingress uses port 443.

### SPCS Data Plane Agent 1.24.0

- Security patches and dependency upgrades.

### Control Plane Core 0.108.0

- Security patches and dependency upgrades.
- Improved handling for users with large sets of roles when they need to provide this list of roles for creating and managing resources.
- Salesforce Bulk API connector is now generally available (GA).

### Control Plane UI 0.74.0

- Upgraded to Stellar 0.28.0.
- The Create Runtime and EAIs dialog can open while EAIs are still loading.

### Data Plane Service 0.108.0

- Security patches and dependency upgrades.

### Openflow Runtime Gateway 2026.3.25.14

- Security patches and dependency upgrades.

## March 24, 2026

### Runtime Server 2026.3.24.18

- Improved layout of vertical space in the Runtime UI for longer lists of tables and schemas.

### Runtime Extensions 2026.3.24.20

- SQL Server: CDC components are now generally available (GA).
- Oracle: Fixed `TIMESTAMPTZ` mapping for named time zones.
- Added processors to support Snowpipe Streaming v2 in CDC database connectors.
- Improved `UpdateSnowflakeTable` caching and query batching for better performance.

### Connectors 2026.3.24.18

- CDC database connectors: Added metrics collection for observability dashboards.
- MySQL: Switched CDC connector from Snowpipe Streaming v1 to v2.
- PostgreSQL: Switched CDC connector from Snowpipe Streaming v1 to v2.
- Salesforce: Salesforce Bulk API connector is now generally available (GA) and includes a parameter to control warehouse cost optimization.

## March 20, 2026

### Control Plane Core 0.107.1

- Improved role picker for users with a large number of available roles.

### Runtime Server 2026.3.19.18

- Fixed Content Repository defragmentation.
- Improved reloading behavior for Scripted Record Reader and Writer processors.

### Runtime Extensions 2026.3.19.20

- PostgreSQL and MySQL: Set explicit field sizes for `VARCHAR` and `BINARY` columns to support larger values.
- PostgreSQL: Fixed cursor-based fetching by disabling `autoCommit` to prevent out-of-memory errors on large rows.
- Salesforce: Salesforce Bulk API components are now generally available (GA).
- Salesforce: Fixed Salesforce Upsert Lookup failing when field values contain a `+` sign.
- SQL Server: Improved handling of source database failover to prevent table sync failures.
- SQL Server: Improved snapshot performance for clustered and partitioned tables.

### Connectors 2026.3.19.15

- Dataverse: Added Table State Service to the Dataverse connector flow.
- Oracle: Parallelized Snowpipe Streaming v1 snapshot by primary key for improved performance.
- Slack: Added option to ignore channels from historical load in the Slack connector.

## March 17, 2026

### AWS Data Plane Agent 1.30.0

- Added support for recovering a deployment after Snowflake organization or account rename via an `update-account.sh` script.
- Improved Runtime metrics collection for larger data flows and Connectors handling large numbers of tables.
- Preparing for dedicated Openflow Ingress Controller to replace Nginx for BYOC runtime traffic.
- Added memory limiter and metrics routing in the OTEL collector for stability and separate pipelines.
- Security patches and dependency upgrades, including OTEL Collector 0.146.1.

### SPCS Data Plane Agent 1.23.0

- Improved Runtime metrics collection for larger data flows and Connectors handling large numbers of tables.
- Security patches and dependency upgrades.

### Control Plane UI 0.73.0

- Upgraded to Stellar icons.
- Fixed a condition that could have prevented the splash screen from hiding when an unhandled error occurs.

### Control Plane Core 0.107.0

- Reliability improvements for Deployments when an account or organization is renamed.

### Data Plane Service 0.107.0

- Security patches and dependency upgrades.

### Runtime Operator 0.57.0

- Security patches and dependency upgrades.

### Openflow Ingress Controller 2026.3.16-17

- Security patches and dependency upgrades.
- Preparing for replacement of Nginx as the ingress controller for BYOC runtime traffic.

### Runtime Server 2026.3.17.13

- New Runtime UI 0.68.0.
- Fixed splash screen which may stay visible under specific conditions.
- Improved content viewer to improve MIME type support.
- Track Content and truncate large resource claims in FileSystemRepository.
- Performance improvements for OpenTelemetry data collection.

### Runtime Extensions 2026.3.17.13

- Updated log configuration to capture INFO level logs for DescribeSFDCObject processor.
- Added Session Header handling to Snowpipe Streaming 2.
- Reduced default batch size and handle query timeout for SQL Server table name fetching.
- Kinesis: Significantly improved the `ConsumeKinesis` processor, removing use of the Kinesis Client Library.
- MySQL: Fixed `NullPointerException` in `CaptureChangeMySQL.disconnectBinlogClient` when `tableMapStore` is `null`.
- MySQL: Added TLS support for JDBC in `CaptureChangeMySQL`.
- SQL Server: Fixed `VARCHAR/NVARCHAR` sorting issue that may cause duplicate rows during batched paging.
- SQL Server: Reduced default batch size and improved query timeout handling table name fetching.
- Added `MultiDatabaseRouteOnSnowflakeParameter` and `MultiDatabaseExitRouteOnSnowflakeParameter` processors.
- Added `GetActiveSnowflakeStreams` processor for stream staleness prevention.

## March 13, 2026

### Control Plane Core 0.106.0

- Oracle connector is now generally available (GA).
- Registered preview of new PostgreSQL CDC SOM connector in the control plane catalog.
- Added data plane configuration options for CDC Snowpipe Streaming v2 rollout across MySQL, PostgreSQL, SQL Server, and Oracle connectors.

## March 12, 2026

### Runtime Server 2026.3.12.13

- Fixed 409 Conflict in Azure DevOps and Bitbucket flow registry clients for multiple Flows with shared branch.
- Fixed Flow Comparison showing changes for nested child components when using nesting flow versioning.

### Runtime Extensions 2026.3.12.15

- Iceberg: Added Storage Class to S3FileIOProvider.
- Salesforce: Use FQN database/schema for Salesforce Merge queries.
- Salesforce: Improved Salesforce formula parsing and logging.
- Salesforce: Fixed ListSFDCObjects becoming invalid after upgrade with dynamic relationships.
- MySQL: Escalate binlog communication failure log from WARN to ERROR.

### Connectors 2026.3.12.15

- Salesforce: Use FQN database/schema for Salesforce Merge queries.
- Salesforce: Do not emit bulletin on suspend warehouse attempts.

## March 11, 2026

### Runtime Server 2026.3.10.21

- New Runtime UI 0.67.0.
- Fixed flicker of overlapping connection warning in connector canvas.
- Aligned reusable canvas renderers for borders around PGs and RPGs.
- Fixed support for floating point numbers in connection flow file expiration.
- Restored special treatment of trigger serially processors (no concurrent tasks).

### Runtime Extensions 2026.3.10.20

- AWS Secrets Manager Parameter Provider now supports plain text secrets.
- ListS3: Fixed V1 pagination failing when delimiter is not set, which caused an infinite loop.
- MultiDatabaseFetchTableSnapshot: Added FlowFile size limiting.
- Slack: ConsumeSlackHistory now has an option to ignore channels from historical load.
- MySQL: Fixed PutSnowpipeStreaming storing JSON in VARIANT columns as strings by directly writing JSON records in CaptureChangeMySQL.
- Dataverse: Added `SNOWFLAKE_ID` column to the schema.
- Snowpipe Streaming: Improved channel error handling in PublishSnowpipeStreaming.
- Snowpipe Streaming v2: Fixed error when streaming `timestamp_tz` with seconds in offset.
- CDC Databases: Fixed tables transitioning to FAILED during snapshot load by adding buffer for lineageStartDate comparison.

### Connectors 2026.3.10.20

- CDC SQL Server: Added Oversized Value Strategy parameter.
- Salesforce Bulk API: Added initial support for formulas.
- Salesforce Bulk API: Warehouse suspension now occurs immediately after all merge queries are executed.

## March 6, 2026

### Runtime Extensions 2026.3.6.12

- UpdateSnowflakeView: Added support for raw SQL.
- PostgreSQL: Fixed PutSnowpipeStreaming storing JSON in VARIANT columns as strings by directly writing JSON records in CaptureChangePostgreSQL and FetchTableSnapshot.
- HubSpot: Added missing CRM object types and fixed API compatibility.
- CDC Oracle: Fixed partitioned tables support during snapshot.
- Snowpipe Streaming v1: Fixed empty FlowFile handling in PutSnowpipeStreaming when configured to use exactly-once delivery.

## March 5, 2026

### AWS Data Plane Agent 1.26.0

- Security patches and dependency upgrades.

### SPCS Data Plane Agent 1.20.0

- Security patches and dependency upgrades.
- Added per-connector error metrics, improving speed and reliability of the Openflow Observability dashboard.

### Control Plane UI 0.72.0

- Introduced a Connector listing for managing Connector Snowflake Objects (hidden by a feature flag until verified and ready).
- Updated the Connector installation process for Connector Snowflake Objects (hidden by a feature flag until verified and ready).
- Added MongoDB Connector Definition icon.
- Updated the Oracle Connector terms dialog to account for the new independent (BYOL) Oracle connector.
- Updated the user-facing action for “Rename” to “Set display name”.

### Control Plane Core 0.105.0

- Snowflake deployments can now heal from `UPGRADE_FAILED` state if they report a healthy status and version.
- Added MongoDB connector flow.
- Added support for `OPENFLOW_INGRESS_NAME` parameter when creating the URL to access Snowflake Deployments.

### Data Plane Service 0.105.0

- **Behavior change:** Runtime Python processor properties are now set based on Runtime node size (Small: disabled, Medium: <=2, Large: <=4).
- Security patches and dependency upgrades.

### Runtime Operator 0.56.0

- **Behavior change:** Python processors are now disabled by default to improve Runtime stability. Python processor usage is controlled by Runtime size (Small: disallowed, Medium: <=2, Large: <=4).
- Security patches and dependency upgrades.

## March 3, 2026

### AWS Data Plane Agent 1.25.0

- Reduced downtime for Openflow Runtimes when upgrading the AMI for BYOC Deployments.
- Added support for upcoming EKS 1.35 upgrade, though BYOC is still using EKS 1.34.

### Runtime Server 2026.3.4.15

- Expression Language: Added `compactDelimitedList()` and `trimDelimitedList()` functions.
- New Runtime UI 0.66.0.
- Hidden environmental changes in show/revert local changes.
- Connections now avoid overlapping, and warnings are shown for existing overlaps.

### Runtime Extensions 2026.3.4.16

- Snowpipe Streaming: Added optional Role property.
- CDC Databases: Fixed JSON column filtering in incremental load.
- CDC Databases: Fixed `clearSession()` removing already-transferred FlowFiles in FetchTableSnapshot.
- CDC Databases: Fixed `SEEN_AT` value being interpreted as seconds instead of milliseconds in incremental mode.
- CDC Databases: Minimized the risk of filling up the waiting queue in EnforceOrder processor.
- CDC Databases: Added “Oversized Value Strategy” to MultiDatabaseFetchTableSnapshot.
- CDC Oracle: Fixed verification in CaptureChangeOracle.
- CDC SQL Server: Added “Oversized Value Strategy” to MultiDatabaseCaptureChangeSqlServer processor.
- CDC SQL Server: Fixed DESC primary key handling in MultidatabaseFetchTableSnapshot.
- Salesforce: Fixed two bulletins in SubmitQueryJob for non-supported objects.
- Snowpipe Streaming: Added “Disabled” option for Offset Token Resolution in PublishSnowpipeStreaming.
- Snowpipe Streaming: Added channel error message on invalid rows log.

### Connectors 2026.3.4.15

- Added customer-facing metrics for MySQL connectors.
- Added customer-facing metrics for PostgreSQL connectors.
- Added customer-facing metrics for Oracle connectors.
- Confluence: Fixed user emails with quotes breaking the connector.
- Salesforce Bulk API: Added WaitForBulkJobs for warehouse usage cost optimization.

## February 26, 2026

### AWS Data Plane Agent 1.24.0

- Improved upgrade speed and reliability from EKS 1.32 to 1.34, fixing the temporary “Upgrade Failed” status for BYOC and BYO-VPC deployments.

### Runtime Server 2026.2.26.15

- Expression Language: Added `unique()` function for removing duplicates from delimited strings.

### Runtime Extensions 2026.2.26.16

- CDC Oracle: Added configurable starting position in CaptureChangeOracle to control where CDC begins reading.
- CDC Oracle: Added SSL/TLS connection support for CaptureChangeOracle.
- CDC Oracle: Removed preview tags from multi-database Oracle CDC processors (now generally available).
- CDC SQL Server: Fixed ChangeTrackingPosition parsing.
- CDC Databases: Removed stale entries from IncrementGroupAttribute processor to prevent unbounded state growth.
- Salesforce Bulk API: Fixed Merge Query failing when containing reserved keywords.
- Salesforce Bulk API: Moved row deduplication in the Merge Query to fix an error and remove the need for the pre-SQL query DELETE.
- Salesforce: Populated `sErrorMessage` when duplicate error occurs in `UpsertSFDCObjects` processor.

### Connectors 2026.2.26.15

- CDC Oracle: Added SSL/TLS connection support in Oracle connector.
- CDC Oracle: Added schema name mapping in Oracle connector.
- CDC Oracle: Parameterized starting position properties in Oracle connector.
- CDC Oracle: Fixed missing log in concurrent snapshot.
- Salesforce Bulk API: Ignore changes on not null constraints to prevent ingestion failures.

## February 25, 2026

### Runtime Server 2026.2.24.16

- Security patches and dependency upgrades.
- Improved observability for Connectors and custom groovy scripts.

### Runtime Extensions 2026.2.24.20

- Salesforce Bulk API: Added SubmitDeleteJob processor to delete data using Bulk API.
- Snowpipe Streaming: Added PublishSnowpipeStreaming processor.
- CDC SQL Server: MultiDatabaseCaptureChangeSqlServer now has parameterized concurrency level.
- CDC Oracle: Fixed CaptureChangeOracle processor blocking during license validation.
- CDC Oracle: Added source state verification in CaptureChangeOracle to detect source database issues.
- CDC PostgreSQL: Added support for enum primary key in PostgreSQL.
- CDC PostgreSQL: Map PostgreSQL `DOUBLE PRECISION` and `MONEY` types to `RecordFieldType.DOUBLE`.
- Snowpipe Streaming v2: Added Snowflake Managed Authentication to PutSnowpipeStreaming2.
- CDC PostgreSQL: Added Password Provider support to CaptureChangePostgreSQL, which gives support for AWS IAM Authentication with AWS RDS.

### Connectors 2026.2.24.20

- Salesforce Bulk API: Added `CLUSTER BY ("ID")` on table creation for better query performance.
- Salesforce Bulk API: Disabled NOT NULL constraints on Alter Table processors to prevent ingestion failures.
- Salesforce Bulk API: Added description for ‘Enable Journal Tables’ parameter.
- Slack: Connector performance optimizations.
- CDC SQL Server: Fixed EnforceOrder processor being triggered every second instead of on flow file arrival.

## February 20, 2026

### AWS Data Plane Agent 1.23.0

- Fixed CloudFormation template formatting that could cause false drift detection by Terraform.
- Fixed a rare issue with custom ingress and PrivateLink where EKS control plane nodes couldn’t communicate with worker nodes.

### Control Plane UI 0.70.0

- Runtime diagnostic bundles are now sorted consistently.

### Control Plane Core 0.104.0

- Deployments and runtimes remain accessible after an organization or account name change.
- Removed the temporary restriction that limited Snowflake deployment upgrades to deployment owners whose active role matched the deployment owner role.

### Data Plane Service 0.104.0

- Deployments and runtimes remain accessible after an organization or account name change.

### Runtime Server 2026.2.19.16

- Fixed an issue where the flow version changed unexpectedly when the flow contains a ghosted parameter provider.
- New Runtime UI 0.65.0.
- The provenance lineage view now displays the component type alongside the event type.
- Diagnostic bundles are now sorted and ordered consistently.

### Runtime Extensions 2026.2.19.20

- Azure: Added support for Azure federated identity credentials.
- Google Ads: GetGoogleAdsReport now supports batch ingestion with configurable date range batching.
- CDC Oracle: Fixed ALTER TABLE parsing for integer-type columns (INT, SMALLINT, INTEGER, DEC, DECIMAL, NUMERIC) that incorrectly defaulted the scale to 19 instead of 0 when precision wasn’t specified.
- Fixed S3 processors using the global endpoint for `us-east-1`.
- Fixed an error in DBCPConnectionPool when a dynamic property has a null value.
- Kafka: ConsumeKafka now includes a `kafka.timestamp` attribute on FlowFiles emitted with the `Record` processing strategy.
- Kinesis: ConsumeKinesis now supports a `Demarcator` processing strategy.
- Snowpipe Streaming v1: PutSnowpipeStreaming now includes a `Binary Encoding Format` property for HEX binary string data.
- CDC SQL Server: MultiDatabaseCaptureChangeSqlServer now uses dynamic backoff when there are no new changes.
- CDC Multi-Database: MultiDatabaseFetchTableSnapshot can now run multiple select statements concurrently.
- CDC SQL Server: Fixed an ingestion failure when a table is re-added with a different schema.
- CDC Oracle: Fixed handling of license changes in a duplicated database.
- CDC Databases: Improved error handling for DML operations in the EnrichCdcStream and MultiDatabaseEnrichCdcStream processors.
- SharePoint: Fixed file path decoding for folders containing percent signs.
- CDC Databases: Warnings are now logged when oversized values are set to null, making it easier to identify data truncation.
- CDC Databases: Added a `CLEARING_FLOWFILE_FAILED` failure reason for table state tracking.
- **Behavior change:** Removed the Vectara, Pinecone, RAG evaluation, Milvus, and Cohere bundles.

### Connectors 2026.2.19.20

- CDC Oracle: The default snapshot fetching strategy is now `CONCURRENT_BY_ROWID` instead of `SEQUENTIAL_BY_PRIMARY_KEY`, improving snapshot performance.
- CDC SQL Server: Added customer-facing metrics for the SQL Server multi-database connector.
- Slack: Thread broadcast replies are now filtered from Slack collection to prevent duplicate messages.
- Salesforce Bulk API: The staging table is now truncated instead of deleted, preventing channel invalidation errors with Snowpipe Streaming.
- Salesforce Bulk API: Object filters are no longer case-sensitive.
- Salesforce Bulk API: Merge queries are no longer executed when no data has been captured.
- Salesforce Bulk API: Added an `Enable Journal Tables` parameter (default: false) that creates a `JOURNAL_Object` table where data changes are appended.
- CDC SQL Server: Snapshots now use multiple channels per table to improve throughput.
- CDC PostgreSQL: The oversized value strategy is now configurable in the PostgreSQL connector.

## February 13, 2026

### AWS Data Plane Agent 1.20.0

- Fixed an upgrade issue for older BYOC deployments where permissions failures occurred for tags on IAM OpenID Connect providers.
- BYOC deployments now more clearly report their `Upgrading` status.

## February 11, 2026

### Control Plane Core 0.102.0

- BYOC deployments now automatically restore access to runtimes when their AWS load balancers are recreated with a new DNS.
- Improved upgrade reliability for deployments and runtimes.

### Openflow Runtime Gateway 2026.2.10.21

- Fixed connector installation failures in Snowflake deployments with PrivateLink enabled.

### AWS Data Plane Agent 1.19.0

- Fixed an upgrade issue for older BYOC deployments caused by an `eks:ListTagsForResource` permissions failure.

### Runtime Server 2026.2.10.18

- Python: Fixed an issue where NAR deletion could block indefinitely while a Python processor was initializing.
- Fixed Parameter Provider version fallback when importing a flow.
- Fixed Parameter Context binding for new process groups during version upgrades.

### Runtime Extensions 2026.2.11.9

- Kafka: Fixed an issue where ConsumeKafka could create duplicate messages during a consumer group rebalance.
- Parquet: Fixed a ParquetReader error (`ClassCastException`) for `java.time` logical types.
- MongoDB: Added components for the upcoming private preview of the MongoDB CDC connector.
- Slack: Fixed duplicate messages caused by thread broadcast replies.
- MySQL: Added an oversized data property to the CaptureChangeMySQL processor.
- MySQL & PostgreSQL: Fixed FetchTableSnapshot incorrectly flagging interim FlowFiles as the final snapshot.
- MySQL & PostgreSQL: You can now configure how values larger than 16 MB are handled when they exceed the supported limit.
- Confluence Data Center: Added support for the export page permission.

### Connectors 2026.2.10.18

- Box: Removed the concurrency limit on stage inserts, improving overall performance.
- MultiDB MS SQL Server: Added schema name mapping.

## February 6, 2026

### Runtime Operator 0.54.0

- Fixed asset synchronization in runtimes when parameter providers are used.

### AWS Data Plane Agent 1.18.0

- Fixed an issue where migrating secrets during an upgrade caused failures for AWS deployments between versions 0.55.0 and 1.1.0.

## February 4, 2026

### Runtime Server 2026.2.3.19

- Python: Fixed an issue where imported properties couldn’t be used as `PropertyDependency` parameters in Python processors.
- Records: Added timestamp truncation support in the RecordPath DSL.
- New Runtime UI 0.64.0.

### Runtime Extensions 2026.2.4.10

- Iceberg: Added `Endpoint URL` and `Path Style Access` properties to the S3 FileIO Iceberg Provider.
- Avro: Added a `Fast Reader Enabled` property to the Avro Reader.
- CDC Databases: MultiDatabaseFetchTableSnapshot now numbers outgoing FlowFiles with a 1-based `chunk.index` attribute.
- CDC Databases: The EnrichCdcStream and MultiDatabaseEnrichCdcStream processors now write `min(seenAt)` to FlowFile attributes.
- CDC Databases: FlowFile attributes now include the number of rows inserted and updated during journal merge.
- CDC Oracle: Oracle DML/DDL FlowFiles now include index attributes, consistent with other CDC database components.
- CDC MySQL: Fixed replication failures for zero-date datetime values (such as 0000-00-00) by aligning snapshot and CDC mapping.
- Salesforce Bulk API: Base64 fields (Blobs) are now automatically skipped for synced objects because this type isn’t supported by the Bulk API.

### Connectors 2026.2.3.18

- Kafka: New Kafka to Snowflake connector with Kafka OAuth authentication support.
- CDC Databases: Non-CDC processors in CDC connectors now include a table state change reason.
- Salesforce Bulk API: Reduced the default `Max Batch Size` in PutSnowpipeStreaming to lower memory pressure for records with large fields.
- Salesforce Bulk API: Added a parameter to disable incremental offloading, allowing full object syncs each execution to account for formula fields.
- Salesforce Bulk API: Added support for non-Bulk API compatible objects such as Knowledge data.

## February 3, 2026

### Control Plane Core 0.101.2

- Temporarily restricting Snowflake deployment upgrades to users whose active role matches the deployment owner role until a related issue is resolved.

## February 2, 2026

### Control Plane Core 0.101.1

- Temporarily limiting Snowflake deployment upgrades to the deployment owner while an issue preventing roles with `OPERATE` privilege from upgrading is resolved.

## January 30, 2026

### Control Plane UI 0.69.0

- Fixed an issue where some actions weren’t reevaluated on the current page after an active role change.
- BYOC deployments running the latest version now show their current status while processing actions like creating, upgrading, and deleting, including reporting failures when they occur.
- Added a `Download validator` button to the deployment creation dialog.

### Control Plane Core 0.101.0

- Fixed an issue where Snowflake deployments briefly showed a `Not Healthy` status while creating, just before becoming active.
- BYOC deployments running the latest version now show their current status while processing actions like creating, upgrading, and deleting, including reporting failures when they occur.
- Improved the logic for showing the Private Link option when creating SPCS deployments to avoid failures when the option isn’t fully supported.
- Added an API to generate and download CloudFormation templates for BYOC and BYO-VPC validators.

### Data Plane Service 0.101.0

- Fixed runtime creation on newly active Snowflake deployments. Previously, the latest available runtime versions weren’t always used.

### AWS Data Plane Agent 1.16.0

- Snowflake-hosted container images are now pulled directly from Snowflake registries into the deployment EC2 agent host and EKS cluster. Upgrade existing Openflow runtimes to switch entirely to Snowflake-hosted images.
- The agent now reports its current status to Openflow while processing user-requested actions, so it can be reflected in the Control Plane UI.
- Security patches and dependency upgrades.
- Added quick validation tools for BYOC and BYO-VPC deployments that report common errors to resolve before installing a full Openflow cluster.
- Improved reliability of deployment upgrades by automatically resolving issues where services were blocked from starting.
- Improved reliability of deleting deployments that had been upgraded multiple times.

### Runtime Server 2026.1.29.22

- Upgraded JDK to 21.0.10.
- Upgraded Apache NiFi API to 2.6.0, adding support for the `Record Gauge` method in ProcessSession.

### Runtime Extensions 2026.1.29.23

- Added the UpdateGauge processor with configurable `Gauge Name` and `Gauge Value` recording.
- Improved JSON Schema validation in GenerateJSON to address potential edge cases for nested fields.
- Added the PutIcebergRecord processor and Iceberg REST Catalog controller services, supporting both AWS and Azure storage FileIO providers.
- Deprecated the PutIcebergTable processor in favor of PutIcebergRecord.

## January 23, 2026

### Runtime Server 2026.1.22.19

- Resolved an issue where simultaneous commits to a Git-based Flow Registry Client could cause one user’s changes to overwrite another’s.
- New Runtime UI 0.63.0.

### Runtime Extensions 2026.1.22.19

- Salesforce Bulk API: Fixed an edge case where the initial snapshot might not create the destination table as expected.
- BigQuery: Processor properties now reference FlowFile attributes, making it easier to understand component behavior.
- Snowpipe Streaming v2: PutSnowpipeStreaming2 now tracks request IDs and automatically terminates empty relationships.
- CDC SQL Server: You can now set a maximum FlowFile size in CaptureChangeSQLServer.
- Jira: Components now include a verification feature to confirm that your configuration is correct.
- Confluence: Components now include a verification feature to confirm that your configuration is correct.

## January 21, 2026

### Runtime Server 2026.1.20.19

- You can now configure custom SSL certificates in GitHub and GitLab Flow Registry Clients.

### Runtime Extensions 2026.1.20.21

- Enhanced PerformSnowflakeCortexOCR with page splitting and filtering features.
- BigQuery: Fixed time travel timestamp handling in TriggerBigQueryCdcOnState processor.
- Jira: Better handling of API rate limiting.
- CDC Oracle: You can now set a maximum FlowFile size in CaptureChangeOracle.
- CDC MySQL: Added logging in CaptureChangeMysql processor to log the retention period for binlog on start.
- Confluence: The connector can now ingest file attachments and embedded images.
- CDC MySQL and PostgreSQL: FetchTableSnapshot now includes partition chunk attributes to enable multi-channel streaming.

### Connectors 2026.1.20.18

- All Connectors: The default Snowflake Authentication Strategy is now SNOWFLAKE\_MANAGED, a token-based method that works in both SPCS and BYOC deployments.
- Salesforce Bulk API: Added new parameter, Initial Load Chunking. This option lets you split large initial data loads into time-based chunks (MONTHLY, QUARTERLY, YEARLY) to avoid timeouts and API limits.

  When set, the initial data load is split into multiple jobs based on the interval. On the first run for an object, the connector queries Salesforce to find the oldest record and uses that as the starting point. Each subsequent job queries the next time chunk until caught up to the current time.

  Once caught up, the processor continues with normal incremental offload behavior.
- Oracle: Initial snapshot loads can now run with multiple concurrent threads for faster performance.
- SharePoint: The connector now logs when it encounters and processes empty files.
- Confluence: A new connector version is available that does not fetch access control lists (ACLs).

## January 16, 2026

### Runtime Server 2026.1.15.20

- New Runtime UI 0.62.0.
- The copy button in the Bulletin tooltip has been moved so it’s always visible.

### Runtime Extensions 2026.1.15.20

- SQL: Added support for Pre-Queries and Post-Queries in PutDatabaseRecord processor.
- CDC PostgreSQL: You can now set a maximum FlowFile size in CaptureChangePostgreSQL.
- CDC PostgreSQL and MySQL: FlowFiles now include start.row.index and last.row.index attributes.
- CDC MySQL: CaptureChangeMySQL now reads the event position from the header instead of from the binlog client.
- CDC Connectors: Splitting FetchTableSnapshot output FlowFiles into chunks of MAX\_OUTPUT\_FLOWFILE\_SIZE size.
- Snowpipe Streaming: PutSnowpipeStreaming2 now has dedicated handling for empty FlowFiles.
- Salesforce Bulk API: Added support for Objects without SystemModStamp field.
- Salesforce Bulk API: You can now configure how the initial snapshot is split into time-based chunks.

### Connectors 2026.1.15.18

- Salesforce Bulk API: Added support for Objects with Tracking History enabled.
- Salesforce Bulk API: Added support for Objects without SystemModStamp field.
- CDC Connectors: Clearer log messages when a table enters a failed replication state.
- Google Ads: New “Login Customer ID” parameter lets you specify which manager account (MCC) to fetch reports for.
- Dataverse: The COPY GRANTS option is now applied to destination tables.

## January 15, 2026

### AWS Data Plane Agent 1.15.0

- Resolved an issue where some IAM policies were not deleted when a Deployment was deleted.

## January 14, 2026

### Runtime Server 2026.1.13.18

- Resolved an issue with how validation was triggered when Flow Registry Clients were configured.

### Runtime Extensions 2026.1.13.19

- Google Ads: The connector now works with manager accounts and their subaccounts.
- Oracle: Added new processors designed to accelerate initial snapshot loads.
- Snowpipe Streaming: PutSnowpipeStreaming2 now includes a counter for each destination.
- SQL: PutDatabaseRecord now uses setBytes binding for BINARY SQL types.

### Connectors 2026.1.13.16

- Slack: Improved handling of file attachments with Slack messages.
- Unstructured Connectors: Resolved Null Pointer Exceptions that occurred when parameters were left empty.
- Google Drive: You can now specify multiple folders by using a comma-separated list in the “Folder Name” parameter.
- Google Drive: New Simple Ingest and Cortex connectors that don’t require domain-wide delegation.
- Streaming Destination Modules: PutSnowpipeStreaming now limits channel concurrency for streaming destinations.

## January 12, 2026

### Control Plane UI 0.68.0

- You no longer need OWNERSHIP privilege on the Snowflake Role when configuring BYOC and SPCS Runtimes.
- You no longer need CREATE USER privilege to create a BYOC Runtime.
- **Behavior change:** Starting with AWS Data Plane Agent 0.37.0, you must specify a Snowflake Role when creating a Runtime.

## January 8, 2026

### Control Plane UI 0.67.0

- The Deployment details dialog now correctly shows Private Link and End User Auth over Private Link settings.
- The SAP connector card now displays an updated icon.
- The Runtime and Deployment details dialogs now display the SQL name when available.
- The Create Runtime dialog now requires a Snowflake role. It no longer requires CREATE USER privilege.

### Data Plane Service 0.98.0

- The system now polls less frequently for new Runtime versions, reducing query costs.
- Runtime Upgrades are now more reliable because all related components are discovered and upgraded together.

### AWS Data Plane Agent 1.13.0

- Resolved an upgrade failure affecting older Deployments that pulled helm charts from AWS OCI Repository.

### SPCS Data Plane Agent 1.11.0

- The deployment creation sequence has been optimized to reduce wait time.

## January 6, 2026

### Runtime Server 2026.1.5.14

- When you clear bulletins on a process group, bulletins for its scoped controller services are also cleared.
- Registry Clients no longer log confusing WARN messages when you commit the first version of a flow.

### Runtime Extensions 2026.1.5.19

- Oracle: Archive logs are now properly removed even when database traffic isn’t captured by XStream Out server.
- JIRA: Resolved a resource leak triggered by certain HTTP error codes and improved log messages.
- Azure components: Fixed NoClassDefFoundError: io/netty/handler/codec/quic/Quic.
- Kafka: The verification process is improved and now returns information about the Kafka Connection Controller Service.
- MS SQL Server: Database names with special characters are now properly quoted when available tables are fetched.

### Connectors 2026.1.5.13

- All Database CDC Connectors: The snapshot completion log now shows the correct total number of rows ingested.
- All Unstructured Connectors: The Cortex service name parameter is now correctly applied to documents.
- MySQL & PostgreSQL: You can now configure concurrency settings for Snapshot loads.
- JIRA: Performance is improved by reducing small FlowFiles and batching data sent via Snowpipe Streaming.
- Google Drive: Inserts via Snowpipe Streaming can now run in parallel instead of sequentially.

## December 19, 2025

### Runtime Oracle Extensions 2025.12.19.8

- Fixed an issue validating Oracle licenses that prevented the OracleCapture processor from starting.
- Improved change detection for large schemas.

## December 17, 2025

### Runtime Server 2025.12.16.19

- Improved how invalid controller services are handled when you enable or disable them.
- Included Registry Clients in the Runtime documentation.

### Runtime Extensions 2025.12.16.19

- PostgreSQL: Fixed ordering of composite key columns.

### Connectors 2025.12.16.19

- Salesforce Bulk API: Added a new parameter to control case sensitivity for object identifiers created in Snowflake. By default, column names remain case sensitive for backward compatibility. This default may change at public preview or general availability.
- Confluence Data Center: New connector to integrate with Confluence Data Center edition.

## December 16, 2025

### AWS Data Plane Agent 1.12.0

- Fixed an issue where BYOC deployment upgrades failed due to a mismatch between the machine image and Kubernetes cluster versions.
- Fixed an issue where BYOC deployment upgrades failed with the error message “OCI Registry Login Failed”.

## December 11, 2025

### Control Plane Core 0.95.0

- Fixed an issue where the Runtime Run As Role couldn’t be set for roles containing Snowflake-restricted characters, such as hyphens.

### Runtime Server 2025.12.11.21

- Improved behavior when enabling controller services that are invalid and shouldn’t be enabled.
- New Runtime UI 0.59.0.
- Registry clients now support property verification.

### Runtime Extensions 2025.12.11.21

- AWS Secrets Manager: Parameter Provider now considers non-string values as valid parameters.
- RenameRecordField processor now properly handles multiple records per FlowFile.
- Kinesis: Fixed an issue where the ConsumeKinesis processor throttled new records even when buffers were empty.
- Snowflake: Added a default network timeout to the Snowflake Connection Service.
- Confluence: Fixed handling of page deletion.
- Confluence Data Center: Fixed the HTTP response decoder for the client.
- MySQL: Improved logging for table mapping when consuming binlog events.
- CDC Databases Connectors: Observability dashboards now display the failure reason when a table’s replication status changes to failed.

### Connectors 2025.12.11.18

- SQL Server: Exposed new parameters (Re-read Tables in State and Starting Change Tracking Position) for starting position.
- Oracle: Set CASE\_INSENSITIVE as the default for created Snowflake objects.
- Jira: Added support for App Forge authentication method.
- Confluence: Added support for App Forge authentication method.
- Oracle: Fixed missing service name in XStream URL in default parameter values.
- Oracle: Added support for internationalization.
- Unstructured Connectors: Added a parameter to specify the Cortex Search Service name.
- Slack Connectors: Added a parameter to control whether user names are resolved.

## December 9, 2025

### Control Plane Core 0.94.0

- Added support for accessing and using Openflow with an organization or account that has been renamed.

## December 8, 2025

### AWS Data Plane Agent 1.11.0

- Fixed issue upgrading older deployments with non-critical “inconsistent result after apply” error message.

## December 5, 2025

### Runtime Server 2025.12.4.19

- New Runtime UI 0.58.0.
- Added new action to clear bulletins.
- Improved error handling when launching the Status History dialog.

### Runtime Extensions 2025.12.4.19

- Kinesis: Fixed checkpoint committed records in ConsumeKinesis that could previously cause data loss.
- PostgreSQL: Fixed issue where CaptureChangePostgreSQL ignored events when data was loaded via COPY FROM STDIN.

### Connectors 2025.12.4.17

- CDC SQL Server MultiDB: Added and exposed support for case sensitivity for created Snowflake objects.

## December 3, 2025

### AWS Data Plane Agent 1.10.0

- Added support for encrypting EBS volumes across the entire Openflow Deployment.

### SPCS Data Plane Agent 1.9.0

- Snowflake Deployments encountering internal certificate authority mismatch issues are now auto-healed on upgrade.

### Control Plane Core 0.93.0

- Retained visibility and use of resources when an account name or organization is changed.
- Improved resource utilization efficiency for Small size runtimes in Snowflake Deployments, allowing 3 runtime pods per node instead of 2.
- Added Manage endpoints action for SPCS deployments (requires account parameter).
- Improved external access integration (EAI) list to only show those EAIs the user has access to when creating a runtime in a Snowflake Deployment.

### Data Plane Service 0.93.0

- Improved resiliency of automatic diagnostic bundling and cleanup behavior when a runtime fails to create.
- Added management capabilities for Openflow endpoints in a deployment accessible via new API methods.
- Extended wait time for runtime upgrade failures in SPCS deployments to avoid premature timeout and failure.

### Control Plane UI 0.65.0

- Added Manage endpoints action for SPCS deployments (requires account parameter).

### Data Plane UI 0.11.0

- Added Openflow endpoints management view for SPCS deployments (requires account parameter).

### Openflow Ingress Controller 2025.12.2-17

- Added support for routing to Openflow endpoints attached to Openflow runtimes.
- Fixed client IP address forwarding when evaluating Snowflake privileges for Openflow runtimes.
- Fixed request header propagation to support deployments with Private Link enabled.

### Runtime Server 2025.12.3.16

- Added support for discovering listen ports from Openflow runtime processors to provide users as available targets for Openflow endpoints.
- Controller Services: Fixed validation and enabling that could take too long and cause the runtime to not start.

### Runtime Extensions 2025.12.3.16

- Kinesis: Introduced Shared Throughput consumer in ConsumeKinesis and removed concurrency limits in the HTTP client.
- Kafka: Added support for specifying custom SASL Extensions.
- EventHub: Added support for OAuth authentication in EventHub processors.
- AWS RDS: Added support for AWS RDS IAM Authentication in the DBCP Connection Pool to access databases over JDBC.
- Listen\* Processors (Examples: ListenHTTP, HandleHttpRequest, ListenOTLP): Added support for new ListenComponent and ListenPortDefinition NiFi APIs to allow discovery of listen ports for use with Openflow endpoints.
- OpenflowRuntimeSSLContextProvider: Added new control service for use with Listen\* Processors to integrate with Openflow endpoints.
- Oracle: Fixed handling of case sensitivity on column names when using lower casing.
- Oracle: Fixed support for internationalization.
- MySQL: Fixed filtering of Azure-specific system tables.
- BigQuery: Added new components for the Google BigQuery Change Data Capture (CDC) connector.
- SQL Server: Added ability to choose the starting position when reading the stream.
- Confluence Data Center: Improved support for Audit Records ingestion.
- Confluence: Improved performance to retrieve Confluence page IDs.
- Confluence: Added support for Forge App authentication method.
- Google Drive: Improved recursive listing efficiency when listing the content of a drive.
- Slack: Fixed fetching information of users for large workspaces with a large number of users.

### Connectors 2025.12.3.15

- Google Drive: Fixed potential NullPointerException when Google Drive Folder parameter is not set.
- Slack: Added check to verify files have content before uploading to Snowflake.
- CDC PostgreSQL: Increased backpressure settings to better support large number of synced tables.
- Dataverse: Improved the query for the deletes in the Journal Table.

## December 2, 2025

### Control Plane Core 0.92.0

- Fixed a thread contention issue in Snowflake Deployments that could cause some Runtime actions triggered from Control Plane to time out and fail.

### Data Plane Service 0.92.0

- Fixed a thread contention issue in Snowflake Deployments that could cause some Runtime actions triggered from Control Plane to time out and fail.

### Openflow Ingress Controller 2025.11.20-18

- Added support for Programmatic Access Token authentication and authorization.

### Openflow Runtime Gateway 2025.11.19.22

- Added support for Programmatic Access Token authentication and authorization.

## November 21, 2025

### AWS Data Plane Agent 1.8.0

- Restores support for private Openflow BYOC Deployments by removing all dependencies on URLs outside of Snowflake and AWS, addressing an issue introduced in 1.6.0

### Control Plane Core 0.91.0

- Fixed a rare issue that prevented a Runtime from being activated after it had been suspended

### Data Plane Service 0.91.0

- Fixed an issue causing connector installations to fail on new Runtimes when bulletins are present

## November 20, 2025

### Runtime Server 2025.11.20.20

- Improved visibility of Runtime operations with new metrics for Connectors

### Runtime Extensions 2025.11.20.19

- New components to interact with SAP Business Data Cloud and mapping of CSNs into Snowflake Semantic Views
- CDC MySQL - Improved reliability by clearing out the table map prior to CDC reconnects
- CDC Databases - Fixed a potential deadlock issue with MergeSnowflakeJournalTable when “poll query result” is cleared during operation
- CDC MariaDB - Added support for MariaDB in the MySQL components
- CDC PostgreSQL - Added support for primary keys of type `numeric`

### Connectors 2025.11.20.17

- CDC Databases - Adjusted backpressure thresholds on some connections when processing a lot of data
- Salesforce - Gracefully handle scenarios where we insert duplicate rows in the staging table
- CDC Databases - Exposed parameter to enable private connectivity in the PutSnowpipeStreaming processor for data ingest
- CDC PostgreSQL - Adjusted yield duration on CaptureChangePostgreSQL to not overuse replication connections

## November 19, 2025

### Runtime Extensions 2025.11.18.22

- SQL Server - Performance improvement in Snapshot query
- Dataverse - Schemas are no longer filtered when no column filtering value is provided
- Telemetry - “Bytes Received” is now available for many Snowflake processors after fixing the file size for provenance events
- Azure components - Fix ConsumeAzureEventHub by excluding netty-codec-http3 dependency
- Google Cloud - Added support for Workload Identity Federation
- Azure Blob Storage - Added support for uploading files larger than 200 GB

### Connectors 2025.11.18.17

- Google Ads - Set the new Authentication Strategy property of the GCP Credentials Controller Service
- Multi Database SQL Server - Fix `source.table.fqn` value handling
- Salesforce - Add logging for successful sync operations to ease monitoring via the events table

### AWS Data Plane Agent 1.6.0

- Improves security by removing unused inbound ports on Load Balancers configured for “Custom Ingress.” You can further limit access with your own Security Group for these Openflow Deployments.
- Improves security and eased configuration of Runtimes with an optional Deployment-level IAM Role to securely access AWS resources like RDS, MSK, Kinesis, and S3. You can now attach IAM Policies to Openflow’s “NodeInstanceRole” that are granted to all Runtimes in that Openflow Deployment.
- Upgrades EKS Cluster from 1.32 to 1.34 for long-term maintenance and security patching
- Resolves an issue where restarting some EC2 nodes frequently caused the Openflow Deployment to freeze
- Security patches and upgrades to third party libraries

### SPCS Data Plane Agent 1.4.0

- A missing event table will no longer cause failure when creating an Openflow Snowflake Deployment.
- Fixed certificate based issues accessing Runtimes and deploying Connectors into Deployments older than 60 days
- Security patches and upgrades to third party libraries

### Control Plane UI 0.64.0

- Adding support for the new Cleaning Up Runtime state
- Adding support for terms accepted trial not started or active trial

### Control Plane Core 0.90.0

- If a Runtime fails to create, it will automatically generate a diagnostics bundle and clean up any partially created resources in the cluster.

### Data Plane Service 0.90.0

- If a Runtime fails to create, it will automatically generate a diagnostics bundle and clean up any partially created resources in the cluster.

### Openflow Ingress Controller 2025.11.12-18

- Security patches and upgrades to third party libraries

## November 15, 2025

### Runtime Extensions 2025.11.16.2

- Improved reliability for high volume deployments by relocating state tracking for replication position and journal versioning in CDC Connectors

## November 14, 2025

### Runtime Server 2025.11.14.17

- Easier debugging with an updated Bulletin Board that can expand stack traces
- Fixed bug when rendering Documentation for extensions that lack tags
- Viewing component state now supports showing 5,000 local entries and 5,000 cluster entries, up from 500 each

### Runtime Extensions 2025.11.14.17

- Reduced costs by removing the validation query in the Snowflake Connection Service

### Connectors 2025.11.14.14

- Google Drive and Google Sheet - Set the new Authentication Strategy property of the GCP Credentials Controller Service

## November 13, 2025

### Runtime Extensions 2025.11.13.19

- Added support for Web Identity authentication to AWS MSK IAM Connection Service in Kafka components
- Added support for Web Identity authentication to AWS Credentials Controller Service for all AWS components
- Added Flow Registry Client support for Bitbucket Data Center edition
- Fixed Worker ID generation in ConsumeKinesis and added provenance data
- Added support for nested paths in HashiCorpVaultParameterProvider
- Dataverse - Added retry-after mechanism
- Added Snowflake Secrets Parameter Provider
- CDC Database Connectors - Improved reliability and performance on state management
- JIRA - Enriched issues with email addresses
- HubSpot - Fixed handling of 414 error code responses while fetching objects

### Connectors 2025.11.12.21

- Dataverse - Add Column JSON Filtering parameter
- PostgreSQL - Added FIFO FlowFile prioritizer on queues in Postgres Snapshot Load
- MySQL - Expose parameter for the starting position of the replication
- Dataverse - Added updated\_at and deleted columns
- Salesforce - Switched the CSV Reader to RFC 4180
- Salesforce - Fixed configuration to capture soft deletes

## October 31, 2025

### AWS Data Plane Agent 1.1.0

- Security patches and upgrades to third party libraries

### SPCS Data Plane Agent 1.1.0

- Security patches and upgrades to third party libraries

### Control Plane Core 0.88.0

- Enable Openflow Oracle Connector in Snowflake Deployments

### Data Plane Service 0.88.0

- Security patches and upgrades to third party libraries

### Runtime Operator 0.45.0

- Security patches and upgrades to third party libraries

### Runtime Extensions 2025.10.31.13

- Improved reliability of high volume CDC Connectors

## October 30, 2025

### Runtime Extensions 2025.10.30.21

- CDC Database Connectors - New components for multi-databases support are now included in the runtime image
- JIRA - Added support for Forge App authentication method
- New OAuth2 controller service to get Snowflake issued JWTs for Workload Identity Federation

### Connectors 2025.10.30.20

- PostgreSQL - Added First In First Out (FIFO) connection prioritizer in PostgreSQL Snapshot load
- CDC Database Connectors - Disabled load balancing in the incremental flow to ensure single node processing of the data
- Dataverse - Added parameter for the new JSON Column Filtering property

## October 29, 2025

### Runtime Server 2025.10.28.18

- Fixed bug in Summary table formatting Process Group task time

### Runtime Extensions 2025.10.28.20

- Kinesis - Support Output Strategy property in ConsumeKinesis processor
- Kinesis - Added the new Kinesis components leveraging the latest AWS client library
- SQL Server - Added support for multiple databases
- MySQL - Added the possibility to specify the binlog starting position for reading the CDC stream
- PostgreSQL - Added support for negative scale in numeric types
- SQL Server - Improved the ordering of the ORDER BY clause
- Snowpipe Streaming - Improved Input Buffer Handling in PutSnowpipeStreaming2
- PostgreSQL - Improved performances in FetchTableSnapshot on large tables with composite primary key
- MySQL - Fixed incorrectly replicated DATEs pre 1582-10-15 (Julian calendar)

### Connectors 2025.10.28.9

- Oracle - support for multiple logical databases
- MySQL, PostgreSQL, SQL Server - no longer writing the unused avro.schema FlowFile attribute
- Jira - support for fetching Worklogs

## October 28, 2025

### AWS Data Plane Agent 0.61.0

- Security patches and upgrades to third party libraries

## October 27, 2025

### Control Plane UI 0.63.0

- Security patches and upgrades to third party libraries

## October 24, 2025

### Control Plane Core 0.86.0

- Fixed issue where a user can’t log into Openflow if their most recently selected active role was revoked.
- Disable creating a Snowflake Deployment if the user’s role is not granted CREATE COMPUTE POOL privilege.

### Control Plane UI 0.62.0

- Improved display for Upgrade Failed, Inactive, and Activate Failed states
- Always show the current “Run As” role even if it’s not in the current user’s set of account roles
- Fixed issue with “Run As” role validation in Create Runtime dialog

## October 23, 2025

### Runtime Server 2025.10.23.16

- Bulletin icons now reflect the severity of the message
- Parameters can now be edited by double clicking on the row in the Parameter Context
- Included state of system diagnostics API call in the loading skeleton and spinner in the Cluster Listing
- Improved awareness of errors through the global banner when extension types fail to load
- Updated styling for unset, blank, empty styles throughout the Runtime UI

### Runtime Extensions 2025.10.23.11

- Fixed incorrect handling of Drop Table actions in UpdateSnowflakeTable processor
- Oracle - Improved performance by moving metadata generation in FetchSnapshot processor
- Oracle - Fixed handling of column filters DDL
- Dataverse - Added optional configuration to filter columns being fetched
- Cortex - Improved error message when there is an issue calling Cortex in PromptSnowflakeCortex processor
- MySQL - Fixed the filtering out of the “user” table
- Salesforce Data Cloud - Added support for detecting deletions of Data Shares and linked Objects in the shares
- MySQL - Fixed skipping compressed transaction DDLs and DMLs spanning over the transaction
- JIRA - Enrich Jira Worklogs processor
- Confluence - Support for Confluence Data Center edition
- Added Offset Tracking Resolution to PutSnowpipeStreaming2 processor
- Sharepoint - Fixed pagination handling when listing more than 200 items
- Salesforce - Added optional lookup key in UpsertSFDCObjects processor allowing user to specify a field other than ID for retrieving the record to upsert

### Connectors 2025.10.22.17

- Excel - Added missing SPCS related configuration options
- HubSpot - Added support for new object types: Notes, Orders and Carts
- Salesforce - Added missing configuration for authentication strategy for usage of the connector in Openflow Snowflake Deployments
- PostgreSQL - Migrated the connector to standard identifiers for better management of case sensitivity on object naming
- Oracle - Removed the addition of Snowflake Specific Columns to leverage FetchSnapshot processor instead and improve performances
- Sharepoint - New Simple Ingest connector that does not fetch the ACLs associated to the data
- Salesforce - Added support for specifying the object fields that should be included/excluded when retrieving the data

## October 20, 2025

### Control Plane Core 0.84.1

- Released Control Plane Core version 0.84.1.

## October 17, 2025

### AWS Data Plane Agent 0.60.0

- Fixed certificate issues that blocked access to runtimes and connector deployments in deployments older than 60 days.

### Control Plane Core 0.84.0

- Fixed input validation issues when filtering in role selection menus.
- Fixed an issue where links to runtimes were shown to users without access privileges.
- Fixed an issue where users with only USAGE privilege on a runtime couldn’t create connectors in that runtime.
- Fixed an issue for users accessing Openflow over PrivateLink with a network policy enforcing the VPCE ID.
- Added support for suspending and activating runtimes in Snowflake deployments.
- Snowflake deployments now display their current version immediately after creation is initiated.

### Control Plane UI 0.60.0

- Warns users before navigating to a deployment or runtime where VPN connectivity may be required when using custom ingress.
- Keeps the selection panel open for multi-select components after a selection is made.
- Enforces user permissions for viewing the runtime canvas and hides links if permissions are missing.
- Improves setup experience by considering total counts of runtimes and deployments, not just those in the ACTIVE state.
- Makes the Snowflake role optional when creating a runtime in a BYOC deployment.
- Improves text overflow handling for connector cards.

### Openflow Ingress Controller 2025.10.16-17

- Fixed an issue that prevented access to runtimes over PrivateLink.
- Fixed an issue where a new runtime couldn’t be accessed if its name matched that of a previously deleted runtime.

## October 15, 2025

### Runtime Extensions 2025.10.14.22

- Added Snowflake Managed Authentication Strategy to SnowflakeConnectionService and PutSnowpipeStreaming.

### Runtime Oracle Extensions 2025.10.14.22

- Improved snapshot query performance by correcting ORDER BY column sorting.

### Runtime Server 2025.10.14.12

- Fixed missing Process Group identifier information in Processor and Controller Service log records.

## October 08, 2025

### AWS Data Plane Agent 0.59.0

- Added support for workarounds when using self-managed certificates in AWS.
- Fixed issues that caused BYOC deployment upgrades to get stuck with invalid image references and job cleanup.
- Restored support for adding customer-managed IAM policies to Openflow’s IAM roles.

## October 03, 2025

### Connectors 2025.9.30.17

- Updated the Dataverse connector to set empty collation for the Dataverse journal table.

### Runtime Extensions 2025.10.2.19

- Added better support for case sensitivity on Snowflake objects in `MergeSnowflakeJournalTable`.
- Improved HubSpot pagination handling when retrieving more than 10,000 records.
- Unstructured Processing - `PerformSnowflakeCortexOCR` now uses the `AI_PARSE_DOCUMENT` function instead of `PARSE_DOCUMENT`.
- Added better support for case sensitivity on Snowflake objects in PutSnowpipeStreaming.
- PostgreSQL - Fixed unsigned handling of type OIDs in the CaptureChangePostgreSQL processor.

### Runtime Server 2025.9.30.19

- New Runtime UI 0.53.0.
- Fixed a regression that prevented tabbed dialogs from remembering the previously active tab.
- Fixed balto icon regressions and selected radio button display issues.
- Fixed an issue where Parameter Context update requests weren’t deleted when users canceled the request.
- Fixed an issue that caused double scroll bars to appear in the asset upload dialog.
- Fixed an issue where the selected asset count could get out of sync.

## September 26, 2025

### AWS Data Plane Agent 0.52.0

- Improved efficiency of private IP addresses used by EKS cluster nodes, reducing the total number required for scaling out to many Runtime nodes.
- Fixed issue with Runtime logs that incorrectly redacted some component IDs.

### Connectors 2025.9.25.17

- Confluence connector - Better failure handling and retries when facing API rate limits.

### Control Plane Core 0.80.0

- Support for deploying Oracle Runtime Extensions to Runtimes in BYOC Deployments for PrPr customers who have accepted the Terms of Service.
- Fixed an issue where Snowflake deployment moved into an active state prematurely during an upgrade.
- Fixed a rare issue where Snowflake deployment deletions could get stuck and need manual intervention.

### Control Plane UI 0.57.0

- Introduced new deployment upgrade dialog that shows the version mapping.

### Data Plane Service 0.80.0

- Support for deploying Oracle Runtime Extensions to Runtimes in BYOC Deployments for PrPr customers who have accepted the Terms of Service.

### Runtime Extensions 2025.9.25.19

- CDC database connectors: Removed Record Reader from MergeSnowflakeJournalTable processor.
- All connectors log the Query ID whenever a connector executes a query in Snowflake.

### Runtime Oracle Extensions 2025.9.23.19

- PrPr release of Oracle Extension for Openflow Runtimes.

### Runtime Server 2025.9.25.19

- Improved the Openflow Connectors upgrade user experience.

## September 23, 2025

### Connectors 2025.9.23.17

- PostgreSQL connector now includes a new parameter so you can set the replication slot name.
- The PostgreSQL, MySQL, and SQL Server connectors now support column names that include special characters.

### Runtime Extensions 2025.9.23.19

- Added compression to rows added using the Insert Rows method through PutSnowpipeStreaming2.
- MySQL: Added support for compressed bin log events.
- Added new processors, UpdateSnowflakeSchema and UpdateSnowflakeStream, to better manage object lifecycles and support case sensitivity.
- HubSpot: Added support for new “Notes,” “Orders,” and “Carts” object types.
- Slack: Fixed Null Pointer Exception when trying to verify the configuration of ConsumeSlackConservations processor.

### Runtime Server 2025.9.23.19

- Using latest Apache NiFi 2.6.0 release.
- Improved the flow upgrade user experience by improving Flow Differences Filters to handle renameProperty, removeProperty, and createControllerService.
- New Runtime UI 0.52.0.
- Fixed bug allowing default values for dynamic properties.
- Improved the performance of the searchable select used in the Property combo editor.

## September 19, 2025

### AWS Data Plane Agent 0.50.0

- Openflow now supports VPCs with DHCP Option Sets, making it easier to connect to private data sources.
- You can now secure Openflow deployments with PrivateLink, while still allowing browser-based authentication to runtimes without PrivateLink.
- Fixed an issue during upgrades where IAM inline policies failed by exceeding maximum character limits.

### Control Plane Core 0.78.0

- Improved error messages for Snowflake deployment failures to show the root causes.
- Fixed a case where BYOC deployment ends up in Not Healthy state but can’t be deleted from Openflow Control Plane.

### Control Plane UI 0.55.0

- Removed unnecessary title on **Runtime and Deployment state** columns.

### Openflow Runtime Gateway 2025.9.18.22

- Improved cookie session handling to allow users to remain logged in, even when Runtime is open in an inactive browser tab.

## September 18, 2025

### Connectors 2025.9.17.18

- Addition of the 2 new Oracle CDC connectors.
- Confluence connector - The introduction of a new controller service to handle API rate limits will show the connector as a process group with local changes.
  This can be ignored and will be resolved when upgrading the connector to the next version, when available.

### Runtime Extensions 2025.9.18.18

- Introduced the `UpdateSnowflakeTable` processor, which is like `UpdateSnowflakeDatabase`, but designed for tables and improved case sensitivity.

## September 16, 2025

### Connectors 2025.9.16.18

- SQL Server connector: Exposed the new SQL Server query interval property as a parameter.
- The new controller service for API rate limits in the Jira connector causes the connector to appear as a process group with local changes. You can safely ignore this; it will be fixed in a future connector upgrade.

### Control Plane UI 0.54.0

- Allow users to optionally configure whether end users authenticate over PrivateLink.
- The **Estimated time to completion** shown when creating Snowflake Deployments and Runtimes is now more accurate.

### Openflow Ingress Controller 2025.9.15-14

- Initial release offering privilege isolation for Openflow runtime authentication and authorization to Snowflake deployments.

### Runtime Extensions 2025.9.16.20

- Added support for DATETIME columns with PutBigQuery processor.
- You can now specify the HTTP protocol version in **StandardWebClientServiceProvider**.
- Better logging and increased timeouts for FetchSharepointFile processor.
- Added the option to set the replication slot name in CaptureChangePostgreSQL processor.
- You can now use `-infinity` and `+infinity` with Postgres TIMESTAMPTZ values.
- New controller service StandardAtlassianRequestRateManager to deal with API rate limits for the Jira connector.
- Fixed exceptions thrown from ListMicrosoftDataverseTables when table schema isn’t returned by API.

### Runtime Operator 0.40.0

- Support deploying the new Openflow ingress controller for PuPr release of Snowflake deployments.

### Runtime Server 2025.9.16.19

- New Runtime UI 0.51.0.
- You can now delete individual entries in the component state if the component allows it.
- Improved tooltips for Property and Parameter values, especially when values are long or reference external resources.

## September 15, 2025

### AWS Data Plane Agent 0.41.1

- Fixed an issue from AWS Data Plane Agent 0.39.0 that blocked the first install of an Openflow deployment into a new AWS region.

## September 11, 2025

### Control Plane Core 0.73.0

- Fixed issue preventing runtime deletion in Snowflake deployments when a network policy is present.

### Data Plane Service 0.73.0

- Fixed an issue that prevented runtime deletion in Snowflake deployments when a network policy was present.
- Fixed an issue that prevented new versions of runtime extensions from being used when runtimes were created or upgraded.

### Runtime Extensions 2025.9.11.18

- CaptureChangeSQLServer: A new setting, `Table Changes Query Interval`, is introduced to reduce the resource pressure on the source database. Now, the processor queries the source database every 10 seconds (`10 sec`) by default. To restore the original behavior, change the setting to `0 sec`.

## September 10, 2025

### AWS Data Plane Agent 0.40.0

- Resolved an issue where deployments were left partially upgraded after AWS Data Plane Agent 0.39.0 was used.

### Connectors 2025.9.9.18

- Unstructured connectors: Improved reporting on `ChunkText` failures.

### Runtime Extensions 2025.9.10.7

- Microsoft Dataverse: Fixed handling of schemas that include the `Edm.Date` type.
- Fixed attribute prefix handling in the XML Reader.
- Fixed MongoDB controller service for certain authentication methods when information is provided through the URI.
- Added Azure DevOps Flow Registry Client for Git integration with Azure DevOps to version flows.

### Runtime Server 2025.9.9.20

- Added the ability to change the version of a ghosted component if a bundle with the same coordinates and a different version exists.

## September 8, 2025

### AWS Data Plane Agent 0.37.0

- Added support for AWS Data Plane Agent deployments that have DHCP Option Sets configured on the account.
- Upgraded all EKS nodes from Amazon Linux 2 to Amazon Linux 2023.

### AWS Data Plane Agent 0.38.0

- Added support for AWS accounts that require encrypted EBS volumes by default, even if an unencrypted EBS volume is requested. Customers can enable this by adding IAM Policies to the `*-eks-role IAM Role` that grant access to their KMS keys.

### Control Plane Core 0.72.0

- Error messages are now clearer and more informative when runtime-related failures occur.
- Fixed a rare case where an older deployment version disallowed creating a runtime with the same name as a previously deleted runtime.

### Control Plane UI 0.52.0

- Deployment listing and details now include the deployment version number.
- Control Plane logout page now offers a link back to Snowsight
- Searchable select control (used in **Create Runtime** and **Manage Access**) now offers improved behavior when text overflows available space.
- Fixed a bug that temporarily showed duplicate roles when revoking privileges through the **Manage Access** dialog.

### Data Plane Service 0.70.0

- Added support for AWS Data Plane Agent deployments that have DHCP Option Sets configured on the account.
- Allowed customers to delete a runtime and create a new one with the same name shortly thereafter.

## September 5, 2025

### Connectors 2025.9.4.19

- Confluence Connector: Refresh frequency is now set to 1 minute and is no longer exposed as a parameter.

### Runtime Extensions 2025.9.4.20

- Resolved an incompatibility between the Github Registry Client and the latest Jackson release.
- Fixed attribute prefix handling in XML Reader
- Added `StandardProtobufReader` controller service for Protobuf record processing
- `ListTableName` won’t fail the entire FlowFile if partial input is incorrect.

### Runtime Server 2025.9.4.20

- Introduced Runtime UI 0.50.0
- Added a new logout page that provides users options for logging back in or navigating to the Control Plane.
- Enhanced the searchable select control to display options more clearly when text exceeds available space.
- Fixed casing and icon issues when inputting attributes during extension verification.
- Fixed header styling applied to additionalDetails markdown files.

## September 2, 2025

### AWS Data Plane Agent 0.35.0

- Support for AWS Tags with dots in the Tag key.

### Connectors 2025.9.2.16

- MySQL CDC: Always create a new table (and fail if the table already exists) when replication mode is set to `full`.

### Runtime Extensions 2025.9.2.17

- The GitLab Flow Registry Client now supports versioning flows larger than 2 MB.
- Fixed issue in the MongoDB Controller Service preventing users to authenticate using X509.
- Fixed irrelevant error logs about schema hash in `UpdateSnowflakeDatabase` processor.
- Confluence: Fixed a bug that prevented users from being added to authorized users even though they had permissions to the space from the group level.
- Fixed `NoSuchElementException` thrown in ChunkText processor and better failure handling with dedicated relationship.
- HubSpot: Fixed bug preventing the List processors to properly go through all the pages.

### Runtime Server 2025.9.2.20

- New Runtime UI 0.48.0.
- Upgraded to the latest version of CodeMirror and updated usage throughout the application.

## August 28, 2025

### Connectors 2025.8.28.17

- MS SQL CDC Connector: Added support for incremental only mode.
- HubSpot connector: Fixed table creation on invalid object type.

### Runtime Extensions 2025.8.28.19

- Added StandardProtobufReader Controller Service for Protobuf record processing

## August 27, 2025

### AWS Data Plane Agent 0.33.0

- Fixes health checks for Load Balancer Target Groups, so everything shows green in the AWS Console.

### Control Plane Core v0.68.0

- Supports a finer-grained privilege model for deployments and runtimes including MONITOR and OPERATE privileges.

### Control Plane UI v0.51.0

- Supports a finer-grained privilege model for deployments and runtimes including MONITOR and OPERATE privileges.

### Runtime Operator 0.39.0

- Supports a finer-grained privilege model for deployments and runtimes including MONITOR and OPERATE privileges.

## August 26, 2025

### Runtime Extensions 2025.8.26.18

- MS SQL Server: Fixes handling of datetime when used as a primary key.

## August 21, 2025

### Connectors 2025.8.21.16

- PostgreSQL connector: Supports TOASTed values.

### Runtime Extensions 2025.8.21.17

- Uses Google Ads API v21 (Note, v18 is no longer supported).

### Runtime Server 2025.8.21.17

- New Runtime UI 0.47.0.

## August 20, 2025

### Connectors 2025.8.19.17

- Slack connectors: Fixes handling of attachments by appending the File ID to the filename for the files stored in the stage.

### Runtime Extensions 2025.8.20.10

- Adds Google Cloud support to PutSnowpipeStreaming2.
- Adds support for Incremental Only mode in PostgreSQL CDC connector.
- Fixes error when trying to verify configuration in List Azure processors.

### Runtime Server 2025.8.19.18

- Supports unquoted parameter references with spaces in their names within an expression language.

## August 15, 2025

### Control Plane Core 0.64.0

- Resolves an issue that sometimes caused runtime deletion to fail in Snowflake deployments.

### Runtime Operator 0.38.0

- Resolves an issue facilitating runtime autoscaling in Snowflake deployments.

### Runtime Server 2025.8.14.18

- Improves readability in Provenance Event dialog.

## August 13, 2025

### Control Plane Core 0.62.0

- New AWS BYO-VPC deployments now add the “Private Security Group” to the EKS cluster, making it easier to configure connections to data sources.
- Resolves an issue for new Deployments with a private security group configuration that
  couldn’t pull images from Snowflake over PrivateLink.

### Control Plane UI 0.49.0

- Runtime and Deployment action menus now have separators to help group actions.
- Account roles show in a searchable selection with virtual scrolling.

### Data Plane Service 0.62.0

- Runtime flows no longer disappear after suspend and reactivate due to a conflicting auto scaling operation.

### Runtime Extensions 2025.8.12.20

- Adds FlowFile attributes support for Database and Schema properties in PutSnowflakeInternalStageFile.
- New GetConfluenceSpaces processor.
- PostgreSQL CDC now properly handles DATE, TIME, TIMESTAMP primary keys.

### Runtime Server 2025.8.12.20

- New Runtime UI 0.45.0: Minor improvements to the Component State dialog to improve
  readability of state entries.

## August 12, 2025

### AWS Data Plane Agent 0.32.0

- Fixes issue destroying BYOC deployments that was introduced with 0.29.0.
- Fixes issue from 0.29.0 release where BYOC deployments in AWS Regions with longer names may fail due to IAM Policy length limitations.

## August 7, 2025

### AWS Data Plane Agent 0.30.0

- Upgrades the AMI of EKS nodes when the deployment is upgraded.
- Removes unnecessary IPv6 Security Group rules for ingress and egress.

### Runtime Extensions 2025.8.7.20

- Improves ConsumeKafka by introducing an Inject Offset Output strategy to add a field kafkaOffset to the records.
- Adds the preview tag for Salesforce, Confluence and HubSpot components.
- Better configuration validation in UpdateSnowflakeDatabase to avoid using empty parameters.
- Adds GetConfluencePageContent and GetConfluencePageIds processors for Confluence.
- Fixes UpdateSnowflakeDatabase to properly redirect to the failure relationship when schema is not specified or does not exist.
- Improves error handling of non-authorized calls in HubSpot processors.

### Runtime Server 2025.8.7.20

- New Runtime UI 0.44.0: Improves ConsumeKinesisStream by introducing a schema difference handling strategy to specify how records using the same schema should be grouped.
- Fixes issue in rendering the canvas that surfaced on initial page load.

## August 6, 2025

### Runtime Extensions 2025.8.5.19

- Adds Pipe Info Counter and Channel Error Message to PutSnowpipeStreaming2.
- MySQL connector: Supports enabling the connector in Incremental mode only.
- HubSpot connector: Improves handling of non-supported object types and fixed processing ordering of the events.

### Runtime Server 2025.8.5.19

- New Runtime UI 0.43.0: The Runtime UI now supports labeling extensions in Preview.
  The badge is shown in the create dialog, on the canvas, in the operate palette,
  in the edit dialog, and in listings for extensions not on the canvas.

## August 5, 2025

### AWS Data Plane Agent 0.29.0

- Private deployments: All images and binaries are provided by Snowflake instead of various internet sources.
- Custom Ingress for “Bring Your Own VPC” deployments: Supports enterprise customers
  who use VPNs to access their cloud infrastructure and self-managed TLS certificates.
- Adds end-to-end support for PrivateLink. Previously, data and management communications
  were available over PrivateLink. Now, the deployment can install over PrivateLink, too.

### Control Plane Core 0.60.0

- Adds improvements necessary to support BYOC private deployments.
- Improves handling of outbound grants when transferring ownership of a runtime or deployment.
- Trial accounts are now permitted to use Openflow with relevant parameter enabled.
- Fixes an issue that disrupted use of Control Plane for customers with a large number of Snowflake roles.

### Control Plane UI 0.48.0

- In runtime and deployment listings, more actions in the menus are disabled rather than hidden.
- Removes a link to accept terms. This change prevents problems when the user doesn’t have an active Snowsight session.
- When a new version is detected, prompts the user to reload the CP UI.
- Disallows changing ownership of runtimes in Snowflake deployments.
- Fixes bug that required a Snowflake role, even when the field was hidden.

### Data Plane Service 0.60.0

- Includes improvements necessary to support BYOC private deployments.
- Fixes an issue that disrupted Connector deployment for customers with a large number of Snowflake roles.

### Openflow Runtime Gateway 2025.8.1.14

- Fixes an issue with certificate refresh upon renewal which prevented users from logging into older runtimes.

## July 31, 2025

### Connectors 2025.7.31.17

- Jira: Improved readability of the flow. The scheduling is now exposed via a parameter.

### Runtime Extensions 2025.7.31.18

- Adds File Fragment Size and Count to PutSnowpipeStreaming2.
- Introduces new Confluence processors for the upcoming connector GetConfluenceGroupUsers,
  GetConfluencePagePermissions, GetConfluenceSpacePermissions, ListConfluenceGroups.
- Adds support for TOASTed value in PostgreSQL CDC.
- Fixes initial rendering of canvas when fonts may load slowly.
- Fixes parameter removal in Parameter Contexts owned by a Parameter Provider.

### Runtime Server 2025.7.31.18

- New Runtime UI 0.42.0: Improves formatting in Status History dialog when values are lengthy.

## July 29, 2025

### Runtime Server 2025.7.29.9

- Fixes an issue with scaling that left some nodes in a disconnected state.

## July 24, 2025

### Connectors 2025.7.24.17

- Kafka Connectors: Fixes referenced readers when writing to Iceberg formatted tables.

### Runtime Extensions 2025.7.24.18

- Fixes S3 Location Type in PutSnowpipeStreaming2.

### Runtime Server 2025.7.24.18

- Adds support for users to reset all Counters in a single action.
- Fixes an issue that caused upgrade failure for runtimes with more than 1 node present.

## July 23, 2025

### Control Plane Core 0.58.0

- Adds support for selecting an active role to use in the application, rather than relying on a default role and secondary role inheritance.
- Adds support for considering Snowflake role hierarchy during authorization controls.

### Control Plane UI 0.47.0

- Adds support for selecting an active role to use in the application, rather than relying on a default role and secondary role inheritance.

### Data Plane Service 0.58.0

- Adds support for considering Snowflake role hierarchy during authorization controls.

### Openflow Runtime Gateway 2025.7.22.20

- Adds support for considering Snowflake role hierarchy during authorization controls.

## July 22, 2025

### Runtime Extensions 2025.7.22.19

- A new controller service better supports Slack API rate limits.
- Fixes SnowflakeSignJWT controller service.

## July 16, 2025

### AWS Data Plane Agent 0.25.1

- Fixes upgrades to pull and use the latest host scripts.
  This change enables Openflow to more easily make changes to the agent itself during an upgrade.

## July 15, 2025

### Connectors 2025.7.15.14

- Confluence JIRA connector: Improves type mapping for the JIRA issues.
  Uses the new processor for managing lifecycle of views.
- Slack connectors: Changes defaults for run schedule properties to avoid rate limiting errors.

### Control Plane Core 0.53.0

- Adds support for generating and downloading runtime diagnostic bundles.

### Control Plane UI 0.46.0

- Adds support for generating and downloading runtime diagnostic bundles.

### Data Plane Service 0.53.0

- Adds support for generating and downloading runtime diagnostic bundles.

### Runtime Extensions 2025.7.15.16

- Adds the PutSnowpipeStreaming2 processor using SSv2.

### Runtime Server 2025.7.15.16

- New Runtime UI 0.40.0: Fixes a bug that prevented tooltips from closing on the canvas.

## July 10, 2025

### Control Plane UI 0.45.2

- Adds support for PrivateLink redirects for the Launch Openflow button.
- Fixes an issue where logout doesn’t log the user out if the user revisits soon after.

## July 9, 2025

### Connectors 2025.7.8.14

- PostgreSQL, SQL Server and MySQL Connectors: Change to Journal creation process
  group to remove the false positive error bulletin for PutSnowpipeStreaming
  when it was asked to create channels on tables/streams that don’t yet exist.

### Control Plane Core 0.52.0

- Users must have proper privileges before they can list or view a runtime.

### Control Plane UI 0.45.1

- Fixes a bug that caused runtime and deployment listings not to show and prevented creation of new resources.

### Runtime Extensions 2025.7.9.14

- Git Registry clients have the option to ignore parameter changes when versioning a new version of a flow.
- New HubSpot processor to retrieve the schema of HubSpot objects.
- New processor UpdateSnowflakeView to manage lifecycle of Snowflake views.
- New controller service RemoveFieldRecordReader to drop fields on read.
- Supports PostgreSQL Aurora.
- CaptureChangeSQLServer generates a valid query when the primary key consists of multiple columns.
- UpdateSnowflakeDatabase now checks only column types when required.

### Runtime Server 2025.7.9.14

- New Runtime UI 0.39.0
- Improves colors in canvas for Process Group version control status.
- Improves styling for better alignment with Balto colors.
- Assets are no longer prevented from being re-uploaded in the Manage Assets dialog.
- When using form control to increment a numeric value, output from a dirty Edit Processor form is no longer prevented.

## July 3, 2025

### AWS Data Plane Agent 0.22.2

- Upgrades no longer get stuck when upgrading due to a missing Data Plane UI 0.7.0 image.

## July 1, 2025

### AWS Data Plane Agent 0.22.1

- New deployments no longer fail to install due to mid-handling failure code when
  checking for the presence of AWS ECR repositories.

### Runtime Extensions 2025.7.1.18

- Google Ads: Limits the numbers of calls to Google Ads API when validating the
  components to avoid rate limit errors.

## June 28, 2025

### Runtime Extensions 2025.6.27.21

- Fixes NullPointerException in PutSnowpipeStreaming when empty flow files are being processed
  and Delivery Guarantee is set to `Exactly once`.

## June 27, 2025

### Control Plane Core 0.51.0

- New terms of service flow: Customers can use Control Plane to create
  Snowflake-managed deployments without accepting BYOC and Connector terms.

### Control Plane UI 0.43.0

- New terms of service flow: Customers can use Control Plane to create
  Snowflake-managed deployments without accepting BYOC and Connector terms.

## June 26, 2025

### Connectors 2025.6.26.15

- Kafka Connectors: Ignore column type mismatch in UpdateSnowflakeDatabase for Kafka
  connectors is more resilient in case of issue with schema inference.
- Google Drive & SharePoint Connectors: Improves the flow to avoid a race condition
  where group synchronization kicks off but PERMS\_GROUPS has not been created yet
- Kafka Connectors: Warehouse is no longer needed. The corresponding parameter is removed.

### Runtime Extensions 2025.6.26.16

- Tables without primary keys are retried instead of failed.
- New Alter Strategy in UpdateSnowflakeDatabase processor has the option to ignore column type changes.
- Fixes fetching of HubSpot archived records.

## June 24, 2025

### Control Plane Core 0.50.0

- New deployments send status updates to Openflow Control Plane indicating when upgrades are present.
- The PrPr tag is included on some new connectors.

### Control Plane UI 0.42.0

- New deployments now surface when an upgrade is available, with a link to documentation.
  Earlier deployments can also use this functionality after a migration to a newer version.

### Data Plane Service 0.50.0

- Fixes Create runtime failures where the minimum node count is greater than one.

### Data Plane UI 0.7.0

- Active role now displays in the current user menu.

## June 20, 2025

### AWS Data Plane Agent 0.21.0

- Deployments created with AWS Data Plane Agent 0.20.0 are no longer prevented from
  adopting future updates to EC2 Agent Host scripts.

## June 18, 2025

### AWS Data Plane Agent 0.19.0

- Supports tagging all AWS resources created and managed by Openflow.
  Enables deployments governed by security controls like AWS SCP and cost controls like AWS MAP.

### AWS Data Plane Agent 0.20.0

- New Openflow BYOC deployments and upgrades of existing deployments are no longer blocked by an “Unsupported block type” error.

### Connectors 2025.6.17.15

- JIRA: Multi-projects support flattened views in Snowflake destination.

### Runtime Server 2025.6.17.16

- Process Group metrics are now visible when using the Stateless engine.
- The toolbar renders properly when font size is scaled in the browser settings.
- The UnpackContent shows the TAR option again.

## June 12, 2025

### Connectors 2025.6.12.19

- Google Sheets: Improves failure handling by retrying when ingesting data into Snowflake.
- Workday: Uses TRUNCATE instead of REPLACE when possible on the destination table.
- Sharepoint / Google Drive: Improves failure handling with proper retry / logging in case of failures.
- SQL Server: Prevents stream staleness.
- Box: Properly reflects permissions when groups are removed from files permissions in Box.
- Google Drive (Simple Ingest) - Fixes handling of files being deleted.
- Workday: Fixes clustering configuration to have the first processor run on the primary node only.

### Control Plane UI 0.41.0

- Skeleton loaders are now shown in the deployment and runtime listings when permissions are evaluated.
- Skeleton loaders are now shown in **Create Runtime** and **Add Connector to Runtime** dialogs
  while options are loaded and permissions are evaluated.

### Runtime Extensions 2025.6.12.21

- Adds the possibility to specify multiple projects to fetch JIRA issues when using ‘Simple Search’.
- Improves handling of all fields in the JIRA connector.
  Improves mapping into destination table by using an individual column per field.
- Adds support for the PuPr of Snowflake Structured Maps/Arrays/Objects.
- Google Sheets connector now supports Boolean and numbers to be used in the same column.
- MySQL: Properly handles a changes in the column filtering parameter during replication.
- MySQL: Fixes potential connection leakage when being disconnected from the binlog.
- SQL Server: Fixes column ordering handling in the Journal Log table.

### Runtime Server 2025.6.12.21

- Error reporting now shows in banners instead of toast notifications.
- Adds support for different ranges in the Status History dialog by selecting different start timestamps.
- Introduces a Process Group column to the Parameter Context table to more efficiently see bound Process Groups.

## June 8, 2025

### Runtime Extensions 2025.6.6.16

- Upgrades Snowflake JDBC Driver to 3.24.2
- Resolves an issue that prevented newer runtimes from installing the latest Microsoft Dataverse Connector.
- Removes Microsoft SQL Server replication of logical databases.

### Runtime Gateway 2025.6.8.2

- Adds support for logging in to Openflow runtimes using role names with dashes.

### Runtime Server 2025.6.6.19

- Adds pre-configured version control support for custom flows.
- Gracefully shuts down processors and controller services for stateless process groups.

## May 31, 2025

### Runtime Extensions 2025.5.31.15

- Add kafka.max.offset attribute to Records produced by ConsumeKafka
