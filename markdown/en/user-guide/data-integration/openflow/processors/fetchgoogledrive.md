# FetchGoogleDrive 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-gcp-nar

## Description

Fetches files from a Google Drive Folder. Designed to be used in tandem with ListGoogleDrive. Please see Additional Details to set up access to Google Drive.

## Tags

drive, fetch, google, storage

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Google Doc Export Type | Google Documents cannot be downloaded directly from Google Drive but instead must be exported to a specified MIME Type. In the event that the incoming FlowFile’s MIME Type indicates that the file is a Google Document, this property specifies the MIME Type to export the document to. |
| Google Drawing Export Type | Google Drawings cannot be downloaded directly from Google Drive but instead must be exported to a specified MIME Type. In the event that the incoming FlowFile’s MIME Type indicates that the file is a Google Drawing, this property specifies the MIME Type to export the drawing to. |
| Google Presentation Export Type | Google Presentations cannot be downloaded directly from Google Drive but instead must be exported to a specified MIME Type. In the event that the incoming FlowFile’s MIME Type indicates that the file is a Google Presentation, this property specifies the MIME Type to export the presentation to. |
| Google Spreadsheet Export Type | Google Spreadsheets cannot be downloaded directly from Google Drive but instead must be exported to a specified MIME Type. In the event that the incoming FlowFile’s MIME Type indicates that the file is a Google Spreadsheet, this property specifies the MIME Type to export the spreadsheet to. |
| connect-timeout | Maximum wait time for connection to Google Drive service. |
| drive-file-id | The Drive ID of the File to fetch. Please see Additional Details for information on how to obtain the Drive ID. |
| gcp-credentials-provider-service | The Controller Service used to obtain Google Cloud Platform credentials. |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |
| read-timeout | Maximum wait time for response from Google Drive service. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | A FlowFile will be routed here for each File for which fetch was attempted but failed. |
| success | A FlowFile will be routed here for each successfully fetched File. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| drive.id | The id of the file |
| filename | The name of the file |
| mime.type | The MIME type of the file |
| drive.size | The size of the file. Set to 0 when the file size is not available (e.g. externally stored files). |
| drive.size.available | Indicates if the file size is known / available |
| drive.timestamp | The last modified time or created time (whichever is greater) of the file. The reason for this is that the original modified date of a file is preserved when uploaded to Google Drive. ‘Created time’ takes the time when the upload occurs. However uploaded files can still be modified later. |
| drive.created.time | The file’s creation time |
| drive.modified.time | The file’s last modification time |
| drive.owner | The owner of the file |
| drive.last.modifying.user | The last modifying user of the file |
| drive.web.view.link | Web view link to the file |
| drive.web.content.link | Web content link to the file |
| drive.parent.folder.id | The id of the file’s parent folder |
| drive.parent.folder.name | The name of the file’s parent folder |
| drive.shared.drive.id | The id of the shared drive (if the file is located on a shared drive) |
| drive.shared.drive.name | The name of the shared drive (if the file is located on a shared drive) |
| error.code | The error code returned by Google Drive |
| error.message | The error message returned by Google Drive |

Expand

Show lessSee more

## Use Cases Involving Other Components

| Retrieve all files in a Google Drive folder |
| --- |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.gcp.drive.ListGoogleDrive](/user-guide/data-integration/openflow/processors/listgoogledrive)
- [org.apache.nifi.processors.gcp.drive.PutGoogleDrive](/user-guide/data-integration/openflow/processors/putgoogledrive)
