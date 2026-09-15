# GetFileResource 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

This processor creates FlowFiles with the content of the configured File Resource. GetFileResource is useful for load testing, configuration, and simulation.

## Tags

file, generate, load, test

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| File Resource | Location of the File Resource (Local File or URL). This file will be used as content of the generated FlowFiles. |
| MIME Type | Specifies the value to set for the [mime.type] attribute. |

Expand

Show lessSee more

## Restrictions

| Required Permission | Explanation |
| --- | --- |
| read filesystem | Provides operator the ability to read from any file that NiFi has access to. |
| reference remote resources | File Resource can reference resources over HTTP/HTTPS |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success |  |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | Sets the MIME type of the output if the ‘MIME Type’ property is set |
| Dynamic property key | Value for the corresponding dynamic property, if any is set |

Expand

Show lessSee more
