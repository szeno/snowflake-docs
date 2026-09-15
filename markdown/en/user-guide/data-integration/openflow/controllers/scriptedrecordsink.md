# ScriptedRecordSink

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Allows the user to provide a scripted RecordSinkService instance in order to transmit records to the desired target. The script must set a variable ‘recordSink’ to an implementation of RecordSinkService.

## Tags

groovy, invoke, record, record sink, script

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Module Directory | Module Directory |  |  | Comma-separated list of paths to files and/or directories which contain modules required by the script. |
| Script Body | Script Body |  |  | Body of script to execute. Only one of Script File or Script Body may be used |
| Script Engine \* | Script Engine | Groovy | - Groovy | Language Engine for executing scripts |
| Script File | Script File |  |  | Path to script file to execute. Only one of Script File or Script Body may be used |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

## Restrictions

| Required Permission | Explanation |
| --- | --- |
| execute code | Provides operator the ability to execute arbitrary code assuming all permissions that NiFi has. |

Expand

Show lessSee more

## System Resource Considerations

This component does not specify system resource considerations.
