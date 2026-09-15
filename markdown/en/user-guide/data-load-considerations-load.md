# Loading data

This topic provides best practices, general guidelines, and important considerations for loading staged data.

## Options for selecting staged data files

The COPY command supports several options for loading data files from a stage:

- By path (internal stages) / prefix (Amazon S3 bucket). See [Organizing data by path](/user-guide/data-load-considerations-stage#label-organizing-data-by-path) for information.
- Specifying a list of specific files to load.
- Using pattern matching to identify specific files by pattern.

These options enable you to copy a fraction of the staged data into Snowflake with a single command. This allows you to execute concurrent COPY statements that match a subset of files, taking advantage of parallel operations.

### Lists of files

The [COPY INTO <table>](/sql-reference/sql/copy-into-table) command includes a FILES parameter to load files by specific name.

Tip

Of the three options for identifying/specifying data files to load from a stage, providing a discrete list of files is
generally the fastest; however, the FILES parameter supports a maximum of 1,000 files, meaning a COPY command executed with the FILES
parameter can only load up to 1,000 files.

For example:

> Copy code
>
> ```
> COPY INTO load1 FROM @%load1/data1/ FILES=('test1.csv', 'test2.csv', 'test3.csv')
> ```

File lists can be combined with paths for further control over data loading.

### Pattern matching

The [COPY INTO <table>](/sql-reference/sql/copy-into-table) command includes a PATTERN parameter to load files using a regular expression.

For example:

> Copy code
>
> ```
> COPY INTO people_data FROM @%people_data/data1/
>    PATTERN='.*person_data[^0-9{1,3}$$].csv';
> ```

Pattern matching using a regular expression is generally the slowest of the three options for identifying/specifying
data files to load from a stage; however, this option works well if you exported your files in
named order from your external application and want to batch load the files in the same order.

Pattern matching can be combined with paths for further control over data loading.

Note

The regular expression is applied differently to bulk data loads versus Snowpipe data loads.

- Snowpipe trims any path segments in the stage definition from the storage location and applies the regular expression to any remaining
  path segments and filenames. To view the stage definition, execute the [DESCRIBE STAGE](/sql-reference/sql/desc-stage) command for the stage.
  The URL property consists of the bucket or container name and zero or more path segments. For example, if the FROM location in a COPY
  INTO *<table>* statement is `@s/path1/path2/` and the URL value for stage `@s` is `s3://mybucket/path1/`, then Snowpipe trims
  `s3://mybucket/path1/path2/` from the storage location in the FROM clause and applies the regular expression to the remaining filenames in the path.
- Bulk data load operations apply the regular expression to the entire storage location in the FROM clause.

Snowflake recommends that you enable cloud event filtering for Snowpipe to reduce costs, event noise, and latency. Only use the PATTERN option when your cloud provider’s event filtering feature is not sufficient. For more information about configuring event filtering for each cloud provider, see the following pages:

- [Configuring event notifications using object key name filtering - Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-filtering.html)
- [Understand event filtering for Event Grid subscriptions - Azure](https://docs.microsoft.com/en-us/azure/event-grid/event-filtering)
- [Filtering messages - Google Pub/Sub](https://cloud.google.com/pubsub/docs/filtering)

## Executing parallel COPY statements that reference the same data files

When a COPY statement is executed, Snowflake sets a load status in the table metadata for the data files referenced in the statement. This prevents parallel COPY statements from loading the same files into the table, avoiding data duplication.

When processing of the COPY statement is completed, Snowflake adjusts the load status for the data files as appropriate. If one or more data files fail to load, Snowflake sets the load status for those files as load failed. These files are available for a subsequent COPY statement to load.

If your workload consists of highly concurrent COPY statements loading data into the same table, use Snowpipe, because the service is designed to handle concurrent COPY statements and can better take advantage of parallel operations including table metadata management. You might need to consider migrating existing COPY statement workloads to Snowpipe over time, possibly due to changes in data volume and the frequency of loads executed. In the meantime, you can space out your COPY statements to reduce concurrency, which might lead to better performance.

## Loading older files

This section describes how the [COPY INTO <table>](/sql-reference/sql/copy-into-table) command prevents data duplication differently based on whether the load status for a file is known or unknown. If you partition your data in stages using logical, granular paths by date (as recommended in [Organizing data by path](/user-guide/data-load-considerations-stage#label-organizing-data-by-path)) and load data within a short period of time after staging it, this section largely does not apply to you. However, if the COPY command skips older files (i.e. historical data files) in a data load, this section describes how to bypass the default behavior.

### Load metadata

Snowflake maintains detailed metadata for each table into which data is loaded, including:

- Name of each file from which data was loaded
- File size
- ETag for the file
- Number of rows parsed in the file
- Timestamp of the last load for the file
- Information about any errors encountered in the file during loading

This load metadata expires after 64 days. If the LAST\_MODIFIED date for a staged data file is less than or equal to 64 days, the COPY command can determine its load status for a given table and prevent reloading (and data duplication). The LAST\_MODIFIED date is the timestamp when the file was initially staged or when it was last modified, whichever is later.

If the LAST\_MODIFIED date is older than 64 days, the load status is still known if either of the following events occurred less than or equal to 64 days prior to the current date:

> - The file was loaded successfully.
> - The initial set of data for the table (i.e. the first batch after the table was created) was loaded.

However, the COPY command cannot definitively determine whether a file has been loaded already if the LAST\_MODIFIED date is older than 64 days and the initial set of data was loaded into the table more than 64 days earlier (and if the file was loaded into the table, that also occurred more than 64 days earlier). In this case, to prevent accidental reload, the command skips the file by default.

### Workarounds

To load files whose metadata has expired, set the LOAD\_UNCERTAIN\_FILES copy option to true. The copy option references load metadata, if available, to avoid data duplication, but also attempts to load files with expired load metadata.

Alternatively, set the FORCE option to load all files, ignoring load metadata if it exists. Note that this option reloads files, potentially duplicating data in a table.

### Examples

![](/static/images/data-load-status1.svg)

In this example:

- A table is created on **March 1**, and the initial table load occurs on the same day.
- 64 days pass. On **May 4**, the load metadata expires.
- A file is staged and loaded into the table on **July 1** and **2**, respectively. Because the file was staged one day prior to being loaded, the LAST\_MODIFIED date was within 64 days. The load status was known. There are no data or formatting issues with the file, and the COPY command loads it successfully.
- 64 days pass. On **September 3**, the LAST\_MODIFIED date for the staged file exceeds 64 days. On **September 4**, the load metadata for the successful file load expires.
- An attempt is made to reload the file into the same table on **November 1**. Because the COPY command cannot determine whether the file has been loaded already, the file is skipped. The LOAD\_UNCERTAIN\_FILES copy option (or the FORCE copy option) is required to load the file.

![](/static/images/data-load-status2.svg)

In this example:

- A file is staged on **March 1**.
- 64 days pass. On **May 4**, the LAST\_MODIFIED date for the staged file exceeds 64 days.
- A new table is created on **September 29**, and the staged file is loaded into the table. Because the initial table load occurred less than 64 days prior, the COPY command can determine that the file had not been loaded already. There are no data or formatting issues with the file, and the COPY command loads it successfully.

## JSON data: Removing “null” values

In a VARIANT column, NULL values are stored as a string containing the word “null,” not the SQL NULL value. If the “null” values in your JSON documents indicate missing values and have no other special meaning, we recommend setting the file format option STRIP\_NULL\_VALUES to TRUE for the [COPY INTO <table>](/sql-reference/sql/copy-into-table) command when loading the JSON files. Retaining the “null” values often wastes storage and slows query processing.

## CSV data: Trimming leading spaces

If your external software exports fields enclosed in quotes but inserts a leading space before the opening quotation character for each field, Snowflake reads the leading space rather than the opening quotation character as the beginning of the field. The quotation characters are interpreted as string data.

Use the TRIM\_SPACE [file format](/sql-reference/sql/create-file-format) option to remove undesirable spaces during the data load.

For example, each of the following fields in an example CSV file includes a leading space:

Copy code

```
"value1", "value2", "value3"
```

The following COPY command trims the leading space and removes the quotation marks enclosing each field:

Copy code

```
COPY INTO mytable
FROM @%mytable
FILE_FORMAT = (TYPE = CSV TRIM_SPACE=true FIELD_OPTIONALLY_ENCLOSED_BY = '0x22');

SELECT * FROM mytable;

+--------+--------+--------+
| col1   | col2   | col3   |
+--------+--------+--------+
| value1 | value2 | value3 |
+--------+--------+--------+
```
