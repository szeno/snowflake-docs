# SHOW PACKAGES IN ARTIFACT REPOSITORY

Note

This command works only for an `APPLICATION` artifact repository.

Lists the packages in an
[APPLICATION artifact repository](/sql-reference/sql/create-artifact-repository).

See also:
:   [CREATE ARTIFACT REPOSITORY](/sql-reference/sql/create-artifact-repository) ,
    [ALTER ARTIFACT REPOSITORY](/sql-reference/sql/alter-artifact-repository) ,
    [DESCRIBE ARTIFACT REPOSITORY](/sql-reference/sql/desc-artifact-repository) ,
    [DROP ARTIFACT REPOSITORY](/sql-reference/sql/drop-artifact-repository) ,
    [SHOW ARTIFACT REPOSITORIES](/sql-reference/sql/show-artifact-repositories) ,
    [SHOW VERSIONS IN ARTIFACT REPOSITORY](/sql-reference/sql/show-versions-in-artifact-repository)

## Syntax

Copy code

```
SHOW PACKAGES [ LIKE '<pattern>' ]
              IN ARTIFACT REPOSITORY <name>
              [ LIMIT <rows> ]
```

## Parameters

`LIKE 'pattern'`
:   Filters the output by package name. The match uses SQL `LIKE` pattern matching
    (case-insensitive) and is applied before `LIMIT`.

`name`
:   Specifies the identifier of the artifact repository.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`LIMIT rows`
:   Limits the maximum number of rows returned. `rows` must be a positive integer.
    The command doesn’t support `LIMIT ... FROM`.

## Output

The command returns one row per package, in package name order:

| Column | Description |
| --- | --- |
| `created_on` | Earliest creation time among the versions included in the row. |
| `name` | Package name. |
| `updated_on` | Latest update time among the versions included in the row. |
| `comment` | Comment on the version included in the row that was created most recently. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Artifact repository | Required to list packages in the repository. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

List the packages in an artifact repository:

Copy code

```
SHOW PACKAGES IN ARTIFACT REPOSITORY my_app_repo;
```

List packages whose names start with `app_`, and return at most 10 rows:

Copy code

```
SHOW PACKAGES LIKE 'app_%' IN ARTIFACT REPOSITORY my_db.my_schema.my_app_repo LIMIT 10;
```
