# SHOW VERSIONS IN ARTIFACT REPOSITORY

Note

This command works only for an `APPLICATION` artifact repository.

Lists the published versions of one package in an
[APPLICATION artifact repository](/sql-reference/sql/create-artifact-repository).

See also:
:   [CREATE ARTIFACT REPOSITORY](/sql-reference/sql/create-artifact-repository) ,
    [ALTER ARTIFACT REPOSITORY](/sql-reference/sql/alter-artifact-repository) ,
    [DESCRIBE ARTIFACT REPOSITORY](/sql-reference/sql/desc-artifact-repository) ,
    [DROP ARTIFACT REPOSITORY](/sql-reference/sql/drop-artifact-repository) ,
    [SHOW ARTIFACT REPOSITORIES](/sql-reference/sql/show-artifact-repositories) ,
    [SHOW PACKAGES IN ARTIFACT REPOSITORY](/sql-reference/sql/show-packages-in-artifact-repository)

## Syntax

Copy code

```
SHOW VERSIONS [ LIKE '<pattern>' ]
              IN ARTIFACT REPOSITORY <name>
              FOR PACKAGE <package_name>
              [ LIMIT <rows> ]
```

## Parameters

`LIKE 'pattern'`
:   Filters the output by version name. The match uses SQL `LIKE` pattern matching
    (case-insensitive) and is applied before `LIMIT`. Unpublished versions are
    excluded before the pattern is applied.

`name`
:   Specifies the identifier of the artifact repository.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`package_name`
:   Specifies the package to list. The name is matched in uppercase. The command
    returns an error if the package doesn’t exist in the repository.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`LIMIT rows`
:   Limits the maximum number of rows returned. `rows` must be a positive integer.
    The command doesn’t support `LIMIT ... FROM`. Unpublished versions don’t count
    toward the limit.

## Output

The command returns one row per published version, in version name order:

| Column | Description |
| --- | --- |
| `version` | Version name. |
| `artifact_repository` | Name of the artifact repository. |
| `package_name` | Package name. |
| `created_on` | Date and time the version was created. |
| `comment` | Comment on the version, if any. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Artifact repository | Required to list versions in the repository. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- `FOR PACKAGE` is required. The command returns an error if that package
  doesn’t exist in the repository.
- Only published versions are returned. A package that exists but has no
  published version returns no rows.

## Examples

List the published versions of a package:

Copy code

```
SHOW VERSIONS IN ARTIFACT REPOSITORY my_app_repo FOR PACKAGE my_package;
```

List versions whose names match a pattern, and return at most 10 rows:

Copy code

```
SHOW VERSIONS LIKE 'VERSION$%' IN ARTIFACT REPOSITORY my_db.my_schema.my_app_repo
  FOR PACKAGE my_package LIMIT 10;
```
