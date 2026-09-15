# Snowpark Connect for Spark release notes for 2025

Snowflake uses semantic versioning for Snowpark Connect for Spark updates.

For documentation, see [Snowpark Connect for Apache Spark](/developer-guide/snowpark-connect/snowpark-connect-apache-spark) and
[Orchestrating Snowpark Connect for Spark workloads](/developer-guide/snowpark-connect/snowpark-connect-orchestration).

## Version 1.7.0 (December 18, 2025)

### Snowpark Connect for Spark

#### New features

- Add support for Spark integral types.
- Add support for Scala 2.13.
- Introduce support for integral types overflow behind `snowpark.connect.handleIntegralOverflow` configuration.
- Add a configuration for using custom JAR files in UDFs.
- Support Scala UDFs if `UDFPacket` lacks input types metadata.
- Allow as input and output types case classes in `reduce` function.

#### Bug fixes

- Fix Parquet logical types (TIMESTAMP, DATE, DECIMAL) handling. Previously, Parquet files were read using physical types only (such as `LongType` for timestamps). Logical types can now be interpreted by returning proper types like `TimestampType`, `DateType`, and `DecimalType`. You can enable this by setting Spark configuration `snowpark.connect.parquet.useLogicalType` to `true`.
- Use the output schema when converting Spark’s `Row` to `Variant`.
- Handle empty `JAVA_HOME`.
- Fix `from_json` function for `MapType`.
- Support of configuration `spark.sql.parquet.outputTimestampType` for `NTZ` timezone.

#### Improvements

None.

### Snowpark Submit

#### New Features

- Add support for Scala 2.13.
- Add support for `--files` argument.

#### Bug Fixes

- Add support for `--jars` for pyspark workload.
- Fix bug for Snowpark Submit JWT authentication.

## Version 1.6.0 (December 12, 2025)

### Snowpark Connect for Spark

#### New features

- Support any type as output or input type in the Scala `map` and `flatmap` functions.
- Support `joinWith`.
- Support any return type in Scala UDFs.
- Support `registerJavaFunction`.

#### Bug fixes

- Fix JSON schema inference issue for JSON reads from Scala.
- Change return types of functions returning incorrect integral types.
- Fix update fields bug with `struct` type.
- Fix unbounded input decoder.
- Fix `struct` function when the argument is `unresolved_star`.
- Fix column name for Scala UDFs when the proto contains no function name.
- Add support for PATTERN in Parquet format.
- Handle `error` and `errorIfExists` write modes.

#### Improvements

None.

## Version 1.5.0 (December 04, 2025)

### Snowpark Connect for Spark

#### New features

- Bump snowflake-connector-python to <4.2.0.
- Add basic support for single-column map and `flatMap` operations on Scala datasets.
- Iceberg writing support `TargetFileSize` and `PartitionBy`.

#### Bug fixes

- Make SAS server initialization synchronous.
- Use `snowpark-connect-deps-1==3.56.3`.
- Fix `saveAsTable` with `input_filename` columns.
- Remove duplicated reading of the cache in Scala UDFs.
- Increase recursion limit.
- Fix `format_number`.
- Fix infer schema when query is provided in JDBC read.
- Only lock dict operation in `cache.py` to improve performance.
- Fix grouped data tests.
- Throw more detailed errors on table and read/write operations.

#### Improvements

None.

## Version 1.4.0 (November 25, 2025)

### Snowpark Connect for Spark

#### New features

- Introduce reduce function for Scala.

#### Improvements

None.

#### Bug fixes

- Fix failing array insert for nullable elements.
- Throw correct error on non-numeric args in covariance.

## Version 1.3.0 (November 19, 2025)

### Snowpark Connect for Spark

#### New features

- Support `filter` on a simple (single column) `Dataset`.
- Support Azure scheme URL parsing and special character file name.

#### Bug fixes

- Fix “Dataframe has no attribute dataframe” error in Scala catalog API.
- Fix aliases in subquery, document not working subqueries.
- Fix `plan_id` resolution after joins.
- Fix `meta.yaml` for multi-py versions.
- Enable `use_vectorized_scanner` as map type from parquet file was error.
- CSV reading `inferSchema` option specify datatype.
- Fix `substr` function handling of negative length.
- Use cached file formats in `read_parquet`.
- Improve local relation performance.
- Generate summary \_common\_metadata for parquet files.
- Remove repetitive `setSchema`, `setRole`, etc, for Snowflake pushdown.

#### Improvements

None.

## Version 1.2.0 (November 17, 2025)

### Snowpark Connect for Spark

#### New features

- Relax version requirements for grpcio and aiobotocore.

#### Improvements

- Specify dependencies version in `meta.yaml`.
- Build compiled and architecture-specific conda package.
- Ensure all `CloudPickleSerializer.loads` are not done in TCM.
- Include OSS SQL tests that start with the WITH clause.
- Do not upload Spark jars when running the server for pyt.
- Update internal queries count.

#### Bug fixes

- Fix tests for tcm.
- Fix CSV column name discrepancy from Spark.
- Use type cache for empty frames.
- Resolve Windows OSS runner general issues.

### Snowpark Submit

#### Improvements

- Generate unique workload names.

#### Bug Fixes

- Fix staged file reading.

## Version 1.0.1 (November 3, 2025)

Note

With the release of this version, version 0.24 and previous versions are deprecated.

### Snowpark Connect for Spark

#### New features

- Add parameter for view creation strategies.
- Support string <-> year month interval.
- Support multiple pivot columns and aliases for pivot values in Spark SQL.
- Integrate OpenTelemetry span and traces.

#### Improvements

None.

#### Bug fixes

- Add a trailing slash for remove command.
- Invalid GROUP BY issue with aggregation function and nilary functions.
- Notebook exceeds gRPC maximum message size.
- Fix temporary view creation with colliding names.
- `array_size` with null argument.
- Fix for `$.0` JSON array access in `get_json_object` function.
- Fix self ANTI and SEMI LEFT joins.
- Handle different types in SQL function range.
- Fixed temporary view describe.

## Version 1.0.0 (October 28, 2025)

### Snowpark Connect for Spark

#### New features

- Add `rowToInferSchema` for CSV reading.
- Support INSERT INTO with CTE SQL command.
- I/O changes to add \_SUCCESS file generation and metadata file filtering.
- `update(submit)`: Support installing Snowpark Connect for Spark in the Snowpark Submit client container.

#### Improvements

None.

#### Bug fixes

- Fix \_SUCCESS path update.
- Throw error on remove failure update.
- Sequence function supporting integral types inputs.
- Fix types in empty `CreateTempViewUsing`.
- Fix Parquet file repartitioning on write.
- Resolve aliases in ORDER BY clause correctly.
- Remove scope temp session parameter.
- Fixed multiple self joins with join condition.
- Fix column name resolution in pivot.
- SQL parser aware of session timezone.
- Interval type coercion with other types.
- Fix having with nested CTEs.
- Improve qualified name resolution in Spark.

## Version 0.33.0 (October 10, 2025)

### Snowpark Connect for Spark

#### New features

- Add script to run on the output from Git action for merging SQLs.
- Add `--rebuild-whl` parameter to notebook test runner.
- Add support for both qualifiers after join.

#### Improvements

None.

#### Bug fixes

- Support escape parameter in SQL LIKE commands.
- Overwrite bug in partitions.
- Validate column count on INSERT.
- Incompatibility for pow with NAN.
- Cross JOIN with condition.
- Column attribution logic in nested queries.
- Update error message for interval test.
- String type coercion in set operation UNION and EXCEPT, coerce NUMERIC, DATE, DATETIME to STRING.
- Correctly resolve Snowpark columns after a full outer self JOIN.
- Expression in aggregate function might be zero improvement.
- Update: Revert “[SCOS GA BUG] string type coercion in set opera”
- DataFrame union of decimal type columns now widen as necessary.
- String type coercion in set operation UNION and EXCEPT, coerce NUMERIC, DATE, DATETIME to STRING (part1).
- Object not existed issue in TCM.
- Fix `to_binary(x, 'hex')` where `x` has odd number of letters and digits.
- Fix joins with empty tables.
- Fix HAVING clause to prioritize grouping columns over aggregate aliases with same name.

## Version 0.32.0 (October 17, 2025)

### Snowpark Connect for Spark

#### New features

- Support for `RepairTable`.
- Make `jdk4py` an optional dependency of Snowpark Connect for Spark to simplify configuring Java home for end users.
- Support more interval type cases.

#### Improvements

None.

#### Bug fixes

- Fix `Join` issues by refactoring qualifiers
- Fix `percentile_cont` to allow filter and sort order expressions.
- Fix `histogram_numeric` UDAF.
- Fix the `COUNT` function when called with multiple args.

## Version 0.31.0 (October 9, 2025)

### Snowpark Connect for Spark

#### New features

- Add support for expressions in the GROUP BY clause when the clause is explicitly selected.
- Add error codes to the error messages for better troubleshooting.

#### Improvements

None.

#### Bug fixes

- Fix the window function unsupported cast issue.
