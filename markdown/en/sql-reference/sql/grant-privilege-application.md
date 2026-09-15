# GRANT *<privileges>* … TO APPLICATION

Grants one or more access privileges on a securable object to an application. The privileges that can be
granted are object-specific.

Variations:
:   [REVOKE <privileges> … FROM APPLICATION](/sql-reference/sql/revoke-privilege-application)

## Syntax

Copy code

```
GRANT {  { globalPrivileges } ON ACCOUNT
       | { accountObjectPrivileges  | ALL [ PRIVILEGES ] } ON { USER | RESOURCE MONITOR | WAREHOUSE | COMPUTE POOL | DATABASE | INTEGRATION | CONNECTION | FAILOVER GROUP | REPLICATION GROUP | EXTERNAL VOLUME | APPLICATION PACKAGE | APPLICATION } <object_name>
       | { schemaPrivileges         | ALL [ PRIVILEGES ] } ON { SCHEMA <schema_name> | ALL SCHEMAS IN DATABASE <db_name> }
       | { schemaObjectPrivileges   | ALL [ PRIVILEGES ] } ON { <object_type> <object_name> | ALL <object_type_plural> IN { DATABASE <db_name> | SCHEMA <schema_name> }
      }
    TO APPLICATION <name>
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

    Bulk grants on pipes are not allowed.

`name`
:   Specifies the identifier for the recipient application (the application to which the privileges are granted).

## Usage notes

- Granting OWNERSHIP privileges on an object or all objects of a specified type in a schema or database to an application, or transferring ownership of the object from one application to another application, is not allowed.
- Any ACCOUNT level privilege grant (not REVOKE) that is not in the current application version manifest is not allowed.

## Example

Grant the SELECT privilege on a view to an application:

Copy code

```
GRANT SELECT ON VIEW data.views.credit_usage
  TO APPLICATION app_snowflake_credits;
```
