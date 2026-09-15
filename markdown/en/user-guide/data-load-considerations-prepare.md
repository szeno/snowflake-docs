# Preparing your data files

This topic provides best practices, general guidelines, and important considerations for preparing your data files for loading.

## File sizing best practices

For best load performance and to avoid [size limitations](#label-size-limits-for-database-objects), consider
the following data file sizing guidelines. Note that these recommendations apply to bulk data loads as well as
continuous loading using Snowpipe.

### General file sizing recommendations

The number of load operations that run in parallel can’t exceed the number of data files to be loaded. To optimize the number of parallel operations for a load, we recommend aiming to produce data files roughly 100-250 MB (or larger) in size compressed.

Note

Loading very large files (for example, 100 GB or larger) is not recommended.

If you must load a large file, carefully consider the [ON\_ERROR](/sql-reference/sql/copy-into-table) copy option value. Aborting or
skipping a file due to a small number of errors could result in delays and wasted credits. In addition, if a data loading operation
continues beyond the maximum allowed duration of 24 hours, it could be aborted without any portion of the file being committed.

Aggregate smaller files to minimize the processing overhead for each file. Split larger files into a greater number of smaller files to distribute the load among the compute resources in an active warehouse. The number of data files that are processed in parallel is determined by the amount of compute resources in a warehouse. We recommend splitting large files by line to avoid records that span chunks.

If your data source doesn’t allow exporting data files in smaller chunks, you can use a third-party utility to split large CSV files.

If you are loading large uncompressed CSV files (greater than 128MB) that follow the RFC4180 specification, Snowflake supports parallel scanning of these CSV files when MULTI\_LINE is set to `FALSE`, COMPRESSION is set to `NONE`, and ON\_ERROR is set to `ABORT_STATEMENT` or `CONTINUE`.

#### Linux or macOS

The `split` utility enables you to split a CSV file into multiple smaller files.

**Syntax:**

> Copy code
>
> ```
> split [-a suffix_length] [-b byte_count[k|m]] [-l line_count] [-p pattern] [file [name]]
> ```

For more information, type `man split` in a terminal window.

**Example:**

> Copy code
>
> ```
> split -l 100000 pagecounts-20151201.csv pages
> ```

This example splits a file named `pagecounts-20151201.csv` by line length. Suppose the large single file is 8 GB and contains 10 million lines. Split by 100,000, each of the 100 smaller files is 80 MB (10 million / 100,000 = 100). The split files are named `pagessuffix`.

#### Windows

Windows does not include a native file split utility; however, Windows supports many third-party tools and scripts that can split large data files.

## Size limits for database objects

When you use any of the available methods for [loading data into Snowflake](/user-guide/data-load-overview),
you can store objects with sizes up to the following limits:

| Data type | Storage limit |
| --- | --- |
| ARRAY | 128 MB |
| BINARY | 64 MB |
| GEOGRAPHY | 64 MB |
| GEOMETRY | 64 MB |
| OBJECT | 128 MB |
| VARCHAR | 128 MB |
| VARIANT | 128 MB |

Expand

Show lessSee more

The default size for VARCHAR columns is 16 MB (8 MB for binary). To create tables with column sizes larger than 16 MB,
specify the size explicitly. For example:

Copy code

```
CREATE OR REPLACE TABLE my_table (
  c1 VARCHAR(134217728),
  c2 BINARY(67108864));
```

To use the new limits for VARCHAR columns, you can alter tables to change the column size. For example:

Copy code

```
ALTER TABLE my_table ALTER COLUMN col1 SET DATA TYPE VARCHAR(134217728);
```

To apply the new size to columns of type BINARY in these tables, recreate the tables. You can’t alter the length
of a BINARY column in an existing table.

For columns of type ARRAY, GEOGRAPHY, GEOMETRY, OBJECT, and VARIANT, you can store objects larger than 16 MB
in existing tables and new tables, by default, without specifying the length. For example:

Copy code

```
CREATE OR REPLACE TABLE my_table (c1 VARIANT);
```

If you have procedures and functions that were created in the past and that use VARIANT, VARCHAR, or BINARY values as input,
you might need to recreate them (without specified length) to support objects larger than 16 MB. For example:

Copy code

```
CREATE OR REPLACE FUNCTION udf_varchar(g1 VARCHAR)
  RETURNS VARCHAR
  AS $$
    'Hello' || g1
  $$;
```

For externally managed [Iceberg tables](/user-guide/tables-iceberg-create), the default length for VARCHAR and BINARY columns is 128 MB.
This default length applies to newly created or refreshed tables. If you have tables that were created in the past, smaller limits might
apply to them. You can refresh these tables so that they support larger size limits.

For managed Iceberg tables, the default length for VARCHAR and BINARY columns is 128 MB. Tables that were created before the new size limits
were enabled still have the previous default lengths. To apply the new size to columns of type VARCHAR in these tables, recreate the tables
or alter the columns. The following example alters a column to use the new size limit:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table ALTER COLUMN col1 SET DATA TYPE VARCHAR(134217728);
```

To apply the new size to columns of type BINARY in these tables, recreate the tables. You can’t alter the length
of a BINARY column in an existing table.

### Driver versions that support large objects in the result set

Drivers support objects larger than 16 MB (8 MB for BINARY, GEOMETRY, and GEOGRAPHY). You might need to update your drivers to the
versions that support larger objects. The following driver versions are required:

| Driver | Minimum supported version | Release date |
| --- | --- | --- |
| Snowpark Library for Python | 1.21.0 | August 19, 2024 |
| Snowflake Connector for Python | 3.10.0 | April 29, 2024 |
| JDBC | 3.17.0 | July 8, 2024 |
| ODBC | 3.6.0 | March 17, 2025 |
| Go Snowflake Driver | 1.1.5 | April 17, 2022 |
| .NET | 2.0.11 | March 15, 2022 |
| Snowpark Library for Scala and Java | 1.14.0 | September 14, 2024 |
| Node.js | 1.6.9 | April 21, 2022 |
| Spark connector | 3.0.0 | July 31, 2024 |
| PHP | 3.0.2 | August 29, 2024 |
| Snowflake CLI | 3.0.0 | October 1, 2024 |
| SnowSQL | 1.3.2 | August 12, 2024 |

Expand

Show lessSee more

If you try to use a driver that doesn’t support larger objects, an error similar to the following example is returned:

```
100067 (54000): The data length in result column <column_name> is not supported by this version of the client.
Actual length <actual_size> exceeds supported length of 16777216.
```

## Continuous data loads — that is, Snowpipe — and file sizing

Snowpipe is designed to load new data typically within a minute after a file notification is sent; however, loading can take significantly longer for really large files or in cases where an unusual amount of compute resources is necessary to decompress, decrypt, and transform the new data.

In addition to resource consumption, an overhead to manage files in the internal load queue is included in the utilization costs charged for Snowpipe. This overhead increases in relation to the number of files queued for loading. This overhead charge appears as Snowpipe charges in your billing statement
because Snowpipe is used for event notifications for the automatic external table refreshes.

For the most efficient and cost-effective load experience with Snowpipe, we recommend following the file sizing recommendations in [File sizing best practices](#label-data-load-file-sizing-best-practices) (in this topic). Loading data files roughly 100-250 MB or larger reduces the overhead charge relative to the amount of total data loaded to the point where the overhead cost is immaterial.

If it takes longer than one minute to accumulate MBs of data in your source application, consider creating a new (potentially smaller) data file once per minute. This approach typically leads to a good balance between cost (that is, resources spent on Snowpipe queue management and the actual load) and performance (that is, load latency).

Creating smaller data files and staging them in cloud storage more often than once per minute has the following disadvantages:

- A reduction in latency between staging and loading the data can’t be guaranteed.
- An overhead to manage files in the internal load queue is included in the utilization costs charged for Snowpipe. This overhead increases in relation to the number of files queued for loading.

Various tools can aggregate and batch data files. One convenient option is Amazon Data Firehose. Firehose allows defining both the
desired file size, called the *buffer size*, and the wait interval after which a new file is sent (to cloud storage in this case), called
the *buffer interval*. For more information, see the
[Amazon Data Firehose documentation](https://docs.aws.amazon.com/firehose/latest/dev/create-configure.html). If your source application
typically accumulates enough data within a minute to populate files larger than the recommended maximum for optimal parallel processing,
you could decrease the buffer size to trigger delivery of smaller files. Keeping the buffer interval setting at 60 seconds (the minimum
value) helps avoid creating too many files or increasing latency.

## Preparing delimited text files

Consider the following guidelines when preparing your delimited text (CSV) files for loading:

- UTF-8 is the default character set, however, additional encodings are supported. Use the ENCODING file format option to specify the character set for the data files. For more information, see [CREATE FILE FORMAT](/sql-reference/sql/create-file-format).
- Fields that contain delimiter characters should be enclosed in quotes (single or double). If the data contains single or double quotes, then those quotes must be escaped.
- Carriage returns are commonly introduced on Windows systems in conjunction with a line feed character to mark the end of a line (`\r \n`). Fields that contain carriage returns should also be enclosed in quotes (single or double).
- The number of columns in each row should be consistent.

## Semi-structured data files and subcolumnarization

When semi-structured data is inserted into a VARIANT column, Snowflake uses certain rules to extract as much of the data as possible
to a columnar form. The rest of the data is stored as a single column in a parsed semi-structured structure.

By default, Snowflake extracts a maximum of 200 elements per partition, per table. To increase this limit, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

# Elements that are not extracted

Elements with the following characteristics are not extracted into a column:

- Elements that contain even a single “null” value are not extracted into a column.
  This applies to elements with “null” values and not to elements with missing values, which are represented in columnar form.

  This rule ensures that no information is lost (that is, that the difference between VARIANT “null” values and SQL NULL values is not lost).
- Elements that contain multiple data types. For example:

  The `foo` element in one row contains a number:

  Copy code

  ```
  {"foo":1}
  ```

  The same element in another row contains a string:

  Copy code

  ```
  {"foo":"1"}
  ```

## How extraction impacts queries

When you query a semi-structured element, Snowflake’s execution engine behaves differently according to whether an element was extracted.

- If the element was extracted into a column, the engine scans only the extracted column.
- If the element was not extracted into a column, the engine must scan the entire JSON structure,
  and then for each row traverse the structure to output values. This impacts performance.

To avoid the performance impact for elements that were not extracted, do the following:

- Extract semi-structured data elements containing “null” values into relational columns before you load them.

  Alternatively, if the “null” values in your files indicate missing values and have no other special meaning,
  we recommend setting the [file format option](/sql-reference/sql/create-file-format) STRIP\_NULL\_VALUES to TRUE
  when you load the semi-structured data files. This option removes OBJECT elements or ARRAY elements containing “null” values.
- Ensure each unique element stores values of a single data type that is native to the format (for example, string or number for JSON).

## Numeric data guidelines

- Avoid embedded characters, such as commas (for example, `123,456`).
- If a number includes a fractional component, it should be separated from the whole number portion by a decimal point (for example, `123456.789`).
- Oracle only. The Oracle NUMBER or NUMERIC types allow for arbitrary scale, meaning they accept values with decimal components even if the data type was not defined with a precision or scale. Whereas in Snowflake, columns designed for values with decimal components must be defined with a scale to preserve the decimal portion.

## Date and timestamp data guidelines

- For information on the supported formats for date, time, and timestamp data, see [Date and time input and output formats](/sql-reference/date-time-input-output).
- Oracle only. The Oracle DATE data type can contain date *or* timestamp information. If your Oracle database includes DATE columns that also store time-related information, map these columns to a TIMESTAMP data type in Snowflake rather than DATE.

Note

Snowflake checks temporal data values at load time. Invalid date, time, and timestamp values (for example, `0000-00-00`) produce an error.
