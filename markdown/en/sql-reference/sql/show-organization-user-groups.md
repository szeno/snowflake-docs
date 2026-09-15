# SHOW ORGANIZATION USER GROUPS

Lists [organization user groups](/user-guide/organization-users#label-org-users-groups).

- If the command is executed in the organization account, it lists all organization user groups in the organization.
- If the command is executed in a regular account, it lists the organization user groups that are available to the account.

See also:
:   [CREATE ORGANIZATION USER GROUP](/sql-reference/sql/create-organization-user-group) , [ALTER ORGANIZATION USER GROUP](/sql-reference/sql/alter-organization-user-group) , [DROP ORGANIZATION USER GROUP](/sql-reference/sql/drop-organization-user-group)

## Syntax

Copy code

```
SHOW ORGANIZATION USER GROUPS
```

## Parameters

None

## Access control requirements

The access control requirements for this command vary depending on the account where it is being executed.

Regular account:
:   Executing this command in a regular account requires the ACCOUNTADMIN role.

Organization account:
:   A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
    [privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

    | Privilege | Object | Notes |
    | --- | --- | --- |
    | MANAGE ORGANIZATION USER GROUPS | Account | By default, only the GLOBALORGADMIN and USERADMIN system roles in the organization account have this privilege. |

    Expand

    Show lessSee more

    For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

    For general information about roles and privilege grants for performing SQL actions on
    [securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `name` | Name of the organization user group. |
| `is_imported` | When executed from a regular account, indicates whether the organization user group has been added to the account successfully. If TRUE, the organization user group was added and the role of the same name created. |
| `created_on` | Date and time when the organization user group was created. |
| `is_grantable` | When executed from a regular account, indicates whether the role that was imported from the organization user group can be granted to a local, account-specific role. If `TRUE`, the role imported from the organization user group can be granted to account-specific roles. |

Expand

Show lessSee more

## Examples

Show information about the organization user groups in the organization:

Copy code

```
SHOW ORGANIZATION USER GROUPS;
```
