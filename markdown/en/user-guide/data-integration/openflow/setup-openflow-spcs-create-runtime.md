# Set up Openflow - Snowflake Deployment: Create runtime

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

A runtime hosts your data integration flows within a deployment: connectors and custom flow definitions. Each runtime is isolated for security and resource
control, and can scale from one node up to fifty to handle varying data volumes.

You can create a runtime from the Openflow UI, which works for both generations, or with SQL. The
SQL commands in this topic create gen 2 runtimes.

### Using the Openflow UI

To create a runtime in your Snowflake deployment:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Ingestion** » **Openflow**.
3. Select **Launch Openflow**. A new tab opens for the Openflow canvas.
4. In **Openflow Control Plane**, select **Create a runtime**. The **Create Runtime** dialog box appears.
5. In the **Create Runtime** populate the following fields:

   | Field | Description |
   | --- | --- |
   | **Runtime Name** | Enter a name for your runtime. |
   | **Deployment** drop down | Choose the deployment previously created in [Set up Openflow - Snowflake Deployment: Create deployment](/user-guide/data-integration/openflow/setup-openflow-spcs-deployment) |
   | **Node type tier** | Choose a node type tier from the **Node type tier** drop-down list. This specifies the CPU and heap memory available to each node. For guidance on choosing a tier, see [Runtime sizing and packing for CDC connectors](/user-guide/data-integration/openflow/connectors/cdc-runtime-sizing). |
   | **Min/Max node** | In the **Min/Max node** range selector, select a range. The minimum value specifies the number of nodes that the runtime starts with when idle and the maximum value specifies the number of nodes that the runtime can scale up to, in the event of high data volume or CPU load. |
   | **Execute-as role** | Choose the execute-as role previously created in [Set up Openflow - Snowflake Deployment: Create the execute-as role and external access integrations](/user-guide/data-integration/openflow/setup-openflow-spcs-create-rr). |
   | **Usage Roles** | Optionally, select the roles created to grant usage to the runtime for required databases, schema, and table access. |
   | **External Access Integrations** | Optionally, select the previously created external access integrations to grant access to external resources. |

   Expand

   Show lessSee more
6. Select **Create**. The runtime takes a couple of minutes to be created.

Your runtime will appear in the runtime table in the control plane.

### Using SQL (gen 2)

Gen 2 runtimes are schema-level objects created with SQL:

Copy code

```
USE ROLE OPENFLOW_ADMIN;
USE DATABASE openflow_db;
USE SCHEMA openflow_schema;

CREATE OPENFLOW RUNTIME my_runtime
  IN DEPLOYMENT my_deployment
  NODE_TYPE = MEDIUM
  NODE_TYPE_TIER = 'M4'
  MIN_NODES = 1
  MAX_NODES = 1
  EXECUTE_AS_ROLE = openflow_execute_as_rl
  EXTERNAL_ACCESS_INTEGRATIONS = (my_eai)
  DISPLAY_NAME = 'My Runtime';
```

For the full gen 2 workflow, see
[Quickstart: gen 2 Openflow](/user-guide/data-integration/openflow/gen2/quickstart#label-openflow-gen2-quickstart-runtime).

## [Optional] Grant MONITOR privileges on the runtime

If you created a [monitoring role](/user-guide/data-integration/openflow/setup-openflow-spcs-deployment#label-openflow-spcs-monitoring-role) when setting up your deployment, you can add the runtime to that role. This allows data engineers or operations teams to monitor the runtime without having the OPENFLOW\_ADMIN role.

- To add the runtime to the monitoring role, run the code for your generation:

  **Gen 2** (runtimes are schema-level objects):

  Copy code

  ```
  USE ROLE OPENFLOW_ADMIN;

  GRANT MONITOR ON OPENFLOW RUNTIME <openflow_db>.<openflow_schema>.<runtime_name> TO ROLE <OPENFLOW_MONITOR_ROLE>;
  ```

  **Gen 1** (runtimes are data plane integrations):

  Copy code

  ```
  USE ROLE OPENFLOW_ADMIN;

  GRANT MONITOR ON INTEGRATION <OPENFLOW_RUNTIME_INTEGRATION_NAME> TO ROLE <OPENFLOW_MONITOR_ROLE>;
  ```

## Next step

Configure allowed domains for Openflow connectors.
See [Set up Openflow - Snowflake Deployment: Configure allowed domains for Openflow connectors](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list).
