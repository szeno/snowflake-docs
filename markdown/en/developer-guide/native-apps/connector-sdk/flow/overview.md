# Connector flow

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

This section describes how the lifecycle of a native connector application is organized from the user perspective.

The connector needs to store its internal state and configuration to be able to work properly.
That information is stored in the tables that are internal to the application.
To prevent accidental manual changes, they are hidden from the end user.
However, the native SDK for connectors provides several views that show the values stored inside them.

The most important tables internally are `STATE.APP_STATE` and `STATE.APP_CONFIG`.
Those tables are described in the below sections.

## Connector internal status

Connector status consists of the two parts called `status` and `configurationStatus`.
`Status` is the global high-level state that the connector is in, while `configurationStatus` can be considered a sub-status during the wizard phase.
The transitions between states are shown in the below diagram:

[![Connector status flow](/static/images/developer-guide/native-apps/connector-sdk/assets/connector_flow.png)](/static/images/developer-guide/native-apps/connector-sdk/assets/connector_flow.png)

The left part of the above diagram shows the transitions of the `status`. The right part shows the transition of the `configurationStatus` during the wizard phase.
For every `configurationStatus`, the value of `status` is `Configuring`.

If at any point the connector *gets stuck* in a particular state - you may need to use the
[PUBLIC.RECOVER\_CONNECTOR\_STATE()](/developer-guide/native-apps/connector-sdk/reference/core_reference#label-connectors-native-sdk-recover-connector-state) procedure
or reinstall the connector to fix the issue.

## Wizard

The wizard phase is the initial phase after installing a connector. It guides the end user through all the needed configurations that need to be finished for the connector to be able to perform ingestion.
Steps of the wizard phase are represented by the `configurationStatus` and are shown in the above diagram in its right part.
This process consists of the following steps:

### Prerequisites

Optional step to ensure that all configurations outside the Connector itself are done. For example authentication in the source system.

More on [Prerequisites](/developer-guide/native-apps/connector-sdk/flow/prerequisites).

### Connector configuration

Configuration of the most crucial properties of the connector application, such as the warehouse, sink database, etc.

More on [Connector Configuration](/developer-guide/native-apps/connector-sdk/flow/connector_configuration).

### Connection configuration

Configuration of the properties required to connect to the external source system, for example authentication method, credentials etc.

More on [Connection Configuration](/developer-guide/native-apps/connector-sdk/flow/connection_configuration).

### Configuration finalization

Finalization is the last step of the wizard. It provides the means to perform any additional configurations custom to the connector.

More on [Configuration Finalization](/developer-guide/native-apps/connector-sdk/flow/finalize_configuration).

## Daily use

After the wizard phase is completed, the connector is ready to start ingesting data. Lifecycle operations are enabled.
The following options become available:

### Ingestion management

Ingestion management is the most important part of the connector. It defines what data should be ingested from the source system.

For more information, see [Ingestion management](/developer-guide/native-apps/connector-sdk/flow/ingestion-management/overview).

### Pausing and Resuming Connector

Pausing and resuming connector allows end user to completely stop and restart all of the connector operations.
Paused connector does not ingest data, but the costs of maintaining it are also minimized.

For more information, see [Pausing Connector](/developer-guide/native-apps/connector-sdk/flow/pause_connector) and [Resuming Connector](/developer-guide/native-apps/connector-sdk/flow/resume_connector).

### Viewing Statistics

Statistics collected during the ingestion allow end user to see how much data connector ingests on the hourly basis and can help to notice anomalies in the connector behavior.

For more information, see [Viewing Statistics](/developer-guide/native-apps/connector-sdk/reference/connector_stats_reference).

## Configuration update

When the wizard phase is complete, the Connector is fully configured and ready to start ingesting data.
To make changes to the configuration after the wizard phase, use one of the following options:

### Updating the connection configuration

To change the configuration which was set in the [Connection Configuration](/developer-guide/native-apps/connector-sdk/flow/connection_configuration) wizard step.

For more information, see [Update Connection Configuration](/developer-guide/native-apps/connector-sdk/flow/update_connection_configuration).

### Updating the warehouse

To change the warehouse which was set in [Connector Configuration](/developer-guide/native-apps/connector-sdk/flow/connector_configuration) wizard step.

For more information, see [Update Warehouse](/developer-guide/native-apps/connector-sdk/flow/update_warehouse).
