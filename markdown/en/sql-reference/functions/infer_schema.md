Categories:
:   [Table functions](/sql-reference/functions-table)

# INFER\_SCHEMA

Automatically detects the file metadata schema in a set of staged data files that contain semi-structured data and retrieves the column
definitions.

The [GENERATE\_COLUMN\_DESCRIPTION](/sql-reference/functions/generate_column_description) function builds on the INFER\_SCHEMA function output to simplify the
creation of new tables, external tables, or views (using the appropriate [CREATE <object>](/sql-reference/sql/create) command) based on the column
definitions of the staged files.

You can execute the [CREATE TABLE](/sql-reference/sql/create-table), [CREATE EXTERNAL TABLE](/sql-reference/sql/create-external-table), or [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table)
command with the USING TEMPLATE clause to create a new table or external table with the column definitions derived from the
INFER\_SCHEMA function output.

To return structured types (`OBJECT`, `ARRAY`, or `MAP`) for nested data, set the
[INFER\_NESTED\_TYPES](/sql-reference/functions/infer_schema#label-infer-schema-infer-nested-types) argument to `TRUE`.

Note

This function supports Apache Parquet, Apache Avro, ORC, JSON, and CSV files.

## Syntax

Copy code

```
INFER_SCHEMA(
  LOCATION => '{ internalStage | externalStage }'
  , FILE_FORMAT => '<file_format_name>'
  , FILES => ( '<file_name>' [ , '<file_name>' ] [ , ... ] )
  , IGNORE_CASE => TRUE | FALSE
  , MAX_FILE_COUNT => <num>
  , MAX_RECORDS_PER_FILE => <num>
  , KIND => '<kind_name>'
  , INFER_NESTED_TYPES => TRUE | FALSE
)
```

Where:

> Copy code
>
> ```
> internalStage ::=
>     @[<namespace>.]<int_stage_name>[/<path>][/<filename>]
>   | @~[/<path>][/<filename>]
> ```
>
> Copy code
>
> ```
> externalStage ::=
>   @[<namespace>.]<ext_stage_name>[/<path>][/<filename>]
> ```

## Arguments

`LOCATION => '...'`
:   Name of the internal or external stage where the files are stored. Optionally include a path to one or more files in the cloud storage
    location; otherwise, the INFER\_SCHEMA function scans files in all subdirectories in the stage:

    |  |  |
    | --- | --- |
    | `@[namespace.]int_stage_name[/path][/filename]` | Files are in the specified named internal stage. |
    | `@[namespace.]ext_stage_name[/path][/filename]` | Files are in the specified named external stage. |
    | `@~[/path][/filename]` | Files are in the stage for the current user. |
    |  |  |
    | This SQL function supports named stages (internal or external) and user stages only. It does not support table stages. |  |

    Expand

    Show lessSee more

`FILES => ( 'file_name' [ , 'file_name' ] [ , ... ] )`
:   Specifies a list of one or more files (separated by commas) in a set of staged files that contain semi-structured data. The files must already have been staged in either the Snowflake internal location or external location specified in the command. If any of the specified files cannot be found, the query will be aborted.

    The maximum number of files names that can be specified is 1000.

    > Note
    >
    > For external stages only (Amazon S3, Google Cloud Storage, or Microsoft Azure), the file path is set by concatenating the URL in the stage definition and the list of resolved file names.
    >
    > However, Snowflake doesn’t insert a separator implicitly between the path and file names. You must explicitly include a separator (`/`) either at the end of the URL in the stage
    > definition or at the beginning of each file name specified in this parameter.

`FILE_FORMAT => 'file_format_name'`
:   Name of the file format object that describes the data contained in the staged files. For more information, see
    [CREATE FILE FORMAT](/sql-reference/sql/create-file-format).

`IGNORE_CASE => TRUE | FALSE`
:   Specifies whether column names detected from stage files are treated as case sensitive. By default, the value is FALSE, which means that Snowflake preserves the case of alphabetic characters when retrieving column names. If you specify the value as TRUE, column names are treated as case-insensitive and all column names are retrieved as uppercase letters.

    This argument applies only to column names. Field names inside structured types keep the case used in the files.

`MAX_FILE_COUNT => num`
:   Specifies the maximum number of files scanned from stage. This option is recommended for large number of files that have identical schema across files. This option cannot determine which files are scanned. If you want to scan specific files, use the `FILES` option instead.

`MAX_RECORDS_PER_FILE => num`
:   Specifies the maximum number of records scanned per file. This option only applies to CSV and JSON files. We recommend that you use this option for large files. This option might affect the accuracy of schema detection.

`KIND => 'kind_name'`
:   Specifies the kind of file metadata schema that can be scanned from the stage. By default, the value is `STANDARD`, which means that
    the file metadata schema that can be scanned from the stage is for Snowflake tables and the output is Snowflake data types. If you specify
    the value as `ICEBERG`, the schema is for Apache Iceberg tables and the output is Iceberg data types.

    Note

    If you’re inferring Parquet files to create Iceberg tables, we strongly recommend that you set `KIND => 'ICEBERG'`. Otherwise, the
    column definitions returned by the function might be incorrect.

`INFER_NESTED_TYPES => TRUE | FALSE`
:   Specifies whether nested data is inferred as structured types, such as `OBJECT(city TEXT, zip NUMBER(10, 0))`, instead of
    semi-structured types, such as `VARIANT`. By default, the value is `FALSE`.

    This argument affects only the column definitions that the function returns. To have schema evolution add structured columns and
    fields when you load files, also set the
    [INFER\_NESTED\_TYPES](/sql-reference/sql/copy-into-table#label-copy-option-infer-nested-types) copy option to `TRUE`.

    When the argument is `TRUE`, note the following:

    - Parquet files that contain maps whose keys aren’t strings or integers are skipped without a warning. With `KIND => 'ICEBERG'`,
      the function returns an error instead.
    - JSON objects are inferred as `OBJECT`, not `MAP`.
    - ORC `UNION` types, and Avro `UNION` types that have more than one non-null type, are returned as `VARIANT`.
    - ORC map data can’t be loaded into `MAP` columns, so change `MAP` types inferred from ORC files to `VARIANT`.
    - When files contain different types for the same field, `NUMBER` types are widened to fit all values. Other conflicting types are
      returned as `VARIANT`, or as `TEXT` for JSON files.
    - For JSON files, numeric types are sized from the scanned values, so review these types before you create a table. For more
      information, see [Choose column types](/user-guide/data-load-schema-evolution#label-schema-evolution-structured-types-review-types).

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| COLUMN\_NAME | TEXT | Name of a column in the staged files. |
| TYPE | TEXT | Data type of the column. |
| NULLABLE | BOOLEAN | Specifies whether rows in the column can store NULL instead of a value. Currently, the inferred nullability of a column can apply to one data file but not others in the scanned set. |
| EXPRESSION | TEXT | Expression of the column in the format `$1:COLUMN_NAME::TYPE` (primarily for external tables). If IGNORE\_CASE is specified as TRUE, the expression of the column will be in the format `GET_IGNORE_CASE ($1, COLUMN_NAME)::TYPE`. |
| FILENAMES | TEXT | Names of the files that contain the column. |
| ORDER\_ID | NUMBER | Column order in the staged files. |

Expand

Show lessSee more

## Usage notes

- For CSV files, you can define column names by using the file format option `PARSE_HEADER = [ TRUE | FALSE ]`.

  - If the option is set to TRUE, the first row headers will be used to determine column names.
  - The default value FALSE will return column names as c\*, where \* is the position of the column. The SKIP\_HEADER option is not supported with PARSE\_HEADER = TRUE.
  - The PARSE\_HEADER option isn’t supported for external tables.
- For both CSV and JSON files, the following file format options are currently not supported: DATE\_FORMAT, TIME\_FORMAT, and TIMESTAMP\_FORMAT.
- The JSON TRIM\_SPACE file format option is not supported.
- The scientific annotations (e.g. 1E2) in JSON files are retrieved as REAL data type.
- All the variations of timestamp data types are retrieved as TIMESTAMP\_NTZ without any time zone information.
- For both CSV and JSON files, all columns are identified as NULLABLE.
- When the staged files contain nested data, note the following:

  - With `INFER_NESTED_TYPES => FALSE` (the default), only the first level of nesting is supported, and nested columns are
    returned as semi-structured types. With `KIND => 'ICEBERG'`, the function fails instead.
  - With `INFER_NESTED_TYPES => TRUE`, multi-level nesting is supported, and nested columns are returned as structured types. With
    `KIND => 'ICEBERG'`, the function fails if any column would be `VARIANT`. To find these columns, run the function with
    `KIND => 'STANDARD'`.

## Examples

### Snowflake column definitions

Retrieve the Snowflake column definitions for Parquet files in the `mystage` stage:

Copy code

```
-- Create a file format that sets the file type as Parquet.
CREATE FILE FORMAT my_parquet_format
  TYPE = parquet;

-- Query the INFER_SCHEMA function.
SELECT *
  FROM TABLE(
    INFER_SCHEMA(
      LOCATION=>'@mystage'
      , FILE_FORMAT=>'my_parquet_format'
      )
    );

+-------------+---------+----------+---------------------+--------------------------+----------+
| COLUMN_NAME | TYPE    | NULLABLE | EXPRESSION          | FILENAMES                | ORDER_ID |
|-------------+---------+----------+---------------------+--------------------------|----------+
| continent   | TEXT    | True     | $1:continent::TEXT  | geography/cities.parquet | 0        |
| country     | VARIANT | True     | $1:country::VARIANT | geography/cities.parquet | 1        |
| COUNTRY     | VARIANT | True     | $1:COUNTRY::VARIANT | geography/cities.parquet | 2        |
+-------------+---------+----------+---------------------+--------------------------+----------+
```

Similar to the previous example, but specify a single Parquet file in the `mystage` stage:

Copy code

```
-- Query the INFER_SCHEMA function.
SELECT *
  FROM TABLE(
    INFER_SCHEMA(
      LOCATION=>'@mystage/geography/cities.parquet'
      , FILE_FORMAT=>'my_parquet_format'
      )
    );

+-------------+---------+----------+---------------------+--------------------------+----------+
| COLUMN_NAME | TYPE    | NULLABLE | EXPRESSION          | FILENAMES                | ORDER_ID |
|-------------+---------+----------+---------------------+--------------------------|----------+
| continent   | TEXT    | True     | $1:continent::TEXT  | geography/cities.parquet | 0        |
| country     | VARIANT | True     | $1:country::VARIANT | geography/cities.parquet | 1        |
| COUNTRY     | VARIANT | True     | $1:COUNTRY::VARIANT | geography/cities.parquet | 2        |
+-------------+---------+----------+---------------------+--------------------------+----------+
```

Retrieve the Snowflake column definitions for Parquet files in the `mystage` stage with IGNORE\_CASE specified as TRUE. In the returned output, all column names are retrieved as uppercase letters.

Copy code

```
-- Query the INFER_SCHEMA function.
SELECT *
  FROM TABLE(
    INFER_SCHEMA(
      LOCATION=>'@mystage'
      , FILE_FORMAT=>'my_parquet_format'
      , IGNORE_CASE=>TRUE
      )
    );

+-------------+---------+----------+----------------------------------------+--------------------------+----------+
| COLUMN_NAME | TYPE    | NULLABLE | EXPRESSION                             | FILENAMES                | ORDER_ID |
|-------------+---------+----------+---------------------+---------------------------------------------|----------+
| CONTINENT   | TEXT    | True     | GET_IGNORE_CASE ($1, CONTINENT)::TEXT  | geography/cities.parquet | 0        |
| COUNTRY     | VARIANT | True     | GET_IGNORE_CASE ($1, COUNTRY)::VARIANT | geography/cities.parquet | 1        |
+-------------+---------+----------+---------------------+---------------------------------------------+----------+
```

Retrieve the Snowflake column definitions for JSON files in the `mystage` stage:

Copy code

```
-- Create a file format that sets the file type as JSON.
CREATE FILE FORMAT my_json_format
  TYPE = json;

-- Query the INFER_SCHEMA function.
SELECT *
  FROM TABLE(
    INFER_SCHEMA(
      LOCATION=>'@mystage/json/'
      , FILE_FORMAT=>'my_json_format'
      )
    );

+-------------+---------------+----------+---------------------------+--------------------------+----------+
| COLUMN_NAME | TYPE          | NULLABLE | EXPRESSION                | FILENAMES                | ORDER_ID |
|-------------+---------------+----------+---------------------------+--------------------------|----------+
| col_bool    | BOOLEAN       | True     | $1:col_bool::BOOLEAN      | json/schema_A_1.json     | 0        |
| col_date    | DATE          | True     | $1:col_date::DATE         | json/schema_A_1.json     | 1        |
| col_ts      | TIMESTAMP_NTZ | True     | $1:col_ts::TIMESTAMP_NTZ  | json/schema_A_1.json     | 2        |
+-------------+---------------+----------+---------------------------+--------------------------+----------+
```

Creates a table using the detected schema from staged JSON files.

> Copy code
>
> ```
> CREATE TABLE mytable
>   USING TEMPLATE (
>     SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
>       FROM TABLE(
>         INFER_SCHEMA(
>           LOCATION=>'@mystage/json/',
>           FILE_FORMAT=>'my_json_format'
>         )
>       ));
> ```

Note

Using `*` for `ARRAY_AGG(OBJECT_CONSTRUCT())` might result in an error if the returned result is larger than 128 MB. We recommend that you avoid using `*` for larger result sets, and only use the required columns, `COLUMN NAME`, `TYPE`, and `NULLABLE`, for the query. Optional column `ORDER_ID` can be included when using `WITHIN GROUP (ORDER BY order_id)`.

Retrieve the column definitions for CSV files in the `mystage` stage and load the CSV files using MATCH\_BY\_COLUMN\_NAME:

Copy code

```
-- Create a file format that sets the file type as CSV.
CREATE FILE FORMAT my_csv_format
  TYPE = csv
  PARSE_HEADER = true;

-- Query the INFER_SCHEMA function.
SELECT *
  FROM TABLE(
    INFER_SCHEMA(
      LOCATION=>'@mystage/csv/'
      , FILE_FORMAT=>'my_csv_format'
      )
    );

+-------------+---------------+----------+---------------------------+--------------------------+----------+
| COLUMN_NAME | TYPE          | NULLABLE | EXPRESSION                | FILENAMES                | ORDER_ID |
|-------------+---------------+----------+---------------------------+--------------------------|----------+
| col_bool    | BOOLEAN       | True     | $1:col_bool::BOOLEAN      | json/schema_A_1.csv      | 0        |
| col_date    | DATE          | True     | $1:col_date::DATE         | json/schema_A_1.csv      | 1        |
| col_ts      | TIMESTAMP_NTZ | True     | $1:col_ts::TIMESTAMP_NTZ  | json/schema_A_1.csv      | 2        |
+-------------+---------------+----------+---------------------------+--------------------------+----------+

-- Load the CSV file using MATCH_BY_COLUMN_NAME.
COPY INTO mytable FROM @mystage/csv/
  FILE_FORMAT = (
    FORMAT_NAME= 'my_csv_format'
  )
  MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE;
```

### Iceberg column definitions

Retrieve the Iceberg column definitions for Parquet files on the `mystage` stage:

Copy code

```
-- Create a file format that sets the file type as Parquet.
  CREATE OR REPLACE FILE FORMAT my_parquet_format
    TYPE = PARQUET
    USE_VECTORIZED_SCANNER = TRUE;

-- Query the INFER_SCHEMA function.
SELECT *
FROM TABLE(
  INFER_SCHEMA(
    LOCATION=>'@mystage'
    , FILE_FORMAT=>'my_parquet_format'
    , KIND => 'ICEBERG'
    )
  );
```

Output:

```
+-------------+---------+----------+---------------------+--------------------------+----------+
| COLUMN_NAME | TYPE    | NULLABLE | EXPRESSION          | FILENAMES                | ORDER_ID |
|-------------+---------+----------+---------------------+--------------------------|----------+
| id          | INT     | False    | $1:id::INT          | sales/customers.parquet   | 0       |
| custnum     | INT     | False    | $1:custnum::INT     | sales/customers.parquet   | 1       |
+-------------+---------+----------+---------------------+--------------------------+----------+
```

Creates an Apache Iceberg™ table by using the detected schema from staged Parquet files.

Copy code

```
 -- Create a file format that sets the file type as Parquet.
 CREATE OR REPLACE FILE FORMAT my_parquet_format
   TYPE = PARQUET
   USE_VECTORIZED_SCANNER = TRUE;

-- Create an Iceberg table.
CREATE ICEBERG TABLE myicebergtable
  USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    WITHIN GROUP (ORDER BY order_id)
      FROM TABLE(
        INFER_SCHEMA(
          LOCATION=>'@mystage',
          FILE_FORMAT=>'my_parquet_format',
          KIND => 'ICEBERG'
        )
      ))
... {rest of the ICEBERG options}
;
```

Note

Using `*` for `ARRAY_AGG(OBJECT_CONSTRUCT())` might result in an error if the returned result is larger than 128 MB. We
recommend avoiding the use of `*` for larger result sets, and only using the required columns, `COLUMN NAME`, `TYPE`, and
`NULLABLE`, for the query. Optional column `ORDER_ID` can be included when using `WITHIN GROUP (ORDER BY order_id)`.

### Structured type column definitions

The following example infers structured column types from Parquet files that contain nested data:

Copy code

```
-- Query the INFER_SCHEMA function with INFER_NESTED_TYPES => TRUE.
SELECT column_name, type
  FROM TABLE(
    INFER_SCHEMA(
      LOCATION => '@mystage/orders/',
      FILE_FORMAT => 'my_parquet_format',
      INFER_NESTED_TYPES => TRUE
      )
    );

+-------------+--------------------------------------+
| COLUMN_NAME | TYPE                                 |
|-------------+--------------------------------------|
| name        | TEXT                                 |
| address     | OBJECT(city TEXT, zip NUMBER(10, 0)) |
| tags        | ARRAY(TEXT)                          |
| metadata    | MAP(TEXT, BOOLEAN)                   |
+-------------+--------------------------------------+
```

The following example creates a table with structured columns from this output:

Copy code

```
CREATE TABLE my_orders_table
  USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    WITHIN GROUP (ORDER BY order_id)
      FROM TABLE(
        INFER_SCHEMA(
          LOCATION => '@mystage/orders/',
          FILE_FORMAT => 'my_parquet_format',
          INFER_NESTED_TYPES => TRUE
        )
      ));
-- The column names keep their case from the files, so enclose them in
-- double quotes in queries, for example, "address".
```

To create an Iceberg table from the same files, set `KIND => 'ICEBERG'`. The following example also sets `ICEBERG_VERSION = 3` to
create an Iceberg v3 table:

Copy code

```
CREATE ICEBERG TABLE my_orders_iceberg_table
  USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    WITHIN GROUP (ORDER BY order_id)
      FROM TABLE(
        INFER_SCHEMA(
          LOCATION => '@mystage/orders/',
          FILE_FORMAT => 'my_parquet_format',
          KIND => 'ICEBERG',
          INFER_NESTED_TYPES => TRUE
        )
      ))
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'my_external_volume'
  BASE_LOCATION = 'my_orders_iceberg_table'
  ICEBERG_VERSION = 3;
```
