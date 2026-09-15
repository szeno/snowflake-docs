# GRANT CALLER

Grants [caller grants](/developer-guide/restricted-callers-rights#label-restricted-callers-rights-about-grants) to a role. If an executable owned by the role runs with restricted caller’s rights, it can only run with the caller’s privileges specified by the caller grants.

Variations of the GRANT CALLER command are as follows:

- GRANT CALLER — Grant caller grants on a specific object. Each caller grant created by the statement allows the executable to
  run with a specified privilege.
- GRANT ALL CALLER PRIVILEGES — Grant caller grants on a specific object. The caller grants created by the statement allow the
  executable to run with all of the caller’s privileges.
- GRANT INHERITED CALLER — Grant caller grants on all current and future objects of the same type when they share a common schema, database,
  or account. Each caller grant created by the statement allows the executable to run with a specified privilege.
- GRANT ALL INHERITED CALLER PRIVILEGES — Grant caller grants on all current and future objects of the same type when they share a common
  schema, database, or account. The caller grants created by the statement allow the executable to run with all of the caller’s privileges.

## Syntax

Copy code

```
GRANT CALLER <object_privilege> [ , <object_privilege> ... ]
  ON <object_type> <object_name>
  TO { ROLE | DATABASE ROLE | APPLICATION } <grantee_name>

GRANT ALL CALLER PRIVILEGES
  ON <object_type> <object_name>
  TO { ROLE | DATABASE ROLE | APPLICATION } <grantee_name>

GRANT INHERITED CALLER <object_privilege> [ , <object_privilege> ... ]
  ON ALL <object_type_plural>
  IN { ACCOUNT | DATABASE <db_name> | SCHEMA <schema_name> | APPLICATION <app_name> | APPLICATION PACKAGE <app_pkg_name> }
  TO { ROLE | DATABASE ROLE | APPLICATION } <grantee_name>

GRANT ALL INHERITED CALLER PRIVILEGES
  ON ALL <object_type_plural>
  IN { ACCOUNT | DATABASE <db_name> | SCHEMA <schema_name> | APPLICATION <app_name> | APPLICATION PACKAGE <app_pkg_name> }
  TO { ROLE | DATABASE ROLE | APPLICATION } <grantee_name>
```

## Parameters

`object_privilege [ , object_privilege ... ]`
:   The object privileges that executables can run with. For a list of privileges for a specific object type, see
    [Access control privileges](/user-guide/security-access-control-privileges).

    Use a comma-delimited list to specify more than one object privilege.

`ON object_type object_name`
:   Allows an executable to run with the specified `object_privilege` when accessing the specified object (`object_name`). Use
    the singular form of `object_type`, for example, `TABLE` or `WAREHOUSE`.

`ON ALL object_type_plural IN ACCOUNT` or `ON ALL object_type_plural IN DATABASE db_name` or `ON ALL object_type_plural IN SCHEMA schema_name` or `ON ALL object_type_plural IN APPLICATION app_name` or `ON ALL object_type_plural IN APPLICATION PACKAGE app_pkg_name`
:   Allows an executable to run with object-level privileges when accessing an object of the specified type. Use the plural form of
    the object type, for example, `TABLES` or `WAREHOUSES`.

    You can use the GRANT statement to control access to all objects in the current account, or just objects in the specified
    database, schema, application, or application package.

`TO ROLE grantee_name` or `TO DATABASE ROLE grantee_name`
:   Owner of the executables that you want to secure with caller grants.

    If you specify a database role, privileges are limited to objects in the same database as the database role.

`TO APPLICATION app_name`
:   Specifies a Snowflake Native App as the grantee.

    Note

    If you specify IN ACCOUNT, not all object types are supported when using TO APPLICATION.
    Only the following objects are supported:

    - DATABASE
    - APPLICATION PACKAGE
    - APPLICATION
    - Object types that are contained within a database or schema.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MANAGE CALLER GRANTS | Account | The account-level MANAGE CALLER GRANTS privilege pertains to caller grants only. It does not allow you to grant privileges to roles. |
| Any privilege | All specified objects | You need at least one privilege on the objects specified in the caller grant. For example, granting a caller grant on a table requires that you have at least one privilege on that table. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

Executables owned by `owner_role` that access a `v1` view can run with the SELECT privilege on the view:

> Copy code
>
> ```
> GRANT CALLER SELECT ON VIEW v1 TO owner_role;
> ```

Executables owned by `owner_role` that access any table in the `db.sch` schema can run with the caller’s SELECT and INSERT privileges.

> Copy code
>
> ```
> GRANT INHERITED CALLER SELECT, INSERT ON ALL TABLES IN SCHEMA db.sch TO ROLE owner_role;
> ```

Executables owned by `owner_role` that access schemas in the current account can run with all of the caller’s privileges on the schemas.

> Copy code
>
> ```
> GRANT ALL INHERITED CALLER PRIVILEGES ON ALL SCHEMAS IN ACCOUNT TO ROLE owner_role;
> ```

Executables owned by the `db.r` database role that access the `db.sch1.t1` table can run with the SELECT privilege on the table.

> Copy code
>
> ```
> GRANT CALLER SELECT ON TABLE db.sch1.t1 TO DATABASE ROLE db.r;
> ```

Executables owned by `owner_role` that access the `my_db` database can run with all of the caller’s privileges on the database.

> Copy code
>
> ```
> GRANT ALL CALLER PRIVILEGES ON DATABASE my_db TO ROLE owner_role;
> ```
