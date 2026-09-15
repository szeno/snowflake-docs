# DeleteSFTP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Deletes a file residing on an SFTP server.

## Tags

delete, remote, remove, sftp

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
| Connection Timeout | Amount of time to wait before timing out while creating a connection |
| Data Timeout | When transferring a file between the local and remote system, this value specifies how long is allowed to elapse without any data being transferred between systems |
| Directory Path | The path to the directory the file to delete is located in. |
| Filename | The name of the file to delete. |
| Host Key File | If supplied, the given file will be used as the Host Key; otherwise, if ‘Strict Host Key Checking’ property is applied (set to true) then uses the ‘known\_hosts’ and ‘known\_hosts2’ files from ~/.ssh directory else no host key file will be used |
| Hostname | The fully qualified hostname or IP address of the remote system |
| Key Algorithms Allowed | A comma-separated list of Key Algorithms allowed for SFTP connections. Leave unset to allow all. Available options are: ecdsa-sha2-nistp256, [ecdsa-sha2-nistp256-cert-v01@openssh.com](mailto:ecdsa-sha2-nistp256-cert-v01@openssh.com), ecdsa-sha2-nistp384, [ecdsa-sha2-nistp384-cert-v01@openssh.com](mailto:ecdsa-sha2-nistp384-cert-v01@openssh.com), ecdsa-sha2-nistp521, [ecdsa-sha2-nistp521-cert-v01@openssh.com](mailto:ecdsa-sha2-nistp521-cert-v01@openssh.com), rsa-sha2-256, [rsa-sha2-256-cert-v01@openssh.com](mailto:rsa-sha2-256-cert-v01@openssh.com), rsa-sha2-512, [rsa-sha2-512-cert-v01@openssh.com](mailto:rsa-sha2-512-cert-v01@openssh.com), [sk-ecdsa-sha2-nistp256@openssh.com](mailto:sk-ecdsa-sha2-nistp256@openssh.com), [sk-ssh-ed25519@openssh.com](mailto:sk-ssh-ed25519@openssh.com), ssh-dss, [ssh-dss-cert-v01@openssh.com](mailto:ssh-dss-cert-v01@openssh.com), ssh-ed25519, [ssh-ed25519-cert-v01@openssh.com](mailto:ssh-ed25519-cert-v01@openssh.com), ssh-rsa, [ssh-rsa-cert-v01@openssh.com](mailto:ssh-rsa-cert-v01@openssh.com) |
| Key Exchange Algorithms Allowed | A comma-separated list of Key Exchange Algorithms allowed for SFTP connections. Leave unset to allow all. Available options are: curve25519-sha256, [curve25519-sha256@libssh.org](mailto:curve25519-sha256@libssh.org), curve448-sha512, diffie-hellman-group-exchange-sha1, diffie-hellman-group-exchange-sha256, diffie-hellman-group1-sha1, diffie-hellman-group14-sha1, diffie-hellman-group14-sha256, diffie-hellman-group15-sha512, diffie-hellman-group16-sha512, diffie-hellman-group17-sha512, diffie-hellman-group18-sha512, ecdh-sha2-nistp256, ecdh-sha2-nistp384, ecdh-sha2-nistp521, mlkem1024nistp384-sha384, mlkem768nistp256-sha256, mlkem768x25519-sha256, sntrup761x25519-sha512, [sntrup761x25519-sha512@openssh.com](mailto:sntrup761x25519-sha512@openssh.com) |
| Message Authentication Codes Allowed | A comma-separated list of Message Authentication Codes allowed for SFTP connections. Leave unset to allow all. Available options are: hmac-md5, hmac-md5-96, hmac-sha1, hmac-sha1-96, [hmac-sha1-etm@openssh.com](mailto:hmac-sha1-etm@openssh.com), hmac-sha2-256, [hmac-sha2-256-etm@openssh.com](mailto:hmac-sha2-256-etm@openssh.com), hmac-sha2-512, [hmac-sha2-512-etm@openssh.com](mailto:hmac-sha2-512-etm@openssh.com) |
| Password | Password for the user account |
| Port | The port that the remote system is listening on for file transfers |
| Private Key Passphrase | Password for the private key |
| Private Key Path | The fully qualified path to the Private Key file |
| Send Keep Alive On Timeout | Send a Keep Alive message every 5 seconds up to 5 times for an overall timeout of 25 seconds. |
| Strict Host Key Checking | Indicates whether or not strict enforcement of hosts keys should be applied |
| Use Compression | Indicates whether or not ZLIB compression should be used when transferring files |
| Username | Username |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | All FlowFiles, for which an existing file could not be deleted, are routed to this relationship |
| not found | All FlowFiles, for which the file to delete did not exist, are routed to this relationship |
| success | All FlowFiles, for which an existing file has been deleted, are routed to this relationship |

Expand

Show lessSee more

## Use cases

| Delete source file only after its processing completed |
| --- |

Expand

Show lessSee more
