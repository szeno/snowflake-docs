# GetFTP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Fetches files from an FTP Server and creates FlowFiles from them

## Tags

FTP, fetch, files, get, ingest, input, remote, retrieve, source

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Connection Mode | The FTP Connection Mode |
| Connection Timeout | Amount of time to wait before timing out while creating a connection |
| Data Timeout | When transferring a file between the local and remote system, this value specifies how long is allowed to elapse without any data being transferred between systems |
| Delete Original | Determines whether or not the file is deleted from the remote system after it has been successfully transferred |
| File Filter Regex | Provides a Java Regular Expression for filtering Filenames; if a filter is supplied, only files whose names match that Regular Expression will be fetched |
| Follow Symbolic Links | If true, will pull even symbolic files and also nested symbolic subdirectories; otherwise, will not read symbolic files and will not traverse symbolic link subdirectories |
| Hostname | The fully qualified hostname or IP address of the remote system |
| Ignore Dotted Files | If true, files whose names begin with a dot (“.”) will be ignored |
| Internal Buffer Size | Set the internal buffer size for buffered data streams |
| Max Selects | The maximum number of files to pull in a single connection |
| Password | Password for the user account |
| Path Filter Regex | When Search Recursively is true, then only subdirectories whose path matches the given Regular Expression will be scanned |
| Polling Interval | Determines how long to wait between fetching the listing for new files |
| Port | The port that the remote system is listening on for file transfers |
| Remote Path | The path on the remote system from which to pull or push files |
| Remote Poll Batch Size | The value specifies how many file paths to find in a given directory on the remote system when doing a file listing. This value in general should not need to be modified but when polling against a remote system with a tremendous number of files this value can be critical. Setting this value too high can result very poor performance and setting it too low can cause the flow to be slower than normal. |
| Search Recursively | If true, will pull files from arbitrarily nested subdirectories; otherwise, will not traverse subdirectories |
| Transfer Mode | The FTP Transfer Mode |
| Use Natural Ordering | If true, will pull files in the order in which they are naturally listed; otherwise, the order in which the files will be pulled is not defined |
| Username | Username |
| ftp-use-utf8 | Tells the client to use UTF-8 encoding when processing files and filenames. If set to true, the server must also support UTF-8 encoding. |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | All FlowFiles that are received are routed to success |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| filename | The filename is set to the name of the file on the remote server |
| path | The path is set to the path of the file’s directory on the remote server. For example, if the <Remote Path> property is set to /tmp, files picked up from /tmp will have the path attribute set to /tmp. If the <Search Recursively> property is set to true and a file is picked up from /tmp/abc/1/2/3, then the path attribute will be set to /tmp/abc/1/2/3 |
| file.lastModifiedTime | The date and time that the source file was last modified |
| file.lastAccessTime | The date and time that the file was last accessed. May not work on all file systems |
| file.owner | The numeric owner id of the source file |
| file.group | The numeric group id of the source file |
| file.permissions | The read/write/execute permissions of the source file |
| absolute.path | The full/absolute path from where a file was picked up. The current ‘path’ attribute is still populated, but may be a relative path |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.PutFTP](/user-guide/data-integration/openflow/processors/putftp)
