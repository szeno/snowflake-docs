# ScanContent 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Scans the content of FlowFiles for terms that are found in a user-supplied dictionary. If a term is matched, the UTF-8 encoded version of the term will be added to the FlowFile using the ‘matching.term’ attribute

## Tags

aho-corasick, byte sequence, content, dictionary, find, scan, search

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Dictionary Encoding | Indicates how the dictionary is encoded. If ‘text’, dictionary terms are new-line delimited and UTF-8 encoded; if ‘binary’, dictionary terms are denoted by a 4-byte integer indicating the term length followed by the term itself |
| Dictionary File | The filename of the terms dictionary |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| matched | FlowFiles that match at least one term in the dictionary are routed to this relationship |
| unmatched | FlowFiles that do not match any term in the dictionary are routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| matching.term | The term that caused the Processor to route the FlowFile to the ‘matched’ relationship; if FlowFile is routed to the ‘unmatched’ relationship, this attribute is not added |

Expand

Show lessSee more
