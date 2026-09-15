# PutFTP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Sends FlowFiles to an FTP Server

## Tags

archive, copy, egress, files, ftp, put, remote

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Batch Size | The maximum number of FlowFiles to send in a single connection |
| Conflict Resolution | Determines how to handle the problem of filename collisions |
| Connection Mode | The FTP Connection Mode |
| Connection Timeout | Amount of time to wait before timing out while creating a connection |
| Create Directory | Specifies whether or not the remote directory should be created if it does not exist. |
| Data Timeout | When transferring a file between the local and remote system, this value specifies how long is allowed to elapse without any data being transferred between systems |
| Dot Rename | If true, then the filename of the sent file is prepended with a “.” and then renamed back to the original once the file is completely sent. Otherwise, there is no rename. This property is ignored if the Temporary Filename property is set. |
| Hostname | The fully qualified hostname or IP address of the remote system |
| Internal Buffer Size | Set the internal buffer size for buffered data streams |
| Last Modified Time | The lastModifiedTime to assign to the file after transferring it. If not set, the lastModifiedTime will not be changed. Format must be yyyy-MM-dd ‘T’HH:mm:ssZ. You may also use expression language such as ${file.lastModifiedTime}. If the value is invalid, the processor will not be invalid but will fail to change lastModifiedTime of the file. |
| Password | Password for the user account |
| Permissions | The permissions to assign to the file after transferring it. Format must be either UNIX rwxrwxrwx with a - in place of denied permissions (e.g. rw-r–r–) or an octal number (e.g. 644). If not set, the permissions will not be changed. You may also use expression language such as ${file.permissions}. If the value is invalid, the processor will not be invalid but will fail to change permissions of the file. |
| Port | The port that the remote system is listening on for file transfers |
| Reject Zero-Byte Files | Determines whether or not Zero-byte files should be rejected without attempting to transfer |
| Remote Path | The path on the remote system from which to pull or push files |
| Temporary Filename | If set, the filename of the sent file will be equal to the value specified during the transfer and after successful completion will be renamed to the original filename. If this value is set, the Dot Rename property is ignored. |
| Transfer Mode | The FTP Transfer Mode |
| Use Compression | Indicates whether or not ZLIB compression should be used when transferring files |
| Username | Username |
| ftp-use-utf8 | Tells the client to use UTF-8 encoding when processing files and filenames. If set to true, the server must also support UTF-8 encoding. |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that failed to send to the remote system; failure is usually looped back to this processor |
| reject | FlowFiles that were rejected by the destination system |
| success | FlowFiles that are successfully sent will be routed to success |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.GetFTP](/user-guide/data-integration/openflow/processors/getftp)
