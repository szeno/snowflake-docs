# Set up and access Openflow

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

To use Openflow, you must configure roles and permissions in your Snowflake account, and set up a database. This topic describes how to set up the necessary roles and permissions. For the privilege model, including `OWNERSHIP`, `USAGE`, `OPERATE`, and `MONITOR`, see [Openflow privileges](/user-guide/data-integration/openflow/privileges).

Note

Openflow isn’t automatically available in trial accounts. To enable it, contact your Snowflake account team.

## Set up the Openflow admin roles

The **Openflow Admin role** is used by a deployment engineer to set up Openflow workflows. A Snowflake administrator adds this role by performing the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Open a SQL worksheet.
3. Create a role for the Openflow admin, granting it the permissions to manage integrations and compute pools required for deployments. In the SQL below, OPENFLOW\_ADMIN is the default name for the Openflow admin, but you can choose any name.

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   CREATE ROLE IF NOT EXISTS OPENFLOW_ADMIN;

   GRANT CREATE ROLE ON ACCOUNT TO ROLE OPENFLOW_ADMIN;

   -- Gen 2 privileges:
   GRANT CREATE OPENFLOW DEPLOYMENT ON ACCOUNT TO ROLE OPENFLOW_ADMIN;
   GRANT CREATE DATABASE ON ACCOUNT TO ROLE OPENFLOW_ADMIN;
   GRANT CREATE INTEGRATION ON ACCOUNT TO ROLE OPENFLOW_ADMIN;

   -- To add a runtime to an existing gen 1 deployment, also grant:
   -- GRANT CREATE OPENFLOW RUNTIME INTEGRATION ON ACCOUNT TO ROLE OPENFLOW_ADMIN;
   ```
4. Grant the admin role and secondary roles to a user.

   When you create an Openflow user, grant the Openflow administrator role and set it as `DEFAULT_ROLE`. Runtime sign-in fails when the default role is `ACCOUNTADMIN`, `ORGADMIN`, `GLOBALORGADMIN`, or `SECURITYADMIN`. While the user is signed in, Openflow can authorize actions with any of that user’s roles.

   Setting `DEFAULT_SECONDARY_ROLES = ('ALL')` is recommended but not required. Users who don’t have it set can select a role by using the role picker in the Openflow UI. The selected role must hold the required Openflow grants, and in gen 2, deployments are visible only through that role. For details, see [Openflow privileges](/user-guide/data-integration/openflow/privileges).

   Substitute <OPENFLOW\_USER> with the appropriate username:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   GRANT ROLE OPENFLOW_ADMIN TO USER <OPENFLOW_USER>;
   ALTER USER <OPENFLOW_USER> SET DEFAULT_ROLE = OPENFLOW_ADMIN;
   ALTER USER <OPENFLOW_USER> SET DEFAULT_SECONDARY_ROLES = ('ALL');
   ```

## Start Openflow

Log in to Openflow by performing the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Ingestion** » **Openflow**.
3. Select **Launch Openflow**.

### Troubleshooting login issues

- If you can sign in to Snowflake but can’t sign in to a runtime, try the following:
  - Set the user’s `DEFAULT_ROLE` to a role other than `ACCOUNTADMIN`, `ORGADMIN`, `GLOBALORGADMIN`, or `SECURITYADMIN`.
  - If you rely on secondary roles for Openflow privileges, add default secondary roles to the user:

    Copy code

    ```
    USE ROLE ACCOUNTADMIN;
    ALTER USER <OPENFLOW_USER> SET DEFAULT_SECONDARY_ROLES = ('ALL');
    ```
