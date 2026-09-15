# LogMessage 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Emits a log message at the specified log level

## Tags

attributes, logging

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| log-level | The Log Level to use when logging the message: [trace, debug, info, warn, error] |
| log-message | The log message to emit |
| log-prefix | Log prefix appended to the log lines. It helps to distinguish the output of multiple LogMessage processors. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | All FlowFiles are routed to this relationship |

Expand

Show lessSee more
