# ScriptedTransformRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-scripting-nar

## Description

Provides the ability to evaluate a simple script against each record in an incoming FlowFile. The script may transform the record in some way, filter the record, or fork additional records. See Processor’s Additional Details for more information.

## Tags

filter, groovy, modify, record, script, transform, update

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Module Directory | Comma-separated list of paths to files and/or directories which contain modules required by the script. |
| Record Reader | The Record Reader to use parsing the incoming FlowFile into Records |
| Record Writer | The Record Writer to use for serializing Records after they have been transformed |
| Script Body | Body of script to execute. Only one of Script File or Script Body may be used |
| Script Engine | The Language to use for the script |
| Script File | Path to script file to execute. Only one of Script File or Script Body may be used |

Expand

Show lessSee more

## Restrictions

| Required Permission | Explanation |
| --- | --- |
| execute code | Provides operator the ability to execute arbitrary code assuming all permissions that NiFi has. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Any FlowFile that cannot be transformed will be routed to this Relationship |
| success | Each FlowFile that were successfully transformed will be routed to this Relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | Sets the mime.type attribute to the MIME Type specified by the Record Writer |
| record.count | The number of records in the FlowFile |
| record.error.message | This attribute provides on failure the error message encountered by the Reader or Writer. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.jolt.JoltTransformRecord](/user-guide/data-integration/openflow/processors/jolttransformrecord)
- [org.apache.nifi.processors.script.ExecuteScript](/user-guide/data-integration/openflow/processors/executescript)
- [org.apache.nifi.processors.standard.LookupRecord](/user-guide/data-integration/openflow/processors/lookuprecord)
- [org.apache.nifi.processors.standard.QueryRecord](/user-guide/data-integration/openflow/processors/queryrecord)
- [org.apache.nifi.processors.standard.UpdateRecord](/user-guide/data-integration/openflow/processors/updaterecord)
