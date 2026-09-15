# DuplicateFlowFile 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Intended for load testing, this processor will create the configured number of copies of each incoming FlowFile. The original FlowFile as well as all generated copies are sent to the ‘success’ relationship. In addition, each FlowFile gets an attribute ‘copy.index’set to the copy number, where the original FlowFile gets a value of zero, and all copies receive incremented integer values.

## Tags

duplicate, load, test

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Number of Copies | Specifies how many copies of each incoming FlowFile will be made |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | The original FlowFile and all copies will be sent to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| copy.index | A zero-based incrementing integer value based on which copy the FlowFile is. |

Expand

Show lessSee more
