# SHOW ORGANIZATION USERS

Lists [organization users](/user-guide/organization-users). Administrators in the organization account can use this command to list all
organization users in the organization. Administrators in a regular account use this command to list all organization users in a specific
organization user group that was added to the account.

See also:
:   [CREATE ORGANIZATION USER](/sql-reference/sql/create-organization-user) , [ALTER ORGANIZATION USER](/sql-reference/sql/alter-organization-user) , [DROP ORGANIZATION USER](/sql-reference/sql/drop-organization-user)

## Syntax

Copy code

```
SHOW ORGANIZATION USERS [ IN ORGANIZATION USER GROUP <org_user_group> ]
```

## Parameters

`IN ORGANIZATION USER GROUP org_user_group`
:   Name of an organization user group. This command displays all of the organization users in the specified group.

    Required when the command is executed by the account administrator in a regular account.

## Access control requirements

The access control requirements for this command vary depending on the account where it is being executed.

Regular account:
:   Executing this command in a regular account requires the ACCOUNTADMIN role.

Organization account:
:   A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
    [privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

    | Privilege | Object | Notes |
    | --- | --- | --- |
    | MANAGE ORGANIZATION USERS | Account | By default, only the GLOBALORGADMIN and USERADMIN system roles in the organization account have this privilege. |

    Expand

    Show lessSee more

    For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

    For general information about roles and privilege grants for performing SQL actions on
    [securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `name` | Name of the organization user. |
| `created_on` | Date and time when the organization user was created. |
| `is_imported` | When executed from a regular account, indicates whether the organization user in the specified organization user group was successfully imported. |
| `display_name` | Name displayed for the user in Snowsight. |
| `login_name` | Name that the user enters to log into the system. |
| `first_name` | First name of the organization user. |
| `middle_name` | Middle name of the organization user. |
| `last_name` | Last name of the organization user. |
| `email` | Email address of the organization user. |
| `comment` | User-specified description of the organization user object. |
| `type` | Type of the organization user. For a list of possible values, see [Organization user types](/user-guide/organization-users#label-org-users-types). |

Expand

Show lessSee more

## Examples

As an organization administrator, list all of the organization users in the organization:

Copy code

```
USE ROLE GLOBALORGADMIN;

SHOW ORGANIZATION USERS;
```

As an account administrator, show information about the organization users in the organization user group `data_stewards`:

Copy code

```
USE ROLE ACCOUNTADMIN;

SHOW ORGANIZATION USERS IN ORGANIZATION USER GROUP data_stewards;
```
