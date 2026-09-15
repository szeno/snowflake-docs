# ListenFTP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Starts an FTP server that listens on the specified port and transforms incoming files into FlowFiles. The URI of the service will be ftp://{hostname}:{port}. The default port is 2221.

## Tags

FTP, FTPS, ingest, listen

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Address | The address the FTP server should be bound to. If not set (or set to 0.0.0.0), the server binds to all available addresses (i.e. all network interfaces of the host machine). |
| Password | If the Username is set, then a password must also be specified. The password provided by the client trying to log in to the FTP server will be checked against this password. |
| Port | The Port to listen on for incoming connections. On Linux, root privileges are required to use port numbers below 1024. |
| SSL Context Service | Specifies the SSL Context Service that can be used to create secure connections. If an SSL Context Service is selected, then a keystore file must also be specified in the SSL Context Service. Without a keystore file, the processor cannot be started successfully. Specifying a truststore file is optional. If a truststore file is specified, client authentication is required (the client needs to send a certificate to the server).Regardless of the selected TLS protocol, the highest available protocol is used for the connection. For example if NiFi is running on Java 11 and TLSv1.2 is selected in the controller service as the preferred TLS Protocol, TLSv1.3 will be used (regardless of TLSv1.2 being selected) because Java 11 supports TLSv1.3. |
| Username | The name of the user that is allowed to log in to the FTP server. If a username is provided, a password must also be provided. If no username is specified, anonymous connections will be permitted. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | Relationship for successfully received files. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| filename | The name of the file received via the FTP/FTPS connection. |
| path | The path pointing to the file’s target directory. E.g.: file.txt is uploaded to /Folder1/SubFolder, then the value of the path attribute will be “/Folder1/SubFolder/” (note that it ends with a separator character). |

Expand

Show lessSee more
