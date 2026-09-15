# MongoDBControllerService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a controller service that configures a connection to MongoDB and provides access to that connection to other Mongo-related components.

## Tags

mongo, mongodb, service

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Database User | Database User |  |  | Database user name |
| Mongo URI \* | Mongo URI |  |  | MongoURI, typically of the form: mongodb://host1[:port1][,host2[:port2],…] |
| Password | Password |  |  | The password for the database user |
| SSL Context Service | SSL Context Service |  |  | The SSL Context Service used to provide client certificate information for TLS/SSL connections. |
| Write Concern \* | Write Concern | ACKNOWLEDGED | - ACKNOWLEDGED - UNACKNOWLEDGED - FSYNCED - JOURNALED - REPLICA\_ACKNOWLEDGED - MAJORITY - W1 - W2 - W3 | The write concern to use |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
