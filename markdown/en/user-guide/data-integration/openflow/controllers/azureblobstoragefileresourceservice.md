# AzureBlobStorageFileResourceService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides an Azure Blob Storage file resource for other components.

## Tags

azure, blob, cloud, file, microsoft, resource, storage

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Blob Name \* | Blob Name | ${azure.blobname} |  | The full name of the blob |
| Container Name \* | Container Name | ${azure.container} |  | Name of the Azure storage container. In case of PutAzureBlobStorage processor, container can be created if it does not exist. |
| Storage Credentials \* | Storage Credentials |  |  | Controller Service used to obtain Azure Blob Storage Credentials. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
