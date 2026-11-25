# File I/O with Snowpark Connect for Spark

With Snowpark Connect for Spark, you can read and write data in several file formats using the standard Spark DataFrame reader and writer APIs.
You can use internal stages, external stages, and cloud storage locations as sources and destinations. For how to configure stages
and cloud URIs, see [External data sources with Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-external-data-sources).

This page describes Snowpark Connect for Spark 1.51.0 and later. For 1.50.0 and earlier, see
[File I/O with Snowpark Connect for Spark 1.50.0 and earlier](/developer-guide/snowpark-connect/snowpark-connect-file-io-previous).

CSV, JSON, and XML options that you set with `.option()` (such as `header`, `sep`, or `dateFormat`) are applied with
Apache Spark semantics. Parquet and text options are translated into the corresponding Snowflake
[file format options](/sql-reference/sql/create-file-format) before Snowpark Connect for Spark executes the operation. The tables in
the [Format-specific options](#format-specific-options) section describe each option.

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

## Next generation file reader and writer (*Preview*)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Starting in version 1.51.0, Snowpark Connect for Spark uses the next generation file reader and writer, which are designed to match
Apache Spark behavior more closely. They handle these operations:

- **CSV**: reads and writes
- **JSON**: reads and writes
- **XML**: reads

Parquet and text reads and writes work the same as in 1.50.0 and earlier. XML writes aren’t supported.

For more information, see:

- [Migrate Snowpark Connect for Spark file I/O to version 1.51.0 (Preview)](/developer-guide/snowpark-connect/snowpark-connect-file-io-migrate): what changes when you upgrade an existing
  workload from 1.50.0 or earlier, and how to update your code.
- [Snowpark Connect for Spark file I/O differences from Apache Spark (Preview)](/developer-guide/snowpark-connect/snowpark-connect-file-io-spark-differences): how file I/O in Snowpark Connect for Spark 1.51.0
  and later differs from Apache Spark, for workloads that you migrate from other Spark platforms.

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

# XML supports schema inference, or you can provide an explicit schema.
# Set rowTag to the element that wraps each row.
df = spark.read.format("xml").option("rowTag", "record").load("@my_stage/exports/")
df = spark.read.format("xml").option("rowTag", "record").schema(schema).load("@my_stage/exports/")

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
Dataset<Row> df = spark.read().format("xml").option("rowTag", "record").load("@my_stage/exports/");
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
val df = spark.read.format("xml").option("rowTag", "record").load("@my_stage/exports/")
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
`snowpark.populateFileMetadata` to `true` on the read to enable `input_file_name()` for CSV, JSON, Parquet, and XML file
reads via `DataFrameReader`. Text reads don’t support `input_file_name()`.

If you omit this option, `input_file_name()` returns an empty string for every row rather than raising an error.

The returned path depends on the format:

- **CSV, JSON, and XML**: the fully qualified stage path, for example `@my_db.my_schema.my_stage/data/file.csv`.
- **Parquet**: the path relative to the stage (from `METADATA$FILENAME`), for example `data/file.parquet`.

Both forms differ from Spark’s full URI form (for example, `s3://bucket/path/file.csv`).

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
import static org.apache.spark.sql.functions.col;
import static org.apache.spark.sql.functions.input_file_name;

Dataset<Row> df = spark.read()
    .option("snowpark.populateFileMetadata", "true")
    .option("header", "true")
    .csv("@my_stage/data/");
df.select(col("*"), input_file_name()).show();
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
| Error if exists | `error` | Default. For table writes, fails if the table already exists. For CSV and JSON file writes, fails with `PATH_ALREADY_EXISTS` if the target path already contains files. For Parquet and text file writes, existing files aren’t detected, and new files are added alongside existing ones (the same behavior as `append`). The `errorifexists` alias isn’t supported. Use `error` instead. |
| Overwrite | `overwrite` | Removes existing files at the target path before writing. For table writes, replaces the table. |
| Append | `append` | Adds new files alongside existing ones. Each write adds a unique ID to its filenames to avoid conflicts. |
| Ignore | `ignore` | For table writes, and for CSV and JSON file writes, skips the write if the target already exists or already contains files. For Parquet file writes, the mode is accepted, but existing files aren’t detected and new files are added. Text file writes raise an error for this mode. |

Expand

Show lessSee more

## Controlling output file count and size

By default, Snowflake decides how to split your output into files. For Parquet and text writes, you can control this
with standard Spark APIs and Snowpark Connect for Spark-specific options. CSV and JSON writes don’t support these controls: Snowflake
always determines the file count and size.

### `coalesce(1)` for a single output file

For Parquet and text writes, the most common Spark idiom for producing one output file is honored:

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
Snowflake file. For CSV and JSON writes, `coalesce(1)` is ignored, and the write can produce more than one file.

### `repartition(n)` and output file count

`repartition(n)` doesn’t control the number of output files for non-partitioned writes. Snowflake determines
the file count:

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

For Parquet and text writes, use `snowflake_max_file_size` to limit the size of each file, and `coalesce(1)` or the
`single` option to produce a single file. When you combine `repartition(n)` with `partitionBy`, the
per-partition directory layout takes precedence and Snowflake controls the file count inside each `col=value/`
directory.

### `single` and `snowflake_max_file_size` write options

Snowpark Connect for Spark provides two additional write options for explicit control over output layout. These options are supported
for Parquet and text writes. CSV and JSON writes don’t support them.

| Option | Description |
| --- | --- |
| `single` | Set to `true` to force a single output file regardless of how many input partitions the DataFrame has. Equivalent to `coalesce(1)` for non-partitioned writes. Ignored when used with `partitionBy`. |
| `snowflake_max_file_size` | Maximum size in bytes per output file. Values below 1 MB (1048576) are treated as 1 MB. Larger values reduce the file count; smaller values produce more files. When single-file behavior is active and this option isn’t set, Snowpark Connect for Spark defaults the cap to 1 GB. With `single` set to `true`, the write fails if the output exceeds this size. |

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
and text, and `SNAPPY` for Parquet. For reads, GZIP, BZ2, ZSTD, and DEFLATE compression is auto-detected if not
specified. For BROTLI and RAW\_DEFLATE files, set `compression` explicitly.

For best performance, use splittable compression formats such as `BZ2` (or `SNAPPY` for Parquet). Splittable formats
allow Snowflake to decompress and process file chunks in parallel, which is significantly faster for large files than
non-splittable formats like `GZIP`.

For text, Snowpark Connect for Spark normalizes codec names: `UNCOMPRESSED` becomes `NONE`, and Spark’s `BZIP2` becomes `BZ2`. For CSV
and JSON writes, use Spark codec names: `bzip2`, not `bz2`. Parquet writes always use `SNAPPY`. Compression can also be
inferred from file extensions (`.gz`, `.bz2`, `.snappy`, `.deflate`).

| CSV / JSON | Text | Parquet |
| --- | --- | --- |
| GZIP, BZIP2, DEFLATE, NONE (writes); GZIP, BZ2, BROTLI, ZSTD, DEFLATE, RAW\_DEFLATE, NONE (reads) | GZIP, BZ2, BROTLI, ZSTD, DEFLATE, RAW\_DEFLATE, NONE | SNAPPY (writes); SNAPPY, LZO, NONE (reads, auto-detected) |

Expand

Show lessSee more

XML reads support compressed files such as `.xml.gz`.

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
| `.DS_Store`, other `.*` files | macOS and hidden files |
| Any file starting with `_` or `.` | General Hadoop convention |

Expand

Show lessSee more

This exclusion applies to CSV, JSON, Parquet, and XML reads at any directory depth, including inside
partition subdirectories (for example, `year=2025/_SUCCESS` is skipped). Files ending in `.crc` aren’t excluded
unless their names start with `_` or `.`. Remove them from the read path or exclude them with `pathGlobFilter` (for
example, `*.csv`).

Snowpark Connect for Spark also anchors read paths so that files outside your requested prefix are never picked up.
For example, reading from `@stage/sales/` won’t accidentally include files from `@stage/sales_archive/`.

`pathGlobFilter` doesn’t override automatic exclusion: files whose names start with `_` or `.` are always
skipped, even if the pattern matches them.

## Directory listing (recursiveFileLookup)

Starting in version 1.29.0, Snowpark Connect for Spark supports the Spark `recursiveFileLookup` DataFrameReader option for
`csv`, `json`, `parquet`, `text`, and `xml` reads. The option controls whether reads descend into nested
subdirectories when you pass a directory path.

- `true`: list data files recursively under the read path. Hive-style partition discovery is skipped.
- `false`: list only direct children of the read path (depth-0). Files under Hive-style partition directories
  (`key=value/`) are still read. For Parquet reads, the partition values are also added as columns. CSV, JSON, and XML
  reads don’t add partition columns. See [Partitioned data](#partitioned-data).

When you omit `recursiveFileLookup`, Snowpark Connect for Spark lists only direct children of the read path (depth-0), matching
Apache Spark 3.5. Earlier versions, starting with 1.29.0, listed files recursively by default.

If your workloads read nested data under a directory root that is not Hive-partitioned, set the option to `true`:

Copy code

```
df = spark.read.option("recursiveFileLookup", "true").csv("@my_stage/sales/")
```

For more details about the default change, see
[Directory listing (recursiveFileLookup)](/developer-guide/snowpark-connect/snowpark-connect-compatibility#label-snowpark-connect-compatibility-directory-listing)
in the compatibility guide.

## Format-specific options

CSV, JSON, and XML options that you set through `.option()` are applied with Apache Spark semantics. Parquet and text
options are translated into Snowflake [file format options](/sql-reference/sql/create-file-format) before Snowpark Connect for Spark
executes the read or write operation; their tables show the Snowflake counterpart of each option.

CSV, JSON, and XML reader options that aren’t recognized are ignored without a warning. CSV and JSON writes don’t accept
writer options that they don’t recognize. For Parquet and text, options that don’t have a Snowflake equivalent are ignored,
and Snowpark Connect for Spark logs a warning for each unsupported option.

### Snowpark Connect read options

These options are specific to Snowpark Connect for Spark and aren’t part of open-source Spark. They apply across CSV, JSON, Parquet, and
XML `DataFrameReader` reads. See [Using `input_file_name()` on file reads](#using-input_file_name-on-file-reads) for usage
details.

| Spark option | Default | Notes |
| --- | --- | --- |
| `snowpark.populateFileMetadata` | `false` | Set to `true` to enable `input_file_name()` on CSV, JSON, Parquet, and XML reads. |

Expand

Show lessSee more

### CSV options

| Spark option | Notes |
| --- | --- |
| `sep` / `delimiter` | Default `,`. `delimiter` is an alias for `sep`. A single backslash isn’t allowed as the delimiter; pass two backslashes (`"\\\\"` in Python) instead. |
| `header` | When `true`, the reader uses column names from the first row. When writing, controls whether a header row is written. |
| `quote` | Default `"`. An empty value turns off quoting. A doubled quote (`""`) inside a quoted field is unescaped only when `escape` is set to `"`. On write, values that contain the delimiter are enclosed in quotes, and embedded quotes are escaped with `\`. |
| `escape` | Default `\`. A single `\` and `\\` behave the same. |
| `nullValue` | Default `""`. Empty fields, quoted or unquoted, are read as null, and null values are written as empty fields. `\N` is read as the literal string `\N` unless you set `nullValue` to `\N`. |
| `lineSep` | Default `\n`. The default also handles `\r\n` line endings on read. |
| `encoding` / `charset` | Default `UTF-8`. `charset` is an alias for `encoding`. |
| `multiLine` | Default `false`. Set to `true` to read quoted fields that contain line breaks. |
| `dateFormat` | Java datetime pattern, for example `dd/MM/yyyy`. Snowflake format tokens such as `DD/MM/YYYY` aren’t supported and raise an error. See [Date and timestamp formats](#date-and-timestamp-formats). |
| `timestampFormat` | Java datetime pattern, as for `dateFormat`. The default write format is `yyyy-MM-dd'T'HH:mm:ss.SSSXXX` (for example, `2025-01-09T15:04:05.123-08:00`). |
| `compression` | See [Compression](#compression). |
| `inferSchema` | Default `false` (read only). When `false`, all columns are read as strings. |
| `rowsToInferSchema` | Not supported. The option is ignored without a warning, and the schema is inferred from all rows. |
| `mode` | Default `PERMISSIVE`. Controls error handling on read: `PERMISSIVE`, `DROPMALFORMED`, or `FAILFAST`, as in Apache Spark. In `PERMISSIVE` mode, malformed rows are stored in the `_corrupt_record` column when that column is in the schema. |
| `ignoreLeadingWhiteSpace` / `ignoreTrailingWhiteSpace` | Each option trims whitespace from its own side only. |
| `mergeSchema` | When `true`, Snowpark Connect for Spark produces a union schema across files. New columns across files become nullable. Type widening (for example, `INT` to `STRING`) is supported. Multi-file reads with `header = true` produce a union schema whether or not `mergeSchema` or `inferSchema` is set. |
| `pathGlobFilter` | Filters which files to read, using a glob pattern such as `*.csv`. Regular expressions aren’t supported. |
| `recursiveFileLookup` | Controls whether reads descend into nested subdirectories. Defaults to depth-0 listing, matching Apache Spark. See [Directory listing](#label-snowpark-connect-file-io-recursive-file-lookup). |

Expand

Show lessSee more

CSV reads treat backslashes in unquoted fields as literal characters, fill missing trailing fields with null, drop
extra fields, and skip blank lines.

### JSON options

| Spark option | Notes |
| --- | --- |
| `multiLine` | Default `false`. When `true`, the reader handles files that contain a JSON array at the top level or a JSON document that spans multiple lines. |
| `dateFormat` | Java datetime pattern, for example `dd/MM/yyyy`. Snowflake format tokens such as `DD/MM/YYYY` raise an error. Without this option, ISO dates are read into `DATE` columns of an explicit schema, but schema inference reads date strings as `STRING`. |
| `timestampFormat` | Java datetime pattern, for example `dd/MM/yyyy HH:mm:ss`. Snowflake format tokens aren’t recognized, and values read with them are null, without an error. |
| `encoding` | Default `UTF-8`. Encodings other than UTF-8 require `lineSep`. |
| `mode` | Default `PERMISSIVE`. Controls error handling on read: `PERMISSIVE`, `DROPMALFORMED`, or `FAILFAST`, as in Apache Spark. In `PERMISSIVE` mode, malformed records are stored in the `_corrupt_record` column when that column is in the schema. |
| `dropFieldIfAllNull` | When `true`, fields that are null in every sampled row are dropped from the inferred schema. |
| `samplingRatio` | Fraction of rows to sample when inferring the schema. `rowsToInferSchema` isn’t supported for JSON and raises an error; use `samplingRatio` instead. |
| `pathGlobFilter` | Filters which files to read, using a glob pattern such as `*.json`. Regular expressions aren’t supported. |
| `recursiveFileLookup` | Controls whether reads descend into nested subdirectories. Defaults to depth-0 listing, matching Apache Spark. See [Directory listing](#label-snowpark-connect-file-io-recursive-file-lookup). |
| `compression` | See [Compression](#compression). |

Expand

Show lessSee more

JSON writes apply `compression`, `dateFormat`, `timestampFormat`, and `ignoreNullFields`, as in Apache Spark. The default
timestamp write format is `yyyy-MM-dd'T'HH:mm:ss.SSSXXX`. `nullValue` isn’t supported for JSON writes.

### Parquet options

| Spark option | Snowflake file format option | Notes |
| --- | --- | --- |
| `pathGlobFilter` | `PATTERN` | Filters which files to read. The value is passed to Snowflake `PATTERN` and is interpreted as a regular expression, not a glob. For example, use `.*\.parquet` instead of `*.parquet`. |
| `compression` | `COMPRESSION` | `AUTO` for reads. Parquet writes always use `SNAPPY`; the `compression` option is ignored on Parquet writes. |
| `mergeSchema` | (internal) | When `true` and reading from multiple paths, Snowpark Connect for Spark infers the schema from each file and produces a union schema. New columns are added; type widening across files (for example, `INT` to `STRING`) isn’t supported. |
| `rowsToInferSchema` | (internal) | Read only. Default 20000. Controls the sample size used by Snowpark Connect for Spark when discovering complex types (STRUCT, MAP, ARRAY) inside Parquet VARIANT columns. |
| `nullValue` | `NULL_IF` | Write only. Passed to `NULL_IF` on unload. Parquet stores null values natively, so null values stay null in the output files and no string is written. |
| `recursiveFileLookup` | (see [Directory listing](#label-snowpark-connect-file-io-recursive-file-lookup)) | Controls whether reads descend into nested subdirectories. Supported in 1.29.0+. Defaults to depth-0 listing, matching Apache Spark. |

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
| `recursiveFileLookup` | (see [Directory listing](#label-snowpark-connect-file-io-recursive-file-lookup)) | Controls whether reads descend into nested subdirectories. Supported in 1.29.0+. Defaults to depth-0 listing, matching Apache Spark. |

Expand

Show lessSee more

Text writes always set `ESCAPE_UNENCLOSED_FIELD = NONE` and `FILE_EXTENSION = txt`. The DataFrame must
contain exactly one string column.

### XML options (read only)

XML supports schema inference. If no schema is provided, Snowpark Connect for Spark infers the schema from the data by reading
the files and merging field types across all input. XML options are applied with Apache Spark semantics.

| Spark option | Notes |
| --- | --- |
| `rowTag` | Specifies the XML element that maps to a DataFrame row. Defaults to `ROW` if not set. If `rowTag` doesn’t match an element in your data, the read returns no rows. |
| `inferSchema` | Default `true`. When a user schema is provided, Snowpark Connect for Spark forces `inferSchema=false` to keep the read single-pass. |
| `samplingRatio` | Default `1.0`. Fraction of rows to sample when inferring the schema. |
| `mode` | Default `PERMISSIVE`. Controls error handling: `PERMISSIVE`, `DROPMALFORMED`, or `FAILFAST`. Values that can’t be converted to the specified schema type, and rows that fail `rowValidationXSDPath` validation, are handled according to the mode, as in Apache Spark. |
| `columnNameOfCorruptRecord` | Default `_corrupt_record`. Column name used to store malformed rows in `PERMISSIVE` mode. |
| `attributePrefix` | Default `_`. Prefix added to XML attribute names in the DataFrame schema. Can’t equal `valueTag`. |
| `valueTag` | Default `_VALUE`. Tag name for the text content of mixed-content elements. Can’t be empty. |
| `encoding` | Default `UTF-8`. |
| `excludeAttribute` | Default `false`. When `true`, attributes aren’t included in the DataFrame. |
| `ignoreSurroundingSpaces` | Default `false`. When `true`, whitespace around values is trimmed. |
| `ignoreNamespace` | Default `false`. When `true`, namespace prefixes are removed from element names. For namespace-prefixed row tags, set `rowTag` to the prefixed name (for example, `p:item`). |
| `nullValue` | String value to interpret as null. There’s no default, so empty elements are read as empty strings. Set `nullValue` to `""` to read them as null. |
| `pathGlobFilter` | Filters which files to read, using a glob pattern such as `*.xml`. Regular expressions aren’t supported. |
| `recursiveFileLookup` | Controls whether reads descend into nested subdirectories. Defaults to depth-0 listing, matching Apache Spark. See [Directory listing](#label-snowpark-connect-file-io-recursive-file-lookup). |
| `rowValidationXSDPath` | Path to an XSD file on a stage (for example, `@my_stage/schema.xsd`) to validate each XML row against. Local XSD files are automatically uploaded to the stage. Rows that fail validation are handled according to the `mode` setting. |

Expand

Show lessSee more

## Date and timestamp formats

For CSV and JSON reads and writes, set `dateFormat` and `timestampFormat` to Java datetime patterns, as in Apache Spark.
Snowflake format tokens such as `DD/MM/YYYY` aren’t supported: for `dateFormat` they raise an error, and for JSON
`timestampFormat` they produce null values without an error.

The following table shows common patterns and their output for the timestamp `2025-01-09 15:04:05.123456` in the
`America/Los_Angeles` time zone:

| Pattern | Meaning | Output |
| --- | --- | --- |
| `yyyy` | Four-digit year | `2025` |
| `yy` | Two-digit year | `25` |
| `MM` | Zero-padded month | `01` |
| `MMM` | Abbreviated month name | `Jan` |
| `dd` | Zero-padded day of month | `09` |
| `d` | Day of month, not padded | `9` |
| `EEEE` | Full day name (writes only; reads that use `EEEE` raise an error) | `Thursday` |
| `HH` | 24-hour clock (00-23) | `15` |
| `hh` | 12-hour clock (01-12) | `03` |
| `h` | 12-hour clock, not padded | `3` |
| `mm` | Minutes | `04` |
| `ss` | Seconds | `05` |
| `SSS` | Fractional seconds (milliseconds) | `123` |
| `SSSSSS` | Fractional seconds (microseconds) | `123456` |
| `a` | AM/PM marker | `PM` |
| `Z` | Time zone offset without a colon | `-0800` |
| `XXX` / `xxx` | Time zone offset with a colon | `-08:00` |

Expand

Show lessSee more

When you don’t set `timestampFormat`, CSV and JSON writes use Spark’s default, `yyyy-MM-dd'T'HH:mm:ss.SSSXXX` (for
example, `2025-01-09T15:04:05.123-08:00`).

## Partitioned data

Snowpark Connect for Spark supports Hive-style `col=value/` directory layouts for Parquet reads and writes, and for CSV and JSON
writes.

Note

CSV, JSON, and XML reads don’t support Hive-style partition discovery: files under `col=value/` directories are read,
but partition columns that exist only in directory names aren’t added to the DataFrame. Because Snowpark Connect for Spark writes the
partition columns into the data files, CSV and JSON data that Snowpark Connect for Spark writes with `partitionBy` keeps those
columns when you read it back. For other partitioned CSV and JSON data, see
[Migrate Snowpark Connect for Spark file I/O to version 1.51.0 (Preview)](/developer-guide/snowpark-connect/snowpark-connect-file-io-migrate).

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
- Partition value types are inferred from the observed values: all integers become `LongType`, all
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
Iceberg table writes. For stage-based file writes, use the session configuration shown in the previous example.
