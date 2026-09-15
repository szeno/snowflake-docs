# REVOKE CALLER

Revokes privileges that were previously granted to an executable owner using a
[caller grant](/developer-guide/restricted-callers-rights#label-restricted-callers-rights-about-grants).

Variations of the REVOKE CALLER command are as follows:

- REVOKE CALLER — Revoke specific privileges on a specific object.
- REVOKE ALL CALLER PRIVILEGES — Revoke all privileges on a specific object. The executable will not be
  able to run with any privileges from the caller when it tries to access the object.
- REVOKE INHERITED CALLER — Revoke caller grants on all current and future objects of the same type when they share a common schema, database,
  or account. Only privileges in a specified list are revoked.
- REVOKE ALL INHERITED CALLER PRIVILEGES — Revoke caller grants on all current and future objects of the same type when they share a common
  schema, database, or account. All privileges are revoked; the executable will not be able to run with any privileges from the caller.

## Syntax

Copy code

```
REVOKE CALLER <object_privilege> [ , <object_privilege> ... ]
  ON <object_type> <object_name>
  FROM { ROLE | DATABASE ROLE } <grantee_name>

REVOKE ALL CALLER PRIVILEGES
  ON <object_type> <object_name>
  FROM { ROLE | DATABASE ROLE } <grantee_name>

REVOKE INHERITED CALLER <object_privilege> [ , <object_privilege> ... ]
  ON ALL <object_type_plural>
  IN { ACCOUNT | DATABASE <db_name> | SCHEMA <schema_name> | APPLICATION <app_name> | APPLICATION PACKAGE <app_pkg_name> }
  FROM { ROLE | DATABASE ROLE } <grantee_name>

REVOKE ALL INHERITED CALLER PRIVILEGES
  ON ALL <object_type_plural>
  IN { ACCOUNT | DATABASE <db_name> | SCHEMA <schema_name> | APPLICATION <app_name> | APPLICATION PACKAGE <app_pkg_name> }
  FROM { ROLE | DATABASE ROLE } <grantee_name>
```

## Parameters

`object_privilege [ , object_privilege ... ]`
:   The object privileges that you want to revoke. Executables owned by the specified role can no longer
    run with these privileges. For a list of privileges for a specific object type, see [Access control privileges](/user-guide/security-access-control-privileges).

    Use a comma-delimited list to specify more than one object privilege.

`ON object_type object_name`
:   The object, including its type, that you want to revoke privileges for. Use the singular form of `object_type`, for example, `TABLE` or `WAREHOUSE`.

`ON ALL object_type_plural IN ACCOUNT` or `ON ALL object_type_plural IN DATABASE db_name` or `ON ALL object_type_plural IN SCHEMA schema_name` or `ON ALL object_type_plural IN APPLICATION app_name` or `ON ALL object_type_plural IN APPLICATION PACKAGE app_pkg_name`
:   Revokes privileges on all objects of a certain type. Use the plural form of the object type, for example, `TABLES` or `WAREHOUSES`.

    You can use the REVOKE statement to revoke access to all objects in the current account or just to objects in the specified database,
    schema, application, or application package.

`FROM ROLE grantee_name` or `FROM DATABASE ROLE grantee_name`
:   Executable owner who was previously granted a caller grant.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MANAGE CALLER GRANTS | Account | The account-level MANAGE CALLER GRANTS privilege pertains to caller grants only. It does not allow you to revoke privileges from roles. |
| Any privilege | All specified objects | You need at least one privilege on the objects specified in the REVOKE command. For example, revoking a caller grant on a table requires that you have at least one privilege on that table. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

Executables owned by `owner_role` can no longer run with the caller’s privileges when they access views in the current account.

> Copy code
>
> ```
> REVOKE ALL INHERITED CALLER PRIVILEGES ON ALL VIEWS IN ACCOUNT FROM ROLE owner_role;
> ```

Executables owned by `owner_role` can no longer run with the USAGE privilege when they access the `db.sch1` schema.

> Copy code
>
> ```
> REVOKE CALLER USAGE ON SCHEMA db.sch1 FROM ROLE owner_role;
> ```
