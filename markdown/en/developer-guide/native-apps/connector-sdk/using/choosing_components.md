# Choosing SDK components

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

The connectors native SDK consists of multiple components, some of them are independent and some of them depend on each other to work.
This section explains how to customize which components will be turned on in the connector.
Additionally, each component will be shortly described and their dependencies will be mentioned.

## Enabling/disabling components

Components are enabled and disabled on the Snowflake database objects level. This means that the executed `setup.sql`
file is the source of truth on what was enabled or disabled. For the first time users it is recommended to use the `all.sql` file provided by the SDK.
This file includes all of the basic features from the SDK (except Task Reactor).

To do so simply put the following line in the `setup.sql` file of the connector:

Copy code

```
EXECUTE IMMEDIATE FROM 'native-connectors-sdk-components/all.sql';
```

For more experienced users it is possible to customize enabled and disabled features.
To do so add and remove `EXECUTE IMMEDIATE` statements as needed.
Keep in mind that excluding a file which is required by the feature will break it.

Copy code

```
-- Core connector objects
EXECUTE IMMEDIATE FROM 'core.sql';

-- Connector configuration prerequisites
EXECUTE IMMEDIATE FROM 'prerequisites.sql';

-- Connector configuration flow
EXECUTE IMMEDIATE FROM 'configuration/app_config.sql';
EXECUTE IMMEDIATE FROM 'configuration/connector_configuration.sql';
```

## Components

The sections below contain a list of the connectors native SDK components
with short descriptions and a list of required other components for each of them.
For more information, see [The Snowflake Native SDK for Connectors reference](/developer-guide/native-apps/connector-sdk/reference/overview).

### Core component

The core component is responsible for creating basic objects for the connector like schemas,
roles and persistence layer for the internal status of the application.

#### Dependencies

This component has no dependencies to other components.

### Application configuration component

The application configuration component is a persistence layer for storing and reading
the internal configuration of the application.

#### Dependencies

This component has no dependencies to other components.

### Prerequisites component

Prerequisites are an optional part of the wizard.
It supports informing the end user about configurations and initial setup that needs to be satisfied,
usually outside of the connector itself.

#### Dependencies

- Core component

### Connector configuration component

The connector configuration is a wizard step responsible for configuring common
connector properties like: sink database, data owner role, warehouse etc.

#### Dependencies

- Core component
- Application configuration component

### Connection configuration component

The connection configuration is a wizard step responsible for configuring
the properties related to the communication with the external source system for the connector,
for example authentication and authorization properties and methods.

#### Dependencies

- Core component
- Application configuration component

### Finalize configuration component

The finalize connector is a wizard step responsible for performing final connection checks to the external source system and connector specific configurations.

#### Dependencies

- Core component
- Recommended: Application configuration component

### Pause/resume component

The pause/resume component provides the option of pausing and resuming the connector whenever desired to stop the credit consumption.

#### Dependencies

- Core component
- Recommended: Application configuration component
- Recommended: Finalize configuration component

### Ingestion component

The ingestion component provides abstraction and persistence to define the data that will be put into Snowflake from the external source system.

#### Dependencies

This component has no dependencies to other component, however requires multiple sql files to be executed.

### Scheduler component

The scheduler component allows provides a mechanism of triggering tasks inside a connector
according to the configuration using Snowflake tasks underneath.

#### Dependencies

- Core component
- Application configuration component
- Connector configuration component

### Connector stats component

The connectors stats component provides useful views to see the metadata from the performed ingestion tasks.
It is useful to monitor how much data is flowing through the connector.

#### Dependencies

- Ingestion component

### Sync status component

The sync status component provides a view to quickly check when was the last data sync.

#### Dependencies

- Ingestion component
- Connector stats component

### Task reactor component

The task reactor is a component that provides a mechanism to queue work items and spread them between a number of worker tasks.
The number of workers can be changed to allow for more of them when there are huge workloads.

#### Dependencies

This component has no dependencies to other components.
