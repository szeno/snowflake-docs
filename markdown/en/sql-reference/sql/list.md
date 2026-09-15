# LIST

Returns a list of files from one of the following Snowflake storage features:

- Stage

  - Named internal
  - Named external
  - For a specified table
  - For the current user
- [Git repository clone in Snowflake](/developer-guide/git/git-overview)

LIST can be abbreviated to LS.

See also:
:   [REMOVE](/sql-reference/sql/remove), [PUT](/sql-reference/sql/put), [COPY INTO <table>](/sql-reference/sql/copy-into-table), [COPY INTO <location>](/sql-reference/sql/copy-into-location), [GET](/sql-reference/sql/get)

## Syntax

The syntax differs depending on whether you’re listing files in a stage or a Git repository clone.

### For a stage

Copy code

```
LIST { internalStage | externalStage } [ PATTERN = '<regex_pattern>' ]
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
>   @[<namespace>.]<ext_stage_name>[/<path>]
> ```

### For a Git repository clone

Copy code

```
LIST repositoryClone [ PATTERN = '<regex_pattern>' ]
```

Where:

> Copy code
>
> ```
> repositoryClone ::=
>   @[<namespace>.]<repository_clone>/<path>
> ```

## Required parameters

### For a stage

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
    > - `<namespace>` is the database and/or schema in which the named stage or table resides. It is **optional** if a database and schema are currently in use within the session; otherwise, it is required.
    > - `<path>` is an optional case-sensitive path for files in the cloud storage location (i.e. files have names that begin with a common string) that limits access to a set of files. Paths are alternatively called *prefixes* or *folders* by different cloud storage services.
    >
    > Note
    >
    > If the stage name or path includes spaces or special characters, it must be enclosed in single quotes (e.g. `'@"my stage"'` for a stage named `"my stage"`).
    >
    > Specifying a path provides a scope for the LIST command, potentially reducing the amount of time required to run the command.

### For a Git repository clone

`repositoryClone`
:   Specifies the name of the [repository clone](/sql-reference/sql/create-git-repository) and the branch, tag, or commit for
    which to list files.

    `@[namespace.]repository_clone/path`

    When listing files from a Git repository clone, the `path` is required and must begin with one of the following:

    > |  |  |
    > | --- | --- |
    > | `branches/branch_name` | List files from the specified branch. |
    > | `tags/tag_name` | List files from the specified tag. |
    > | `commits/commit_hash` | List files from the commit specified by the commit hash. |
    >
    > Expand
    >
    > Show lessSee more
    >
    > If the repository clone name or path includes spaces or special characters, it must be enclosed in single quotes (for example, `'@"my repository"'` for a repository named `"my repository"`).

## Optional parameters

`PATTERN = 'regex_pattern'`
:   Specifies a regular expression pattern for filtering files from the output. The command lists all files in the specified `path`
    and applies the regular expression pattern on each of the files found.

## Usage notes

- To run this command with an external stage that uses a storage integration,
  you must use a role that has or inherits the USAGE privilege on the storage integration.

  For more information, see [Stage privileges](/user-guide/security-access-control-privileges#label-access-control-privileges-stage).
- In contrast to named stages, table and user stages are not first-class database objects; rather, they are implicit stages associated with
  the table/user. As such, they have no grantable privileges of their own:
  - You can always list files in your user stage (i.e. no privileges are required).
  - To list files in a table stage, you must use a role that has the OWNERSHIP privilege on the table.
  - PATTERN supports the [Java Pattern class](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html) syntax.

## Output

The command returns columns in the following tables. Column values differ depending on whether you’re using LIST with a stage or Git
repository clone.

### For a stage

| Column | Data type | Description |
| --- | --- | --- |
| name | VARCHAR | Name of the staged file |
| size | NUMBER | Size of the file compressed (in bytes) |
| md5 | VARCHAR | The MD5 column stores an MD5 hash of the contents of the staged data file.  For internal stages with default encryption (SNOWFLAKE\_FULL), during upload the source file is encrypted with a random key, and its resulting MD5 digest will always differ from the original local file.  Amazon S3 stages report the value via the S3 eTag field, which might not be an MD5 hash of the file contents.  For Google Cloud stages that use a customer-managed encryption key (CMEK), md5 is expected to be NULL.  For more information, see [Customer-managed encryption keys](https://cloud.google.com/storage/docs/encryption/customer-managed-keys). |
| sha1 | VARCHAR | Not used |
| last\_modified | VARCHAR | Timestamp when the file was last updated in the stage |

Expand

Show lessSee more

### For a Git repository clone

| Column | Data type | Description |
| --- | --- | --- |
| name | VARCHAR | Full file path with extension |
| size | NUMBER | Size of the file compressed (in bytes) |
| md5 | VARCHAR | Not used |
| sha1 | VARCHAR | A unique identifier generated by applying the SHA-1 hashing algorithm to the file’s contents. It is used by Git to track and reference the exact version of a file in the repository, and can be used to detect changes in the file’s content. |
| last\_modified | VARCHAR | Timestamp of the commit associated with the listed files. This does not necessarily indicate when the file content was last changed. |

Expand

Show lessSee more

## Examples

### For a stage

List all the files in the stage for the `mytable` table:

Copy code

```
LIST @%mytable;
```

List all the files in the `path1` path of the `mystage` named stage:

Copy code

```
LIST @mystage/path1;
```

List the files that match a regular expression (i.e. all file names containing the string `data_0`) in the stage for the `mytable`
table:

Copy code

```
LIST @%mytable PATTERN='.*data_0.*';
```

List the files in the `/analysis/` path of the `my_csv_stage` named stage that match a regular expression (i.e. all file names containing
the string `data_0`):

Copy code

```
LIST @my_csv_stage/analysis/ PATTERN='.*data_0.*';
```

Use the abbreviated form of the command to list all the files in the stage for the current user:

Copy code

```
LS @~;
```

### For a Git repository clone

For examples, see [View a list of repository files](/developer-guide/git/git-operations#label-git-integration-viewing-repository-files).
