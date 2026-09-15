# Copying data from an S3 stage

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

The following example loads data from files in the named `my_ext_stage` stage created in [Create an S3 stage](/user-guide/data-load-s3-create-stage). Using pattern matching, the statement only loads files whose names start with the string `sales`:

> Copy code
>
> ```
> COPY INTO mytable
>   FROM @my_ext_stage
>   PATTERN='.*sales.*.csv';
> ```

Note that file format options are not specified because a named file format was included in the stage definition.

The following example loads all files prefixed with `data/files` in your S3 bucket using the named `my_csv_format` file format created in [Preparing to load data](/user-guide/data-load-prepare):

> Copy code
>
> ```
> COPY INTO mytable
>   FROM s3://mybucket/data/files credentials=(AWS_KEY_ID='$AWS_ACCESS_KEY_ID' AWS_SECRET_KEY='$AWS_SECRET_ACCESS_KEY')
>   FILE_FORMAT = (FORMAT_NAME = my_csv_format);
> ```

The following ad hoc example loads data from all files in the S3 bucket. The COPY command specifies file format options instead of referencing a named file format. This example loads CSV files with a pipe (`|`) field delimiter. The COPY command skips the first line in the data files:

Copy code

```
COPY INTO mytable
  FROM s3://mybucket credentials=(AWS_KEY_ID='$AWS_ACCESS_KEY_ID' AWS_SECRET_KEY='$AWS_SECRET_ACCESS_KEY')
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
