# CREATE ORGANIZATION USER GROUP

[Enterprise Edition Feature](/user-guide/intro-editions)

Organization users and organization user groups require Enterprise Edition. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Creates a new [organization user group](/user-guide/organization-users#label-org-users-groups).

See also:
:   [ALTER ORGANIZATION USER GROUP](/sql-reference/sql/alter-organization-user-group) , [DROP ORGANIZATION USER GROUP](/sql-reference/sql/drop-organization-user-group) , [SHOW ORGANIZATION USER GROUPS](/sql-reference/sql/show-organization-user-groups)

## Syntax

Copy code

```
CREATE ORGANIZATION USER GROUP [ IF NOT EXISTS ] <name>
  [ IS_GRANTABLE = { TRUE | FALSE } ]
```

## Required parameters

`name`
:   Identifier for the organization user group; must be unique for your organization.

    The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also case sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`IS_GRANTABLE = { TRUE | FALSE }`
:   Specifies whether the role that is imported into a regular account from the organization user group can be granted to an account-specific role. If `TRUE`, the role that is created when the ACCOUNTADMIN imports the organization user group can be granted to another role.

    Default: `FALSE`

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE ORGANIZATION USER GROUP | Account | By default, only the GLOBALORGADMIN and USERADMIN system roles in the organization account have this privilege. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

Create an organization user group named `data_stewards`:

Copy code

```
CREATE ORGANIZATION USER GROUP data_stewards;
```
