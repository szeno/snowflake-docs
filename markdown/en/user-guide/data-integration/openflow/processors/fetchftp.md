# FetchFTP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Fetches the content of a file from a remote FTP server and overwrites the contents of an incoming FlowFile with the content of the remote file.

## Tags

fetch, files, ftp, get, ingest, input, remote, retrieve, source

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Completion Strategy | Specifies what to do with the original file on the server once it has been pulled into NiFi. If the Completion Strategy fails, a warning will be logged but the data will still be transferred. |
| Connection Mode | The FTP Connection Mode |
| Connection Timeout | Amount of time to wait before timing out while creating a connection |
| Create Directory | Used when ‘Completion Strategy’ is ‘Move File’. Specifies whether or not the remote directory should be created if it does not exist. |
| Data Timeout | When transferring a file between the local and remote system, this value specifies how long is allowed to elapse without any data being transferred between systems |
| Hostname | The fully-qualified hostname or IP address of the host to fetch the data from |
| Internal Buffer Size | Set the internal buffer size for buffered data streams |
| Log Level When File Not Found | Log level to use in case the file does not exist when the processor is triggered |
| Move Destination Directory | The directory on the remote server to move the original file to once it has been ingested into NiFi. This property is ignored unless the Completion Strategy is set to ‘Move File’. The specified directory must already exist on the remote system if ‘Create Directory’ is disabled, or the rename will fail. |
| Password | Password for the user account |
| Port | The port to connect to on the remote host to fetch the data from |
| Remote File | The fully qualified filename on the remote system |
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
| comms.failure | Any FlowFile that could not be fetched from the remote server due to a communications failure will be transferred to this Relationship. |
| not.found | Any FlowFile for which we receive a ‘Not Found’ message from the remote server will be transferred to this Relationship. |
| permission.denied | Any FlowFile that could not be fetched from the remote server due to insufficient permissions will be transferred to this Relationship. |
| success | All FlowFiles that are received are routed to success |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| ftp.remote.host | The hostname or IP address from which the file was pulled |
| ftp.remote.port | The port that was used to communicate with the remote FTP server |
| ftp.remote.filename | The name of the remote file that was pulled |
| filename | The filename is updated to point to the filename fo the remote file |
| path | If the Remote File contains a directory name, that directory name will be added to the FlowFile using the ‘path’ attribute |
| fetch.failure.reason | The name of the failure relationship applied when routing to any failure relationship |

Expand

Show lessSee more

## Use Cases Involving Other Components

| Retrieve all files in a directory of an FTP Server |
| --- |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.GetFTP](/user-guide/data-integration/openflow/processors/getftp)
- [org.apache.nifi.processors.standard.GetSFTP](/user-guide/data-integration/openflow/processors/getsftp)
- [org.apache.nifi.processors.standard.PutFTP](/user-guide/data-integration/openflow/processors/putftp)
- [org.apache.nifi.processors.standard.PutSFTP](/user-guide/data-integration/openflow/processors/putsftp)
