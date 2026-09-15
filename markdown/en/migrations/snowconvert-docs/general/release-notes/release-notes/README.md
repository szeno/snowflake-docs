# SnowConvert AI - Recent Release Notes

## Version 2.44.0 (Sep 10, 2026)

### CLI

#### New Features

- Added CLI profiles and profile-aware connection precedence via `--profile`.
- Added `scai workload-insights` command for analyzing SQL Server Extended Events and Query Store data.
- Added `--with-lineage` flag to `scai test etl-validate` for auto-generating and ordering validations by ETL lineage.
- Added SQL code coverage reporting to `scai test validate`.
- Added Microsoft Entra ID service principal authentication for SQL Server source connections.
- Added Oracle Tableau repointing support via `scai code convert --tableauRepointing`.
- Added IBM DB2 as a full-migration source.
- Added BigQuery as a supported source for cloud data migration and data validation.
- Added Snowflake-to-Snowflake data validation support.
- Added native multi-database extraction in `scai code extract`.
- Added complexity-band-weighted migration effort estimation to the assessment report.
- Added OAuth token authentication support in legacy mode without requiring a license.
- Added `data orchestrator update` and `data worker update` SPCS commands.
- Added `--database-bindings` support to `scai code deploy`, `scai test seed`, `scai test validate`, and `scai test etl-validate`.
- Added DataStage as a supported ETL source alongside SSIS.

#### Improvements

- Registered Windows-1252 encodings in the SQL code processor on Linux.
- Improved error reporting when a Snowflake session cannot be opened.
- Improved `data doctor` to detect missing deploy privileges per SPCS scenario.
- Installed the IBM DB2 driver in CLI-provisioned data exchange agent workers.
- Added relative tolerance forwarding for data validation configuration.
- Improved client-side bulk load failure reporting to identify the real cause.

#### Bug Fixes

- Fixed handling of SQL Server `GO` batch separators when separated by blank lines from their `USE` statement.
- Fixed numeric YAML scalars being corrupted in workflow configuration.
- Fixed `data-re-validate` to reuse partition metadata on schema failure.

### Desktop App

#### Improvements

- Redesigned the next-steps prompt as an interactive question card.
- Updated the plugin greeting to display the product name.
- Improved telemetry to flush all events before app shutdown or update restarts.

### Conversion Engine

#### New Features

##### Oracle

- Added translation of wrapped and composite `BULK COLLECT` statements.
- Added explicit reporting for unsupported `ALTER TABLE` clauses.
- Corrected `NUMBER` type size argument rounding and added reporting for untranslatable scales.

##### SQL Server

- Folded `DATABASE_PRINCIPAL_ID` existence tests for known literals.
- Rendered self-contained `OPENQUERY` pass-through as a local derived table.
- Assigned database-less objects to the default database during arrange-only conversion.

##### Teradata

- Sized `FORMAT` numeric pictures from a proved type.
- Translated `ANTISELECT` to Snowflake `SELECT * EXCLUDE`.

##### SSIS

- Included Excel Source files in the ingestion manifest.
- Translated fixed-width Flat File Source via `SUBSTR`.
- Bound `ConnectionString` expressions as runtime landing paths.

##### Tableau

- Added SQL Server Tableau workbook repointing to Snowflake, including connection XML, session SQL, Custom SQL relations, `RAWSQL` calculated fields, native calculated fields, and filter structure.

##### DataStage

- Translated horizontal and vertical `PxPivot` to dbt.
- Translated `PxCopy`, `PxAggregator`, `PxLookup`, and `PxRemDup` stages to dbt.
- Translated accumulator and previous-row Transformer stage variables.
- Translated substring and field-extraction bracket access.
- Bound Transformer job-parameter identifiers to dbt vars.
- Added Connector `WriteMode=4` (Update then Insert) UPSERT support.

#### Improvements

##### General

- Carried declared type precision and scale through Migration Project Context symbol serialization.

#### Bug Fixes

##### Oracle

- Lowered supported `EXECUTE IMMEDIATE USING` binds for improved correctness.
- Consolidated read-only UDF lift into one derived-table mechanism.
- Flattened collection `TABLE()` unnest and mapped `DBMS_SQL` built-in collection parameters to `ARRAY`.
- Translated `MULTISET` operators.
- Converted `DBMS_SESSION` no-ops and `SET_NLS` date formats.
- Translated table dictionary views and drop gates.
- Folded definer-rights package owner lookups.
- Preserved count-based existence functions.
- Translated record collection assignments.
- Allowlisted and rewrote `TO_CHAR` format tokens.
- Preserved SQL `NULL` reads in record `BULK COLLECT`.

##### SQL Server

- Fixed `ObjectDependencies` false missing flags when a schema name matches its database name.
- Reordered function parameters and calls when necessary.
- Mapped East Asian Windows collations to Snowflake specifiers.
- Translated static `OBJECT_DEFINITION` to `GET_DDL`.
- Resolved `dbo`-qualified legacy compatibility views through `sys`.
- Fixed parenthesized `SELECT INTO UNION` and `WITH-UPDATE` of a joined alias.
- Emitted inline table-valued function parameters as Snowflake identifiers instead of host binds.
- Renamed `END` locals in SnowScript output.
- Converted parenthesized `SELECT` variable assignments.
- Gated `FORMAT` comma scaling on a proved digit bound.
- Failed closed on `FORMAT` zero-pad tails that scale or lose digits.
- Fixed scope-serialization crashes and legacy T-SQL parse gaps.
- Fixed SSIS connection-manager bleed across packages.

##### Teradata

- Unified `UNPIVOT` value-column types for Snowflake compatibility.

##### DataStage

- Translated DataStage math and numeric functions to Snowflake SQL.
- Forced `WriteMode=4` UPSERT materialization to incremental regardless of `TableAction`.

### Data Validation

#### New Features

- Added L3 signature comparison with Snowflake pushdown for improved validation performance.
- Added native signature extraction for Redshift (`UNLOAD`), SQL Server (BCP and CETAS), PostgreSQL (`COPY`), Azure Synapse (ODBC), BigQuery (DB-API), and IBM DB2 (`cloud_direct`).
- Added IBM DB2 key-inference strategy for data validation.
- Added Teradata data type coverage for data migration and data validation.
- Added PostgreSQL native data validation types.
- Added Oracle two-phase `VECTOR` metadata extraction.
- Added support for arbitrary `columnMappings` in L3 validation.
- Added `primaryKey: ["*"]` support to use all columns as the primary key in DV L3.
- Added `excludeSourceColumns` to exclude specific source columns from data migration.
- Added `CHECKSUM` synchronization strategy for PostgreSQL.
- Added `selectModifier` and `queryModifier` support for BigQuery and Redshift.
- Added Snowflake-to-Snowflake in-warehouse L3 `acceptedTransformations` support.

#### Improvements

- Improved IEEE-754 bit-level float comparison for Teradata, BigQuery, DB2, Oracle, SQL Server, Azure Synapse, PostgreSQL, and Redshift.
- Applied relative tolerance semantics for L2 metrics comparison.
- Improved Teradata view L1 precision via `DBC.ColumnsQV`.
- Improved Teradata logical text comparison across different character sets.
- Mapped Redshift `HLLSKETCH` to `VARCHAR` via `HLL_CARDINALITY` for data migration and data validation.
- Aligned DB2 type mappings across migration and validation to the engine.
- Improved L3 text comparison to follow `RTRIM` semantics instead of full strip.
- Preserved `VARCHAR` whitespace in Snowflake L3 hashes and Redshift L2 distinct counts.
- Preferred Microsoft’s native `mssql-python` driver for SQL Server with ODBC fallback.
- Recognized Teradata DBC integer codes in Iceberg v2-compatible mappings.
- Parsed Oracle `DATE` as ISO NTZ on `COPY INTO`.
- Reduced task contention for concurrent multi-worker access to the task queue.
- Locked `NUMBER(38,10)` when catalog precision is missing.
- Added `DMVF_TASK_KIND` to per-task Snowflake `QUERY_TAG`.

#### Bug Fixes

- Fixed Oracle `SAMPLE` alias ordering in partition queries.
- Fixed DV periodic pipe-refresh polling and dropped eager DEA refresh.
- Fixed query history lag timing before publishing query buckets.
- Fixed SQL Server and Azure Synapse L3 row hash splitting when `CONCAT` exceeds 254 arguments.
- Fixed incorrect watermark expressions.
- Fixed trailing tab preservation when Redshift `RTRIM` matches Snowflake.
- Fixed null Snowpipe drain field preservation.
- Fixed glob-escaping and double-quoting for `PUT` local sources.
- Fixed DM worker upload crash and guarded preprocessing hang.
- Fixed overlapping partition error reporting for both DM and DV.
- Improved DEA doctor TCP reachability probe retry behavior.
- Fixed Redshift DV float vector alignment with source seeding.
- Increased `COPY HISTORY` start time to 14 days prior.
- Fixed BigQuery checksum expression for incremental `CHECKSUM` synchronization.

### Others

#### Migration Plugin

##### New Features

- Added Workload Insights support for SQL Server Extended Events and Query Store data, including an HTML report and assessment dashboard visualization.
- Added BigQuery as a full-migration source in the plugin.
- Added Snowflake-to-Snowflake data validation support in the migration plugin.
- Added Oracle Tableau repointing support in the plugin.
- Added editable effort calculator to both the HTML report and assessment dashboard.
- Enabled git by default on fresh project directories.

##### Improvements

- Added Migration Setup step to the plugin checklist.
- Improved source connection setup to warn against using production databases.

#### Testing Framework

##### New Features

- Added per-code-unit `delta_ignore_columns` overrides.
- Added Redshift source UDF end-to-end coverage for seed, capture, and validate.
- Added MWAA Airflow target executor for ETL validation.
- Added external-command executor for ETL validation.
- Added converted coverage view alongside source view.
- Added canonical AST signature matching for coverage.
- Added connect-first `etl-validate` that fails on connection before discovery.

##### Bug Fixes

- Fixed `NaT`-string crash in datetime/date/time cast.
- Fixed baseline `PUT` glob expansions as paths.

#### Code Unit Registry

##### Bug Fixes

- Fixed C# FFI string argument marshaling to use UTF-8 instead of ANSI.

## Version 2.41.1 (Aug 20, 2026)

### CLI

#### New Features

- Added `--resume-compute-pool` flag for `data orchestrator` and `data worker` commands.
- Added `--renamingfile` support for Druid conversions on the CLI.
- Added `--dbt-repointing` CLI flag for dbt project repointing during conversion.
- Added `--json` and `--yes` support for data orchestrator and worker agent updates.

#### Improvements

- Added a warning when starting a local orchestrator while an SPCS orchestrator is already configured.
- Improved `doctor` command to validate DEW-config Snowflake account connectivity and block start on errors.
- Improved local data migration performance by lowering poll intervals.
- Scoped `data start` doctor checks to `--local` mode and moved grant checks to setup.
- Resolved Snowflake metadata for all assessment commands.
- Added data identity affinity axis to data commands.

#### Bug Fixes

- Fixed DECIMAL key repair to stay within declared precision.
- Fixed `enum_domain` unsolved constraints to gate on branch predicate and join edge relevance.

### Conversion Engine

#### New Features

##### General

- Added Hybrid Table conversion support.
- Added dbt repointing integration into the conversion pipeline with ETL and BI repointing report generation.

##### Druid

- Extended the renaming file format to support table-scoped column mappings.

##### Power BI

- Added pre-scan and validated dependent-connection repointing with renaming bridge for Teradata sources.

##### SQL Server

- Added inlining of certain multi-statement dynamic SQL batches as `BEGIN...END` blocks.

#### Bug Fixes

##### Oracle

- Fixed parsing of `NORMALIZE` as an identifier.
- Fixed parsing of `CONSTRAINT` and `RENAME` as unquoted identifiers.
- Fixed parsing and transformation of `XMLPI(NAME ...)`.
- Fixed parsing of `DIMENSION` as an unquoted identifier in procedures.
- Fixed parsing of indexed collection elements as `BULK COLLECT INTO` targets.
- Fixed chained `PIVOT` parsing where `AsClause` consumed the next `PIVOT`.
- Fixed parsing of newline `/` as division before a parenthesized operand.
- Fixed parsing of `EXTERNAL C` callouts in package procedures.
- Fixed `OverallProcedure` parsing errors.
- Fixed parsing of nested indexed collection method calls like `map(key)(i).EXTEND`.
- Fixed parsing of `MATCH_RECOGNIZE PATTERN` star quantifier and `ALL ROWS PER MATCH`.
- Fixed record-collection `BULK COLLECT` mapping to `ARRAY` of `OBJECT`s with unified dense-collection index handling.
- Fixed demoted-UDF temp variable name qualification.

##### SQL Server

- Fixed `MERGE INTO` with updatable CTE to rewrite to base table reference.
- Fixed `WITH` clause comment-out when only `DATA_COMPRESSION` option remains.
- Added `SSC-EWI-0073` warning for `MEMORY_OPTIMIZED` table option.
- Fixed `sp_executesql` OUTPUT parameter collision producing doubled `INTO` clause.
- Fixed `FORMAT` function conversion for `'0,,'` scale and `'00 - '` zero-pad with literal tail patterns.

##### Tableau

- Fixed identifier casing preservation and statement terminator stripping in Tableau embedded SQL for Oracle sources.

##### Teradata

- Fixed `HybridTableConversionMode` to default to `Standard` when unset.

##### General

- Fixed conversion state isolation by building a fresh task manager per conversion job.

### Data Validation

#### New Features

- Added IBM DB2 platform support for data validation, data migration orchestrator, and data exchange agent.
- Added Iceberg table support for DMVF workflows including Iceberg-aware runtime writers and SPCS environment integration.
- Added Iceberg example workflows and documentation.

#### Improvements

- Improved large table partition boundary analysis by sampling before NTILE computation.
- Added support for snake\_case YAML configuration keys and improved SQL Server index key inference.
- Changed `cleanUpTransientResources` default to `on-success` for improved resource management.
- Added per-table column selection support for L2 metrics.
- Adopted the native `redshift_connector` for Redshift connections in the Data Exchange Agent.

#### Bug Fixes

- Fixed an issue where DV L2 coverage was incorrectly disabled by the metrics exclude-list bug.
- Fixed Oracle data migration and data validation type mapping inconsistencies and aligned DM CREATE with SnowConvert output.
- Fixed an issue where VARCHAR partition keys containing only digits were not reliably used in WHERE clauses for partitioned queries.

### Others

#### Testing Framework

##### New Features

- Added target-side zero-copy-clone isolation for ETL test runs in `scai test`.
- Added source-side backup and restore isolation for the ETL write-set in `scai test etl-validate`, gated on a write-privilege pre-check.
- Added per-side column selection support for test comparisons.
- Added query ID recording for result-set procedure CALL executions.
- Added `SELECT * FROM` emission for table-valued functions in `scai test seed`.

##### Improvements

- Improved test-YAML validation block shape checking at the discovery boundary.
- Improved test seeding to run against the physical target database.
- Improved testing results isolation by separating the results database and rewriting logical names.
- Improved ETL validation to verify Snowflake source tables for non-equivalent validations in `scai test etl-validate`.
- Resolved the source dialect from the SCAI project configuration in the test runner.
- Resolved the DVF comparison source for Teradata and failed declared-but-uncomparable tables.
- Quoted identifiers across the clone isolation chain.
- Re-paired registry `targetName` with its own source parameter.

##### Bug Fixes

- Fixed LOGGER warnings and errors not appearing on stderr for user visibility.

#### Migration Plugin

##### New Features

- Added Dynamic SQL Assessment dashboard with API endpoints and visualization.
- Added Anti-Patterns report to the Assessment dashboard.
- Added Dependencies tab to the Assessment waves view, including overview KPIs, impact tables, and detail modal with export.
- Added data migration and validation strategy capture during the setup phase.

##### Improvements

- Improved DMV infrastructure lifecycle with down guard, readiness gate, and idempotent startup.
- Added session ownership information to object claims.
- Accepted `group` as an alias for `group_id` in `migration_status` tool calls.

##### Bug Fixes

- Fixed SCAI project defaults resolution from the app startup path.
- Fixed spurious `plugin.yml` creation at the current working directory for `dashboard_port`.

#### Code Unit Registry

##### New Features

- Made user-initiated registry renames durable on Windows.

##### Bug Fixes

- Fixed directory sync on Windows skipping `fsync` to prevent registry corruption.

## Version 2.40.1 (Aug 13, 2026)

### CLI

#### New Features

- Added Apache Druid as a code-conversion-only dialect.

#### Improvements

- Scoped DEW worker configuration to the project level and added connection-name template support.
- Added forwarding of `useSnowpipeForResults` from Data Validation workflow configuration to the orchestrator.
- Unified DMVF subprocess logs under `scai logs` for streamlined troubleshooting.
- Added preservation of per-column `COLLATE` settings during Redshift extraction.
- Added `--json` output for per-check results from `scai data-doctor` on check failure.

#### Bug Fixes

- Fixed an issue where `localhost` was not normalized to IPv4 loopback for SQL Server data validation sources.

### Desktop App

#### Improvements

- Updated the Cortex Code migration promotion to reference Snowflake AIM for Data Warehouses preview and link to the request form.

### Conversion Engine

#### New Features

##### Oracle

- Added translation of record-field associative element access via `OBJECT`.
- Added parsing of `$IF`/`$THEN`/`$END` conditional compilation on procedure and function headers.
- Added translation of `SYS_CONTEXT('USERENV','SID')` to `CURRENT_SESSION()`.
- Added translation of dense collection element writes and `EXTEND` to array rebuilds.
- Added translation of collection operations on built-in package types (`DBMS_SQL.VARCHAR2A`, `UTL_HTTP.COOKIE_TABLE`).
- Added support for label-qualified variable references (`label.var`) in Snowflake Scripting output.
- Added translation of dense `coll(i).EXTEND` and deconflicted bare `EXTEND` EWI emission.

##### Power BI

- Added multi-database detection and splicing for Teradata-sourced Power BI repointing.
- Added recognition of bare Teradata base-connection expressions.
- Added recognition of dependent connection references for Teradata sources.

#### Bug Fixes

##### Oracle

- Fixed parsing of `MATCH_RECOGNIZE` for cursor and `SELECT` pass-through.
- Fixed parsing of `RECORD` field `NULL`/`NOT NULL` constraints.
- Fixed parsing of empty `PACKAGE BODY` declarations.
- Fixed handling of `SET TRANSACTION` statements (now removed with `SSC-FDM-0027`).
- Fixed parsing of `XMLELEMENT(NAME ...)` so `FORALL INSERT VALUES` succeeds.
- Fixed handling of `MODEL` clause (now kept with `SSC-EWI-OR0042`).
- Fixed parsing of `FOR UPDATE` before `ORDER BY`.
- Fixed `ALTER TRIGGER` to use `SSC-FDM-OR0084` instead of generic `SSC-EWI-0073`.
- Fixed parsing of collection methods on indexed elements.
- Fixed parsing and transformation of `JSON_OBJECT(AGG)` value form.
- Fixed parsing of function-based and expression `CREATE INDEX` keys.
- Fixed parsing of `XMLELEMENT(EVALNAME)` and added `OR0016` null stub.
- Fixed null-guard for `GetSinglePartitionTarget` when `FromClause.Tables` is null.
- Fixed parsing and wrapping of bare table functions in `FROM` clauses.
- Fixed null-safe `SqlObjectCollector` name resolution.
- Fixed `UPDATE (subquery) SET` crash on select aliases.
- Fixed package-level associative-array element write aborting file generation.
- Fixed parsing of `XMLSERIALIZE(... INDENT)` and mapped to `TO_VARCHAR`.
- Fixed `SSC-EWI-0013` on `DATE + INTERVAL` inside procedures.

##### Teradata

- Fixed `COLLATE`-wrapping of non-character operands in case-sensitivity comparisons.

##### SQL Server

- Improved mining of row-count and `EXISTS` gates as cardinality predicates.

##### General

- Fixed empty scope stack guard in `SymbolResolver.OpenScope`.

### Data Validation

#### New Features

- Added support for geographic and geometry data types in data migration and validation for SQL Server, PostgreSQL, and Teradata.

#### Improvements

- Added a warning for unrecognized `configuration.toml` keys in the data exchange agent.
- Added backward compatibility for IPv4 address handling.
- Added in-warehouse L3 SQL cell fall-through for mismatched keys.
- Added Redshift `TIME` type mapping in Data Validation seed Snowflake DDL.
- Made task-queue batch inserts transactional.
- Added a guard to claim only tables owned by a specific workflow.
- Reconciled PostgreSQL type mappings for `MONEY`, `BIT*`, and `OID`.
- Reconciled Teradata type mappings for `PERIOD`, `XML`, `CLOB`, and `TIMESTAMP WITH TIME ZONE`.

#### Bug Fixes

- Fixed ordinal position warning in schema validation.
- Fixed an issue where partitions with `NULL` boundary values were not handled correctly.
- Fixed an issue where `indexColumnList` was not respecting casing and column renames.

### Others

#### Migration Plugin

##### New Features

- Added anti-patterns assessment API endpoints.
- Added Data Migration & Validation journey page to the Assessment dashboard.
- Added Testing journey content page to the Assessment dashboard.
- Added Object Exclusion Report View with category-based exclusion recommendations.

##### Improvements

- Simplified data migration workflow confirmation prompt labels.

##### Bug Fixes

- Fixed duplicate ETL registry entries by importing at register time instead of convert time.
- Fixed dashboard reporting in-progress tasks as completed.
- Fixed convert dead-end for untyped object types.

#### Testing Framework

##### New Features

- Added a coverage report writer with multiple renderers.

##### Bug Fixes

- Fixed reading of converted ETL orchestration DDL under the `_etl` root so task names resolve correctly.

#### Code Unit Registry

##### New Features

- Made user-initiated registry renames durable on Windows.

##### Bug Fixes

- Fixed directory `fsync` skip on Windows in registry sync operations.

## Version 2.40.0 (Aug 11, 2026)

### CLI

#### New Features

- Added `scai code convert --list-settings` command and `recommend-settings` plugin sub-skill.
- Added `scai data list` command showing connection and database information with affinity filtering.
- Added `scai test etl-validate --pipeline` regex filter for selective ETL pipeline validation.
- Added `scai assessment report` command for migration assessment report generation.
- Added `scai project info` command that reports local config without requiring a Snowflake connection.
- Added worker primitives with local worker `--no-server` mode and SPCS `--service-name` support.
- Added parallelism support for Code Deployment.

#### Improvements

- Shortened DMO and DAE virtual environment paths on Windows to avoid `MAX_PATH` limitations.
- Improved natural-key lookup joins to value-align joins that have no foreign key edge.

#### Bug Fixes

- Fixed an issue where Spectre markup characters in terminal output were not properly escaped.
- Fixed a mismatch between the doctor’s schema validator and DEW config format.

### Conversion Engine

#### New Features

##### Oracle

- Added emulation of cursor `%ISOPEN` as a manual `BOOLEAN` flag instead of emitting SSC-EWI-OR0128.
- Added translation of single-column `BULK COLLECT INTO` a dense collection to `SELECT ARRAY_AGG(col) INTO :arr`.
- Added translation of provably-safe `JSON_TABLE` subset to Snowflake `FLATTEN`.
- Added translation of local associative arrays using the `OBJECT` type.
- Added resolution of unqualified cross-schema object references through unique synonym fallback.
- Added combined OverallProcedure and OverallFunction Assessment CSV output family.

##### SQL Server

- Added routing of `ALTER TABLE` masking policies to `masking_policies.sql`.

##### Teradata

- Added parsing of positional bind parameters (`:1`, `:2`).

##### Druid

- Added registration of Druid query code units in the Code Unit Registry.

##### DataStage

- Added DataStage `.pjb` (ISX PJB) parser frontend for processing DataStage jobs.

##### General

- Added registration of masking policy objects in the Code Unit Registry.

#### Bug Fixes

##### Oracle

- Fixed parsing of schema-qualified sequence `CURRVAL`/`NEXTVAL` so the EWI correctly fires.
- Fixed parsing and marking of `CREATE TABLE` partitioning clauses and DB links.
- Fixed `UNPIVOT IN`-list labels to carry across as identifier aliases.
- Fixed emitting a supported exception code for `RAISE_APPLICATION_ERROR`.
- Fixed routing of record/`%ROWTYPE` field `:= NULL` through `OBJECT_INSERT`.
- Fixed translation of structured UDT assignments through the `OBJECT` pipeline.
- Fixed a `MultiReplace` crash on labeled `OPEN FOR` OUT cursor.
- Fixed parsing of `bool`, `file`, `specific`, `uid`, `empty`, `global`, and `clone` as unquoted identifiers.
- Fixed suppression of SSC-EWI-0094 false positive for loop labels.

##### SQL Server

- Fixed conversion of `FOR XML PATH('') + STUFF` idiom to `LISTAGG`.
- Fixed renaming of scalar SQL UDF parameters that collide with body columns.
- Fixed table-valued parameter and `RETURNS TABLE` identifiers.
- Fixed reformatting of packed date literals compared against date columns.

##### Teradata

- Fixed recognition of SQL Assistant `?NAME` client-side named parameters.
- Fixed removal of `NULL CALL` clause on SQL UDFs with SSC-FDM-TD0059 advisory.

##### Druid

- Fixed emitting the aggregate expression in a native-query `groupBy` `HAVING` clause.

##### SSIS

- Fixed `SanitizeEmptyElements` incorrectly deleting data-carrying elements, which caused packages to be silently dropped.

##### Redshift

- Fixed various conversion issues identified through systematic verification.

##### BigQuery

- Fixed various conversion issues identified through systematic verification.

##### Sybase

- Fixed various conversion issues identified through systematic verification.

##### General

- Improved PK/FK column reference binding to their definition name through the dialect key factory.
- Fixed symmetric PK-to-PK inferred foreign keys to emit at most one canonical direction.
- Fixed various cross-platform conversion issues identified through systematic verification.

### Data Validation

#### New Features

- Added “Cloud-Direct” extraction strategy which writes data files directly to cloud storage services instead of writing to disk first.
- Added Iceberg v2-compatible L1 and L3 profile support for data validation.
- Added Iceberg DEA Parquet packaging with codec support, typed timestamps, and UTC homogenization.
- Added support for geographic and geometry data types for BigQuery data migration and validation.
- Added support for geographic and geometry data types for Redshift data migration and validation.
- Added in-warehouse L3 set-difference gate with multiplicity and `MINUS` support.
- Added Snowflake key inference with inline resolve for in-warehouse data validation.
- Added orchestrator-side L1 schema comparison for the in-warehouse lane.
- Added orchestrator-side L2 metrics comparison for the in-warehouse lane.
- Added in-warehouse validation routing.
- Added support for BigQuery `ARRAY<INT64>` and parameterized `STRUCT` in DMO partition strategy.

#### Improvements

- Improved initial partition sync to fix watermark issues.
- Improved handling of `initialWaterMark` when incremental strategy is switched.
- Improved early failure reporting when `trackModifications=true` is set with Snowpipe as the ingestion mechanism.
- Adjusted parameterization of data types for cases in which tables are created from scratch.
- Improved Teradata incremental source isolation and baseline diagnostics.
- Improved extraction of `OdbcConnectionStringBuilder` across all ODBC dialect configs.
- Clustered `CELL_VALIDATION_RESULTS` and `ROW_VALIDATION_RESULTS` tables for improved query performance.

#### Bug Fixes

- Fixed preservation of zero-valued `ordinal_position` and `scale` in `read_schema_from_stage`.
- Fixed target-only columns now being flagged as L1 schema failures.
- Fixed `NaT` sentinel value replacement with regular `None` before converting to Polars DataFrame.
- Fixed a race condition related to the task chain “Extract schema” to “Determine Partition Strategy”.
- Fixed `Decimal` zero being rendered as scientific notation in the data types harness.
- Fixed “Clear partition” tasks failing with case-insensitive partition keys.
- Fixed cell early-stop combined with AT and Snowpipe DV configuration.
- Fixed a race condition in the `COMPLETE_TASK` definition for complex task chains.

### Others

#### Testing Framework

##### New Features

- Added coverage collector with history fetch for test execution tracking.
- Added support for SQL Server `DATETIMEOFFSET` (ODBC type -155) in baseline capture.
- Added auto-sorting of result sets for order-independent TVF validation.

##### Improvements

- Made `model-config.toml` the source of truth for lane models in `scai test seed`.
- Annotated empty results with `vacuous_match` for clearer test diagnostics.
- Replaced generic error with a descriptive message when validate selects zero tests.
- Improved target database, schema, and task name resolution from the CUR.
- Improved SSIS package folder, project, and store resolution from the source server.
- Improved SQL Server identifier handling by unquoting at the point of use instead of in the seed.
- Improved reporting of unusable row-comparison index keys instead of silently substituting.
- Improved comparison column lists to emit inline.
- Improved validation performance by reusing a persistent target clone in `scai test validate`.

#### Migration Plugin

##### New Features

- Added Assessment & Planning dashboard with Journey Overview and Code and ETL Conversion Overview pages.
- Added assessment evaluation setup guidance and report delivery.
- Added customer and project name to the Assessment report.
- Added `migrateData` and `validateData` batch mode declaration.
- Added conditional setup prompts and one-call answers in the MCP server.
- Added code-conversion-only sources in the setup dialect picker.

##### Improvements

- Improved session start speed with configure returning a status summary and ask-first hook.
- Improved source-connection registration by folding it into `register-code`.
- Improved DEW config delegation to `scai project-default` generation.
- Improved `inScope`/`isMissing` persistence as a top-level flag.
- Improved resume and right-directory detection when no project is found.
- Improved view verification stage derivation from `validateView` instead of `runTests`.
- Improved fallback to a standard `OBJECT_CLAIMS` table when hybrid is unavailable.

##### Bug Fixes

- Fixed `migration_status` sync for git worktrees.
- Fixed `finish`/`isDone` blocking on non-terminal objects.
- Fixed schema-check login failures to frame as connection errors.
- Fixed stale pre-consolidation filenames in ETL stabilization.
- Fixed path traversal in semantic-equivalence-checker report writes.
- Fixed `transition_status(bypass)` constraints.
- Fixed skipped terminal state and `is_done` gate on data phases.

#### Code Unit Registry

##### New Features

- Added durability for user-initiated registry renames on Windows.

##### Bug Fixes

- Fixed directory fsync being skipped on Windows in registry sync.

## Version 2.39.1 (Aug 05, 2026)

### CLI

#### Bug Fixes

- Fixed an issue where the schema name was incorrectly included when generating configurations for Teradata.

### Data Validation

#### New Features

- Added support for `HIERARCHYID` and `ROWVERSION` data types in data validation.
- Added an option to clean up transient resources from internal and external stages after validation.

#### Bug Fixes

- Fixed an issue with Redshift where empty tables caused validation failures.

### Others

#### Testing Framework

##### Improvements

- Improved resolution of Snowflake table identifiers from the Code Unit Registry target side.

#### Migration Plugin

##### Bug Fixes

- Fixed an issue where view validation results were written to an incorrect registry location.
- Fixed an issue where the plugin failed to persist testing status when the testing field was null.

#### Code Unit Registry

##### New Features

- Added support for Druid as a source platform with query object type.
- Added an exclusion field to the Code Unit schema for assessment status tracking.

## Version 2.39.0 (Aug 04, 2026)

### CLI

#### New Features

- Added auto-detection of update channel and `scai versions --remote` to check for newer releases.
- Added support for `private_key_path` alias for Snowflake keypair authentication.
- Added SSIS package support to `scai init` with `object_type=PACKAGE`.
- Added SSIS read-path views for inspecting branches, listing unsolved patterns, and proposing enrichments.
- Added SSIS package clustering via shared source and lookup tables.
- Added SSIS validation semantics to `scai testbed validate`.
- Added SSIS-covering synthetic CSV generation with provenance tracking.
- Added `temporal_window_bindings` enrichment to clamp child dates into matched SCD parent windows.
- Added spec-driven testbed generation for `BINARY`, `UUID`, and `date_key` surrogate key columns.
- Added MERGE/UPSERT natural key correlation between staging tables and targets in `scai testbed generate`.
- Added support for generating DMV workflow files by inferring objects from the source connection.
- Added exclusion findings to the code unit registry via `scai assessment`.

#### Improvements

- Improved Faker value generation in `scai testbed generate` by streaming writes per table for better performance.
- Updated DEW configuration path to the project root.
- Added exact object-name matching to prevent silent sibling extraction during code mining.
- Improved insufficient SPCS privileges detection before deployment.
- Forced cryptography binary wheel installation in migration virtual environments.

#### Bug Fixes

- Fixed `scai deploy` to surface the inner schema-not-found reason behind `CNX0021` connect errors.
- Fixed `scai deploy` to surface the inner Snowflake login error instead of a generic “Unable to connect” message.
- Fixed `ShellProcess` async-read error when falling back from zsh to bash during deployment.
- Fixed testbed generation to never null a declared `NOT NULL` column.
- Fixed testbed generation to prioritize distinctness over branch coverage on single-column keys.

### Conversion Engine

#### New Features

##### General

- Added initial support for IBM DataStage DSX file processing.

##### BigQuery

- Added translation of `IS_NAN` to Snowflake equivalent.
- Added translation of `TO_CODE_POINTS` with JavaScript UDF helpers.

##### Druid

- Added support for `scan` native-query conversion to Snowflake.
- Added support for `postAggregations` in native-query conversion.
- Added support for native-query aggregators beyond basic count and sum/min/max.
- Added support for remaining native-query JSON types (`search`, `timeBoundary`, `segmentMetadata`, `dataSourceMetadata`).

##### Oracle

- Added translation of multi-element `TO_CHAR` datetime formats natively.
- Added translation of `PRAGMA EXCEPTION_INIT` with `SQLERRM()` and actionable EWIs.
- Added translation of `DBMS_STATS.GATHER_TABLE_STATS` as a commented-out no-op.
- Added `WHERE` clause synthesis from single named partition targets.
- Added faithful translation of PL/SQL collection operations and fixed silent mistranslations.
- Added translation of `DBMS_UTILITY.FORMAT_ERROR_BACKTRACE` and `FORMAT_ERROR_STACK` to `SQLERRM`.
- Added translation of `ALTER SESSION` NLS timestamp/time format parameters.
- Added translation of `KEEP (DENSE_RANK FIRST|LAST)` aggregate clause.
- Added translation of scalar `TABLE(collection)` to `FLATTEN` derived table.

##### SQL Server

- Added conversion of `DATEDIFF_BIG` to `DATEDIFF`.
- Added support for N-prefixed `HASHBYTES` algorithm literals.
- Added conversion of `MASKED WITH` columns to Snowflake masking policies.

##### Teradata

- Added translation of `PERIOD` set operators (`P_INTERSECT`, `LDIFF`, `RDIFF`).

#### Improvements

##### General

- Improved deterministic parallel view fill via by-reference `FROM` scopes.

#### Bug Fixes

##### Druid

- Fixed reserved-word metric references in the post-aggregation outer projection to be properly quoted.

##### Oracle

- Fixed `%TYPE` anchor resolution through in-scope synonyms and `CurrentSchema`.
- Fixed multiple conversion defects across Oracle procedures, functions, and expressions.

##### PostgreSQL

- Fixed multiple conversion defects in PostgreSQL-to-Snowflake translation.

##### SQL Server

- Fixed quoting of `DEFAULT` reserved keyword in view column lists.
- Fixed multiple conversion defects in T-SQL-to-Snowflake translation.

##### SSIS

- Fixed multiple defects in SSIS inventory processing.

##### Teradata

- Fixed `OREPLACE` null-handling in Teradata-to-Snowflake conversion.
- Fixed multiple conversion defects in Teradata-to-Snowflake translation.

##### IBM DB2

- Fixed multiple conversion defects in DB2-to-Snowflake translation.

##### General

- Fixed multiple defects in assessment report generation.

### Data Validation

#### New Features

- Added support for Snowflake as a cloud data validation source platform.
- Added rate limiting features for validation workflows.
- Added support for `SDO_GEOMETRY` data type validation.
- Added support for `SDO_GEOMETRY` data type migration.
- Added support for `CHECKSUM` incremental sync for Oracle.
- Added Azure AD authentication modes for SQL Server data validation.
- Added trusted connection and Azure AD authentication modes for Azure Synapse.
- Added raw text comparison mode (text codec) for Redshift and SQL Server.
- Added L3 signature-based validation with control plane, partitioning, and extract handlers.
- Added Iceberg v2-compatible data migration type mapping resolution.
- Added `executionTimeoutMinutes` configuration to data migration workflow schema.

#### Improvements

- Improved error handling to preserve all error messages for each task instead of only the last one.
- Improved Iceberg `create_fresh` pipeline to fail closed with DEA extract path and `postLoadOptimize` support.
- Improved Iceberg `create_fresh` DDL to emit `STORAGE_SERIALIZATION_POLICY`.
- Improved Iceberg `create_fresh` to require storage topology and preflight reachability checks.
- Improved performance by skipping “Automatic Key Inference” tasks when not necessary.
- Improved signature extract charset parity across Redshift, Teradata, and Oracle.

#### Bug Fixes

- Fixed PostgreSQL `TIMETZ` and `TIMESTAMP` columns landing zero rows in Snowflake.
- Fixed Redshift normalization issues during data validation.
- Fixed `DATA_SOURCE_PORT` being incorrectly required in SQL Server connector image.
- Fixed “invalid identifier” error for SQL Server caused by target-case folding.
- Fixed Redshift and BigQuery data validation hang and hybrid validation failures.
- Fixed partition column mapping to target names for NTILE boundary queries.
- Fixed analysis of partition boundaries for SQL Server with composite partition keys.
- Fixed text codec column matching to be case-insensitive across source and target.

### Others

#### Testing Framework

##### New Features

- Added support for seeding hybrid SSIS ETL units as Snowflake task targets in `scai test seed`.

##### Bug Fixes

- Fixed `scai test validate` to use target-side fully-qualified names for isolation DDL.
- Fixed `scai test validate` to set the database context from the project configuration.
- Fixed test comparison to derive its verdict from DVF-level results instead of a never-set output handler.
- Fixed `scai test capture` to fail explicitly when seedable objects match but no test YAMLs are found.
- Fixed SSIS child task resumption in `scai test validate` to use `SHOW TASKS` instead of `SYSTEM$TASK_DEPENDENTS_ENABLE`.

#### Migration Plugin

##### New Features

- Added SQL Server effort estimates to the assessment multi-report.
- Extended assessment effort estimation to Redshift.
- Added data validation monitoring to the migration workflow.
- Added data migration monitoring to the migration workflow.
- Added support for running data validation locally without a compute pool.
- Added ability to reach assessment without a Snowflake target, deferring object-migration setup.

##### Improvements

- Restructured the Assessment report sidebar into a Migration Journey view.
- Improved assessment overview cards to show every object type.
- Improved dashboard startup instructions for clarity.
- Improved the setup prompt to clarify it asks for the target Snowflake connection.
- Improved add-code-locally to present it as one automated step.
- Improved setup-machine routing with done-signals and dialect gating.
- Added fix guides for the three most frequent blocking ETL conversion codes.
- Stored `RULE_ENGINE` in the metadata database instead of the target database.
- Improved reporting to show which table is validating during data validation.
- Configured compute pool `AUTO_SUSPEND_SECS=60` at creation.
- Deferred the target-database prompt to post-assessment.
- Served the dashboard at `/dashboard`.

##### Bug Fixes

- Fixed Unicode encoding errors on Windows consoles.
- Fixed the fixer to stop stubbing unsupported logic to `NULL`.
- Fixed the my-objects summary to return empty when no deploy database is set.
- Fixed git requirement to not require a remote for migrations.
- Fixed progress tracking to stop issuing one call per workflow step.
- Fixed git initialization to create a local repo for embedding hosts.

#### Code Unit Registry

##### New Features

- Added exclusion field to the CodeUnit schema under `codeStatus.assessment`.
- Added Druid source platform and query object type.

## Version 2.38.0 (Jul 29, 2026)

### CLI

#### New Features

- Added `scai data validate --incremental` command for incremental data validation.
- Added Teradata as a supported source for `scai data worker setup`.
- Added `--schema` override to `scai data migrate generate-config`.
- Added ability to create data migration and validation configuration files outside SCAI projects.

#### Improvements

- Dynamic SQL analysis is now enabled by default (removed the experimental `--enable-dynamic-sql-analysis` flag).
- Improved pip virtual environment logging and Teradata connection test feedback.
- Improved console output formatting for data commands.

#### Bug Fixes

- Fixed lowercase PostgreSQL target identifiers causing “Object does not exist” errors.
- Fixed path separator mismatch on Windows when generating configuration output.

### Desktop App

#### Improvements

- Added SQL Server certificate trust forwarding for Windows authentication connections.

### Conversion Engine

#### New Features

##### BigQuery

- Added `CODE_POINTS_TO_STRING` translation to Snowflake.
- Added `SAFE.SUBSTR` translation to Snowflake.

##### Druid

- Added faithful timeseries native-query conversion with support for bucket-only grouping, descending order, grand totals, and complex granularity.
- Added support for non-default dimension specs including extraction, list-filtered, and regex-filtered types.
- Added support for the `groupBy` `having` clause in native-query conversion.
- Added mapping of native-query named granularities to `DATE_TRUNC` and `TIME_SLICE`.

##### Oracle

- Added translation of `CONNECT BY NOCYCLE` to a recursive CTE.
- Added translation of sequence `CURRVAL` via captured `NEXTVAL` value.
- Added translation of `V$TIMER` and actionable EWIs for `ALL_TABLES`, partitions, and scheduler views.
- Added translation of the PL/JSON (`pljson`) library to Snowflake native `VARIANT`.
- Added emulation of the `HTP` and `OWA_UTIL` web toolkit with runtime helper bodies.
- Added translation of `CAST(... AS NUMBER 'L'/'FML')` to `TO_NUMBER`, and collection `TABLE(CAST(...))` to `FLATTEN`.
- Improved cursor semantics with removal of inert `REF CURSOR` type definitions and actionable cursor EWIs.

##### SQL Server

- Added support for recovering `GO`-less SSMS scripts during arrange, with identifier path sanitization.

##### Teradata

- Added translation of derived period columns (`PERIOD FOR`) with DDL drop and reference rewrite.
- Added support for `.LOGON` with `host:port/user` syntax in BTEQ scripts.

##### SSIS

- Added Data Flow translation to Snowflake Scripting for Excel sources, Data Conversion, and unsupported components.

##### Power BI

- Added bridge renaming for function columns that have no existing rename step.

#### Improvements

##### Oracle

- Made the `%TYPE` unresolved EWI (`SSC-EWI-OR0129`) actionable.
- Made the database-link EWI (`SSC-EWI-OR0123`) actionable.
- Removed the unsupported `FOR UPDATE` clause with an EWI, and made `ROWID` and nested-function EWIs actionable.
- Replaced `DBMS_SESSION.SET_IDENTIFIER` calls with `SSC-FDM-OR0067`.
- Added package-specific EWIs for unsupported `UTL_SMTP`, `UTL_TCP`, and `UTL_FILE` usage.
- Added `SSC-EWI-0130` for unqualified missing-object calls in the `SSC-FDM-0007` set.

##### SQL Server

- Single-`RETURN` T-SQL user-defined function bodies are now emitted as plain SQL UDFs.
- Expanded the Windows-to-IANA time zone map to the full CLDR set, with case-sensitive trimming lookup.

##### Druid

- Reserved-word aliases and `ORDER BY` items are now quoted in native-query conversion.

#### Bug Fixes

##### Oracle

- Fixed package call qualification lost under dynamic SQL analysis.
- Fixed spurious `SSC-EWI-0126` and now emits `SSC-FDM-0131` for unparseable dynamic SQL branches.
- Fixed a false-positive EWI for hierarchical `LEVEL` used natively with `PRIOR`, and added an actionable EWI for the row-generator form.

##### SQL Server

- Fixed four inline SQL user-defined function translation defects.

##### General

- Fixed `SSC-EWI-0125` attribution that collapsed the whole-file conversion rate.

### Data Validation

#### New Features

- Added initial implementation of incremental data validation.
- Added base VECTOR data type support for data migration and data validation.
- Added support for customizable normalization expressions in row-hashing validation and cell-by-cell comparison.
- Added support for all INTERVAL data types in Teradata.
- Added INTERVAL data type support for PostgreSQL and BigQuery mixed-precision intervals.
- Added support for additional Teradata authentication options.
- Added support for custom extraction plugins in data migration.
- Added initial Iceberg target configuration support.
- Added data type coverage for Azure Synapse validation.

#### Improvements

- Added BCP support in the Docker image for SQL Server data exchange workflows.
- Expanded VECTOR data type coverage for PostgreSQL and Oracle.
- Added Teradata connectivity support in the unified SPCS image.
- Standardized camelCase as the default format for workflow configuration options, with continued support for snake\_case.
- Added process watchdog to detect and handle unexpected parent process termination.
- Added protection against overlapping data migration workflows on the same table.
- Added source nullability propagation to target table DDL generation.

#### Bug Fixes

- Fixed data validation workflows to work correctly with custom metadata schemas.
- Fixed invalid identifier errors for SQL Server column casing in data validation.
- Fixed Oracle CLOB, NCLOB, and BLOB truncation at 4000 bytes during migration and validation.
- Fixed L3 row-hash false negatives when using pipe as column delimiter.
- Fixed pre-flight disk check to honor the configured local results directory.

### Others

#### Testing Framework

##### New Features

- Added automatic SQL Agent job creation for SSIS testing with support for MSDB-stored packages.
- Added support for capturing and validating Teradata scalar UDFs in `scai test seed`.
- Added AutoSys JIL parser for orchestration lineage analysis.
- Added ETL load pattern identification from CUR for intelligent delta comparison.

##### Improvements

- Task validation now uses the Snowflake task graph root task instead of GUID-based identifiers.
- Improved task validation to hard-fail on un-triggerable Snowflake task DAGs and honor YAML-defined task names.
- Task validation now derives Snowflake task names from authoritative CUR metadata.

##### Bug Fixes

- Fixed result-set comparison by normalizing actual-side column keys to uppercase.
- Fixed revert-key lookup to handle quoted Oracle identifiers correctly in `scai test seed`.
- Fixed `scai test seed` to bind Snowflake CALL arguments by converted name when parameter reordering applies.

#### Migration Plugin

##### New Features

- Added incremental data validation to the plugin experience.
- Added ability to run data migration locally without requiring a compute pool.
- Added deploy-gated ETL seed and validate tasks for SSIS live comparison.

##### Improvements

- Improved migration status performance by batching object ID lookups.
- Improved query registry output by capping and slimming responses.

##### Bug Fixes

- Fixed assessment routing to correctly reflect when an assessment has been run.

## Version 2.37.0 (Jul 21, 2026)

### CLI

#### New Features

- Added `scai revalidate` command for re-running validation on previously converted code.
- Added `scai test` testbed commands (`init`, `mine`, `compile`, `propose-enrichments`, `validate`, and `generate`) for automated test-driven translation workflows.
- Extended anti-patterns assessment to Redshift.
- Added `--local-results-directory` flag to the DEW worker CLI.
- Added BigQuery schema extraction for `code extract`.
- Added Teradata support to InMemory and Toml credentials managers with save error propagation.
- Added support for custom `COMMON` and `TEMP` schema names via environment variable.

#### Improvements

- Improved `scai test etl-validate` to default Snowflake connection and `--platform` from the `scai` project configuration.
- Improved connector reuse for `scai test etl-validate --check-env`.

### Desktop App

#### Improvements

- Improved navigation by routing the assessment card to the Migration Skill page.

### Conversion Engine

#### New Features

##### Oracle

- Added pipelined function to Snowflake SQL UDTF translation (safe subset).
- Added translation of USERENV session/role parameters (`SESSIONID`, `SID`, `ISDBA`).
- Added translation of `SQL%FOUND` / `SQL%NOTFOUND` to Snowflake `SQLFOUND` / `SQLNOTFOUND`.
- Added translation of `DBMS_LOB` write pipeline to a VARCHAR accumulator.
- Added translation of `XMLTABLE` comma-split idiom to a Snowflake table split.
- Added translation of `DBMS_OUTPUT.PUT` / `NEW_LINE` helper UDFs.
- Added support for reserved built-in name `TRANSLATE` as a user-defined function name.
- Added transformation of `V$MYSTAT` SID read to `CURRENT_SESSION()`.
- Added mapping of native JSON object-type API (`JSON_OBJECT_T`, `JSON_ARRAY_T`, `JSON_ELEMENT_T`) to Snowflake VARIANT.
- Added translation of `SQLERRM` and `SQLERRM(SQLCODE)` to Snowflake `SQLERRM`.
- Added translation of `DBMS_STATS.GATHER_TABLE_STATS` as a no-op built-in package.
- Added translation of `htf.formText` to Snowflake string concatenation.

##### BigQuery

- Added mapping of `TRUNC` to Snowflake `TRUNC`.
- Added `DATETIME_ADD` to Snowflake `DATEADD` conversion.
- Added mapping of `TO_BASE64` to Snowflake `BASE64_ENCODE`.

##### Druid

- Added Druid native query JSON ingestion with routing and deterministic JSON-to-SQL conversion.
- Added support for `EXPLAIN PLAN FOR`.
- Added support for `REPLACE INTO` ingestion DML (`OVERWRITE ALL` / `WHERE`).
- Added translation of `AGG(...) FILTER (WHERE p)` to Snowflake.
- Added support for `topN` native-query JSON conversion.

#### Bug Fixes

##### Oracle

- Fixed UROWID size preservation in `ROWID`/`UROWID` data-type mapping.
- Fixed deterministic `%ROWTYPE` conversion.
- Fixed false-positive `SSC-EWI-0108` on compilable correlated scalar-aggregate subqueries.
- Fixed over-flagging `SSC-EWI-OR0008` on valid `TO_CHAR` datetime masks.
- Fixed `SSC-EWI-0073` pending-review marker on the `EVALNAME` node.
- Fixed inline-view `MERGE` target folding into named target.

##### SQL Server

- Fixed reserved keywords used as column identifiers now being properly quoted.
- Fixed subquery-bearing computed columns now routed to workaround view.

### Data Validation

#### New Features

- Added session tagging for SQL Server, Azure Synapse, Oracle, BigQuery, and Teradata to improve query tracing.
- Added support for Oracle’s `BOOLEAN` data type in data migration and validation.
- Added Teradata non-Latin column UTF-8 hex hashing for server-side row validation.
- Added support for the `INTERVAL` data type in data migration and validation.
- Added key inference for Azure Synapse, BigQuery, and SQLite.
- Added BigQuery native driver and connection checks to the data-exchange-agent `doctor` command.
- Added support for overriding orchestrator and Data Exchange Agent logs directory via environment variable.

#### Improvements

- Improved charset-aware normalization in query generators.
- Improved numeric scale and float rendering alignment across source and target.
- Simplified snowpipe drain for data validation.

#### Bug Fixes

- Fixed staged file readability verification before DEA task completion.
- Fixed BigQuery `BIGNUMERIC` handling by casting to `STRING` for Parquet schema inference.

### Others

#### Testing Framework

##### New Features

- Added CUR-only extraction support in the ETL lineage tool for SQL-only projects without XML/DTSX.

##### Improvements

- Improved error visibility and step timing in `scai test seed`.
- Improved per-case error counting in stats.
- Improved parsing of bracketed SQL Server `[schema].[object]` FQNs in delta-capture snapshot SQL.

#### Migration Plugin

##### New Features

- Added retry data validation plugin for resuming failed validation runs.
- Added Data Validation Dashboard UI.
- Added testbed enrichment and orchestration skills for automated test-driven translation.
- Added Snowflake Scripting preview with skip stabilization and deploy support.

##### Bug Fixes

- Fixed setup skipping the non-empty-directory check and directory confirmation.

## Version 2.36.0 (July 15, 2026)

### CLI

#### New Features

- Added anti-pattern detection to the `scai assessment` command for identifying migration risks.
- Added custom schema overrides for data validation with `.env` file support.

#### Improvements

- Made the `user` field optional for OAuth in the Snowflake connection requirements gate.
- Added connectivity probing for the configured Snowflake connection host in the CLI connectivity check.

#### Bug Fixes

- Fixed `scai test seed` crashing on object names with square brackets.

### Desktop App

#### Improvements

- Added persistence of setup-machine configuration before project initialization for session recovery.

### Conversion Engine

#### New Features

##### Oracle

- Added translation of associative-array `COUNT`/`FIRST`/`LAST` collection methods.
- Added translation of the `COLLECT` aggregate function to `ARRAY_AGG`.
- Added translation of `DBMS_LOB.GETLENGTH`/`INSTR` and other built-in package functions.
- Added translation of XML functions to Snowflake equivalents.
- Added translation of `ALL_*` built-in data-dictionary views to `INFORMATION_SCHEMA` equivalents.
- Added translation of `DBMS_UTILITY.GET_TIME` and `DBMS_LOCK.SLEEP`/`SESSION.SLEEP`.
- Added translation of resolvable date arithmetic (date ± number) to `DATEADD`/`DATEDIFF`.

##### Power BI

- Added support for database/schema renaming in embedded SQL in connectors without DDL.

##### Teradata

- Added transformation of `PERIOD` literals (parentheses to brackets, typed literal for time zones).
- Added transformation of the `PERIOD(...)` constructor to `PERIOD_CONSTRUCT`.
- Added transformation of `PERIOD` accessors (`BEGIN`/`END`/`LAST`).

#### Improvements

##### Oracle

- Added `SSC-EWI-0130` for calls to objects missing from the source.
- Simplified `SSC-EWI-OR0036` description by removing the operator placeholder.
- Translated `DBMS_OUTPUT.ENABLE` to an inert no-op (`SSC-FDM-OR0061`).
- Suppressed `SSC-EWI-0073` for `FORALL SUBQUERY` with UNION/CTE cursor queries.

#### Bug Fixes

##### BigQuery

- Fixed `BIT_COUNT` mapping to `BITCOUNT` and reordered 2-arg `LOG` arguments.
- Suppressed Python UDF `container_*` OPTIONS from `SSC-EWI-0016`.

##### Oracle

- Fixed parsing of `MOD` as an infix operator in PL/SQL.
- Fixed parsing of double db-link references in calls.
- Fixed parsing of reserved words `AUDIT`, `COPY`, and `TRAN` as identifiers.

##### SQL Server

- Fixed parsing of `INLINE` and other non-reserved keywords as identifiers.

### Data Validation

#### New Features

- Added BigQuery support to the Data Exchange Agent and Data Migration Orchestrator for cloud data validation (L1/L2/L3).
- Added automatic primary key inference for SQL Server, PostgreSQL, Oracle, Teradata, and Redshift.
- Added support for using system columns and pseudo-columns as watermark columns for incremental synchronization.
- Added support for tracking deletions with the `WATERMARK` strategy for incremental synchronization.
- Added Oracle thick-mode support to the Data Exchange Agent.
- Added row-validation KPI tiles for mismatch categories.
- Added Redshift data type coverage for data migration and data validation.

#### Improvements

- Improved data validation reliability with an automatic retry mechanism.
- Improved connection handling with connection reuse and ODBC diagnostics in the `scai data doctor` command.
- Improved numeric precision with scale-aware canonical rendering for Oracle, Teradata, Redshift, and PostgreSQL.
- Improved orchestrator reliability by waiting for task and database readiness before proceeding.

#### Bug Fixes

- Fixed BigQuery data validation seed handling for `TIMESTAMP` literals with spaced offsets.
- Fixed Snowflake mirror schema not being created for BigQuery data validation.
- Fixed row-validation KPI lookup failing with a `KeyError`.

### Others

#### Testing Framework

##### Improvements

- Made infrastructure errors fatal at the CLI level for early failure detection.
- Added surfacing of baseline-load failures with detailed load statistics.

## Version 2.35.0 (July 9, 2026)

### CLI

#### New Features

- Added persistence of conversion settings per project in `code-conversion-config.yaml`, allowing settings to be reused across sessions.
- Added the `scai validate-workflow-config` command to validate migration workflow configuration files against orchestrator schemas.

#### Improvements

- Improved data-command Python environment setup with centralized, parallelized initialization for faster startup.
- Added automatic SSIS ETL file arrangement during `scai code add` and `scai init` commands.
- Added live progress display while `scai data doctor` runs.
- Promoted converted ETL output to `snowflake/_etl` after conversion for improved project organization.
- Updated the Data Egress Wizard to configure source connection egress settings.

#### Bug Fixes

- Fixed code extraction for SQL Server to use `FOR XML PATH` aggregation for correct code unit extraction.
- Fixed the orchestrator schema-readiness poll to target the correct `COMMON` tracker.

### Conversion Engine

#### New Features

##### BigQuery

- Added support for parsing and translating `CAST` and `SAFE_CAST` expressions with a `FORMAT` pattern argument.
- Added support for the `TIMESTAMP_TRUNC` function with a third timezone argument.

##### Druid

- Added support for common table expressions (`WITH` clauses).

##### Oracle

- Added translation of `DBMS_UTILITY.GET_TIME` to `DATE_PART(EPOCH_MILLISECOND, ...) / 10`.

##### Teradata

- Added conversion of BTEQ `.GOTO` and `.LABEL` directives to a `LOOP` + `SC_LABEL` state machine for Snowflake scripting.

#### Improvements

##### BigQuery

- Suppressed redundant `SSC-EWI-0016` Error Warning Information (EWI) messages on Python UDF options.

##### SQL Server

- Inlined `DATENAME(MONTH)` and `DATENAME(WEEKDAY)` to native Snowflake built-in functions, eliminating `SSC-EWI-0021` EWI messages.
- Added `CREATE LOGIN` and `ALTER LOGIN` statements to the list of out-of-scope code units.

##### General

- Changed table comment output to use `ALTER TABLE ... SET COMMENT` instead of `COMMENT ON TABLE` for Iceberg compatibility.
- Narrowed `SSC-EWI-0108` to exclude compilable correlated scalar-aggregate subqueries, reducing false-positive EWI messages.

#### Bug Fixes

##### BigQuery

- Fixed parsing of `PARTITION BY` and `CLUSTER BY` clauses appearing before `AS SELECT` in `CREATE TABLE AS SELECT` statements.

### Data Validation

#### New Features

- Added Azure Synapse support to the Data Exchange Agent unified worker Docker entrypoint.
- Added BigQuery Docker entrypoint support to the Data Exchange Agent with credential handling and a configuration template.
- Added a charset normalization foundation for cross-database encoding consistency during data migration.
- Added a wall-clock execution timeout to Analyze Boundaries tasks to prevent runaway processes.
- Added support for custom checksum expressions in incremental synchronization using the `CHECKSUM` strategy.
- Added the `validate-workflow-config` orchestrator command for validating migration workflow configuration files.

#### Improvements

- Improved L2/L3 canonical rendering for scale-aware numeric, full-precision float, boolean, and binary values for T-SQL and Snowflake targets.
- Added L3 Data Exchange Agent support for SQL Server and Azure Synapse query modifiers.
- Added Data Exchange Agent support for stripping Teradata `LOCKING ... FOR ACCESS` modifiers before SQL command classification.
- Clarified source/target `WHERE` clause pairing in data validation with `sourceWhereClause` semantics and unpaired-entry warnings.
- Improved Orchestrator Table Task Queue stability.

#### Bug Fixes

- Fixed Data Exchange Agent container startup by writing configuration files under `$HOME` to ensure the app user has write access when running on SPCS.
- Fixed an issue where the SCAI logger failed to start because the app user did not have a writable `HOME` directory on SPCS.
- Fixed zero-row migration for Oracle `NUMBER` columns with decimal scale by fetching fixed-point values as `Decimal`.
- Fixed Teradata L3 row-hash computation in the Data Exchange Agent.

### Others

#### Testing Framework

##### New Features

- Added support for user-defined BTEQ binding grammars (`@PARAM@` and `<param>` patterns) in `scai test seed`.
- Added detection and prevention of destructive operations (DDL statements and nested commits) during stored procedure testing and validation.
- Added the `scai test lineage` command for ETL pipeline lineage analysis.

##### Improvements

- Added T-SQL source node alignment to converted Snowflake output for test coverage tracking.
- Improved BTEQ testing determinism with enhanced diagnostic validation, connection handling, and missing-BTEQ guidance.
- Renamed lineage report sections from “waves” to “steps” in the lineage generator and `--use-lineage` consumer.
- Added helper methods to the case validator for more expressive test assertions.

##### Bug Fixes

- Fixed the result-set comparator to surface exceptions instead of silently discarding them.

#### Migration Plugin

##### New Features

- Added a Data Migration Dashboard UI for monitoring migration progress.
- Added ETL deployment support in the plugin with agent guidance and deploy tooling.

##### Improvements

- Added support for disabling prompt nodes in project profiles.
- Added the `SCAI_PROJECT_DIR` environment variable for configuring the SCAI project directory at startup.
- Added BTEQ script routing through the plugin test flow.
- Updated the Migration Dashboard UI with style improvements.
- Passed the session `project_dir` as the SCAI working directory for global plugin commands.

##### Bug Fixes

- Fixed setup-task skip behavior to correctly persist state and route task status.

## Version 2.34.1 (July 2, 2026)

### CLI

#### New Features

- Added ETL code deployment support (deployment gate, Snowflake CLI executor, orchestrator, and write-back).

#### Improvements

- Improved `scai data doctor` performance with a fail-fast source probe, a reused orchestrator connection, and by skipping the pip upgrade.
- Removed the deprecated `scai data migrate-legacy`, `validate-legacy`, and `diagnostics` commands.
- Improved the data validation status report.

#### Bug Fixes

- Fixed `scai data` to honor an existing Data Exchange config and the project `source_connection`, and standardized doctor config-path resolution.
- Fixed `scai data doctor` to scope the Snowflake grants section to the detected flow.

### Conversion Engine

#### New Features

##### General

- Added parser support for the modulo operator (`%`) via a shared ANSI node.
- Added parser support for `CREATE MASKING POLICY` and `ALTER TABLE ... SET MASKING POLICY`.

##### BigQuery

- Added support for `CREATE FUNCTION LANGUAGE python` with `SSC-EWI-BQ0029`.
- Added `SSC-EWI-BQ0032` for `REMOTE WITH CONNECTION` functions.
- Added parsing of `CREATE AGGREGATE FUNCTION`, flagged with `SSC-EWI-BQ0030`.
- Added a `DROP TABLE FUNCTION` parser, translation, and Error Warning Information (EWI).
- Rewrote the `TABLE<...>` function parameter to `TABLE(...)` with `SSC-EWI-BQ0031`.
- Added translation of `INSTR` to `POSITION` / `REGEXP_INSTR`.
- Added mapping of `SAFE.PARSE_JSON` to `TRY_PARSE_JSON`.

##### Druid

- Added translation of JSON and nested-data functions to Snowflake.
- Added translation of array functions and `UNNEST` to Snowflake.
- Added translation of built-in string and scalar functions to Snowflake.
- Added translation of numeric and math functions to Snowflake.
- Added translation of date/time built-in functions to Snowflake.
- Added translation of multi-value string (`MV_*`) functions to Snowflake.
- Added coverage for `COALESCE`, `NVL`, `NULLIF`, and `IFNULL` conditional and null-handling translation.
- Flagged `LOOKUP` with `SSC-EWI-DR0002` (no Snowflake equivalent).

##### Oracle

- Added translation of non-parametrized package cursor `FOR...IN` loops to the `RESULTSET` pattern.
- Added translation of parametrized package-level cursor `FOR...IN` loops to the `RESULTSET` pattern.
- Added translation of package-level cursor `OPEN`/`FETCH`/`CLOSE` to `PACKAGE_CURSOR` helper calls.
- Added translation of unqualified package cursor `OPEN`/`FETCH`/`CLOSE` to `PACKAGE_CURSOR` helpers.
- Added translation of parametrized package-level cursor declarations to a `PACKAGE_CURSOR` registry.
- Added translation of parametrized package-level cursor `OPEN` to `OBJECT_CONSTRUCT`.
- Added parser support allowing `EQUALS` as a function-call name.

##### Teradata

- Added recognition of `@param@` BTEQ bindings.

#### Improvements

##### SQL Server

- Emit explicit `NULLS FIRST` / `NULLS LAST` on window-function `ORDER BY`.

##### Teradata

- Use native `LIKE ANY` / `ILIKE ANY` instead of `OR` expansion.

##### General

- Route generated columns with non-deterministic datetime registers to a view workaround.

#### Bug Fixes

##### BigQuery

- Accept hyphenated project ids in `CREATE SCHEMA`, `UPDATE`, and `MERGE` targets.

##### SQL Server

- Mapped `INFORMATION_SCHEMA.COLUMNS` identity to clear a false-positive `SSC-EWI-TS0046`.
- Commented out `SET TRANSACTION ISOLATION LEVEL` with `SSC-FDM-TS0073`.

##### General

- Bounded dynamic-SQL resolution size and merge-branch count to fix out-of-memory and overflow errors.
- Preserved NULL-for-empty-group semantics using `NULLIF(LISTAGG(...), '')` for BigQuery, Teradata, and Sybase.

### Data Validation

#### New Features

- Added SQLite as a source platform for data validation.
- Added a unified objects section with runtime type detection for cloud data validation.
- Added a query-modifiers foundation (resolver, Data Exchange Agent config, scan registry, and validation templates).
- Added a configurable text comparison mode (defaulting to logical comparison).
- Added timestamp timezone preservation for Azure Synapse data validation.
- Added a BigQuery `EXPORT DATA` handler to the Data Exchange Agent for cloud extraction.

#### Improvements

- Improved timestamp normalization for Teradata data validation.
- The Data Exchange Agent no longer refreshes the stage after upload for data-extraction tasks.

#### Bug Fixes

- Fixed the Snowpipe drain wait so ingestion completes before the validation task finishes.
- Fixed migration of Oracle `NUMBER`, `BLOB`, `LONG`, `LONG RAW`, and `XMLTYPE` columns that were landing zero rows.
- Fixed BigQuery cloud-extraction type and timestamp correctness in the Data Migration Orchestrator.
- Fixed handling of a missing `database` attribute on the Data Exchange Agent connection config.
- Fixed SQL Server data migration using BCP and Snowpipe.
- Fixed row-hash early-stop and empty-source handling in data validation.
- Fixed table preprocessing to halt on collapsed partition slices.

### Others

#### Testing Framework

##### New Features

- Added an SSIS DTSX lineage extractor to the testing framework.
- Added lineage diff and gap validation on top of lineage extraction.
- Added three-part fully-qualified names for Oracle package members in `scai test seed`.
- Added wave-ordered execution via `--use-lineage` to `scai etl-validate`.
- Added doctor findings output to `scai test doctor --json`.

##### Improvements

- Improved BTEQ binding and fixture-input resolution from the shell wrapper.
- Eliminated duplicate `CREATE FILE FORMAT` statements per batch-load pair during capture.

##### Bug Fixes

- Fixed `scai etl-validate` silently skipping SSIS/ETL parts converted to stored procedures.
- Fixed baseline capture so glob metacharacters in the baseline PUT source are escaped.

#### Migration Plugin

##### New Features

- Added a step to edit configuration files during migration.
- Added Oracle package-member guidance to the migrate-objects skills.
- Added reporting for data migration and data validation error results.
- Added canonical workloads (RedShift, SQL Server) and source-deployment skills.

##### Improvements

- Added troubleshooting guidance for workflows that finish with pending tables.
- Snowflake identifiers are now quoted only when necessary.
- Integrated `scai data doctor` into the data migration and validation skills.
- The plugin now honors `snowflake_database` and `snowflake_warehouse` project defaults in the MCP session.
- Self-heal the MCP worker connection on session expiry.

##### Bug Fixes

- Fixed ETL code units not being claimed before stabilization.

## Version 2.33.0 (June 24, 2026)

### CLI

#### New Features

- Added the `--analyze-partition-keys` flag to the data doctor.
- Added an unsupported-language gate to the data migration/validation (DMV) commands.

#### Improvements

- Stopped emitting `earlyStopping` in generated data validation configs.

### Conversion Engine

#### New Features

##### BigQuery

- Added translation of quantified `LIKE` (`ANY`/`SOME`/`ALL`) and an Error Warning Information (EWI) for non-literal `UNNEST` arrays.
- Added translation of `RAND()` to `UNIFORM(0::FLOAT, 1::FLOAT, RANDOM())`.
- Added `SSC-EWI-BQ0021` for `MERGE ... WHEN NOT MATCHED BY SOURCE`.
- Added translation of `DIV(x, y)` to `TRUNC(x / y)`.
- Added translation of `DATETIME_SUB` to `DATEADD` with a negated count and `TIMESTAMP_NTZ` cast.
- Added translation of `ST_INTERSECTS`, `ST_CONTAINS`, and `ST_ASGEOJSON`.
- Added `SSC-EWI-BQ0027` for cursor row-fields in `FOR` loop bodies.

##### Oracle

- Added a `PACKAGE_CURSOR` helper schema for Oracle package cursor simulation.
- Added translation of non-parametrized package cursor definitions to the `PACKAGE_CURSOR` registry.

##### Power BI

- Added multi-database parameter generation.

##### SSIS

- Added lineage enrichment wired through parse-and-assess.

##### General

- Added an IBM DataStage DSX AST and parser, plus an initial DataStage BASIC expression parser.
- Added parser support for the Snowflake stage/load flow (`CREATE STAGE`, `PUT`, `COPY INTO`, `EXECUTE IMMEDIATE`).
- Added parser support for `ERROR_TABLE(<table>)` as a `FROM` source.
- Added parser support for `CREATE [OR REPLACE] ICEBERG TABLE` with table-level properties.
- Added translation of Druid aggregate functions (including `EARLIEST`/`LATEST`).

#### Bug Fixes

##### BigQuery

- Fixed `CURRENT_DATE(tz)` translation to use `TO_DATE(CONVERT_TIMEZONE(...))`.
- Fixed nested-`STRUCT` Functional Difference Message (FDM) field-text garbling and verified `STRUCT` type-declaration conversion.

##### Oracle

- Improved package-constant resolution to source from the live AST.

##### SQL Server

- Fixed `EXEC` argument parsing that swallowed a following `MERGE` statement.
- Mapped `sys.objects.schema_id` to `OBJECT_SCHEMA`.
- Mapped `INFORMATION_SCHEMA.TABLES` system columns 1:1 to stop false-positive EWIs.
- Sanitized embedded newlines in arranged file names.
- Routed computed columns with subqueries to a compensating view.

##### Teradata

- Fixed a crash on `TIMESTAMP_NTZ` cast and interval-without-qualifier.

##### General

- Sized decimal-arithmetic computed columns to Snowflake `NUMBER(p,s)`.
- Repointed workaround-view references in `CREATE VIEW` bodies, `UPDATE...FROM`, and `MERGE...USING`.
- Fixed weekday `DATEPART` replacement ordering relative to the SnowScript UDF body rewrite.

### Data Validation

#### New Features

- Added BigQuery as a source platform in the migration orchestrator.
- Added support for specifying `projectName` and `datasetName` on BigQuery sources.
- Added a BigQuery driver for regular extraction in the Data Exchange Agent.
- Added Oracle ISO timestamp normalization for migration and validation.
- Added ISO 8601 timestamp timezone preservation for Teradata migration and validation.
- Added ISO 8601 timestamp timezone preservation for SQL Server migration and validation.
- Added support for accepted transformations (V1) in data validation.
- Added an identifier case-sensitivity policy with case-sensitive Snowflake target handling.

#### Improvements

- Improved the partition mechanism for L2/L3 data validation.
- Replaced `TRIM` with `RTRIM` in L2/L3 validation query templates.
- Hardened the Data Exchange Agent worker idle shutdown with a pre-exit safety gate.

#### Bug Fixes

- Fixed SQL Server datetime normalization for L2/L3 data validation.
- Fixed Oracle `DATE`/`TIMESTAMP` normalization to match Snowflake ISO FF9.
- Aligned PostgreSQL `BYTEA` normalization with the Snowflake `BINARY` `0x` prefix.
- Aligned Oracle `RAW`/`BLOB` normalization with the Snowflake `BINARY` `0x` prefix.
- Fixed Oracle type mapping and `COPY INTO` timestamp loading.
- Fixed data validation result uploads on Windows by normalizing local file paths for the Snowflake `PUT` command.
- Added a fail-fast check on Redshift when the worker database does not match the task database.

### Others

#### Testing Framework

##### New Features

- Added an ETL validate command with dbt Cloud support.
- Added Oracle `TableStep` support in `scai test seed`.

##### Improvements

- Added restoration of dropped tables in capture isolation.
- Enriched test validation terminal output with per-column failure details.
- Added asyncio support for the test pollers.

##### Bug Fixes

- Fixed Windows compatibility and validation output display issues.

#### Migration Plugin

##### New Features

- Added a lineage gap analysis tool.
- Added a SQL Server ODBC driver pre-flight check to the worker local setup.
- Added blocking and escalation on unresolvable deploy error codes.

##### Improvements

- Replaced SSIS-specific terminology and field names with platform-agnostic names across ETL stabilization.
- Stamped the registry as running when async migration/validation jobs start.

##### Bug Fixes

- Fixed `enableDashboard` advancing setup when the dashboard bind fails.

#### Code Unit Registry

##### New Features

- Added support for root-level dependencies and issues on ETL code units.

##### Bug Fixes

- Extended self-dependency exclusion to part-origin edges.

## Version 2.31.0 (June 10, 2026)

### CLI

#### New Features

- Added `scai connection add-azure-synapse` command for connecting to Azure Synapse Analytics.

#### Improvements

- Added `-d`/`--database` flag to the `data generate-config` command.
- Updated the default `RowValidationMode` to `Hybrid`.
- Added BigQuery connection support to the CLI.
- Improved `scai doctor` to auto-detect configuration type when `--config` is passed.
- Added schema filter with wildcard support to the non-interactive migration flow.
- Made the `user` field optional for OAuth Snowflake connections.
- Improved `scai doctor` partition probe performance by collapsing to a single-pass query.
- Relaxed `scai init` to allow initialization in directories that already contain a `.scai` directory.
- Added bundled Python library versions to `scai --version` output.
- Updated `validation_database` to be sourced from configuration only, with an explicit error when missing.
- Aligned data migration YAML validation output format.

#### Bug Fixes

- Fixed `snowflake_database_for_metadata` not being passed to the DEW configuration.
- Fixed a DVF version conflict.
- Fixed `scai configure` (MCP) bypassing the configure hint when `project_dir` is unset.

### Desktop App

#### New Features

- Added Azure Synapse Analytics as a supported source platform with three authentication methods.
- Added Azure Synapse external objects extraction support (External Tables, Data Sources, and File Formats).
- Added BigQuery code extraction support.
- Added PostgreSQL as a supported source in the migrations plugin.
- Added Redshift as a supported source deployment platform in the migration plugin.
- Added Oracle cloud data migration and validation support in the migration plugin.
- Added Teradata cloud data migration and validation support in the migration plugin.
- Added support for custom skills.

#### Improvements

- Added Azure Synapse database operations and extraction queries.
- Added task preconditions with the ability to complete, skip, or exclude individual tasks.
- Improved Snowpark worker reliability with auto-respawn and retry exhaustion signaling.
- Reduced token usage in MCP tool results.

#### Bug Fixes

- Fixed a `TABLE_PROGRESS` view column name mismatch in data validation.
- Fixed duplicated code extraction — duplicate files are now skipped or overwritten based on configuration.
- Fixed an ETL double-copy issue in the SQL handler legacy path.
- Fixed a Snowpark worker panic when the target database does not exist.
- Fixed an invalid `OVERRIDE GENERATED ALWAYS` clause in Teradata restore SQL (Error 3707).

### Conversion Engine

#### New Features

##### BigQuery

- Added Error Warning Information (EWI) emission for unconvertible pseudo-columns `_TABLE_SUFFIX`, `_PARTITIONDATE`, and `_PARTITIONTIME`.
- Added `REGEXP_INSTR` replacer with RE2/POSIX flavor handling.
- Added translation of `TIME_SUB` to `DATEADD` with negated count.
- Added translation of `TIME_ADD` to `DATEADD`.
- Added translation of `TIME_DIFF` to `DATEDIFF` with swapped arguments.

#### Bug Fixes

##### General

- Fixed parsing of `EXECUTE IMMEDIATE $$...$$` scripting blocks whose body starts with a comment.

### Others

#### Testing Framework

##### New Features

- Added `scai test doctor` command for diagnosing testing environment readiness.
- Added support for capturing and validating Teradata BTEQ shell-variable bindings in test-seed, capture, and validate workflows.
- Added SSIS end-to-end orchestrator support.

##### Improvements

- Improved per-case glyph display and per-shape totals in capture and validate output.

#### Data Validation

##### New Features

- Added normalized cell validation and row hashing support for SQL Server.
- Added BigQuery source type and object-type query support.

##### Improvements

- Made the `COPY` extraction strategy the default for PostgreSQL.

## Version 2.30.0 (June 2, 2026)

### CLI

#### New Features

- Added a dbt Cloud target executor to orchestrate dbt Cloud runs from the CLI.
- Added Redshift as a supported source for source-target deployment.
- Added PostgreSQL commands and configuration to the CLI migration pipeline.
- Added Azure Synapse as a recognized source dialect for migrations.
- Added partition-key feasibility checks for Hybrid Tables to `scai data doctor`.

#### Improvements

- Refactored the `scai data doctor` experience for clearer prompts and output.
- Made the MCP allowlist case-insensitive when matching tool names.
- Reduced memory growth on long-running migrations by closing resource leaks in the DMV layer.
- Added the `CUSTOM_SNOWCONVERT_DATABASE` environment variable to select a custom internal SnowConvert database.
- Tightened partition-key feasibility thresholds in `scai data doctor` for more accurate recommendations.
- Expanded the `by_type` output of `migration_status(mode="summary")` to support richer reporting.
- Propagated proxy settings to all internal HTTP clients so outbound requests honor configured proxies end-to-end.

#### Bug Fixes

- `scai data validate` and `scai data migrate status` now honor the project’s default connection.
- Fixed a crash when the working directory is deleted while the CLI is running.
- Added an integrity check that detects truncated `pip install` artifacts and fails fast with a clear error message.

### Desktop App

#### New Features

- Added per-object detail views in the assessment report.
- Added detail views for stage objects in the assessment report.

#### Improvements

- Restyled the missing-object report for improved readability.
- Switched task labels to be server-controlled for consistent naming across versions.
- Added an environment variable to skip the dashboard build for faster iteration.
- Removed `compute_pool` enforcement when running DMV locally.

#### Bug Fixes

- Restored sections that were missing from the comprehensive assessment report.

### Conversion Engine

#### New Features

##### BigQuery

- Translated `GENERATE_UUID` to Snowflake `UUID_STRING`.
- Translated `PARSE_JSON` and stripped the `wide_number_mode` argument when present.
- Translated `UNICODE` as a pass-through to Snowflake.
- Translated `DATE_DIFF` with date-part support.
- Translated `PARSE_DATE` to Snowflake `TO_DATE`.
- Translated `PARSE_DATETIME` to Snowflake `TO_TIMESTAMP_NTZ`.
- Translated the `DATETIME` constructor to `TIMESTAMP_NTZ_FROM_PARTS`.
- Translated `FORMAT_TIMESTAMP` to Snowflake `TO_CHAR`.
- Translated `FORMAT_TIME` to Snowflake `TO_CHAR`.
- Translated `ERROR()` to a Snowflake user-defined function named `ERROR_UDF`.
- Translated `DATE_SUB` to Snowflake `DATEADD`.
- Translated `PIVOT` as a pass-through and added a Functional Differences Mapping (FDM) annotation.
- Dropped the `use_spheroid` argument from `ST_DISTANCE` translations.
- Reordered the arguments in `DATE_TRUNC` translations to match Snowflake semantics.

##### SQL Server

- Promoted format-specifier translation to general availability and removed the `--EnableFormatSpecifiersPreview` flag.
- Translated `RENAME OBJECT` to `ALTER TABLE ... RENAME TO`.

##### Teradata

- Added support for the `NAMED` keyword as a synonym for `AS`.
- Added support for BTEQ script bindings that use bash variables.
- Added support for `@variableName@` external-substitution placeholders in BTEQ scripts.

##### Power BI

- Added schema-renaming support through the `Schemas` section of the `--RenamingFile` mapping.

#### Improvements

##### Teradata

- Commented out the `UPPERCASE` column attribute and wrapped `INSERT` values for the affected columns in `UPPER()` to preserve behavior.

#### Bug Fixes

##### BigQuery

- Fixed the off-by-one offset in `EXTRACT(DAYOFWEEK)` translations.
- Fixed `EXTRACT(ISOWEEK)` translation to emit `EXTRACT(WEEKISO)` so ISO week numbers match.

##### Oracle

- Fixed a null Code Unit Registry target after running `code convert` on Oracle sources.

##### SQL Server

- Suppressed a spurious EWI raised on reserved column names when running with the Transact dialect.

##### Teradata

- Fixed `FOR`-loop body parenthesization when the body contains a query followed by a set operator.
- Suppressed the EWI emitted on `.OS rm` statements that precede a `.EXPORT FILE`.

##### Power BI

- Fixed duplicate column renaming in Power BI repointing.

##### General

- Updated the Snowflake parser to accept a derived column list on parenthesized table references.
- Fixed broken documentation links for `SSC-EWI-0121`, `SSC-EWI-TS0015`, and 17 other category and dialect mismatches.

### Others

#### Testing Framework

##### New Features

- Added support for capturing and validating user-provided Teradata macros.
- Added two-pass capture support for Teradata in `scai test seed`.
- Added support for capturing and validating stored procedures with `INOUT` and `OUT` parameters.
- Added support for capturing and validating Teradata `PERIOD` columns.
- Added support for capturing and validating Teradata `SET` tables.
- Added capture and validation support for SQL Server `OUT` parameters.
- Added a Snowflake Task DAG validator to the testing harness.

##### Improvements

- Improved baseline storage and replay performance for long-running capture suites.
- Improved the diffing strategy for result-set comparisons.
- Improved the parallel executor for capture and validation runs.

##### Bug Fixes

- Fixed snapshot-mode side-effects validation when targets reference shared state.
- Fixed delta-capture comparator behavior on truncated baselines.
- Fixed `scai test capture` baseline cleanup when `--keep-baselines` is set.

#### Data Validation

##### New Features

- Added ODBC data migration support for Azure Synapse serverless SQL pools.

##### Improvements

- Added an L3 row-validation safeguard for cases where the target table’s column list does not match the source.

##### Bug Fixes

- Fixed identifier quoting so that uppercase identifiers stay unquoted, while lowercase and mixed-case identifiers are auto-quoted.

## Version 2.29.0 (May 28, 2026)

### CLI

#### New Features

- Added the `scai versions` command with `list` and `remove` subcommands for managing installed CLI versions.
- Added the `scai data doctor` command (Phase 1) for running local system checks and surfacing recommendations.
- Added Oracle as a supported source for cloud Data Migration in the CLI.
- Added Oracle as a supported source for Data Validation in the CLI.
- Added Teradata as a supported source for cloud Data Migration and Data Validation in the CLI.
- Added Azure Synapse as a first-class dialect for `scai code convert`.
- Promoted PostgreSQL to the full migration pipeline.
- Added Data Validation results CSV reports.
- Added SQL Server source-target deploy support.
- Added RedShift source-deploy support with identifier consolidation.

#### Improvements

- Hid the legacy `results/` folder at project initialization and redirected `legacy-validate` output to the standard location.
- Added an override confirmation prompt in DMV when generating a workflow file that already exists.
- Enhanced Data Validation configuration handling.
- Deprecated Snowpark-based validation in favor of the unified Data Validation pipeline.
- Consolidated test seeding under `scai test seed`, replacing the standalone `Snowflake.SnowConvert.Testing.Seed.Cli` binary.
- Upgraded the DMV orchestrator and worker versions.

#### Bug Fixes

- Fixed the percentage calculation reported during code deployment.
- Surfaced the Snowflake driver `errno` and `sqlstate` on the .NET banner and fixed a Python 3.10 incompatibility in the validator zip.
- Fixed the `-y` and `--json` flag interaction in `scai data worker generate-config`.
- Forwarded SQL Server connection parameters to the data worker.
- Fixed object-error display on Data Validation cloud results.
- Validated that procedure paths honor `isolation_strategy` with automatic fallback.

### Desktop App

#### New Features

- Added a status dashboard for migration progress.

#### Improvements

- Made the Dashboard the default landing view after the first visit.
- Recommended the safe-tool allowlist as an opt-in setup step.
- Updated the migration agent’s `claim_objects` skill to always prompt for explicit object selection before claiming, removing implicit auto-claim on casual confirmation.

#### Bug Fixes

- Fixed the setup-machine resolver connection fallback.
- Surfaced a clear message when the MCP `next_objects` call returns empty.

### Conversion Engine

#### New Features

##### SQL Server

- Added translation of `IF OBJECT_ID(...) IS NULL CREATE TABLE` to `CREATE TABLE IF NOT EXISTS`.

#### Bug Fixes

##### Teradata

- Fixed a `FormatException` in `FillTokenMatchData` when a token contains curly braces.

### Others

#### Testing Framework

##### New Features

- Added a `--where` filter to `scai test seed` for selective row capture.
- Added the BTEQ-script validate pipeline.
- Added Oracle source dialect support to `scai test seed`.
- Added server-driven testing setup with auto-deploy validation and prerequisite probes.
- Added seed-first test generation with YAML recipes.

##### Improvements

- Skipped `test_config.yaml` regeneration when the file already exists.
- Moved `test_config.yaml` under `.scai/settings/`.
- Used a per-test working directory for `snow sql -f` execution.
- Added centralized logging infrastructure for `test-seed` and `test-runner`.

##### Bug Fixes

- Fixed `scai test capture` failures on Teradata tables with `IDENTITY` columns (CTAS error 5788).

#### Code Unit Registry

##### New Features

- Marked `index`, `trigger`, and `dblink` object types as out-of-scope in the Code Unit Registry.
- Added `scriptBindings` and `FindOptions.bindings` to support BTEQ script testing.

## Version 2.28.0 (May 19, 2026)

### CLI

#### New Features

- Added the `scai data doctor` command shell with core domain models for data troubleshooting workflows.
- Added the `scai data worker generate-config` command for generating data worker configuration files.
- Added workflow lifecycle commands: `scai data migrate workflow pause`, `resume`, and `cancel`.
- Added Kerberos preflight validation for SQL Server Windows authentication on non-Windows hosts.
- Added support for deploying to source SQL Server databases, including per-engine database-context handling.

#### Improvements

- Added proxy environment variable support (`HTTPS_PROXY`, `HTTP_PROXY`, `NO_PROXY`) for the Snowflake connection string.
- Updated the default config paths for Data Migration (DM) and Data Validation (DV) to `./scai/config`.
- Hardened CLI input handling.
- Renamed the `--skip-split` flag to `--code-already-split`.
- Centralized the `client_store_temporary_credential` flag per authentication method with cross-platform parity.
- Forwarded SQL Server `trust_server_certificate` and `encrypt` options to the data worker configuration.
- Installed Teradata extras in the Data Engine Worker (DEW) Python environment for Teradata projects.

### Desktop App

#### New Features

- Added a Share Feedback link on the migration skill page and promo carousels.

### Conversion Engine

#### New Features

##### BigQuery

- Added `BQForStatementReplacer` for BigQuery `FOR...IN` loops.

##### PostgreSQL

- Translated the `'now'` string-literal cast to `CURRENT_DATE`/`CURRENT_TIMESTAMP`.
- Translated `session_user` to `CURRENT_USER()`.

##### SSIS

- Added parse-and-assess Embedded SQL lineage emission.

##### Teradata

- Added support for `çç` (U+00E7 ×2) as a Teradata concatenation operator.
- Added BTEQ `.EXPORT` translation to `COPY INTO @stage` + `GET`.
- Wrapped multi-DML Teradata macros in `BEGIN TRANSACTION` / `COMMIT` / `ROLLBACK`.

#### Improvements

##### PostgreSQL

- Flagged the Yellowbrick `rowid` pseudo-column with an Error Warning Information (EWI).

##### SQL Server

- Included constraints in SQL Server table DDL output.

##### Teradata

- Mapped known Teradata error codes to Snowflake equivalents and suppressed redundant Functional Difference Messages (FDM).

#### Bug Fixes

##### BigQuery

- Fixed `BREAK`, `CONTINUE`, and `ITERATE` being assessed as not-converted.

##### Spark SQL

- Fixed backslash-escaped single quotes in string literals.

##### SQL Server

- Fixed `CREATE TYPE FROM [bracketed_type]` parsing and transformation.

##### Teradata

- Fixed an infinite loop in volatile-table `UPDATE` conversion.
- Fixed `SSC-EWI-0001` raised on `REPLACE MACRO` with a TRAN table alias.
- Fixed hardcoded Python fallback in `TaskManager` for `BteqTargetLanguage`.
- Fixed `SfsParser` to correctly parse `EXECUTE IMMEDIATE $$...$$` blocks.
- Suppressed `SSC-EWI-0058` false positive on inner labeled compound blocks.

##### General

- Allowed `PARAMETERS` as an identifier across all SQL dialects.

### Others

#### Testing Framework

##### New Features

- Added an ETL test YAML emitter to `scai test seed`.
- Added a BTEQ script step parser for capturing and validating BTEQ workflows.
- Wired BTEQ scripts into the capture pipeline.
- Added support for multi-database delta validation via the `database_map` configuration.
- Added capture and validation support for SSIS orchestration in the testing harness.
- Added an ETL placeholder substitution engine for ETL test fixtures.

##### Improvements

- Switched Data Validation configuration from JSON to YAML.
- Added support for multiple test YAMLs per code unit in `scai test`.
- Forced autocommit in SQL Server backup-restore so backups survive procedure rollbacks.
- Handled `IDENTITY` columns during SQL Server backup-restore in the testing harness.

##### Bug Fixes

- Fixed a missing `AFFINITY` column in data validation workflow creation.
- Fixed breaking changes affecting data-validation in `testing-infrastructure`.

#### Code Unit Registry

##### New Features

- Added an `updatedAt` flag to conversion status and resync status entries.
- Added a temporal table object type.
- Added a Schema Migration Manager.
- Added 1:1 `TopLevelObjectType` entries for all Code Unit Registry `ObjectType` values.
- Added Index and Synonym `ObjectType` mappings.

##### Improvements

- Added per-part `dependsOn` emission at parse-and-assess for SSIS code units.
- Trimmed non-essential logs in SSIS code-unit registration.

##### Bug Fixes

- Forbade root-level issues on ETL code units.

## Version 2.27.0 (May 12, 2026)

### CLI

#### New Features

- Added `scai` SPCS service lifecycle commands for the Data Migration (DMV) orchestrator and worker.
- Added the `--consolidate-dbt-model-chains` option to consolidate generated dbt model chains.
- Added a `status` command to the Data Migration (DMV) orchestrator and worker.

#### Improvements

- Removed deprecated references to cloud data commands.

### Conversion Engine

#### New Features

##### SQL Server

- Added translation support for `CREATE STATISTICS`.

##### Teradata

- Added translation for BTEQ `.IMPORT VARTEXT`, `.IMPORT REPORT`, and `.IMPORT FILE` to Snowflake `COPY INTO` with a staging-pattern bulk DML flow.

#### Improvements

##### Teradata

- Changed the default `--scripttargetlanguage` for Teradata BTEQ from Python to SnowScript.

##### General

- Activated the nested CTE simplification feature.

#### Bug Fixes

##### Teradata

- Fixed `null;` placeholder emission and Error Warning Information (EWI) ordering for unsupported BTEQ nodes.

### Others

#### Testing Framework

##### New Features

- Added a typed `ScriptStep` for BTEQ and other script-based tests in `scai test seed`.
- Added an ETL result writer for capturing and validating ETL conversion output.
- Added `scai test-seed` extensions for generating BTEQ test YAML.
- Added BTEQ enrichment and discovery support on the test runner.

##### Improvements

- Folded the testing-orchestrator binaries into the `scai` CLI distribution.
- Handled `IDENTITY` columns during SQL Server backup-restore teardown in the testing harness.

#### Code Unit Registry

##### New Features

- Emitted Code Unit Registry entries for Oracle package members.

## Version 2.26.0 (May 7, 2026)

### CLI

#### New Features

- Added `token_file_path` support and improved error handling for Programmatic Access Token (PAT) credentials read from TOML configuration.
- Added directory permission validation before executing SCAI commands.
- Enabled the new `scai assessment waves` command, including the underlying assessment services and partitioning logic.

#### Improvements

- Added an auto-config option to `data migrate` and `data validate` start.
- Removed the deprecated `ai-convert` and `etl-ai-convert` CLI features.
- Removed `ai-convert` from the post-conversion next-steps suggestion.

### Conversion Engine

#### New Features

##### Oracle

- Added DML error logging support with error tables.

##### Teradata

- Added DML error logging support with error tables.

#### Bug Fixes

##### SQL Server

- Commented out `DROP SYNONYM` statements during conversion.

### Others

#### Testing Framework

##### New Features

- Added `bteq` and `snow` binary detection on the capture side, with skip-with-warning behavior when the binaries are not found.
- Added server-side source diffing for SQL Server tables with primary keys.
- Added a Layer 4 `DataRows` test target for PostgreSQL with local Docker fixtures.

##### Improvements

- Honored SQL Server Windows authentication in the test capture bridge.

#### Code Unit Registry

##### New Features

- Introduced a `ScriptItem` abstraction to separate scripts from the DDL pipeline.
- Added new SQL object types to the `ObjectType` enum, including `externalTable`.
- Added a `source.package` field and made `canonicalName` package-aware.

##### Improvements

- Deduplicated registry dependencies and code units by canonical identifier.

## Version 2.25.0 (May 5, 2026)

### CLI

#### New Features

- Added `scai settings` commands to manage CLI configuration.
- Added `--enable-dynamic-sql-analysis` flag to `code add` and `code convert`.
- Added `--start-orchestrator` support for cloud Data Migration and Data Validation.
- Added `--no-pip-upgrade` flag and version override support to the Python package environment manager.
- Added JSON output support for `cloud data migrate` and `cloud data validate`.
- Added support for installing a specific version via `scai update [VERSION]` and the `install.sh`/`install.ps1` scripts.

#### Improvements

- Unified Data Migration and Data Validation workflow commands.
- Removed the `cloud` prefix from data commands.
- Reduced CLI installer size by approximately 21% (down to about 119 MB) by removing duplicated .NET runtime files.
- Made `project defaults` always write to `project.local.yml` and removed the `--local` flag.
- Improved CLI Python environment manager to no longer force install on every run.

#### Bug Fixes

- Fixed the URL hint shown in the SCAI update notification.
- Fixed Data Migration / Validation (DMV) configuration serialization to ignore null values.
- Fixed `UnsupportedCommand` dependency injection resolution.
- Deprecated the `ai-convert` commands as they are no longer supported.

### Desktop App

#### New Features

- Added a Migration Skill Page integrated into the project workflow.
- Added code deployment support to Oracle projects.
- Added PostgreSQL as a supported source database via the new `connection add-postgresql` command with standard authentication.
- Added an SSIS executor with full pipeline support.
- Added SSIS code support to the `code add` command.

#### Improvements

- Improved Windows installer reliability and refactored installer scripts for cross-platform compatibility.
- Updated the connectivity check URL to `https://snowconvert.snowflake.com`.

### Conversion Engine

#### New Features

##### BigQuery

- Allowed reserved keywords as unquoted column names.

##### IBM DB2

- Added `COMMENT ON` statement support.
- Added `CREATE SEQUENCE` transformation to Snowflake.

##### Oracle

- Added Enterprise Business Suite (EBS) schema detection support to Oracle metadata queries.

##### PostgreSQL

- Added PostgreSQL as a supported source dialect with metadata catalog queries, identifier utilities, and DDL reconstruction with PostgreSQL-version-safe `attgenerated` handling.

##### Redshift

- Added CSV support and column mapping for CloudWatch Logs.
- Enhanced query log parsing.

##### SQL Server

- Added snapshot isolation support for capturing deltas.
- Added support for the style argument in `CONVERT` for unresolved expression types.

##### SSIS

- Flagged Data Flow components reached via an error-output path.

##### General

- Added `MD5` to ANSI built-in function mappings.

#### Improvements

##### Teradata

- Updated variable syntax from `&{VAR}` to `<%VAR%>` and updated Functional Difference Message (FDM) text to reference Snowflake CLI.

#### Bug Fixes

##### Oracle

- Fixed false positive `SSC-EWI-OR0036` for numeric arithmetic.

##### PostgreSQL

- Fixed handling of `nextval('seq'::regclass)` in `PgNextValReplacer`.

##### SQL Server

- Fixed `SSC-EWI-0013` crash on lower-case error context functions.
- Fixed dynamic-SQL back-propagation marker displacement and comment preservation.
- Fixed `ALTER TABLE ENABLE/DISABLE TRIGGER` comment-out scope.
- Fixed schema context being lost after `USE DATABASE` in clone isolation.

##### Teradata

- Fixed macro assessment to count lines instead of ignoring them.

### Others

#### Testing Framework

##### New Features

- Added `--check-env` flag to `etl-validate` to verify the runtime environment.
- Added a Snowflake Task DAG validator with `EXECUTE TASK`, `TASK_HISTORY` polling, and DAG comparison.
- Added `--step-based` flag for v2 YAML generation in `scai test seed`.
- Made `--execution-log` optional for `scai test seed`.
- Added cell-level diff support to data validation.
- Added a synthetic key-based diffing strategy.
- Added a primary-key-based delta capture strategy.
- Added side-effects validation for stored procedures.
- Added User-Defined Function (UDF) validation support.
- Added unquoting of identifiers when injecting values during validation.
- Added parallel execution for read-only test cases.
- Added a 2-pass snapshot mode for performance.
- Added a BTEQ execution strategy with a native BTEQ runner and doctor command.
- Added an ETL test YAML schema and parser.
- Added support for capturing and validating Teradata `PERIOD` columns.
- Added 2-pass support for Teradata in `scai test seed`.
- Added support for capturing and validating Teradata stored procedures with `INOUT` and `OUT` parameters.
- Added support for capturing and validating Teradata `SET` tables.
- Added support for capturing and validating Teradata user-provided macros.
- Added capture and validation support for RedShift `OUT`, `INOUT` scalar, and `INOUT` refcursor parameters.
- Added capture and validation support for SQL Server `OUT` parameters.

##### Improvements

- Made step-based test YAML the default in `scai test seed` and deprecated the v1 format.
- Honored `--source-connection` in `scai test capture`.
- Defaulted baseline storage to Snowflake.
- Annotated collation in result-set diffs caused by collation differences.
- Showed result-set row count and output parameter names in validate output.

##### Bug Fixes

- Fixed `scai test capture` access denied for non-administrator Windows users.
- Fixed transient table validation querying the entire stage.
- Fixed wrong type coercion in the delta comparator.
- Fixed baseline stage lookup collision across objects with identical parameter hashes.
- Fixed an additional replay suffix being appended when the schema and database had the same name.
- Fixed table corruption on procedures wrapped in transactions.
- Filtered non-tabular objects from delta capture affected tables.

#### Code Unit Registry

##### New Features

- Added scripting collection support for `MLoad`, `FastLoad`, `TPump`, and `TPT` in the code unit registry.
- Standardized platform and format identifiers in the code unit registry to canonical SnowConvert enum values.

##### Bug Fixes

- Fixed a race condition while emitting code unit test YAMLs.
- Fixed schema `canonicalName` resolution producing an `UNKNOWN_SCHEMA` placeholder.

## Version 2.24.0 (Apr 24, 2026)

### CLI

#### Improvements

- Improved JSON output in the console.

### Desktop App

#### New Features

- Added an ETL/PowerBI conversion summary.

#### Improvements

- Updated the banners on the Project Page.

### Conversion Engine

#### New Features

##### Hive

- Added support for converting double-quoted string literals to single-quoted Snowflake literals.

##### PostgreSQL

- Added support for converting the `"char"` function/cast to Snowflake `LEFT`.

##### General

- **Check Constraints Support**: Added comprehensive support for converting CHECK constraints to Snowflake across multiple languages, enabling migration of table-level and column-level CHECK constraints with automatic translation to Snowflake’s native syntax:

  - [Oracle CHECK constraints](../../../translation-references/oracle/sql-translation-reference/create-table#check-constraints)
  - [SQL Server CHECK constraints](../../../translation-references/transact/transact-create-table#check-constraints)
  - [Teradata CHECK constraints](../../../translation-references/teradata/sql-translation-reference/ddl-teradata#check-constraints)
  - [PostgreSQL CHECK constraints](../../../translation-references/postgres/ddls/create-table/postgresql-create-table#check-attribute)
  - [IBM DB2 CHECK constraints](../../../translation-references/db2/db2-create-table#check-constraint)
  - [Sybase IQ CHECK constraints](../../../translation-references/sybase/sybase-create-table#constraints)
  - [Vertica CHECK constraints](../../../translation-references/vertica/vertica-create-table#check-constraint)
- Added support for converting User-Defined Functions (UDFs) containing DDL statements to procedures, issuing `SSC-EWI-0068`.

#### Improvements

##### Teradata

- Made exception handler translation handler-type-aware.

#### Bug Fixes

##### SSIS

- Fixed an issue where a variable was not updated in the variables control table during `For Each` enumerator conversion.

## Version 2.23.0 (Apr 23, 2026)

### CLI

#### New Features

- Added `scai ai-convert list-drivers` and `scai ai-convert remove-driver` commands to manage uploaded Teradata driver wheel files on the AI verification stage.

#### Improvements

- Added optional path option to `start-cloud-worker --auto-config`.
- Improved handling of unknown workflow status in Data Validation and Data Migration.

### Desktop App

#### New Features

- Added Macro and JoinIndex extraction support for Teradata.
- Added execution summary output for ETL replatform and PowerBI repointing projects.

#### Bug Fixes

- Fixed interactive code extract dropping Database and Schema, and incorrect within-rank ordering during code deploy.
- Fixed empty source directory validation and improved error messages.

### Conversion Engine

#### New Features

##### BigQuery

- Added `EXECUTE IMMEDIATE` translation to Snowflake.

##### SQL Server

- Replaced `ORIGINAL_LOGIN()` with `CURRENT_USER()` in Transact-SQL.

##### SSIS

- Added `.ispac` file support for SSIS ETL migrations.

##### General

- Added dynamic SQL analysis task.
- Added User-Defined Type (UDT) constructor transformations for Oracle and IBM DB2 `ARRAY` types.

#### Improvements

##### dbt

- Excluded disconnected columns from target dbt models.

#### Bug Fixes

##### Teradata

- Reclassified translatable `CAST`-level date `FORMAT` clauses as Functional Difference Message (FDM).
- Commented out macros referencing unsupported DBC views.

##### SSIS

- Fixed `RowCount` components with the same name generating concurrency issues when data flows execute in parallel.
- Fixed `m_update_row_count_variable` macro emitting invalid dotted `SET` for session variables.

##### General

- Fixed emitted names on parent nodes not preserving comments.

## Version 2.22.0 (Apr 20, 2026)

### CLI

#### New Features

- Added `scai update` command for self-updating the local CLI installation.

#### Improvements

- Moved driver cache location from `~/.scai` to `~/.snowflake/scai`.

### Desktop App

#### Improvements

- Updated AI Verification banner wording for clarity.

### Conversion Engine

#### New Features

##### Teradata

- Added support for case-specific column attributes.

#### Improvements

##### Teradata

- Propagated numeric column-level `FORMAT` attribute to DML `CAST`-to-string conversions.

## Version 2.21.0 (Apr 17, 2026)

### CLI

#### New Features

- Added new `cloud-list-migrations` and `cloud-list-validations` commands.
- Added `--driver-path` support to `query` and `project defaults set` commands.
- Added support for additional source authentication methods during code extraction: Windows integrated security (SQL Server), IAM (Redshift provisioned cluster and serverless), and LDAP (Teradata).
- Added auto-update support for the local CLI installer.
- Added object exclusion support to the `scai assessment` command.

#### Improvements

- Allowed override of warehouse and role for cloud Data Validation and Data Migration.
- Synced cloud Data Validation and Data Migration with Data Migration Orchestration (DMO) validations.
- Updated `cloud-diagnostics` to include Data Validation checks.
- Enabled cloud data validation by default.
- Improved CLI installer scripts reliability and output.
- Standardized compressed artifact folders and improved install reliability.

### Desktop App

#### New Features

- Added support for local overrides of project values at the project level.

#### Improvements

- Enhanced AI Verification and migration pages with Cortex plugin promotions.
- Improved data migration connection handling with timeouts and safe connection string parsing.

### Conversion Engine

#### New Features

##### Oracle

- Added Oracle as a supported source database for code extraction, including connection setup, metadata queries, object definitions, and external driver loading.
- Added extraction support for `Package`, `Synonym`, and `Type` objects.

##### Teradata

- Added user-provided driver support.
- Added Teradata support for local data validation.
- Added `TD_MONTH_OF_YEAR` and `MONTHNUMBER_OF_YEAR` translation to Snowflake `MONTH`.
- Added `TD_YEAR_OF_CALENDAR` translation to Snowflake `YEAR`.
- Migrated `ACTIVITY_COUNT` to Snowflake native support.
- Translated BTEQ `ERRORLEVEL` 4-line `DROP` pattern and standalone `IF ERRORLEVEL` checks.
- Transformed `ECHO` to `SYSTEM$LOG_INFO` with FDM.

#### Improvements

##### Oracle

- Preserved `PIVOT` inline aliases.

#### Bug Fixes

##### Multi-Platform

- Normalized lineage keys in `ObjectReferences.csv`.

##### Teradata

- Fixed `TRANSLATE USING *_TO_LATIN` incorrectly marked with EWI.
- Fixed `InvalidCastException` in `CAST(aggregate AS INTERVAL)`.

##### SSIS

- Fixed expression patterns not being converted (`SSC-EWI-SSIS0002`).

## Version 2.20.0 (Apr 13, 2026)

### New Features

#### General

- `USER-DEFINED TYPES` translation to Snowflake-native `USER-DEFINED TYPES`. Enabled for:

  - IBM DB2
  - Oracle
  - PostgreSQL
  - SQLServer
  - Sybase IQ
  - Teradata
- `INTERVAL` datatype translation to Snowflake-native `INTERVAL` datatype (PuPr). Enabled for:

  - Amazon Redshift
  - Google BigQuery
  - IBM Netezza
  - Oracle
  - PostgreSQL/Greenplum
  - Spark/Hive SQL
  - Teradata
- Added Snowflake account-level feature flags.
- Added mechanism to set default source connection at project level.

#### Teradata

- Added Teradata support for code extraction.
- Added support for code add for Teradata projects.
- Added column `FORMAT` attribute support in DML statements.
- Added `SIGNAL SQLSTATE` to `RAISE` transformation with FDM for unsupported `SET` items.

### Improvements

#### SQL Server

- Added `FORMAT` date specifiers `dddd`, `F`–`FFFFFFF`, `z` with FDM markers.

#### Teradata

- Replaced `SSC-EWI-TD0031` with `RTRIM` fix for `LIKE` on `CHAR` columns.
- Moved `USING` clause to `EXECUTE IMMEDIATE` for `PREPARE` with variable markers.
- Added Teradata driver upload validation against approved versions for AI Verification.

### Bug Fixes

#### Oracle

- Fixed `TRIM`/`LTRIM`/`RTRIM` on `RAW` (`BINARY`) columns.

#### SSIS

- Fixed Execute SQL task not being converted when invoking stored procedure.
- Fixed column naming with single or double quotes in `SQLCommand` of OLEDB Source generating runtime errors.
- Fixed parsing error EWIs not being generated on SQL output code for tasks executing SQL.

#### Teradata

- Fixed `to_binary()` incorrectly throwing `SSC-EWI-0073`.

#### General

- Fixed Migration Skill promo banner layout on the Home page.
- Fixed `NullReferenceException` from engine execution with actionable error message (`CVT0011`).
- Fixed wrong counting in selection summary in AI code conversion.
- Fixed CSnake corrupted environment when pip is not installed.
- Fixed routing to code conversion from an unavailable page.

## Version 2.19.0 (Apr 08, 2026)

### New Features

#### Teradata

- Added Teradata connection support.
- Added Teradata driver upload functionality for two-sided AI Verification.

#### General

- Integrated deployment reports into the code deployment workflow.
- Added Migration Skill promotional banner to the Home page.
- Added support for user-defined alias type extraction.

### Improvements

#### SQL Server

- Added dedicated EWI for `SAVE TRANSACTION` statement.

#### Teradata

- Improved `SSC-FDM-TD0013` to avoid false positives in certain situations.

#### General

- Added path validation before conversion.
- Suppressed `FDM-0007` for `DROP IF EXISTS` statements in lineage phase.

### Bug Fixes

#### SSIS

- Fixed variable redeclarations inside of containers.
- Fixed plus operator for `VARBINARY` concatenation.

#### General

- Fixed `CONCAT_WS` to wrap value arguments in `ARRAY_CONSTRUCT`.
- Fixed AI code conversion reporting different numbers in results.
- Fixed AI Verification showing default testing mode instead of two-sided mode when status is pending.

## Version 2.18.0 (Mar 30, 2026)

### New Features

#### PostgreSQL

- Added transformation support for the `QUOTE_LITERAL` function.

#### Redshift

- Added support for Iceberg migrations.
- Enabled Cloud Data Migration for Redshift.
- Added support for `CASCADE DROP` transformation.

#### SSIS

- Added conversion of `UserName`, `PackageName`, `PackageID`, and `ExecutionInstanceGUID` SSIS System Variables.
- Enabled SSIS Data Flow Simplification as a GA feature.

#### Teradata

- Enabled AI Conversion for Teradata.
- Added `CREATE DATABASE` translation to Snowflake.

#### General

- Added Cloud Data Validation foundation layer.
- Added CSV report writer for code extraction.
- Added extraction log writer for code extraction.
- Integrated extraction reports into the code extraction workflow.
- Added opt-in support for cloud deployment status tracking.

### Improvements

#### General

- Added autoplay to the carousel component.
- Improved uploaded drivers retrieval for AI Verification.
- Enabled ReadyToRun pre-compilation for improved startup performance.
- Improved AI code conversion error messages when Cortex/LLM access is denied.
- Improved two-sided AI Verification environment handling and navigation stability.
- Improved performance by using local credentials first to avoid unnecessary Snowflake connections.
- Added Functional Difference Messages (FDMs) to reusable transformations.

### Bug Fixes

#### BigQuery

- Fixed false positive `EWI-0073` in BigQuery transaction replacers.

#### SQL Server

- Fixed `CONVERT` with `GETDATE` in `DEFAULT` expressions.
- Fixed missing comma before `CONSTRAINT` in `CREATE TABLE`.

#### SSIS

- Fixed identifier sanitization for Snowflake root task names.
- Fixed SSIS `ExecutePackage` connection manager-based references.

#### General

- Fixed telemetry and logs directory permissions.
- Fixed error code when connection test fails.
- Fixed default object type from `views` to `view` in selector report creation.
- Fixed AI Conversion “not processed” typo in results display.

## Version 2.17.0 (Mar 25, 2026)

### New Features

#### Oracle

- Added `CONNECT_BY_ROOT` pass-through support.

#### PostgreSQL

- Added support for the `EXTRACT` built-in function.

#### Redshift

- Added support for the `EXTRACT` built-in function.
- Added support for the `HLL` aggregate function.

#### SQL Server

- Added `OBJECTPROPERTY()` function conversion support.
- Added `UNPIVOT` operator translation support.
- Added support for `GOTO`/`LABEL` statement translation to nested procedures.
- Added SQL Server Agent Job closure support with ownership, tagging, notification, and multi-schedule fan-out.
- Added `CREATE SYNONYM` statement support.

#### SSIS

- Added Microsoft Cache Transform (`Microsoft.Cache`) translation to dbt.
- Added `--simplify-ssis-dataflow` option for SSIS conversion.

#### General

- Added Teradata driver upload functionality for two-sided AI Verification.
- Added carousel with CLI and Cloud Data Migration information.
- Enabled Cloud Data Migration by default.
- Added ability to deploy objects when status is verified by user.
- Enabled an additional ETL replatform source in the UI.

### Improvements

#### SQL Server

- Added defensive guards to `GOTO`/`LABEL` decomposition logic.
- Added `WAITFOR TIME` commenting with Functional Difference Message (FDM).
- Added `SSC-FDM-TS0055` for database-scoped `CREATE USER`.
- Added FDM for global temporary tables.
- Changed `DEALLOCATE` to use FDM instead of EWI.

#### SSIS

- Normalized reusability tracker keys and conditionally suppressed `SSC-EWI-SSIS0008`.
- Simplified SSIS FileSystem Task SQL output.

#### General

- Enhanced AI Verification with estimation formulas retrieval.
- Added validation for two-sided AI Verification source files (UTF-8 no BOM, LF line endings).
- Improved engine crash exception propagation to provide clearer error messages.
- Added TaskManager crash diagnostics for Windows `CVT0008` errors.
- Added filename generation in the element inventory.
- Removed `VARCHAR` length limits from control variables schema.

### Bug Fixes

#### Redshift

- Fixed database not being added to qualified object names on extraction.

#### General

- Fixed code conversion failing when using offline mode.
- Fixed consolidated source not being preserved across repeated code extractions.
- Fixed error message to show supported languages for invalid source language errors.
- Fixed rendering of icons for UTF-8 consoles.

## Version 2.16.1 (Mar 20, 2026)

### New Features

#### SQL Server

- Added SQL Server Agent Job support for CRON schedule building, `sp_send_dbmail`, and `sp_add_category` translation.
- Added `SCOPE_IDENTITY()` transformation to Snowflake time-travel queries.
- Added support for `DROP PROCEDURE` statement with type signatures.

#### SSIS

- Added ADO NET Source (`Microsoft.DataReaderSourceAdapter`) translation to dbt.

#### Power BI

- Added implementation flag support on entity connector types.

#### General

- Added Cloud Data Exchange Worker for data migration workflows.
- Added infrastructure diagnostics for Cloud Data Migration.

### Improvements

#### Hive

- Included table naming convention support.

#### Oracle

- Added `INSTR` negative position workaround for `position = -1`.

#### SQL Server

- Added `CONVERT` with style mapping to `TO_DATE`/`TO_TIMESTAMP`.
- Added `CREATE STATISTICS` commenting with `SSC-FDM-TS0048` Functional Difference Message (FDM).
- Replaced `EWI-0035` with specific FDMs for `CHECK` constraint handling.
- Removed partition placement `ON` clause from constraints in `CREATE TABLE`.
- Added new Error Warning Information (EWI) for `OBJECT_SCHEMA_NAME`.
- Updated `SSC-FDM-TS0035` trigger FDM message.

#### SSIS

- Improved per-executable resilience, pipeline column enrichment, and GUID resolution.
- Added package name as a prefix of the Snowflake task names.

#### Teradata

- Included `FORMAT` literal in `TD0040` message.

#### General

- Deprecated the selector for code deployment, restricting it to SQL Server and Redshift only.
- Improved conversion performance for code-only projects by disabling registry generation.
- Renamed `legacy_structure` project type to `Full` and `Code` for clarity.
- Improved assessment cleanup by removing engine output after execution.
- Removed legacy `converted` folder references from the project structure.
- Added AI verification status column with parent tooltips in the UI.
- Cloud Data Migration now uses images from the SPCS Image Registry directly.

### Bug Fixes

#### Oracle

- Fixed a variable named `current_date` being incorrectly converted to a function call.

#### Redshift

- Fixed database not being recognized in Redshift code units.
- Fixed EWI on out cursor transformation.

#### SQL Server

- Fixed `FOR XML PATH('')` transformation dropping expressions.

#### SSIS

- Fixed version upgrade emitting malformed XML.
- Fixed nested Jinja in dbt `source()` calls for VariableTable access mode.

#### General

- Fixed language flags to avoid repeated short names.
- Fixed code conversion input and output path resolution in the UI.
- Fixed AI code conversion on Windows by preparing report paths before zipping.
- Fixed AI Conversion status display and progress tracking.
- Fixed ArrangeLog Logger not being disposed, causing Windows file locking.

## Version 2.15.1 (Mar 13, 2026)

### New Features

#### General

- Added an assessment report page with a code tag component for viewing conversion results.

### Improvements

#### General

- Improved code deployment to include dependencies when a `WHERE` clause filter is defined.
- Scoped the new project structure and registry to SQL Server and Redshift platforms.
- Added source identifier tracking to schema objects during extraction.
- Updated application update notifications to display the download URL directly.

### Bug Fixes

#### General

- Fixed broken Data Validation endpoints.
- Fixed a terminal output issue where progress bars could collide with other output.

## Version 2.15.0 (Mar 13, 2026)

### New Features

#### Hive

- Added support for the `GET_JSON_OBJECT` function.

#### SQL Server

- Added non-ASCII identifier double-quoting transformation for Transact-SQL.

#### Teradata

- Added support for Teradata file extraction.

#### SSIS

- Added conversion support for `Microsoft.CharacterMap` transformations.
- Added conversion of `sp_add_jobstep` for SQL Server Agent Job orchestration.

#### General

- Added support for iteratively adding code units to a project.
- Added local report generation for Cloud Data Migration.
- Integrated Testing Orchestration (seed, capture, and validate) into the desktop application.

### Improvements

#### SQL Server

- Added a Functional Difference Message (FDM) for `SET IDENTITY_INSERT` statements, which are now commented out during conversion.

#### Power BI

- Improved Power BI version integration and applied general cleanup.

#### General

- Integrated the resync command with the conversion engine for re-scanning modified converted files.
- Integrated resync into the code accept workflow to keep issue metadata in sync.
- Enhanced the selection summary panel layout for smaller window sizes.
- Disabled connections with invalid authenticators in Snowflake.
- Extended the close-app guard to cover active Code Extraction jobs.
- Added application type information to CSV reports.
- Improved IPC channel error handling.

### Bug Fixes

#### SQL Server

- Fixed an issue where semicolons in SQL Server passwords caused connection failures.
- Fixed alias duplication in `UPDATE...FROM` translation.
- Fixed `XML.value()` instance parsing and absolute-path handling.

#### SSIS

- Fixed `FuzzyLookup` to only propagate passthrough columns.
- Fixed `ExcelSource` not displaying Error Warning Information (EWI) markers in dbt models.

#### Power BI

- Fixed SQL extraction from Power Query connections when schema and object names use double quotes without an ending semicolon.

#### General

- Fixed account locator extraction for AI Code Conversion when using Key Pair authentication.
- Fixed an issue where the Key Pair passphrase argument was incorrectly omitted when empty or null.
- Fixed an issue where code formatting could cause errors.
- Fixed a race condition that could affect job initialization during concurrent operations.
- Applied general stability fixes.

## Version 2.14.0 (Mar 06, 2026)

### New Features

#### SSIS

- Added conversion support for `ExcelDestination` components to Snowflake dbt.
- Added conversion support for SQL Server Agent Job `TSQL` command references.
- Added a catch-all replacer for unsupported SQL Server Agent Job procedures.
- Added conversion of `sp_delete_job` to `DROP TASK IF EXISTS` for SQL Server Agent Jobs.
- Added conversion of `sp_update_job` to `ALTER TASK ... SUSPEND/RESUME` for SQL Server Agent Jobs.
- Added conversion support for `Microsoft.FileSystemTask` transformations.
- Added conversion support for `Microsoft.FuzzyLookup` transformations.
- Added support for SSIS `Project.params` conversion.

#### SQL Server

- Added conversion of `WAITFOR DELAY` to `CALL SYSTEM$WAIT`.

#### General

- Added Single Sign-On (SSO) support for executing AI Verification jobs.
- Added Time-based One-Time Password (TOTP) Multi-Factor Authentication (MFA) support.
- Added a resync command for re-scanning modified converted files to update issue metadata.
- Added estimation report generation support.
- Added the last job status per code unit on the selection page.

### Improvements

#### SSIS

- Improved support for older SSIS package formats with automatic version upgrade.

#### Redshift

- Improved the layout of the Redshift connection form.

#### General

- Improved specification and migration report artifact downloads to include terminal job status.
- Extended the close-app guard to cover data migration, data validation, and deployment jobs.
- Improved connection error messages with better formatting.
- Improved log and report file path handling.
- Added individual object listing in the code deploy success summary.
- Added validation for AI Verification job files in the project directory.
- Added application type information to the assessment report.
- Added a flag to skip split operations during code extraction.

### Bug Fixes

#### SQL Server

- Fixed the double-dot identifier transformation to correctly reference the latest active database.
- Fixed `BEGIN TRAN` syntax conversion to Snowflake.

#### SSIS

- Fixed handling of empty XML elements and hardened upgrade error handling.

#### Redshift

- Fixed Redshift code unit name matching in AI Verification.

#### General

- Fixed Data Validation Framework (DVF) progress corruption.

## Version 2.13.0 (Mar 03, 2026)

### New Features

#### Redshift

- Added support for RedShift function extraction.

#### SSIS

- Added support for converting `sp_stop_job` to `ALTER TASK ... SUSPEND` for SQL Server Agent Job orchestration.
- Added an orchestration file generator for SQL Server Agent Job conversion.

#### Power BI

- Added `QUOTED_IDENTIFIERS_IGNORE_CASE` validation for column renaming support in Power BI conversions.

#### General

- Added a `CodeSyncService` and `IssuesService` for synchronizing issue metadata (Error Warning Information, Functional Difference Messages, Out of Scope, Performance Review) in the code unit registry when converted files are modified.
- Added connection timeout support for Snowflake credentials with authentication-specific defaults.

### Improvements

#### General

- Added a terminal link and icon to the SnowConvert AI home page for quick access to the command-line interface.
- Updated `AgentJobOptions` to support custom database usage and extra file dependencies.
- AI Verification files are now persisted in the project directory instead of temporary folders.
- Improved error handling for source connection resolution.

### Bug Fixes

#### General

- Fixed an issue where the application did not handle .NET backend process crashes gracefully.

## Version 2.12.0 (Feb 27, 2026)

### New Features

#### General

- Added a `SessionManagerService` for session lifecycle management.
- Moved the license file activation from the Login page to the Help menu.

### Improvements

#### General

- Implemented mode-aware documentation links in update notification banners.

### Bug Fixes

#### General

- Fixed an issue where missing C# dependencies caused build errors.
- Fixed a crash on the progress page when step titles were unmapped, by filtering out steps without display strings.
- Fixed slow loading for AI Verification jobs.

## Version 2.11.0 (Feb 27, 2026)

### New Features

#### General

- Implemented state management for code deployment.
- Added a Testing Orchestration engine with CSnakes Python interop.
- Implemented file size validation for AI processing.
- Added T-SQL to Snowflake TDD workflow skills for AI-assisted translation development.

#### Hive

- Added support for the Hive `InStr` function.
- Added support for the Hive `COLLECT_SET` function.

#### Netezza, SQL Server, Sybase, Teradata

- Added a `disable-use-database-generation` flag for schemas.

#### PostgreSQL

- Added PostgreSQL `RETURN QUERY` transformation support.
- Added preprocess and partial transformation support for Python functions in PostgreSQL.

#### Redshift

- Added support for transforming cursor out parameters in RedShift.

#### SSIS

- Added multi-target column unpivot translation support for SSIS.
- Added Microsoft.Pivot transformation support for dbt translation.
- Added Error Warning Information (EWI) for unreviewed SSIS expression functions.
- Introduced Agent Job 2.1 with base replacer and EWI/FDM codes for SSIS.

### Improvements

#### General

- Enhanced error handling in AI verification results by adding `lastError` to the job state.
- Enhanced the AI Verification Orchestrator to handle transient PENDING statuses.
- Enhanced AI verification job status handling by adding a ‘FAILED’ state and improving error logging.

#### Power BI

- Removed the renaming of calculated columns in Power BI conversions.
- Removed table aliases when generating column renames for Power BI.

### Fixes

#### General

- Fixed a bug related to Extract Code and Code Unit Registry.

#### Redshift

- Fixed an issue with data migration navigation.

#### SSIS

- Fixed FlatFileSource naming to use the component path for unique identifiers.

## Version 2.10.0 (Feb 24, 2026)

### New Features

#### Hive

- Added support for the Hive `regexp_extract` built-in function.
- Added a replacer for the Hive `ISNULL` function, incorporating validation best practices.

#### SSIS

- Implemented conversion for SSIS Excel Source components to Snowflake dbt.

#### General

- Added an option to disable the generation of `USE DATABASE` statements.

### Improvements

#### SQL Server

- Optimized Transact-SQL conversions by using the native `parse_json()` function instead of a custom UDF helper.

#### SSIS

- Added sanitization of identifiers for the flat file source translator.
- Improved the SSIS TDD skill based on insights from Microsoft Pivot migration retrospectives.

#### General

- Added test generation capabilities guard and `TST0003` error handling.
- Renamed the Data Validation CSnakes bridge to `_dvf_csnakes_bridge.py`.

### Bug Fixes

#### Power BI

- Fixed an issue where query values were lost when migrating multiple Power BI Template (`.pbit`) files simultaneously.

## Version 2.9.0 (Feb 23, 2026)

### New Features

#### Hive

- Added support for converting the `FROM_UTC_TIMESTAMP` function from Hive to Snowflake.

#### SSIS

- Added support for SSIS Aggregate transformation in dbt translation.
- Added an `ssis-tdd` skill to support the SSIS-to-Snowflake Test-Driven Development (TDD) workflow.
- Added support for translating `Microsoft.Sort` transformations from SSIS to Snowflake.

#### Power BI

- Added an optional `ROLE` parameter for Power BI conversions.

#### General

- Enhanced AI Verification by adding support for Key Pair Authentication.
- Added registry generation to the Extract command.
- Integrated with the `scai test seed` test generation library.
- Added `CUBE` to the list of supported ANSI built-in functions.

### Improvements

#### General

- Enhanced AI conversion logs with improved detail and readability.
- Improved the display of friendly error messages and server-side error details on the AI code conversion error page.

### Bug Fixes

#### SSIS

- Fixed dot-delimited table names being incorrectly split during dbt model generation for SSIS conversions.
- Fixed the `ExcelSource` conversion to the previous Snowflake dbt TDD implementation.

#### General

- Fixed an issue with AI Verification where double-nested source directories were not resolved correctly.
- Fixed an issue with AI Verification two-sided mode serialization.
- Fixed an issue with Data Validation and the minimum Python environment version installation.

## Version 2.8.0 (Feb 19, 2026)

### New Features

#### Hive

- Added support for converting the `FROM_UTC_TIMESTAMP` function from Hive to Snowflake.

#### SSIS

- Added support for SSIS Aggregate transformation in dbt translation.
- Added an SSIS-TDD skill to support the SSIS-to-Snowflake Test-Driven Development workflow.
- Added support for Microsoft.Sort operations in SSIS-to-Snowflake conversions.

#### Power BI

- Added an optional `ROLE` parameter for Power BI conversions.

#### General

- Introduced an `-o` option for ETL AI verification.
- Implemented Snowflake credential override options and improved authentication error messages.
- Added `CUBE` to the list of supported ANSI built-in functions.

### Improvements

#### General

- Enhanced internal data transfer objects, input building, and progress handling.
- Updated the version retrieval script to save results directly to a file.
- Unified AI Verification with the Standard Job Orchestrator for streamlined operations.
- Refactored job orchestration to support asynchronous job initiation.
- Updated the ‘limit reached’ message for improved clarity.

## Version 2.7.0 (Feb 13, 2026)

### New Features

#### General

- Added Snow-to-Snow support in Data Validation.
- Added AI verification support for `SEQUENCE` object types.
- Added support for a new AI code conversion contract.

### Improvements

#### SSIS

- Extended `IsString` functionality to detect strings through parentheses, function calls, casts, and concatenation (`+`) expressions.

#### General

- Implemented code unit deduplication in the Job Status Mapper to prevent duplicate entries.
- Added a link to the assessment report and improved the ordering of cards on the project page.
- Enabled offline mode for license installation and improved connection error logging.
- Improved error messages for Snowflake authentication failures and refactored connection resolution for commands.
- Introduced `AiVerificationTestBase` to support language as a parameter in AI verification tests.
- Updated the AI initial prompt message and corrected a UI icon.
- Enhanced AI verification job execution to prioritize the `source_Processed` directory when available.
- Added `InvalidInputError` handling for AI verification inputs.

### Fixes

#### SSIS

- Fixed inconsistent Start/End block tagging in stored procedure output.

#### General

- Fixed an issue where SnowConvert AI displayed unsupported objects as pending.

## Version 2.6.3 (Feb 11, 2026)

### New Features

#### SQL Server

- Added support for `INSERT INTO EXECUTE` in procedures.
- Added support for `CONCAT_NULL_YIELDS_NULL`, `NUMERIC_ROUNDABORT`, and `ARITHABORT` SET options.

#### SSIS

- Added OLE DB Command (DELETE/UPDATE) support for SSIS to dbt translation.
- Added conversion of completion precedence constraints.

#### Power BI

- Added support for repointing connections identified as pending changes.

#### General

- Added Terms and Conditions acceptance functionality.

### Improvements

#### SSIS

- Improved the placement of SSIS task comment tags for better readability.

#### General

- Enhanced the project header to display source dialect names alongside project names.
- Improved error handling for array-type errors in conversion results.

### Bug Fixes

#### SQL Server

- Fixed resultset handling for set operators.

#### SSIS

- Fixed false column collision on Lookup No Match output paths.
- Fixed start tags not being added to unsupported control flow tasks.

#### General

- Fixed deployment error messages not being cleared after a successful redeployment.
- Fixed an issue where empty capabilities caused unexpected behavior.

## Version 2.5.0 (Feb 06, 2026)

### New Features

#### Hive

- Added support for Hive Date Format.

#### General

- Added new outcomes for source and converted dependency failures in AI Verification.
- Added a SQL platform selector.
- Implemented logic to split logs by execution and to clean up logs older than 30 days.

### Improvements

#### General

- Changed connection testing to use session state instead of querying data.
- Updated conversion status messages and adjusted icon usage in status templates for better clarity and consistency.
- Updated the `deployment_order` column to allow null values and enhanced parsing logic in the CodeConversionService.
- Changed conversion status and type to object type.
- Enhanced script extraction descriptions and integrated source dialect information in the CodeConversionService CodeLoadPage.
- Added quick access to the connections file from the Login page.
- Ensured all files are copied in AI output when AI flags are enabled.

## Version 2.3.3 (Feb 04, 2026)

### New Features

#### BigQuery

- Enabled BigQuery dialect support for AI Verification.

#### PostgreSQL

- Enabled PostgreSQL dialect support for AI Verification.

#### Redshift

- Added support for the `STRTOL` function.
- Added support for assigning query results to variables within stored procedures.

#### SQL Server

- Added support for the `HASHBYTES` function.

#### General

- Added accept command for AI-Convert.
- Added object selector support in Code Deployment.
- Added source and target mapping information in the ETL.Elements report.
- Added support for the `FROM_UNIXTIME` built-in function.

### Improvements

#### SQL Server

- Improved code formatting.
- Excluded aliases from the Object References report.

#### General

- Added ‘Learn More’ links to footers and introduced `body-small-italic` text variant.
- Migrated from `InternalError` to the `ScError` interface for enhanced error handling.
- Added safeguard to prevent accidental application closure during active conversions.
- Enhanced error handling for code conversions and added tooltips to results tables in Data Migration and Validation.
- Removed unused reject change functionality.
- Refactored connection resolution to separate credential validation from connectivity testing.
- Updated DataMigrator component and refactored Snowflake credential handling.

### Bug Fixes

#### PostgreSQL

- Fixed the ordering of generated function options to prevent deployment errors in Snowflake.

#### General

- Fixed an issue preventing the reporting issue modal from displaying correctly.
- Fixed `HOST_NAME()` function conversion to `CURRENT_IP_ADDRESS()` when using FDM.

## Version 2.3.2 (Jan 30, 2026)

### New Features

#### General

- Added a legacy view for code process results.
- Added support for using a `.yaml` configuration file in the Data Validation command.
- Added direct access to OpenLogs from the application menu.
- Added support for an object selector in Data Validation.

### Improvements

#### General

- Implemented a mechanism to read from `connections.toml` and fall back to `config.toml` when retrieving the default connection.

### Fixes

#### General

- Fixed an issue where AI Verification was missing `.sql` content.
- Fixed an issue where the application did not navigate to results after partially successful migration and validation, and resolved name overflow in progress cards.

## Version 2.3.1 (Jan 28, 2026)

### New Features

#### Redshift

- Added support for RedShift in Data Validation.

#### General

- Added a Sign Out option to the application menu.
- Implemented an offline mode for project commands.
- Added support for the `Unix_TimeStamp` built-in function.

### Improvements

#### Redshift

- Improved error propagation within the Data Validation feature.

#### General

- Added a loading fallback mechanism for the Login page.
- Added dynamic model validation to AI Verification processes.
- Refactored the AI Verification Service to manage job options on a per-project basis.
- Set the connection project default and improved AI Verification commands.
- Improved handling of `ConvertedObjectFixAttemptFailed` status in two-sided conversion runs.
- Added migration project context, loading it from a project-relative path.

### Fixes

#### Teradata

- Fixed the ordering of column options when column-level collation is generated for Teradata conversions.

#### General

- Fixed path comparison logic to correctly handle null or whitespace input in the `ValidateInputPath` method.
- Resolved an issue causing blinking when opening a project.

## Version 2.3.0 (Jan 26, 2026)

### Improvements

#### SSIS

- Added support for converting Microsoft.BulkInsertTask.
- Implemented conversion support for Execute Package Variable Binding.
- Added support for converting `INSERT...OUTPUT INSERTED` statements to `INSERT + SELECT INTO`.

#### PostgreSQL

- Updated the transformation of `<<` and `>>` bitwise operators to correctly handle integer type differences when converting from PostgreSQL to Snowflake.

#### General

- Updated Snowflake authentication to be handled directly through the IConnectionResolver, utilizing the provided connection when available.
- Implemented data validation improvements.

### Fixes

#### SSIS

- Resolved a styling issue affecting cards in the ETL SSIS Report.
- Fixed an issue where the “Check dependencies” button in the ETL SSIS Report was not functioning.

#### General

- Corrected the architecture name used for macOS Intel installers.
- Removed the access code requirement and implemented a direct redirect to the login page.
- Added source system text and corrected color display.

## Version 2.2.7 (Jan 22, 2026)

### Improvements

#### General

- Cached the VS Code path to improve performance.
- Updated connection redirection to fetch the last used credentials.

### Fixes

#### Oracle

- Added support for the `NULLIF` function to trim transformations for Oracle.

#### Redshift

- Fixed the RedShift connection handling for the default port and removed duplicated authentication method input.

#### SQL Server

- Fixed an issue where `JSON_UDF.sql` was not being deployed for SQL Server.
- Fixed integer divisions to correctly use truncation for SQL Server.

## Version 2.2.6 (Jan 21, 2026)

### Improvements

#### General

- Implemented renaming in testing mode and on the verify button.
- Changed the name of “AI Verification” to “AI Code Conversion”.
- Created data models for selector commands and refactored the TopLevelCodeUnits reader.
- Added `useUserMetadata` to set user metadata for telemetry.
- Replaced temporary credentials with active credentials across the application.
- Added the `useCredentialStorage` hook for managing credential IDs in local storage.
- Added a host URL input field to the Snowflake Connection Form.
- Added an AI Verification disclaimer.
- Added pre-extraction checks for the Code Extraction command, including a source connection test.
- Added collation support to code extraction.
- Added a Technical Discovery section.

### Fixes

#### Redshift

- Changed the `WITH NO SCHEMA BINDING` transformation to always remove it for Redshift conversions.

#### SQL Server

- Fixed an issue with `SELECT` statements containing a variable in the `TOP` clause for SQL Server conversions.

#### Teradata

- Removed the `NEXT` keyword in fetch next statements for Teradata conversions.

#### General

- Fixed an issue where procedures and views were not marked as verified by the user.
- Fixed an issue in two-sided validation.
- Fixed path validation when autocompleting.
- Implemented UI fixes for the “Use the extraction script” section.
- Fixed an issue with temporary tables having an incorrect schema.

## Version 2.2.5 (Jan 16, 2026)

### New Features

#### Hive/Spark/Databricks

- Added `DATE_SUB` function replacers.

#### PostgreSQL

- Added an arrange option for routines with quoted definitions.
- Added preprocessing for single-quoted procedure bodies.

#### Teradata

- Added support for `.IMPORT` and `.SET` commands in Mload.

#### SSIS

- Added an ETL SSIS Report.
- Enhanced variables conversion with improvements and refactoring.

#### Power BI

- Added support for column renaming in embedded SQL cases.

#### General

- Implemented project input validations.
- Added user metadata to telemetry upon login.
- Added list, cancel, and status commands for AI Verification.
- Added an initial Login Page with enhanced licensing features.
- Added support for AI Verification contracts.
- Added transformation of SQL code within `dbt_project.yml` variables.

### Improvements

#### SQL Server

- Improved the transformation of the `ROW` keyword as a reserved keyword.
- Removed unnecessary commas from Transact-SQL transformation output.

#### Teradata

- Updated the collation conversion setting to align with the tool’s new default behavior.
- Updated current collation support to ensure compatibility with Iceberg Tables transformations.
- Removed CREATE STAGE and PUT commands from the EXECUTE IMMEDIATE block in Mload transformations.

#### General

- Improved AI Verification status reporting.
- Improved consistency of capitalization in Settings tabs.
- Consolidated the definition of source languages that support database connections for an improved end-to-end flow.
- Updated the code extraction command to enhance object type handling and improve progress reporting.
- Refactored the Translation API and implemented logic for Mapplet CTE generation.
- Refactored SQL transformation for variables.
- Added a Mapplet CTE Builder Module.

### Fixes

#### SQL Server

- Fixed an issue with the `coalesce` function for integer types when an empty string was present.

#### General

- Corrected an issue where AI verification results were not showing two-sided comparisons.
- Removed Etl instrumentation argument.
- Added null validation to the RAISERROR helper parameters.

## Version 2.2.2 (Jan 13, 2026)

### Improvements

#### General

- SQL Server extraction process now adds ‘GO’ statements after `USE database` commands in object definition files to allow files to be executable.
- Metadata extraction now intelligently focuses on extracting only supported object types for each specific platform.
- Improved conversion settings and disabled action buttons when a conversion status is pending (e.g., during AI verification).
- Added a ConnectionInfoBanner component to clearly display saved connection information.
- Refactored credential management by removing secret handling methods and simplifying connection processes.
- Introduced a database dropdown in data migration and validation screens and removed unnecessary required fields in connection configurations.
- Updated an internal dependency from ‘balto’ to ‘stellar’.
- Enhanced internal utilities for managing test results and progress.

## Version 2.2.1 (Jan 08, 2026)

### New Feature

#### General

- The Missing Object Report has been merged into Object References, streamlining reporting. This unifies both valid and missing object references in a single report.

### Improvements

#### General

- Implemented a mechanism to parse and modify `.toml` files for credentials for Snowflake and various source languages.

## Version 2.2.0 (Jan 07, 2026)

### New Features

#### General

- Implemented initial code unit state management using JSON files.
- Added a new JobStorageService.
- Implemented AI verification server and interfaces.
- Added support for identity columns in table definition queries.
- Added required credentials configuration for the Data Migration Connection Page and updated the Data Validation Connection Page to include KeyPair as a supported authentication method.
- Migrated AI Verification to the new jobs infrastructure and services.
- Added models for the AI Verification job.
- Defined reader and writer components for TOML files.

### Improvements

#### General

- Updated the VersionInfoProvider to strip branch and commit hash from the version string.
- Added a missing singletons registry for dependency injection.
- Made the `reportFilePath` optional in `CodeUnitConversionProgress`.
- Moved the `SpcsManager` and its dependencies to the Databases project for better organization.
- Implemented an AI verification orchestrator.
- Refactored credential management methods to utilize `CreateOrEditCredentials`.
- Updated conversion status in other features when verified by a user.
- Removed AI Verification v1.
- Enhanced password input fields to prevent overflowing.
- Refactored AI Verification to use `CredentialsId` instead of `ConnectionString`.
- Improvements in the deploy command.
- Updated application version retrieval to use semantic versioning.

### Fixes

#### Teradata

- Fixed parenthesis issues that caused incorrect `PARTITION BY` generation for Iceberg table transformations in Teradata.

#### General

- Fixed SSO URL handling in Snowflake credentials configuration.
- Addressed minor issues related to AI verification.
- Fixed relative paths in AI verification job execution and application state management.

## Version 2.1.0 (Dec 18, 2025)

### New Features

#### IBM DB2

- Implemented DECFLOAT transformation.

#### Oracle

- Added support for transforming `NUMBER` to `DECFLOAT` using the [Data Type Mappings](../../getting-started/running-snowconvert/conversion/oracle-conversion-settings#data-type-mappings) feature.
- Added a new report [TypeMappings.csv](../../getting-started/running-snowconvert/review-results/reports/type-mappings-report) that displays the data types that were changed using the Data Type Mappings feature.

#### Power BI

- Added support for the Transact connector pattern for queries and multiple properties in the property list for PowerBI.

#### Teradata

- Added a new conversion setting [Tables Translation](../../getting-started/running-snowconvert/conversion/teradata-conversion-settings#table-translation) which allows transforming all tables in the source code to a specific table type supported by Snowflake.
- Enabled conversion of tables to Snowflake-managed Iceberg tables.

#### SSIS

- Added support for full cache in SSIS lookup transformations.

#### General

- Added temporary credentials retrieval for AI Verification jobs.
- Added summary cards for selection and result pages.
- Implemented full support for the Git Service.
- Added ‘verified by user’ checkboxes and bulk actions to the selection and results pages.
- Added a dependency tag for AI Verification.
- Implemented the generation of a SqlObjects Report.

### Improvements

#### Redshift

- Optimized RedShift transformations to only add escape characters when necessary in `LIKE` conditions.

#### SSIS

- Improved Microsoft.DerivedColumn migrations for SSIS.

#### General

- Added the number of copied files to relevant outputs.
- Changed some buttons to the footer for improved UI consistency.

### Fixes

#### Teradata

- Fixed transformation of bash variables substitution in scripts.

## Version 2.0.86 (Dec 10, 2025)

### Improvements

#### Redshift

- Added support for the `MURMUR3_32_HASH` function.
- Replaced Redshift epoch and interval patterns with Snowflake `TO_TIMESTAMP`.

#### SSIS

- Added support for converting Microsoft SendMailTask to Snowflake SYSTEM.
- Implemented SSIS event handler translation for `OnPreExecute` and `OnPostExecute`.

#### SQL Server

- Enhanced transformation for the `Round` function with three arguments.

#### General

- Enhanced procedure name handling and improved identifier splitting logic.
- Improved object name normalization in DDL extracted code.
- Implemented a temporal variable to keep credentials in memory and retrieve the configuration file.
- Updated the TOML Credential Manager.
- Improved error suggestions.
- Added missing path validations related to ETL.
- Improved the application update mechanism.
- Implemented an exception to be thrown when calling the `ToToml` method for Snowflake credentials.
- Changed the log path and updated the cache path.
- Implemented a mechanism to check for updates.
- Merged the Missing Object References Report with ObjectReferences.
- Changed values in the name and description columns of the ETL.Issues report.
- Added support for Open Source and Converted models in AI Verification.
- Added a new custom JSON localizer
- Added a dialog to appear when accepting changes if multiple code units are present in the same file.
- Added a `FileSystemService`.
- Added an expression in the ETL issues report for `SSISExpressionCannotBeConverted`.

### Fixes

#### SQL Server

- Fixed a bug that caused the report database to be generated incorrectly.
- Fixed a bug that caused unknown Code Units to be duplicated during arrangement.

#### General

- Fixed an issue that prevented the cancellation of AI Verification jobs.
- Fixed an issue to support EAI in the AI specification file.
- Fixed an issue where the progress number was not being updated.
- Fixed the handling of application shutdowns during updates.

## Version 2.0.57 (Dec 03, 2025)

### Improvements

#### SQL Server

- Enhanced SQL Server code extraction to return schema-qualified objects.

#### General

- Enhanced Project Service and Snowflake Authentication for improved execution.
- Removed GS validation from client-side, as it is now performed on the server side.
- Implemented connection validation to block deployment, data migration, and data validation when a connection is unavailable.
- Enhanced conversion to use the source dialect from project initialization.
- Improved `CodeUnitStatusMapper` to accurately handle progress status in UI status determination.
- Implemented batch insert functionality for enhanced object result processing.

### Fixes

#### General

- Resolved an issue where conversion settings were not being saved correctly.
- Corrected data validation select tree to properly skip folders.
- Fixed content centering issues in the UI.
- Normalized object names in AI Verification responses to prevent missing status entries in the catalog.

## Version 2.0.34 (Nov 27, 2025)

### Improvements

#### General

- Resolved an issue where PowerBI was not correctly displayed in the list of supported languages.

## Version 2.0.30 (Nov 26, 2025)

### New Features 🚀

#### IBM DB2

- Added transformation support for SELECT INTO and VALUES statement for variable assignments within User-Defined Functions (UDFs).

#### Oracle

- Added transformation support for SELECT INTO for variables assignments within User-Defined Functions (UDFs).

#### SQL Server

- Added transformation support for SELECT INTO for variables assignments within User-Defined Functions (UDFs).

#### SSIS

- Added support for SSIS Event Handlers.

#### General

- Introduced AI Verification Contract Model Codes.
- Created a base component for the Code Processing View.
- Implemented YAML reading and writing services with an enhanced `info` command.
- Created an execution type selector page.

### Improvements

#### General

- Updated GS Version to 9.50.99 to ensure compatibility with newer versions of GS.
- Expanded job storage test coverage across data validation, migration, deployment, extraction, metadata, and AI verification.
- Refactored the FilteredObjectExplorer layout and removed unnecessary container styles from the AI Verification Selection Page and Mappings Page to improve UI consistency.
- Enhanced deployment database selection.

### Fixes

#### SQL Server

- Resolved an error that occurred when parsing SQL Server connections with a specific port.

#### General

- Resolved an issue where mappings were not functioning correctly in code conversion.
- Corrected the process for cleaning the conversion directory before conversion.
- Fixed deployment dropdown functionality.

## Version 2.0.8 (Nov 21, 2025)

### Improvements

#### Teradata

- Added support for `GOTO-LABELS` in SnowScript.

#### Spark SQL

- Added support for transformation rules to handle `INSERT OVERWRITE` statements.

#### SQL Server

- Added support for the `CREATE SEQUENCE` statement.

#### General

- Added support for IBM Db2 from the UI.
- Fixed Db2 support in SourceDialect and Update Conversion settings window.
- Added support for tables with large numbers of rows (> 2.5B) in data migrator.

## Version 2.0.0 (Nov 20, 2025)

The SnowConvert AI interface is revised to improve efficiency, control, and usability.
In the improved interface, you can run specific flows independently, including extraction, deployment, and
data validation. There is now a dedicated project page to show you which flows you can run. The improved
interface gives you more granular control over your project and makes managing complex workflows easier.

For more information, [SnowConvert AI: Project Creation](../../user-guide/project-creation)

## Version 1.21.0 (Nov 08, 2025)

### Improvements

#### SQL Server

- Added support for the CREATE SEQUENCE statement.

#### General

- Added a notification to inform users about the SnowConvertAI 2.0 New UI experience.

## Version 1.20.11 (Nov 07, 2025)

### Improvements

#### Redshift

- Added support for the `CURRENT_SETTING` timezone.

#### Spark SQL

- Added support for `INSERT BY NAME` and removed the `TABLE` keyword and partition clause.

#### Power BI

- Supported dynamic parameterization in connectors with embedded queries in WHERE clauses.

## Version 1.20.10 (Nov 06, 2025)

### Improvements and Fixes

#### Redshift

- Added support for HLL functions.
- Added support for JSON functions.
- Added support for OBJECT\_TRANSFORM.

#### SSIS

- Added conversion support for SSIS Microsoft.ExpressionTask.
- Modified the condition used to determine if an SSIS package is reusable.

#### Teradata

- Added support for named arguments in the EXECUTE (Macro Form) statement.
- Fixed an issue where scripts were not being migrated to Snowscript.
- The Continue Handler is now available for Scripts.

#### PostgreSQL

- Fixed an issue where procedures did not have the EXECUTE AS CALLER clause generated by default when the SECURITY clause was absent in the input.

#### Redshift

- Fixed an issue where non-ASCII characters in columns were not quoted during data migration.

#### SQL Server

- Fixed an issue where default GETDATE column constraints applied an unnecessary double cast in the column definition.

## Version 1.20.8 (Nov 05, 2025)

### Improvements

#### General

- Added support for alert preview notifications.
- Improved Claude model validation to inform users about required access.

## Version 1.20.7 (Oct 31, 2025)

### IBM DB2 Stored Procedures & User-Defined Functions Support

SnowConvert AI now supports the conversion of DB2 stored procedures to Snowflake equivalents, enabling seamless migration of procedural code. This feature includes support for variable operations and control flow statements. Also, DB2 user-defined functions will be converted to Snowflake Scripting UDFs when possible.

### New Features 🚀

#### SSIS

- Implemented SSIS to Snowflake string literal escape sequence conversion.

### Improvements

#### Teradata

- Updated scripts transformation to utilize a `continue` handler.

#### General

- Cleaned up `package.json` for customer distribution.

### Fixes

#### BigQuery

- Fixed an aggregation issue that occurred when column aliases had the same name as table columns.

#### Oracle

- Fixed `NOT NULL` constraint behavior with `INLINE`, `CHECK`, and `PK` constraints.

#### SSIS

- Fixed an issue where comment tags were not displayed in converted reusable packages.

#### General

- Updated database dependencies and resolved dependencies vulnerabilities.

## Version 1.20.6 (Oct 29, 2025)

### New Features 🚀

#### SSIS

- **SSIS Replatform migration (Public Preview)** - SnowConvert AI now supports SSIS package migration to Snowflake in Public Preview, enabling automated conversion of SSIS workflows to modern cloud-native data pipelines.

#### BigQuery

- Added support for the `JSON_TYPE` built-in function.
- Added support for the `SAFE.POW` function.
- Added transformation for array slice patterns.
- Added more array pattern support.

#### IBM DB2

- Added support for `CONTINUE HANDLER`.

#### Oracle

- Added support for the `PARTITION` clause in `MERGE` statements.

#### Redshift

- Added support for `CONTINUE HANDLER`.

#### Teradata

- Added support for `CONTINUE HANDLER`.

#### Power BI

- Added the `HierarchicalNavigation` flag as an optional parameter in native connectors.

### Improvements

#### Oracle

- Enhanced arithmetic operations with `TIMESTAMP` values.

#### SSIS

- Enhanced the UI for the SSIS Replatform Public Preview release with improved user experience and workflow optimization.

#### General

- Removed the SSC-EWI-0009 warning from non-literal expressions and added FDM instead.
- AiVerification - Added support for `n_tests` parameter in configuration file.

### Fixes

#### BigQuery

- Fixed an issue where UDF files were not generated.

#### General

- Fixed an issue where symbols were not loaded in views and set operations.

## Version 1.20.3 (Oct 20, 2025)

### Fixes

#### General

- Fixed incorrect verified objects count calculation during validation process.
- Updated warehouse validation error messages to maintain consistency with connector messaging.

## Version 1.20.2 (Oct 20, 2025)

### New Features 🚀

#### BigQuery

- Added support for `REGEXP_EXTRACT_ALL` and `ROW_NUMBER` built-in functions.
- Added support for the `ARRAY` built-in function.

### Improvements

#### SQL Server

- Migrated `XACT_STATE` to `CURRENT_TRANSACTION`.
- Enabled `ROLLBACK` transformation within explicit transactions.

#### Power BI

- Improved the ‘Pending Work Description’ on repointing reports.

### Fixes

#### BigQuery

- Fixed an issue where literals inside `IN UNNEST` were not being transformed.
- Fixed `SAFE_CAST` behavior when the input type is not `VARCHAR`.

#### General

- Fixed queries containing aggregate functions and multiple columns.

## Version 1.20.1 (Oct 16, 2025)

### New Features 🚀

#### BigQuery

- Added support for the `REGEXP_REPLACE` function.
- Added support for the `FORMAT` function with the `%t` argument.
- Added support for the `BYTE_LENGTH` function.
- Added support for the `TIMESTAMP_TRUNC` function.

### Improvements

#### Teradata

- Improved the preservation of default values in `SELECT INTO` statements for empty results.

#### Power BI

- Improved M-Query source retrieving from metadata files.

### Fixes

#### Power BI

- Fixed an issue where the parameter list was not read correctly when the connection pattern was rejected.
- Added description in ETLAndBiRepointing assessment report when non-database or non-applicable connectors are unmodified.

## Version 1.20.0 (Oct 15, 2025)

### New Features 🚀

#### BigQuery

- Added support for `TimestampDiff`, `Safe_Divide`, and `Except` functions.
- Added support for the `ARRAY_AGG` function.
- Added the `UNNEST` built-in symbol.
- Added support for the `UNIX_SECONDS` built-in function.
- Added support for `UNIX_MILLIS` and `UNIX_MICROS` built-in functions.
- Added support for `ARRAY_CONCAT`, `TIMESTAMP_MILLIS`, and `ENDS_WITH` functions.
- Added support for `JSON_QUERY`, `JSON_EXTRACT`, `JSON_QUERY_ARRAY`, and `JSON_EXTRACT_ARRAY` functions.

#### Teradata

- Added support for `.REMARK` in SnowScript.

#### SSIS

- Implemented SSIS ForEach File Enumerator translation logic.

#### Tableau

- Added repointing assessment for Tableau repointing.

#### General

- Added support for the MD5 function.

### Improvements

#### Teradata

- Commented out ERROR LEVEL in BTEQ.

#### SSIS

- Enhanced identifier sanitization for SSIS.
- Improved retrieval of the “CopyFromReferenceColumn” property for output columns in SSIS Lookup.

#### General

- Added account information to AiVerification logs.
- Added warehouse validation to the Snowflake login.
- Wrapped control variable values with `TO_VARIANT` in `UpdateControlVariable` calls.
- Refactored SQL task creation to use `CREATE OR REPLACE` syntax.
- Added `INSERT...SELECT` with `TO_VARIANT` for control variables.
- Added transformation for string case-insensitive comparisons.

### Fixes

#### General

- Fixed name collisions of tasks in the main control flow with container tasks.
- Fixed “No expression translation for negative numbers (or unary ‘minus’)” issues.

## Version 1.19.7 (Oct 10, 2025)

### New Features 🚀

#### BigQuery

- Support was added for the `TO_HEX` and `ARRAY_TO_STRING_FUNCTION`.

#### Oracle

- SnowScript UDF is now generally available.

#### SQL Server

- SnowScript UDF is now generally available.

#### General

- A feature flag was added to hide additional options for the AiVerification API.
- An interface was added to Abstract Syntax Trees (ASTs) for representing string comparisons.
- Partial support was added for the `ARRAY_CONCAT_AGG` function.
- Support was added for the `REGEXP_EXTRACT` function.
- Transformation support was added for the `UNNEST` function within an `IN` predicate.
- Support was added for the `NET.IPV4_TO_INT64` function.

### Improvements

- The maximum GS version was bumped to 9.37 to extend the period of SC usage until the end of October.
- The `TSqlNotSupportedStatementReplacer` rule is now bypassed when processing ETL SQL fragments.
- Predecessor name generation now uses the SSIS package file name.

### Fixes

- The verified objects count issue was resolved.

## Version 1.19.6 (Oct 08, 2025)

### New Features 🚀

#### SSIS

- Added core foundation for ForEach File Enumerator.
- Added base infrastructure for Dynamic SQL.
- Added cursor-based iteration structure for SSIS ForEach Loop containers.
- Added dynamic SQL support for SSIS Execute SQL Task.

#### Oracle

- Added support for the BigQuery UNNEST operator.
- Added support for JSON\_VALUE\_ARRAY built-in function.
- Added support for multiple built-in functions.
- Added support for TIMESTAMP\_SECONDS.
- Added support for SnowScript UDF.

#### SQL Server

- Added TSqlSetIdentityInsertReplacer to handle SET IDENTITY\_INSERT in Transact.

#### General

- Added AI Verification PuPr Followup items.
- Added ‘connection’ element in Tableau repointing.
- Added semicolons to execute SQL task statements inside containers.
- Added transformation for NET.SAFE\_IP\_FROM\_STRING function.
- Added support for HLL\_COUNT.MERGE function.
- Added support for NET.IP\_NET\_MASK function.
- Added ETL Preprocess Task.
- Added transformation for HLL\_COUNT.INIT function.
- Added support for offset array accessor function.

### Improvements

- Added serialization and deserialization of query symbols in the migration context.

### Fixes

#### Teradata

- Fixed issues related to CAST formats.

#### Oracle

- Fixed an issue where supported formats were incorrectly marked as unsupported.
- Fixed a bug related to symbol key creation.

#### General

- Fixed an issue with symbol key creation when loading symbols with context.
- Fixed an issue with quotes and value length in Tableau repointing.

## Version 1.19.5 (Oct 03, 2025)

### New Features 🚀

#### General

- Added support for Snowflake select asterisk column expressions.

#### SSIS

- Added support for converting CAST expressions.

### Improvements

#### General

- Enhanced the SnowflakeLogin method to handle email users correctly.
- Moved the Declare Statement Replacer to SQL.

### Fixes

#### SSIS

- Fixed an issue where SSIS containers BEGIN END without a semicolon.

#### Oracle

- Fixed an issue with incorrect function transformation.
- Fixed an issue where SYS\_REFCURSOR was not being migrated correctly.

#### dbt

- Fixed an issue with conditional split downstream ref() calls.

## Version 1.19.4 (Oct 1, 2025)

### New Features 🚀

#### Power BI

- Expanded test scenarios for Teradata Power BI repointing.

#### SSIS

- Introduced support for the SSIS Merge Join transformation.
- Implemented orchestrator task variable wrappers for SSIS tasks.

#### Teradata

- Ensured script files are now correctly reported as code units when Snowscript is the target.

#### Oracle

- Implemented a warning system for users when a referenced datatype might be unsupported.
- Renamed `RAISE_MESSAGE_UDF.sql` to `RAISE_MESSAGE.sql` for clarity and consistency.

#### SQL Server

- Added parameters as an identifier for improved recognition.

#### dbt

- Relocated configuration files to the ETL output directory and removed analyses and snapshots folders from dbt projects.

#### General

- Added transformations for BTEQ labels to support nested procedures.
- Enabled result binding for the Execute SQL Task.
- Included Migration ID in object tagging and relevant reports for enhanced telemetry.
- Reduced the frequency of the AI Verification prompt.

### Improvements

#### Oracle

- Enhanced the conversion process for `%TYPE` declarations.
- Refactored DB2 variable declarations for improved consistency.

#### General

- Improved collision detection and resolution mechanisms for ETL transformations.

### Fixes

#### Oracle

- Resolved an issue where `RAISE_MESSAGE_UDF.sql` was incorrectly referenced in PostgreSQL tests.
- Addressed a problem where EWI (Error Warning Information) was not being added to unresolved types in Oracle.

#### General

- Improved error handling and logging within the `AiVerificationHttpClient`.

## Version 1.19.3 (Sep 29, 2025)

### Improvements

#### General

- Enhanced VerifiedTemplate to better manage child verification states.

### Fixes

#### General

- Fixed an issue where the role was not being propagated correctly to the login endpoint.
- Fixed an issue where ZIP files created in Windows did not preserve proper Unix permissions.

## Version 1.19.2 (Sep 26, 2025)

### New Features 🚀

#### Power BI

- Added support for dynamic or custom concatenation for greater flexibility in data transformations.

#### SSIS

- Implemented the core infrastructure for recursive conversion of SSIS containers (e.g., `For Loop`, `Foreach Loop`), enabling the processing of more complex structures.

### Improvements

#### SSIS

- Completed the implementation of inlined conversion for containers to better handle control flows.

#### Teradata

- Reordered UDFs and updated the default time format (`HH:MI:SS.FF6`) to improve conversion compatibility.

#### dbt

- Removed angled brackets (`<>`) from generated YML configuration files to prevent potential syntax errors.
- Removed unnecessary tags from models generated during ETL conversions to produce cleaner code.
- Simplified the names of generated models in ETL conversions to enhance project readability.

### Fixes

#### PostgreSQL

- Resolved an error in the `RAISE_MESSAGE_UDF` when it was called with only two parameters.

#### General

- Updated SQLite storage filename to include file extension for better file management.
- Corrected an issue in the `TRANSFORM_SP_EXECUTE_SQL_STRING_UDF` helper where `datetime` values were formatted incorrectly in dynamic SQL.
- Applied internal fixes related to Nuget package management.
- Corrected an incorrect enumeration in an internal resource file (`IssueResources.json`).

## Version 1.19.0 (Sep 24, 2025)

### New Features 🚀

#### General

- Added support for IDENTITY in CTAS statements.
- Enhanced telemetry settings in data migration configuration for improved metrics collection control.

#### Tableau

- Added initial infrastructure for converting Tableau projects.

#### ETL & SSIS

- Implemented new output structure for ETL conversions, grouped by filename.
- Added support for ISNULL function conversion and variables in “Derived Column” expressions.
- Enhanced SSIS assessment report and task generation using original package names.

#### DB2

- Added support for DECLARE TABLE statement transformation.

#### BigQuery

- Added support for REGEXP\_CONTAINS function.

#### dbt

- Refactored dbt project generator to unify variable conversion logic.

### Fixes

#### Power BI

- Fixed CommandTimeout parameter and schema uppercase conversion issues.

#### SSIS

- Fixed critical bug with plus operator (+) on numeric operands.

#### General

- Corrected conversion rate calculation.
- Enhanced DROP TABLE handling and COALESCE type resolution.
- Removed conversion of On Commit Preserve Rows node for Teradata.

## Version 1.18.3 (Sep 22, 2025)

### Fixes

- Improved the refresh deployment catalog functionality in the end-to-end experience.
- Fixed navigation issues with the Retry Conversion flow.

## Version 1.18.0 (Sep 18, 2025)

### New Features 🚀

#### PuPr AI Verification

- Added new [AI Verification](../../../../snowconvert-docs/snowconvert-ai-verification) step for SQL Server migrations.

#### SQL Server

- [Preview Feature] Support for UDF translation to [Snowflake Scripting UDFs](../../../../../developer-guide/udf/sql/udf-sql-procedural-functions)
- Support for `ERROR_NUMBER` to `SQLCODE`.
- Support for `COL_LENGTH` built-in function.

#### Teradata

- Support for the `TD_MONTH_BEGIN`, `TD_WEEK_BEGIN`, and `TD_WEEK_END` built-in functions.
- Support for hex literals in the `OREPLACE` built-in function.

#### Oracle

- Support `ASCIISTR` built-in function.
- Support for `MAX DENSE_RANK FIRST` and `MIN DENSE_RANK LAST` clauses.

#### SSIS

- Added SSIS Microsoft.Merge transformation
- Enhanced SSIS variable handling transformation

### Fixes

#### Oracle

- Improved recognition of correlated queries.

## Version 1.17.6 (Sep 5, 2025)

### Fixes

- Fixed crashes in code conversion on SnowConvert classic mode.

## Version 1.17.2 (Sep 4, 2025)

### Fixes

- Fixed visual issues in the object selection screen.

## Version 1.17.1 (Sep 1, 2025)

### New Features 🚀

#### General

- [IBM DB2 SQL Support](../../getting-started/running-snowconvert/supported-languages/ibm-db2)  
  SnowConvert AI now supports the conversion of Tables and Views to Snowflake. This feature includes support for the following:

  - Translation of [Tables](../../../translation-references/db2/db2-create-table).
  - Translation of Views.
  - Translation of [Data Types](../../../translation-references/db2/db2-data-types).
  - Translation of Built-in Functions.
- Added new columns to [Top Level Code Unit report](../../getting-started/running-snowconvert/review-results/reports/top-level-code-units-report): Code Unit Database, Code Unit Schema and Code Unit Name

#### PostgreSQL & Based Languages

- Support for Bitwise Functions

### Fixes

#### General

- Modified [SSC-EWI-0040](../../technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0040) to specify the error node.

#### Teradata

- Removed .SET FORMAT from BTEQ transformation
- Fixed several BTEQ parsing errors
- Added support for BTEQ `.MESSAGEOUT` command
- Added pending transformation for shell variables inside conditions
- Added support for BTEQ `.SET FOLDLINE` command
- Added transformation for `.SET TITLEDASHES` command
- Downgraded EWI to FDM for `STATISTICS` BTEQ clause
- Downgraded EWI to FDM for `PERIOD` BTEQ clause

#### Oracle

- Fix transformation for DATE type attribute

#### SQL Server

- Improved the handling of procedures containing `SELECT INTO` statements that return a query.
- Transform `@@DateFirst` to `GET_WEEK_START`
- `Numeric format` function support
- `Convert` function support
- `Datename` function support
- Removed the symbol `@` in the conversion that uses XML queries.
- `Print` statement support
- Formats for datetime support.
- Improved the update statement by removing the table name from the clause when it appears in the target table.
- Error functions translation support.

## Version 1.16.2 (Aug 19, 2025)

### New Features 🚀

#### General

- Added a [new report](../../getting-started/running-snowconvert/review-results/reports/functions-usage-report), SQLFunctionsUsage.csv, that summarizes the invocations of built-in and user-defined functions grouped by their migration status. This report allows users to get details about function usages, whether they were transformed to Snowflake with no problem, or whether they require an additional post-conversion action.

#### Teradata

- Added transformation for the period `CONTAINS` clause

### Fixes

#### Oracle

- Fixed the `GENERATED ALWAYS` AS expr column option not being transformed
- Fixed dynamic SQL code strings not having their literal values properly escaped in the output

#### SQL Server

- Fixed the `DATETIME2` datatype not transformed correctly when precision is specified
- Fixed object names without brackets not being renamed when using the renamed feature
- Promoted SSC-FDM-TS0015 to EWI [SSC-EWI-TS0015](../../technical-documentation/issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0015) to fix objects with unsupported datatypes incorrectly marked as successfully transformed
- Fixed some virtual columns transformed to datatype `VARIANT` instead of the right datatype for their expression
- Implemented transformation for the `STRING_SPLIT` function, previously being left as is in the output code
- Fixed `CREATE FUNCTION` bodies not generated when a `SELECT` statement was found in the `ELSE` clause of an `IF` statement
- Fixed identifiers containing the `@` character producing parsing errors
- Fixed the `DATE_PART` function incorrect transformation when the weekday part is specified
- Fixed the empty statements generated by parsing error recovery causing a pending functional equivalence error to be reported
- Fixed the `DATENAME` function transformation not generating the necessary UDF definitions in the `UDF Helpers` folder
- Fixed the `TRY_CAST/TRY_CONVERT` functions not being transformed in some cases

## Version 1.16.1 (Aug 11, 2025)

### New Features 🚀

- Added Key Pair authentication to login to Snowflake.
- Upgraded data validation Python support to 3.13.

## Version 1.16.0 (Aug 8, 2025)

### Fixes

- Fixed issue with retrieving access codes from SnowConvert due to certificate handling problems.
- Added Data Validation manual execution instructions and scripts.

## Version 1.15.1 (Aug 6, 2025)

### New Features 🚀

- Added support for PostgreSQL Array Expression and Array Access.

### Fixes

- Fixed transformation for Oracle’s JSON\_OBJECT function.
- Updated links to the new [official documentation site](../../../overview).
- Fixed bug when clicking on retry conversion on a non E2E platform.
- Fixed optional fields in Snowflake connection form.
- Fixed some Oracle functions not being transformed to the correct target.

## Version 1.14.0 (Jul 30, 2025)

### New Features 🚀

- Added Migration Project Context feature.

## Version 1.13.0 (Jul 28, 2025)

### New Features 🚀

- Enhanced data migration performance by increasing default timeout values for large-scale operations including data extraction, analysis, and loading processes.
- Support for [nested procedures](../../../translation-references/oracle/pl-sql-to-snowflake-scripting/README#nested-procedures) in Oracle.

### Fixes

- Routed SnowConvert AI API traffic from Azure-hosted domains (*.azurewebsites.net) to Snowflake-hosted domains (*.snowflake.com) to streamline integration and deliver a unified user experience.
- Fixed SSO authentication token caching during data migration processes, eliminating repeated authentication prompts that previously opened new browser tabs for each request.

## Version 1.12.1 (Jul 21, 2025)

### New Features 🚀

Conversion Option for External Tables for Hive-Spark-Databricks SQL.

### Fixes

- Backtick Identifiers Support in Sybase.
- Translation for Amazon Redshift COMMENT ON statement.
- Non-returning functions translated to stored procedures for PostgreSQL.

## Version 1.11.1 (Jul 11, 2025)

### New Features 🚀

Support for new Snowflake Out Arguments syntax within Snowflake Scripting on Teradata, Oracle, SQL Server, and Redshift migrations.

### Fixes

Enhanced Teradata Data Type Handling: JSON to VARIANT migration.
Improved recovery on Redshift procedures written with Python.

## Version 1.11.0 (Jul 1, 2025)

### New Features 🚀

New [Data Validation framework integration](../../user-guide/data-validation) for SQL Server End-to-End experience: Now, users can validate their data after migrating it. The Data Validation framework offers the following validations:
Schema validation: Validate the table structure to attest the correct mappings among datatypes.
Metrics validation: Generate metrics of the data stored in a table, ensuring the consistency of your data post-migration.

## Version 1.3.0 (Mar 25, 2025)

### Sybase IQ Support

SnowConvert AI now supports the conversion of Sybase IQ Create Table to Snowflake. This feature includes support for the following:

### New Features 🚀

- Sybase:
  - Translation of Regular and Temporary Tables
  - Translation of Constraints
  - Translation of Data Types

### Azure Synapse

- Fix Object References not shown in Object References and Missing Object References reports.
- Added parsing support for Materialized Views with distribution clause

## Version 1.2.17 (Mar 18, 2025)

### Azure Synapse Support

SnowConvert AI is adding support for Azure Synapse to Snowflake, now enabling direct translation for Azure Synapse SQL scripts and stored procedures to Snowflake’s SQL dialect. This complements our existing support for Transact-SQL (T-SQL) and provides a more comprehensive solution for users migrating from Microsoft’s data warehousing ecosystem.

### New Features 🚀

- **Common**:
  - Add a Relation Type column to the [Object References](../../getting-started/running-snowconvert/review-results/reports/object-references-report) and [Missing Object References](../../getting-started/running-snowconvert/review-results/reports/missing-objects-report) reports.

## Version 1.2.16 (Mar 10, 2025)

### Redshift Stored Procedures Support

SnowConvert AI now supports the conversion of Redshift stored procedures to Snowflake, enabling seamless migration of procedural code. This feature includes support for variable operations, control flow statements, cursor handling, and transaction management capabilities.

### New Features 🚀

Stored procedures new supported functionality.

- **General support**:
  - Transformation for `SELECT INTO` variables inside stored procedures.
  - Transformation for `CASE` statements without ELSE clauses.
  - Transformation of `RETURN` statement in Redshift.
  - Support of `RAISE` for logging, warnings, and exceptions.
- **Variable Binding**:
  - Support for binding variables in stored procedures.
  - Handling positional arguments for binding variables.
  - Variable bindings in the `OPEN cursor` statement.
- **Transaction Support**:
  - Initial support for `COMMIT`, `ROLLBACK`, and `TRUNCATE` statements.
- **Cursor Operations**:
  - Support for the `FETCH` statement.
  - Transformation for `refcursor variable declaration`.
- **DML Operations**:
  - Transformations for `INSERT`, `UPDATE`, `MERGE`, `SELECT INTO` statements.
- **Control Flow Statements**:
  - Support for basic control flows statements.
  - Transformations of Labels Stats against loops.
- **DDL Operations**:
  - Support for `CREATE TABLE AS` statement.

### Breaking Changes ⛓️‍💥

- Renamed Code Unit Name to Code Unit ID in Top-Level Code Units report.

## Version 1.2.6 (Feb 26, 2025)

### Oracle

- Fixed CONSTRAINT clauses incorrectly reported as parsing errors.

### Redshift

Added

- Support for **Declare** statement.
- Support for **Merge** statement.
- Support for **Update** statement.
- Support for variable declaration with **Refcursor** type.
- Support for **Declare**, **Open** and **Close** Cursor.

### Teradata

- Fixed ‘chars’, and ‘characters’ built-in functions being reported as missing references.

## Version 1.2.5 (Feb 7, 2025)

### Common

- Improved SnowConvert AI CLI help messages.

## Version 1.2.4 (Feb 7, 2025)

### Common

- Improved SnowConvert AI CLI help messages.

### Teradata

- Improved EWI consistency on DATE casting.

## Version 1.2.1 (Jan 31, 2025)

### Common

**Fixed**

- Improved mechanism to validate the SnowConvert AI license by preventing the use of the powershell current user profile settings, ensuring a smoother execution.

## Version 1.2.0 (Jan 28, 2025)

- **Free** access for anyone with a corporate email.
- **Redshift** conversion is now supported under preview.
- Removed assessment step. Assessment and conversion are now completed in only one step.
- Introduction of the new Code Completeness Score and Code Unit Methodology.
- Improved messages like Functional Difference Messages (FDMs), Performance Reviews (PRFs) and EWIs (error, warnings, and issues).

### Common

**Fixed**

- Usage of correlated scalar subqueries erroneously causing [SSC-EWI-0108](../../technical-documentation/issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0108) under certain scenarios.

### Teradata

**Fixed**

- Set **Character Set** as optional in description of columns in derived tables.

## Version 1.1.91 (Dec 19, 2024)

### Common

**Fixed**

- Correlated scalar subqueries missing an aggregate function.
- Uncorrelated scalar subqueries are being marked as unsupported.

### Teradata

#### Added

- Added “ANSI/TERA Session Mode” and “Use COLLATE for Case Specification” settings:
  - ANSI mode with COLLATE.
  - ANSI mode without COLLATE.
  - TERA mode with COLLATE.
  - TERA mode without COLLATE.
- Support parsing of GENERATED TIMECOLUMN column option.
- Support parsing of TD\_NORMALIZE\_MEET function.

#### Fixed

- Fixed inconsistencies in column names when it comes to Snowflake reserved keywords.
- Parsing errors in PARTITION BY RANGE\_N clause.
- Improved support for COALESCE expression.

### SQL Server

#### Fixed

- Some functions were incorrectly marked as a pending functional.

## Version 1.1.80 (Dec 5, 2024)

### Common

**Fixed**

- SnowConvert AI was incorrectly marking scalar subqueries as invalid when some function aliases were used.
- Crash when SnowConvert AI didn’t have read/write permissions to configuration folder.

### Teradata

#### Fixed

- Renaming feature now contemplates function with parameters.
- The UPDATE statement with ELSE INSERT syntax was not converted correctly.

### SQL Server

#### Fixed

- SnowConvert AI now successfully converts @@ROWCOUNT using the global variable SQLROWCOUNT.
- View and column names from sys objects are now be paired with INFORMATION\_SCHEMA.

## Version 1.1.69 (Nov 14, 2024)

### SQL Server

#### Fixed

- BIT Datatype with DEFAULT value is not converted to true or false but 1 or 0.

### Oracle

#### Fixed

- Code missing when converting a function with CONNECT BY.

## Version 1.1.67 (Oct 30, 2024)

### Teradata

#### Fixed

- Flag TeraModeForStringComparison is set to true as default.

### SQL Server

#### Fixed

- Columns with default value are now converted correctly with their respective data type casting.

### Oracle

#### Fixed

- Code missing when converting a function with CONNECT BY.

## Version 1.1.63 (Oct 24, 2024)

### Common

- Recovery codes removed from the parsing error messages.
- Windows close button now works as intended.
- Added a new field **domain** to the comment clause for each DDL SnowConvert AI generates.

### Teradata

**Added**

- Support for UNION ALL clause with different data types and column sizes.
- Support for sp\_executeql.

#### Fixed

- Inconsistencies in string comparison in Tera mode and ANSI mode.
- Complex column alias with syntax ‘’n is not being recognized by SnowConvert.

### SQL Server

**Added**

- FDM in every corelated subquery.

#### Fixed

- Issue with WITH DISTRIBUTION and CLUSTERED in table creation.

### Oracle

#### Fixed

- Issue that caused SP conversion to fail when using .rownum within a FOR statement.

## Version 1.1.61 (Oct 18, 2024)

### Teradata

#### Fixed

- Conversion of stored procedures inside macros is now supported.
- StringSimilarity Teradata Function is now converted successfully

### Oracle

#### Fixed

- DATEDIFF\_UDF now returns date difference with timestamp as parameter with decimals (time part difference).

## Version 1.1.56 (Oct 9, 2024)

### Teradata

#### Fixed

- Create a Stored Procedure to compliance the same flow as in Teradata (StoredProcedure inside a Macro)
- Use a UDF Helper to emulate the functionality given for a VALIDTIME column in Teradata

### Oracle

#### Fixed

- Empty Create Statement
- Return date difference with timestamp as parameter with decimals (time part difference).

## Version 1.1.54 (Oct 3, 2024)

### Common

- Improved the auto-update mechanism.

### Teradata

#### Fixed

- UDF called “PERIOD\_TO\_TIME\_UDF” is now included as part of the code output if it is used in the converted code.
- UDF called “DATE\_TO\_PERIOD\_UDF” is now included as part of the code output if it is used in the converted code.

### SQL Server

#### Fixed

- The CLUSTERED clause is no longer in the output code.

### Oracle

#### Fixed

- PARTITION clause in queries is now identified as an EWI instead of FDM.

## Version 1.1.52 (Sep 24, 2024)

### Common

- Adding an informative message when there is no communication to the licensing API and a link with more information of what is happening.
- A new column named “Lines of Code” was added on the report, specifically the “2.1 Conversion Rates Summary” table

### Teradata

#### Fixed

- Cast to CHAR/CHARACTER causing parsing error

### SQL Server

#### Fixed

- Empty STAT EWI when there is an extra ‘;’.
- Continue statement is not marked as an EWI any more.

### Oracle

#### Fixed

- `DATE_TO_RR_FORMAT_UDF` is now included on the output if there is a reference to it on the input source code.

## Version 1.1.45 (Sep 12, 2024)

### Common

Fix Encoding issue SSC-EWI-0041

#### Teradata

Added

- New conversion setting for TERA MODE strings comparison transformation

Fixed

- Anonymous block of code converted to a stored procedure.
- PRIMARY TIME INDEX not being parsed.

#### SQL Server

Fixed

- Empty stat should not be classified as pending functional
- SQL report has a text referring to Teradata

#### Oracle

Added

- Oracle function conversion to Functions (single statement)

Fixed

- DATE\_TO\_RR\_FORMAT\_UDF is added in the view conversion but is not part of the SC output

## Version 1.1.38 (Aug 29, 2024)

### Common

- Improved the performance for running SnowConvert.

#### Teradata

- Added translation for EXTRACT function.
- Fix translation in procedure when there is a presence of IMMUTABLE/VOLATILE.
- Improved translation of EXTRACT\_TIMESTAMP\_DIFFERENCE\_UDF to support timestamp as parameter.

#### SQL Server

- Improved error handling when translating long-named columns.

#### Oracle

- Added translation for STANDARD\_HASH function.
- Improved the parser to be able to read DBMS\_DATAPUMP.detach.

## Version 1.1.33 (Aug 9, 2024)

### Common

- Fixed numerous SSC-EWI-0013 occurrences.
- Improved UI experience when user does not have read/write permissions on a particular local directory.

#### Teradata

- Added translation for `PREPARE STATEMENT`, `ACTIVITY_COUNT`, `DAY_OF_MONTH`, `DAY_OF_WEEK`, `WEEK_OF_CALENDAR`, `MONTH_OF_CALENDAR`.
- Added translation for `CREATE SCHEMA`.
- Fixed `INTERVAL` literal not converted in minus operations.
- Improved parser capability to read `LATEST` as a column name.

#### Oracle

- Improved translation on PL/SQL parameter data types: VARCHAR and INTEGER.
- Fixed duplicated comments in PL/SQL procedure declarations.

## Version 1.1.26 (Jul 28, 2024)

### Oracle

- Add parsing of `ACCESS PARAMETERS` table options.
- Add parsing of `XMLType` table.
- Added translation for `FUNCTION` definition within anonymous blocks.
- Fixed duplicated code SSC-FDM-OR0045.
- Improve parsing of `XMLSchema` specification.

#### SQL Server

- Fixed `EXECUTE AS` statement wrongly transformed to `EXECUTE IMMEDIATE`.
- Fixed temporary table generated erroneously.
- Improve parsing of `WITH xmlnamespaces` statement.

## Version 1.1.16 (Jun 26, 2024)

### Teradata

- Fixed translation of `LIKE NOT CASESPECIFIC`.
- Improved translation of variable declarations inside `BEGIN…END`.
- Improved parsing of `AS OF` clause and `WITH TIE`S option from `CREATE VIEW`.

#### Oracle

- Fixed translation for columns with whitespaces in `CREATE VIEW`.
- Improved description of `SSC-EWI-OR0042`.
- Improved parsing of `ACCESSIBLE BY` clause and `SQL_MACRO` option from `CREATE FUNCTION`.
- Improved parsing of the `DECLARE` statement.

#### SQL Server

- Fixed translation of `BEGIN…END` showing pending functional equivalence.
- Added translation for `FOR XML PATH` clause.

## Version 1.1.9 (Jun 12, 2024)

### Common

- Added more info in the COMMENT clause of each object.

#### Teradata

- Added an EWI 0073 to `PREPARE` statement.
- Added `OR REPLACE` to `CREATE TABLE`

#### Oracle

- Added translation for Materialized View’s `REFRESH_MODE` property.
- Improved parsing capability to read MODEL clause and to read CREATE VIEW alternate routes.

## Version 1.1.8 (May 31, 2024)

### Common

- Added translation of Materialized View to Dynamic Tables.
- Improved CodeUnit Report to show more code units.

#### SQL Server

- Added translation of SET ANSI\_NULLS.
- Added translation of INSERT that contains a FROM Subquery + MERGE INTO pattern.

## Version 1.1.6 (May 21, 2024)

### Teradata

- Fixed translation for `Cast('POINT(x t)' As ST_GEOMETRY`
- Fixed translation of casting from one format to another.
- Fixed translation related to `DATEADD_UDF` and `TO_INTERVAL_UDF`

#### Oracle

- Improved parsing capability to read `JSON_OBJECT` and `JSON_ARRAYAGG` built-in functions.

#### SQL Server

- Improved Missing Object References report’s content.
- Improved robustness during the semantic analysis phase and translation phase.

## Version 1.1.5 (May 10, 2024)

### Common

- Provide more information and details for SSC-EWI-0001
- Improved robustness of assessment mode when providing free tables.

#### Teradata

- Improved translation related to date handling.
- Improved parsing capability to read code that contains block comments.
- Improved parsing capability to read NOT NULL column option before the data type declaration in a table.
- Improved the functionality of TIMESTAMP\_DIFFERENCE\_UDF and EXTRACT\_TIMESTAMP\_DIFFERENCE\_UDF.

#### SQL Server

- Improved translation for ALTER TABLE CHECK constraint.

## Version 1.1.4 (May 2, 2024)

### Common

- Added a new assessment report EmbeddedCodeUnitReport, for more information, please visit [here](../../getting-started/running-snowconvert/review-results/reports/embedded-code-units-report).
- Improved the TopLevelCodeUnitReport. Added four more columns: FDM Count, PRF Count, FDM and PRF. For more information, please visit [here](../../getting-started/running-snowconvert/review-results/reports/embedded-code-units-report#information-in-the-embedded-code-units-report).
- Fixed an unexpected error in creating an assessment report.

#### Teradata

- Added translation for CONTINUE HANDLER.
- Added new parsing capability for BYTE data type.
- Improved binding variable translations.

#### Oracle

- Added and improved parsing capability to read EXPLAIN PLAN statement, U-Literals and CTAS.
- Improve CURSOR translation when it has to define a cursor with object\_construct.
- Improved translation of procedure parameters avoiding deployment errors.

#### SQL Server

- Added translation for DB\_ID function.
- Added basic translation for CREATE SCHEMA.
- Added an FDM for CREATE INDEX.
- Improved ALTER TABLE translation.
