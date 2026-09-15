# PutAzureDataLakeStorage 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-azure-nar

## Description

Writes the contents of a FlowFile as a file on Azure Data Lake Storage Gen 2

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
| Base Temporary Path | The Path where the temporary directory will be created. The Path name cannot contain a leading ‘/’. The root directory can be designated by the empty string value. Non-existing directories will be created. The Temporary File Directory name is \_nifitempdirectory |
| Conflict Resolution Strategy | Indicates what should happen when a file with the same name already exists in the output directory |
| Directory Name | Name of the Azure Storage Directory. The Directory Name cannot contain a leading ‘/’. The root directory can be designated by the empty string value. In case of the PutAzureDataLakeStorage processor, the directory will be created if not already existing. |
| File Name | The filename |
| File Resource Service | File Resource Service providing access to the local resource to be transferred |
| Filesystem Name | Name of the Azure Storage File System (also called Container). It is assumed to be already existing. |
| Resource Transfer Source | The source of the content to be transferred |
| Writing Strategy | Defines the approach for writing the Azure file. |
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
| azure.filesystem | The name of the Azure File System |
| azure.directory | The name of the Azure Directory |
| azure.filename | The name of the Azure File |
| azure.primaryUri | Primary location for file content |
| azure.length | The length of the Azure File |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.azure.storage.DeleteAzureDataLakeStorage](/user-guide/data-integration/openflow/processors/deleteazuredatalakestorage)
- [org.apache.nifi.processors.azure.storage.FetchAzureDataLakeStorage](/user-guide/data-integration/openflow/processors/fetchazuredatalakestorage)
- [org.apache.nifi.processors.azure.storage.ListAzureDataLakeStorage](/user-guide/data-integration/openflow/processors/listazuredatalakestorage)
