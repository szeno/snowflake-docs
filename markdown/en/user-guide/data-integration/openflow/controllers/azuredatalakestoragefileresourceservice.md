# AzureDataLakeStorageFileResourceService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides an Azure Data Lake Storage (ADLS) file resource for other components.

## Tags

adlsgen2, azure, cloud, datalake, file, microsoft, resource, storage

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| ADLS Credentials \* | ADLS Credentials |  |  | Controller Service used to obtain Azure Credentials. |
| Directory Name \* | Directory Name | ${azure.directory} |  | Name of the Azure Storage Directory. The Directory Name cannot contain a leading ‘/’. The root directory can be designated by the empty string value. In case of the PutAzureDataLakeStorage processor, the directory will be created if not already existing. |
| File Name \* | File Name | ${azure.filename} |  | The filename |
| Filesystem Name \* | Filesystem Name | ${azure.filesystem} |  | Name of the Azure Storage File System (also called Container). It is assumed to be already existing. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
