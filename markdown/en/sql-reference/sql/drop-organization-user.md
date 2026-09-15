# DROP ORGANIZATION USER

[Enterprise Edition Feature](/user-guide/intro-editions)

Organization users and organization user groups require Enterprise Edition. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Removes an [organization user](/user-guide/organization-users) from the organization.

See also:
:   [CREATE ORGANIZATION USER](/sql-reference/sql/create-organization-user) , [ALTER ORGANIZATION USER](/sql-reference/sql/alter-organization-user) , [SHOW ORGANIZATION USERS](/sql-reference/sql/show-organization-users)

## Syntax

Copy code

```
DROP ORGANIZATION USER [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Identifier for the organization user; must be unique for your organization.

    The identifier value must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also case
    sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Organization user |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Dropped organization users cannot be recovered; they must be recreated.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Example

Copy code

```
DROP ORGANIZATION USER joe;
```
