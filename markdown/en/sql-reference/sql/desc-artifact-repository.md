# DESCRIBE ARTIFACT REPOSITORY

Describes the properties of an
[artifact repository](/sql-reference/sql/create-artifact-repository),
including its type, owning role, and creation time.

`DESC` is an alias for `DESCRIBE`.

See also:
:   [CREATE ARTIFACT REPOSITORY](/sql-reference/sql/create-artifact-repository) ,
    [ALTER ARTIFACT REPOSITORY](/sql-reference/sql/alter-artifact-repository) ,
    [DROP ARTIFACT REPOSITORY](/sql-reference/sql/drop-artifact-repository) ,
    [SHOW ARTIFACT REPOSITORIES](/sql-reference/sql/show-artifact-repositories)

## Syntax

Copy code

```
{ DESC | DESCRIBE } ARTIFACT REPOSITORY <name>
```

## Parameters

`name`
:   Specifies the identifier of the artifact repository to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Artifact repository | Required to describe the repository. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

Copy code

```
DESCRIBE ARTIFACT REPOSITORY my_app_repo;
```
