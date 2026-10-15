# GRANT APPLICATION ROLE

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Assigns an application role to an account role, another application role, an application, or a user.

This command creates a “parent-child” relationship between the application role and the role
to which it is granted, also referred to as a role hierarchy.

For more details, see [Overview of Access Control](/user-guide/security-access-control-overview).

See also:
:   [ALTER APPLICATION ROLE](/sql-reference/sql/alter-application-role), [CREATE APPLICATION ROLE](/sql-reference/sql/create-application-role),
    [REVOKE APPLICATION ROLE](/sql-reference/sql/revoke-application-role), [SHOW APPLICATION ROLES](/sql-reference/sql/show-application-roles)

    [GRANT ROLE](/sql-reference/sql/grant-role), [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role)

## Syntax

Copy code

```
GRANT APPLICATION ROLE <name> TO ROLE <parent_role_name> [ WITH GRANT OPTION ]

GRANT APPLICATION ROLE <name> TO { APPLICATION ROLE <application_role> | APPLICATION <application_name> | USER <user_name> }
```

## Parameters

`name`
:   Specifies the identifier for the application role to grant. If the identifier contains spaces or
    special characters, the entire string must be enclosed in double quotes. Identifiers enclosed in
    double quotes are also case-sensitive.

`ROLE parent_role_name`
:   Grants the application role to the specified account role.

`APPLICATION ROLE application_role`
:   Grants the application role to the specified application role in the same application. This grant
    creates a role hierarchy of application roles.

    If the identifier isn’t fully qualified in the form of
    `application_name.application_role_name`, the command looks for the
    application role in the current application for the session.

`APPLICATION application_name`
:   Grants the application role to the specified application.

`USER user_name`
:   Grants the application role to the specified user.

`WITH GRANT OPTION`
:   If specified, allows the recipient account role to grant the application role further. The recipient
    can include `WITH GRANT OPTION` on those grants.

    Default: No value, which means the recipient account role can’t grant the application role further.
    The recipient still inherits the privileges of the granted application role.

    Application roles are granted to the application owner with `WITH GRANT OPTION`. The application owner
    can grant an application role to another account role with `WITH GRANT OPTION`. That grantee can then
    grant the application role further.

    `WITH GRANT OPTION` applies when the grantor is an account role, including the application owner. It
    doesn’t apply when the application grants an application role to another application role in the same
    application.

    For revoke behavior, see [REVOKE APPLICATION ROLE](/sql-reference/sql/revoke-application-role).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

The following table lists two different grantors. The application owner grants an application role outside
the application, and the application grants an application role to another application role in the same
application:

| Privilege or role | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Application | The application owner can grant an application role to an account role, another application, or a user. A grant to an account role can include `WITH GRANT OPTION`. A role that was granted the application role with `WITH GRANT OPTION` can also grant it to an account role, another application, or a user. |
| OWNERSHIP | Application role | The application can grant an application role to another application role in the same application. This grant forms the application role hierarchy. |

Expand

Show lessSee more

Only the application owner, or a role that was granted the application role with `WITH GRANT OPTION`, can
grant an application role to an account role, another application, or a user. The MANAGE GRANTS privilege
doesn’t apply to these grants. `ACCOUNTADMIN` can grant an application role only when it owns the
application or was granted the application role with `WITH GRANT OPTION`. For example, `ACCOUNTADMIN`
doesn’t own the `SNOWFLAKE` application, but it has the `SNOWFLAKE` application roles with
`WITH GRANT OPTION`, so it can grant them to other roles.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

Granting an application role to another application role can only be performed within the
context of an installed application, for example, in the application’s setup script.

## Examples

Grants the application role `app_role` to a different application role `other_app_role`:

Copy code

```
GRANT APPLICATION ROLE app_role TO APPLICATION ROLE other_app_role;
```

Grants the application role `app_role` in the application `my_app` to the account role `analyst`. The
`analyst` role can grant `my_app.app_role` further:

Copy code

```
GRANT APPLICATION ROLE my_app.app_role TO ROLE analyst WITH GRANT OPTION;
```

Grants the application role `app_role` in the application `my_app` to the user `user1`:

Copy code

```
GRANT APPLICATION ROLE my_app.app_role TO USER user1;
```
