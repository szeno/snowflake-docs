# FetchSharepointFile 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-msgraph-nar

## Description

Fetches the contents of a file from a Sharepoint Drive, optionally downloading a PDF or HTML version of the file when applicable. Any FlowFile that represents a Sharepoint folder will be routed to success without fetching contents.

## Tags

cdc, document, graph, microsoft, openflow, sharepoint, unstructured

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Authentication Service | The service that provides authentication for the SharePoint API |
| Download PDF/HTML Version | Sharepoint supports automatically converting certain file formats to PDF or HTML. If this property is set to *true*, the Processor will inspect the FlowFile’s filename extension to determine if the file can be converted to PDF or HTML. If the file can be converted, the Processor will download the converted version. If the file cannot be converted, the Processor will download the original file. If this property is set to *false*, the Processor will always download the original file. |
| Drive ID | The ID of the drive that contains the file to fetch |
| Fallback Retry Duration | The time to wait before retrying the operation after a communication failure. This value is used when the response doesn’t contain a Retry-After header. |
| Item ID | The ID of the item to fetch |
| Update Extension | If true, the Processor will update the filename extension to match the format of the downloaded file |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| comms.failure | A FlowFile is routed here if the processor failed to communicate with the Graph API. Can be retried |
| failure | An incoming FlowFile is routed to this relationship if the contents of the item could not be fetched |
| not.found | A FlowFile is routed here if the item was not found |
| success | An incoming FlowFile is routed to this relationship after the contents of the item have been fetched and written to the FlowFile |

Expand

Show lessSee more

## Use Cases Involving Other Components

| Fetch a file from Sharepoint by the Site URL, Drive Name and file path. |
| --- |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.sharepoint.CaptureSharepointChanges](/user-guide/data-integration/openflow/processors/capturesharepointchanges)
