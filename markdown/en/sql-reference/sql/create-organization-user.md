# CREATE ORGANIZATION USER

[Enterprise Edition Feature](/user-guide/intro-editions)

Organization users and organization user groups require Enterprise Edition. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Creates a new [organization user](/user-guide/organization-users).

See also:
:   [ALTER ORGANIZATION USER](/sql-reference/sql/alter-organization-user) , [DROP ORGANIZATION USER](/sql-reference/sql/drop-organization-user) , [SHOW ORGANIZATION USERS](/sql-reference/sql/show-organization-users)

## Syntax

Copy code

```
CREATE ORGANIZATION USER [ IF NOT EXISTS ] <name>
  [ objectProperties ]
```

Where:

> Copy code
>
> ```
> objectProperties ::=
>   EMAIL = '<string>'
>   LOGIN_NAME = '<string>'
>   DISPLAY_NAME = '<string>'
>   FIRST_NAME = '<string>'
>   MIDDLE_NAME = '<string>'
>   LAST_NAME = '<string>'
>   TYPE = { PERSON | SERVICE }
>   COMMENT = '<string>'
> ```

## Required parameters

`name`
:   Identifier for the organization user; must be unique for your organization.

    The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also case sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`EMAIL = 'string'`
:   Email address of the user.

## Optional parameters

`LOGIN_NAME = 'string'`
:   Name that the user enters to log into the system. Login names for users must be unique across your entire organization. It cannot match the login name in a regular account that tries to import the organization user.

    A login name can be any string, including spaces and non-alphanumeric characters, such as exclamation points (`!`), percent signs
    (`%`), and asterisks (`*`); however, if the string contains spaces or non-alphanumeric characters, it must be enclosed in single
    or double quotes. Login names are always case insensitive.

    Snowflake allows specifying different user and login names to enable using common identifiers (for example, email addresses) for login.

    Default: User’s name/identifier (that is, if no value is specified, the value specified for `name` is used as the login name)

`DISPLAY_NAME = 'string'`
:   Name displayed for the user in the Snowflake web interface.

    Default: User’s name/identifier (that is, if no value is specified, the value specified for `name` is used as the display name)

`FIRST_NAME = 'string'` , `MIDDLE_NAME = string` , `LAST_NAME = 'string'`
:   First, middle, and last name of the user.

    Default: `NULL`

`TYPE = { PERSON | SERVICE }`
:   Specifies whether the organization user represents a person or a service.

    `PERSON`
    :   Organization user is a human user who can interact with Snowflake.

    `SERVICE`
    :   Organization user is a service or application that interacts with Snowflake without human interaction.

    For the characteristics of each type of user, including the authentication methods that a service user can use, see
    [Types of users](/user-guide/admin-user-management#label-user-management-types).

    `PERSON` and `SERVICE` are the only types that an organization user can have. Types that are valid for a user in a regular account but
    not for an organization user, such as `SERVICE_AGENT` and `LEGACY_SERVICE`, are rejected.

    The type determines which existing users the organization user can be linked to, and is applied to the user objects that Snowflake
    creates when the organization user is imported into a regular account. For more information, see
    [Organization user types](/user-guide/organization-users#label-org-users-types).

    You can’t change the type after you create the organization user. The [ALTER ORGANIZATION USER](/sql-reference/sql/alter-organization-user) command doesn’t
    accept the `TYPE` property.

    Default: `PERSON`

`COMMENT = 'string'`
:   Description of the user.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE ORGANIZATION USER | ACCOUNT | By default, only the GLOBALORGADMIN and USERADMIN system roles in the organization account have this privilege. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

Create an organization user and set the EMAIL property. Because the `TYPE` property isn’t specified, the organization user is a
`PERSON` user:

Copy code

```
CREATE ORGANIZATION USER joe EMAIL = 'joe.davis@example.com';
```

Create an organization user for a service that runs in more than one account:

Copy code

```
CREATE ORGANIZATION USER etl_pipeline
  EMAIL = 'data-platform@example.com'
  TYPE = SERVICE;
```

When an account administrator imports an organization user group that contains `etl_pipeline`, the user object created in the regular
account is also a `SERVICE` user. For an example of linking this kind of organization user to an existing service user, see
[SYSTEM$LINK\_ORGANIZATION\_USER](/sql-reference/functions/system_link_organization_user).
