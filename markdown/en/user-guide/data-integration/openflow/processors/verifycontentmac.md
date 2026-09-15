# VerifyContentMAC 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-cipher-nar

## Description

Calculates a Message Authentication Code using the provided Secret Key and compares it with the provided MAC property

## Tags

Authentication, HMAC, MAC, Signing

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Message Authentication Code | The MAC to compare with the calculated value |
| Message Authentication Code Algorithm | Hashed Message Authentication Code Function |
| Message Authentication Code Encoding | Encoding of the Message Authentication Code |
| Secret Key | Secret key to calculate the hash |
| Secret Key Encoding | Encoding of the Secret Key |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Signature Verification Failed |
| success | Signature Verification Succeeded |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mac.calculated | Calculated Message Authentication Code encoded by the selected encoding |
| mac.encoding | The Encoding of the Hashed Message Authentication Code |
| mac.algorithm | Hashed Message Authentication Code Algorithm |

Expand

Show lessSee more
