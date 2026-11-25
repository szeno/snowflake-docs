# Migrate Snowpark Connect for Spark file I/O to version 1.51.0 (*Preview*)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Starting in version 1.51.0, Snowpark Connect for Spark uses the next generation file reader and writer for CSV and JSON reads and
writes and for XML reads. Parquet and text reads and writes don’t change.

This topic lists the changes to validate when you upgrade an existing workload from 1.50.0 or earlier, and shows how to
update your code. Many changes make results match Apache Spark more closely, but they can still change the schema, row
count, or values that your workload gets. For the full 1.51.0 behavior, see
[File I/O with Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-file-io). For the 1.50.0 and earlier behavior, see
[File I/O with Snowpark Connect for Spark 1.50.0 and earlier](/developer-guide/snowpark-connect/snowpark-connect-file-io-previous).

## Before you upgrade

Run your CSV, JSON, and XML reads and writes on 1.51.0 against representative data, and compare these results with
your current version:

- The full schema, including column names, column order, data types, and partition columns.
- The collected rows and row counts, not only `count()`.
- Null values compared with empty strings, especially in nested columns and in columns that use `nullValue`.
- Behavior for malformed input, corrupt files, and the read `mode` you use.
- The options that you set. Several options that had no effect in 1.50.0 and earlier are applied in 1.51.0, and some
  write options are no longer supported.
- The files that your writes produce: their number, names, compression, and layout.

## Changes for CSV, JSON, and XML reads

### Partition columns aren’t added from directory names

For layouts such as `year=2024/month=1/`, 1.50.0 and earlier added `year` and `month` columns to CSV and JSON reads.
In 1.51.0, CSV, JSON, and XML reads still read the files under those directories but don’t add the partition columns,
so filters and joins on those columns don’t work. Parquet reads still add partition columns.

To keep the partition values, derive them from the file path:

Copy code

```
from pyspark.sql.functions import input_file_name, regexp_extract

df = (
    spark.read
    .option("header", "true")
    .option("snowpark.populateFileMetadata", "true")
    .csv("@my_stage/sales/")
    .withColumn("year", regexp_extract(input_file_name(), r"year=(\d+)", 1).cast("int"))
)
```

Alternatively, store the partition values as columns inside the files. Don’t test only with partitioned files that
Snowpark Connect for Spark wrote: those files include the partition columns in the data and hide this change.

### `pathGlobFilter` takes a glob, not a regular expression

In 1.50.0 and earlier, CSV, JSON, and XML reads passed `pathGlobFilter` to Snowflake as a regular expression. In 1.51.0,
the value is a glob pattern, as in Apache Spark. A regular expression usually matches no files, and the read fails
with `UNABLE_TO_INFER_SCHEMA`.

Copy code

```
# 1.50.0 and earlier
df = spark.read.option("pathGlobFilter", r".*\.csv").csv("@my_stage/data/")

# 1.51.0
df = spark.read.option("pathGlobFilter", "*.csv").csv("@my_stage/data/")
```

Parquet reads still take a regular expression.

### Repeated input paths are read once

For a directory that contains two rows, reading the path list `[A, A]` returned four rows in 1.50.0 and earlier and
returns two rows in 1.51.0. Reading `[A, A, A]` also returns two rows. This removes repeated paths, not duplicate
records within a file. Check code that builds path lists or that repeats inputs on purpose.

### Wildcard paths that failed can return an empty result

In testing, a CSV read of `dir/*.csv` failed in 1.50.0 and earlier but returns zero rows without an error in 1.51.0.
Paths with a wildcard in the file extension and paths with brace alternatives (such as `{a,b}`) can fail. To select
files by name, read the directory and use `pathGlobFilter`:

Copy code

```
df = spark.read.option("pathGlobFilter", "*.csv").csv("@my_stage/dir/")
```

### `input_file_name()` returns the fully qualified stage path

With `snowpark.populateFileMetadata=true`, 1.50.0 and earlier returned a path relative to the stage, such as
`data/file.csv`, for CSV and JSON reads and an empty string for XML reads. In 1.51.0, CSV, JSON, and XML reads return the
fully qualified stage path, such as `@my_db.my_schema.my_stage/data/file.csv`. Parquet reads still return the relative
path. Check audit columns, routing based on file names, and lineage calculations that parse the path.

To get the path relative to the stage, remove the stage prefix:

Copy code

```
from pyspark.sql.functions import input_file_name, regexp_replace

df = df.withColumn("source_file", regexp_replace(input_file_name(), r"^@[^/]+/", ""))
```

### Options follow Apache Spark semantics

In 1.50.0 and earlier, CSV and JSON options were translated into Snowflake file format options. In 1.51.0, they’re
applied with Apache Spark semantics. Options that had no effect are applied, and some Snowflake-specific values no
longer work:

- **Date and timestamp formats**: Use Java datetime patterns. Snowflake tokens such as `DD/MM/YYYY` raise an error for
  `dateFormat`, and return null for JSON `timestampFormat`, without an error.

  Copy code

  ```
  # 1.50.0 and earlier (JSON accepted Snowflake tokens)
  df = spark.read.option("timestampFormat", "DD/MM/YYYY HH24:MI:SS").json("@my_stage/events/")

  # 1.51.0
  df = spark.read.option("timestampFormat", "dd/MM/yyyy HH:mm:ss").json("@my_stage/events/")
  ```
- **`rowsToInferSchema`**: Not supported. JSON reads raise an error, and CSV and XML reads ignore the option without a
  warning. Use `samplingRatio`, or supply an explicit schema. `samplingRatio` isn’t a row-count equivalent, so compare
  the inferred schema on representative data.

  Copy code

  ```
  # 1.50.0 and earlier
  df = spark.read.option("rowsToInferSchema", "1000").json("@my_stage/events/")

  # 1.51.0
  df = spark.read.option("samplingRatio", "0.1").json("@my_stage/events/")
  ```
- **Unknown options**: Unknown reader options are ignored without a warning. In 1.50.0 and earlier, Snowpark Connect for Spark logged
  a warning.
- **`mode`**: `PERMISSIVE`, `DROPMALFORMED`, and `FAILFAST` behave as in Apache Spark. `FAILFAST` raises a Spark
  malformed-record error (for CSV, `MALFORMED_RECORD_IN_PARSING`) instead of a Snowflake `ON_ERROR` error. Update error
  handlers that match the error text.

## CSV read changes

**Null values and quotes**:

- `\N` is read as the literal string `\N` instead of null. If your files use `\N` for null values, set
  `.option("nullValue", "\\N")`.
- A quoted empty field (`""`) is read as null instead of an empty string.
- A doubled quote inside a quoted field (`"say ""hi"""`) is unescaped only when you set `.option("escape", "\"")`.
  In 1.50.0 and earlier, it was unescaped by default.

**Whitespace trimming**: `ignoreLeadingWhiteSpace` and `ignoreTrailingWhiteSpace` each trim only their own side. In
1.50.0 and earlier, either option trimmed both sides. To keep the earlier behavior, set both options to `true`.

**Schema inference**:

- Integer columns are inferred as `IntegerType` instead of `LongType`, and an explicit `IntegerType` stays `int`.
- Values such as `y` and `n` stay strings instead of being inferred as `BOOLEAN`.
- Multi-file reads with `header=true` merge the columns by name even when `inferSchema` isn’t set.
- When files in a read have different headers, Snowpark Connect for Spark returns the union of the columns, with nulls where a column
  is absent. In 1.50.0 and earlier, it kept one file’s header and could return nulls for values in columns with other
  names. Column order can also differ between repeated reads when inferred columns tie for position. Select the columns
  you need by name instead of relying on `SELECT *` or position.

**Delimiters**: A single backslash isn’t allowed as the delimiter. Pass two backslashes instead:
`.option("sep", "\\\\")` in Python.

**Comments, malformed rows, and parser limits**:

- With the `comment` option set, comment lines are skipped. In 1.50.0 and earlier, they were returned as rows. Remove
  any filtering that you added to drop comment lines.
- In a tested `DROPMALFORMED` read, 1.50.0 and earlier collected four rows, and 1.51.0 collects zero, as Apache Spark
  does.
- With `maxCharsPerColumn` set, the limit is enforced and an oversized field fails the read. Setting
  `ignoreCorruptFiles=true` doesn’t skip that failure.

**Options that were ignored are applied**: `charToEscapeQuoteEscaping`, `unescapedQuoteHandling`, `locale` (for
decimals), `timestampNTZFormat`, `enableDateTimeParsingFallback`, `maxColumns`, and `samplingRatio`. Review jobs that
set these options: earlier runs might have succeeded only because the options were ignored.

## JSON read changes

**Schema inference**:

- Signed 64-bit integers are inferred as `LongType` instead of `DecimalType`.
- Arrays stay arrays instead of becoming strings, and strings that look like booleans stay strings.
- Date strings are inferred as `STRING` instead of `DATE` unless you declare a `DATE` column or set `dateFormat`.
- Files with different fields are merged by name. In a tested read, 1.50.0 and earlier failed with an invalid identifier
  error.
- The extra null row that some `multiLine=true` reads returned in 1.50.0 and earlier doesn’t appear.

**Field names that differ only in case**: With case-insensitive settings, files that use names such as `name` and
`NAME` produced three columns in 1.50.0 and earlier, and produce six or nine columns in 1.51.0, with values spread across
them. Normalize field names or select the columns you need before filters, joins, and writes.

**Comments**: With `allowComments=true`, `/* */` and `//` comments are skipped. In 1.50.0 and earlier, the option was
ignored. In testing, a file that returned three rows in 1.50.0 returns two in 1.51.0.

**Options that were ignored are applied**: `locale`, `timestampNTZFormat`, `enableDateTimeParsingFallback`,
`allowNonNumericNumbers`, and `samplingRatio`. They can change timestamp values, `NaN` and `Infinity` parsing, and
inferred schemas.

## XML read changes

**Empty and missing elements**:

- Empty string elements such as `<a></a>` and `<a/>` are read as `''` instead of null, because `nullValue` has no
  default. To read them as null, set `.option("nullValue", "")` or `.option("treatEmptyValuesAsNulls", "true")`.
- A missing nested element returns null instead of a struct whose fields are all null, or an array with one null
  element (`[NULL]`). `isNull()` filters, counts, and `size()` results on nested columns can change.

**Invalid values follow the read mode**: With an explicit schema, a value that can’t be converted (for example, `abc`
for an integer) failed the whole read in 1.50.0 and earlier with `100071 Failed to cast variant value`, in every mode.
In 1.51.0, `PERMISSIVE` returns the row with that field set to null and the raw record in the corrupt record column,
`DROPMALFORMED` drops the row, and `FAILFAST` fails the read. Fields declared `NOT NULL` are reported as nullable.

**String columns that contain child elements return XML text**: When a field declared as `StringType` contains child
elements, 1.50.0 and earlier returned JSON, such as `{"x":"1"}`. 1.51.0 returns the element’s inner XML. Calls to
`from_json` or `get_json_object` on those columns stop working. Declare a struct schema instead:

Copy code

```
from pyspark.sql.types import StructType, StructField, StringType

schema = StructType([
    StructField("id", StringType()),
    StructField("detail", StructType([StructField("x", StringType())])),
])
df = spark.read.format("xml").option("rowTag", "record").schema(schema).load("@my_stage/exports/")
```

**Options that were ignored are applied**: `dateFormat`, `timestampFormat`, `timestampNTZFormat`,
`treatEmptyValuesAsNulls`, `wildcardColName`, `excludeAttribute`, and `ignoreSurroundingSpaces`. For example, with
`ignoreSurroundingSpaces=true`, `" 5 "` is trimmed and inferred as a number. With `ignoreNamespace=true` and a prefixed
`rowTag` such as `p:item`, columns are returned without prefixes and with their values. In 1.50.0 and earlier, those
columns were null.

**Reads that failed return results**: 1.50.0 and earlier failed on `.xml.gz` files, on a `rowTag` that matched no
element, and on a directory with no XML file. 1.51.0 reads the compressed file and returns an empty DataFrame in the
other cases. If your pipeline used those failures to detect missing input, check row counts explicitly.

**Hidden files are skipped**: `.xml` files whose names start with `_` or `.` are skipped, as for the other formats.

## CSV and JSON write changes

### Bucketed file writes aren’t supported

`bucketBy` and `sortBy` aren’t supported for CSV and JSON file writes. In 1.50.0 and earlier, they were silently
ignored, and the files were written without bucketing or sorting. Remove these calls from CSV and JSON file writes.
`partitionBy` works the same as in 1.50.0 and earlier.

Copy code

```
# 1.50.0 and earlier: bucketBy was silently ignored
df.write.bucketBy(4, "id").sortBy("id").csv("@my_stage/out/")

# 1.51.0
df.write.csv("@my_stage/out/")
```

### Output file count and size options aren’t supported

The `single` and `snowflake_max_file_size` options aren’t supported for CSV and JSON writes, and `coalesce(1)` is
ignored, so a
large write can produce more than one file. Remove these options from CSV and JSON writes, and make the code that reads
the output accept multiple files. To write a single file, write Parquet or text instead, where these options still work.

Copy code

```
# 1.50.0 and earlier
df.write.option("single", "true").csv("@my_stage/out/report/")

# 1.51.0: remove the option and read the whole directory downstream
df.write.csv("@my_stage/out/report/")
```

### Fewer compression codecs

CSV and JSON writes support only `gzip`, `bzip2`, `deflate`, and `none` (or `uncompressed`). The `bz2`, `brotli`, `zstd`,
and `raw_deflate` values aren’t supported.

Copy code

```
# 1.50.0 and earlier
df.write.option("compression", "bz2").csv("@my_stage/out/")

# 1.51.0
df.write.option("compression", "bzip2").csv("@my_stage/out/")
```

### Save modes detect existing files

- `error` (the default) fails with `PATH_ALREADY_EXISTS` when the target path already contains files. In 1.50.0 and
  earlier, the write added files alongside the existing ones. To keep that behavior, set `mode("append")`.
- `ignore` skips the write when the target path already contains files. In 1.50.0 and earlier, `ignore` raised an
  error.

### Output format follows Apache Spark

- **Timestamps**: The default timestamp format is `yyyy-MM-dd'T'HH:mm:ss.SSSXXX` (for example,
  `2025-01-09T15:04:05.123-08:00`) instead of `yyyy-MM-dd HH:mm:ss.SSSSSS`. To keep the earlier format, set
  `.option("timestampFormat", "yyyy-MM-dd HH:mm:ss.SSSSSS")`.
- **Date patterns**: Single-letter patterns such as `d` write unpadded values (`9` instead of `09`), and `EEEE` writes
  the full day name (`Thursday` instead of `Thu`).
- **JSON `dateFormat` and `timestampFormat`**: These options are applied. In 1.50.0 and earlier, they were ignored.
- **JSON `nullValue`**: Not supported for JSON writes, so remove it.
- **CSV null values and quotes**: Null values are written as empty fields instead of `\N`. Values that contain the
  delimiter are enclosed in quotes, and embedded quotes are escaped with `\`.
- **Unknown writer options**: Not supported, so remove them. In 1.50.0 and earlier, they were ignored with a
  warning.

## Files written by earlier versions

JSON files that Snowpark Connect for Spark 1.50.0 or earlier wrote can read back differently in 1.51.0:

- **Null array elements**: Earlier versions could write an array that contains a null element as `["c",undefined,"d"]`
  instead of valid JSON `["c",null,"d"]`. 1.51.0 rejects that record, as Apache Spark does: in a `PERMISSIVE` read,
  every data field in the record becomes null, and the raw text appears in the `_corrupt_record` column. Regenerate the
  files. Don’t replace `undefined` with a text substitution, because the same text can appear inside JSON strings.
- **Timestamps**: Earlier versions could write timestamps as RFC 822 strings. With an explicit `timestamp` or
  `timestamp_ntz` schema, 1.51.0 reads them as null. Inspect the timestamp strings in your files and set a matching
  `timestampFormat`, or regenerate the files.

Validate both cases with files from your workload before you upgrade.
