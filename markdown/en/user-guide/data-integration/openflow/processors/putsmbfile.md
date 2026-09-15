# PutSmbFile 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-smb-nar

## Description

Writes the contents of a FlowFile to a samba network location. Use this processor instead of a cifs mounts if share access control is important. Configure the Hostname, Share and Directory accordingly: [Hostname][Share][pathtoDirectory]

## Tags

samba, smb, cifs, files, put

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Batch Size | The maximum number of files to put in each iteration |
| Conflict Resolution Strategy | Indicates what should happen when a file with the same name already exists in the output directory |
| Create Missing Directories | If true, then missing destination directories will be created. If false, flowfiles are penalized and sent to failure. |
| Directory | The network folder to which files should be written. This is the remaining relative path after the share: \hostnameshare[dir1dir2]. You may use expression language. |
| Domain | The domain used for authentication. Optional, in most cases username and password is sufficient. |
| Hostname | The network host to which files should be written. |
| Password | The password used for authentication. Required if Username is set. |
| Share | The network share to which files should be written. This is the “first folder”after the hostname: \hostname[share]dir1dir2 |
| Share Access Strategy | Indicates which shared access are granted on the file during the write. None is the most restrictive, but the safest setting to prevent corruption. |
| Temporary Suffix | A temporary suffix which will be appended to the filename while it’s transferring. After the transfer is complete, the suffix will be removed. |
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
| failure | Files that could not be written to the output network path for some reason are transferred to this relationship |
| success | Files that have been successfully written to the output network path are transferred to this relationship |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.smb.FetchSmb](/user-guide/data-integration/openflow/processors/fetchsmb)
- [org.apache.nifi.processors.smb.GetSmbFile](/user-guide/data-integration/openflow/processors/getsmbfile)
- [org.apache.nifi.processors.smb.ListSmb](/user-guide/data-integration/openflow/processors/listsmb)
