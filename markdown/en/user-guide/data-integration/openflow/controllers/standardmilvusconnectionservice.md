# StandardMilvusConnectionService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides connection service to a Milvus instance

## Tags

connection, database, milvus, openflow, vector

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| API Key \* | API Key |  |  | Milvus API Key for authenticating connections |
| Authentication Strategy \* | Authentication Strategy | PASSWORD | - Password - API Key | Strategy for authenticating Milvus connections |
| Connection Timeout \* | Connection Timeout | 30 seconds |  | Maximum amount of time to wait for a connection from a reusable pool |
| Idle Timeout \* | Idle Timeout | 10 minutes |  | Maximum amount of time for a connection to remain idle in a reusable pool |
| Password \* | Password |  |  | Milvus password for authenticating connections |
| SSL Context Service | SSL Context Service |  |  | The SSL Context Service used to provide client certificate information for TLS/SSL connections. |
| Service URI \* | Service URI |  |  | The URI to use to communicate with Milvus |
| User \* | User |  |  | Milvus username for authenticating connections |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
