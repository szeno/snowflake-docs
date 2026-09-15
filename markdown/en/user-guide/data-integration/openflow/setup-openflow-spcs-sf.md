# Set up Openflow - Snowflake Deployment: Core Snowflake

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow - Snowflake Deployment requires the creation of the following Snowflake specific resources:

> 1. [Create the OPENFLOW\_ADMIN role](#create-the-openflow-admin-role)
> 2. [Configure required privileges](#configure-required-privileges)

To complete these tasks, Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) and open a SQL worksheet.

## Create the OPENFLOW\_ADMIN role

Create the required Openflow administration role.

Note

`<OPENFLOW_USER>` denotes the user that will be used to access Openflow.

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS OPENFLOW_ADMIN;

GRANT ROLE OPENFLOW_ADMIN TO USER <OPENFLOW_USER>;
```

Caution

Users with a default role of ACCOUNTADMIN can’t login to Openflow - Snowflake Deployment runtimes and will get an error message when attempting to do so.
Snowflake recommends assigning a different default role to any user that will login to a runtime.
In addition, Snowflake recommends setting default secondary roles to `ALL` for all Openflow users.

To change the default role and enable all secondary roles, execute the following:

For example:

Copy code

```
USE ROLE ACCOUNTADMIN;

ALTER USER <openflow_user> SET DEFAULT_ROLE = <openflow_admin>;
ALTER USER <openflow_user> SET DEFAULT_SECONDARY_ROLES = ('ALL');
```

## Configure required privileges

Openflow requires defining specific Snowflake account-level privileges.
These privileges are assigned to the ACCOUNTADMIN role as part of the default set of privileges.
ACCOUNTADMIN will automatically have the following privileges and will be able to grant them
to a role of their choosing for the Openflow admin role, shown as `OPENFLOW_ADMIN` role in the following examples.

### Gen 2 privileges

Gen 2 deployments are account-level objects, while runtimes and connectors are schema-level objects.
Those schema-level objects need a database and schema to live in. Snowflake recommends designating one
database and schema to hold your Openflow infrastructure objects, which keeps them easy to manage.

1. Grant the Openflow admin role the account-level privileges it needs:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   GRANT CREATE OPENFLOW DEPLOYMENT ON ACCOUNT TO ROLE OPENFLOW_ADMIN;
   GRANT CREATE DATABASE ON ACCOUNT TO ROLE OPENFLOW_ADMIN;
   GRANT CREATE INTEGRATION ON ACCOUNT TO ROLE OPENFLOW_ADMIN;

   -- Snowflake deployments only:
   GRANT CREATE COMPUTE POOL ON ACCOUNT TO ROLE OPENFLOW_ADMIN;
   ```
2. Create the database and schema that will hold your gen 2 Openflow objects:

   Copy code

   ```
   USE ROLE OPENFLOW_ADMIN;

   CREATE DATABASE IF NOT EXISTS openflow_db;
   CREATE SCHEMA IF NOT EXISTS openflow_db.openflow_schema;
   ```

   This is your Openflow **infrastructure database and schema**, also referred to as the control
   schema. Your deployments’ runtimes, your connectors, and any secrets those connectors reference
   live here. You create it once and reuse it.

   Important

   Keep the infrastructure database separate from the databases your connectors write data to.
   Snowflake recommends a dedicated destination database per connector.

   A connector creates destination schemas and tables named after the source’s schemas and tables.
   Those names aren’t under your control and can change as the source changes, so pointing a
   connector at your infrastructure database risks collisions with the Openflow objects that live
   there.
3. Grant the Openflow admin role the ability to create gen 2 objects in that schema:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   GRANT CREATE OPENFLOW RUNTIME ON SCHEMA openflow_db.openflow_schema TO ROLE OPENFLOW_ADMIN;
   GRANT CREATE OPENFLOW CONNECTOR ON SCHEMA openflow_db.openflow_schema TO ROLE OPENFLOW_ADMIN;
   ```

For the full gen 2 setup workflow, see
[Quickstart: gen 2 Openflow](/user-guide/data-integration/openflow/gen2/quickstart).

### Gen 1 privileges

New gen 1 deployments can’t be created. If you have an existing gen 1 deployment, grant these
privileges to add a runtime to it:

Copy code

```
USE ROLE ACCOUNTADMIN;

GRANT CREATE OPENFLOW RUNTIME INTEGRATION ON ACCOUNT TO ROLE OPENFLOW_ADMIN;
GRANT CREATE DATABASE ON ACCOUNT TO ROLE OPENFLOW_ADMIN;
GRANT CREATE INTEGRATION ON ACCOUNT TO ROLE OPENFLOW_ADMIN;
GRANT CREATE COMPUTE POOL ON ACCOUNT TO ROLE OPENFLOW_ADMIN;
```

## Next steps

Optionally, [Set up PrivateLink UI access](/user-guide/data-integration/openflow/setup-openflow-spcs-configure-pr-ui) to access the Snowflake Openflow Runtime UI using private connectivity.

[Create deployment](/user-guide/data-integration/openflow/setup-openflow-spcs-deployment)
