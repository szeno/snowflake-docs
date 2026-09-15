# Set up Openflow - Snowflake Deployment: Create deployment

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

After configuring core Snowflake, create an Openflow deployment. A deployment is the
data plane container for your runtimes and connectors. Each deployment can host
multiple runtimes, and each runtime can run multiple connectors, giving you flexibility to
isolate workloads by project, team, or environment. There is no separate charge for the
deployment itself; only active runtimes consume Snowflake credits.

1. [Create a deployment](#label-openflow-spcs-create-deployment).
2. [[Optional] Configure an Openflow-specific event table](#label-openflow-spcs-event-table) - configure an Openflow-specific event table to store Openflow logs and metrics.

## Create a deployment

You can create a deployment from the Openflow UI or with SQL. All new deployments are gen 2.

Note

New gen 1 deployments can’t be created. Existing gen 1 deployments continue to work unchanged.

For other ways to tell gen 1 and gen 2 resources apart, see
[How to identify gen 1 and gen 2 resources](/user-guide/data-integration/openflow/gen2/openflow-generations#label-openflow-generations-identify).

### Using the Openflow UI

Note

To access the Openflow Runtime UI using PrivateLink as described in [Setup PrivateLink UI access](/user-guide/data-integration/openflow/setup-openflow-spcs-configure-pr-ui),
ensure the **PrivateLink** option is enabled when creating a new Openflow - Snowflake Deployment.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) with a role defined in [Configure core Snowflake requirements](/user-guide/data-integration/openflow/setup-openflow-spcs-sf).
2. In the navigation menu, select **Ingestion** » **Openflow**.
3. Select **Launch Openflow**.
4. In the Openflow UI, select **Create a deployment**. The **Deployments** tab opens.
5. Select **Create a deployment**. The Creating a deployment wizard opens.
6. In the **Prerequisites** step, ensure that you meet all the requirements. Select **Next**.
7. In the **Deployment location** step, select **Snowflake** as the deployment location.
   Enter a name for your deployment. Select **Next**.
8. Select **Create Deployment**.

### Using SQL (gen 2)

Gen 2 deployments are first-class Snowflake objects created with SQL:

Copy code

```
USE ROLE OPENFLOW_ADMIN;

CREATE OPENFLOW DEPLOYMENT my_deployment
  DEPLOYMENT_TYPE = SNOWFLAKE
  -- USE_PRIVATE_LINK = TRUE,  -- Enable if you need PrivateLink
  DISPLAY_NAME = 'My Snowflake Deployment';
```

For PrivateLink considerations and additional parameters, see
[Quickstart: gen 2 Openflow](/user-guide/data-integration/openflow/gen2/quickstart#create-a-gen-2-deployment).

## [Optional] Configure an Openflow-specific event table

Openflow generates logs and metrics and sends them to the Snowflake Event Table.
For helpful queries to analyze this telemetry data, see [Monitor Openflow](/user-guide/data-integration/openflow/monitor).

By default, Openflow uses the [account event table](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-default) (SNOWFLAKE.TELEMETRY.EVENTS), but you can configure an Openflow-specific event table per deployment. A dedicated event table is recommended to optimize query performance, enable granular access control, and simplify Openflow monitoring and maintenance.

1. Create the event table in the Openflow infrastructure schema:

   Copy code

   ```
   USE ROLE OPENFLOW_ADMIN;
   USE DATABASE <openflow_db>;
   USE SCHEMA <openflow_schema>;

   CREATE EVENT TABLE IF NOT EXISTS <openflow_db>.<openflow_schema>.openflow_events;
   ```
2. Get your deployment name and set the event table:

   **Gen 2:**

   Copy code

   ```
   SHOW OPENFLOW DEPLOYMENTS;

   ALTER OPENFLOW DEPLOYMENT <deployment_name>
     SET EVENT_TABLE = '<openflow_db>.<openflow_schema>.openflow_events';
   ```

   **Gen 1:**

   Copy code

   ```
   SHOW OPENFLOW DATA PLANE INTEGRATIONS;

   ALTER OPENFLOW DATA PLANE INTEGRATION <OPENFLOW_DATAPLANE_INTEGRATION_NAME>
     SET EVENT_TABLE = '<openflow_db>.<openflow_schema>.openflow_events';
   ```

## [Optional] Create a monitoring role

A monitoring role lets data engineers or operations teams monitor Openflow without having the OPENFLOW\_ADMIN role.

- To create a monitoring role, run the following code:

  **Gen 2:**

  Copy code

  ```
  USE ROLE OPENFLOW_ADMIN;

  CREATE ROLE IF NOT EXISTS <OPENFLOW_MONITOR_ROLE>;
  GRANT MONITOR ON OPENFLOW DEPLOYMENT <deployment_name> TO ROLE <OPENFLOW_MONITOR_ROLE>;
  GRANT ROLE <OPENFLOW_MONITOR_ROLE> TO ROLE <OPENFLOW_ADMIN_ROLE>;
  GRANT ROLE <OPENFLOW_MONITOR_ROLE> TO USER <SNOWFLAKE_USER>;
  ```

  **Gen 1:**

  Copy code

  ```
  USE ROLE OPENFLOW_ADMIN;

  CREATE ROLE IF NOT EXISTS <OPENFLOW_MONITOR_ROLE>;
  GRANT MONITOR ON INTEGRATION <OPENFLOW_DATAPLANE_INTEGRATION_NAME> TO ROLE <OPENFLOW_MONITOR_ROLE>;
  GRANT ROLE <OPENFLOW_MONITOR_ROLE> TO ROLE <OPENFLOW_ADMIN_ROLE>;
  GRANT ROLE <OPENFLOW_MONITOR_ROLE> TO USER <SNOWFLAKE_USER>;
  ```

### Next steps

[Create the execute-as role and external access integrations](/user-guide/data-integration/openflow/setup-openflow-spcs-create-rr)
