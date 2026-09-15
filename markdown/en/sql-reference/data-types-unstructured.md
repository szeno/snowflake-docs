# Unstructured data types

Snowflake supports three different kinds of data:

- *Structured data* (such as a CSV file) follows a strict tabular schema. Structured data can be easily loaded into SQL tables.
- *Semi-structured data* (such as a JSON or XML file) has a flexible schema. Snowflake can access fields in semi-structured data using
  special functions, but the data is not as easily queried as structured data. Semi-structured data can be loaded into SQL tables
  using VARIANT columns.
- *Unstructured data* (such as a document, image, or audio file) has no inherent schema. Unstructured data might still
  have an internal structure (for example, PNG image files must follow a documented format) but such technical details do not generally
  relate to the information in the file.

Snowflake provides ways of accessing and processing data in unstructured files, such as
the [AI COMPLETE function](/sql-reference/functions/ai_complete).

To use unstructured data in Snowflake, it must first be stored on an internal or external stage. The Snowflake function
that processes the unstructured data reads it from there. Depending on the function, you specify the file in
one or more of the following ways:

- By passing a stage name and a relative path to the file as two separate arguments to the function that will use it.
- By passing a [staged](/sql-reference/functions/build_stage_file_url) or [scoped](/sql-reference/functions/build_scoped_file_url) URL as a string.
- By passing a [FILE](#label-data-types-file) object created using the [TO\_FILE](/sql-reference/functions/to_file) or [TRY\_TO\_FILE](/sql-reference/functions/try_to_file) function.

## FILE data type

Snowflake provides the FILE data type for unstructured data. A FILE value represents a file stored in an internal or
external stage, but does not store the file’s data, only a reference to it. It includes the following metadata:

- STAGE: The name of the stage on which the file resides.
- RELATIVE\_PATH: The relative path of the file in its stage.
- STAGE\_FILE\_URL: The stage file URL.
- SCOPED\_FILE\_URL: A scoped file URL.
- CONTENT\_TYPE: The MIME type of the file.
- SIZE: The size, in bytes, of the file.
- ETAG: A unique hash of the file contents.
- LAST\_MODIFIED: The timestamp at which the file was last modified.

Not all of these fields are required. A FILE must have CONTENT\_TYPE, SIZE, ETAG, and LAST\_MODIFIED fields, and also the
file’s location specified by STAGE plus RELATIVE\_PATH, STAGE\_FILE\_URL, or SCOPED\_FILE\_URL.

You can create a file by passing a scoped file URL, a stage and path, or a metadata object to the
[TO\_FILE](/sql-reference/functions/to_file) or [TRY\_TO\_FILE](/sql-reference/functions/try_to_file) function.

### FILE functions

| Sub-category | Function |
| --- | --- |
| Constructors | [TO\_FILE](/sql-reference/functions/to_file) |
|  | [TRY\_TO\_FILE](/sql-reference/functions/try_to_file) |
| Accessors | [FL\_GET\_CONTENT\_TYPE](/sql-reference/functions/fl_get_content_type) |
|  | [FL\_GET\_ETAG](/sql-reference/functions/fl_get_etag) |
|  | [FL\_GET\_FILE\_TYPE](/sql-reference/functions/fl_get_file_type) |
|  | [FL\_GET\_LAST\_MODIFIED](/sql-reference/functions/fl_get_last_modified) |
|  | [FL\_GET\_RELATIVE\_PATH](/sql-reference/functions/fl_get_relative_path) |
|  | [FL\_GET\_SCOPED\_FILE\_URL](/sql-reference/functions/fl_get_scoped_file_url) |
|  | [FL\_GET\_SIZE](/sql-reference/functions/fl_get_size) |
|  | [FL\_GET\_STAGE](/sql-reference/functions/fl_get_stage) |
|  | [FL\_GET\_STAGE\_FILE\_URL](/sql-reference/functions/fl_get_stage_file_url) |
| Utility Functions | [FL\_IS\_AUDIO](/sql-reference/functions/fl_is_audio) |
|  | [FL\_IS\_COMPRESSED](/sql-reference/functions/fl_is_compressed) |
|  | [FL\_IS\_DOCUMENT](/sql-reference/functions/fl_is_document) |
|  | [FL\_IS\_IMAGE](/sql-reference/functions/fl_is_image) |
|  | [FL\_IS\_VIDEO](/sql-reference/functions/fl_is_video) |

Expand

Show lessSee more

## Usage notes

- FILE values may become inconsistent with the underlying staged files. FILE values are not updated when you modify or
  delete the underlying file. Conversely, if a FILE value is deleted from a table, the underlying file is not affected.
- Permissions on the underlying files are governed by the type of URL that was specified when creating the FILE. Stage
  file URLs and stage/path combinations give permanent permission to callers that have access to the associated stage.
  Scoped URLs give temporary user-based access to the underlying file for a 24-hour period.

## Using unstructured data in Snowflake via SQL

Create a table with a FILE column.

Copy code

```
CREATE TABLE images_table(img FILE);
```

Load data into the table from an external stage `my_images` that contains image files. `my_images` can be an internal or external
stage.

Note

This process requires directory table support on the stage. Enable it, if necessary, using the SQL below:

Copy code

```
ALTER STAGE my_images DIRECTORY=(ENABLE=true);
```

Load data into the Snowflake table.

Copy code

```
INSERT INTO images_table
    SELECT TO_FILE(file_url) FROM DIRECTORY(@my_images);
```

Run SQL statements against `images_table`. For example, the following query returns the relative path of each file in
the table that was last modified between January 1, 2021 and January 1, 2023.

Copy code

```
SELECT FL_GET_RELATIVE_PATH(f)
    FROM images_table
    WHERE FL_GET_LAST_MODIFIED(f) BETWEEN '2021-01-01' and '2023-01-01';
```

## Known limitations

The FILE data type currently cannot be used in:

- CLUSTER BY, GROUP BY, and ORDER BY clauses
- Hybrid tables, Iceberg tables, and external tables
- SnowScript
- Secured views
- Binds
- Search optimization
- Clients and connectors except Snowpark Python
