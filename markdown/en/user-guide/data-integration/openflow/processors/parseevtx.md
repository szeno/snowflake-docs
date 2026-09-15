# ParseEvtx 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-evtx-nar

## Description

Parses the contents of a Windows Event Log file (evtx) and writes the resulting XML to the FlowFile

## Tags

event, evtx, file, logs, message, windows

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Granularity | Output flow file for each Record, Chunk, or File encountered in the event log |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| bad chunk | Any bad chunks of records will be transferred to this relationship in their original binary form |
| failure | Any FlowFile that encountered an exception during conversion will be transferred to this relationship with as much parsing as possible done |
| original | The unmodified input FlowFile will be transferred to this relationship |
| success | Any FlowFile that was successfully converted from evtx to XML |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| filename | The output filename |
| mime.type | The output filetype (application/xml for success and failure relationships, original value for bad chunk and original relationships) |

Expand

Show lessSee more
