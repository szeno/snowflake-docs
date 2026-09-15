# AzureStorageCredentialsControllerService\_v12

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides credentials for Azure Storage processors using Azure Storage client library v12.

## Tags

azure, blob, cloud, credentials, microsoft, queue, storage

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Account Key \* | Account Key |  |  | The storage account key. This is an admin-like password providing access to every container in this account. It is recommended one uses Shared Access Signature (SAS) token, Managed Identity or Service Principal instead for fine-grained control with policies. |
| Credentials Type \* | Credentials Type | SAS\_TOKEN | - Account Key - SAS Token - Managed Identity - Service Principal | Credentials type to be used for authenticating to Azure |
| Endpoint Suffix \* | Endpoint Suffix | blob.core.windows.net |  | Storage accounts in public Azure always use a common FQDN suffix. Override this endpoint suffix with a different suffix in certain circumstances (like Azure Stack or non-public Azure regions). |
| Managed Identity Client ID | Managed Identity Client ID |  |  | Client ID of the managed identity. The property is required when User Assigned Managed Identity is used for authentication. It must be empty in case of System Assigned Managed Identity. |
| SAS Token \* | SAS Token |  |  | Shared Access Signature token (the leading ‘?’ may be included) |
| Service Principal Client ID \* | Service Principal Client ID |  |  | Client ID (or Application ID) of the Client/Application having the Service Principal. |
| Service Principal Client Secret \* | Service Principal Client Secret |  |  | Password of the Client/Application. |
| Service Principal Tenant ID \* | Service Principal Tenant ID |  |  | Tenant ID of the Azure Active Directory hosting the Service Principal. |
| Storage Account Name \* | Storage Account Name |  |  | The storage account name. |
| Proxy Configuration Service | proxy-configuration-service |  |  | Specifies the Proxy Configuration Controller Service to proxy network requests. In case of SOCKS, it is not guaranteed that the selected SOCKS Version will be used by the processor. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
