# GetSmbFile 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-smb-nar

## Description

Reads file from a samba network location to FlowFiles. Use this processor instead of a cifs mounts if share access control is important. Configure the Hostname, Share and Directory accordingly: [Hostname][Share][pathtoDirectory]

## Tags

samba, smb, cifs, files, get

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Batch Size | The maximum number of files to pull in each iteration |
| Directory | The network folder to which files should be written. This is the remaining relative path after the share: \hostnameshare[dir1dir2]. |
| Domain | The domain used for authentication. Optional, in most cases username and password is sufficient. |
| File Filter | Only files whose names match the given regular expression will be picked up |
| Hostname | The network host to which files should be written. |
| Ignore Hidden Files | Indicates whether or not hidden files should be ignored |
| Keep Source File | If true, the file is not deleted after it has been copied to the Content Repository; this causes the file to be picked up continually and is useful for testing purposes. If not keeping original NiFi will need write permissions on the directory it is pulling from otherwise it will ignore the file. |
| Password | The password used for authentication. Required if Username is set. |
| Path Filter | When Recurse Subdirectories is true, then only subdirectories whose path matches the given regular expression will be scanned |
| Polling Interval | Indicates how long to wait before performing a directory listing |
| Recurse Subdirectories | Indicates whether or not to pull files from subdirectories |
| Share | The network share to which files should be written. This is the “first folder”after the hostname: \hostname[share]dir1dir2 |
| Share Access Strategy | Indicates which shared access are granted on the file during the read. None is the most restrictive, but the safest setting to prevent corruption. |
| Username | The username used for authentication. If no username is set then anonymous authentication is attempted. |
| enable-dfs | Enables accessing Distributed File System (DFS) and following DFS links during SMB operations. |
| smb-dialect | The SMB dialect is negotiated between the client and the server by default to the highest common version supported by both end. In some rare cases, the client-server communication may fail with the automatically negotiated dialect. This property can be used to set the dialect explicitly (e.g. to downgrade to a lower version), when those situations would occur. |
| timeout | Timeout for read and write operations. |
| use-encryption | Turns on/off encrypted communication between the client and the server. The property’s behavior is SMB dialect dependent: SMB 2.x does not support encryption and the property has no effect. In case of SMB 3.x, it is a hint/request to the server to turn encryption on if the server also supports it. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | All files are routed to success |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| filename | The filename is set to the name of the file on the network share |
| path | The path is set to the relative path of the file’s network share name. For example, if the input is set to \hostnamesharetmp, files picked up from tmp will have the path attribute set to tmp |
| file.creationTime | The date and time that the file was created. May not work on all file systems |
| file.lastModifiedTime | The date and time that the file was last modified. May not work on all file systems |
| file.lastAccessTime | The date and time that the file was last accessed. May not work on all file systems |
| absolute.path | The full path from where a file was picked up. This includes the hostname and the share name |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.smb.FetchSmb](/user-guide/data-integration/openflow/processors/fetchsmb)
- [org.apache.nifi.processors.smb.ListSmb](/user-guide/data-integration/openflow/processors/listsmb)
- [org.apache.nifi.processors.smb.PutSmbFile](/user-guide/data-integration/openflow/processors/putsmbfile)
