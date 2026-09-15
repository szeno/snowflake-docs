# StandardAzureCredentialsControllerService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provide credentials to use with an Azure client.

## Tags

azure, credentials, provider, security, session

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Credential Configuration Strategy \* | Credential Configuration Strategy | default-credential | - Default Credential - Managed Identity |  |
| Managed Identity Client ID | Managed Identity Client ID |  |  | Client ID of the managed identity. The property is required when User Assigned Managed Identity is used for authentication. It must be empty in case of System Assigned Managed Identity. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
