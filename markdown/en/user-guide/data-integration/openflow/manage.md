# Manage Openflow

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

This topic covers the following management tasks:

- [Back up flow definitions and protect runtime state](#back-up-flow-definitions-and-protect-runtime-state)
- [Effect of Snowflake account suspension on Openflow Snowflake Deployments](#effect-of-snowflake-account-suspension-on-openflow-snowflake-deployments)
- [Runtime availability and autoscaling behavior](#runtime-availability-and-autoscaling-behavior)
- [Delete a deployment](#delete-a-deployment)
- [Upgrade a deployment](#upgrade-a-deployment)
- [Upgrade a runtime](#upgrade-a-runtime)
- [Upgrade a connector](#upgrade-a-connector)

## Back up flow definitions and protect runtime state

Warning

Flow definitions and runtime-local state (including processor configuration and Apache NiFi flow state held on the runtime) live on **Openflow runtime storage**, not in Snowflake tables. If you remove, replace, or manually tear down that infrastructure **without** exporting your flows first, that data can be **lost permanently**. Snowflake does not provide Time Travel or Fail-safe for this storage.

Before you delete a deployment, delete or recreate a runtime, or manually remove underlying Snowpark Container Services resources or compute tied to Openflow, **export** your flows from the canvas. Right-click the **process group** » **Version** » **Export** (or use the equivalent command your canvas shows).

**Routine upgrades** through the supported Openflow UI ([Upgrade a deployment](#label-update-a-deployment) and [Upgrade a runtime](#label-openflow-upgrading-a-runtime)) are different from destructive removal. You should still export flows regularly as a best practice.

Note

Do not run [DROP ROLE](/sql-reference/sql/drop-role) for a role that provisions or owns Openflow objects until you transfer ownership and privileges to another role you intend to keep (for example with `GRANT OWNERSHIP`). Dropping a role revokes grants and can leave deployments in a broken state.

## Effect of Snowflake account suspension on Openflow Snowflake Deployments

Snowflake organizations and accounts can be suspended for a variety of reasons including non-payment, billing issues, and trial expiration. When an account is suspended, the Openflow - Snowflake Deployment is decommissioned and cannot be recovered.

Check the **Deployments** tab in the Openflow UI. If a deployment shows **Not Reporting** after the account is reactivated, the deployment, its runtimes, and their connectors can’t be recovered.

To continue using Openflow, [create a new deployment](/user-guide/data-integration/openflow/setup-openflow-spcs-deployment).

## Runtime availability and autoscaling behavior

Openflow runtime nodes are not strictly always-on, single-host processes.
Each runtime is a Kubernetes workload that the cluster can reschedule onto
a different compute host. When that happens, the runtime briefly restarts
while a new pod becomes ready. Plan your flows to tolerate short
interruptions rather than assuming the runtime stays on the same host
indefinitely.

Snowflake doesn’t automatically upgrade BYOC runtimes. Upgrades happen
only when a deployment owner initiates them through the Openflow UI or
the deployment agent. Restarts you observe outside of an upgrade window
are typically caused by cluster rebalancing or by host-level events on
the underlying compute.

For Openflow Snowflake deployments running on
[Snowpark Container Services](/developer-guide/snowpark-container-services/overview)
(SPCS), runtimes can also be affected briefly by the scheduled SPCS
[maintenance window](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-maintenance-window).

### Causes of runtime restarts

Runtime or deployment upgrades
:   When the owner of a deployment runs an upgrade, the affected runtime
    restarts to pick up the new version. See
    [Upgrade a runtime](#label-openflow-upgrading-a-runtime) and
    [Upgrade a deployment](#label-update-a-deployment).

Cluster rebalancing and autoscaling
:   Openflow scales the underlying compute up and down based on demand.
    See [Openflow BYOC cost and scaling considerations](/user-guide/data-integration/openflow/cost-byoc) for details on
    how BYOC deployments scale the EC2 node group. During scale-in,
    node-drain, or rebalancing events, the cluster can reschedule a runtime
    pod from one node to another so that the cluster continues to run
    efficiently.

Cloud provider host events
:   The virtual machines that host BYOC runtimes are subject to events
    outside Snowflake’s control, including instance retirement, unexpected
    reboots, and host-level maintenance performed by the cloud service
    provider. When a host becomes unavailable, the cluster reschedules the
    affected runtime onto a healthy node.

### What to expect during a restart

- Openflow runtimes and connectors maintain data integrity across
  restarts. In-flight data held in the runtime’s persistent storage is
  preserved, and the flow resumes after the new pod is ready.
- Expect a short service interruption while the new pod starts and
  reattaches its storage.
- Diagnostic output may report
  `LAST_REQUESTED_RESTART_REASON: "nifi.properties changed"` after a
  reschedule, even when no NiFi configuration was modified. The runtime
  operator reconciles the underlying StatefulSet whenever the pod
  identity or node assignment changes, so this message can reflect a
  reschedule rather than an actual configuration change.

### Design flows for resilience

Because brief runtime interruptions are expected, design your flows to
recover automatically:

- Configure source and destination connectors to checkpoint progress so
  that processing resumes from the last committed position after a
  restart.
- For streaming sources such as
  [Kafka](/user-guide/data-integration/openflow/connectors/kafka/about)
  or [Kinesis](/user-guide/data-integration/openflow/connectors/kinesis/about),
  rely on consumer-group offsets or sequence numbers rather than
  in-memory state on the runtime.
- [Monitor your runtimes](/user-guide/data-integration/openflow/monitor)
  so that you’re notified if a restart doesn’t recover on its own within
  the expected window.
- Choose your caching strategy with restarts in mind. A local, in-memory
  cache is cleared when a runtime node restarts, and Openflow’s locally
  persisted caches are managed per runtime node rather than shared across
  the cluster. If your flow depends on cache state surviving restarts or
  being shared across nodes, use an external cache service such as Redis.

## Delete a deployment

Deleting a deployment removes the management compute pool and all deployment-level
configuration. You must delete all runtimes first. Any data or objects
already integrated into Snowflake aren’t affected.

Warning

Deleting a deployment can’t be undone. Before you delete, make sure all runtimes
have been removed and you no longer need the deployment configuration.

**Gen 2 (SQL):** Drop the deployment directly:

Copy code

```
DROP OPENFLOW DEPLOYMENT my_deployment;
```

**Gen 1 BYOC (AWS Console):**

1. Navigate to EC2 Instances.
2. Select the `openflow-agent-{deployment-key}` instance with your deployment key.
3. Click **Connect** at the top of the page.
4. Switch from **EC2 Instance Connect** to **Connect using EC2 Instance Connect Endpoint**. Leave the default EC2 Instance Connect Endpoint
   in place.
5. Click **Connect**. A new browser tab or window will appear with a
   command-line interface.
6. Run `./destroy.sh` from the shell.

   - This may take 20-30 minutes. If your connection is interrupted, the process continues running in the background.
   - You can log back in and view its status with the command: `journalctl -u docker -f -n 250`
   - The `destroy` process is complete when you see output of `delete successful`.
7. Navigate to
   [CloudFormation](https://us-east-1.console.aws.amazon.com/cloudformation/home)
   in the AWS Console for your region.
8. Delete the CloudFormation stack for your deployment.

From Snowsight:

1. In the navigation menu, select **Ingestion** » **Openflow**.
2. Select **Launch Openflow**.
3. Select the **Deployments** tab.
4. In the row of the deployment you want to delete, select the More options icon.
5. Select **Delete**.
6. In the confirmation dialog, type `delete` to confirm deletion.
7. Click **Delete deployment**.

## Upgrade a deployment

A deployment includes several components: the agent, deployment service, deployment UI,
runtime gateway, and runtime operator. You can upgrade Snowflake deployments and eligible
BYOC deployments directly from the UI: on the **Deployments** tab, an eligible deployment
shows an **Upgrade** option in its More options ([![Three vertical dots indicating more options](/static/images/icons/vertical-more-icon.png)](/static/images/icons/vertical-more-icon.png)) menu. If a BYOC
deployment isn’t eligible, that option doesn’t appear, so upgrade it using the deployment
agent script instead. For details on what’s included in each release, see
[Openflow version history](/user-guide/data-integration/openflow/version-history).

Note

**Snowflake deployments** are upgraded automatically by Snowflake on a rolling basis. If your
deployment is on an older version, it will be upgraded to the latest version automatically;
you do not need to initiate the upgrade yourself. Once a deployment has been upgraded to a
recent version, it will continue to receive automatic upgrades going forward.

**BYOC deployments** are not upgraded automatically. You determine upgrade timing and
frequency using the [deployment agent script](#upgrade-via-the-deployment-agent-byoc) or the
[UI](#upgrade-from-the-ui).

### Upgrade from the UI

The UI upgrade path applies to BYOC deployments. Snowflake deployments are upgraded
automatically and do not require manual intervention.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Ingestion** » **Openflow**.
3. Select **Launch Openflow**.
4. Select the **Deployments** tab.
5. Look for the upgrade arrow to the left of the deployment name. This indicates an upgrade is available.
   [![Deployments tab showing the upgrade arrow indicator next to a deployment name](/static/images/openflow/upgrade-available-deployment.png)](/static/images/openflow/upgrade-available-deployment.png)
6. Select [![Three vertical dots indicating more options](/static/images/icons/vertical-more-icon.png)](/static/images/icons/vertical-more-icon.png) next to the deployment » **Upgrade**.

### Upgrade via the deployment agent (BYOC)

Use the deployment agent script for older BYOC deployments that cannot be upgraded via the UI, or when you prefer to upgrade manually. This upgrades the agent, deployment service, deployment UI, ingress controller, runtime operator, and all other component dependencies.

#### Connect to the deployment agent

1. Navigate to Openflow.
2. Select the **Deployments** tab.
3. View your deployment details and note the deployment key.
4. In your AWS account, view the EC2 instances and filter using the deployment key.
5. Locate the deployment agent EC2 instance named `openflow-agent-{deployment-key}`.
6. Connect using EC2 Instance Connect Endpoint and accepting all defaults.
7. Run the remaining commands from the new browser tab or window that appears with a command-line interface.

#### Check for available upgrades

Copy code

```
cat ~/.upgrade
```

The script will display the latest available version of the various deployment components.

If no upgrades are available, you will see an output similar to this:

```
AGENT_IMAGE_VERSION_UPGRADE=
OPERATOR_CHART_VERSION_UPGRADE=
GATEWAY_IMAGE_VERSION_UPGRADE=
DPS_CHART_VERSION_UPGRADE=
DPUI_CHART_VERSION_UPGRADE=
```

Otherwise, you will see the version that upgraded components will use, such as:

```
AGENT_IMAGE_VERSION_UPGRADE=0.17.0
OPERATOR_CHART_VERSION_UPGRADE=0.31.0
GATEWAY_IMAGE_VERSION_UPGRADE=
DPS_CHART_VERSION_UPGRADE=
DPUI_CHART_VERSION_UPGRADE=
```

#### Upgrading the AMI for the Openflow BYOC deployment

When you upgrade your Openflow BYOC deployment, Openflow will find and upgrade to the latest AMI for Amazon Linux 2023 recommended by
[AWS Systems Manager](https://aws.amazon.com/systems-manager/).

If a new AMI is found, it will restart all Openflow services in your deployment, and runtimes will be temporarily halted.
Openflow runtimes and connectors maintain data integrity across restarts automatically.

Snowflake does not automatically upgrade deployments. You determine upgrade timing and frequency.

#### Initiate the upgrade

If the output indicates that upgrades are available, run the following script to initiate the upgrade. Older Openflow deployments may use the script `upgrade-data-plane.sh` instead.

Copy code

```
./upgrade.sh
```

You will see output similar to this:

```
openflow-data-plane-agent-aws is set to version 0.16.0
   Upgrade set to version 0.17.0
openflow-dataplane-service-chart is set to version 0.47.0
   No upgrade is available
openflow-dataplane-ui-chart is set to version 0.5.0
   No upgrade is available
openflow-runtime-gateway is set to version 2025.6.8.2
   No upgrade is available
runtime-operator-chart is set to version 0.30.0
   Upgrade set to version 0.31.0
```

Then, you have two options:

- Wait for an automatic upgrade: The system will automatically initiate the upgrade process within approximately 10 minutes.
- Manual upgrade: To start the upgrade immediately, run the following command:

Copy code

```
./create.sh
```

#### Monitor the upgrade process

To track the progress of the upgrade, use the `journalctl` command:

Copy code

```
journalctl -u openflow-apply-infrastructure -f -n 250
```

#### Verify a successful upgrade

A successful upgrade will typically show output similar to this:

```
All resources applied successfully and log uploaded to s3
openflow-apply-infrastructure.service: Deactivated successfully
```

## Upgrade a runtime

Snowflake periodically releases runtime updates that introduce new Openflow processors, newer versions of
existing processors, or new runtime functionality. When updates are available, an indicator
appears next to the runtime name in the UI. For details on what’s included in each release, see
[Openflow version history](/user-guide/data-integration/openflow/version-history).

Note

Only the owner of a deployment can perform an upgrade.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Ingestion** » **Openflow**.
3. Select **Launch Openflow**.
4. Select the **Runtimes** tab.
5. Look for the upgrade arrow to the left of the runtime name. This indicates an upgrade is available.
   [![Runtimes tab showing the upgrade arrow indicator next to a runtime name](/static/images/openflow/upgrade-available-runtime.png)](/static/images/openflow/upgrade-available-runtime.png)
6. Select [![Three vertical dots indicating more options](/static/images/icons/vertical-more-icon.png)](/static/images/icons/vertical-more-icon.png) next to the runtime » **Upgrade**.

## Upgrade a connector

Connector updates are made available by Snowflake when functionality is added,
processing logic is improved, or new processor versions are used–for example, to add support for a new source API version.

Note

This section describes upgrading **gen 1** connectors on the runtime canvas. For gen 2 connectors,
see [Manage the gen 2 Openflow connector lifecycle](/user-guide/data-integration/openflow/gen2/manage-connector-lifecycle).

When connector updates are available, you will see an **Upgrade** icon in your process group on the canvas.

Note

You can only upgrade connectors after you have [upgraded their runtime](#label-openflow-upgrading-a-runtime).

If the connector process group has local changes, Openflow analyzes whether it can retain those changes while applying
the connector update. Review the rebase analysis before you apply the update. If the analysis identifies a conflicting
or unsupported local change, the update is blocked. Resolve or revert the change, then retry the connector update.

To upgrade a connector, do the following:

1. In the navigation menu, select **Ingestion** » **Openflow**.
2. Select **Launch Openflow**.
3. Select the **Runtimes** tab.
4. Select the runtime name, or select **View Canvas** in the **More Options** menu to navigate to the canvas.
5. Find the processor groups with a red upgrade arrow next to their names. For each of these groups, change the version:
   1. Recommended: Check to see whether the parameter uses a custom value for the Parameter context. If so, make a note of the custom value. You will need to reapply it after the upgrade.

      1. Right-click the process group and select **Parameters**.
      2. Select **Parameters** in the Parameter Contexts list.
      3. Select the **Inheritance** tab, and check if it uses custom values. If so, make a note of the custom values.
   2. Right-click the group and select **Version** » **Change Version**.
   3. Select the latest available version and select **Change**.
   4. Confirm that the connector was upgraded to the latest version. The upgraded version should show a green check mark.
   5. Confirm that all processors in the connector’s process group are running. If not, start them.

      You can also validate the version by hovering over the speech bubble at the bottom right of the process group.
   6. If you noted a custom parameter value in step 4, reapply the custom value. For more information, see [Openflow connectors](/user-guide/data-integration/openflow/connectors/about-openflow-connectors).

### Configure Snowflake Connector Flow Registry

Important

Early preview releases of Openflow did not configure a runtime for connector upgrades.
If you don’t see the Version option when right clicking on a process group, you
have to configure the Snowflake Connector Flow Registry and manually enable version control for existing connectors.

To configure the Snowflake Connector Flow Registry, do the following:

1. Navigate to the canvas.
2. Click on the menu in the top right corner and select **Controller Settings**.
3. Switch to the **Registry Clients** tab.
4. Click the **+** icon to add a new Registry Client.
5. Select the **ConnectorFlowRegistryClient** and select **Add**.
6. Click **More Options** for the **ConnectorFlowRegistryClient** row and select **Edit**.
7. Enter `/nifi/configuration_resources/connector_flow_registry` as the value
   for **Storage Location** and select **Apply**.

After configuring the Snowflake Connector Flow Registry you can now enable version control for your existing connectors.

To enable version control for existing connectors, do the following:

1. Navigate to the canvas and locate the process group where you want to add version control.
2. Right click on the process group and select **Version** » **Set Version**.
3. In the **Set Version** dialog, choose the flow that matches your process group.

   For example, choose **sqlserver** if you are using the SQL Server connector.

   Note that flow names do not exactly match the connector name.
4. Select the latest version and then select **Set version** to enable version control.
5. From the canvas, right click on the process group again and select **Version** » **Revert Local Changes**
   to apply the latest connector version.
6. Review the list of changes and select **Revert**.
7. Confirm that your connector was upgraded to the latest version which should now show a green check mark.
   You can also validate the version by hovering over the speech bubble at the bottom right of the process group.
