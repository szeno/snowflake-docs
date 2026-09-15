# FetchAzureDataLakeStorage 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-azure-nar

## Description

Fetch the specified file from Azure Data Lake Storage

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
| Number of Retries | The number of automatic retries to perform if the download fails. |
| Range Length | The number of bytes to download from the object, starting from the Range Start. An empty value or a value that extends beyond the end of the object will read to the end of the object. |
| Range Start | The byte position at which to start reading from the object. An empty value or a value of zero will start reading at the beginning of the object. |
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

## Writes attributes

| Name | Description |
| --- | --- |
| azure.datalake.storage.statusCode | The HTTP error code (if available) from the failed operation |
| azure.datalake.storage.errorCode | The Azure Data Lake Storage moniker of the failed operation |
| azure.datalake.storage.errorMessage | The Azure Data Lake Storage error message from the failed operation |

Expand

Show lessSee more

## Use Cases Involving Other Components

| Retrieve all files in an Azure DataLake Storage directory |
| --- |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.azure.storage.DeleteAzureDataLakeStorage](/user-guide/data-integration/openflow/processors/deleteazuredatalakestorage)
- [org.apache.nifi.processors.azure.storage.ListAzureDataLakeStorage](/user-guide/data-integration/openflow/processors/listazuredatalakestorage)
- [org.apache.nifi.processors.azure.storage.PutAzureDataLakeStorage](/user-guide/data-integration/openflow/processors/putazuredatalakestorage)
