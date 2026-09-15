Categories:
:   [File functions](/sql-reference/functions-file) (AI Functions)

# TO\_FILE

Constructs a value of type [FILE](/sql-reference/data-types-unstructured#label-data-types-file) from a file location or from metadata.

# Syntax

Use one of the following:

```
TO_FILE( <stage_name>, <relative_path> )

TO_FILE( <file_url> )

TO_FILE( <metadata> )
```

## Arguments

Specify the file by providing:

- Both `stage_name` and `relative_path`
- `file_url`
- `metadata`

Only one of these methods can be used at a time.

`stage_name`
:   The name of the stage where the file is located, as a string, in the form `'@stage_name'`.

`relative_path`
:   The path to the file on the stage specified by `stage_name` as a string.

`file_url`
:   A valid stage or scoped file URL as a string.

`metadata`
:   An OBJECT containing the required FILE attributes. A FILE must have CONTENT\_TYPE, SIZE, ETAG, and LAST\_MODIFIED fields.
    It must also specify the file’s location in one of the following ways:

    - Both STAGE and RELATIVE\_PATH
    - STAGE\_FILE\_URL
    - SCOPED\_FILE\_URL

## Returns

A [FILE](/sql-reference/data-types-unstructured) that represents the staged file.

## Usage notes

Raises an error when:

- The supplied URL is not valid.
- The file is on a stage that the user lacks privileges to access.
- The supplied metadata doesn’t contain the required FILE fields.

## Examples

### Creating FILE objects using TO\_FILE

A simple use of the TO\_FILE function with a stage name and relative path:

Copy code

```
SELECT TO_FILE('@mystage', 'image.png');
```

Result:

```
+-----------------------------------------------------+
| TO_FILE('@MYSTAGE', 'IMAGE.PNG')                    |
|-----------------------------------------------------|
| {                                                   |
|   "CONTENT_TYPE": "image/png",                      |
|   "ETAG": "2859efde6e26491810f619668280a2ce",       |
|   "LAST_MODIFIED": "Thu, 18 Sep 2025 09:02:00 GMT", |
|   "RELATIVE_PATH": "image.png",                     |
|   "SIZE": 23698,                                    |
|   "STAGE": "@MYDB.MYSCHEMA.MYSTAGE"                 |
| }                                                   |
+-----------------------------------------------------+
```

A simple use of the TO\_FILE function with a staged file URL:

Copy code

```
SELECT TO_FILE(BUILD_STAGE_FILE_URL('@mystage', 'image.png'));
```

Result:

```
+--------------------------------------------------------------------------------------------------------------------+
| TO_FILE(BUILD_STAGE_FILE_URL('@MYSTAGE', 'IMAGE.PNG'))                                                             |
|--------------------------------------------------------------------------------------------------------------------|
| {                                                                                                                  |
|   "CONTENT_TYPE": "image/png",                                                                                     |
|   "ETAG": "..."                                                                                                    |
|   "LAST_MODIFIED": "Wed, 11 Dec 2024 20:24:00 GMT",                                                                |
|   "RELATIVE_PATH": "image.png",                                                                                    |
|   "SIZE": 105859,                                                                                                  |
|   "STAGE": "@MYDB.MYSCHEMA.MYSTAGE",                                                                               |
|   "STAGE_FILE_URL": "https://snowflake.account.snowflakecomputing.com/api/files/MYDB/MYSCHEMA/MYSTAGE/image.png"   |
| }                                                                                                                  |
+--------------------------------------------------------------------------------------------------------------------+
```

Or use the FILE\_URL from a file in the directory of your stage:

Copy code

```
SELECT TO_FILE(FILE_URL) FROM DIRECTORY(@mystage) LIMIT 1;
```

```
+--------------------------------------------------------------------------------------------------------------------+
| TO_FILE(FILE_URL)                                                                                                  |
|--------------------------------------------------------------------------------------------------------------------|
| {                                                                                                                  |
|   "CONTENT_TYPE": "image/png",                                                                                     |
|   "ETAG": "..."                                                                                                    |
|   "LAST_MODIFIED": "Wed, 11 Dec 2024 20:24:00 GMT",                                                                |
|   "RELATIVE_PATH": "image.png",                                                                                    |
|   "SIZE": 105859,                                                                                                  |
|   "STAGE": "@MYDB.MYSCHEMA.MYSTAGE",                                                                               |
|   "STAGE_FILE_URL": "https://snowflake.account.snowflakecomputing.com/api/files/MYDB/MYSCHEMA/MYSTAGE/image.png"   |
| }                                                                                                                  |
+--------------------------------------------------------------------------------------------------------------------+
```

This example uses TO\_FILE function directly with a scoped file URL:

Copy code

```
SELECT TO_FILE(`https://snowflake.account.snowflakecomputing.com/api/files/01ba4df2-0100-0001-0000-00040002e2b6/299017/Y6JShH6KjV`);

+------------------------------------------------------------------------------------------------------------------------------------------------+
| TO_FILE(https://snowflake.account.snowflakecomputing.com/api/files/01ba4df2-0100-0001-0000-00040002e2b6/299017/Y6JShH6KjV                      |
|------------------------------------------------------------------------------------------------------------------------------------------------|
| {                                                                                                                                              |
|   "CONTENT_TYPE": "image/png",                                                                                                                 |
|   "ETAG": "..."                                                                                                                                |
|   "LAST_MODIFIED": "Wed, 11 Dec 2024 20:24:00 GMT",                                                                                            |
|   "SCOPED_FILE_URL": "https://snowflake.account.snowflakecomputing.com/api/files/01ba4df2-0100-0001-0000-00040002e2b6/299017/Y6JShH6KjV",      |
|   "SIZE": 105859                                                                                                                               |
| }                                                                                                                                              |
+-----------------------------------------------------------------------------------------------------------------------------------------------+|
```

This shows an example of constructing a FILE from an object containing the required metadata:

Copy code

```
SELECT TO_FILE(OBJECT_CONSTRUCT('STAGE', 'MYSTAGE', 'RELATIVE_PATH', 'image.png', 'ETAG', '<ETAG value>',
  'LAST_MODIFIED', 'Wed, 11 Dec 2024 20:24:00 GMT', 'SIZE', 105859, 'CONTENT_TYPE', 'image/png'));

+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| TO_FILE(OBJECT_CONSTRUCT('STAGE', 'MYSTAGE', 'RELATIVE_PATH', 'IMAGE.PNG', 'ETAG', '<ETAG value>', 'LAST_MODIFIED', 'WED, 11 DEC 2024 20:24:00 GMT', 'SIZE', 105859, 'CONTENT_TYPE', 'IMAGE/PNG')) |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| {                                                                                                                                                                                                  |
|   "CONTENT_TYPE": "image/png",                                                                                                                                                                     |
|   "ETAG": "<ETAG value>>"                                                                                                                                                                          |
|   "LAST_MODIFIED": "Wed, 11 Dec 2024 20:24:00 GMT",                                                                                                                                                |
|   "RELATIVE_PATH": "image.png",                                                                                                                                                                    |
|   "SIZE": 105859,                                                                                                                                                                                  |
|   "STAGE": "@MYDB.MYSCHEMA.MYSTAGE"                                                                                                                                                                |
| }                                                                                                                                                                                                  |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

### Adding FILE to a table

The following example demonstrates how to create FILE and store it in a table, then perform various operations using that
column, including saving and loading from Parquet, SnowPipe, datasets, materialized views, dynamic tables, and cloning
with time travel.

Creating a table with a FILE column:

Copy code

```
CREATE OR REPLACE TABLE sample_table (a INT, f FILE NOT NULL);
DESCRIBE TABLE sample_table;
INSERT INTO sample_table SELECT 1, TO_FILE('@mystage', 'image.png');
INSERT INTO sample_table SELECT 1, TO_FILE('@mystage', relative_path) FROM DIRECTORY('@mystage');
SELECT * FROM sample_table WHERE fl_get_file_type(f) = 'image';
```

To write a table containing a FILE column to a stage as a Parquet file and load it back:

Copy code

```
-- Write to stage as Parquet
CREATE OR REPLACE STAGE test_stage_parquet;

CREATE OR REPLACE FILE FORMAT parquet_format
  TYPE = 'PARQUET'
  USE_LOGICAL_TYPE = TRUE;

COPY INTO @test_stage_parquet/file_copy.parquet FROM sample_table
  FILE_FORMAT = (FORMAT_NAME = parquet_format) HEADER = TRUE ->> SELECT "rows_unloaded" FROM $1;
ALTER STAGE test_stage_parquet SET DIRECTORY = (ENABLE=TRUE);
ALTER STAGE test_stage_parquet REFRESH;

-- Read Parquet files back from stage
SELECT * FROM @TEST_STAGE_PARQUET/file_copy.parquet_0_0_0.snappy.parquet(FILE_FORMAT => parquet_format);
SELECT * FROM @TEST_STAGE_PARQUET (PATTERN => '.*.parquet', FILE_FORMAT => parquet_format);
```

Create a dataset from a Parquet file:

Copy code

```
CREATE OR REPLACE DATASET mydataset;
ALTER DATASET mydataset ADD VERSION 'v1' FROM
  (SELECT * FROM @TEST_STAGE_PARQUET/file_copy.parquet_0_0_0.snappy.parquet(
    FILE_FORMAT => my_parquet_format))
  COMMENT = 'test dataset';
```

Copy Parquet files into a table:

Copy code

```
CREATE OR REPLACE TABLE t1_copy_parquet (a INT, f OBJECT NOT NULL);

COPY INTO t1_copy_parquet
  FROM @test_stage_parquet
  FILE_FORMAT = (FORMAT_NAME = parquet_format)
  MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

SELECT FL_GET_STAGE(f), FL_GET_RELATIVE_PATH(f) FROM t1_copy_parquet;
```

Create a Snowpipe:

Copy code

```
CREATE OR REPLACE TABLE t1_copy_parquet_snowpipe (f OBJECT NOT NULL);
CREATE OR REPLACE PIPE test_pipe AS
  COPY INTO t1_copy_parquet_snowpipe
  FROM @test_stage_parquet
FILE_FORMAT = (FORMAT_NAME = my_parquet_format)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

ALTER PIPE TEST_PIPE REFRESH;
```

Create a materialized view or a dynamic table from the table:

Copy code

```
CREATE OR REPLACE MATERIALIZED VIEW MV AS SELECT * FROM SAMPLE_TABLE;

CREATE OR REPLACE DYNAMIC TABLE sample_dynamic_table
  WAREHOUSE = my_warehouse
  TARGET_LAG = '60 minutes'
AS SELECT f FROM sample_table;
```

Store files in an array in a table column:

Copy code

```
CREATE OR REPLACE TABLE files_array_table(files ARRAY);
INSERT INTO files_array_table SELECT ARRAY_CONSTRUCT(TO_FILE('@mystage', 'image.png'));
CREATE OR REPLACE TABLE files_array_table_copy(files ARRAY);
INSERT INTO files_array_table_copy SELECT files[0] FROM files_array_table;
```

### Examples of errors

These examples illustrate common mistakes in using TO\_FILE that result in the function raising an error.

The following example constructs a FILE from a metadata object but omits a required field:

Copy code

```
SELECT TO_FILE(OBJECT_CONSTRUCT('RELATIVE_PATH', 'image.png', 'ETAG', '<ETAG value>',
  'LAST_MODIFIED', 'Wed, 11 Dec 2024 20:24:00 GMT', 'SIZE', 105859, 'CONTENT_TYPE', 'image/png'));
```

```
Invalid file metadata. Must provide (STAGE and RELATIVE_PATH), SCOPED_FILE_URL, or STAGE_FILE_URL.
```

The following example is similar, but omits the ETAG field, which is required.

Copy code

```
SELECT TO_FILE(OBJECT_CONSTRUCT('STAGE', 'MYSTAGE', 'RELATIVE_PATH', 'image.png',
  'LAST_MODIFIED', 'Wed, 11 Dec 2024 20:24:00 GMT', 'SIZE', 105859, 'CONTENT_TYPE', 'image/png'));
```

```
Invalid file metadata. Missing required fields: ETAG.
```

The following example shows attempts to GROUP BY, ORDER BY, and CLUSTER BY a FILE column, which is not supported
because FILE values cannot be compared.

Copy code

```
SELECT f, count(*) FROM sample_table GROUP BY f;
-- Expressions of type FILE cannot be used as GROUP BY keys

SELECT * FROM sample_table ORDER by f;
-- Expressions of type FILE cannot be used as ORDER BY keys

CREATE OR REPLACE TABLE cluster_to_file (a int, url string) CLUSTER BY (to_file(url));
-- Unsupported type 'FILE' for clustering keys
```

This final example uses an incorrect stage name, specifically a slash at the end of the stage name.
Snowflake already adds a slash between the stage name and relative path, so this results in
two slashes, and the combined stage path does not specify any file.

Copy code

```
SELECT TO_FILE('@mystage/', 'image.png');
```

```
Remote file '@mystage//image.png' was not found. There are several potential causes.
The file might not exist. The required credentials may be missing or invalid. If you
are running a copy command, please make sure files are not deleted when they are
being loaded or files are not being loaded into two different tables concurrently
with auto purge option.
```

## Known limitations

- TO\_FILE cannot be used in INSERT INTO TABLE <t> VALUES clause. Use INSERT INTO TABLE <t> SELECT instead.
