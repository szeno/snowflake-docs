# Snowflake Feature Store access control model

The privileges required by the Snowflake Feature Store depend on the type of user.

- *Producers* can create and operate on feature views.
- *Consumers* can read information about feature views and entities in the feature store.

Typically, each type of user will have their own [Snowflake database role](/sql-reference/snowflake-db-roles) with
the necessary privileges. Feature store roles are most naturally configured using a
[role hierarchy](/user-guide/security-access-control-overview#label-role-hierarchy-and-privilege-inheritance).

![Examples of setting up consumer and producer roles in two feature stores](/static/images/screens/snowflake-feature-store-dual-fs-roles.png)

Producers require the following privileges:

- CREATE DYNAMIC TABLE, CREATE TAG, and CREATE VIEW on the feature store schema.

  > Note
  >
  > For Snowflake-managed feature views (backed by a dynamic table) with incremental refresh, the source tables must have
  > [change tracking enabled](/user-guide/dynamic-tables/troubleshoot-creation#label-dynamic-tables-and-change-tracking), or the user must have OWNERSHIP of these tables
  > to automatically enable change tracking when the feature view is created.
- CREATE TABLE and CREATE DATASET on the feature store schema and/or the destination schema when generating datasets for
  training.
- OPERATE on the dynamic tables and tasks in the feature store schema to manage Feature View refresh settings.
- USAGE on the warehouse passed in to the feature store initializer.
- CREATE SCHEMA is optional if the feature store schema already exists and the producers have usage privileges on it.
- All consumer privileges listed below.

Consumers require the following privileges at minimum:

- USAGE on the feature store database and schema.
- SELECT on and MONITOR on DYNAMIC TABLES in the feature store schema.
- SELECT and REFERENCE on views in the feature store schema.
- USAGE on the warehouse passed to the feature store initializer.

Consumers can also have the following privileges to allow them to use feature store data:

- CREATE TABLE and CREATE DATASET on the feature store schema and/or the destination schema for generating datasets for training.
- SELECT and REFERENCE on tables in the feature store or any schemas containing generated datasets.
- USAGE on DATASETs in the feature store schema or any schemas containing generated datasets.

With multiple feature stores, you probably will have these two types of roles for each individual feature store,
or for logical groupings of feature stores.

Note

A role with `MANAGE GRANTS`, `CREATE ROLE`, and `CREATE SCHEMA ON DATABASE <DB>`
privileges is needed to configure the necessary Feature Store roles and privileges. You may use the
[ACCOUNTADMIN](/user-guide/security-access-control-considerations#label-security-accountadmin-role) built-in role or use a custom role with these privileges.

## Access control setup in Python

`snowflake-ml-python` package version 1.6.3 and later include a `setup_feature_store` utility API for configuring a
new feature store with producer and consumer roles and privileges. In the following example, fill in the names of the
database, schema, warehouse, and producer and consumer role where indicated.

Copy code

```
from snowflake.ml.feature_store import setup_feature_store

setup_feature_store(
    session=session,
    database="<FS_DATABASE_NAME>",
    schema="<FS_SCHEMA_NAME>",
    warehouse="<FS_WAREHOUSE>",
    producer_role="<FS_PRODUCER_ROLE>",
    consumer_role="<FS_CONSUMER_ROLE>",
)
```

## Access control setup in SQL

You can manually configure the Feature Store roles and privileges using the following SQL commands. Note that in the
first block, there are several SET commands that tell the script the names you want to use for your producer and
consumer roles as well as the names of the database and schema where the feature views will be stored. All of these
objects are created if they do not exist.

Copy code

```
-- Initialize variables for usage in SQL scripts below
SET FS_ROLE_PRODUCER = '<FS_PRODUCER_ROLE>';
SET FS_ROLE_CONSUMER = '<FS_CONSUMER_ROLE>';
SET FS_DATABASE = '<FS_DATABASE_NAME>';
SET FS_SCHEMA = '<FS_SCHEMA_NAME>';
SET FS_WAREHOUSE = '<FS_WAREHOUSE>';

-- Create schema
SET SCHEMA_FQN = CONCAT($FS_DATABASE, '.', $FS_SCHEMA);
CREATE SCHEMA IF NOT EXISTS IDENTIFIER($SCHEMA_FQN);

-- Create roles
CREATE ROLE IF NOT EXISTS IDENTIFIER($FS_ROLE_PRODUCER);
CREATE ROLE IF NOT EXISTS IDENTIFIER($FS_ROLE_CONSUMER);

-- Build role hierarchy
GRANT ROLE IDENTIFIER($FS_ROLE_PRODUCER) TO ROLE SYSADMIN;
GRANT ROLE IDENTIFIER($FS_ROLE_CONSUMER) TO ROLE IDENTIFIER($FS_ROLE_PRODUCER);

-- Grant PRODUCER role privileges
GRANT CREATE DYNAMIC TABLE ON SCHEMA IDENTIFIER($SCHEMA_FQN) TO ROLE IDENTIFIER($FS_ROLE_PRODUCER);
GRANT CREATE VIEW ON SCHEMA IDENTIFIER($SCHEMA_FQN) TO ROLE IDENTIFIER($FS_ROLE_PRODUCER);
GRANT CREATE TAG ON SCHEMA IDENTIFIER($SCHEMA_FQN) TO ROLE IDENTIFIER($FS_ROLE_PRODUCER);
GRANT CREATE DATASET ON SCHEMA IDENTIFIER($SCHEMA_FQN) TO ROLE IDENTIFIER($FS_ROLE_PRODUCER);
GRANT CREATE TABLE ON SCHEMA IDENTIFIER($SCHEMA_FQN) TO ROLE IDENTIFIER($FS_ROLE_PRODUCER);

-- Grant CONSUMER role privileges
GRANT USAGE ON DATABASE IDENTIFIER($FS_DATABASE) TO ROLE IDENTIFIER($FS_ROLE_CONSUMER);
GRANT USAGE ON SCHEMA IDENTIFIER($SCHEMA_FQN) TO ROLE IDENTIFIER($FS_ROLE_CONSUMER);

GRANT SELECT, MONITOR ON FUTURE DYNAMIC TABLES IN SCHEMA IDENTIFIER($SCHEMA_FQN) TO ROLE IDENTIFIER($FS_ROLE_CONSUMER);
GRANT SELECT, MONITOR ON ALL DYNAMIC TABLES IN SCHEMA IDENTIFIER($SCHEMA_FQN) TO ROLE IDENTIFIER($FS_ROLE_CONSUMER);

GRANT SELECT, REFERENCES ON FUTURE VIEWS IN SCHEMA IDENTIFIER($SCHEMA_FQN) TO ROLE IDENTIFIER($FS_ROLE_CONSUMER);
GRANT SELECT, REFERENCES ON ALL VIEWS IN SCHEMA IDENTIFIER($SCHEMA_FQN) TO ROLE IDENTIFIER($FS_ROLE_CONSUMER);

GRANT USAGE ON FUTURE DATASETS IN SCHEMA IDENTIFIER($SCHEMA_FQN) TO ROLE IDENTIFIER($FS_ROLE_CONSUMER);
GRANT USAGE ON ALL DATASETS IN SCHEMA IDENTIFIER($SCHEMA_FQN) TO ROLE IDENTIFIER($FS_ROLE_CONSUMER);

-- Grant USAGE ON WAREHOUSE to CONSUMER
GRANT USAGE ON WAREHOUSE IDENTIFIER($FS_WAREHOUSE) TO ROLE IDENTIFIER($FS_ROLE_CONSUMER);
```
