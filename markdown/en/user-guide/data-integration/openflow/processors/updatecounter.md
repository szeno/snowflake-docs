# UpdateCounter 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

This processor allows users to set specific counters and key points in their flow. It is useful for debugging and basic counting functions.

## Tags

counter, debug, instrumentation

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| counter-name | The name of the counter you want to set the value of - supports expression language like ${counterName} |
| delta | Adjusts the counter by the specified delta for each flow file received. May be a positive or negative integer. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | Counter was updated/retrieved |

Expand

Show lessSee more
