# ModifyBytes 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Discard byte range at the start and end or all content of a binary file.

## Tags

binary, discard, keep

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| End Offset | Number of bytes removed at the end of the file. |
| Remove All Content | Remove all content from the FlowFile superseding Start Offset and End Offset properties. |
| Start Offset | Number of bytes removed at the beginning of the file. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | Processed flowfiles. |

Expand

Show lessSee more
