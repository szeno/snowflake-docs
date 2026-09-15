# GRANT *<privileges>* … TO ROLE

Grants one or more access privileges on a securable object to a role or database role. The privileges that can be granted are object-specific.

For information on granting privileges on securable objects to a share, see [GRANT <privilege> … TO SHARE](/sql-reference/sql/grant-privilege-share).

Roles:
:   The privileges that can be granted to roles are grouped into the following categories:

    - Global privileges.
    - Privileges for account objects, such as resource monitors, virtual warehouses, and databases.
    - Privileges for schemas.
    - Privileges for schema objects, such as tables, views, stages, file formats, UDFs, and sequences.

Database roles:
:   The privileges that can be granted to database roles are grouped into the following categories:

    - Privileges for the database that contains the database role.
    - Privileges for schemas in the database that contains the database role.
    - Privileges for schema objects, such as tables, views, stages, file formats, UDFs, and sequences in the database that contains the
      database role.

For more details about roles and securable objects, see [Overview of Access Control](/user-guide/security-access-control-overview).

Variations:
:   [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) , [GRANT <privilege> … TO SHARE](/sql-reference/sql/grant-privilege-share)

See also:
:   [REVOKE <privileges> … FROM ROLE](/sql-reference/sql/revoke-privilege)

## Syntax

Account roles:

Copy code

```
GRANT {  { globalPrivileges         | ALL [ PRIVILEGES ] } ON ACCOUNT
       | { accountObjectPrivileges  | ALL [ PRIVILEGES ] } ON { USER | RESOURCE MONITOR | WAREHOUSE | COMPUTE POOL | DATABASE | INTEGRATION | CONNECTION | FAILOVER GROUP | REPLICATION GROUP | EXTERNAL VOLUME | APPLICATION PACKAGE | APPLICATION } <object_name>
       | { schemaPrivileges         | ALL [ PRIVILEGES ] } ON { SCHEMA <schema_name> | ALL SCHEMAS IN DATABASE <db_name> }
       | { schemaPrivileges         | ALL [ PRIVILEGES ] } ON { FUTURE SCHEMAS IN DATABASE <db_name> }
       | { schemaObjectPrivileges   | ALL [ PRIVILEGES ] } ON { <object_type> <object_name> | ALL <object_type_plural> IN { DATABASE <db_name> | SCHEMA <schema_name> } }
       | { schemaObjectPrivileges   | ALL [ PRIVILEGES ] } ON FUTURE <object_type_plural> IN { DATABASE <db_name> | SCHEMA <schema_name> }
      }
  TO [ ROLE ] <role_name> [ WITH GRANT OPTION ]
```

Database roles:

Copy code

```
GRANT {  { CREATE SCHEMA | MODIFY | MONITOR | USAGE } [ , ... ] } ON DATABASE <object_name>
       | { schemaPrivileges         | ALL [ PRIVILEGES ] } ON { SCHEMA <schema_name> | ALL SCHEMAS IN DATABASE <db_name> }
       | { schemaPrivileges         | ALL [ PRIVILEGES ] } ON { FUTURE SCHEMAS IN DATABASE <db_name> }
       | { schemaObjectPrivileges   | ALL [ PRIVILEGES ] } ON { <object_type> <object_name> | ALL <object_type_plural> IN { DATABASE <db_name> | SCHEMA <schema_name> } }
       | { schemaObjectPrivileges   | ALL [ PRIVILEGES ] } ON FUTURE <object_type_plural> IN { DATABASE <db_name> | SCHEMA <schema_name> }
      }
  TO DATABASE ROLE <database_role_name> [ WITH GRANT OPTION ]
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
:   Plural form of `object_type` (for example, `TABLES`, `VIEWS`).

    Note that bulk grants on pipes are not allowed.

`role_name`
:   Specifies the identifier for the recipient role (that is, the role to which the privileges are granted).

`database_role_name`
:   Specifies the identifier for the recipient database role (that is, the role to which the privileges are granted). If the identifier is not
    fully qualified in the form of `db_name.database_role_name`, the command looks for the database role in the current database
    for the session.

    All privileges are limited to the database that contains the database role, as well as other objects in the same database.

## Optional parameters

`FUTURE`
:   Specifies that privileges are granted on new (that is, future) database or schema objects of a specified type (such as tables or views) rather
    than on existing objects. Note that future grants can be revoked at any time using [REVOKE <privileges> … FROM ROLE](/sql-reference/sql/revoke-privilege) with the
    ON FUTURE parameter; any privileges granted on existing objects are retained. For more information about future grants, see
    [Future grants on database or schema objects](#future-grants-on-database-or-schema-objects) in this topic.

`WITH GRANT OPTION`
:   If specified, allows the recipient role to grant the privileges to other roles.

    Default: No value, which means the recipient role cannot grant the privileges to other roles.

    Note

    The WITH GRANT OPTION parameter does not support the IMPORTED PRIVILEGES privilege. For more information, see
    [Granting privileges on an imported database](/user-guide/data-share-consumers#label-granting-privileges-on-shared-database).

## Usage notes

- Privileges cannot be granted or revoked directly on any class. You can, however, create an instance of a class and
  grant [instance roles](/sql-reference/snowflake-db-classes#label-instance-roles) to an account role. Grant the CREATE <class\_name> privilege on the schema to enable a
  role to create an instance of a class.
- OWNERSHIP is a valid privilege across all object types that support future grants.
- To grant the OWNERSHIP privilege on an object (or all objects of a specified type in a schema) to a role, transferring ownership of the
  object from one role to another role, use [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) instead. The GRANT OWNERSHIP command has a different
  syntax.
- Multiple privileges can be specified for the same object type in a single GRANT statement (with each privilege separated by commas), or
  the special `ALL [ PRIVILEGES ]` keyword can be used to grant all applicable privileges to the specified object type. Note,
  however, that only privileges held and grantable by the role executing the GRANT command are actually granted to the target role. A
  warning message is returned for any privileges that could not be granted.

  - You cannot specify this keyword for tags.
  - This keyword does not grant privileges on a class if you try to grant `ALL` privileges on a schema. To allow a role to create
    instances of a particular class, grant the CREATE privilege directly as shown in the [Classes](#label-grant-privilege-create-class) example.
- Privileges granted to a particular role are automatically inherited by any other roles to which the role is granted, as well as any other
  higher-level roles within the role hierarchy. For more details, see [Overview of Access Control](/user-guide/security-access-control-overview).
- For databases, the IMPORTED PRIVILEGES privilege only applies to shared databases (that is, databases created from a share). For more details,
  see [Consume imported data](/user-guide/data-share-consumers). Note that the IMPORTED PRIVILEGES privilege cannot be granted to a database role.
- For schemas and objects in schemas, an `ALL object_type_plural in container` option is provided to grant privileges on all
  objects of the same type within the container (that is, a database or schema). This is a convenience option; internally, the command is expanded
  into a series of individual GRANT commands on each object. Only objects that currently exist within the container are affected.

  However, note that, in the Snowflake model, bulk granting of privileges is not a recommended practice. Instead, Snowflake recommends
  creating a shared role and using the role to create objects that are automatically accessible to all users who have been granted the role.

  You cannot specify ALL TAGS or ALL MASKING POLICIES.
- In managed access schemas:

  - The OWNERSHIP privilege on objects can only be transferred to a subordinate role of the schema owner.
- For stages:

  - USAGE only applies to external stages.
  - READ | WRITE only applies to internal stages. In addition, to grant the WRITE privilege on an internal stage, the READ privilege must
    first be granted on the stage.

  For more details about external and internal stages, see [CREATE STAGE](/sql-reference/sql/create-stage).
- When granting privileges on an individual UDF or stored procedure, you must specify the data types of the arguments, if any,
  using the following syntax:

  Copy code

  ```
  <udf_or_stored_procedure_name> ( [ <arg_data_type> [ , ... ] ] )
  ```

  Snowflake uses argument data types to resolve UDFs or stored procedures that have the same name within a schema. For more
  information, see [Overloading procedures and functions](/developer-guide/udf-stored-procedure-naming-conventions#label-procedure-function-name-overloading).
- For dynamic tables, the receiving role must be granted the USAGE privilege on the database and schema that contains the dynamic table, and
  on the warehouse used to refresh the table. For more information, see [Dynamic table access control](/user-guide/dynamic-tables/privileges).
- To grant the privilege to create hybrid tables, grant `CREATE HYBRID TABLE` on the schema. The `CREATE TABLE` privilege isn’t sufficient.
- For artifact repositories, future grants are supported. For example:

  Copy code

  ```
  GRANT READ ON FUTURE ARTIFACT REPOSITORIES IN SCHEMA mydb.myschema TO ROLE myrole;
  ```

  There is no separately grantable `WRITE` privilege on artifact repositories. Publishing new package versions requires `OWNERSHIP`. For a full list of privileges, see [Artifact repository privileges](/user-guide/security-access-control-privileges#label-artifact-repository-privileges).
- For Application Services, any privilege on the object (`USAGE`, `OPERATE`, `MONITOR`, or `OWNERSHIP`) allows `DESCRIBE`. The
  `USAGE`, `OPERATE`, and `MONITOR` privileges can be granted on all or future Application Services in a schema. For example:

  Copy code

  ```
  GRANT USAGE ON FUTURE APPLICATION SERVICES IN SCHEMA mydb.myschema TO ROLE myrole;
  ```

  `OWNERSHIP` cannot be transferred on an Application Service, and privileges cannot be granted on an Application Service in a
  [personal database](/user-guide/personal-databases). For a full list of privileges, see
  [Application Service privileges](/user-guide/security-access-control-privileges#label-application-service-privileges). For grant patterns, see
  [Access control for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/access-control).

## Access control requirements

Granting privileges on individual objects:
:   In general, a role with any one of the following sets of privileges can grant privileges on an object to other roles:

    - The global MANAGE GRANTS privilege.

      Only the SECURITYADMIN and ACCOUNTADMIN system roles have the MANAGE GRANTS privilege; however, the privilege can be granted
      to custom roles.
    - The OWNERSHIP privilege on the object. When granting privileges on schema objects (e.g. tables and views), the role must
      also have USAGE or any other privilege on the parent database and schema.
    - If a privilege was granted to a role with the WITH GRANT OPTION parameter included in the
      GRANT *<privileges>* … TO ROLE statement, the role can grant the same privilege to other roles.

    In managed access schemas (that is, schemas created using the CREATE SCHEMA … WITH MANAGED ACCESS syntax), object owners lose
    the ability to make grant decisions. Only the schema owner (that is, the role with the OWNERSHIP privilege on the schema) or a
    role with the global MANAGE GRANTS privilege can grant privileges on objects in the schema.

    Note that a role that holds the global MANAGE GRANTS privilege can grant additional privileges to the current (grantor) role.

Defining grants on future objects of a specified type:
:   **Database level**

    The global MANAGE GRANTS privilege is required to grant privileges on future objects in a database. Only the SECURITYADMIN and
    ACCOUNTADMIN system roles have the MANAGE GRANTS privilege; however, the privilege can be granted to custom roles.

    **Schema level**

    In managed access schemas (that is, schemas created using the CREATE SCHEMA … WITH MANAGED ACCESS syntax), either the schema owner
    (that is, the role with the OWNERSHIP privilege on the schema) or a role with the global MANAGE GRANTS privilege can grant privileges
    on future objects in the schema.

    In standard schemas, the global MANAGE GRANTS privilege is required to grant privileges on future objects in the schema.

    **Database roles**

    To grant future privileges to a database role, a role with the global MANAGE GRANTS privilege, such as SECURITYADMIN, also
    requires the USAGE privilege on the database that contains the database role.

For more information about defining grants on future objects of a specified type, see
[Future grants on database or schema objects](#future-grants-on-database-or-schema-objects) (in this topic).

## Future grants on database or schema objects

The notes in this section apply when assigning future grants on objects in a schema or a database; that is, when using the ON FUTURE parameter.

For more information, see [managed access schemas](/user-guide/security-access-control-configure#label-managed-access-schemas).

### Considerations

- When future grants are defined on the same object type for a database and a schema in the same database, the schema-level
  grants take precedence over the database level grants, and the database level grants are ignored. This behavior applies to privileges
  on future objects granted to one role or different roles.

  For example, the following statements grant different privileges on objects of the same type at the database and schema levels.

  Grant the SELECT privilege on all future tables in database `d1` to role `r1`. This grant gives access to all future tables in all
  schemas in `d1`:

  Copy code

  ```
  GRANT SELECT ON FUTURE TABLES IN DATABASE d1 TO ROLE r1;
  ```

  Grant the INSERT and DELETE privileges on all future tables only in the `d1.s1` schema to role `r2`.

  Copy code

  ```
  GRANT INSERT, DELETE ON FUTURE TABLES IN SCHEMA d1.s1 TO ROLE r2;
  ```

  The future grants assigned to the `r1` role are ignored completely. When new tables are created in schema `d1.s1`, only the
  future privileges defined on tables for the `r2` role are granted.
- Database-level future grants apply to both regular and
  [managed access schemas](/user-guide/security-access-control-configure#label-managed-access-schemas).

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

  - A future grant of the OWNERSHIP privilege on objects can only be applied to a subordinate role of the schema owner (that is, the role
    that has the OWNERSHIP privilege on the schema).
  - Before ownership of a managed access schema can be transferred to a different role, all open future grants of the OWNERSHIP
    privilege must be revoked using [REVOKE <privileges> … FROM ROLE](/sql-reference/sql/revoke-privilege) with the ON FUTURE parameter.
- Future grants are not applied when renaming or swapping a table.
- Future grants are supported on named stages with the following restrictions:

  - The WRITE privilege cannot be specified without the READ privilege.
  - The READ privilege cannot be revoked if the WRITE privilege is present.
  - For internal stages, only future grants with the READ or WRITE privilege are materialized.
  - For external stages, only future grants with the USAGE privileges are materialized.

## Examples

### Roles

Grant the necessary privileges to operate (that is, suspend or resume) the `report_wh` warehouse to the `analyst` role:

> Copy code
>
> ```
> GRANT OPERATE ON WAREHOUSE report_wh TO ROLE analyst;
> ```

Repeat the previous example, but also allow the `analyst` role to grant the privilege to other roles:

> Copy code
>
> ```
> GRANT OPERATE ON WAREHOUSE report_wh TO ROLE analyst WITH GRANT OPTION;
> ```

Grant the SELECT privilege on all existing tables in the `mydb.myschema` schema to the `analyst` role:

> Copy code
>
> ```
> GRANT SELECT ON ALL TABLES IN SCHEMA mydb.myschema to ROLE analyst;
> ```

Grant all privileges on two UDFs in the `mydb.myschema` schema to the `analyst` role:

> Copy code
>
> ```
> GRANT ALL PRIVILEGES ON FUNCTION mydb.myschema.add5(number) TO ROLE analyst;
>
> GRANT ALL PRIVILEGES ON FUNCTION mydb.myschema.add5(string) TO ROLE analyst;
> ```
>
> Note
>
> The UDFs have different arguments, which is how Snowflake uniquely identifies UDFs with the same name. For more details about
> UDF naming, see [User-defined functions overview](/developer-guide/udf/udf-overview).

Grant USAGE privilege on a stored procedure in the `mydb.myschema` schema to the `analyst` role:

> Copy code
>
> ```
> GRANT USAGE ON PROCEDURE mydb.myschema.myprocedure(number) TO ROLE analyst;
> ```
>
> Note
>
> Stored procedure names (like UDF names) can be overloaded, so you must specify the data type of the arguments(s). For more details about
> name overloading, see [Overloading procedures and functions](/developer-guide/udf-stored-procedure-naming-conventions#label-procedure-function-name-overloading).

Grant the WRITE privilege on a shared workspace in the `mydb.myschema` schema to the `analyst` role:

> Copy code
>
> ```
> GRANT WRITE ON WORKSPACE mydb.myschema.my_workspace TO ROLE analyst;
> ```

Grant the CREATE PROVISIONED THROUGHPUT privilege to a role:

> Copy code
>
> ```
> GRANT CREATE PROVISIONED THROUGHPUT ON ACCOUNT TO ROLE myrole;
> ```

Grant the privilege to create hybrid tables in the specified schema:

> Copy code
>
> ```
> GRANT CREATE HYBRID TABLE ON SCHEMA mydb.myschema TO ROLE myrole;
> ```

Grant the privilege to create materialized views in the specified schema:

> Copy code
>
> ```
> GRANT CREATE MATERIALIZED VIEW ON SCHEMA mydb.myschema TO ROLE myrole;
> ```

Grant the SELECT and INSERT privileges on all future tables created in the `mydb.myschema` schema to the `role1` role:

> Copy code
>
> ```
> GRANT SELECT, INSERT ON FUTURE TABLES IN SCHEMA mydb.myschema TO ROLE role1;
> ```

Grant the USAGE privilege on all future schemas in the `mydb` database to the `role1` role:

> Copy code
>
> ```
> USE ROLE ACCOUNTADMIN;
>
> GRANT USAGE ON FUTURE SCHEMAS IN DATABASE mydb TO ROLE role1;
> ```

Grant ALL PRIVILEGES on all tables in a given schema to a given role. Note that this grant applies to both standard tables and hybrid tables
in the specified schema:

> Copy code
>
> ```
> GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA ht_schema TO ROLE ht_role;
> ```

### Database roles

Create a database role `dr1` in the `mydb.myschema` schema:

> Copy code
>
> ```
> CREATE DATABASE ROLE mydb.myschema.dr1;
> ```

Grant the SELECT privilege on all existing tables in the `mydb.myschema` schema to the `mydb.dr1` database role:

> Copy code
>
> ```
> GRANT SELECT ON ALL TABLES IN SCHEMA mydb.myschema
>   TO DATABASE ROLE mydb.dr1;
> ```

Grant all privileges on two UDFs in the `mydb.myschema` schema to the `mydb.dr1` database role:

> Copy code
>
> ```
> GRANT ALL PRIVILEGES ON FUNCTION mydb.myschema.add5(number)
>   TO DATABASE ROLE mydb.dr1;
>
> GRANT ALL PRIVILEGES ON FUNCTION mydb.myschema.add5(string)
>   TO DATABASE ROLE mydb.dr1;
> ```
>
> Note
>
> The UDFs have different arguments, which is how Snowflake uniquely identifies UDFs with the same name. For more details about UDF naming,
> see [User-defined functions overview](/developer-guide/udf/udf-overview).

Grant usage privilege on a stored procedure in the `mydb.myschema` schema to the `mydb.dr1` database role:

> Copy code
>
> ```
> GRANT USAGE ON PROCEDURE mydb.myschema.myprocedure(number)
>   TO DATABASE ROLE mydb.dr1;
> ```
>
> Note
>
> Stored procedure names (like UDF names) can be overloaded, so you must specify the data type of the arguments(s). For more
> details about overloading stored procedures, see [Overloading procedures and functions](/developer-guide/udf-stored-procedure-naming-conventions#label-procedure-function-name-overloading).

Grant the privilege to create materialized views in the specified schema to the `mydb.dr1` database role:

> Copy code
>
> ```
> GRANT CREATE MATERIALIZED VIEW ON SCHEMA mydb.myschema
>   TO DATABASE ROLE mydb.dr1;
> ```

Grant the SELECT and INSERT privileges on all future tables created in the `mydb.myschema` schema to the `mydb.dr1` database role:

> Copy code
>
> ```
> GRANT SELECT,INSERT ON FUTURE TABLES IN SCHEMA mydb.myschema
>   TO DATABASE ROLE mydb.dr1;
> ```

Grant the USAGE privilege on all future schemas in the `mydb` database to the `dr1` role:

> Copy code
>
> ```
> USE ROLE ACCOUNTADMIN;
>
> GRANT USAGE ON FUTURE SCHEMAS IN DATABASE mydb
>   TO DATABASE ROLE mydb.dr1;
> ```

Grant future privileges to the database role `mydb.dr1` using the SECURITYADMIN role:

> Copy code
>
> ```
> USE ROLE ACCOUNTADMIN;
>
> GRANT USAGE ON DATABASE mydb TO ROLE SECURITYADMIN;
>
> USE ROLE SECURITYADMIN;
>
> GRANT SELECT, INSERT ON FUTURE TABLES IN SCHEMA mydb.myschema
>   TO DATABASE ROLE mydb.dr1;
> ```
>
> Note
>
> The SECURITYADMIN role requires the USAGE privilege on a database that contains a database role in order to grant future privileges
> to that database role.

Show that a user `testuser`, with role `public` and granted database role `dr1` , can select and insert to a new table in `mydb.myschema`:

> Copy code
>
> ```
> USE ROLE ACCOUNTADMIN;
> CREATE USER testuser DEFAULT_ROLE=public DEFAULT_SECONDARY_ROLES=all;
> CREATE TABLE mydb.myschema.test_table (id INT, name VARCHAR(100));
>
> USE ROLE SECURITYADMIN;
> GRANT DATABASE ROLE mydb.dr1 TO USER testuser;
> ```

When logged in as `testuser`:

> Copy code
>
> ```
> INSERT INTO mydb.myschema.test_table (id, name)
>   VALUES (1, 'Test Record');
>
> SELECT * FROM mydb.myschema.test_table;
> ```

Expected output:

> ```
> -- +----+-------------+
> -- | ID | NAME        |
> -- +----+-------------+
> -- | 1  | Test Record |
> -- +----+-------------+
> ```

### Classes

To allow an account role to create budgets in a schema, grant the CREATE SNOWFLAKE.CORE.BUDGET privilege on the schema to the role:

> Copy code
>
> ```
> USE ROLE ACCOUNTADMIN;
>
> GRANT CREATE SNOWFLAKE.CORE.BUDGET ON SCHEMA budgets_db.budgets_schema
>   TO ROLE budget_admin;
> ```

To allow an account role to create an ML Function model or instance (forecast, anomaly detection, or classification) in a schema,
grant the appropriate privilege on the schema to the role. The following privileges are available.

- CREATE SNOWFLAKE.ML.ANOMALY\_DETECTION
- CREATE SNOWFLAKE.ML.CLASSIFICATION
- CREATE SNOWFLAKE.ML.FORECAST
- CREATE SNOWFLAKE.ML.TOP\_INSIGHTS
