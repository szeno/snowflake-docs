# StandardDatabricksWorkspaceClientService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Databricks client.

## Tags

databricks, openflow

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Authentication Method \* | Authentication Method | OAUTH\_M2M | - OAuth M2M - PAT | Method to authenticate with Databricks |
| OAuth Client ID \* | OAuth Client ID |  |  | Databricks OAuth Client ID, also known as an application ID |
| OAuth Client Secret \* | OAuth Client Secret |  |  | Databricks Service Principal’s OAuth Client Secret. |
| Personal Access Token \* | Personal Access Token |  |  | Databricks Personal Access Token |
| Workspace ID \* | Workspace ID |  |  | Databricks Workspace ID |
| Proxy Configuration Service | proxy-configuration-service |  |  | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
