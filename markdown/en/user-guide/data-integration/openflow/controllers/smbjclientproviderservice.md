# SmbjClientProviderService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides access to SMB Sessions with shared authentication credentials.

## Tags

samba, smb, cifs, files

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Domain | domain |  |  | The domain used for authentication. Optional, in most cases username and password is sufficient. |
| Enable DFS \* | enable-dfs | false | - true - false | Enables accessing Distributed File System (DFS) and following DFS links during SMB operations. |
| Hostname \* | hostname |  |  | The network host of the SMB file server. |
| Password | password |  |  | The password used for authentication. |
| Port \* | port | 445 |  | Port to use for connection. |
| Share \* | share |  |  | The network share to which files should be listed from. This is the “first folder”after the hostname: [smb://hostname:port/[share]/dir1/dir2](smb://hostname:port/%5Bshare%5D/dir1/dir2) |
| SMB Dialect \* | smb-dialect | AUTO | - AUTO - SMB 2.0.2 - SMB 2.1 - SMB 3.0 - SMB 3.0.2 - SMB 3.1.1 | The SMB dialect is negotiated between the client and the server by default to the highest common version supported by both end. In some rare cases, the client-server communication may fail with the automatically negotiated dialect. This property can be used to set the dialect explicitly (e.g. to downgrade to a lower version), when those situations would occur. |
| Timeout \* | timeout | 5 sec |  | Timeout for read and write operations. |
| Use Encryption \* | use-encryption | false | - true - false | Turns on/off encrypted communication between the client and the server. The property’s behavior is SMB dialect dependent: SMB 2.x does not support encryption and the property has no effect. In case of SMB 3.x, it is a hint/request to the server to turn encryption on if the server also supports it. |
| Username | username | Guest |  | The username used for authentication. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
