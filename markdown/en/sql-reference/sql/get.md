# GET

Downloads data files from one of the following [internal stage](/user-guide/data-load-overview#label-data-load-overview-internal-stages)
types to a local directory or folder on a client machine:

- Named internal stage.
- Internal stage for a specified table.
- Internal stage for the current user.

You can use this command to download data files after unloading data from a table onto a
Snowflake stage using the [COPY INTO <location>](/sql-reference/sql/copy-into-location) command.

For more information about using the GET command, see [Unload into a Snowflake stage](/user-guide/data-unload-snowflake).

See also:
:   [LIST](/sql-reference/sql/list) , [PUT](/sql-reference/sql/put) , [REMOVE](/sql-reference/sql/remove) , [COPY FILES](/sql-reference/sql/copy-files)

## Syntax

Copy code

```
GET internalStage file://<local_directory_path>
    [ PARALLEL = <integer> ]
    [ PATTERN = '<regex_pattern>'' ]
```

Where:

> Copy code
>
> ```
> internalStage ::=
>     @[<namespace>.]<int_stage_name>[/<path>]
>   | @[<namespace>.]%<table_name>[/<path>]
>   | @~[/<path>]
> ```

## Required parameters

`internalStage`
:   Specifies the location in Snowflake from which to download the files:

    > |  |  |
    > | --- | --- |
    > | `@[namespace.]int_stage_name[/path]` | Files are downloaded from the specified named internal stage. |
    > | `@[namespace.]%table_name[/path]` | Files are downloaded from the stage for the specified table. |
    > | `@~[/path]` | Files are downloaded from the stage for the current user. |
    >
    > Expand
    >
    > Show lessSee more
    >
    > Where:
    >
    > - `<namespace>` is the database and/or schema in which the named internal stage or table resides. It is **optional** if a database and schema are currently in use within the session; otherwise, it is required.
    > - `<path>` is an optional case-sensitive path for files in the cloud storage location (that is, files have names that begin with a common string) that limits access to a set of files. Paths are alternatively called *prefixes* or *folders* by different cloud storage services. If `<path>` is specified, but no file is explicitly named in the path, all data files in the path are downloaded.
    >
    > Note
    >
    > If the stage name or path includes spaces or special characters, it must be enclosed in single quotes (example: `'@"my stage"'` for a stage named `"my stage"`).

`file://local_directory_path`
:   Specifies the local directory path on the client machine where the files are downloaded:

    Linux/macOS:
    :   You must include the initial forward slash in the path (example: `file:///tmp/load`).

        If the directory path includes special characters, the entire file URI must be enclosed in single quotes.

    Windows:
    :   You must include the drive and backslash in the path (example: `file://C:tempload`).

        If the directory path includes special characters, the entire file URI must be enclosed in single quotes. Note that
        the drive and path separator is a forward slash (`/`) in enclosed URIs (example: `'file://C:/Users/%Username%/Data 2025-01'`).

    Note

    The GET command returns an error if you specify a filename as part of the path, except if you use the
    [JDBC driver](/developer-guide/jdbc/jdbc) or [ODBC driver](/developer-guide/odbc/odbc). If you specify a filename when
    using either driver, the driver treats the filename as part of the directory path and creates a subdirectory with the specified
    filename.

    For example, if you specify `file:///tmp/load/file.csv`, the JDBC or ODBC driver creates a subdirectory named `file.csv/`
    under the path `/tmp/load/`. The GET command then downloads the staged files into this new subdirectory.

## Optional parameters

`PARALLEL = integer`
:   Specifies the number of threads to use for downloading the files. The granularity unit for downloading is one file.

    Increasing the number of threads can improve performance when downloading large files.

    Supported values: Any integer value from `1` (no parallelism) to `99` (use 99 threads for downloading files).

    Default: `10`

`PATTERN = 'regex_pattern'`
:   Specifies a regular expression pattern for filtering files to download. The command lists all files in the specified `path`
    and applies the regular expression pattern on each of the files found.

    Default: No value (all files in the specified stage are downloaded)

## Usage notes

- GET does not support the following actions:

  - Downloading files from external stages. To download files from external stages, use the utilities
    provided by your cloud service.
  - Downloading multiple files with divergent directory paths. The command
    *does not* preserve stage directory structure when transferring files to your client machine.

    For example, the following GET statement returns an error since you can’t download multiple files named `tmp.parquet` that are in
    different subdirectories on the stage.

    Copy code

    ```
    GET @my_int_stage my_target_path PATTERN = "tmp.parquet";
    ```
- The [ODBC driver](/developer-guide/odbc/odbc) supports GET with Snowflake accounts hosted on the following platforms:

> - Amazon Web Services (using ODBC Driver Version 2.17.5 and higher).
> - Google Cloud (using ODBC Driver Version 2.21.5 and higher).
> - Microsoft Azure (using ODBC Driver Version 2.20.2 and higher).

- The command cannot be executed from the **Worksheets** [![Worksheet tab](/static/images/screens/ui-navigation-worksheet-icon.svg)](/static/images/screens/ui-navigation-worksheet-icon.svg) page in either Snowflake web interface; instead, use the
  SnowSQL client to download data files, or check the documentation for the specific Snowflake client to verify support for this command.
- The command does not rename files.
- Downloaded files are automatically decrypted using the same key that was used to encrypt the file when it was either uploaded
  (using [PUT](/sql-reference/sql/put)) or unloaded from a table (using [COPY INTO <location>](/sql-reference/sql/copy-into-location)).
- For the [PUT](/sql-reference/sql/put) and [GET](/sql-reference/sql/get) commands,
  an EXECUTION\_STATUS of `success` in the [QUERY\_HISTORY](/sql-reference/account-usage/query_history)
  does \_not\_ mean that data files were successfully uploaded or downloaded.
  Instead, the status indicates that Snowflake received authorization to proceed with the file transfer.

## Examples

Download all files in the stage for the `mytable` table to the `/tmp/data` local directory (in a Linux or macOS environment):

> Copy code
>
> ```
> GET @%mytable file:///tmp/data/;
> ```

Download files from the `myfiles` path in the stage for the current user to the `/tmp/data` local directory (in a Linux or
macOS environment):

> Copy code
>
> ```
> GET @~/myfiles file:///tmp/data/;
> ```

For additional examples, see [Unload into a Snowflake stage](/user-guide/data-unload-snowflake).
