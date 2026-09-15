# Copy data from a Google Cloud Storage stage

Load data from your staged files into the target table.

## Load your data

Execute [COPY INTO <table>](/sql-reference/sql/copy-into-table) to load your data into the target table.

Note

Loading data requires a [warehouse](/user-guide/warehouses). If you are using a warehouse that is
not configured to auto resume, execute [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) to resume the warehouse. Note
that starting the warehouse could take up to five minutes.

> Copy code
>
> ```
> ALTER WAREHOUSE mywarehouse RESUME;
> ```

Important

The list of objects returned for an external stage may include one or more “directory blobs”; essentially, paths that end in a forward slash character (`/`), e.g.:

Copy code

```
LIST @my_gcs_stage;

+---------------------------------------+------+----------------------------------+-------------------------------+
| name                                  | size | md5                              | last_modified                 |
|---------------------------------------+------+----------------------------------+-------------------------------|
| my_gcs_stage/load/                    |  12  | 12348f18bcb35e7b6b628ca12345678c | Mon, 11 Sep 2019 16:57:43 GMT |
| my_gcs_stage/load/data_0_0_0.csv.gz   |  147 | 9765daba007a643bdff4eae10d43218y | Mon, 11 Sep 2019 18:13:07 GMT |
+---------------------------------------+------+----------------------------------+-------------------------------+
```

These blobs are listed when directories are created in the Google Cloud console rather than using any other tool provided by Google.

COPY statements that reference a stage can fail when the object list includes directory blobs. To avoid errors, we recommend using file pattern matching to identify the files for inclusion (i.e. the PATTERN clause) when the file list for a stage includes directory blobs. For an example, see [Load data using pattern matching](#load-data-using-pattern-matching) (in this topic). Alternatively, set ON\_ERROR = SKIP\_FILE in the COPY statement.

### Load data using pattern matching

The following example loads data from files in the named `my_gcs_stage` stage created in [Configure an integration for Google Cloud Storage](/user-guide/data-load-gcs-config). Using pattern matching, the statement only loads files whose names start with the string `sales`:

> Copy code
>
> ```
> COPY INTO mytable
>   FROM @my_gcs_stage
>   PATTERN='.*sales.*.csv';
> ```

Note that file format options are not specified because a named file format was included in the stage definition.

### Load data using a path / prefix

The following example loads all files with the `data/files` path (i.e. prefix) in your Cloud Storage bucket using the named `my_csv_format` file format created in [Preparing to load data](/user-guide/data-load-prepare). Note that a path can be combined with pattern matching:

> Copy code
>
> ```
> COPY INTO mytable
>   FROM @my_gcs_stage/mybucket/data/files
>   FILE_FORMAT = (FORMAT_NAME = my_csv_format);
> ```

### Load data using ad hoc file format options

The following ad hoc example loads data from all files in the Cloud Storage bucket. The COPY command
specifies file format options instead of referencing a named file format. This example loads CSV files
with a pipe (`|`) field delimiter. The COPY command skips the first line in the data files.

Note that the storage integration reference is required in ad hoc data loads; that is, when the
COPY statement does not reference a stage:

Copy code

```
COPY INTO mytable
  FROM 'gcs://mybucket/data/files'
  STORAGE_INTEGRATION = myint
  FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = '|' SKIP_HEADER = 1);
```

## Validate your data

Before loading your data, you can validate that the data in the uploaded files will load correctly.

To validate data in an uploaded file, execute [COPY INTO <table>](/sql-reference/sql/copy-into-table) in validation mode using
the VALIDATION\_MODE parameter. The VALIDATION\_MODE parameter returns errors that it encounters in the file. You
can then modify the data in the file to ensure it loads without error.

In addition, [COPY INTO <table>](/sql-reference/sql/copy-into-table) provides the ON\_ERROR copy option to specify an action
to perform if errors are encountered in a file during loading.

## Monitor data loads

Snowflake retains historical data for COPY INTO commands executed within the previous 14 days. The metadata can be used to monitor and
manage the loading process, including deleting files after upload completes:

- Monitor the status of each [COPY INTO <table>](/sql-reference/sql/copy-into-table) command on the **Query History** page of Snowsight.
- Use the [LOAD\_HISTORY](/sql-reference/info-schema/load_history) Information Schema view to retrieve the history of data loaded into tables
  using the COPY INTO command.

## Copy files from one stage to another

Use the [COPY FILES](/sql-reference/sql/copy-files) command to organize data into a single location
by copying files from one named stage to another.

The following example copies all of the files from a source stage (`src_stage`) to a target stage (`trg_stage`):

Copy code

```
COPY FILES
  INTO @trg_stage
  FROM @src_stage;
```

You can also specify a list of file names to copy, or copy files by using pattern matching.
For information, see the [COPY FILES examples](/sql-reference/sql/copy-files#label-copy-files-examples).
