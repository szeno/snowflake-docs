# COPY FILES

Copy files from a source location to an output stage. You can either use a stage or a query as the source of the files to copy.

- Use a stage as the source to copy files from one stage to another without renaming.
- Use a query as a source for the following tasks:
  - Copy from or to a set of files defined by a query ([SELECT](/sql-reference/sql/select) statement).
  - Copy from files written by a UDF (for example, [Writing files from Snowpark Python UDFs and UDTFs](/developer-guide/snowpark/python/creating-udfs#label-snowpark-python-udf-write-files)).
  - Copy from scoped or stage URLs.

You can copy from and to existing named stages, as the following table illustrates:

| Source location | Target location |
| --- | --- |
| Internal named stage | Internal named stage |
| External stage | Internal named stage |
| Internal named stage | External stage |
| External stage | External stage |
| Snowflake [Git repository clone](/developer-guide/git/git-overview) | Internal named stage |
| Snowflake [Git repository clone](/developer-guide/git/git-overview) | External stage |

Expand

Show lessSee more

A target or source external stage can reference files in any of the following cloud storage services or on-premises locations:

- Amazon S3
- Google Cloud Storage
- Microsoft Azure Blob storage
- Microsoft Data Lake Storage Gen2
- Microsoft Azure General-purpose v2
- [Amazon S3-compatible storage](/user-guide/data-load-s3-compatible-storage)

See also:
:   [External stages](/user-guide/data-load-overview#label-data-load-overview-external-stages) , [Internal stages](/user-guide/data-load-overview#label-data-load-overview-internal-stages), [Git repository clone](/developer-guide/git/git-overview#label-integrating-git-repository-stage)

## Syntax

### Copy from a stage

Copy code

```
COPY FILES INTO @[<namespace>.]<stage_name>[/<path>/]
  FROM @[<namespace>.]<stage_name>[/<path>/]
  [ FILES = ( '<file_name>' [ , '<file_name>' ] [ , ... ] ) ]
  [ PATTERN = '<regex_pattern>' ]
  [ DETAILED_OUTPUT = { TRUE | FALSE } ]
```

### Copy from a query

Copy code

```
COPY FILES INTO @[<namespace>.]<stage_name>[/<path>/]
  FROM ( SELECT <existing_url> [ , <new_filename> ] FROM ... )
  [ DETAILED_OUTPUT = { TRUE | FALSE } ]
```

## Required parameters

`INTO @[namespace.]stage_name[/path/]`
:   > Specifies the target location for the copied files.

    - `namespace` is the database or schema in which the internal or external stage resides, in the form of `database_name.schema_name` or `schema_name`. The namespace is optional if a database and schema are currently in use within the user session; otherwise, it is required.
    - `path` is an optional, case-sensitive path in the cloud storage location that specifies a set of files to copy from the source stage or a specific location on the target stage. Your cloud storage service might call the path a *prefix* or a *folder*.

    > Note
    >
    > - If a target or source path name includes special characters or spaces, you must enclose the `INTO ...`
    >   value in single quotes.
    > - The values for `INTO ...` must be literal constants.
    >   The values cannot be [SQL variables](/sql-reference/session-variables).

### Using a stage as a source

`FROM @[namespace.]stage_name[/path/]`
:   Specifies the source location where the files to copy are staged. The values provided to `FROM ...` follow the same specification and constraints as `INTO...` values.

### Using a query as a source

`FROM (SELECT existing_url [ , new_filename ] FROM ... )`
:   Specifies the source location and optional relative output location for the copied files. Each row that the [SELECT](/sql-reference/sql/select)
    query returns represents a file to copy.

    - `existing_url` is a scoped URL, stage name, or stage URL.
    - `new_filename` is an optional relative path from the output stage specified for the `INTO` clause.

    Snowflake copies the file to the following location:

    `@[<namespace>.]<stage_name>[/<path>]<new_filename>`

    If you don’t specify a value for `new_filename`, Snowflake uses the relative path of the `existing_url`.

## Optional parameters

`FILES = ( 'file_name' [ , 'file_name' ... ] )`
:   Specifies a list of one or more comma-separated file names to copy.
    The files must already be staged in the source location that you specify in the command.
    Snowflake skips any specified files that can’t be found.

    You can specify a maximum of 1000 file names.

    Copy files from query does not support this option. Instead, use the query to provide the filename list.

    Note

    To set the file path for external stages, Snowflake prepends the URL in the stage definition to each file name in the list.

    However, Snowflake does not insert a separator between the path and file name.
    You must explicitly include a separator (`/`) at the end of the URL in the stage definition
    or at the beginning of each file name in the `FILES` list.

`PATTERN = 'regex_pattern'`
:   Specifies a regular expression pattern for filtering the list of files to copy.
    This command applies the regular expression to the entire storage location in the `FROM` clause.

    Copy files from query does not support this option. Instead, use the query to match the pattern.

    Tip

    For best performance, avoid patterns that filter on a large number of files.

`DETAILED_OUTPUT = { TRUE | FALSE }`
:   Specifies whether the command output should summarize the results of the copy operation or list each file copied.

    Values:
    :   - If `TRUE`, the output includes a row for each file copied to the target location.
          A single column named `file` contains the target path (if applicable) and file name for each copied file.
        - If `FALSE`, the output is a single row with the number of files that were copied.

    Default:
    :   `TRUE`

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) (depending on the source and target locations) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | External stage | Required on a source or target external stage. |
| READ | Internal named stage | Required on a source internal stage. |
| WRITE | Internal named stage | Required on a target internal stage. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- This command does not support the following:

  - Copying files to or from *table* stages.
  - When using a stage as a source, copying files to or from *user* stages.
  - Copying data in archival cloud storage classes that requires restoration before it can be retrieved.
    Archival storage classes include Amazon S3 Glacier Flexible Retrieval, Glacier Deep Archive,
    or Microsoft Azure Archive Storage.
  - Copying files that are larger than 5GB.
- Considerations for running this command:

  - COPY FILES statements overwrite any existing files with matching names in the target location. The command does
    not remove any existing files that don’t match the names of the copied files.
  - If a file copy operation fails, Snowflake does not perform any automatic cleanup.
  - **Copying files from Google Cloud Storage**: A COPY FILES statement might fail if the object list for an external stage includes
    one or more directory blobs. A *directory blob* is a path that ends in a forward slash character (`/`). In the following example output
    for `LIST @<stage>`, `my_gcs_stage/load/` is a directory blob.

    ```
    +---------------------------------------+------+----------------------------------+-------------------------------+
    | name                                  | size | md5                              | last_modified                 |
    |---------------------------------------+------+----------------------------------+-------------------------------|
    | my_gcs_stage/load/                    |  12  | 12348f18bcb35e7b6b628ca12345678c | Mon, 11 Aug 2022 16:57:43 GMT |
    | my_gcs_stage/load/data_0_0_0.csv.gz   |  147 | 9765daba007a643bdff4eae10d43218y | Mon, 11 Aug 2022 18:13:07 GMT |
    +---------------------------------------+------+----------------------------------+-------------------------------+
    ```

    Google creates directory blobs when you use the Google Cloud console to create a directory.

    To avoid this issue and specify which files to copy, use the `PATTERN` option (for copy from stage) or `FROM` (for copy from query).

    For an example, see [Copy files using pattern matching](#label-copy-files-pattern-matching-examples).
  - Snowflake uses multipart uploads when uploading to Amazon S3 and Google Cloud Storage.
    To prevent incomplete uploads from accumulating, we recommend that you set a lifecycle rule.
    For instructions, see the [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpu-abort-incomplete-mpu-lifecycle-config.html)
    or [Google Cloud Storage](https://cloud.google.com/storage/docs/lifecycle#abort-mpu) documentation.

- The COPY FILES command incurs data transfer and compute costs:

  - **Data transfer**: Cloud providers might charge for data transferred out of their own network. To recover these expenses,
    Snowflake charges a per-byte fee when you copy files from an internal Snowflake stage
    into an external stage in a different [region](/user-guide/intro-regions)
    or with a different cloud provider. Snowflake does not charge for data ingress
    (for example, when copying files from an external stage into an internal stage).

    For more information about data transfer billing, see [Understanding data transfer cost](/user-guide/cost-understanding-data-transfer).
  - **Compute**: COPY FILES is a [serverless](/user-guide/cost-understanding-compute#label-serverless-credit-usage) feature and doesn’t require a virtual warehouse.
    The line item for the COPY FILES command on your Snowflake bill does not include any cloud services charges.

    For more information about compute resource billing, see [Understanding compute cost](/user-guide/cost-understanding-compute).

  Note

  Some Snowflake features, such as Native Apps and worksheets, incur COPY FILES charges. As a result, you might see
  COPY FILES charges even if you haven’t executed the COPY FILES command. For more information about these charges,
  contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
- Snowflake does not maintain a file copy history for this command.

## Examples

### Copy files

Copy all of the files from an existing source stage (`src_stage`) to an existing target stage (`trg_stage`):

Copy code

```
COPY FILES
  INTO @trg_stage
  FROM @src_stage;
```

Note

To copy files from or to an external stage with a protected storage location,
make sure the stage definition includes credentials to access the cloud storage location.

Specify the names of files to copy from an existing source stage (`src_stage`) to an existing target stage (`trg_stage`):

Copy code

```
COPY FILES
  INTO @trg_stage
  FROM @src_stage
  FILES = ('file1.csv', 'file2.csv');
```

Copy files from a specific path on an existing stage (`src_stage/src_path/`)
to a specific path on an existing target stage (`trg_stage/trg_path/`):

Copy code

```
COPY FILES
  INTO @trg_stage/trg_path/
  FROM @src_stage/src_path/;
```

### Copy files using pattern matching

Use pattern matching to load only compressed CSV files in any path on an existing source stage (`src_stage`) to an existing target stage (`trg_stage`):

Copy code

```
COPY FILES
  INTO @trg_stage
  FROM @src_stage
  PATTERN='.*/.*/.*[.]csv[.]gz';
```

The `.*` component represents zero or more occurrences of any character.
The square brackets escape the period character (`.`) that precedes a file extension.

Copy only uncompressed CSV files whose names include the string `sales`:

Copy code

```
COPY FILES
  INTO @trg_stage
  FROM @src_stage
  PATTERN='.*sales.*[.]csv';
```

### Copy files using a query

#### Copy a single file

The file name remains the same as in the source stage.

Copy code

```
COPY FILES
  INTO @trg_stage
  FROM (SELECT '@src_stage/file.txt');
```

#### Copy and rename a single file

Copy code

```
COPY FILES
  INTO @trg_stage
  FROM (SELECT '@src_stage/file.txt', 'new_filename.txt');
```

#### Copy all of the files from a table

To copy multiple files using a query, you can use a generic query.

Copy code

```
-- Create a table with URLs
CREATE TABLE urls(src_file STRING, trg_file STRING);
INSERT INTO urls VALUES ('@src_stage/file.txt', 'new_filename.txt');

-- Insert additional URLs here
COPY FILES
  INTO @trg_stage
  FROM (SELECT src_file, trg_file FROM urls);
```

#### Copy only some files

This example uses a filter to copy files that match a pattern.

Copy code

```
COPY FILES
  INTO @trg_stage
  FROM (SELECT src_file, trg_file FROM urls WHERE src_file LIKE '%file%');
```

#### Copy files from a directory table

Copy code

```
COPY FILES
  INTO @trg_stage
  FROM (SELECT relative_path FROM directory(@src_stage) WHERE relative_path LIKE '%.txt');
```

#### Copy files with detailed output

- To produce command output with a list of files that are copied to the target location, use `DETAILED_OUTPUT = TRUE`.

  The output has a single column named `file` that contains the target path, if applicable, and the file name for each copied file.

  Copy code

  ```
  COPY FILES
    INTO @trg_stage
    FROM @src_stage
    DETAILED_OUTPUT = TRUE;
  ```

  An example output:

  ```
  +--------------------+
  | file               |
  |--------------------|
  | employees01.csv.gz |
  | employees02.csv.gz |
  | employees03.csv.gz |
  | employees04.csv.gz |
  | employees05.csv.gz |
  +--------------------+
  ```
- To produce command output that summarizes the results of the copy operation, use `DETAILED_OUTPUT = FALSE`.

  The output is a single row with the number of files that were copied.

  Copy code

  ```
  COPY FILES
    INTO @trg_stage
    FROM @src_stage
    DETAILED_OUTPUT = FALSE;
  ```

  An example output:

  ```
  +-------------------+
  | numOfFilesCopied  |
  | 5                 |
  +-------------------+
  ```
