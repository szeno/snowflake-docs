# REMOVE

Removes files from either an external (external cloud storage) or internal (i.e. Snowflake) stage.

For internal stages, the following stage types are supported:

- Named internal stage
- Stage for a specified table
- Stage for the current user

REMOVE can be abbreviated to RM.

See also:
:   [LIST](/sql-reference/sql/list)

## Syntax

Copy code

```
REMOVE { internalStage | externalStage } [ PATTERN = '<regex_pattern>' ]
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
>
> Copy code
>
> ```
> externalStage ::=
>     @[<namespace>.]<ext_stage_name>[/<path>]
> ```

## Required parameters

`internalStage | externalStage`
:   Specifies the location where the data files are staged:

    > |  |  |
    > | --- | --- |
    > | `@[namespace.]int_stage_name[/path]` | Files are in the specified named internal stage. |
    > | `@[namespace.]ext_stage_name[/path]` | Files are in the specified named external stage. |
    > | `@[namespace.]%table_name[/path]` | Files are in the stage for the specified table. |
    > | `@~[/path]` | Files are in the stage for the current user. |
    >
    > Expand
    >
    > Show lessSee more
    >
    > Where:
    >
    > - `<namespace>` is the database and/or schema in which the named internal stage or table resides. It is **optional** if a database and schema are currently in use within the session; otherwise, it is required.
    > - `<path>` is an optional case-sensitive path for files in the cloud storage location (i.e. files have names that begin with a common string) that limits access to a set of files. Paths are alternatively called *prefixes* or *folders* by different cloud storage services.
    >
    > Note
    >
    > If the stage name or path includes spaces or special characters, it must be enclosed in single quotes (e.g. `'@"my stage"'` for a stage named `"my stage"`).

## Optional parameters

`PATTERN = 'regex_pattern'`
:   Specifies a regular expression pattern for filtering files to remove. The command lists all files in the specified `path`
    and applies the regular expression pattern on each of the files found.

## Usage notes

- If you are loading data from a file on a stage, do not remove the staged files until the data has been loaded successfully. To check if the data has been loaded successfully, use the [COPY\_HISTORY](/sql-reference/functions/copy_history) command. Check the `STATUS` column to determine if the data from the file has been loaded. Note that if the status is `Load in progress`, removing the staged file can result in partial loads and data loss.
- To run this command with an external stage that uses a storage integration,
  you must use a role that has or inherits the USAGE privilege on the storage integration.

  For more information, see [Stage privileges](/user-guide/security-access-control-privileges#label-access-control-privileges-stage).
- Removing files from an external stage requires granting the following role or permission to Snowflake in your cloud storage account:

  | Cloud Storage Service | Role or Permission | Instructions |
  | --- | --- | --- |
  | Amazon S3 | `s3:DeleteObject` | [Configuring secure access to Amazon S3](/user-guide/data-load-s3-config) |
  | Google Cloud Storage | `storage.objects.delete` | [Configure an integration for Google Cloud Storage](/user-guide/data-load-gcs-config) |
  | Microsoft Azure (Blob storage) | `Storage Blob Data Contributor` | [Configure an Azure container for loading data](/user-guide/data-load-azure-config) |

  Expand

  Show lessSee more
- The command removes all directories and files that match a specified path. For example, the following statement would match any of
  the following objects in the `mytable` table stage:

  - `myobject.csv.gz` (file)
  - `myobject` (directory)
  - `myobject_new` (directory)

  Copy code

  ```
  rm @%mytable/myobject;
  ```
- To remove all files for a specific directory, include a forward-slash (`/`) at the end of the path. For example:

  Copy code

  ```
  rm @%mytable/myobject/;
  ```
- If a REMOVE statement is interrupted before it has completed running, any files already removed by the statement are not restored.

## Examples

Remove all files from the `path1/subpath2` path in a named internal or external stage named `mystage`:

> Copy code
>
> ```
> REMOVE @mystage/path1/subpath2;
> ```

Remove all files from the stage for the `orders` table:

> Copy code
>
> ```
> REMOVE @%orders;
> ```

Use the abbreviated form of the command to remove files whose names match the pattern `*jun*` from the stage for the current user:

> Copy code
>
> ```
> RM @~ pattern='.*jun.*';
> ```
