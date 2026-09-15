# DROP ARTIFACT REPOSITORY

Removes the specified
[artifact repository](/sql-reference/sql/create-artifact-repository) from
the current or specified schema.

See also:
:   [CREATE ARTIFACT REPOSITORY](/sql-reference/sql/create-artifact-repository) ,
    [ALTER ARTIFACT REPOSITORY](/sql-reference/sql/alter-artifact-repository) ,
    [DESCRIBE ARTIFACT REPOSITORY](/sql-reference/sql/desc-artifact-repository) ,
    [SHOW ARTIFACT REPOSITORIES](/sql-reference/sql/show-artifact-repositories)

## Syntax

Copy code

```
DROP ARTIFACT REPOSITORY [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier of the artifact repository to drop. If the
    identifier isn’t fully qualified, the command looks for the repository in
    the current schema for the session.

## Access control requirements

Your role must have the following [privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) on objects:

| Privilege | Object |
| --- | --- |
| OWNERSHIP | Artifact repository that you remove |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Dropping a repository deletes all packages and versions it contains.
- You can’t drop a repository while an
  [APPLICATION SERVICE](/sql-reference/sql/create-application-service) is
  actively deployed from a package in that repository. Drop the service first,
  or upgrade it to a package in a different repository.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

Copy code

```
DROP ARTIFACT REPOSITORY IF EXISTS my_app_repo;
```
