# REVOKE *<privileges>* … FROM USER

Removes one or more privileges on a securable object from a user. The privileges that can be revoked are object-specific.

See also:

> [GRANT <privileges> … TO USER](/sql-reference/sql/grant-privilege-user)

## Syntax

Copy code

```
REVOKE [ GRANT OPTION FOR ]
    {
       { globalPrivileges         | ALL [ PRIVILEGES ] } ON ACCOUNT
     | { accountObjectPrivileges  | ALL [ PRIVILEGES ] } ON { RESOURCE MONITOR | WAREHOUSE | COMPUTE POOL | DATABASE | INTEGRATION | CONNECTION | FAILOVER GROUP | REPLICATION GROUP | EXTERNAL VOLUME } <object_name>
     | { schemaPrivileges         | ALL [ PRIVILEGES ] } ON { SCHEMA <schema_name> | ALL SCHEMAS IN DATABASE <db_name> }
     | { schemaObjectPrivileges   | ALL [ PRIVILEGES ] } ON { <object_type> <object_name> | ALL <object_type_plural> IN SCHEMA <schema_name> }
    }
  FROM [ USER ] <user_name> [ RESTRICT | CASCADE ]
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
:   Specifies the identifier for the object on which the privileges are revoked.

`object_type`
:   Specifies the type of object for schema-level objects.

    - `AGENT`
    - `AGGREGATION POLICY`
    - `ALERT`
    - `AUTHENTICATION POLICY`
    - `CORTEX EXTENSION`
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
    - `ICEBERG TABLE`
    - `IMAGE REPOSITORY`
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
    - `SEQUENCE`
    - `SERVICE`
    - `SESSION POLICY`
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

`user_name`
:   Specifies the identifier for the recipient user (the user from which the privileges are revoked).

## Optional parameters

`GRANT OPTION FOR`
:   If specified, removes the ability for the recipient user to grant the privileges to another role or user.

    Default: No value

`RESTRICT | CASCADE`
:   If specified, determines whether the revoke operation succeeds or fails for the privileges, based on the whether the privileges had been
    re-granted to another role or user.

    - `RESTRICT`: If the privilege being revoked has been re-granted to another role or user, the REVOKE command fails.
    - `CASCADE`: If the privilege being revoked has been re-granted, the REVOKE command recursively revokes these dependent grants.
      If the same privilege on an object has been granted to the target user by a different grantor (parallel grant), that grant is not
      affected and the target user retains the privilege.

    Default: `RESTRICT`

## Usage notes

- Privileges cannot be granted or revoked directly on any class.

- A privilege can be granted to a user multiple times by different grantors. A `REVOKE privilege` statement only revokes grants for
  which the user is the grantor. Any additional grants of a specified privilege by other grantors are ignored.

  Also note that a `REVOKE privilege` statement is successful even if no privileges are revoked. `REVOKE privilege` only
  returns an error if a specified privilege has dependent grants and the CASCADE clause is omitted from the statement.
- Multiple privileges can be specified for the same object type in a single GRANT statement (with each privilege separated by commas),
  or the special `ALL [ PRIVILEGES ]` keyword can be used to grant all applicable privileges to the specified object type. Note,
  however, that only privileges held and grantable by the role or user executing the GRANT command are actually granted to the target user.
  A warning message is returned for any privileges that could not be granted.

  You cannot specify the `ALL [ PRIVILEGES ]` keyword for tags.

- For stages:

  - USAGE only applies to external stages.
  - READ | WRITE only applies to internal stages. In addition, to grant the WRITE privilege on an internal stage, the READ privilege
    must first be granted on the stage.

  For more information about external and internal stages, see [CREATE STAGE](/sql-reference/sql/create-stage).
- For storage integrations:

  - To run the following commands using an external stage that relies on a storage integration, the USAGE privilege on the storage
    integration must be directly granted to the user or use a role that has or inherits the privilege.

    - [LIST](/sql-reference/sql/list)
    - [REMOVE](/sql-reference/sql/remove)
    - [COPY INTO <table>](/sql-reference/sql/copy-into-table)
    - [COPY INTO <location>](/sql-reference/sql/copy-into-location)

    If you revoke the USAGE privilege from the user, the user cannot run these commands. For more information, see
    [Stage privileges](/user-guide/security-access-control-privileges#label-access-control-privileges-stage).
  - Revoking the USAGE privilege on a storage integration does not block a user from querying external tables associated with the
    storage integration. Querying an external table does not require the USAGE privilege on its underlying storage integration.

## Access control requirements

Revoking privileges on individual objects:
:   An [active role](/user-guide/security-access-control-overview#label-access-control-overview-active-roles) or user that meets either of the following criteria, or a
    [higher role](/user-guide/security-access-control-overview#label-role-hierarchy-and-privilege-inheritance), can be used to revoke privileges on an object from users:

    - The role or user is identified as the *grantor* of the privilege in the GRANTED\_BY column in the [SHOW GRANTS](/sql-reference/sql/show-grants)
      output.

      If multiple instances of a privilege have been granted on the specified object, only the instances granted by the active grantor role
      are revoked.
    - The role or user has the global MANAGE GRANTS privilege.

      If multiple instances of a privilege have been granted on the specified object, all instances are revoked.

      Note that only the SECURITYADMIN system role and higher have the MANAGE GRANTS privilege by default; however, the privilege can be
      granted to custom roles.

    In [managed access schemas](/user-guide/security-access-control-configure#label-managed-access-schemas) (schemas created using the `CREATE SCHEMA ... WITH MANAGED ACCESS`)
    syntax, only the schema owner (the role with the OWNERSHIP privilege on the schema), a role or user with the global MANAGE GRANTS
    privilege, or a higher role can revoke privileges on objects in the schema.

## Examples

To revoke the USAGE privilege on a Streamlit application from a specific user, `joe`:

Copy code

```
REVOKE USAGE ON STREAMLIT streamlit_db.streamlit_schema.streamlit_app FROM USER joe;
```

To revoke the USAGE privilege on a procedure from a specific user, `user1`:

Copy code

```
REVOKE USAGE ON PROCEDURE mydb.myschema.myprocedure(number) FROM USER user1;
```
