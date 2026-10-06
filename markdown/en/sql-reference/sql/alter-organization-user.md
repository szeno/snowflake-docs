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
>   TYPE = { PERSON | SERVICE }
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

`UNSET ...`
:   Unset object properties. For a description of the object properties, see [CREATE ORGANIZATION USER](/sql-reference/sql/create-organization-user).

    Unsetting the `TYPE` property makes the organization user a `PERSON` user, which is the default type.

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

## Usage notes

- When you change the `TYPE` property of an organization user, Snowflake also changes the type of the corresponding user object in every
  regular account that imported the organization user. This change also applies to existing users that were linked to the organization
  user with [SYSTEM$LINK\_ORGANIZATION\_USER](/sql-reference/functions/system_link_organization_user). Administrators in a regular account can’t change the type of these
  users.
- The type of a user determines which authentication methods it can use. For example, a `SERVICE` user can’t authenticate with a
  password, and you can’t set up [workload identity federation](/user-guide/workload-identity-federation) for a `PERSON` user. Before you
  change the type of an organization user, make sure that the corresponding users in each regular account authenticate with a method that
  the new type supports. For more information, see [Types of users](/user-guide/admin-user-management#label-user-management-types).

## Examples

Change the email address of the organization user `alice`:

Copy code

```
ALTER ORGANIZATION USER alice
  SET EMAIL = 'asmith@example.com';
```

Change the organization user `report_loader` to a `SERVICE` user. The corresponding user object in each regular account that imported
`report_loader` also becomes a `SERVICE` user:

Copy code

```
ALTER ORGANIZATION USER report_loader
  SET TYPE = SERVICE;
```

Change `report_loader` back to a `PERSON` user, which is the default type:

Copy code

```
ALTER ORGANIZATION USER report_loader
  UNSET TYPE;
```
