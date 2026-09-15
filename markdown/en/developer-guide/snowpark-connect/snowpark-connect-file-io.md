# File I/O with Snowpark Connect for Spark

With Snowpark Connect for Spark, you can read and write data in several file formats using the standard Spark DataFrame reader and writer APIs.
You can use internal stages, external stages, and cloud storage locations as sources and destinations. For how to configure stages
and cloud URIs, see [External data sources with Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-external-data-sources).

When you set Spark-style options (such as `header`, `delimiter`, or `dateFormat`), Snowpark Connect for Spark translates them into the
corresponding Snowflake [file format options](/sql-reference/sql/create-file-format) before executing the operation. The
tables in the [Format-specific options](#format-specific-options) section show exactly how each Spark option maps to its Snowflake counterpart.

## Supported formats

| Format | Read | Write |
| --- | --- | --- |
| CSV | Supported | Supported |
| JSON | Supported | Supported |
| Parquet | Supported | Supported |
| Text | Supported | Supported |
| XML | Supported | Not supported |
| Avro | Not supported | Not supported |
| ORC | Not supported | Not supported |

Expand

Show lessSee more

## Reading data

Use the standard Spark `read` API with format short-hands or `.format()`. Paths can be Snowflake stage notation
(for example, `@my_stage/path/`), cloud URIs configured for your account, or local file paths on the machine
where Snowpark Connect for Spark is running. Chain `.option()` calls to control format behavior.

PythonJavaScala

Copy code

```
# Read from a Snowflake stage
df = spark.read.csv("@my_stage/data/")
df = spark.read.json("@my_stage/events/")
df = spark.read.parquet("@my_stage/warehouse/")
df = spark.read.text("@my_stage/logs/")

# Read from a local file
df = spark.read.csv("/tmp/local_data.csv")

# XML supports schema inference, or you can provide an explicit schema
df = spark.read.format("xml").load("@my_stage/exports/")
df = spark.read.format("xml").schema(schema).load("@my_stage/exports/")

# Set format options
df = (
    spark.read.option("header", "true")
    .option("delimiter", ";")
    .option("dateFormat", "yyyy-MM-dd")
    .csv("@my_stage/data/")
)

# Apply an explicit schema
df = spark.read.schema(my_schema).csv("@my_stage/data/")
```

Copy code

```
// Read from a Snowflake stage
Dataset<Row> df = spark.read().csv("@my_stage/data/");
Dataset<Row> df = spark.read().json("@my_stage/events/");
Dataset<Row> df = spark.read().parquet("@my_stage/warehouse/");
Dataset<Row> df = spark.read().text("@my_stage/logs/");

// XML uses .format("xml")
Dataset<Row> df = spark.read().format("xml").load("@my_stage/exports/");
Dataset<Row> df = spark.read().format("xml")
    .option("rowTag", "record")
    .schema(mySchema)
    .load("@my_stage/exports/");

// Set format options
Dataset<Row> df = spark.read()
    .option("header", "true")
    .option("delimiter", ";")
    .option("dateFormat", "yyyy-MM-dd")
    .csv("@my_stage/data/");

// Apply an explicit schema
Dataset<Row> df = spark.read().schema(mySchema).csv("@my_stage/data/");
```

Copy code

```
// Read from a Snowflake stage
val df = spark.read.csv("@my_stage/data/")
val df = spark.read.json("@my_stage/events/")
val df = spark.read.parquet("@my_stage/warehouse/")
val df = spark.read.text("@my_stage/logs/")

// XML uses .format("xml")
val df = spark.read.format("xml").load("@my_stage/exports/")
val df = spark.read.format("xml")
  .option("rowTag", "record")
  .schema(mySchema)
  .load("@my_stage/exports/")

// Set format options
val df = spark.read
  .option("header", "true")
  .option("delimiter", ";")
  .option("dateFormat", "yyyy-MM-dd")
  .csv("@my_stage/data/")

// Apply an explicit schema
val df = spark.read.schema(mySchema).csv("@my_stage/data/")
```

## Using `input_file_name()` on file reads

Spark’s [`input_file_name()`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.input_file_name.html)
function returns the path of the file that produced each row. In Snowpark Connect for Spark, file metadata isn’t populated by default. Set
`snowpark.populateFileMetadata` to `true` on the read to enable `input_file_name()` for CSV, JSON, and Parquet file reads via
`DataFrameReader`.

If you omit this option, `input_file_name()` returns an empty string for every row rather than raising an error.

Returned paths are Snowflake stage-relative (from `METADATA$FILENAME`), which may differ from Spark’s full URI form (for example,
`s3://bucket/path/file.csv`).

Enabling file metadata on multi-file paths can increase read cost compared with bulk reads that don’t need per-row filenames.

PythonJavaScala

Copy code

```
from pyspark.sql.functions import input_file_name

df = (
    spark.read
    .option("snowpark.populateFileMetadata", "true")
    .option("header", "true")
    .csv("@my_stage/data/")
)
df.select("*", input_file_name()).show()
```

Copy code

```
import static org.apache.spark.sql.functions.input_file_name;

Dataset<Row> df = spark.read()
    .option("snowpark.populateFileMetadata", "true")
    .option("header", "true")
    .csv("@my_stage/data/");
df.select("*", input_file_name()).show();
```

Copy code

```
import org.apache.spark.sql.functions._

val df = spark.read
  .option("snowpark.populateFileMetadata", "true")
  .option("header", "true")
  .csv("@my_stage/data/")
df.withColumn("source_file", input_file_name()).show()
```

Note

Text and XML reads don’t support `snowpark.populateFileMetadata` for filename metadata today.

## Reading files with SQL identifiers

In addition to the `DataFrameReader` API, you can read files directly from SQL using Spark’s format-prefix
identifier syntax with `spark.sql()`:

PythonJavaScala

Copy code

```
spark.sql("SELECT * FROM parquet.`@my_stage/sales/`").show()

spark.sql("SELECT count(*) FROM csv.`@my_stage/raw/orders.csv`").show()

spark.sql("""
  SELECT user_id, event_type
  FROM   json.`@my_stage/events/2025/01/`
  WHERE  event_type IN ('click', 'view')
""").show()

spark.sql("SELECT value FROM text.`@my_stage/logs/access.log`").show()
```

Copy code

```
spark.sql("SELECT * FROM parquet.`@my_stage/sales/`").show();

spark.sql("SELECT count(*) FROM csv.`@my_stage/raw/orders.csv`").show();

spark.sql("SELECT value FROM text.`@my_stage/logs/access.log`").show();
```

Copy code

```
spark.sql("SELECT * FROM parquet.`@my_stage/sales/`").show()

spark.sql("SELECT count(*) FROM csv.`@my_stage/raw/orders.csv`").show()

spark.sql("SELECT value FROM text.`@my_stage/logs/access.log`").show()
```

Supported prefixes: `csv.`…`` , `json.`... ``, `parquet.`…`` , `text.`... ``.

The path inside the backticks is treated the same as it would be by `spark.read.<format>(path)`.
Snowflake stage paths (`@stage/...`), cloud URIs, and local paths all work. Default format options
apply (no header for CSV, automatic schema inference, and so on). If you need non-default options,
use `spark.read` instead because the SQL identifier form doesn’t accept per-call options.

You can combine these file reads with the rest of your SQL: joins, aggregations, CTEs, and subqueries
all work on top of them.

## Writing data

Use the DataFrame `write` API with the same format short-hands.

PythonJavaScala

Copy code

```
df.write.csv("@my_stage/out/csv/")
df.write.json("@my_stage/out/json/")
df.write.parquet("@my_stage/out/parquet/")
df.write.text("@my_stage/out/text/")
```

Copy code

```
df.write().csv("@my_stage/out/csv/");
df.write().json("@my_stage/out/json/");
df.write().parquet("@my_stage/out/parquet/");
df.write().text("@my_stage/out/text/");
```

Copy code

```
df.write.csv("@my_stage/out/csv/")
df.write.json("@my_stage/out/json/")
df.write.parquet("@my_stage/out/parquet/")
df.write.text("@my_stage/out/text/")
```

## Reading from and writing to Snowflake tables

You can treat Snowflake tables as Spark DataFrame sources and sinks.

PythonJavaScala

Copy code

```
# Read
df = spark.read.table("my_database.my_schema.my_table")
df = spark.table("my_table")

# Write
df.write.saveAsTable("my_database.my_schema.my_table")
df.write.mode("overwrite").saveAsTable("my_table")
```

Copy code

```
// Read
Dataset<Row> df = spark.read().table("my_database.my_schema.my_table");
Dataset<Row> df = spark.table("my_table");

// Write
df.write().saveAsTable("my_database.my_schema.my_table");
df.write().mode("overwrite").saveAsTable("my_table");
```

Copy code

```
// Read
val df = spark.read.table("my_database.my_schema.my_table")
val df = spark.table("my_table")

// Write
df.write.saveAsTable("my_database.my_schema.my_table")
df.write.mode("overwrite").saveAsTable("my_table")
```

## Save modes

Set `mode` on the writer to control how writes interact with existing data. Not all modes are available for every
format or destination type.

PythonJavaScala

Copy code

```
df.write.mode("overwrite").parquet("@my_stage/out/")
```

Copy code

```
df.write().mode("overwrite").parquet("@my_stage/out/");
```

Copy code

```
df.write.mode("overwrite").parquet("@my_stage/out/")
```

| Mode | Spark name | Behavior in Snowpark Connect for Spark |
| --- | --- | --- |
| Error if exists | `error` / `errorifexists` | Default. Fails if data already exists at the target path or table. |
| Overwrite | `overwrite` | Removes existing files at the target path before writing. For table writes, replaces the table. |
| Append | `append` | Adds new files alongside existing ones. Uses a random filename prefix to avoid conflicts. |
| Ignore | `ignore` | Skips the write if data already exists. **Supported for Parquet file writes and table writes only.** CSV, JSON, and text file writes raise an error for this mode. |

Expand

Show lessSee more

## Controlling output file count and size

By default, Snowflake decides how to split your output into files. You can control this with
standard Spark APIs and Snowpark Connect for Spark-specific options.

### `coalesce(1)` for a single output file

The most common Spark idiom for producing one output file is honored:

PythonJavaScala

Copy code

```
df.coalesce(1).write.parquet("@my_stage/single_output/")
```

Copy code

```
df.coalesce(1).write().parquet("@my_stage/single_output/");
```

Copy code

```
df.coalesce(1).write.parquet("@my_stage/single_output/")
```

When `coalesce(1)` is used without `partitionBy`, Snowpark Connect for Spark routes the write into a single
Snowflake file.

### `repartition(n)` for multiple output files

When you request `n` output files, Snowpark Connect for Spark produces `n` files with Spark-compatible names:

PythonJavaScala

Copy code

```
df.repartition(8).write.parquet("@my_stage/8way_output/")
```

Copy code

```
df.repartition(8).write().parquet("@my_stage/8way_output/");
```

Copy code

```
df.repartition(8).write.parquet("@my_stage/8way_output/")
```

Rows are distributed across the `n` target files so each file gets roughly the same amount of
data. When you combine `repartition(n)` with `partitionBy`, the per-partition directory layout
takes precedence and Snowflake controls the file count inside each `col=value/` directory.

### `single` and `snowflake_max_file_size` write options

Snowpark Connect for Spark provides two additional write options for explicit control over output layout:

| Option | Description |
| --- | --- |
| `single` | Set to `true` to force a single output file regardless of how many input partitions the DataFrame has. Equivalent to `coalesce(1)` for non-partitioned writes. Ignored when used with `partitionBy`. |
| `snowflake_max_file_size` | Maximum size in bytes per output file. Larger values reduce the file count; smaller values produce more files. When single-file behavior is active and this option isn’t set, Snowpark Connect for Spark defaults the cap to 1 GB. |

Expand

Show lessSee more

PythonJavaScala

Copy code

```
df.write \
    .option("single", "true") \
    .option("snowflake_max_file_size", str(256 * 1024 * 1024)) \
    .parquet("@my_stage/sized_output/")
```

Copy code

```
df.write()
    .option("single", "true")
    .option("snowflake_max_file_size", String.valueOf(256 * 1024 * 1024))
    .parquet("@my_stage/sized_output/");
```

Copy code

```
df.write
  .option("single", "true")
  .option("snowflake_max_file_size", (256 * 1024 * 1024).toString)
  .parquet("@my_stage/sized_output/")
```

## Compression

Set compression through `.option("compression", "<codec>")`. For writes, the default is `NONE` for CSV, JSON,
and text, and `SNAPPY` for Parquet. For reads, compression is auto-detected if not specified.

For best performance, use splittable compression formats such as `BZ2` or `SNAPPY`. Splittable formats allow
Snowflake to decompress and process file chunks in parallel, which is significantly faster for large files than
non-splittable formats like `GZIP`.

Snowpark Connect for Spark normalizes codec names: `UNCOMPRESSED` becomes `NONE`, and Spark’s `BZIP2` becomes `BZ2`
for CSV, JSON, and text. Compression can also be inferred from file extensions (`.gz`, `.bz2`,
`.snappy`, `.deflate`).

| CSV / JSON / Text | Parquet |
| --- | --- |
| GZIP, BZ2, BROTLI, ZSTD, DEFLATE, RAW\_DEFLATE, NONE | SNAPPY, LZO, NONE |

Expand

Show lessSee more

Note

Compression isn’t supported for XML reads.

## Parallel file reads

### Multiple files

When you read from a directory or pass a list of file paths, Snowpark Connect for Spark reads the files in
parallel automatically. No additional configuration is required.

PythonJavaScala

Copy code

```
# Read all files in a directory in parallel
df = spark.read.parquet("@my_stage/data/")

# Read a specific list of files in parallel
df = spark.read.parquet(
    "@my_stage/data/part-001.parquet",
    "@my_stage/data/part-002.parquet",
    "@my_stage/data/part-003.parquet",
)
```

Copy code

```
// Read all files in a directory in parallel
Dataset<Row> df = spark.read().parquet("@my_stage/data/");

// Read a specific list of files in parallel
Dataset<Row> df = spark.read().parquet(
    "@my_stage/data/part-001.parquet",
    "@my_stage/data/part-002.parquet",
    "@my_stage/data/part-003.parquet"
);
```

Copy code

```
// Read all files in a directory in parallel
val df = spark.read.parquet("@my_stage/data/")

// Read a specific list of files in parallel
val df = spark.read.parquet(
  "@my_stage/data/part-001.parquet",
  "@my_stage/data/part-002.parquet",
  "@my_stage/data/part-003.parquet"
)
```

### Single large file

Snowpark Connect for Spark can also split a single large file into chunks and read them in parallel, so one large
file doesn’t become a bottleneck. This is supported for CSV, JSON, and XML.

**CSV**: The file must be uncompressed (`compression` set to `none`) and `multiLine` must be
`false` (the default):

PythonJavaScala

Copy code

```
df = spark.read.format("csv") \
    .option("compression", "none") \
    .load("@my_stage/large_file.csv")
```

Copy code

```
Dataset<Row> df = spark.read().format("csv")
    .option("compression", "none")
    .load("@my_stage/large_file.csv");
```

Copy code

```
val df = spark.read.format("csv")
  .option("compression", "none")
  .load("@my_stage/large_file.csv")
```

**JSON**: The file must be uncompressed (`compression` set to `none`) or BZ2-compressed, and `multiLine`
must be `false` (the default):

PythonJavaScala

Copy code

```
df = spark.read.option("compression", "none") \
    .json("@my_stage/large_file.jsonl")

# BZ2-compressed NDJSON also reads in parallel
df = spark.read.option("compression", "bz2") \
    .json("@my_stage/large_file.jsonl.bz2")
```

Copy code

```
Dataset<Row> df = spark.read().json("@my_stage/large_file.jsonl");

// BZ2-compressed NDJSON also reads in parallel
Dataset<Row> df = spark.read().option("compression", "bz2")
    .json("@my_stage/large_file.jsonl.bz2");
```

Copy code

```
val df = spark.read.json("@my_stage/large_file.jsonl")

// BZ2-compressed NDJSON also reads in parallel
val df = spark.read.option("compression", "bz2")
  .json("@my_stage/large_file.jsonl.bz2")
```

**XML**: Parallel reads are enabled by default:

PythonJavaScala

Copy code

```
df = spark.read.format("xml") \
    .option("rowTag", "record") \
    .load("@my_stage/large_export.xml")
```

Copy code

```
Dataset<Row> df = spark.read().format("xml")
    .option("rowTag", "record")
    .load("@my_stage/large_export.xml");
```

Copy code

```
val df = spark.read.format("xml")
  .option("rowTag", "record")
  .load("@my_stage/large_export.xml")
```

## Automatic exclusion of metadata files

When you read from a directory, Snowpark Connect for Spark automatically skips files that Spark also skips, so you
don’t have to filter them out manually:

| Excluded pattern | Reason |
| --- | --- |
| `_SUCCESS` | Spark write-completion marker |
| `_metadata`, `_common_metadata` | Parquet metadata sidecars |
| `*.crc` | Hadoop checksum files |
| `.DS_Store`, other `.*` files | macOS and hidden files |
| Any file starting with `_` or `.` | General Hadoop convention |

Expand

Show lessSee more

This exclusion applies to CSV, JSON, Parquet, and XML reads at any directory depth, including inside
partition subdirectories (for example, `year=2025/_SUCCESS` is skipped).

Snowpark Connect for Spark also anchors read paths so that files outside your requested prefix are never picked up.
For example, reading from `@stage/sales/` won’t accidentally include files from `@stage/sales_archive/`.

If you set `pathGlobFilter` to a pattern that explicitly matches hidden or metadata files
(for example, `_*`), that pattern takes precedence and those files are included.

## Directory listing (recursiveFileLookup)

Starting in version 1.29.0, Snowpark Connect for Spark supports the Spark `recursiveFileLookup` DataFrameReader option for
`csv`, `json`, `parquet`, `text`, and `xml` reads. The option controls whether reads descend into nested
subdirectories when you pass a directory path.

- `true` — list data files recursively under the read path. Hive-style partition discovery is skipped.
- `false` — list only direct children of the read path (depth-0). Hive-style partition directories
  (`key=value/`) are still discovered.

When you omit `recursiveFileLookup`, Snowpark Connect for Spark 1.29.0 retains the prior behavior and lists files recursively.
In a future release, omitting the option will match Apache Spark 3.5 (depth-0 listing with Hive partition discovery).

If your workloads read nested data under a directory root that is not Hive-partitioned, set the option
explicitly now to avoid surprises when the default changes:

Copy code

```
df = spark.read.option("recursiveFileLookup", "true").csv("@my_stage/sales/")
```

For more details about the planned default change, see
[Directory listing (recursiveFileLookup)](/developer-guide/snowpark-connect/snowpark-connect-compatibility#label-snowpark-connect-compatibility-directory-listing)
in the compatibility guide.

## Format-specific options

Spark options set through `.option()` are translated into Snowflake
[file format options](/sql-reference/sql/create-file-format) before Snowpark Connect for Spark executes the read or write
operation. The tables below show how each Spark option maps to its Snowflake counterpart and note any behavioral
differences.

Options that don’t have a Snowflake equivalent are ignored. Snowpark Connect for Spark logs a warning for each
unsupported option.

### Snowpark Connect read options

These options are specific to Snowpark Connect for Spark and aren’t part of open-source Spark. They apply across CSV, JSON, and Parquet
`DataFrameReader` reads. See [Using `input_file_name()` on file reads](#using-input_file_name-on-file-reads) for usage
details.

| Spark option | Default | Notes |
| --- | --- | --- |
| `snowpark.populateFileMetadata` | `false` | Set to `true` to enable `input_file_name()` on CSV, JSON, and Parquet reads. |

Expand

Show lessSee more

### CSV options

| Spark option | Snowflake file format option | Notes |
| --- | --- | --- |
| `sep` / `delimiter` | `FIELD_DELIMITER` | Default `,`. `delimiter` is an alias for `sep`. |
| `header` | `PARSE_HEADER` | When `true`, the reader sets `PARSE_HEADER` and uses column names from the first row. When writing, controls whether a header row is written. |
| `quote` | `FIELD_OPTIONALLY_ENCLOSED_BY` | Default `"` for reads. Semantics differ from Spark: Snowflake uses optional enclosure rather than mandatory quoting. An empty value removes enclosure. |
| `escape` | `ESCAPE` | A single `\` is normalized to `\\`. Dropped when the field delimiter is `\` or when `escape` equals `quote`. |
| `nullValue` | `NULL_IF` | Spark defaults to `""`; Snowflake defaults to `\N`. Explicitly set this option if your files use a specific null representation. |
| `lineSep` | `RECORD_DELIMITER` | Default `\n`. |
| `encoding` / `charset` | `ENCODING` | Default `UTF-8`. `charset` is an alias for `encoding`. |
| `multiLine` | `MULTI_LINE` | Default `false`. |
| `dateFormat` | `DATE_FORMAT` | Java `SimpleDateFormat` patterns are automatically converted to Snowflake tokens (for example, `dd/MM/yyyy` becomes `DD/MM/YYYY`). See [Date and timestamp format conversion](#date-and-timestamp-format-conversion). |
| `timestampFormat` | `TIMESTAMP_FORMAT` | Default `yyyy-MM-dd HH:mm:ss.SSSSSS`. Same Java-to-Snowflake token conversion as `dateFormat`. |
| `compression` | `COMPRESSION` | See [Compression](#compression). |
| `inferSchema` | `INFER_SCHEMA` | Default `false` (read only). |
| `rowsToInferSchema` | `INFER_SCHEMA_OPTIONS.MAX_RECORDS_PER_FILE` | Read only. Default 20000. Sets the number of rows sampled per file when inferring the schema. Reduce this value to speed up reads when the data is uniform. Requires `inferSchema = true`. |
| `mode` | `ON_ERROR` | Controls error handling on read. `DROPMALFORMED` maps to `CONTINUE`, `FAILFAST` maps to `ABORT_STATEMENT`. `PERMISSIVE` (the Spark default) is only partially supported. |
| `ignoreLeadingWhiteSpace` / `ignoreTrailingWhiteSpace` | `TRIM_SPACE` | If either option is `true`, Snowflake trims whitespace from both sides. One-sided trimming isn’t available. |
| `mergeSchema` | (internal) | When `true`, Snowpark Connect for Spark infers schemas per file group and produces a union schema. Requires `header = true` and `inferSchema = true`. New columns across files become nullable. Type widening (for example, `INT` to `STRING`) is supported. |
| `relaxTypesToInferSchema` | (internal) | When `true`, widens narrow numeric types to match Spark’s inference behavior (for example, `Short` to `Integer`, small `Decimal` to `Long`). Enabled automatically when `rowsToInferSchema` is set. |
| `pathGlobFilter` | `PATTERN` | Filters which files to read based on a glob pattern. |
| `recursiveFileLookup` | (see [Directory listing](#label-snowpark-connect-file-io-recursive-file-lookup)) | Controls whether reads descend into nested subdirectories. Supported in 1.29.0+. In a future release, the default when omitted will align with Apache Spark. |

Expand

Show lessSee more

In addition, Snowpark Connect for Spark always sets the following on CSV reads:

- `ESCAPE_UNENCLOSED_FIELD = NONE`
- `ERROR_ON_COLUMN_COUNT_MISMATCH = False`
- `SKIP_BLANK_LINES = True`

### JSON options

| Spark option | Snowflake file format option | Notes |
| --- | --- | --- |
| `multiLine` | `STRIP_OUTER_ARRAY` + `MULTI_LINE` | Both Snowflake options are set to the same value. When `true`, the reader handles files that contain a JSON array at the top level or span multiple lines. |
| `dateFormat` | `DATE_FORMAT` | Default `auto`. Unlike CSV, JSON date format strings are **not** converted from Java patterns. Pass Snowflake-compatible format tokens directly. |
| `timestampFormat` | `TIMESTAMP_FORMAT` | Default `auto`. Same as `dateFormat`: pass Snowflake-compatible tokens. |
| `encoding` | `ENCODING` | Default `UTF-8`. |
| `mode` | `ON_ERROR` | Controls error handling on read. `DROPMALFORMED` maps to `CONTINUE`, `FAILFAST` maps to `ABORT_STATEMENT`. `PERMISSIVE` (the Spark default) is only partially supported. |
| `dropFieldIfAllNull` | (schema inference) | When `true`, fields that are null in every sampled row are dropped from the inferred schema. |
| `rowsToInferSchema` | `INFER_SCHEMA_OPTIONS.MAX_RECORDS_PER_FILE` | Read only. Sets the number of rows sampled per file when inferring the schema. Reduce this value to speed up reads when the data is uniform. |
| `relaxTypesToInferSchema` | (internal) | When `true`, widens narrow numeric types to match Spark’s inference behavior (for example, `Short` to `Integer`, small `Decimal` to `Long`). Enabled automatically when `rowsToInferSchema` is set. |
| `pathGlobFilter` | `PATTERN` | Filters which files to read. |
| `recursiveFileLookup` | (see [Directory listing](#label-snowpark-connect-file-io-recursive-file-lookup)) | Controls whether reads descend into nested subdirectories. Supported in 1.29.0+. In a future release, the default when omitted will align with Apache Spark. |
| `compression` | `COMPRESSION` | See [Compression](#compression). |

Expand

Show lessSee more

When writing JSON, Snowpark Connect for Spark converts the DataFrame into a single VARIANT column using `OBJECT_CONSTRUCT`
before unloading. On the write path, `nullValue` is mapped to `NULL_IF` and `compression` is mapped to
`COMPRESSION`. Other Spark JSON writer options (such as `dateFormat`) aren’t applied.

### Parquet options

| Spark option | Snowflake file format option | Notes |
| --- | --- | --- |
| `pathGlobFilter` | `PATTERN` | Filters which files to read. |
| `compression` | `COMPRESSION` | Default `SNAPPY` for writes, `AUTO` for reads. Allowed values: `AUTO`, `LZO`, `SNAPPY`, `NONE`. `UNCOMPRESSED` is also accepted and normalized to `NONE`. |
| `mergeSchema` | (internal) | When `true` and reading from multiple paths, Snowpark Connect for Spark infers the schema from each file and produces a union schema. New columns are added; type widening across files (for example, `INT` to `STRING`) isn’t supported. |
| `rowsToInferSchema` | (internal) | Read only. Default 20000. Controls the sample size used by Snowpark Connect for Spark when discovering complex types (STRUCT, MAP, ARRAY) inside Parquet VARIANT columns. |
| `nullValue` | `NULL_IF` | Write only. Sets the string that represents null values in the output files. |
| `recursiveFileLookup` | (see [Directory listing](#label-snowpark-connect-file-io-recursive-file-lookup)) | Controls whether reads descend into nested subdirectories. Supported in 1.29.0+. In a future release, the default when omitted will align with Apache Spark. |

Expand

Show lessSee more

Snowpark Connect for Spark also sets these options automatically based on session configuration:

- `BINARY_AS_TEXT = False` (always)
- `USE_LOGICAL_TYPE`: controlled by `snowpark.connect.parquet.useLogicalType`

When writing Parquet, structured complex types (ARRAY, MAP, STRUCT) are cast to VARIANT before
unload so that Snowflake’s `COPY INTO` can produce valid Parquet files.

### Text options

Text I/O uses a CSV file format internally with `FIELD_DELIMITER = NONE`.

| Spark option | Snowflake file format option | Notes |
| --- | --- | --- |
| `lineSep` / `linesep` | `RECORD_DELIMITER` | Default `\n`. Controls the line separator for both reads and writes. |
| `wholetext` | `RECORD_DELIMITER = NONE` | When `true`, each file is read as a single row. |
| `compression` | `COMPRESSION` | Default `auto` for reads, `NONE` for writes. |
| `recursiveFileLookup` | (see [Directory listing](#label-snowpark-connect-file-io-recursive-file-lookup)) | Controls whether reads descend into nested subdirectories. Supported in 1.29.0+. In a future release, the default when omitted will align with Apache Spark. |

Expand

Show lessSee more

Text writes always set `ESCAPE_UNENCLOSED_FIELD = NONE` and `FILE_EXTENSION = txt`. The DataFrame must
contain exactly one string column.

### XML options (read only)

XML supports schema inference. If no schema is provided, Snowpark Connect for Spark infers the schema from the data by reading
the files and merging field types across all input.

| Spark option | Internal mapping | Notes |
| --- | --- | --- |
| `rowTag` | `rowTag` | Specifies the XML element that maps to a DataFrame row. Defaults to `ROW` if not set. |
| `inferSchema` | `inferSchema` | Default `true`. When a user schema is provided, Snowpark Connect for Spark forces `inferSchema=false` to keep the read single-pass. |
| `samplingRatio` | `samplingRatio` | Default `1.0`. Fraction of rows to sample when inferring the schema. |
| `mode` | `mode` | Default `PERMISSIVE`. Controls error handling: `PERMISSIVE`, `DROPMALFORMED`, or `FAILFAST`. `PERMISSIVE` is partially supported: if input data doesn’t match the specified schema type and can’t be coerced, an error might be thrown instead of placing the row in the corrupt record column. |
| `columnNameOfCorruptRecord` | `columnNameOfCorruptRecord` | Default `_corrupt_record`. Column name used to store malformed rows in `PERMISSIVE` mode. |
| `attributePrefix` | `attributePrefix` | Default `_`. Prefix added to XML attribute names in the DataFrame schema. Can’t equal `valueTag`. |
| `valueTag` | `valueTag` | Default `_VALUE`. Tag name for the text content of mixed-content elements. Can’t be empty. |
| `encoding` | `charset` | Renamed internally. Default `UTF-8`. |
| `excludeAttribute` | `excludeAttributes` | Renamed internally. Default `false`. |
| `ignoreSurroundingSpaces` | `ignoreSurroundingWhitespace` | Renamed internally. Default `false`. |
| `ignoreNamespace` | `ignoreNamespace` | Default `false`. When `true`, XML namespace prefixes are stripped from element and attribute names. |
| `nullValue` | `nullValue` | Default `""`. String value to interpret as null. |
| `pathGlobFilter` | `PATTERN` | Filters which files to read. |
| `recursiveFileLookup` | (see [Directory listing](#label-snowpark-connect-file-io-recursive-file-lookup)) | Controls whether reads descend into nested subdirectories. Supported in 1.29.0+. In a future release, the default when omitted will align with Apache Spark. |
| `rowValidationXSDPath` | `rowValidationXSDPath` | Path to an XSD file on a stage (for example, `@my_stage/schema.xsd`) to validate each XML row against. Local XSD files are automatically uploaded to the stage. Rows that fail validation are handled according to the `mode` setting. |

Expand

Show lessSee more

## Date and timestamp format conversion

For CSV reads and writes, Snowpark Connect for Spark automatically converts Java `SimpleDateFormat` patterns (used by Spark)
to Snowflake file format tokens. Common conversions:

| Java/Spark pattern | Snowflake token | Example |
| --- | --- | --- |
| `yyyy` | `YYYY` | Four-digit year |
| `yy` | `YY` | Two-digit year |
| `MM` | `MM` | Zero-padded month |
| `MMM` | `MON` | Abbreviated month name (Jan, Feb) |
| `dd` | `DD` | Zero-padded day of month |
| `HH` | `HH24` | 24-hour clock (00-23) |
| `hh` | `HH12` | 12-hour clock (01-12) |
| `mm` | `MI` | Minutes |
| `ss` | `SS` | Seconds |
| `SSS` | `FF3` | Fractional seconds (milliseconds) |
| `SSSSSS` | `FF6` | Fractional seconds (microseconds) |
| `a` | `AM` | AM/PM marker |

Expand

Show lessSee more

Some patterns don’t have exact Snowflake equivalents:

- **Unpadded values**: Spark’s single-letter patterns (`d` for day, `h` for hour) produce unpadded output (for example,
  `9`), but Snowflake always zero-pads (`DD` produces `09`).
- **Full day name**: Spark’s `EEEE` (`Thursday`) maps to abbreviated `DY` (`Thu`) in Snowflake.
- **Timezone offsets**: Spark’s `Z` (`-0500`) maps to `TZHTZM` (`-0500`) without a colon separator.
  The colon-separated `TZH:TZM` format (`-05:00`) applies to `XXX` and `xxx` patterns.

Important

This conversion applies only to **CSV**. For JSON, date and timestamp format strings are passed directly to
Snowflake without conversion. Use Snowflake-compatible format tokens (such as `YYYY-MM-DD`) when setting
`dateFormat` or `timestampFormat` on JSON readers.

## Partitioned data

Snowpark Connect for Spark supports Hive-style `col=value/` directory layouts for CSV, JSON, and Parquet formats.

### Writing partitioned data

Use the standard `partitionBy(...)` API. Snowpark Connect for Spark produces the same `col=value/` directory tree that Spark
does:

PythonJavaScala

Copy code

```
df.write.partitionBy("year", "month").parquet("@my_stage/out/partitioned/")
```

Copy code

```
df.write().partitionBy("year", "month").parquet("@my_stage/out/partitioned/");
```

Copy code

```
df.write.partitionBy("year", "month").parquet("@my_stage/out/partitioned/")
```

Note

Unlike open-source Spark, Snowpark Connect for Spark includes the partition columns in the written data files themselves, not
only in the directory structure. The output files contain all columns of the DataFrame, including the ones used
for partitioning.

### Reading partitioned data

Point the reader at the root directory and Snowpark Connect for Spark discovers partition columns from the directory names
automatically:

PythonJavaScala

Copy code

```
df = spark.read.parquet("@my_stage/out/partitioned/")
df.printSchema()

# Read a specific partition directly by path
df = spark.read.parquet("@my_stage/out/partitioned/year=2025/month=1/")

# Read all partitions and filter on a partition column
df = spark.read.parquet("@my_stage/out/partitioned/")
recent = df.filter(df["year"] == 2025)
recent.show()
```

Copy code

```
Dataset<Row> df = spark.read().parquet("@my_stage/out/partitioned/");
df.printSchema();

// Read a specific partition directly by path
Dataset<Row> jan = spark.read().parquet("@my_stage/out/partitioned/year=2025/month=1/");

// Read all partitions and filter on a partition column
Dataset<Row> all = spark.read().parquet("@my_stage/out/partitioned/");
Dataset<Row> recent = all.filter(col("year").equalTo(2025));
recent.show();
```

Copy code

```
val df = spark.read.parquet("@my_stage/out/partitioned/")
df.printSchema()

// Read a specific partition directly by path
val jan = spark.read.parquet("@my_stage/out/partitioned/year=2025/month=1/")

// Read all partitions and filter on a partition column
val all = spark.read.parquet("@my_stage/out/partitioned/")
val recent = all.filter($"year" === 2025)
recent.show()
```

Partition discovery behavior:

- Partition columns appear at the **end** of the schema, in the order they appear in the directory tree.
- Partition value types are inferred from the observed values: all integers become `IntegerType`, all
  floating-point values become `DoubleType`, otherwise `StringType`. You can override a partition
  column’s type by supplying a `.schema(...)` that includes it.
- `null` values in a partition column are written as the directory segment `__HIVE_DEFAULT_PARTITION__`
  and read back as `null`.
- Mixed-depth or conflicting layouts (for example, the same key at two different depths) raise an error
  rather than producing incorrect values.

Important

Filters on partition columns don’t reduce the number of files read. Snowpark Connect for Spark reads all files in
the directory subtree and applies filters after loading.

### Dynamic partition overwrite

When writing partitioned data to a stage, you can overwrite only the partitions that appear in the current
DataFrame instead of deleting all existing data. Set the `spark.sql.sources.partitionOverwriteMode` session
configuration to `dynamic`:

PythonJavaScala

Copy code

```
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

df.write.mode("overwrite") \
    .partitionBy("year", "month") \
    .parquet("@my_stage/out/partitioned/")
```

Copy code

```
spark.conf().set("spark.sql.sources.partitionOverwriteMode", "dynamic");

df.write().mode("overwrite")
    .partitionBy("year", "month")
    .parquet("@my_stage/out/partitioned/");
```

Copy code

```
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

df.write.mode("overwrite")
  .partitionBy("year", "month")
  .parquet("@my_stage/out/partitioned/")
```

This removes only the partition subdirectories that match the DataFrame. See
[Snowpark Connect for Spark properties](/developer-guide/snowpark-connect/snowpark-connect-parameters) for more on this configuration property.

Note

The `.option("overwrite-mode", "dynamic")` writer option is supported only for
Iceberg table writes. For stage-based file writes, use the session configuration shown above.

## Known limitations

- **Save mode support varies by format**: `ignore` mode is supported only for Parquet file writes and table writes.
  CSV, JSON, and text file writes raise an error for `ignore` mode.
- **ORC and Avro**: These formats aren’t supported for read or write.
- **Bucketed writes**: `bucketBy` and `sortBy` aren’t supported for file or table writes.
- **One-sided whitespace trimming**: Spark’s `ignoreLeadingWhiteSpace` and `ignoreTrailingWhiteSpace` both map
  to `TRIM_SPACE`, which trims from both sides. Trimming only leading or only trailing whitespace isn’t possible.
- **CSV quote semantics**: Spark’s `quote` option and Snowflake’s `FIELD_OPTIONALLY_ENCLOSED_BY` have different
  semantics. Snowflake treats enclosure as optional, while Spark applies mandatory quoting rules.
- **Text column constraint**: Text writes require exactly one string column in the DataFrame.
- **XML MapType**: `MapType` isn’t supported for XML reads. Use `StructType` to represent key-value
  structures.
- **XML via Spark SQL**: Reading XML files with `spark.sql()` (for example,
  `SELECT * FROM xml.`@stage/file.xml``) isn’t supported. Use the `DataFrameReader` API instead.
- **`input_file_name()` requires opt-in metadata**: Unlike Spark, file metadata isn’t populated by default. Set
  `snowpark.populateFileMetadata=true` on the read; otherwise `input_file_name()` returns an empty string. See
  [Using `input_file_name()` on file reads](#using-input_file_name-on-file-reads).
