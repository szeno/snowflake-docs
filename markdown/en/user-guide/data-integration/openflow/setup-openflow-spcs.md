# Set up Openflow - Snowflake Deployment - Task overview

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

To setup an Openflow - Snowflake Deployment, perform the following tasks:

Note

The steps below cover both generations. New deployments are always gen 2; existing gen 1
deployments continue to work unchanged. For details, see
[Create a deployment](/user-guide/data-integration/openflow/setup-openflow-spcs-deployment#label-openflow-spcs-create-deployment).
New to gen 2? See the [gen 2 Openflow quickstart](/user-guide/data-integration/openflow/gen2/quickstart)
for a streamlined SQL-first walkthrough.

| Order | Task | Description | Persona |
| --- | --- | --- | --- |
| 1 | [Setup core Snowflake](/user-guide/data-integration/openflow/setup-openflow-spcs-sf) | Before creating a deployment, you must configure core Snowflake which include an Openflow admin role, required privileges, and network configuration. | Snowflake administrator |
| 2 | Optionally [Set up PrivateLink UI access](/user-guide/data-integration/openflow/setup-openflow-spcs-configure-pr-ui) | Configure PrivateLink to access the Snowflake Openflow Runtime UI using private connectivity. | Snowflake administrator |
| 3 | [Create deployment](/user-guide/data-integration/openflow/setup-openflow-spcs-deployment) | After configuring core Snowflake, you then create an Openflow deployment. Deployments are created with `CREATE OPENFLOW DEPLOYMENT` (SQL) or the Openflow UI.  Optionally, configure an Openflow-specific event table to store Openflow logs and metrics. | Deployment engineer, Snowflake administrator for event table configuration |
| 4 | [Create the execute-as role and external access integrations](/user-guide/data-integration/openflow/setup-openflow-spcs-create-rr) | Create the role that connectors use to access Snowflake resources. This is called the execute-as role. Both require external access integrations for Snowflake deployments. | Data engineer |
| 5 | [Create runtime](/user-guide/data-integration/openflow/setup-openflow-spcs-create-runtime) | Create a runtime associated with the previously created role. Gen 2 uses `CREATE OPENFLOW RUNTIME` (SQL); gen 1 uses the Openflow UI. | Data engineer |
| 6 | [Configure allowed domains for Openflow connectors](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list) | Configure access to external domains for Openflow connectors. | Data engineer |
| 7 | [Connect your data sources using Openflow connectors](/user-guide/data-integration/openflow/connectors/about-openflow-connectors) | Configure one or more connectors in the Openflow - Snowflake Deployment. Gen 2 connectors can be created with SQL (`CREATE OPENFLOW CONNECTOR`) or the [setup wizard](/user-guide/data-integration/openflow/gen2/setup-connector-wizard). Gen 1 connectors are installed from the catalog on the runtime canvas. | Data engineer |

Expand

Show lessSee more

Note that step 3 (deployment creation) is typically done once. Steps 4 and 5 (role and runtime creation) are repeated for each runtime you add to the deployment.

## Next steps

[Set up Openflow - Snowflake Deployment: Core Snowflake](/user-guide/data-integration/openflow/setup-openflow-spcs-sf)
