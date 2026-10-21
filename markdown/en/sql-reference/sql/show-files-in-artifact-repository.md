# SHOW FILES IN ARTIFACT REPOSITORY

Note

This command is in preview and might not be available in all accounts.

Lists retained files in a `PYPI` [artifact repository](/sql-reference/sql/create-artifact-repository).

See also:
:   [CREATE ARTIFACT REPOSITORY](/sql-reference/sql/create-artifact-repository),
    [ALTER ARTIFACT REPOSITORY](/sql-reference/sql/alter-artifact-repository),
    [DESCRIBE ARTIFACT REPOSITORY](/sql-reference/sql/desc-artifact-repository),
    [DROP ARTIFACT REPOSITORY](/sql-reference/sql/drop-artifact-repository),
    [SHOW ARTIFACT REPOSITORIES](/sql-reference/sql/show-artifact-repositories),
    [SHOW PACKAGES IN ARTIFACT REPOSITORY](/sql-reference/sql/show-packages-in-artifact-repository),
    [SHOW VERSIONS IN ARTIFACT REPOSITORY](/sql-reference/sql/show-versions-in-artifact-repository)

## Syntax

Copy code

```
SHOW FILES [ LIKE '<pattern>' ] IN ARTIFACT REPOSITORY <name>
  [ LIMIT <rows> ];
```

## Parameters

`LIKE 'pattern'`
:   Filters the output by file name or package name. Matching a package name also finds files whose file names use underscores instead of hyphens. The match uses SQL `LIKE` pattern matching and is case-insensitive.

`name`
:   Name of the artifact repository.

`LIMIT rows`
:   Limits the maximum number of rows returned. The value can’t exceed the current maximum result limit, which is 10,000 by default.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| READ | Artifact repository | None |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Output

The command returns one row per retained file with the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the file was retained in the repository, returned as a timestamp with scale 3. |
| `name` | Name of the retained file. |
| `package_name` | Name of the package associated with the file. |
| `version` | Version of the package. |
| `sha256` | SHA-256 digest of the file. |
| `size` | File size in bytes. |

Expand

Show lessSee more

## Usage notes

- The command returns a maximum of ten thousand records for the specified object type, as dictated by the access privileges for the role
  used to execute the command.

  To view results for which more than ten thousand records exist, query the corresponding view (if one exists) in the [Snowflake Information Schema](/sql-reference/info-schema).
- The command returns only published, retained files. This is the list of files that are copied from a package index into Snowflake-managed storage. Files appear only after retention completes.
- The command supports `PYPI` artifact repositories. `APPLICATION` repositories aren’t supported.
- Rows are ordered lexicographically by package name, package version, and file name.

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Examples

List the retained files in the `my_pypi_repository` repository:

Copy code

```
SHOW FILES IN ARTIFACT REPOSITORY my_pypi_repository;
```

List up to 10 retained files for the `emoji` package:

Copy code

```
SHOW FILES LIKE 'emoji' IN ARTIFACT REPOSITORY my_pypi_repository LIMIT 10;
```

The command returns output similar to the following:

```
+-------------------------------+------------------------------------------+--------------+---------+------------------------------------------------------------------+-------+
| created_on                    | name                                     | package_name | version | sha256                                                           | size  |
|-------------------------------+------------------------------------------+--------------+---------+------------------------------------------------------------------+-------|
| 2026-10-09 10:43:22.049 -0700 | emoji-2.16.0-py3-none-any.whl            | emoji        | 2.16.0  | c4230d80640def9071599ff56b1b5950fe13a2a94c0da98c5deab12431b24330 | 610912|
+-------------------------------+------------------------------------------+--------------+---------+------------------------------------------------------------------+-------+
```
