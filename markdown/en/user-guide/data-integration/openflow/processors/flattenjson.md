# FlattenJson 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Provides the user with the ability to take a nested JSON document and flatten it into a simple key/value pair document. The keys are combined at each level with a user-defined separator that defaults to ‘.’. This Processor also lets you unflatten the flattened JSON. It supports four kinds of flatten mode such as normal, keep-arrays, dot notation for MongoDB query and keep-primitive-arrays. Default flatten mode is ‘keep-arrays’.

## Tags

flatten, json, unflatten

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| flatten-json-character-set | The Character Set in which file is encoded |
| flatten-json-pretty-print-json | Specifies whether or not resulted json should be pretty printed |
| flatten-json-return-type | Specifies the desired return type of json such as flatten/unflatten |
| flatten-json-separator | The separator character used for joining keys. Must be a JSON-legal character. |
| flatten-mode | Specifies how json should be flattened/unflattened |
| ignore-reserved-characters | If true, reserved characters in keys will be ignored |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Files that cannot be flattened/unflattened go to this relationship. |
| success | Successfully flattened/unflattened files go to this relationship. |

Expand

Show lessSee more
