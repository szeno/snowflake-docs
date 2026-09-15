# REVOKE *<privileges>* … FROM APPLICATION

Revokes one or more access privileges on a securable object from an application. The privileges that can be revoked are
object-specific.

For more details about roles and securable objects, see [Overview of Access Control](/user-guide/security-access-control-overview).

Variations:
:   [GRANT <privileges> … TO APPLICATION](/sql-reference/sql/grant-privilege-application)

## Syntax

Copy code

```
REVOKE {  { globalPrivileges } ON ACCOUNT
        | { accountObjectPrivileges  | ALL [ PRIVILEGES ] } ON { USER | RESOURCE MONITOR | WAREHOUSE | COMPUTE POOL | DATABASE | INTEGRATION | CONNECTION | FAILOVER GROUP | REPLICATION GROUP | EXTERNAL VOLUME } <object_name>
        | { schemaPrivileges         | ALL [ PRIVILEGES ] } ON { SCHEMA <schema_name> | ALL SCHEMAS IN DATABASE <db_name> }
        | { schemaObjectPrivileges   | ALL [ PRIVILEGES ] } ON { <object_type> <object_name> | ALL <object_type_plural> IN { DATABASE <db_name> | SCHEMA <schema_name> }
       }
     FROM APPLICATION <name>
```

Where:

Copy code

```
globalPrivileges ::=
  {
      CREATE {
       COMPUTE POOL | DATABASE | WAREHOUSE
      }
      | BIND SERVICE ENDPOINT
      | EXECUTE MANAGED TASK
      | MANAGE WAREHOUSES
      | READ SESSION
  }
  [ , ... ]
```

Copy code

```
accountObjectPrivileges ::=
-- For COMPUTE POOL
   { MODIFY | MONITOR | OPERATE | USAGE } [ , ... ]
-- For CONNECTION
   { FAILOVER } [ , ... ]
-- For DATABASE
   { APPLYBUDGET | CREATE { DATABASE ROLE | SCHEMA }
   | IMPORTED PRIVILEGES | MODIFY | MONITOR | USAGE } [ , ... ]
-- For EXTERNAL VOLUME
   { USAGE } [ , ... ]
-- For FAILOVER GROUP
   { FAILOVER | MODIFY | MONITOR | REPLICATE } [ , ... ]
-- For INTEGRATION
   { USAGE | USE_ANY_ROLE } [ , ... ]
-- For REPLICATION GROUP
   { MODIFY | MONITOR | REPLICATE } [ , ... ]
-- For RESOURCE MONITOR
   { MODIFY | MONITOR } [ , ... ]
-- For USER
   { MONITOR } [ , ... ]
-- For WAREHOUSE
   { APPLYBUDGET | MODIFY | MONITOR | USAGE | OPERATE } [ , ... ]
```

Copy code

```
schemaPrivileges ::=
ADD SEARCH OPTIMIZATION
| CREATE {
    ALERT | EXTERNAL TABLE | FILE FORMAT | FUNCTION
    | IMAGE REPOSITORY | MATERIALIZED VIEW | PIPE | PROCEDURE
    | { AGGREGATION | MASKING | PASSWORD | PROJECTION | ROW ACCESS | SESSION } POLICY
    | SECRET | SEMANTIC VIEW | SEQUENCE | SERVICE | SNAPSHOT | STAGE | STREAM
    | TAG | TABLE | TASK | VIEW
  }
| MODIFY | MONITOR | USAGE
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
  -- For MATERIALIZED VIEW
     { APPLYBUDGET | REFERENCES | SELECT } [ , ... ]
```

For more information about the privileges supported for each object type, see [Access control privileges](/user-guide/security-access-control-privileges).

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

    Bulk grants on pipes are not allowed.

`name`
:   Specifies the identifier for the recipient application (the role to which the privileges are granted).

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

    In managed access schemas (schemas created using the CREATE SCHEMA … WITH MANAGED ACCESS syntax), only the schema owner (the
    role with the OWNERSHIP privilege on the schema) or a role with the global MANAGE GRANTS privilege, or a higher role, can revoke
    privileges on objects in the schema.

## Usage notes

- Privileges cannot be granted or revoked directly on any class. You can, however, create an instance of a class and
  revoke [instance roles](/sql-reference/snowflake-db-classes#label-instance-roles) from an
  account role. Revoke the CREATE <class\_name> privilege on the schema to prevent a role from creating an instance of a
  class.
- A privilege can be granted to a role multiple times by different grantors. A REVOKE *<privilege>* statement only revokes grants for which
  the active role, or a lower role in a hierarchy, is the grantor. Any additional grants of a specified privilege by other grantors are
  ignored.

  Also note that a REVOKE *<privilege>* statement is successful even if no privileges are revoked. A REVOKE *<privilege>* statement only
  returns an error if a specified privilege has dependent grants and the CASCADE clause is omitted in the statement.
- Multiple privileges can be specified for the same object type in a single GRANT statement (with each privilege separated by commas),
  or the special `ALL [ PRIVILEGES ]` keyword can be used to grant all applicable privileges to the specified object type. Note,
  however, that only privileges held and grantable by the role executing the GRANT command are actually granted to the target role.
  A warning message is returned for any privileges that could not be granted.

  You cannot specify this keyword for tags.
- For databases, the IMPORTED PRIVILEGES privilege only applies to shared databases (i.e. databases created from a share). For more
  details, see [Consume imported data](/user-guide/data-share-consumers).
- For schemas and objects in schemas, an option is provided to grant privileges on all objects of the same type within the container
  (database or schema). This is a convenience option; internally, the command is expanded into a series of individual GRANT commands
  on each object. Only objects that currently exist within the container are affected.

  However, note that, in the Snowflake model, bulk granting of privileges is not a recommended practice. Instead, Snowflake recommends
  creating a shared role and using the role to create objects that are automatically accessible to all users who have been granted the
  role.
- For stages:

  - USAGE only applies to external stages.
  - READ | WRITE only applies to internal stages. In addition, to grant the WRITE privilege on an internal stage, the READ privilege
    must first be granted on the stage.

  For more details about external and internal stages, see [CREATE STAGE](/sql-reference/sql/create-stage).
- When granting privileges on an individual UDF, you must specify the data types for the arguments, if any, for the UDF in the form of
  `udf_name ( [ arg_data_type , ... ] )`. This is required because Snowflake uses argument data types to resolve UDFs that
  have the same name within a schema. For more details, see
  [User-defined functions overview](/developer-guide/udf/udf-overview).
- When granting privileges on an individual stored procedure, you must specify the data types for the arguments, if any, for the
  procedure in the form of `procedure_name ( [ arg_data_type , ... ] )`. This is required because Snowflake uses argument
  data types to resolve stored procedures that have the same name within a schema.

  For more information, see [managed access schemas](/user-guide/security-access-control-configure#label-managed-access-schemas).

## Example

Revoke the SELECT privilege on a view from an application:

Copy code

```
REVOKE SELECT ON VIEW data.views.credit_usage
  FROM APPLICATION app_snowflake_credits;
```
