# PutRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

The PutRecord processor uses a specified RecordReader to input (possibly multiple) records from an incoming flow file, and sends them to a destination specified by a Record Destination Service (i.e. record sink).

## Tags

put, record, sink

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| put-record-include-zero-record-results | If no records are read from the incoming FlowFile, this property specifies whether or not an empty record set will be transmitted. The original FlowFile will still be routed to success, but if no transmission occurs, no provenance SEND event will be generated. |
| put-record-reader | Specifies the Controller Service to use for reading incoming data |
| put-record-sink | Specifies the Controller Service to use for writing out the query result records to some destination. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | A FlowFile is routed to this relationship if the records could not be transmitted and retrying the operation will also fail |
| retry | The original FlowFile is routed to this relationship if the records could not be transmitted but attempting the operation again may succeed |
| success | The original FlowFile will be routed to this relationship if the records were transmitted successfully |

Expand

Show lessSee more
