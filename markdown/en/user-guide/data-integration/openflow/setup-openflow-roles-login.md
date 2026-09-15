# Set up and access Openflow

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

To use Openflow, you must configure roles and permissions in your Snowflake account, and set up a database. This topic describes how to set up the necessary roles and permissions.

Note

Openflow isn’t automatically available in trial accounts. To enable it, contact your Snowflake account team.

## Set up the Openflow admin roles

The **Openflow Admin role** is used by a deployment engineer to set up Openflow workflows. A Snowflake administrator adds this role by performing the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Open a SQL worksheet.
3. Create a role for the Openflow admin, allowing it the required permissions to manage integrations and compute pools required for deployments. In the SQL below, OPENFLOW\_ADMIN is the default name for the Openflow admin, but you can choose any name.

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

   To prevent issues with login, when you create an Openflow user, Snowflake recommends that you also assign and set default secondary roles to that user. This is helpful because Openflow doesn’t allow users with the following roles to log in: ACCOUNTADMIN, ORGADMIN, GLOBALORGADMIN, or SECURITYADMIN. While logged in, Openflow actions can be authorized by any of the authenticated user’s roles, not just the default role.

   Substitute <OPENFLOW\_USER> with the appropriate username:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   GRANT ROLE OPENFLOW_ADMIN TO USER <OPENFLOW_USER>;
   ALTER USER <OPENFLOW_USER> SET DEFAULT_ROLE = OPENFLOW_ADMIN;
   ALTER USER <OPENFLOW_USER> SET DEFAULT_SECONDARY_ROLES = ('ALL');
   ```

## Accept the Openflow terms of service

This step is only required once for your organization.

1. Sign in to Snowflake as a user with the ORGADMIN role.
2. In the navigation menu, select **Ingestion** » **Openflow**.
3. Review the agreement and select **Accept**.

## Start Openflow

Log in to Openflow by performing the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Ingestion** » **Openflow**.
3. Select **Launch Openflow**.

### Troubleshooting login issues

- If you can log into Snowflake but can’t log into Openflow, try the following:
  - Try changing your role to something other than ACCOUNTADMIN, ORGADMIN, GLOBALORGADMIN, or SECURITYADMIN.
  - Try adding default secondary roles to the account:

    Copy code

    ```
    USE ROLE ACCOUNTADMIN;
    ALTER USER <OPENFLOW_USER> SET DEFAULT_SECONDARY_ROLES = ('ALL');
    ```
