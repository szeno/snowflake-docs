# CryptographicHashContent 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Calculates a cryptographic hash value for the flowfile content using the given algorithm and writes it to an output attribute. Please refer to <https://csrc.nist.gov/Projects/Hash-Functions/NIST-Policy-on-Hash-Functions> for help to decide which algorithm to use.

## Tags

blake2, content, cryptography, hash, md5, sha

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| fail\_when\_empty | Route to failure if the content is empty. While hashing an empty value is valid, some flows may want to detect empty input. |
| hash\_algorithm | The hash algorithm to use. Note that not all of the algorithms available are recommended for use (some are provided for legacy compatibility). There are many things to consider when picking an algorithm; it is recommended to use the most secure algorithm possible. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Used for flowfiles that have no content if the ‘fail on empty’ setting is enabled |
| success | Used for flowfiles that have a hash value added |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| content\_<algorithm> | This processor adds an attribute whose value is the result of hashing the flowfile content. The name of this attribute is specified by the value of the algorithm, e.g. ‘content\_SHA-256’. |

Expand

Show lessSee more
