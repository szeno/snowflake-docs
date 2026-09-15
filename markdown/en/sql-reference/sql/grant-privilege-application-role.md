# GRANT *<privileges>* … TO APPLICATION ROLE

[Preview Feature](/release-notes/preview-features) — Open

Available to accounts in all non-government AWS regions. For details on other supported cloud platforms
contact your Snowflake representative.

Grants one or more access privileges on a securable schema-level object to an application role. The privileges that can be granted are
object-specific.

For more details about roles and securable objects, see [Overview of Access Control](/user-guide/security-access-control-overview).

Variations:
:   [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) , [REVOKE <privileges> … FROM APPLICATION ROLE](/sql-reference/sql/revoke-privilege-application-role)

## Syntax

Copy code

```
GRANT {
        { schemaPrivileges         | ALL [ PRIVILEGES ] } ON SCHEMA <schema_name>
        | { schemaObjectPrivileges | ALL [ PRIVILEGES ] } ON { <object_type> <object_name> | ALL <object_type_plural> IN { DATABASE <db_name> | SCHEMA <schema_name> }
        | { schemaObjectPrivileges | ALL [ PRIVILEGES ] } ON FUTURE <object_type_plural> IN SCHEMA <schema_name>
      }
    TO APPLICATION ROLE <name> [ WITH GRANT OPTION ]
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
  -- For { AGGREGATION | MASKING | PACKAGES | PASSWORD | PROJECTION | ROW ACCESS | SESSION } POLICY or TAG
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

`ON FUTURE`
:   Specifies that privileges are granted on new (i.e. future) schema objects of a specified type rather than existing objects. Future grants
    can be revoked at any time using [REVOKE <privileges> … FROM APPLICATION ROLE](/sql-reference/sql/revoke-privilege-application-role) with the ON FUTURE keywords; any privileges granted
    on existing objects are retained. For more information about future grants, see [Future Grants on Schema Objects](#future-grants-on-schema-objects) in this topic.

`WITH GRANT OPTION`
:   If specified, allows the recipient application role to grant the privileges to other application roles.

    Default: No value, which means the recipient application role cannot grant the privileges to other application roles.

    Note

    The WITH GRANT OPTION clause does not support the IMPORTED PRIVILEGES privilege. For more information, refer to
    [Granting privileges on an imported database](/user-guide/data-share-consumers#label-granting-privileges-on-shared-database).

## Usage notes

You must use an application role to grant and revoke privileges on objects in an application.

This command has different restrictions depending on whether you are the application provider or consumer.

The application consumer cannot do the following with respect to an application role:

- Grant or revoke object privileges with respect to an application role.
- Grant an application role to a database or share, or revoke an application role from a database or share.
- Grant an application role to same application or a different application, or revoke an application role from the same application or a
  different application.

These items apply the application provider with respect to an application role.

- To grant the OWNERSHIP privilege on an object or all objects of a specified type in a schema to an application role, transferring
  ownership of the object from one application role to another application role, use the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command.
- Multiple privileges can be specified for the same object type in a single GRANT statement with each privilege separated by commas.

  However, only privileges held and grantable by the application role executing the GRANT command are actually granted to the target
  application role. A warning message is returned for any privileges that could not be granted.
- Privileges granted to a particular application role are automatically inherited by any other application roles to which the application
  role is granted, as well as any other higher-level application roles within the role hierarchy.

  For more details, see [Overview of Access Control](/user-guide/security-access-control-overview).
- In managed access schemas:

  - The OWNERSHIP privilege on objects can only be transferred to a subordinate role of the schema owner.
  - For stages:
    - USAGE only applies to external stages.
    - READ
    - WRITE only applies to internal stages. In addition, to grant the WRITE privilege on an internal stage, the READ privilege must
      first be granted on the stage.

  For more details about external and internal stages, refer to [CREATE STAGE](/sql-reference/sql/create-stage) and [Access Control Requirements](#access-control-requirements)
  (in this topic).
- When granting privileges on an individual UDF or stored procedure, you must specify the data types of the arguments, if any,
  using the syntax shown below:

  Copy code

  ```
  <udf_or_stored_procedure_name> ( [ <arg_data_type> [ , ... ] ] )
  ```

  Snowflake uses argument data types to resolve UDFs and stored procedures that have the same name within a schema. For more
  information, refer [Overloading procedures and functions](/developer-guide/udf-stored-procedure-naming-conventions#label-procedure-function-name-overloading).

## Access control requirements

- This command can only be executed from within the application.
- Privileges can only be granted or revoked on objects owned by the application. To determine these objects,
  use the [SHOW OBJECTS](/sql-reference/sql/show-objects) command:

  Copy code

  ```
  SHOW OBJECTS OWNED BY APPLICATION myapp;
  ```
- Regarding managed access schemas:

  - In managed access schemas (i.e. schemas created using the CREATE SCHEMA … WITH MANAGED ACCESS syntax), object owners lose
    the ability to make grant decisions.

    The following roles can grant privileges on objects in a managed access schema:

    - The application role because this role is the schema owner (i.e. the role with the OWNERSHIP privilege on the schema).
    - A role that inherits the application role.
    - A role with the global MANAGE GRANTS privilege can grant privileges on objects in the schema.

      A role that holds the global MANAGE GRANTS privilege can grant additional privileges to the current (grantor) role.
  - Refer to [Future Grants on Schema Objects](#future-grants-on-schema-objects) (in this topic) for the access control requirements of future grants in managed access
    schemas.

## Future grants on schema objects

The notes in these sections apply when assigning future grants on objects in a schema (i.e. when using the ON FUTURE keywords).

### Considerations

- When future grants are defined on the same object type for a schema, the schema-level grants take precedence over the database
  level grants, and the database level grants are ignored. This behavior applies to privileges on future objects granted to one application
  role or different application roles.

### Restrictions and limitations

- No more than one future grant of the OWNERSHIP privilege is allowed on each securable object type.

- Future grants cannot be defined on objects of the following types:
  - Compute pool
  - External function
  - Image repository
  - Organization profile
  - Policy objects:

    - Aggregation policy
    - Join policy
    - Masking policy
    - Packages policy
    - Projection policy
    - Row access policy
    - Session policy
    - Storage lifecycle policy
  - Snapshot
  - Tag

- A future grant of the OWNERSHIP privilege on objects of a specified type in a database do not apply to new objects in a managed
  access schema.
- The following restrictions apply to future grants on objects in a managed access schema:

  - A future grant of the OWNERSHIP privilege on objects can only be applied to a subordinate role of the schema owner
    (i.e. the role that has the OWNERSHIP privilege on the schema).
  - Before ownership of a managed access schema can be transferred to a different role, all open future grants of the OWNERSHIP
    privilege must be revoked using [REVOKE <privileges> … FROM ROLE](/sql-reference/sql/revoke-privilege) with the ON FUTURE keywords.
- Future grants are not applied when renaming or swapping a table.
- Future grants are supported on named stages with the following restrictions:

  - The WRITE privilege cannot be specified without the READ privilege.
  - The READ privilege cannot be revoked if the WRITE privilege is present.
  - For internal stages, only future grants with the READ or WRITE privilege are materialized.
  - For external stages, only future grants with the USAGE privileges are materialized.
- In a managed access schema, the application role and a role with the global MANAGE GRANTS privilege can grant privileges on future
  objects in the managed access schema.

  In standard schemas, the global MANAGE GRANTS privilege is required to grant privileges on future objects in the schema.

## Example

Grant the SELECT privilege on a view to an application role:

Copy code

```
GRANT SELECT ON VIEW data.views.credit_usage
  TO APPLICATION ROLE app_snowflake_credits;
```
