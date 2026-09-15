# DROP DCM PROJECT

Removes the specified [DCM project](/user-guide/dcm-projects/dcm-projects-overview) from the current/specified schema.

See also:
:   [CREATE DCM PROJECT](/sql-reference/sql/create-dcm-project) , [ALTER DCM PROJECT](/sql-reference/sql/alter-dcm-project), [DESCRIBE DCM PROJECT](/sql-reference/sql/desc-dcm-project) , [EXECUTE DCM PROJECT](/sql-reference/sql/execute-dcm-project), [SHOW DCM PROJECTS](/sql-reference/sql/show-dcm-projects), [SHOW DEPLOYMENTS IN DCM PROJECT](/sql-reference/sql/show-deployments-in-dcm-project)

## Syntax

Copy code

```
DROP DCM PROJECT [ IF EXISTS ] <name>
```

## Required parameters

`name`
:   Specifies the identifier for the DCM project to drop.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`IF EXISTS`
:   Optionally specifies to not return an error when the DCM project does not exist.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | DCM project | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

- Dropping a DCM project in Snowflake doesn’t remove any objects created by executing the DCM project.

## Examples

Drop the DCM project named `my_project`:

Copy code

```
DROP DCM PROJECT my_project;
```
