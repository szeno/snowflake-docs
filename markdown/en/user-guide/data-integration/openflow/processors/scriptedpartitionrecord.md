# ScriptedPartitionRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-scripting-nar

## Description

Receives Record-oriented data (i.e., data that can be read by the configured Record Reader) and evaluates the user provided script against each record in the incoming flow file. Each record is then grouped with other records sharing the same partition and a FlowFile is created for each groups of records. Two records shares the same partition if the evaluation of the script results the same return value for both. Those will be considered as part of the same partition.

## Tags

groovy, group, organize, partition, record, script, segment, split

## Input Requirement

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
| failure | If a FlowFile cannot be partitioned from the configured input format to the configured output format, the unchanged FlowFile will be routed to this relationship |
| original | Once all records in an incoming FlowFile have been partitioned, the original FlowFile is routed to this relationship. |
| success | FlowFiles that are successfully partitioned will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| partition | The partition of the outgoing flow file. If the script indicates that the partition has a null value, the attribute will be set to the literal string “<null partition>” (without quotes). Otherwise, the attribute is set to the String representation of whatever value is returned by the script. |
| mime.type | Sets the mime.type attribute to the MIME Type specified by the Record Writer |
| record.count | The number of records within the flow file. |
| record.error.message | This attribute provides on failure the error message encountered by the Reader or Writer. |
| fragment.index | A one-up number that indicates the ordering of the partitioned FlowFiles that were created from a single parent FlowFile |
| fragment.count | The number of partitioned FlowFiles generated from the parent FlowFile |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.script.ScriptedFilterRecord](/user-guide/data-integration/openflow/processors/scriptedfilterrecord)
- [org.apache.nifi.processors.script.ScriptedTransformRecord](/user-guide/data-integration/openflow/processors/scriptedtransformrecord)
- [org.apache.nifi.processors.script.ScriptedValidateRecord](/user-guide/data-integration/openflow/processors/scriptedvalidaterecord)
