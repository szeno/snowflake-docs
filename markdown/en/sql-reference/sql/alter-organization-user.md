# ALTER ORGANIZATION USER

[Enterprise Edition Feature](/user-guide/intro-editions)

Organization users and organization user groups require Enterprise Edition. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Modifies the properties of an existing [organization user](/user-guide/organization-users).

See also:
:   [CREATE ORGANIZATION USER](/sql-reference/sql/create-organization-user) , [DROP ORGANIZATION USER](/sql-reference/sql/drop-organization-user) , [SHOW ORGANIZATION USERS](/sql-reference/sql/show-organization-users)

## Syntax

Copy code

```
ALTER ORGANIZATION USER [ IF EXISTS ] <name> SET [ objectProperties ]

ALTER ORGANIZATION USER <name> UNSET [ objectProperties ]
```

Where:

> Copy code
>
> ```
> objectProperties ::=
>   EMAIL = '<string>'
>   DISPLAY_NAME = '<string>'
>   FIRST_NAME = '<string>'
>   MIDDLE_NAME = '<string>'
>   LAST_NAME = '<string>'
>   COMMENT = '<string>'
> ```

## Parameters

`name`
:   Specifies the identifier for the organization user to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET ...`
:   Set object properties. For a description of the object properties, see [CREATE ORGANIZATION USER](/sql-reference/sql/create-organization-user).

    The `TYPE` property isn’t included in the object properties that this command accepts. You choose whether an organization user is a
    `PERSON` or a `SERVICE` user when you create it, and you can’t change the type afterward.

`UNSET ...`
:   Unset object properties. For a description of the object properties, see [CREATE ORGANIZATION USER](/sql-reference/sql/create-organization-user).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MANAGE ORGANIZATION USERS | Account | By default, only the GLOBALORGADMIN and USERADMIN system roles in the organization account have this privilege. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

Copy code

```
ALTER ORGANIZATION USER alice
  SET LOGIN_NAME = 'asmith';
```
