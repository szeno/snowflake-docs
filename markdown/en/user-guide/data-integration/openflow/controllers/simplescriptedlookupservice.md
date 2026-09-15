# SimpleScriptedLookupService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Allows the user to provide a scripted LookupService instance in order to enrich records from an incoming flow file. The script is expected to return an optional string value rather than an arbitrary object (record, e.g.). Also the scripted lookup service should implement StringLookupService, otherwise the getValueType() method must be implemented even though it will be ignored, as SimpleScriptedLookupService returns String as the value type on the script’s behalf.

## Tags

groovy, invoke, lookup, script

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
