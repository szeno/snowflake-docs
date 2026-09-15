# DeleteAzureDataLakeStorage 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-azure-nar

## Description

Deletes the provided file from Azure Data Lake Storage

## Tags

adlsgen2, azure, cloud, datalake, microsoft, storage

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| ADLS Credentials | Controller Service used to obtain Azure Credentials. |
| Directory Name | Name of the Azure Storage Directory. The Directory Name cannot contain a leading ‘/’. The root directory can be designated by the empty string value. In case of the PutAzureDataLakeStorage processor, the directory will be created if not already existing. |
| File Name | The filename |
| Filesystem Name | Name of the Azure Storage File System (also called Container). It is assumed to be already existing. |
| Filesystem Object Type | They type of the file system object to be deleted. It can be either folder or file. |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. In case of SOCKS, it is not guaranteed that the selected SOCKS Version will be used by the processor. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Files that could not be written to Azure storage for some reason are transferred to this relationship |
| success | Files that have been successfully written to Azure storage are transferred to this relationship |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.azure.storage.FetchAzureDataLakeStorage](/user-guide/data-integration/openflow/processors/fetchazuredatalakestorage)
- [org.apache.nifi.processors.azure.storage.ListAzureDataLakeStorage](/user-guide/data-integration/openflow/processors/listazuredatalakestorage)
- [org.apache.nifi.processors.azure.storage.PutAzureDataLakeStorage](/user-guide/data-integration/openflow/processors/putazuredatalakestorage)
