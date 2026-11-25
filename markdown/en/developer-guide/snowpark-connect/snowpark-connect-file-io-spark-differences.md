# Snowpark Connect for Spark file I/O differences from Apache Spark (*Preview*)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Starting in version 1.51.0, Snowpark Connect for Spark reads and writes CSV and JSON files, and reads XML files, with the next
generation file reader and writer. They’re designed to match Apache Spark behavior, but some differences remain. This
topic lists the file I/O differences to validate when you move an Apache Spark workload to Snowpark Connect for Spark 1.51.0 or later.
For differences that aren’t specific to file I/O, see [Snowpark Connect for Spark known differences from Apache Spark](/developer-guide/snowpark-connect/snowpark-connect-limitations).

The baseline for this topic is Apache Spark 3.5. Behavior can vary with your Spark version, options, and data, so test
your workload with representative files. If you’re upgrading an existing Snowpark Connect for Spark workload from 1.50.0 or earlier,
see [Migrate Snowpark Connect for Spark file I/O to version 1.51.0 (Preview)](/developer-guide/snowpark-connect/snowpark-connect-file-io-migrate) instead.

## All formats

**`input_file_name()` requires opt-in and returns stage paths.**
File metadata isn’t populated by default. Set `snowpark.populateFileMetadata=true` on the read; otherwise
`input_file_name()` returns an empty string. CSV, JSON, and XML reads return the fully qualified stage path (for example,
`@my_db.my_schema.my_stage/data/file.csv`), and Parquet reads return the path relative to the stage, where Apache Spark
returns a full URI such as `s3://bucket/data/file.csv`. Text reads don’t support `input_file_name()`.

**Filters on partition columns don’t prune files.**
Snowpark Connect for Spark reads every file in the directory tree and applies partition filters after loading.

**Save mode `ignore` isn’t supported for every format.**
Text file writes raise an error for `ignore` mode. Parquet file writes accept `ignore` but add new files even when the
target path already contains data. In Apache Spark, `ignore` skips the write when the target path exists.

**`bucketBy` and `sortBy` are ignored for table writes.**
No error is raised, and the table is written without bucketing or sorting. Apache Spark writes a bucketed, sorted table.

**XML files can’t be read with `spark.sql()`.**
Queries such as `` SELECT * FROM xml.`@stage/file.xml` `` aren’t supported. Use the `DataFrameReader` API instead.

## CSV and JSON writes

- **Partition columns in files**: `partitionBy` writes the same `col=value/` directory tree as Apache Spark, but the
  output files also contain the partition columns. Apache Spark writes those columns only in the directory names. As in
  Apache Spark, `bucketBy` and `sortBy` aren’t supported for file writes.
- **File count**: `coalesce(1)` and `repartition(n)` don’t control the number of output files. Snowflake determines the
  file count and size, so a large write can produce several files where Spark produces one.
- **Compression**: Only `gzip`, `bzip2`, `deflate`, and `none` are supported. Apache Spark also supports `lz4` and
  `snappy` for CSV and JSON.
- **`_SUCCESS` marker**: Writes don’t create a `_SUCCESS` file. This matters only if an external process waits for that
  marker.

## CSV

**Hive-style partition discovery isn’t supported.**
Partition columns that exist only in `key=value` directory names aren’t added to the DataFrame, where Apache Spark adds
them. Filters on a partition column can fail. Explicit schemas that include a partition field can change the field order
or return null for a value that Spark fills in, and invalid numeric partition values can be accepted where Spark rejects
them. Validate directory-only partition layouts, reads of a subdirectory or with `basePath`, explicit schemas, field
order, and filtered values. Don’t test only with partitioned files written by Snowpark Connect for Spark: those files can include the
partition fields inside the data and hide the difference.

**Repeated paths and wildcard paths can return fewer rows or fail.**
Apache Spark reads each occurrence of a repeated path: for the path list `[A, A]`, Spark returns four rows and
Snowpark Connect for Spark returns two, because it reads the directory once. Globs in a CSV path (such as `dir/*.csv`) can return zero
rows; paths with a wildcard in the file extension don’t always match Spark, and paths with brace alternatives (such as
`{a,b}`) can be rejected as missing. Reading a directory with a simple `pathGlobFilter` pattern selected the expected files
in testing. Verify the selected files and row counts for each path pattern you use.

**Files with different headers are merged by name.**
When files in a read have different headers, Snowpark Connect for Spark returns the union of the column names, with nulls where a
column is absent. In the tested cases, Apache Spark returned fewer columns and placed values by position. For example, a
two-column Spark result became three columns, and a three-column result became four. The values are kept, but the schema
and column mapping differ. Column order can also differ between repeated reads when inferred columns tie for position.
Normalize headers and map columns explicitly; don’t depend on `SELECT *` or positional access.

**Schema inference with `samplingRatio` can differ.**
In a tested read with `samplingRatio` below `1.0`, Snowpark Connect for Spark inferred `double` where Apache Spark inferred `int`.
Specify a schema when type stability matters.

**Corrupt files, parser limits, and `DROPMALFORMED` need separate validation.**
With an oversized field and `maxCharsPerColumn` set, Apache Spark honored `ignoreCorruptFiles=true` and returned the rows
from the valid files; Snowpark Connect for Spark fails the read. Some corrupt gzip files are accepted by Snowpark Connect for Spark where Spark fails.
For `DROPMALFORMED`, a tested read collected zero rows in both Spark and Snowpark Connect for Spark, but `count()` returned five in Spark
and zero in Snowpark Connect for Spark. Compare collected rows, error handling, and counts on representative malformed and compressed
input.

**Some encodings and date and time settings differ.**
Schema inference for UTF-16 files returned the header as an extra data row, and a charset alias behaved the same way. A
session time zone with a positive offset failed with a SQL compilation error, and `timeParserPolicy=EXCEPTION` raised an
error where Spark parsed the value. Validate the exact encoding, header handling, date pattern, and time zone that your
workload uses.

**Some types and CSV APIs aren’t fully compatible.**

- Explicit interval schemas aren’t supported.
- Legacy `CHAR` and `VARCHAR` options and file-block metadata functions aren’t supported.
- Some `from_csv` and `schema_of_csv` calls raise errors where Spark succeeds. A successful `spark.read.csv` doesn’t mean
  these functions work.
- Streaming jobs with file sources (`readStream` and `writeStream.start`) aren’t supported.

## JSON

**Hive-style partition discovery isn’t supported.**
Fields that Apache Spark derives from `key=value` directory names aren’t added to the DataFrame, including for reads with
`basePath` or partition predicates. Filters on a partition column can fail, and explicit partition schemas and values are
validated differently. Compare full schemas, partition values, and filtered rows on files whose records don’t contain
the directory field. Files written by Snowpark Connect for Spark can contain that field and hide the difference.

**Repeated paths, wildcard paths, and local files don’t always match Spark.**
A repeated two-row directory `[A, A]` returns two rows in Snowpark Connect for Spark and four in Apache Spark. A brace-alternative path
such as `{a,b}.json` is rejected as missing where Spark expands it. If you read a local file and delete the original
before the action runs, Snowpark Connect for Spark can still read the uploaded copy where Spark fails or skips it. Verify path
expansion, row multiplicity, the files read, and `ignoreMissingFiles` behavior.

**Field names that differ only in case can produce different schemas.**
For files whose field names differ only in case, Snowpark Connect for Spark returns each case variant as a separate column (six or nine
columns where Spark returned three, in the tested files), with values spread across them and nulls where a variant is
absent. Snowpark Connect for Spark kept values that Spark lost in those cases, so the difference is the schema shape and column mapping.
Snowpark Connect for Spark also accepts some partly overlapping or explicitly colliding schemas where Spark raises
`COLUMN_ALREADY_EXISTS`. Normalize field names before projections, joins, and writes. Setting `caseSensitive=false`
doesn’t guarantee the same merge behavior as Spark.

**JSON parser limits aren’t enforced.**
The `maxNestingDepth`, `maxNumLen`, and `maxStringLen` options aren’t enforced: input over the limit is kept where Spark
drops the record under `DROPMALFORMED` or fails under `FAILFAST`. Invalid limit values are also accepted where Spark
rejects them. Don’t rely on these limits for validation.

**Corrupt record queries and declared schemas can behave differently.**
A declared corrupt record field that’s non-nullable is rejected where Spark succeeds, and some queries on compressed files
that count or select corrupt records are rejected where Spark succeeds. Validate the projection, action, compression,
declared nullability, and corrupt record column name that you use.

**Encoding and timestamp settings need targeted tests.**
Some non-UTF-8 JSON files fail to read where Spark succeeds. Session time zones with a positive offset can fail, and the
`timeZone` read option can produce different values. ISO 8601 timestamps written by Apache Spark read correctly in
testing. Compare actual values, not only the schema, using the encoding, time zone, and timestamp pattern that your
workload needs.

**`NullType`, interval and `CHAR` schemas, and some JSON APIs differ.**

- A declared `NullType` field is returned as `StringType`.
- Interval-typed JSON reads and writes, and legacy `CHAR` and `VARCHAR` settings, aren’t supported.
- Some `from_json` and `schema_of_json` calls raise errors where Spark succeeds. Test them separately from
  `spark.read.json`.
- Streaming jobs with file sources aren’t supported.

## XML

**Hive-style partition discovery isn’t supported.**
Files under `key=value/` directories are read, but partition columns that exist only in the directory names aren’t
added to the DataFrame, where Apache Spark adds them.

**XML writes aren’t supported.**
`df.write.format("xml")` and `df.write.xml()` aren’t supported, regardless of options, save mode, partitioning, or
compression.

**Fields declared `NOT NULL` are relaxed.**
With an explicit schema, a non-nullable field that receives a value that can’t be parsed is returned as null, and the
schema reports the field as nullable. `spark-xml` fails the read in this case. Don’t rely on `nullable=False` for input
validation; use `FAILFAST` mode or explicit checks.

## Display, metadata, and error handling

- **Schema display**: `printSchema()` can show `long` for a column declared as `IntegerType`, even though `df.schema`
  still reports `int`. A tab character can display differently in `show()` output. These are display differences, not
  value changes.
- **Column names and nullability after table writes**: writing to a Snowflake table can change column nullability and
  metadata, and column names can become uppercase. This affects code that accesses Python `Row` fields by name.
- **Exception types**: errors such as a header mismatch or a `FAILFAST` failure raise `QueryExecutionException`, which is
  a subclass of `SparkConnectGrpcException`, so handlers that catch the base class still work. A missing path in a
  multi-directory read, or accessing a nested field with the wrong case when `caseSensitive=true`, can raise
  `QueryExecutionException` instead of `AnalysisException`. Handlers that catch only `AnalysisException` miss these
  errors.
- **Validation errors**: some checks that Spark rejects at analysis time, such as sorting nested values that contain a
  map, are accepted. Don’t rely on an expected Spark failure for data validation.
