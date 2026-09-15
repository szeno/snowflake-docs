# MoveAzureDataLakeStorage 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-azure-nar

## Description

Moves content within an Azure Data Lake Storage Gen 2. After the move, files will be no longer available on source location.

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
| Conflict Resolution Strategy | Indicates what should happen when a file with the same name already exists in the output directory |
| Destination Directory | Name of the Azure Storage Directory where the files will be moved. The Directory Name cannot contain a leading ‘/’. The root directory can be designated by the empty string value. Non-existing directories will be created. If the original directory structure should be kept, the full directory path needs to be provided after the destination directory. e.g.: destdir/${azure.directory} |
| Destination Filesystem | Name of the Azure Storage File System where the files will be moved. |
| File Name | The filename |
| Source Directory | Name of the Azure Storage Directory from where the move should happen. The Directory Name cannot contain a leading ‘/’. The root directory can be designated by the empty string value. |
| Source Filesystem | Name of the Azure Storage File System from where the move should happen. |
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
| azure.source.filesystem | The name of the source Azure File System |
| azure.source.directory | The name of the source Azure Directory |
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
