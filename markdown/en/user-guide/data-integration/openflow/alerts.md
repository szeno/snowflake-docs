# Set up alerts for Openflow

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow alerts are [Snowflake alerts](/user-guide/alerts) that are based on [Openflow telemetry](/user-guide/data-integration/openflow/monitor).
Snowflake provides alert templates for Openflow connectors and runtimes. An alert created from a template regularly queries
the event table and notifies you when its condition is met. The template defines the condition and the action, and you supply only the settings:
connectors, runtimes, or deployments to monitor, and the notification type and target.

Note

Templates come in separate [gen 1 and gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations) versions.
Each version monitors only connectors and runtimes of its own generation, so to monitor both, create an alert for each version.

## Before you begin

- Openflow must write telemetry to an event table. See [Prerequisites for Openflow alerts](/user-guide/alerts-ui#label-alerts-center-prerequisites-openflow).
- To send notifications, create a notification integration. See
  [Setting up notifications for alerts](/user-guide/alerts-ui#label-alerts-center-prerequisites-notification).
- Use a role that can create and monitor alerts. See [Creating a role for accessing alerts in Snowsight](/user-guide/alerts-ui#label-alerts-center-prerequisites-role).

## Create an alert from a template

In Snowsight, choose a template from the **OPENFLOW** template group. See
[Creating a new alert](/user-guide/alerts-ui#label-alerts-center-create). To create the alert with SQL, see
[Creating an alert from a template with SQL](/user-guide/alerts#label-alerts-create-from-template).

## Connector templates

The following templates monitor connectors. Each alert notification identifies the connector and links to its
details page in Snowsight.

| Template | Description | Settings |
| --- | --- | --- |
| **Connector backpressure (object count)** | Fires when a connection of a connector applies back pressure based on the number of queued FlowFiles for at least the configured fraction of the lookback window. Can be configured for the account, a deployment, a runtime, or a connector. | - **Alert threshold**: Fraction of the lookback window that back pressure must be applied for. Default: *0.1*. - **Lookback window (minutes)**: Default: *60*. |
| **Connector backpressure (bytes)** | Fires when a connection of a connector applies back pressure based on the size of queued FlowFiles for at least the configured fraction of the lookback window. Can be configured for the account, a deployment, a runtime, or a connector. | - **Alert threshold**: Fraction of the lookback window that back pressure must be applied for. Default: *0.1*. - **Lookback window (minutes)**: Default: *60*. |
| **High queued count alert** | Fires when the number of FlowFiles queued in a connection of a connector exceeds a fraction of the back pressure threshold for at least the configured fraction of the lookback window. Can be configured for the account, a deployment, a runtime, or a connector. | - **High threshold**: Fraction of the back pressure threshold. Default: *0.8*. - **Alert threshold**: Fraction of the lookback window that the queue must exceed the threshold for. Default: *0.1*. - **Lookback window (minutes)**: Default: *60*. |
| **High queued bytes alert** | Fires when the size of the FlowFiles queued in a connection of a connector exceeds a fraction of the back pressure threshold for at least the configured fraction of the lookback window. Can be configured for the account, a deployment, a runtime, or a connector. | - **High threshold**: Fraction of the back pressure threshold. Default: *0.8*. - **Alert threshold**: Fraction of the lookback window that the queue must exceed the threshold for. Default: *0.1*. - **Lookback window (minutes)**: Default: *60*. |
| **High error rate alert** | Fires when the components of a connector log at least the threshold number of errors during the lookback window. Can be configured for the account, a deployment, a runtime, or a connector. | - **Alert threshold (error count)**: Default: *10*. - **Lookback window (minutes)**: Default: *60*. |
| **No data alert** | Fires when a connector doesn’t receive data or doesn’t send data during the lookback window. Can be configured for the account, a deployment, a runtime, or a connector. | **Lookback window (hours)**: Default: *4*. |
| **Openflow connector health alert** | Fires when a connector becomes unhealthy. The definition of health differs across connector types. Can be configured for the account, a deployment, a runtime, or a connector. | **Lookback window (hours)**: Default: *1*. |

Expand

Show lessSee more

## Runtime templates

The following templates monitor runtimes. Each alert notification identifies the runtime.

| Template | Description | Settings |
| --- | --- | --- |
| **Out of memory alert** | Fires when a runtime logs at least the threshold number of *OutOfMemoryError* errors during the lookback window. Can be configured for the account, a deployment, or a runtime. | - **Alert threshold (OutOfMemoryError count)**: Default: *1*. - **Lookback window (minutes)**: Default: *60*. |
| **High runtime storage usage alert** | Fires when the disk usage of a runtime reaches the threshold. Can be configured for the account, a deployment, or a runtime. | **Storage usage threshold**: Fraction of the storage capacity. Default: *0.85*. |

Expand

Show lessSee more

## Connector-specific templates

Some connectors have additional alerts that are based on metrics specific to them.
For those templates, see the monitoring page of the connector:

- [Openflow Connector for MongoDB](/user-guide/data-integration/openflow/connectors/mongodb/monitor)
- [Openflow Connector for MySQL](/user-guide/data-integration/openflow/connectors/mysql/monitor)
- [Openflow Connector for Oracle](/user-guide/data-integration/openflow/connectors/oracle/monitor)
- [Openflow Connector for PostgreSQL](/user-guide/data-integration/openflow/connectors/postgres/monitor)
- [Openflow Connector for SQL Server](/user-guide/data-integration/openflow/connectors/sql-server/monitor)
- [Openflow Connector for SQL Server (CDC)](/user-guide/data-integration/openflow/connectors/sql-server-cdc/monitor)
