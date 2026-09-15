# FetchSmb 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-smb-nar

## Description

Fetches files from a SMB Share. Designed to be used in tandem with ListSmb.

## Tags

cifs, fetch, files, samba, smb

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Completion Strategy | Specifies what to do with the original file on the server once it has been processed. If the Completion Strategy fails, a warning will be logged but the data will still be transferred. |
| Create Destination Directory | Specifies whether or not the remote directory should be created if it does not exist. |
| Destination Directory | The directory on the remote server to move the original file to once it has been processed. |
| remote-file | The full path of the file to be retrieved from the remote server. Expression language is supported. |
| smb-client-provider-service | Specifies the SMB client provider to use for creating SMB connections. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | A FlowFile will be routed here when failed to fetch its content. |
| success | A FlowFile will be routed here for each successfully fetched file. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| error.code | The error code returned by SMB when the fetch of a file fails. |
| error.message | The error message returned by SMB when the fetch of a file fails. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.smb.GetSmbFile](/user-guide/data-integration/openflow/processors/getsmbfile)
- [org.apache.nifi.processors.smb.ListSmb](/user-guide/data-integration/openflow/processors/listsmb)
- [org.apache.nifi.processors.smb.PutSmbFile](/user-guide/data-integration/openflow/processors/putsmbfile)
