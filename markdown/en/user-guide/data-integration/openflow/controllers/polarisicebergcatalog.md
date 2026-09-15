# PolarisIcebergCatalog

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides Apache Iceberg integration with Apache Polaris Catalog access over REST HTTP

## Tags

catalog, iceberg, openflow, polaris

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Access Token Scopes \* | Access Token Scopes | catalog |  | Comma-separated list of one or more OAuth 2 scopes requested for Access Tokens |
| Authentication Strategy \* | Authentication Strategy | OAUTH2 | - Bearer Authentication - OAuth 2.0 | Strategy for authenticating with the Apache Iceberg Catalog over HTTP |
| Authorization Grant Type \* | Authorization Grant Type | CLIENT\_CREDENTIALS | - Client Credentials | OAuth 2.0 Authorization Grant Type for obtaining Access Tokens |
| Authorization Server URI \* | Authorization Server URI |  |  | Authorization Server URI supporting OAuth 2 |
| Bearer Token \* | Bearer Token |  |  | Bearer Token for authentication to Apache Iceberg Catalog |
| Catalog URI \* | Catalog URI |  |  | Apache Iceberg Catalog REST URI |
| Client ID \* | Client ID |  |  | Client ID for OAuth 2 Client Credentials |
| Client Secret \* | Client Secret |  |  | Client Secret for OAuth 2 Client Credentials |
| Warehouse Location | Warehouse Location |  |  | Apache Iceberg Catalog Warehouse location or identifier |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
