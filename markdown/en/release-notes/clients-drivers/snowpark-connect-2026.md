# Snowpark Connect for Spark release notes for 2026

Snowflake uses semantic versioning for Snowpark Connect for Spark updates.

For documentation, see [Snowpark Connect for Apache Spark](/developer-guide/snowpark-connect/snowpark-connect-apache-spark) and
[Orchestrating Snowpark Connect for Spark workloads](/developer-guide/snowpark-connect/snowpark-connect-orchestration).

## 1.42.0 (September 10, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Fix Iceberg branch-name quoting that caused SQL syntax errors on `CREATE`/`DROP BRANCH` and branch DML
- Fix correlated subquery over a reused relation losing its correlation
- Fix Iceberg `ALTER TABLE ... RENAME TO`
- Reduce query size by reusing CTEs across sibling correlated subqueries

#### New features

- Support leftover text after the pattern in legacy `to_timestamp` parsing
- Support Iceberg `CREATE BRANCH ... AS OF VERSION`
- Support Iceberg `TABLE_PROPERTIES` on `CREATE`, `CREATE TABLE AS SELECT`, and `ALTER TABLE SET`/`UNSET`
- Forward Iceberg write options to Snowflake
- Support Iceberg incremental reads on catalog-linked databases

#### Other updates

- Bump Snowpark Python dependency

## 1.41.0 (September 3, 2026)

### Snowpark Connect for Spark

#### Behavior changes

- Lower default Python recursion limit to 2000, configurable via `snowpark.connect.python.recursionLimit`

#### Bug fixes

- Speed up Iceberg `append` writes by caching table metadata
- Reject duplicate column names in an explicit CSV schema
- Prevent built-in UDFs from inheriting session imports and packages
- Improve the error when a partitioned write target is missing or not visible
- Fix JSON reads when nested struct field names are invalid identifiers

#### New features

- Support Iceberg tag DDL including `RETAIN`, bare `CREATE TAG`, and `REPLACE TAG`
- Support Iceberg write-audit-publish branch writes and `fast_forward`
- Support reading CSV and JSON from multiple paths
- Improve user-supplied schema handling for CSV and JSON reads

## 1.40.0 (August 26, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Raise errors for unsupported Delta Lake writes instead of silently creating other table types
- Forward legacy JSON and CSV date-time parsing fallback session settings
- Fix chained `mapInPandas`, `mapInArrow`, and `cogroup` with pandas UDTFs
- Make `uncacheTable` a no-op when the table is not cached
- Treat `addArtifacts()` with no paths as a no-op

#### New features

- Support Iceberg `CALL system.ancestors_of`

## 1.39.0 (August 19, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Fix Scala code bundles failing on warehouse compute with a missing JVM error
- Preserve integer and timestamp types for top-level scalar columns

#### New features

- Support calling native and externally registered Snowflake functions via config
- Support the Iceberg `.partitions` metadata table

#### Other updates

- Update bundled `spark-core` to 3.5.7 and Jackson to address security advisories
- Remove unused Spark web UI assets from bundled dependencies

## 1.38.0 (August 12, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Fix CSV and JSON stage file reads to honor user reader options and Spark session configs
- Map blank CSV/JSON column names to Spark-style `_c{i}` placeholders
- Apply strict-mode nullable schema normalization for explicit-schema CSV/JSON reads
- Fix stage file reader schema column ordering
- Fix Python UDF/UDTF imports in Native Apps to use version-stage-relative paths
- Fix `mapInPandas` and `applyInPandas` import inheritance in Native Apps
- Fix schema analysis crash on untyped array columns with integral-type emulation

#### New features

- Route CSV and JSON reads through Snowflake stage file reader TVFs when enabled
- Support Iceberg `.all_files` and `.all_delete_files` metadata tables
- Support Iceberg branch DDL (`CREATE BRANCH` / `DROP BRANCH`)
- Support Iceberg write-audit-publish branch DML and DataFrame writes
- Support `spark.addArtifact` for Python files, archives, and data files in Native Apps

## 1.37.0 (August 03, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Flatten chained `DISTINCT` `UNION` operations to avoid deep nested subqueries
- Fix structured `ARRAY` columns returned as JSON text in stored procedures
- Prefer `SNOWFLAKE_MAIN_FILE_PATH` for default notebook session name
- Route Iceberg `VERSION AS OF` tag and branch reads through `VERSION_REF`
- Fix Python UDTF and pandas UDF inlining in Snowflake Native App mode
- Cache repeated `spark.sql()` plan parsing within a single action

#### New features

- Support Iceberg `.entries`, `.data_files`, and `.delete_files` metadata tables
- Support Iceberg `.all_entries`, `.all_data_files`, and `.all_manifests` metadata tables
- Support `CREATE VERSION_TAG IF NOT EXISTS` and `AS OF TIMESTAMP` for Iceberg
- Support `DROP TABLE ... PURGE` for Iceberg tables in catalog-linked databases

#### Other updates

- Bump `snowpark-python` dependency to 1.54.0

## 1.36.0 (July 23, 2026)

### Snowpark Connect for Spark

#### Behavior changes

- Validate `get_json_object` and `json_tuple` require STRING input to match Spark

#### Bug fixes

- Fix `collect()` and `count()` failures on JDK 21 with an Arrow MemoryUtil shim
- Fix qualified column and correlated subquery resolution in `spark.sql` plans
- Return Spark-compatible columns for Iceberg `.files` metadata table
- Raise a clear error for Iceberg incremental and changelog reads on catalog-linked databases
- Fix `spark.read.text` on external S3 stages with a URL prefix
- Honor `ORDER BY` direction for windowed `collect_list` over a whole partition
- Fix deep plan recursion limit errors on large unmaterialized DataFrame pipelines
- Fail fast and surface the primary error on critical JVM warm-up failure
- Align nullability propagation for collection functions and cast coercion
- Cast non-float `nanvl` arguments to Double for String and mixed-type inputs
- Raise `ParseException` for empty SQL in passthrough mode
- Reject integral-to-binary casts in ANSI mode to match Spark
- Reduce redundant identity casts in `df.to(schema)`

#### New features

- Support Iceberg `check-nullability` and `check-ordering` write options
- Support Iceberg table properties `storage_serialization_policy`, `target_file_size`, and `max-snapshot-age.ms`
- Optimize Python UDF and UDTF execution with a native-type fast path
- Support Iceberg metadata tables `.snapshots`, `.history`, `.refs`, `.manifests`, and `.metadata_log_entries`
- Support `overwrite(condition)` on catalog-linked Iceberg tables

#### Other updates

- Allow pyarrow 14.0.x as a dependency alongside Snowpark Connect

## 1.35.0 (2026-07-16)

### Snowpark Connect for Spark

#### Behavior changes

- Reject `from_json` on structured (`ARRAY`/`STRUCT`/`MAP`) columns with a Spark-compatible `DATATYPE_MISMATCH` error (gated by a config flag)

#### Bug fixes

- Fix `CREATE FILE FORMAT` failing on stage reads when the session has no current database
- Fix `NULL - date` type inference to return an interval matching Spark
- Fix `mapInPandas` batch semantics and honor UDTF table-argument `PARTITION BY`/`ORDER BY`
- Fix `unionByName` to reject duplicate column names like Spark
- Honor `spark.sql.legacy.sizeOfNull` for `size` and `cardinality` null handling
- Honor `spark.sql.ansi.doubleQuotedIdentifiers` and raise on empty identifiers to match Spark
- Fix Iceberg table-type casing so `ALTER TABLE` correctly promotes to `ALTER ICEBERG TABLE`
- Fix crash in dynamic partition overwrite when the partition spec is unreadable
- Fix `execute_jar` JVM classpath resolution so Spark Connect client classes take precedence

#### New features

- Support Java, Scala, and Python UDFs (including UDAF and UDTF) inside Snowflake Native Apps and Data Clean Rooms
- Support `native_app` mode for the `create-jvm-sproc` generator
- Add `spark_conf` parameters and a `--conf` flag to the `execute_jar` API
- Support running Snowpark Connect in Snowflake notebooks
- Support Iceberg branch reads via `option("branch", ...)` and `spark.wap.branch` for WAP workflows
- Support Iceberg `<table>.branch_<name>` and `<table>.tag_<name>` identifiers in SQL reads
- Support `tableProperty` `comment` and `format-version` in the DataFrameWriter V2 API
- Support `mergeSchema` for V2 `overwrite` and `overwritePartitions` Iceberg writes

#### Other updates

- Allow `snowflake-snowpark-python` 1.53.x
- Update bundled `snowpark-connect-deps` packages to 3.56.6 (includes jackson-databind CVE fix)

## 1.34.0 (July 10, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Raise a Spark-compatible `AnalysisException` when a non-boolean column is used directly as a filter predicate
- Fix `ModuleNotFoundError` for `distutils` when importing Snowpark Connect on Python 3.12
- Fix invalid numeric literal errors from string-to-integer casts and string-column aggregates (opt-in via config)
- Align two-digit year (`yy`) parsing with Spark’s 2000-2099 window (opt-in via config)
- Surface the real parser error for invalid `cast` type strings instead of a misleading `struct<...>` error
- Fix `CREATE TABLE ... PARTITIONED BY` being silently dropped for catalog-linked Iceberg tables
- Fix Iceberg `insertInto` overwrite to replace rows in place without rebuilding the table definition
- Add an actionable error for `CREATE NAMESPACE` on case-insensitive catalog-linked databases (Unity and Glue)
- Return one row for a global aggregate over an empty DataFrame to match Spark
- Fix `timestamp` in DDL schema strings resolving to the wrong timestamp type
- Pass `datetime` values instead of strings to registered Python UDFs with timestamp inputs
- Fix `UNRESOLVED_COLUMN` errors for backtick-quoted column names in `stat` and `na` APIs
- Fix Python UDFs that return arrays containing timestamps
- Optimize JVM UDF execution for temporal, interval, decimal, and binary types
- Improve the error message for Iceberg SQL time travel when `spark.sql.extensions` is not set

#### New features

- Support `overwritePartitions` on Iceberg tables partitioned by `day`, `month`, `year`, or `hour` transforms
- Support Iceberg incremental reads via the `start-snapshot-id` and `end-snapshot-id` options

#### Other updates

- Upgrade bundled `jackson-databind` to 2.18.8 to address high-severity CVEs
- Pin `pandas` to `<3.0` for compatibility with PySpark 3.5.3

## 1.33.0 (July 02, 2026)

### Snowpark Connect for Spark

#### Behavior changes

- Bind the Spark Connect gRPC server to IPv4 loopback (`127.0.0.1`) by default

#### Bug fixes

- Translate the “feature not supported” error for `CREATE VIEW` on catalog-linked databases into an actionable message
- Honor `CREATE NAMESPACE IF NOT EXISTS` on catalog-linked databases
- Fix stage directory reads silently returning zero rows
- Preserve the table definition on `DataFrameWriterV2` `overwrite()` by using `INSERT OVERWRITE` instead of `CREATE OR REPLACE`
- Classify duplicate write columns as a user error instead of an internal failure
- Make external-catalog Iceberg overwrites atomic to prevent data loss on failure
- Fix `CREATE ICEBERG TABLE` failures on case-insensitive catalog-linked databases
- Fix JSON reads of `VARIANT`-typed fields
- Raise `CAST_OVERFLOW` when casting an interval to an integral type overflows
- Fix silent row loss and parallelize `repartition(n)` writes
- Fix stale temporary view state left after an explicit drop
- Restore permissive casting for struct, array, and map fields in `FAILFAST` JSON reads
- Resolve `ORDER BY` to a grouping column when a `SELECT` alias shadows it
- Fix fetching of top-level `INTERVAL SECOND` columns
- Honor `spark.sql.timestampType` in CSV schema inference
- Honor `replaceInvalidCharacters=false` as a strict opt-out on JSON reads
- Reject `partitionedBy` on standard (FDN) tables across all `DataFrameWriterV2` modes
- Add actionable errors for Iceberg metadata table queries on managed and catalog-linked tables
- Add an actionable error for nested struct schema evolution on catalog-linked Iceberg tables
- Optimize `map_from_arrays` using native server-side SQL
- Optimize `map_concat` using native server-side object merge
- Optimize `create_map` to generate a flatter query
- Optimize `to_timestamp` to eliminate redundant double parsing

#### New features

- Map `spark.sql.files.maxPartitionBytes` to the Iceberg `TARGET_FILE_SIZE` table parameter
- Support Iceberg `partitionedBy()` partition transforms (`years`, `months`, `days`, `hours`, `bucket`)
- Support casting numeric types to ANSI interval types
- Support a per-session `spark.sql.extensions` override to enable Iceberg SQL extensions (`VERSION AS OF` / `TIMESTAMP AS OF`)

## 1.32.0 (June 24, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Fix `TRY_CAST` error when appending string columns to `VARIANT` targets
- Raise error for unknown configuration parameters in `RuntimeConfig.get`, matching Spark behavior
- Eliminate VARIANT JSON serialization round-trip for JVM UDFs with primitive types, improving performance
- Prevent exponential SQL size blowup in chained integer arithmetic with overflow checking
- Eliminate Python UDF in `from_utc_timestamp`/`to_utc_timestamp` for dynamic timezone columns
- Handle `CharType(n)` and `VarcharType(n)` in type mapping, raising appropriate errors on cast
- Render whole-number Double/Float as `'980.0'` (not `'980'`) in `cast(StringType())`
- Fix `dropTempView` and `createOrReplaceTempView` to handle name conflicts with permanent views and tables
- Implement `aes_encrypt`/`aes_decrypt`/`try_aes_decrypt` using native `ENCRYPT_RAW`/`DECRYPT_RAW` for byte-level Spark compatibility
- Surface CSV column-count mismatch as an error under `FAILFAST` mode
- Accept null and numeric arguments in `to_timestamp`, `try_to_timestamp`, `to_timestamp_ltz`, and `to_timestamp_ntz`
- Fix Maven Central publishing 429 errors and GPG signing for Java client releases
- Quote column names in Iceberg DDL to handle special characters
- Use parameterized SQL in interrupt handler to prevent query injection

#### New features

- Support positional column matching for CSV reads with explicit schema and header
- Support multi-directory reads for CSV, JSON, and Parquet formats
- Handle PyArrow `large_string` and `large_binary` types in `createDataFrame`
- Preserve JSON field names instead of converting `cN`-shaped keys to positional `_cN` names
- Deduplicate duplicate and empty CSV headers like Spark (`a,b,a` becomes `a0,b,a2`)
- Honor CSV `nanValue`, `positiveInf`, and `negativeInf` options for float/double parsing
- Name telemetry spans by terminal DataFrame operation (e.g., `collect`, `show`, `saveAsTable`)
- Add caller stack details (file, line, function) to Snowflake `QUERY_TAG`
- Return full source URI from `input_file_name()` (e.g., `s3a://bucket/key`)
- Support `parse_json` and `try_parse_json` functions

#### Other updates

- Bump `snowpark-connect-deps-iceberg` to 1.0.2 (Iceberg 1.10.2, fixes GHSA-vx9q-rhv9-3jvg)

## 1.31.0 (June 18, 2026)

### Snowpark Connect for Spark

#### Behavior changes

- Validate `spark.sql.session.timeZone` and reject invalid timezone identifiers
- Require literal class and method names for `reflect` and `java_method`

#### Bug fixes

- Fix crash when a Spark config value is a Python boolean (e.g. `spark.sql.ansi.enabled`)
- Fix `modifiedBefore`/`modifiedAfter` timestamp parsing with a `Z` suffix on Python 3.10
- Restore positional column order for header-less CSV reads with 10 or more columns
- Fix `zip_with` failures on structured arrays
- Fix empty-CSV write/read round-trip to preserve the header row
- Preserve the describe-query cache across `ALTER SESSION` statements
- Support struct and array-of-struct merging in `unionByName` with `allowMissingColumns`
- Use the alias from `expr("... AS alias")` arguments as the struct field name
- Fix schema nullability corruption in `intersect` and `except` set operations
- Preserve column metadata set via `Column.alias` through projections
- Optimize CSV reads with `inferSchema=false` by skipping the full schema-inference scan
- Escape embedded single quotes in generated SQL for Java and Scala UDFs
- Reject path traversal in the `AddArtifacts` handler
- Avoid redundant Snowpark session reconfiguration when a session is reused

#### New features

- Support Hadoop-style glob paths in `spark.read`
- Prune Hive partition directories using static filter predicates
- Support `modifiedBefore` and `modifiedAfter` file read filters
- Translate Iceberg tag DDL (`CREATE TAG` / `DROP TAG`) to Snowflake `VERSION_TAG`

### Snowpark Submit

#### Bug fixes

- Harden dollar-quoting in `EXECUTE JOB SERVICE` DDL to reject specs containing `$`

## 1.30.0 (June 11, 2026)

### Snowpark Connect for Spark

#### Behavior changes

- Default `recursiveFileLookup` to `false` for Spark-compatible file reads
- Make `persist` and `cache` lazy and evict cached plans on `unpersist`

#### Bug fixes

- Fix three-valued logic handling in the `exists` higher-order function
- Enable structured type fixes at session startup
- Support `explode` and `posexplode` for semi-structured arrays
- Create persistent managed tables with `spark.catalog.createTable`
- Reuse analyzed plans to avoid redundant relation traversal
- Honor the CSV `emptyValue` read and write option
- Add `skipBlankLines` support for CSV reads
- Support multi-character CSV delimiters and escaped delimiter literals
- Preserve startup compatibility with older Snowpark Python versions
- Infer DataFrameWriterV2 Iceberg targets correctly for create modes

#### New features

- Support Iceberg tag time travel and `versionAsOf`/`timestampAsOf`
- Support Iceberg SQL `VERSION AS OF` and `TIMESTAMP AS OF`

#### Other updates

- Update Snowpark Python dependency to `1.52.0`

### Snowpark Submit

#### Bug fixes

- Register Snowpark Submit jobs in `SparkApplicationDpo`
- Add `--version` support to `snowpark-submit`

## 1.29.0 (June 5, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Preserve user-supplied CSV column names like `c0`, `c1` instead of rewriting them to `_cN`
- Fix CSV header validation with `enforceSchema=false` when `columnNameOfCorruptRecord` is set
- Fix `recursiveFileLookup` semantics for CSV, JSON, Parquet, and XML reads to match Spark
- Suppress telemetry spans for internal session setup, resource warmup, and CLD-detection queries
- Support adding nested struct columns recursively to Iceberg tables
- Collapse redundant `//` slashes in cloud and stage read paths
- Fix `from_unixtime` with string input to use truncation instead of a regex strip
- Eliminate redundant describe round-trips on the read hot path and on the V1 overwrite write path
- Honor CLD identifier rules on `DataFrameWriterV2.create`, `createOrReplace`, and `replace`
- Refresh CLD context when the session database changes at runtime
- Refresh the aggregation-function list asynchronously during session init
- Support BZ2-compressed input for parallel NDJSON scans
- Resolve filters that reference columns dropped by an earlier `select`
- Reduce SQL complexity for `pow` and `sqrt` expressions
- Normalize describe-query cache keys to reduce describe queries
- Treat empty `StructType()` as `VARIANT` on the default JSON read path
- Preserve column aliases inside lambda expressions that reference outer-scope columns
- Strip trailing slash only when joining the COPY output prefix
- Cast structured `ARRAY`, `MAP`, and `STRUCT` to `VARIANT` before `OBJECT_CONSTRUCT` in JSON writes
- Eliminate dead SQL in `pow`, `unbase64`, and `cast` expressions
- Reduce query size for `size` and `split` functions
- Remove double cast in aggregation expression resolution for `sum`

#### New features

- Added support for the `recursiveFileLookup` DataFrameReader option on file reads (`csv`, `json`, `parquet`, `text`, `xml`), including explicit `true` and `false` values. See [File I/O guide](/developer-guide/snowpark-connect/snowpark-connect-file-io#label-snowpark-connect-file-io-recursive-file-lookup).
- **Upcoming behavior change (next release):** The default for `recursiveFileLookup` when not specified will change to match Apache Spark (depth-0 listing). In 1.29.0, omitting the option retains Snowpark Connect for Spark’s prior recursive listing behavior. Set `recursiveFileLookup=true` explicitly if your workloads depend on recursive directory reads.
- Support reading the Iceberg `snapshots` metadata table
- Support Iceberg Spark SQL extensions via the new `snowpark-connect[iceberg]` install extra
- Support Iceberg time travel via `snapshot-id` and `as-of-timestamp` reader options
- Support the `format-version` table property on Iceberg `DataFrameWriterV2`
- Support `ignoreNullFields` option for JSON writes
- Optimize `str_to_map` using native SQL when delimiters are literal strings
- Optimize `schema_of_csv` and `schema_of_json` to evaluate at plan time

### Snowpark Submit

#### Bug fixes

- Load JDBC drivers through an isolated `URLClassLoader` so `--jars` and bundled-driver fat jars resolve correctly

## 1.28.0 (May 21, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Replace `stack()` Python UDTF with native `LATERAL FLATTEN` for ~6x performance improvement
- Reject incompatible Parquet timestamp schemas (string/binary to timestamp)
- Validate store-assignment types on SQL INSERT and DataFrame append under ANSI/STRICT policies
- Infer partition columns for dynamic partition overwrite when `.partitionBy()` is omitted
- Use SQL path for `getDatabase`, `databaseExists`, and `listDatabases` catalog APIs
- Fix JSON structured `infer_schema` to handle nested late-appearing keys
- Speed up Parquet `COPY INTO` with `$1:"col"` fast path when case sensitivity is disabled
- Disable redundant read-result caching for Parquet `COPY INTO` paths

#### New features

- Add opt-in Scala 2.13 support for `execute_jar` via `--scala-version` flag
- Support JSON corrupt record column (`columnNameOfCorruptRecord`) in PERMISSIVE reads
- Bridge JVM log4j2 logs to Snowflake event table for stored procedure workloads

#### Other updates

- Relax `aiobotocore` version cap and bump `snowflake-connector-python` to unblock customer CVE remediation

### Snowpark Submit

#### Bug fixes

- Validate `snowflake-workload-name` upfront with a clear error instead of failing at `EXECUTE JOB SERVICE`

## 1.27.0 (May 14, 2026)

## 1.27.0 (2026-05-14)

### Snowpark Connect for Spark

#### Behavior changes

- Strip USING-join source columns at user-visible boundaries to match Spark
- Remove `snowpark.connect.sql.identifiers.auto-uppercase` config; identifier casing now follows `spark.sql.caseSensitive`
- Drop timestamp from auto-generated session name in Spark Job History UI

#### Bug fixes

- Use `CREATE ICEBERG TABLE` syntax for Iceberg tables in catalog-linked databases
- Use `ALTER ICEBERG TABLE` for column operations on Iceberg tables
- Skip default `CATALOG` property when creating Iceberg tables in catalog-linked databases
- Validate `LIKE` / `ILIKE` escape patterns and preserve pattern type to match Spark
- Update bundled JARs with CVE fixes for Jetty (CVE-2026-2332) and Log4j (CVE-2026-34477)
- Honor per-write `partitionOverwriteMode` option for CSV, Parquet, JSON, and text writes
- Fix numeric overflow in `aggregate` and `reduce` higher-order functions caused by literal seeds
- Pass call-site input types to Python UDFs registered without explicit input types
- Strip `PRIVATE-SNOWFLAKE-SQL` marker before applying SQL passthrough config flag
- Ship `spark-sketch_{2.12,2.13}-3.5.6.jar` in `snowpark_connect_deps_2`
- Fix `YearMonthIntervalType` display rendering after connector compatibility update
- Pin `jpype1` away from broken versions on macOS arm64 to fix `pip install`

#### New features

- Support `java.time.Period` and `java.time.Duration` as Scala UDF input types
- Support `_corrupt_record` column for CSV reads in `PERMISSIVE` mode
- Add opt-in `partition_specs` column to `SHOW TABLES` for Iceberg tables
- Expose `snowpark.connect.large_query_breakdown.*` configs for tuning query complexity bounds

#### Other updates

- Drop `<4.2.0` upper bound on `snowflake-connector-python`

### Snowpark Submit

#### Behavior changes

- Ignore `connection_parameters` argument in `init_spark_session` under snowpark-submit instead of raising

## 1.26.0 (May 8, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Fix `colRegex` to handle backtick-wrapped and qualifier-prefixed patterns
- Fix `add_months` to preserve day-of-month per Spark semantics
- Fix `partitionBy` case sensitivity when `spark.sql.caseSensitive` is false
- Fix gRPC message-size error when materializing large result sets
- Fix catalog `getTable` and `listColumns` intermittent failures under load
- Fix JSON schema inference to recurse into array elements
- Honor `encoding` option for JSON writes
- Honor user-supplied `DecimalType` and `MapType` in JSON schema reads
- Optimize `bin` function using native server-side UDFs
- Reduce `inspect.stack()` overhead for better notebook performance

#### New features

- Support PERMISSIVE, DROPMALFORMED, and FAILFAST modes for JSON reads
- Support server-side structured type schema inference for Parquet and JSON
- Add stored procedure backend for running workloads on warehouse

## 1.25.0 (May 5, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Validate JSON write encoding to surface unsupported charsets eagerly
- Fix `joinWith` outer joins to return `NULL` struct for unmatched side
- Preserve generator output types in `LATERAL VIEW` alias
- Escape glob metacharacters in JSON stage paths
- Canonicalize encoding names case-insensitively for JSON reader
- Fix `BigInteger` overflow during JSON schema inference
- Normalize compression codec names case-insensitively for JSON reader
- Always treat JSON read schemas as nullable to match Spark
- Use `limit` instead of `sample` for Parquet variant schema discovery
- Anchor stage paths to prevent unintended prefix matches in stage reads
- Map Spark CSV `PERMISSIVE` mode to Snowflake `ON_ERROR=PERMISSIVE`
- Allow empty CSV files to be read without raising an error
- Treat `RESOLVED_REFERENCE_COLUMN_NOT_FOUND` as a no-op in `drop`
- Raise `COLUMN_ALREADY_EXISTS` for conflicts between `*` and aliased columns
- Honor `spark.sql.legacy.negativeIndexInArrayInsert` in `array_insert`
- Optimize `map_zip_with` using native SQL instead of a Python UDF
- Optimize `substring` and `substr` using a native Snowflake function
- Prevent temporary object name collisions in multithreaded applications
- Force nullable schemas on table creation via `CREATE TABLE AS SELECT`

#### New features

- Support the `truncate` write option to preserve table identity on overwrite
- Implicitly cast scalar types when reading JSON to match user-supplied schema
- Track nullability of grouping columns in `ROLLUP`, `CUBE`, and `GROUPING SETS`
- Propagate nullability through star (`*`) expression expansion
- Track nullability through implicit and explicit casts

## 1.24.0 (April 24, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Disable `filter_classpath_jars` at server startup
- Support UDT cast-to-string and reject invalid UDT casts
- Fix DataFrame `describe` and `summary` APIs
- Add `SUPPORTED_SCALES` guard to skip workloads at unsupported scales

#### New features

- Add Scala 2.13 equivalent JARs to dependency packages
- Add Hive partitioning implementation and limitations reference
- Remove 29 unused JARs from `snowpark_connect_deps` packages (~23 MB)
- Skip explicit structured cast when server supports implicit cast for Parquet
- Bump Snowpark dependency to 1.50.0

## 1.23.0 (April 22, 2026)

### Snowpark Connect for Spark

#### Behavior changes

- Set Parquet `useLogicalType` default to `true`

#### Bug fixes

- Fix `count()` to match Spark SQL behavior
- Relax protobuf version constraint from `<6.32.0` to `<6.34.0`
- Consistently coerce to unstructured types
- Replace `snowflake.snowpark_connect.includes` import with `pyspark.sql`
- Always use vectorized Parquet scanner; remove `useVectorizedScanner` configuration option
- Fix `regexp_extract` defaults, inline flags, and PCRE handling
- Fix SQL operator compatibility gaps
- Fix `IN NULL` semantics to match Spark behavior
- Support named persistent external stage read in XML UDTF
- Preserve UDT metadata through temp views and `toDF` renames
- Use SQL path for catalog table existence checks
- Allow star expression in the map columns aggregation

#### New features

- Implement sequence support for timestamp/date and interval types
- Add CTE session parameter
- Initialize tracking nullability of columns and complex types
- Track nullability for built-in functions across multiple expression categories
- Track nullable in `Set` command
- Add nullability to `range`
- Introduce performance regression gate in GitHub Actions

## 1.22.0 (April 18, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Fix CTE-qualified column refs in ORDER BY/WHERE/GROUP BY
- Fix `withColumn` on join key after using-style join
- Fix `fillna` raising immediately for missing subset column
- Fix case sensitive read of internal stage
- Reduce window function boundary materialization
- Preserve struct/map/array schema with empty content
- Support ON\_ERROR=CONTINUE for INFER\_SCHEMA in CSV and JSON reads
- Fix hex compile-time type dispatch
- Avoid redundant temp table creation for `read.parquet` to `saveAsTable`
- Preserve `StructType`/`MapType` in strict mode
- Case-insensitive qualifier comparison in column resolution
- Use Snowpark builtin for `CBRT` function
- Fix XML `nullValue` and whitespace handling
- Use Decimal for `DecimalType` in strict mode
- Fix `map_concat` bug
- Fix `unionByName` to handle quotes in column names and respect caseSensitive config
- Remove trailing commas from JSON test resource file

#### New features

- Snowpark Connect Java Client library to support Spark Scala and Java workloads
- Use native implementation for `ARRAY_REPEAT` and `MAP_ENTRIES`
- Use `MAP_ENTRIES` in `map_cast`
- Reduce number of queries used for VARIANT inference in `read_parquet`
- Add cross-request sub-plan cache for `map_relation`

## 1.21.1 (April 10, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Implement JSON encoding validation
- Reduce query size for functions that internally rename columns
- Relax py4j version constraints to allow for broader compatibility
- Isolate artifacts by spark session

#### New features

- Add default application name for session
- Add JSON date/time format conversion

## 1.21.0 (April 09, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Handle glob metacharacter escaping in CSV/JSON paths
- Fix JSON non-nullable schema to match Spark behavior
- Add default column matching case for XML
- Fix TEXT `lineSep` with hex encoding for RECORD\_DELIMITER
- Fix spark read xml external stage
- Empty CSV returns empty DataFrame
- Add default idx to `regexp_extract`
- Fix CSV non-nullable schema to match Spark behavior
- Fix temp stage naming collision under parallel tests
- Add fast path to regexp functions
- Schema coercion on `storeAssignmentPolicy`
- CSV backslash delimiter double-escape
- Optimize `posexplode`
- CSV `lineSep` empty validation
- Fix bug that xml cannot read external stage file
- Reduce default log verbosity for users

#### New features

- Added support for DML row counts
- Support `overwrite(condition)` for `DataFrameWriterV2`
- Iceberg `mergeSchema` on write — top-level column evolution
- Added support for partition overwrites in `DataFrameWriterV2`
- Add `app_name` parameter to `init_spark_session`

## 1.20.0 (April 03, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Fix performance issue
- Fix merge schema for JSON
- Fix `arrays_zip` for complex types
- Fix LCAs in implicit aggregations

#### New features

- Cache result of JSON file format
- Resolve known types from `map_unresolved_function` without typer
- Support hive partitioning for JSON copy into mode
- Add SCOS session registration on server initialization
- Modify warmup query with distinct string for filtering

## 1.19.0 (March 26, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Fix accessing struct field from array via getItem
- Fix names for accessing array elements
- Added missing compression for TEXT format
- Reduce query size in `DataFrame.replace`, UDTF creation, and `read_parquet`
- Emulate types on create [temp] view
- Fixed casting structured types to
- Fix text write type validation
- Support XML read dir in parallel
- Optimize `conv` function usage
- Support both Snowflake and `net.snowflake.spark.snowflake` format read and write
- Emulate types on create table
- Fix accessing nested structs with arrays
- Fix Parquet error message
- Optimize to\_number reducing query size
- Fix UDF cache to consider query database change
- Optimize `mask` function
- Pass PATTERN to NVS fallback reader during Parquet schema inference
- Null and structured type coercion

#### New features

- Introduce DIRECTED join hint
- Integrate XML inferSchema

## 1.18.0 (March 19, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Added missing JDBC Type mapping
- Support user provided schema in parquet
- Handle invalid UTF-8 characters in JSON gracefully
- Resolve LCA columns only if actually used
- Optimize get\_json\_object query generation
- Strip semicolon from SQL query
- Make `processInBulk=True` the default for JSON reads and fix `NullType` schema inference
- Fix bug regarding incorrect stage read
- Add non check in udf registration
- Tighten limit for error message
- Allow missing fields in user provided schema
- JSON and CSV compression inference
- Fix for `coalesce(1)` creating a single file

#### New features

- Add `execute_jar` method to launch Java/Scala workloads

### Snowpark Submit

#### Bug fixes

- Fix error swallowing with `--wait-for-completion` flag

## 1.17.0 (March 13, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- JSON and CSV compression inference.
- Fix for `coalesce` creating a single file.
- Refactor JSON read to use `COPY INTO` for single-file reads and add `VariantType` schema inference.
- Allow JSON loading without explicit schema.
- Fix `multi_line` in JSON.
- Fix JSON infer schema to avoid scanning whole files.
- Correctly handle casting to timestamp `ltz`.
- Clamp hash returned value.
- Fix for `repartition` with `partitionBy`.
- Fix to use `[connections.spark-connect]` section header in `config.toml`.
- Convert Java `date`/`timestamp` format tokens to Snowflake equivalents for CSV reads.
- Calculate schema for `pivot` functions.
- Fix UDTFs in aliased lateral join.
- Align result for SQL `SET` command.
- Fix return type for `CEIL` and `FLOOR` functions.
- Improve query generation in `unbase64` v2.
- Fix some of option to Snowflake mapping for CSV.
- Fix serialization for `POJO`.
- Improve CSV header error messages.
- Improve `mapType` detection logic with `try_cast` for Parquet reads.

#### New features

- Support for `reduceGroups` API.
- Support specifying connection name inside `init_spark_session`.
- Add config param to use UDF for `unbase64`.

## 1.16.0 (March 12, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Optimize SQL generation in function `unbase64`.
- Fix `from_json` regression
- Fix for records that span multiple BZ2 compression block boundaries
- Fix nullability mapping in unresolved attribute
- Initialize `spark-connect` session with any connection, not just one named `spark-connect`
- Add XML options validation
- Drop CSV ESCAPE option when it matches the quote character to prevent compilation error
- Fix incorrect conversion of named tuples in `productEncoder`
- Verify `mergeSchema` for CSV and JSON is not supported
- Fix Parquet complex type round-trip (write + read)
- Fix schema for `pivot`/`unpivot`
- Fix return type for `MOD` and `PMOD` functions
- Fix CSV header extraction for files with leading blank lines
- Test timezones correctly and replace string-based date/time serialization with epoch-based
- Update Java version check for Windows
- Flatten nested `withColumn` calls
- Change logic for `Literal _IntegralType` in add/sub operations
- Return `LongType` for `COUNT` functions
- Read JSON: test compression = bz2/bzip2/none
- Improve performance of `to_varchar`/`to_char`
- Make better comparison in I/O testing
- Set `multi_line` to `False` by default for copy JSON

### Snowpark Submit

#### Bug fixes

- Throw error on unspecified compute pool.

## 1.15.0 (March 06, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Remove result scan when calling `df.count()`
- Make sure infer schema runs on limited rows for reading JSON
- Fix `createDataFrame` for interval types
- Change logic for `Literal _IntegralType` in multiplication and division operations
- Widen and coerce type for `Set` operations
- Fix `neo4j` multi label support
- Modify JAR metadata so that Grype does not detect Netty vulnerability
- Return correct type for `ANY_VALUE` function
- Return widened type for sequence
- Add support for config `spark.sql.parquet.inferTimestampNTZ.enabled`
- Batch column rename/cast in `_validate_schema_and_get_writer`
- JDBC hang when partitioned queries given with fetch size
- Return trimmed exception message when it exceeds the HTTP header limits
- Fix `map_type_to_snowflake_type` for `BigDecimal`
- Fix literal decimal precision and scale
- Improve random string generation
- Make BZ2 compressed JSON loading ignore corrupt records

#### New features

- Use staged files from config in Scala UDFs
- Use permissive `TRY_CAST` in JSON reading
- Make the number of server threads configurable

### Snowpark Submit

#### Bug fixes

- Adding back `init_spark_session()` to testing
- Update `snowpark-submit` command line output to clarify `snowflake-connection-name` is required.

## 1.14.0 (February 19, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Cache table type when running `saveAsTable`
- Optimize literal input for substring and type casting for `coalesce`
- Handle decimal overflow in `avg`/`mean` and fix decimal type coercion
- Iceberg - Preserve grants on overwrite
- Standardize SQL passthrough mode
- Optimize `from_utc_timestamp`/`to_utc_timestamp` for literal timezone
- Handle JSON null values in structured types to match Spark semantics
- Emulate integral types on creating tables from SQL
- Fix edge case with mapping nested rows in Scala UDFs
- Fix how Parquet handles read and write of complex structured datatypes
- Support save ignore argument for parquet files
- Add support for artifact repository
- Fix array nullability in Scala UDxF
- Fix `log1p` for args from (-1, 0) range
- Fix `first_value` and `last_value` in aggregate context
- Fix reading `DayTimeIntervalType` for Scala client

#### New features

- Handle timezones correctly in Scala UDFs
- Support Java 11 and 17 without any configuration

### Snowpark Submit updates

#### New features

- Support `snowpark-submit` for python 3.9
- Enhance `init_spark_session` to be usable in `snowpark-submit` workflow

## 1.13.0 (February 13, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Fixed `split` function issue
- Downgraded snowflake-snowpark-python dependency to version 1.44
- Fixed `Neo4j` dialect matching to improve SQL translation
- Fixed operation ID returned in execute responses to be consistent
- Fixed `gRPC` metadata handling for TCP channel connections

#### New features

- Added support for `partition_hint` in `mapPartitions` operations
- Added XML reader support for scenarios with user-defined schemas

## 1.11.0 (January 28, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Preserve hidden columns after various DataFrame operators
- Fix issues for scala udf input types (`byte`, `binary`, `scala.math.BigDecimal`)

#### Other updates

- Add `snowpark-submit` User Defined Args to comment

## 1.10.0 (January 22, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Fix config unset error for session configuration.
- Use copy into to load CSV files in parallel.
- Fix writes for DataFrames using outer joins.
- Handle nulls in Scala UDFs.
- Optimize CTE query generation with parameter protection.
- Avoid casting arguments of `DATEDIFF`.
- Fix appending partitioned files and reading of null partitions.
- Make a 10X performance improvement for conversion between base 10 and 16 using SQL.

#### New features

- Overwrite only modified partitions for parquet files.

#### Other updates

- Updated logic to detect if Snowpark Connect for Spark is running on XP.
- Support writing to a table with variant data type in Snowflake.
- Remove unnecessary info logs.
- Move Java tests out of Scala tests job to a separate job.
- Update the dependency version for gcsfs.

### Snowpark Submit

None.

## 1.9.0 (January 14, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Fix serializing Scala tuples.
- Fix loading huge JSON files.
- Implement small fixes for customer issues.
- Implement fixes for struct comparisons.
- Add handling for 0-column DataFrames.
- Correct upload file path.
- Fix `Upload_files_if_needed` not running in parallel.
- Improve input type inference when UDF input types are not defined in the proto.
- Fix NA edge cases.

#### New features

- Support reading single JSON BZ2 file.
- Support Scala UDFs in server-side Snowpark Connect for Spark.
- Implement cast between string and `daytime`.
- Add support for Scala UDFs in `group_map`.

### Snowpark Submit

#### Bug fixes

- Reduce generated workload names.

## 1.8.0 (January 07, 2026)

### Snowpark Connect for Spark

#### Bug fixes

- Fixed JAVA\_HOME handling for Windows.

#### New features

- Support `neo4j` data source via JDBC.

### Snowpark Submit

None.
