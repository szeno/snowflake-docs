# StandardKustoQueryService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Standard implementation of Kusto Query Service for Azure Data Explorer

## Tags

ADX, Azure, Data, Explorer, Kusto

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Application Client ID \* | Application Client ID |  |  | Azure Data Explorer Application Client Identifier for Authentication |
| Application Key \* | Application Key |  |  | Azure Data Explorer Application Key for Authentication |
| Application Tenant ID \* | Application Tenant ID |  |  | Azure Data Explorer Application Tenant Identifier for Authentication |
| Authentication Strategy \* | Authentication Strategy | MANAGED\_IDENTITY | - Application Credentials - Managed Identity - Azure CLI (Dev Only) | Authentication method for access to Azure Data Explorer |
| Cluster URI \* | Cluster URI |  |  | Azure Data Explorer Cluster URI |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
