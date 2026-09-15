# FetchSFTP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Fetches the content of a file from a remote SFTP server and overwrites the contents of an incoming FlowFile with the content of the remote file.

## Tags

fetch, files, get, ingest, input, remote, retrieve, sftp, source

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Algorithm Negotiation | Configuration strategy for SSH algorithm negotiation |
| Ciphers Allowed | A comma-separated list of Ciphers allowed for SFTP connections. Leave unset to allow all. Available options are: 3des-cbc, aes128-cbc, aes128-ctr, [aes128-gcm@openssh.com](mailto:aes128-gcm@openssh.com), aes192-cbc, aes192-ctr, aes256-cbc, aes256-ctr, [aes256-gcm@openssh.com](mailto:aes256-gcm@openssh.com), arcfour128, arcfour256, blowfish-cbc, [chacha20-poly1305@openssh.com](mailto:chacha20-poly1305@openssh.com), none |
| Completion Strategy | Specifies what to do with the original file on the server once it has been pulled into NiFi. If the Completion Strategy fails, a warning will be logged but the data will still be transferred. |
| Connection Timeout | Amount of time to wait before timing out while creating a connection |
| Create Directory | Used when ‘Completion Strategy’ is ‘Move File’. Specifies whether or not the remote directory should be created if it does not exist. |
| Data Timeout | When transferring a file between the local and remote system, this value specifies how long is allowed to elapse without any data being transferred between systems |
| Disable Directory Listing | Control how ‘Move Destination Directory’ is created when ‘Completion Strategy’ is ‘Move File’ and ‘Create Directory’ is enabled. If set to ‘true’, directory listing is not performed prior to create missing directories. By default, this processor executes a directory listing command to see target directory existence before creating missing directories. However, there are situations that you might need to disable the directory listing such as the following. Directory listing might fail with some permission setups (e.g. chmod 100) on a directory. Also, if any other SFTP client created the directory after this processor performed a listing and before a directory creation request by this processor is finished, then an error is returned because the directory already exists. |
| Host Key File | If supplied, the given file will be used as the Host Key; otherwise, if ‘Strict Host Key Checking’ property is applied (set to true) then uses the ‘known\_hosts’ and ‘known\_hosts2’ files from ~/.ssh directory else no host key file will be used |
| Hostname | The fully-qualified hostname or IP address of the host to fetch the data from |
| Key Algorithms Allowed | A comma-separated list of Key Algorithms allowed for SFTP connections. Leave unset to allow all. Available options are: ecdsa-sha2-nistp256, [ecdsa-sha2-nistp256-cert-v01@openssh.com](mailto:ecdsa-sha2-nistp256-cert-v01@openssh.com), ecdsa-sha2-nistp384, [ecdsa-sha2-nistp384-cert-v01@openssh.com](mailto:ecdsa-sha2-nistp384-cert-v01@openssh.com), ecdsa-sha2-nistp521, [ecdsa-sha2-nistp521-cert-v01@openssh.com](mailto:ecdsa-sha2-nistp521-cert-v01@openssh.com), rsa-sha2-256, [rsa-sha2-256-cert-v01@openssh.com](mailto:rsa-sha2-256-cert-v01@openssh.com), rsa-sha2-512, [rsa-sha2-512-cert-v01@openssh.com](mailto:rsa-sha2-512-cert-v01@openssh.com), [sk-ecdsa-sha2-nistp256@openssh.com](mailto:sk-ecdsa-sha2-nistp256@openssh.com), [sk-ssh-ed25519@openssh.com](mailto:sk-ssh-ed25519@openssh.com), ssh-dss, [ssh-dss-cert-v01@openssh.com](mailto:ssh-dss-cert-v01@openssh.com), ssh-ed25519, [ssh-ed25519-cert-v01@openssh.com](mailto:ssh-ed25519-cert-v01@openssh.com), ssh-rsa, [ssh-rsa-cert-v01@openssh.com](mailto:ssh-rsa-cert-v01@openssh.com) |
| Key Exchange Algorithms Allowed | A comma-separated list of Key Exchange Algorithms allowed for SFTP connections. Leave unset to allow all. Available options are: curve25519-sha256, [curve25519-sha256@libssh.org](mailto:curve25519-sha256@libssh.org), curve448-sha512, diffie-hellman-group-exchange-sha1, diffie-hellman-group-exchange-sha256, diffie-hellman-group1-sha1, diffie-hellman-group14-sha1, diffie-hellman-group14-sha256, diffie-hellman-group15-sha512, diffie-hellman-group16-sha512, diffie-hellman-group17-sha512, diffie-hellman-group18-sha512, ecdh-sha2-nistp256, ecdh-sha2-nistp384, ecdh-sha2-nistp521, mlkem1024nistp384-sha384, mlkem768nistp256-sha256, mlkem768x25519-sha256, sntrup761x25519-sha512, [sntrup761x25519-sha512@openssh.com](mailto:sntrup761x25519-sha512@openssh.com) |
| Log Level When File Not Found | Log level to use in case the file does not exist when the processor is triggered |
| Message Authentication Codes Allowed | A comma-separated list of Message Authentication Codes allowed for SFTP connections. Leave unset to allow all. Available options are: hmac-md5, hmac-md5-96, hmac-sha1, hmac-sha1-96, [hmac-sha1-etm@openssh.com](mailto:hmac-sha1-etm@openssh.com), hmac-sha2-256, [hmac-sha2-256-etm@openssh.com](mailto:hmac-sha2-256-etm@openssh.com), hmac-sha2-512, [hmac-sha2-512-etm@openssh.com](mailto:hmac-sha2-512-etm@openssh.com) |
| Move Destination Directory | The directory on the remote server to move the original file to once it has been ingested into NiFi. This property is ignored unless the Completion Strategy is set to ‘Move File’. The specified directory must already exist on the remote system if ‘Create Directory’ is disabled, or the rename will fail. |
| Password | Password for the user account |
| Port | The port to connect to on the remote host to fetch the data from |
| Private Key Passphrase | Password for the private key |
| Private Key Path | The fully qualified path to the Private Key file |
| Remote File | The fully qualified filename on the remote system |
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
| comms.failure | Any FlowFile that could not be fetched from the remote server due to a communications failure will be transferred to this Relationship. |
| not.found | Any FlowFile for which we receive a ‘Not Found’ message from the remote server will be transferred to this Relationship. |
| permission.denied | Any FlowFile that could not be fetched from the remote server due to insufficient permissions will be transferred to this Relationship. |
| success | All FlowFiles that are received are routed to success |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| sftp.remote.host | The hostname or IP address from which the file was pulled |
| sftp.remote.port | The port that was used to communicate with the remote SFTP server |
| sftp.remote.filename | The name of the remote file that was pulled |
| filename | The filename is updated to point to the filename fo the remote file |
| path | If the Remote File contains a directory name, that directory name will be added to the FlowFile using the ‘path’ attribute |
| fetch.failure.reason | The name of the failure relationship applied when routing to any failure relationship |

Expand

Show lessSee more

## Use Cases Involving Other Components

| Retrieve all files in a directory of an SFTP Server |
| --- |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.GetFTP](/user-guide/data-integration/openflow/processors/getftp)
- [org.apache.nifi.processors.standard.GetSFTP](/user-guide/data-integration/openflow/processors/getsftp)
- [org.apache.nifi.processors.standard.PutFTP](/user-guide/data-integration/openflow/processors/putftp)
- [org.apache.nifi.processors.standard.PutSFTP](/user-guide/data-integration/openflow/processors/putsftp)
