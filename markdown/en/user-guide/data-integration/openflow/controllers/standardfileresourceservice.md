# StandardFileResourceService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a file resource for other components. The file needs to be available locally by Nifi (e.g. local disk or mounted storage). NiFi needs to have read permission to the file.

## Tags

file, resource

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| File Path \* | file-path | ${absolute.path}/${filename} |  | Path to a file that can be accessed locally. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

## Restrictions

| Required Permission | Explanation |
| --- | --- |
| read filesystem | Provides operator the ability to read from any file that NiFi has access to. |

Expand

Show lessSee more

## System Resource Considerations

This component does not specify system resource considerations.
