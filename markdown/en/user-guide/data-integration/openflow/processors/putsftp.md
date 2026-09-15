# PutSFTP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Sends FlowFiles to an SFTP Server

## Tags

archive, copy, egress, files, put, remote, sftp

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Algorithm Negotiation | Configuration strategy for SSH algorithm negotiation |
| Batch Size | The maximum number of FlowFiles to send in a single connection |
| Ciphers Allowed | A comma-separated list of Ciphers allowed for SFTP connections. Leave unset to allow all. Available options are: 3des-cbc, aes128-cbc, aes128-ctr, [aes128-gcm@openssh.com](mailto:aes128-gcm@openssh.com), aes192-cbc, aes192-ctr, aes256-cbc, aes256-ctr, [aes256-gcm@openssh.com](mailto:aes256-gcm@openssh.com), arcfour128, arcfour256, blowfish-cbc, [chacha20-poly1305@openssh.com](mailto:chacha20-poly1305@openssh.com), none |
| Conflict Resolution | Determines how to handle the problem of filename collisions |
| Connection Timeout | Amount of time to wait before timing out while creating a connection |
| Create Directory | Specifies whether or not the remote directory should be created if it does not exist. |
| Data Timeout | When transferring a file between the local and remote system, this value specifies how long is allowed to elapse without any data being transferred between systems |
| Disable Directory Listing | If set to ‘true’, directory listing is not performed prior to create missing directories. By default, this processor executes a directory listing command to see target directory existence before creating missing directories. However, there are situations that you might need to disable the directory listing such as the following. Directory listing might fail with some permission setups (e.g. chmod 100) on a directory. Also, if any other SFTP client created the directory after this processor performed a listing and before a directory creation request by this processor is finished, then an error is returned because the directory already exists. |
| Dot Rename | If true, then the filename of the sent file is prepended with a “.” and then renamed back to the original once the file is completely sent. Otherwise, there is no rename. This property is ignored if the Temporary Filename property is set. |
| Host Key File | If supplied, the given file will be used as the Host Key; otherwise, if ‘Strict Host Key Checking’ property is applied (set to true) then uses the ‘known\_hosts’ and ‘known\_hosts2’ files from ~/.ssh directory else no host key file will be used |
| Hostname | The fully qualified hostname or IP address of the remote system |
| Key Algorithms Allowed | A comma-separated list of Key Algorithms allowed for SFTP connections. Leave unset to allow all. Available options are: ecdsa-sha2-nistp256, [ecdsa-sha2-nistp256-cert-v01@openssh.com](mailto:ecdsa-sha2-nistp256-cert-v01@openssh.com), ecdsa-sha2-nistp384, [ecdsa-sha2-nistp384-cert-v01@openssh.com](mailto:ecdsa-sha2-nistp384-cert-v01@openssh.com), ecdsa-sha2-nistp521, [ecdsa-sha2-nistp521-cert-v01@openssh.com](mailto:ecdsa-sha2-nistp521-cert-v01@openssh.com), rsa-sha2-256, [rsa-sha2-256-cert-v01@openssh.com](mailto:rsa-sha2-256-cert-v01@openssh.com), rsa-sha2-512, [rsa-sha2-512-cert-v01@openssh.com](mailto:rsa-sha2-512-cert-v01@openssh.com), [sk-ecdsa-sha2-nistp256@openssh.com](mailto:sk-ecdsa-sha2-nistp256@openssh.com), [sk-ssh-ed25519@openssh.com](mailto:sk-ssh-ed25519@openssh.com), ssh-dss, [ssh-dss-cert-v01@openssh.com](mailto:ssh-dss-cert-v01@openssh.com), ssh-ed25519, [ssh-ed25519-cert-v01@openssh.com](mailto:ssh-ed25519-cert-v01@openssh.com), ssh-rsa, [ssh-rsa-cert-v01@openssh.com](mailto:ssh-rsa-cert-v01@openssh.com) |
| Key Exchange Algorithms Allowed | A comma-separated list of Key Exchange Algorithms allowed for SFTP connections. Leave unset to allow all. Available options are: curve25519-sha256, [curve25519-sha256@libssh.org](mailto:curve25519-sha256@libssh.org), curve448-sha512, diffie-hellman-group-exchange-sha1, diffie-hellman-group-exchange-sha256, diffie-hellman-group1-sha1, diffie-hellman-group14-sha1, diffie-hellman-group14-sha256, diffie-hellman-group15-sha512, diffie-hellman-group16-sha512, diffie-hellman-group17-sha512, diffie-hellman-group18-sha512, ecdh-sha2-nistp256, ecdh-sha2-nistp384, ecdh-sha2-nistp521, mlkem1024nistp384-sha384, mlkem768nistp256-sha256, mlkem768x25519-sha256, sntrup761x25519-sha512, [sntrup761x25519-sha512@openssh.com](mailto:sntrup761x25519-sha512@openssh.com) |
| Last Modified Time | The lastModifiedTime to assign to the file after transferring it. If not set, the lastModifiedTime will not be changed. Format must be yyyy-MM-dd ‘T’HH:mm:ssZ. You may also use expression language such as ${file.lastModifiedTime}. If the value is invalid, the processor will not be invalid but will fail to change lastModifiedTime of the file. |
| Message Authentication Codes Allowed | A comma-separated list of Message Authentication Codes allowed for SFTP connections. Leave unset to allow all. Available options are: hmac-md5, hmac-md5-96, hmac-sha1, hmac-sha1-96, [hmac-sha1-etm@openssh.com](mailto:hmac-sha1-etm@openssh.com), hmac-sha2-256, [hmac-sha2-256-etm@openssh.com](mailto:hmac-sha2-256-etm@openssh.com), hmac-sha2-512, [hmac-sha2-512-etm@openssh.com](mailto:hmac-sha2-512-etm@openssh.com) |
| Password | Password for the user account |
| Permissions | The permissions to assign to the file after transferring it. Format must be either UNIX rwxrwxrwx with a - in place of denied permissions (e.g. rw-r–r–) or an octal number (e.g. 644). If not set, the permissions will not be changed. You may also use expression language such as ${file.permissions}. If the value is invalid, the processor will not be invalid but will fail to change permissions of the file. |
| Port | The port that the remote system is listening on for file transfers |
| Private Key Passphrase | Password for the private key |
| Private Key Path | The fully qualified path to the Private Key file |
| Reject Zero-Byte Files | Determines whether or not Zero-byte files should be rejected without attempting to transfer |
| Remote Group | Integer value representing the Group ID to set on the file after transferring it. If not set, the group will not be set. You may also use expression language such as ${file.group}. If the value is invalid, the processor will not be invalid but will fail to change the group of the file. |
| Remote Owner | Integer value representing the User ID to set on the file after transferring it. If not set, the owner will not be set. You may also use expression language such as ${file.owner}. If the value is invalid, the processor will not be invalid but will fail to change the owner of the file. |
| Remote Path | The path on the remote system from which to pull or push files |
| Send Keep Alive On Timeout | Send a Keep Alive message every 5 seconds up to 5 times for an overall timeout of 25 seconds. |
| Strict Host Key Checking | Indicates whether or not strict enforcement of hosts keys should be applied |
| Temporary Filename | If set, the filename of the sent file will be equal to the value specified during the transfer and after successful completion will be renamed to the original filename. If this value is set, the Dot Rename property is ignored. |
| Use Compression | Indicates whether or not ZLIB compression should be used when transferring files |
| Username | Username |
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

- [org.apache.nifi.processors.standard.GetSFTP](/user-guide/data-integration/openflow/processors/getsftp)
