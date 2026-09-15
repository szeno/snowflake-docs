# REVOKE *<privileges>* … FROM ROLE

Removes one or more privileges on a securable object from a role or database role. The privileges that can be revoked are object-specific.

Roles:
:   The privileges that can be revoked from roles are grouped into the following categories:

    - Global privileges
    - Privileges for account objects (resource monitors, virtual warehouses, and databases)
    - Privileges for schemas
    - Privileges for schema objects (tables, views, stages, file formats, UDFs, and sequences)

Database roles:
:   The privileges that can be revoked from database roles are grouped into the following categories:

    - Privileges for the database that contains the database role.
    - Privileges for schemas in the database that contains the database role.
    - Privileges for schema objects (tables, views, stages, file formats, UDFs, and sequences) in the database that contains the database role.

See also:
:   [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) , [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership)

    [REVOKE <privilege> … FROM SHARE](/sql-reference/sql/revoke-privilege-share)

## Syntax

Account roles:

Copy code

```
REVOKE [ GRANT OPTION FOR ]
    {
       { globalPrivileges         | ALL [ PRIVILEGES ] } ON ACCOUNT
     | { accountObjectPrivileges  | ALL [ PRIVILEGES ] } ON { RESOURCE MONITOR | WAREHOUSE | COMPUTE POOL | DATABASE | INTEGRATION | CONNECTION | FAILOVER GROUP | REPLICATION GROUP | EXTERNAL VOLUME } <object_name>
     | { schemaPrivileges         | ALL [ PRIVILEGES ] } ON { SCHEMA <schema_name> | ALL SCHEMAS IN DATABASE <db_name> }
     | { schemaPrivileges         | ALL [ PRIVILEGES ] } ON { FUTURE SCHEMAS IN DATABASE <db_name> }
     | { schemaObjectPrivileges   | ALL [ PRIVILEGES ] } ON { <object_type> <object_name> | ALL <object_type_plural> IN SCHEMA <schema_name> }
     | { schemaObjectPrivileges   | ALL [ PRIVILEGES ] } ON FUTURE <object_type_plural> IN { DATABASE <db_name> | SCHEMA <schema_name> }
    }
  FROM [ ROLE ] <role_name> [ RESTRICT | CASCADE ]
```

Database roles:

Copy code

```
REVOKE [ GRANT OPTION FOR ]
    {
       { CREATE SCHEMA | MODIFY | MONITOR | USAGE } [ , ... ] } ON DATABASE <object_name>
       { globalPrivileges         | ALL [ PRIVILEGES ] } ON ACCOUNT
     | { accountObjectPrivileges  | ALL [ PRIVILEGES ] } ON { RESOURCE MONITOR | WAREHOUSE | COMPUTE POOL | DATABASE | INTEGRATION | EXTERNAL VOLUME } <object_name>
     | { schemaPrivileges         | ALL [ PRIVILEGES ] } ON { SCHEMA <schema_name> | ALL SCHEMAS IN DATABASE <db_name> }
     | { schemaPrivileges         | ALL [ PRIVILEGES ] } ON { FUTURE SCHEMAS IN DATABASE <db_name> }
     | { schemaObjectPrivileges   | ALL [ PRIVILEGES ] } ON { <object_type> <object_name> | ALL <object_type_plural> IN SCHEMA <schema_name> }
     | { schemaObjectPrivileges   | ALL [ PRIVILEGES ] } ON FUTURE <object_type_plural> IN { DATABASE <db_name> | SCHEMA <schema_name> }
    }
  FROM DATABASE ROLE <database_role_name> [ RESTRICT | CASCADE ]
```

Where:

Copy code

```
globalPrivileges ::=
  {
      CREATE {
          ACCOUNT | APPLICATION | APPLICATION PACKAGE | COMPUTE POOL | LISTING
          | DATABASE | EXTERNAL VOLUME | FAILOVER GROUP | INTEGRATION | NETWORK POLICY
          | ORGANIZATION LISTING | ORGANIZATION PROFILE | PREVIEW APPLICATION
          | REPLICATION GROUP | ROLE | SHARE | USER | WAREHOUSE
       }
      | ATTACH POLICY | AUDIT | BIND SERVICE ENDPOINT
      | APPLY {
         { AGGREGATION | AUTHENTICATION | JOIN | MASKING | PACKAGES | PASSWORD
           | PROJECTION | ROW ACCESS | SESSION | STORAGE LIFECYCLE } POLICY
         | CONTACT
         | TAG }
      | EXECUTE { ALERT | DATA METRIC FUNCTION | MANAGED ALERT | MANAGED TASK | TASK }
      | IMPORT { SHARE | ORGANIZATION LISTING }
 | MANAGE { ACCOUNT SUPPORT CASES | APPLICATION SPECIFICATIONS | EVENT SHARING | GRANTS | LISTING AUTO FULFILLMENT | ORGANIZATION SUPPORT CASES | SHARE TARGET | USER SUPPORT CASES | VISIBILITY | WAREHOUSES }
      | MODIFY { LOG LEVEL | TRACE LEVEL | SESSION LOG LEVEL | SESSION TRACE LEVEL }
      | MONITOR { EXECUTION | SECURITY | USAGE }
      | OVERRIDE SHARE RESTRICTIONS | PURCHASE DATA EXCHANGE LISTING | RESOLVE ALL
      | READ SESSION
      | READ UNREDACTED ERROR TABLE
      | USE AI FUNCTION <name>
      | USE AI FUNCTIONS
  }
  [ , ... ]
```

Copy code

```
accountObjectPrivileges ::=
-- For APPLICATION PACKAGE
    { ATTACH LISTING | DEVELOP | INSTALL | MANAGE VERSIONS | MANAGE RELEASES } [ , ... ]
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
-- For ORGANIZATION PROFILE
   { MODIFY } [ , ... ]
-- For REPLICATION GROUP
   { MODIFY | MONITOR | REPLICATE } [ , ... ]
-- For RESOURCE MONITOR
   { MODIFY | MONITOR } [ , ... ]
-- For USER
   { IMPERSONATE | MODIFY PROGRAMMATIC AUTHENTICATION METHODS | MONITOR } [ , ... ]
-- For WAREHOUSE
   { APPLYBUDGET | MODIFY | MONITOR | USAGE | OPERATE } [ , ... ]
```

Copy code

```
schemaPrivileges ::=

    ADD SEARCH OPTIMIZATION | APPLYBUDGET
  | CREATE {
       AGENT | ALERT | APPLICATION SERVICE | ARTIFACT REPOSITORY | CONTACT | CORTEX SEARCH SERVICE | DATA METRIC FUNCTION | DATASET
      | DBT PROJECT | EVENT TABLE | EXPERIMENT | FILE FORMAT | FUNCTION
      | GATEWAY | { GIT | IMAGE } REPOSITORY | MCP SERVER
      | MODEL | NETWORK RULE | NOTEBOOK | PIPE | PROCEDURE
      | { AGGREGATION | AUTHENTICATION | MASKING | PACKAGES
         | PASSWORD | PRIVACY | PROJECTION | ROW ACCESS | SESSION
         | STORAGE LIFECYCLE } POLICY
      | SECRET | SEQUENCE | SERVICE | SNAPSHOT | SNAPSHOT POLICY | SNAPSHOT SET
      | STAGE | STREAM | STREAMLIT
      | SNOWFLAKE.CORE.BUDGET
      | SNOWFLAKE.DATA_PRIVACY.CLASSIFICATION_PROFILE
      | SNOWFLAKE.DATA_PRIVACY.CUSTOM_CLASSIFIER
      | SNOWFLAKE.ML.ANOMALY_DETECTION | SNOWFLAKE.ML.CLASSIFICATION
         | SNOWFLAKE.ML.FORECAST | SNOWFLAKE.ML.TOP_INSIGHTS
      | SNOWFLAKE.ML.DOCUMENT_INTELLIGENCE
      | [ { DYNAMIC | EXTERNAL | HYBRID | ICEBERG | INTERACTIVE | ONLINE FEATURE } ] TABLE
      | TAG | TASK | TYPE | WORKSPACE | [ { MATERIALIZED | SEMANTIC } ] VIEW
      }
   | MODIFY | MONITOR | USAGE
   [ , ... ]
```

Copy code

```
schemaObjectPrivileges ::=
  -- For AGENT
     { MODIFY | MONITOR | USAGE } [ , ... ]
  -- For ALERT
     { MONITOR | OPERATE } [ , ... ]
  -- For APPLICATION SERVICE
     { MONITOR | OPERATE | USAGE } [ , ... ]
  -- For ARTIFACT REPOSITORY
     READ [ , ... ]
  -- For CONTACT
     { APPLY | MODIFY } [ , ... ]
  -- For CORTEX SEARCH SERVICE
     { OPERATE | USAGE } [ , ... ]
  -- For DATA METRIC FUNCTION
     USAGE [ , ... ]
  -- For DATASET, FILE FORMAT, FUNCTION (UDF or external function), MODEL, PROCEDURE, SECRET, SEQUENCE, SNAPSHOT, or TYPE
     USAGE [ , ... ]
  -- For SNAPSHOT POLICY or SNAPSHOT SET (for WORM snapshots)
     USAGE [ , ... ]
  -- For DBT PROJECT
     USAGE, MONITOR [ , ... ]
  -- For DYNAMIC TABLE
     MONITOR, OPERATE, SELECT [ , ... ]
  -- For EXPERIMENT
     { CREATE | MODIFY | USAGE } [ , ... ]
  -- For EVENT TABLE
     { APPLYBUDGET | DELETE | OWNERSHIP | REFERENCES | SELECT | TRUNCATE } [ , ... ]
  -- For GATEWAY
     { CREATE | MODIFY | USAGE } [ , ... ]
  -- For GIT REPOSITORY
     { READ, WRITE } [ , ... ]
  -- For HYBRID TABLE
     { APPLYBUDGET | DELETE | INSERT | REFERENCES | SELECT | TRUNCATE | UPDATE } [ , ... ]
  -- For IMAGE REPOSITORY
     { READ, WRITE } [ , ... ]
  -- For ICEBERG TABLE
     { APPLYBUDGET | DELETE | INSERT | REFERENCES | SELECT | TRUNCATE | UPDATE } [ , ... ]
  -- For INTERACTIVE TABLE
     { REFERENCES | SELECT } [ , ... ]
  -- For MATERIALIZED VIEW
     { APPLYBUDGET | REFERENCES | SELECT } [ , ... ]
 -- For MCP SERVER
     { MODIFY | USAGE } [ , ... ]
  -- For ONLINE FEATURE TABLE
     { MONITOR | SELECT } [ , ... ]
  -- For PIPE
     { APPLYBUDGET | MONITOR | OPERATE } [ , ... ]
  -- For { AGGREGATION | AUTHENTICATION | MASKING | JOIN | PACKAGES | PASSWORD | PRIVACY | PROJECTION | ROW ACCESS | SESSION | STORAGE LIFECYCLE } POLICY or TAG
     APPLY [ , ... ]
  -- For SECRET
     { READ | USAGE } [ , ... ]
  -- For SEMANTIC VIEW
     { SELECT | REFERENCES | MONITOR } [ , ... ]
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
  -- For WORKSPACE
     { READ | WRITE } [ , ... ]
```

For more details about the privileges supported for each object type, see [Access control privileges](/user-guide/security-access-control-privileges).

## Required parameters

`object_name`
:   Specifies the identifier for the object on which the privileges are revoked.

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
:   Plural form of `object_type` (for example, `TABLES`, `VIEWS`).

`role_name`
:   Specifies the identifier for the recipient role (that is, the role from which the privileges are revoked).

`database_role_name`
:   Specifies the identifier for the recipient database role (that is, the role from which the privileges are revoked). If the identifier is not
    fully qualified (in the form of `db_name.database_role_name`), the command looks for the database role in the current database
    for the session.

## Optional parameters

`GRANT OPTION FOR`
:   If specified, removes the ability for the recipient role to grant the privileges to another role.

    Default: No value

`ON FUTURE`
:   If specified, only removes privileges granted on new (that is, future) schema objects of a specified type (such as tables or views) rather than
    existing objects. Note that any privileges granted on existing objects are retained.

`RESTRICT | CASCADE`
:   If specified, determines whether the revoke operation succeeds or fails for the privileges, based on the whether the privileges had been
    re-granted to another role.

    - `RESTRICT`: If the privilege being revoked has been re-granted to another role, the REVOKE command fails.
    - `CASCADE`: If the privilege being revoked has been re-granted, the REVOKE command recursively revokes these dependent grants.
      If the same privilege on an object has been granted to the target role by a different grantor (parallel grant), that grant is not
      affected and the target role retains the privilege.

    Default: `RESTRICT`

## Security requirements

Revoking privileges on individual objects:
:   An [active role](/user-guide/security-access-control-overview#label-access-control-overview-active-roles) that meets either of the following criteria, or a
    [higher role](/user-guide/security-access-control-overview#label-role-hierarchy-and-privilege-inheritance), can be used to revoke privileges on an object from other roles:

    - The role is identified as the *grantor* of the privilege in the GRANTED\_BY column in the [SHOW GRANTS](/sql-reference/sql/show-grants) output.

      If multiple instances of a privilege have been granted on the specified object, only the instances granted by the active grantor role
      are revoked.
    - The role has the global MANAGE GRANTS privilege.

      If multiple instances of a privilege have been granted on the specified object, all instances are revoked.

      Note that only the SECURITYADMIN system role and higher have the MANAGE GRANTS privilege by default; however, the privilege can be
      granted to custom roles.

    In managed access schemas (that is, schemas created using the CREATE SCHEMA … WITH MANAGED ACCESS syntax), only the schema owner (that is, the
    role with the OWNERSHIP privilege on the schema) or a role with the global MANAGE GRANTS privilege, or a higher role, can revoke
    privileges on objects in the schema.

Revoking grants on future objects of a specified type:
:   **Database level**

    The global MANAGE GRANTS privilege is required to revoke privileges on future objects in a database. Only the SECURITYADMIN system role
    and higher have the MANAGE GRANTS privilege; however, the privilege can be granted to custom roles.

    **Schema level**

    In managed access schemas (that is, schemas created using the CREATE SCHEMA … WITH MANAGED ACCESS syntax),
    either the schema owner (that is, the role with the OWNERSHIP privilege on the schema) or a role with the
    global MANAGE GRANTS privilege can revoke privileges on future objects in the schema.

    In standard schemas, the global MANAGE GRANTS privilege is required to revoke privileges on future objects
    in the schema.

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
- Privileges granted to a particular role are automatically inherited by any other roles to which the role is granted, as well as any
  other higher-level roles within the role hierarchy. For more details, see [Overview of Access Control](/user-guide/security-access-control-overview).
- For databases, the IMPORTED PRIVILEGES privilege only applies to shared databases (that is, databases created from a share). For more
  details, see [Consume imported data](/user-guide/data-share-consumers).
- For schemas and objects in schemas, an option is provided to grant privileges on all objects of the same type within the container
  (that is, a database or schema). This is a convenience option; internally, the command is expanded into a series of individual GRANT commands
  on each object. Only objects that currently exist within the container are affected.

  However, note that, in the Snowflake model, bulk granting of privileges is not a recommended practice. Instead, Snowflake recommends
  creating a shared role and using the role to create objects that are automatically accessible to all users who have been granted the
  role.
- For stages:

  - USAGE only applies to external stages.
  - READ | WRITE only applies to internal stages. In addition, to grant the WRITE privilege on an internal stage, the READ privilege
    must first be granted on the stage.

  For more details about external and internal stages, see [CREATE STAGE](/sql-reference/sql/create-stage).
- For storage integrations:

  - To run the following commands using an external stage that relies on a storage integration,
    you must use a role that has or inherits the USAGE privilege on the storage integration.

    - [LIST](/sql-reference/sql/list)
    - [REMOVE](/sql-reference/sql/remove)
    - [COPY INTO <table>](/sql-reference/sql/copy-into-table)
    - [COPY INTO <location>](/sql-reference/sql/copy-into-location)

    If you revoke the USAGE privilege from the role, the role
    can’t run these commands. For more information, see [Stage privileges](/user-guide/security-access-control-privileges#label-access-control-privileges-stage).
  - Revoking the USAGE privilege on a storage integration does not block a role from querying external tables associated with the storage
    integration. Querying an external table does not require the USAGE privilege on its underlying storage integration.
- When granting privileges on an individual UDF, you must specify the data types for the arguments, if any, for the UDF in the form of
  `udf_name ( [ arg_data_type , ... ] )`. This is required because Snowflake uses argument data types to resolve UDFs that
  have the same name within a schema. For an example, see [Examples](#examples) (in this topic). For more details, see
  [User-defined functions overview](/developer-guide/udf/udf-overview).
- When granting privileges on an individual stored procedure, you must specify the data types for the arguments, if any, for the
  procedure in the form of `procedure_name ( [ arg_data_type , ... ] )`. This is required because Snowflake uses argument
  data types to resolve stored procedures that have the same name within a schema.
- OWNERSHIP is a valid privilege across all object types that support future grants.
- **Future grants:** Revoking future grants only drops grants of privileges for future objects of a specified type. Any
  privileges granted on existing objects are retained.

  For more information, see [managed access schemas](/user-guide/security-access-control-configure#label-managed-access-schemas).
- To revoke the privilege to create hybrid tables, revoke `CREATE HYBRID TABLE` on the schema.
- To revoke privileges on interactive tables, use the standard TABLE or TABLES keyword. You cannot specify INTERACTIVE TABLE or INTERACTIVE TABLES.

## Examples

### Roles

Revoke the privilege to create a warehouse in the account from the `analyst` role:

Copy code

```
REVOKE CREATE WAREHOUSE ON ACCOUNT FROM ROLE analyst;
```

Revoke the necessary privileges to operate (that is, suspend or resume) the `report_wh` warehouse
from the `analyst` role:

Copy code

```
REVOKE OPERATE ON WAREHOUSE report_wh FROM ROLE analyst;
```

Revoke only the GRANT OPTION privilege for the OPERATE privilege on the `report_wh` warehouse from the
`analyst` role. The role retains the OPERATE privilege but can no longer grant the OPERATE privilege
on the warehouse to other roles:

Copy code

```
REVOKE GRANT OPTION FOR OPERATE ON WAREHOUSE report_wh FROM ROLE analyst;
```

Revoke the SELECT privilege on all existing tables in the `mydb.myschema` schema from the `analyst` role:

Copy code

```
REVOKE SELECT ON ALL TABLES IN SCHEMA mydb.myschema from ROLE analyst;
```

Revoke all privileges on two UDFs (with the same name in the current schema) from the `analyst` role:

Copy code

```
REVOKE ALL PRIVILEGES ON FUNCTION add5(number) FROM ROLE analyst;

REVOKE ALL PRIVILEGES ON FUNCTION add5(string) FROM ROLE analyst;
```

Note that the UDFs have different arguments, which is how Snowflake uniquely identifies UDFs with the same name.
For more details about UDF naming, see [User-defined functions overview](/developer-guide/udf/udf-overview).

Revoke all privileges on two stored procedures (with the same name in the current schema) from the `analyst` role:

Copy code

```
REVOKE ALL PRIVILEGES ON PROCEDURE clean_schema(string) FROM ROLE analyst;

REVOKE ALL PRIVILEGES ON procedure clean_schema(string, string) FROM ROLE analyst;
```

Note that the two stored procedures have different arguments, which is how Snowflake uniquely identifies procedures
with the same name.

Revoke the SELECT and INSERT privileges granted on all future tables created in the `mydb.myschema` schema from the
`role1` role:

Copy code

```
REVOKE SELECT, INSERT ON FUTURE TABLES IN SCHEMA mydb.myschema
  FROM ROLE role1;
```

Revoke the USAGE privilege on a notebook called `mynotebook` from the `finance` role:

> Copy code
>
> ```
> REVOKE USAGE ON NOTEBOOK db_one.schema_one.mynotebook FROM ROLE finance;
> ```

### Database roles

Revoke the SELECT privilege on all existing tables in the `mydb.myschema` schema from the `mydb.dr1` database role:

Copy code

```
REVOKE SELECT ON ALL TABLES IN SCHEMA mydb.myschema
  FROM DATABASE ROLE mydb.dr1;
```

Revoke all privileges on two UDFs (with the same name in the current schema) from the `mydb.dr1` database role:

Copy code

```
REVOKE ALL PRIVILEGES ON FUNCTION add5(number)
  FROM DATABASE ROLE mydb.dr1;

REVOKE ALL PRIVILEGES ON FUNCTION add5(string)
  FROM DATABASE ROLE mydb.dr1;
```

Note that the UDFs have different arguments, which is how Snowflake uniquely identifies UDFs with the same name.
For more details about UDF naming, see [User-defined functions overview](/developer-guide/udf/udf-overview).

Revoke all privileges on two stored procedures (with the same name in the current schema) from the
`mydb.dr1` database role:

Copy code

```
REVOKE ALL PRIVILEGES ON PROCEDURE clean_schema(string)
  FROM DATABASE ROLE mydb.dr1;

REVOKE ALL PRIVILEGES ON procedure clean_schema(string, string)
  FROM DATABASE ROLE mydb.dr1;
```

Note that the two stored procedures have different arguments, which is how Snowflake uniquely identifies procedures
with the same name.

Revoke the SELECT and INSERT privileges granted on all future tables created in the `mydb.myschema` schema
from the `mydb.dr1` database role:

Copy code

```
REVOKE SELECT,INSERT ON FUTURE TABLES IN SCHEMA mydb.myschema
  FROM DATABASE ROLE mydb.dr1;
```

Revoke the USAGE privilege on a notebook from the `mydb.dr1` database role:

Copy code

```
REVOKE USAGE ON NOTEBOOK db_one.schema_one.mynotebook
  FROM DATABASE ROLE mydb.dr1;
```
