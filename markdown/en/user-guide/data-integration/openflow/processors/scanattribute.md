# ScanAttribute 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Scans the specified attributes of FlowFiles, checking to see if any of their values are present within the specified dictionary of terms

## Tags

attributes, find, lookup, scan, search, text

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Attribute Pattern | Regular Expression that specifies the names of attributes whose values will be matched against the terms in the dictionary |
| Dictionary File | A new-line-delimited text file that includes the terms that should trigger a match. Empty lines are ignored. The contents of the text file are loaded into memory when the processor is scheduled and reloaded when the contents are modified. |
| Dictionary Filter Pattern | A Regular Expression that will be applied to each line in the dictionary file. If the regular expression does not match the line, the line will not be included in the list of terms to search for. If a Matching Group is specified, only the portion of the term that matches that Matching Group will be used instead of the entire term. If not specified, all terms in the dictionary will be used and each term will consist of the text of the entire line in the file |
| Match Criteria | If set to All Must Match, then FlowFiles will be routed to ‘matched’ only if all specified attributes ‘values are found in the dictionary. If set to At Least 1 Must Match, FlowFiles will be routed to’ matched’ if any attribute specified is found in the dictionary |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| matched | FlowFiles whose attributes are found in the dictionary will be routed to this relationship |
| unmatched | FlowFiles whose attributes are not found in the dictionary will be routed to this relationship |

Expand

Show lessSee more
