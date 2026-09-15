# Manage directory tables

This topic provides instructions for creating and managing external or internal stages with directory tables.

## Create a stage with a directory table

This section provides instructions for creating stages (using [CREATE STAGE](/sql-reference/sql/create-stage)) that layer a directory table to store
metadata about the staged files.

Directory tables on internal stages require [manual metadata refreshes](#label-directory-table-manual-refreshes).
You could also choose to include a directory table on external stages and refresh the metadata manually. For information about automated metadata refreshes, see
[automated metadata refreshes](#label-directory-table-auto-refreshes).

The syntax for creating a stage with a directory table is nearly identical to creating a standard external or internal stage. Set the
optional DIRECTORY parameter to TRUE.

For the complete syntax and parameter descriptions, see [CREATE STAGE](/sql-reference/sql/create-stage). To add a directory table to an existing stage, use the [ALTER STAGE … SET DIRECTORY](/sql-reference/sql/alter-stage#label-alter-stage-directory-table-syntax) command.

Note

After you create a stage with a directory table, you must execute ALTER STAGE … REFRESH to manually refresh the directory table
metadata.

### Examples

Create an internal stage named `mystage` that includes a directory table. The stage references a file format named `myformat`:

> Copy code
>
> ```
> CREATE STAGE mystage
>   DIRECTORY = (ENABLE = TRUE)
>   FILE_FORMAT = myformat;
> ```

Create an external stage named `mystage` that includes a directory table. The stage references a bucket or container named `load`
with a path of `files`. Secure access to the cloud storage location is provided via the `my_storage_int` storage integration:

Note

The storage location in the URL value must end in a forward slash (`/`).

**Amazon S3**

Copy code

```
CREATE STAGE mystage
  URL='s3://load/files/'
  STORAGE_INTEGRATION = my_storage_int
  DIRECTORY = (ENABLE = TRUE);
```

**Google Cloud Storage**

Copy code

```
CREATE STAGE mystage
  URL='gcs://load/files/'
  STORAGE_INTEGRATION = my_storage_int
  DIRECTORY = (ENABLE = TRUE);
```

**Microsoft Azure**

Copy code

```
CREATE STAGE mystage
  URL='azure://myaccount.blob.core.windows.net/load/files/'
  STORAGE_INTEGRATION = my_storage_int
  DIRECTORY = (ENABLE = TRUE);
```

## Refresh directory table metadata

### Automated refresh

You can automatically refresh the metadata for a directory table by using the event messaging service for your cloud storage service.
To configure automated refreshes, see [Automated directory table metadata refreshes](/user-guide/data-load-dirtables-auto).

### Manual refresh

Note

- Manual refreshes on an external stage block simultaneous automated refreshes.
  Automated refreshes resume after the manual refresh completes.
- Manual refreshes perform a list operation on a stage, and can be slow or expensive for large or fast-growing stages.
  Instead, use event-based [automated refreshes](/user-guide/data-load-dirtables-auto).

To manually refresh the metadata in a directory table, use the [ALTER STAGE](/sql-reference/sql/alter-stage) command.

For best performance, use a selective `SUBPATH` with [ALTER STAGE](/sql-reference/sql/alter-stage).
Doing so reduces the number of files that need to be listed and checked. To learn about organizing your data by path,
see [best practices for staging your data files](/user-guide/data-load-considerations-stage).

For example:

Copy code

```
ALTER STAGE my_stage REFRESH SUBPATH = '2024/01/31';
```

The command returns the following columns:

| Column | Description |
| --- | --- |
| `file` | Name of the staged source file and relative path to the file. |
| `status` | Status: REGISTERED\_NEW, REGISTERED\_UPDATE, REGISTER\_SKIPPED, REGISTER\_FAILED, UNREGISTERED, or UNREGISTER\_FAILED. |
| `description` | Detailed description of the file registration status. |

Expand

Show lessSee more
