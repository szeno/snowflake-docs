# GRANT *<privileges>* … TO USER

Grants one or more access privileges on a securable object to a user. The privileges that can be granted are object-specific.

For more information about roles and securable objects, see [Overview of Access Control](/user-guide/security-access-control-overview).

For more information about privileges, see [Access control privileges](/user-guide/security-access-control-privileges).

See also:
:   [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) , [REVOKE <privileges> … FROM USER](/sql-reference/sql/revoke-privilege-user)

## Syntax

Copy code

```
GRANT {  { globalPrivileges         | ALL [ PRIVILEGES ] } ON ACCOUNT
       | { accountObjectPrivileges  | ALL [ PRIVILEGES ] } ON { USER | RESOURCE MONITOR | WAREHOUSE | COMPUTE POOL | DATABASE | INTEGRATION | CONNECTION | FAILOVER GROUP | REPLICATION GROUP | EXTERNAL VOLUME } <object_name>
       | { schemaPrivileges         | ALL [ PRIVILEGES ] } ON { SCHEMA <schema_name> | ALL SCHEMAS IN DATABASE <db_name> }
       | { schemaObjectPrivileges   | ALL [ PRIVILEGES ] } ON { <object_type> <object_name> | ALL <object_type_plural> IN { DATABASE <db_name> | SCHEMA <schema_name> } }
      }
  TO [ USER ] <user_name> [ WITH GRANT OPTION ]
```

Where:

Copy code

```
globalPrivileges ::=
  {
      | ATTACH POLICY | AUDIT | BIND SERVICE ENDPOINT
      | APPLY {
         { AGGREGATION | AUTHENTICATION | JOIN | MASKING | PACKAGES | PASSWORD
           | PROJECTION | ROW ACCESS | SESSION } POLICY
         | TAG }
      | EXECUTE { ALERT | DATA METRIC FUNCTION | MANAGED ALERT | MANAGED TASK | TASK }
      | IMPORT SHARE
      | MANAGE { ACCOUNT SUPPORT CASES | EVENT SHARING | GRANTS | LISTING AUTO FULFILLMENT | ORGANIZATION SUPPORT CASES | USER SUPPORT CASES | WAREHOUSES }
      | MODIFY { LOG LEVEL | TRACE LEVEL | SESSION LOG LEVEL | SESSION TRACE LEVEL }
      | MONITOR { EXECUTION | SECURITY | USAGE }
      | OVERRIDE SHARE RESTRICTIONS | PURCHASE DATA EXCHANGE LISTING | RESOLVE ALL
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
   { APPLYBUDGET
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

    ADD SEARCH OPTIMIZATION | APPLYBUDGET
   | MODIFY | MONITOR | USAGE
   [ , ... ]
```

Copy code

```
schemaObjectPrivileges ::=
  -- For ALERT
     { MONITOR | OPERATE } [ , ... ]
  -- For DATA METRIC FUNCTION
     USAGE [ , ... ]
  -- For DYNAMIC TABLE
     MONITOR, OPERATE, SELECT [ , ...]
  -- For EVENT TABLE
     { APPLYBUDGET | DELETE | REFERENCES | SELECT | TRUNCATE } [ , ... ]
  -- For FILE FORMAT, FUNCTION (UDF or external function), MODEL, PROCEDURE, SECRET, SEQUENCE, SNAPSHOT, or TYPE
     USAGE [ , ... ]
  -- For GIT REPOSITORY
     { READ, WRITE } [ , ... ]
  -- For HYBRID TABLE
     { APPLYBUDGET | DELETE | INSERT | REFERENCES | SELECT | TRUNCATE | UPDATE } [ , ... ]
  -- For IMAGE REPOSITORY
     { READ, WRITE } [ , ... ]
  -- For ICEBERG TABLE
     { APPLYBUDGET | DELETE | INSERT | REFERENCES | SELECT | TRUNCATE | UPDATE } [ , ... ]
  -- For MATERIALIZED VIEW
     { APPLYBUDGET | REFERENCES | SELECT } [ , ... ]
  -- For PIPE
     { APPLYBUDGET | MONITOR | OPERATE } [ , ... ]
  -- For { AGGREGATION | AUTHENTICATION | MASKING | JOIN | PACKAGES | PASSWORD | PRIVACY | PROJECTION | ROW ACCESS | SESSION } POLICY or TAG
     APPLY [ , ... ]
  -- For SECRET
     { READ | USAGE } [ , ... ]
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
  -- For STREAMLIT
     USAGE [ , ... ]
  -- For TABLE
     { APPLYBUDGET | DELETE | EVOLVE SCHEMA | INSERT | REFERENCES | SELECT | SELECT ERROR TABLE | TRUNCATE | UPDATE } [ , ... ]
  -- For TAG
     READ
  -- For TASK
     { APPLYBUDGET | MONITOR | OPERATE } [ , ... ]
  -- For VIEW
     { REFERENCES | SELECT } [ , ... ]
```

For more information about the privileges supported for each object type, see [Access control privileges](/user-guide/security-access-control-privileges).

## Required parameters

`object_name`
:   Specifies the identifier for the object on which the privileges are granted.

`object_type`
:   Specifies the type of object for schema-level objects.

    - `AGENT`
    - `AGGREGATION POLICY`
    - `ALERT`
    - `AUTHENTICATION POLICY`
    - `CORTEX SEARCH SERVICE`
    - `DATA METRIC FUNCTION`
    - `DATASET`
    - `DBT PROJECT`
    - `DYNAMIC TABLE`
    - `EVENT TABLE`
    - `EXPERIMENT`
    - `EXTERNAL TABLE`
    - `FILE FORMAT`
    - `FUNCTION`
    - `GATEWAY`
    - `GIT REPOSITORY`
    - `IMAGE REPOSITORY`
    - `ICEBERG TABLE`
    - `INTERACTIVE TABLE`
    - `JOIN POLICY`
    - `MASKING POLICY`
    - `MATERIALIZED VIEW`
    - `MCP SERVER`
    - `MODEL`
    - `MODEL MONITOR`
    - `NETWORK RULE`
    - `NOTEBOOK`
    - `ONLINE FEATURE TABLE`
    - `PACKAGES POLICY`
    - `PASSWORD POLICY`
    - `PIPE`
    - `PRIVACY POLICY`
    - `PROCEDURE`
    - `PROJECTION POLICY`
    - `RESTRICTED SESSION SCOPE`
    - `ROW ACCESS POLICY`
    - `SECRET`
    - `SEMANTIC VIEW`
    - `SERVICE`
    - `SESSION POLICY`
    - `SEQUENCE`
    - `SNAPSHOT`
    - `SNAPSHOT POLICY`
    - `SNAPSHOT SET`
    - `STAGE`
    - `STORAGE LIFECYCLE POLICY`
    - `STREAM`
    - `STREAMLIT`
    - `TABLE`
    - `TAG`
    - `TASK`
    - `TYPE`
    - `VIEW`
    - `WORKSPACE`

`object_type_plural`
:   Plural form of `object_type` (for example `TABLES`, `VIEWS`).

    Note that bulk grants on pipes are not allowed.

`user_name`
:   Specifies the identifier for the recipient user (the user to which the privileges are granted).

## Optional parameters

`WITH GRANT OPTION`
:   If specified, allows the recipient user to grant the privileges to other roles or users.

    Default: No value, which means the recipient role cannot grant the privileges to other roles or users.

    Note

    The WITH GRANT OPTION parameter does not support the IMPORTED PRIVILEGES privilege. For more information, see
    [Granting privileges on an imported database](/user-guide/data-share-consumers#label-granting-privileges-on-shared-database).

## Usage notes

- Privileges assigned directly to users are only effective when the user has all secondary roles enabled.
- Granting privileges directly to users may increase the proliferation of grants in your account. Outside of person-to-person sharing
  scenarios, we recommend that you grant privileges to roles to manage access that users need in Snowflake.
- [Future grants](/sql-reference/sql/grant-privilege#label-grant-privilege-schema-future-grants) is not available.
- CREATE and OWNERSHIP privileges cannot be granted to users.

- Privileges cannot be granted or revoked directly on any class.

- Multiple privileges can be specified for the same object type in a single GRANT statement (with each privilege separated by commas).
  Alternatively, the special `ALL [ PRIVILEGES ]` keyword can be used to grant all applicable privileges to the specified object type.

  Note

  - Only privileges held and grantable by the user executing the GRANT command are actually granted to the target role. A warning message
    is returned for any privileges not granted.
  - You cannot specify `ALL [ PRIVILEGES ]` for tags.
  - `ALL [ PRIVILEGES ]` does not grant privileges on a *class* if you try to grant `ALL [ PRIVILEGES ]` on a *schema*.

- For schemas and objects in schemas, an `ALL object_type_plural IN container` option is provided to grant privileges on all
  objects of the same type within the container (that is, database or schema). This option provides convenience. Internally, the command is
  expanded into a series of individual GRANT commands on each object. This option only affects objects that currently exist within the
  container.

  Note

  Bulk granting of privileges is not a recommended practice in the Snowflake model. Instead, Snowflake recommends creating a shared role and
  then using that role to create objects that are automatically accessible to all users who have been granted the role.

  You cannot specify ALL TAGS or ALL MASKING POLICIES.

- For stages:

  - USAGE only applies to external stages.
  - READ | WRITE only applies to internal stages. In addition, to grant the WRITE privilege on an internal stage, the READ
    privilege must first be granted on the stage.

  For more information about external and internal stages, see [CREATE STAGE](/sql-reference/sql/create-stage).
- When granting privileges on an individual UDF or stored procedure, you must specify the data types of the arguments, if any,
  using syntax such as `udf_or_stored_procedure_name ( [ arg_data_type [ , ... ] ] )`. Snowflake uses argument data types to
  resolve UDFs or stored procedures that have the same name within a schema. For more information, see [Overloading procedures and functions](/developer-guide/udf-stored-procedure-naming-conventions#label-procedure-function-name-overloading).
- For dynamic tables, the receiving user must be granted the USAGE privilege on the database and schema that contains the dynamic table, and
  on the warehouse used to refresh the table. For more information, see [Dynamic table access control](/user-guide/dynamic-tables/privileges).
- When granting privileges on an individual UDF, you must specify the data types for the arguments, if any, for the UDF using syntax such as
  `udf_name ( [ arg_data_type , ... ] )`. This is required because Snowflake uses argument data types to resolve UDFs that
  have the same name within a schema. For more information, see [User-defined functions overview](/developer-guide/udf/udf-overview).
- When granting privileges on an individual stored procedure, you must specify the data types for the arguments, if any, for the
  procedure using syntax such as `procedure_name ( [ arg_data_type , ... ] )`. This is required because Snowflake uses argument
  data types to resolve stored procedures that have the same name within a schema.

  For more information, see [managed access schemas](/user-guide/security-access-control-configure#label-managed-access-schemas).

## Access control requirements

Granting privileges on individual objects:
:   In general, a role or user with any one of the following privileges can grant privileges on an object to other users:

    - The global `MANAGE GRANTS` privilege.

      Only the SECURITYADMIN and ACCOUNTADMIN system roles have the MANAGE GRANTS privilege; however, the privilege can be granted
      to custom roles or users.
    - The OWNERSHIP privilege.

      The role that has OWNERSHIP privilege on the object.
    - The USAGE privilege.
      When granting privileges on schema objects (for example, tables and views), the role or user must also have the USAGE privilege on the
      parent database and schema.

    If a privilege has been granted to a user with the `GRANT privileges ... TO USER WITH GRANT OPTION` command, then that user can
    re-grant that same privilege to other users or roles.

    In [managed access schemas](/user-guide/security-access-control-configure#label-managed-access-schemas) (schemas created using the `CREATE SCHEMA ... WITH MANAGED ACCESS`)
    syntax, object owners lose the ability to make grant decisions. Only the schema owner (the role with the OWNERSHIP privilege on the
    schema) or a role with the global MANAGE GRANTS privilege can grant privileges on objects in that schema.

    Note

    A role that holds the global MANAGE GRANTS privilege can grant additional privileges to the current (grantor) role or user.

## Examples

To grant the USAGE privilege on a Streamlit application to a specific user, `joe`:

Copy code

```
GRANT USAGE ON STREAMLIT streamlit_db.streamlit_schema.streamlit_app TO USER joe;
```

To grant the USAGE privilege on a procedure to a specific user, `user1`:

Copy code

```
GRANT USAGE ON PROCEDURE mydb.myschema.myprocedure(number) TO USER user1;
```
