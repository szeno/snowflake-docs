# EncodeContent 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Encode or decode the contents of a FlowFile using Base64, Base32, or hex encoding schemes

## Tags

base32, base64, decode, encode, hex

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Encoded Line Length | Each line of encoded data will contain up to the configured number of characters, rounded down to the nearest multiple of 4. |
| Encoding | Specifies the type of encoding used. |
| Line Output Mode | Controls the line formatting for encoded content based on selected property values. |
| Mode | Specifies whether the content should be encoded or decoded. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Any FlowFile that cannot be encoded or decoded will be routed to failure |
| success | Any FlowFile that is successfully encoded or decoded will be routed to success |

Expand

Show lessSee more
