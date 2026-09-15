# ReplaceTextWithMapping 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Updates the content of a FlowFile by evaluating a Regular Expression against it and replacing the section of the content that matches the Regular Expression with some alternate value provided in a mapping file.

## Tags

Change, Mapping, Modify, Regex, Regular Expression, Replace, Text, Update

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Character Set | The Character Set in which the file is encoded |
| Mapping File | The name of the file (including the full path) containing the Mappings. |
| Mapping File Refresh Interval | The polling interval to check for updates to the mapping file. The default is 60s. |
| Matching Group | The number of the matching group of the provided regex to replace with the corresponding value from the mapping file (if it exists). |
| Maximum Buffer Size | Specifies the maximum amount of data to buffer (per file) in order to apply the regular expressions. If a FlowFile is larger than this value, the FlowFile will be routed to ‘failure’ |
| Regular Expression | The Regular Expression to search for in the FlowFile content |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that could not be updated are routed to this relationship |
| success | FlowFiles that have been successfully updated are routed to this relationship, as well as FlowFiles whose content does not match the given Regular Expression |

Expand

Show lessSee more
