# REVOKE *<privileges>* … FROM APPLICATION ROLE

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Revokes one or more access privileges on a securable schema-level object from an application role. The privileges that can be revoked are
object-specific.

For more details about roles and securable objects, see [Overview of Access Control](/user-guide/security-access-control-overview).

Variations:
:   [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) , [GRANT <privileges> … TO APPLICATION ROLE](/sql-reference/sql/grant-privilege-application-role)

## Syntax

Account roles:

Copy code

```
REVOKE [ GRANT OPTION FOR ]
    {
    | { schemaPrivileges         | ALL [ PRIVILEGES ] } ON { SCHEMA <schema_name> | ALL SCHEMAS IN DATABASE <db_name> }
    | { schemaPrivileges         | ALL [ PRIVILEGES ] } ON { FUTURE SCHEMAS IN DATABASE <db_name> }
    | { schemaObjectPrivileges   | ALL [ PRIVILEGES ] } ON { <object_type> <object_name> | ALL <object_type_plural> IN SCHEMA <schema_name> }
    | { schemaObjectPrivileges   | ALL [ PRIVILEGES ] } ON FUTURE <object_type_plural> IN { DATABASE <db_name> | SCHEMA <schema_name> }
    }
  FROM APPLICATION ROLE <name> [ RESTRICT | CASCADE ]
```

Where:

Copy code

```
schemaPrivileges ::=
  {
    ADD SEARCH OPTIMIZATION
    | CREATE {
        ALERT | EXTERNAL TABLE | FILE FORMAT | FUNCTION
        | IMAGE REPOSITORY | MATERIALIZED VIEW | PIPE | PROCEDURE
        | { AGGREGATION | MASKING | PASSWORD | PROJECTION | ROW ACCESS | SESSION } POLICY
        | SECRET | SEMANTIC VIEW | SEQUENCE | SERVICE | SNAPSHOT | STAGE | STREAM
        | TAG | TABLE | TASK | VIEW
      }
    | MODIFY | MONITOR | USAGE
  }
  [ , ... ]
```

Copy code

```
schemaObjectPrivileges ::=
  -- For ALERT
     { MONITOR | OPERATE } [ , ... ]
  -- For DYNAMIC TABLE
     OPERATE, SELECT [ , ...]
  -- For EVENT TABLE
     { INSERT | SELECT } [ , ... ]
  -- For FILE FORMAT, FUNCTION (UDF or external function), PROCEDURE, SECRET, SEQUENCE, SNAPSHOT, or TYPE
     USAGE [ , ... ]
  -- For IMAGE REPOSITORY
     { READ, WRITE } [ , ... ]
  -- For MATERIALIZED VIEW
     { APPLYBUDGET | REFERENCES | SELECT } [ , ... ]
  -- For PIPE
     { APPLYBUDGET | MONITOR | OPERATE } [ , ... ]
  -- For { MASKING | PACKAGES | PASSWORD | ROW ACCESS | SESSION } POLICY or TAG
     APPLY [ , ... ]
  -- For SECRET
     READ, USAGE [ , ... ]
  -- For SEMANTIC VIEW
     REFERENCES [ , ... ]
  -- For SERVICE
     { MONITOR | OPERATE } [ , ... ]
  -- For external STAGE
     USAGE [ , ... ]
  -- For internal STAGE
     READ [ , WRITE ] [ , ... ]
  -- For STREAM
     SELECT [ , ... ]
  -- For TABLE
     { APPLYBUDGET | DELETE | EVOLVE SCHEMA | INSERT | REFERENCES | SELECT | TRUNCATE | UPDATE } [ , ... ]
  -- For TAG
     READ
  -- For TASK
     { APPLYBUDGET | MONITOR | OPERATE } [ , ... ]
  -- For VIEW
     { REFERENCES | SELECT } [ , ... ]
```

For more details about the privileges supported for each object type, see [Access control privileges](/user-guide/security-access-control-privileges).

## Required parameters

`object_name`
:   Specifies the identifier for the object on which the privileges are granted.

`object_type`
:   Specifies the type of object for schema-level objects.

    - `ALERT`
    - `DYNAMIC TABLE`
    - `EVENT TABLE`
    - `EXTERNAL TABLE`
    - `FILE FORMAT`
    - `FUNCTION`
    - `MASKING POLICY`
    - `MATERIALIZED VIEW`
    - `NETWORK RULE`
    - `PACKAGES POLICY`
    - `PASSWORD POLICY`
    - `PIPE`
    - `PROCEDURE`
    - `ROW ACCESS POLICY`
    - `SECRET`
    - `SEMANTIC VIEW`
    - `SESSION POLICY`
    - `SEQUENCE`
    - `STAGE`
    - `STREAM`
    - `TABLE`
    - `TAG`
    - `TASK`
    - `TYPE`
    - `VIEW`

`object_type_plural`
:   Plural form of `object_type` (e.g. `TABLES`, `VIEWS`).

    Note that bulk grants on pipes are not allowed.

`name`
:   Specifies the identifier for the recipient application role (i.e. the role to which the privileges are granted).

## Optional parameters

`FUTURE`
:   If specified, only removes privileges granted on new (i.e. future) schema objects of a specified type (e.g. tables or views) rather than
    existing objects. Note that any privileges granted on existing objects are retained.

`RESTRICT | CASCADE`
:   If specified, determines whether the revoke operation succeeds or fails for the privileges, based on the whether the privileges had been
    re-granted to another application role.

    `RESTRICT`
    :   If the privilege being revoked has been re-granted to another application role, the REVOKE command fails.

    `CASCADE`
    :   If the privilege being revoked has been re-granted, the REVOKE command recursively revokes these dependent grants. If the same
        privilege on an object has been granted to the target role by a different grantor (parallel grant), that grant is not affected and the
        target role retains the privilege.

    Default: `RESTRICT`

## Security requirements

Revoking privileges on individual objects:
:   You can use an [active role](/user-guide/security-access-control-overview#label-access-control-overview-active-roles) that meets either of the following criteria, or a
    [higher role](/user-guide/security-access-control-overview#label-role-hierarchy-and-privilege-inheritance), to revoke privileges on an object from other application
    roles:

    - The role is identified as the *grantor* of the privilege in the GRANTED\_BY column in the [SHOW GRANTS](/sql-reference/sql/show-grants) output.

      If you have multiple instances of a privilege grant on the specified object, only the instances granted by the active grantor role
      are revoked.
    - The role has the global MANAGE GRANTS privilege.

      If you have multiple instances of a privilege grant on the specified object, all instances are revoked.

      Note that only the SECURITYADMIN system role and higher have the MANAGE GRANTS privilege by default; however, the privilege can be
      granted to custom roles.

    The following roles can revoke privileges from objects in a managed access schema
    (i.e. schemas created using the CREATE SCHEMA … WITH MANAGED ACCESS syntax):

    - The application role because this role is the schema owner (i.e. has the OWNERSHIP privilege on the schema).
      (i.e. the role with the OWNERSHIP privilege on the schema)
    - A role with the global MANAGE GRANTS privilege.

Revoking grants on future objects of a specified type:
:   In managed access schemas, either the application role or a role with the global MANAGE GRANTS privilege can revoke privileges on
    future objects in the schema.

    In standard schemas, the global MANAGE GRANTS privilege is required to revoke privileges on future objects in the schema.

## Usage notes

- A privilege can be granted to an application role multiple times by different grantors. A REVOKE *<privilege>* statement only revokes
  grants for which the active role, or a lower role in a hierarchy, is the grantor. Any additional grants of a specified privilege by other
  grantors are ignored.

  A REVOKE *<privilege>* statement is successful even if no privileges are revoked. A REVOKE *<privilege>* statement only
  returns an error if a specified privilege has dependent grants and the CASCADE clause is omitted in the statement.
- When revoking privileges on an individual UDF, you must specify the data types for the arguments, if any, for the UDF in the form of
  `udf_name ( [ arg_data_type , ... ] )`. This is required because Snowflake uses argument data types to resolve UDFs that
  have the same name within a schema. For more details, refer [User-defined functions overview](/developer-guide/udf/udf-overview).
- When revoking privileges on an individual stored procedure, you must specify the data types for the arguments, if any, for the
  procedure in the form of `procedure_name ( [ arg_data_type , ... ] )`. This is required because Snowflake uses argument
  data types to resolve stored procedures that have the same name within a schema.
- **Future grants:** Revoking future grants only drops grants of privileges for future objects of a specified type. Any
  privileges granted on existing objects are retained.

  For more information, see [managed access schemas](/user-guide/security-access-control-configure#label-managed-access-schemas).

## Example

Revoke the SELECT privilege on a view from an application role:

Copy code

```
REVOKE SELECT ON VIEW data.views.credit_usage
  FROM APPLICATION ROLE app_snowflake_credits;
```
