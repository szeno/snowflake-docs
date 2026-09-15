# FilterAttribute 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Filters the attributes of a FlowFile by retaining specified attributes and removing the rest or by removing specified attributes and retaining the rest.

## Tags

Attribute Expression Language, attributes, delete, filter, modification, regex, regular expression, remove, retain

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Attribute Matching Strategy | Specifies the strategy to filter attributes by. |
| Filter Mode | Specifies the strategy to apply on filtered attributes. Either ‘Remove’ or ‘Retain’ only the matching attributes. |
| Filtered Attributes | A set of attribute names to filter from FlowFiles. Each attribute name is separated by the comma delimiter ‘,’. |
| Filtered Attributes Pattern | A regular expression to match names of attributes to filter from FlowFiles. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | All successful FlowFiles are routed to this relationship |

Expand

Show lessSee more

## Use cases

| Retain all FlowFile attributes matching a regular expression |
| --- |
| Remove only a specified set of FlowFile attributes |

Expand

Show lessSee more
